# ==== cell 2 ====
import json, warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from datetime import datetime
import joblib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.inspection import permutation_importance
from sklearn.neural_network import MLPRegressor

try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    from catboost import CatBoostRegressor, Pool
except ImportError:
    CatBoostRegressor = None
    Pool = None

SEED = 42
np.random.seed(SEED)

EPS = 1e-9

FAST_MODE = True   # target <10 min while keeping 3+1 models
QUICK_MODE = True  # set False for more thorough tuning
USE_GPU = False    # CPU by default; avoids repeated GPU fallback overhead
EARLY_STOPPING_ROUNDS = 30 if FAST_MODE else 50
WEIGHT_MODE = "sqrt"  # "sqrt" usually gives better MAE than raw uncertainty weights



# ==== cell 5 ====
def load_data():
    df = pd.read_csv("c13k_selections.csv")
    with open("c13k_problems.json", "r") as f:
        problems_dict = json.load(f)
    return df, problems_dict

def safe_div(a, b):
    return float(a / (b + EPS))


def soft_ratio(a, b, scale=1.0):
    return float(a / (abs(b) + scale))


# ==== cell 7 ====
def get_gamble_stats(outcomes):
    probs = np.array([o[0] for o in outcomes], dtype=float)
    probs = probs / (probs.sum() + EPS)
    pays  = np.array([o[1] for o in outcomes], dtype=float)

    ev = float(np.sum(probs * pays))
    var = float(np.sum(probs * (pays - ev) ** 2))
    sd = float(np.sqrt(var))

    mn = float(np.min(pays))
    mx = float(np.max(pays))
    rng = float(mx - mn)

    p_gain = float(np.sum(probs[pays > 0])) if np.any(pays > 0) else 0.0
    p_loss = float(np.sum(probs[pays < 0])) if np.any(pays < 0) else 0.0
    p_zero = float(np.sum(probs[pays == 0])) if np.any(pays == 0) else 0.0

    ev_gain = float(np.sum(probs[pays > 0] * pays[pays > 0])) if np.any(pays > 0) else 0.0
    ev_loss = float(np.sum(probs[pays < 0] * pays[pays < 0])) if np.any(pays < 0) else 0.0

    mean_gain = safe_div(ev_gain, p_gain) if p_gain > 0 else 0.0
    mean_loss = safe_div(ev_loss, p_loss) if p_loss > 0 else 0.0

    abs_pays = np.abs(pays)
    mean_abs = float(np.sum(probs * abs_pays))
    max_gain = float(np.max(pays[pays > 0])) if np.any(pays > 0) else 0.0
    max_loss = float(np.min(pays[pays < 0])) if np.any(pays < 0) else 0.0

    if sd > 0:
        z = (pays - ev) / sd
        skew = float(np.sum(probs * z**3))
        kurt = float(np.sum(probs * z**4))
    else:
        skew = 0.0
        kurt = 0.0

    pclip = np.clip(probs, EPS, 1.0)
    ent = float(-np.sum(pclip * np.log(pclip)))

    return {
        "EV": ev,
        "SD": sd,
        "Var": var,
        "Min": mn,
        "Max": mx,
        "Range": rng,
        "P_Gain": p_gain,
        "P_Loss": p_loss,
        "P_Zero": p_zero,
        "EV_Gain": ev_gain,
        "EV_Loss": ev_loss,
        "Mean_Gain": mean_gain,
        "Mean_Loss": mean_loss,
        "Mean_Abs": mean_abs,
        "Max_Gain": max_gain,
        "Max_Loss": max_loss,
        "Skew": skew,
        "Kurt": kurt,
        "Entropy": ent,
        "Num_Out": float(len(outcomes)),
    }


# ==== cell 9 ====
def psych_ev(outcomes, alpha=0.88, gamma=0.65):
    probs = np.array([o[0] for o in outcomes], dtype=float)
    probs = probs / (probs.sum() + EPS)
    pays  = np.array([o[1] for o in outcomes], dtype=float)

    subj_pays = np.sign(pays) * (np.abs(pays) ** alpha)
    probs_clipped = np.clip(probs, EPS, 1.0)
    weighted_probs = np.exp(-(-np.log(probs_clipped)) ** gamma)

    return float(np.sum(weighted_probs * subj_pays))

def prob_B_better_than_A(outA, outB):
    pA = np.array([o[0] for o in outA], dtype=float)
    pA = pA / (pA.sum() + EPS)
    xA = np.array([o[1] for o in outA], dtype=float)
    pB = np.array([o[0] for o in outB], dtype=float)
    pB = pB / (pB.sum() + EPS)
    xB = np.array([o[1] for o in outB], dtype=float)

    mat = (xB[:, None] > xA[None, :]).astype(float)
    return float(np.sum((pB[:, None] * pA[None, :]) * mat))


# ==== cell 13 ====
def build_dataset(df, problems_dict):
    raw_cols = ["Ha","La","pHa","Hb","Lb","pHb"]
    have_raw = all(c in df.columns for c in raw_cols)
    have_std = "bRate_std" in df.columns
    has_n = "n" in df.columns

    feats, y, w, groups = [], [], [], []

    stat_keys = [
        "EV","SD","Var","Min","Max","Range",
        "P_Gain","P_Loss","P_Zero",
        "EV_Gain","EV_Loss","Mean_Gain","Mean_Loss",
        "Mean_Abs","Max_Gain","Max_Loss",
        "Skew","Kurt","Entropy","Num_Out"
    ]

    problem_cache = {}

    for row in df.itertuples(index=False):
        pid = str(row.Problem)
        base = problem_cache.get(pid)
        if base is None:
            prob = problems_dict.get(pid)
            if prob is None:
                continue

            outA = prob["A"]
            outB = prob["B"]

            sA = get_gamble_stats(outA)
            sB = get_gamble_stats(outB)

            peA = psych_ev(outA)
            peB = psych_ev(outB)
            peA2 = psych_ev(outA, alpha=0.70, gamma=0.90)
            peB2 = psych_ev(outB, alpha=0.70, gamma=0.90)

            base = {}
            for k in stat_keys:
                base[f"{k}_A"] = sA[k]
                base[f"{k}_B"] = sB[k]
                base[f"{k}_Diff"] = sB[k] - sA[k]

            base["Psych_EV_A"] = peA
            base["Psych_EV_B"] = peB
            base["Psych_EV_Diff"] = peB - peA

            base["Psych_EV2_A"] = peA2
            base["Psych_EV2_B"] = peB2
            base["Psych_EV2_Diff"] = peB2 - peA2

            base["CV_A"] = safe_div(sA["SD"], abs(sA["EV"]) + 1e-6)
            base["CV_B"] = safe_div(sB["SD"], abs(sB["EV"]) + 1e-6)
            base["CV_Diff"] = base["CV_B"] - base["CV_A"]

            base["EV_Ratio"] = soft_ratio(sB["EV"], sA["EV"], scale=1.0)
            base["SD_Ratio"] = soft_ratio(sB["SD"], sA["SD"], scale=1.0)
            base["Range_Ratio"] = soft_ratio(sB["Range"], sA["Range"], scale=1.0)
            base["P_Gain_Ratio"] = soft_ratio(sB["P_Gain"], sA["P_Gain"], scale=1.0)
            base["P_Loss_Ratio"] = soft_ratio(sB["P_Loss"], sA["P_Loss"], scale=1.0)
            base["Entropy_Ratio"] = soft_ratio(sB["Entropy"], sA["Entropy"], scale=1.0)

            base["P_B_better_A"] = prob_B_better_than_A(outA, outB)

            problem_cache[pid] = base

        rec = base.copy()

        rec.update({
            "Amb": int(bool(row.Amb)),
            "Corr": int(row.Corr),
            "Feedback": int(bool(row.Feedback)),
            "LotShapeB": int(row.LotShapeB),
            "LotNumB": int(row.LotNumB),
            "Block": int(row.Block),
        })

        if have_raw:
            rec.update({
                "Ha": float(row.Ha),
                "La": float(row.La),
                "pHa": float(row.pHa),
                "Hb": float(row.Hb),
                "Lb": float(row.Lb),
                "pHb": float(row.pHb),
            })
            rec["EV_A_raw"] = float(row.pHa * row.Ha + (1 - row.pHa) * row.La)
            rec["EV_B_raw"] = float(row.pHb * row.Hb + (1 - row.pHb) * row.Lb)
            rec["EV_raw_Diff"] = rec["EV_B_raw"] - rec["EV_A_raw"]

        rec["Amb_x_SD_Diff"] = rec["Amb"] * rec["SD_Diff"]
        rec["Feedback_x_EV_Diff"] = rec["Feedback"] * rec["EV_Diff"]
        rec["Amb_x_Range_Diff"] = rec["Amb"] * rec["Range_Diff"]
        rec["Feedback_x_PGain_Diff"] = rec["Feedback"] * rec["P_Gain_Diff"]

        rec["EV_Diff_Abs"] = abs(rec["EV_Diff"])
        rec["SD_Diff_Abs"] = abs(rec["SD_Diff"])
        rec["Entropy_Diff_Abs"] = abs(rec["Entropy_Diff"])
        rec["Psych_EV_Diff_Abs"] = abs(rec["Psych_EV_Diff"])

        n = float(row.n) if has_n else 1.0
        if have_std:
            std = float(row.bRate_std)
            noise_factor = 1.0 / (std*std + 1e-4)
            noise_factor = min(noise_factor, 50.0)
            w.append(n * noise_factor)
        else:
            w.append(n)

        feats.append(rec)
        y.append(float(row.bRate))
        groups.append(pid)

    X = pd.DataFrame(feats)
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    y = np.array(y, dtype=float)
    w = np.array(w, dtype=float)
    groups = np.array(groups)
    return X, y, w, groups


# ==== cell 15 ====
def clip01(a):
    return np.clip(np.asarray(a, dtype=float), 0, 1)

def metrics(y_true, y_pred):
    y_pred = clip01(y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2


# ==== cell 19 ====
def _is_gpu_error(err):
    msg = str(err).lower()
    return "cuda" in msg or "gpu" in msg

def _xgb_fit_compat(model, X, y, fit_kwargs, sample_weight):
    try:
        model.fit(X, y, **fit_kwargs)
        return model
    except TypeError as e:
        msg = str(e)
        if "early_stopping_rounds" in msg:
            fit_kwargs.pop("early_stopping_rounds", None)
            try:
                model.fit(X, y, **fit_kwargs)
                return model
            except TypeError:
                pass
        if "sample_weight_eval_set" in msg:
            fit_kwargs.pop("sample_weight_eval_set", None)
            try:
                model.fit(X, y, **fit_kwargs)
                return model
            except TypeError:
                pass
        fit_kwargs.pop("eval_set", None)
        fit_kwargs.pop("sample_weight_eval_set", None)
        fit_kwargs.pop("early_stopping_rounds", None)
        try:
            model.fit(X, y, **fit_kwargs)
        except TypeError:
            model.fit(X, y, sample_weight=sample_weight)
        return model

def fit_with_weights(model, X, y, sample_weight, X_val=None, y_val=None, val_weight=None):
    module = model.__class__.__module__

    if module.startswith("xgboost"):
        fit_kwargs = {
            "sample_weight": sample_weight,
            "verbose": False
        }
        if X_val is not None and y_val is not None:
            fit_kwargs.update({
                "eval_set": [(X_val, y_val)],
                "early_stopping_rounds": EARLY_STOPPING_ROUNDS
            })
            if val_weight is not None:
                fit_kwargs["sample_weight_eval_set"] = [val_weight]
        try:
            return _xgb_fit_compat(model, X, y, fit_kwargs, sample_weight)
        except Exception as e:
            if _is_gpu_error(e) and USE_GPU:
                params = model.get_params()
                params.pop("device", None)
                params["tree_method"] = "hist"
                model = model.__class__(**params)
                return _xgb_fit_compat(model, X, y, fit_kwargs, sample_weight)
            raise

    if module.startswith("catboost"):
        if Pool is None:
            raise ImportError("catboost not installed. Run: pip install catboost")
        train_pool = Pool(X, y, weight=sample_weight)
        try:
            if X_val is not None and y_val is not None:
                if val_weight is not None:
                    val_pool = Pool(X_val, y_val, weight=val_weight)
                else:
                    val_pool = Pool(X_val, y_val)
                model.fit(
                    train_pool,
                    eval_set=val_pool,
                    use_best_model=True,
                    early_stopping_rounds=EARLY_STOPPING_ROUNDS,
                    verbose=False
                )
            else:
                model.fit(train_pool, verbose=False)
            return model
        except Exception as e:
            if _is_gpu_error(e) and USE_GPU:
                params = model.get_params()
                params["task_type"] = "CPU"
                model = CatBoostRegressor(**params)
                if X_val is not None and y_val is not None:
                    if val_weight is not None:
                        val_pool = Pool(X_val, y_val, weight=val_weight)
                    else:
                        val_pool = Pool(X_val, y_val)
                    model.fit(
                        train_pool,
                        eval_set=val_pool,
                        use_best_model=True,
                        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
                        verbose=False
                    )
                else:
                    model.fit(train_pool, verbose=False)
                return model
            raise

    try:
        model.fit(X, y, sample_weight=sample_weight)
    except TypeError:
        model.fit(X, y)
    return model


# ==== cell 21 ====
def cv_mae_sklearn(build_fn, params, X, y, w, groups, n_splits=3, scale=False, splits=None, X_values=None):
    if X_values is None:
        X_values = X.values

    if splits is None:
        gkf = GroupKFold(n_splits=n_splits)
        splits = list(gkf.split(np.zeros(len(y)), y, groups=groups))

    fold_maes = []

    for tr_i, val_i in splits:
        X_tr = X_values[tr_i]
        X_val = X_values[val_i]
        y_tr, y_val = y[tr_i], y[val_i]
        w_tr = w[tr_i]
        w_val = w[val_i]

        if scale:
            scaler = StandardScaler()
            Xtr_sc = scaler.fit_transform(X_tr)
            Xval_sc = scaler.transform(X_val)
        else:
            Xtr_sc = X_tr
            Xval_sc = X_val

        model = build_fn(params)
        model = fit_with_weights(model, Xtr_sc, y_tr, w_tr, X_val=Xval_sc, y_val=y_val, val_weight=w_val)

        pred = clip01(model.predict(Xval_sc))
        fold_maes.append(mean_absolute_error(y_val, pred))

    return float(np.mean(fold_maes)), float(np.std(fold_maes, ddof=1))

def cv_oof_sklearn(build_fn, params, X, y, w, groups, n_splits=5, scale=False, splits=None, X_values=None):
    if X_values is None:
        X_values = X.values

    if splits is None:
        gkf = GroupKFold(n_splits=n_splits)
        splits = list(gkf.split(np.zeros(len(y)), y, groups=groups))

    oof = np.zeros_like(y, dtype=float)

    for tr_i, val_i in splits:
        X_tr = X_values[tr_i]
        X_val = X_values[val_i]
        y_tr, y_val = y[tr_i], y[val_i]
        w_tr = w[tr_i]
        w_val = w[val_i]

        if scale:
            scaler = StandardScaler()
            Xtr_sc = scaler.fit_transform(X_tr)
            Xval_sc = scaler.transform(X_val)
        else:
            Xtr_sc = X_tr
            Xval_sc = X_val

        model = build_fn(params)
        model = fit_with_weights(model, Xtr_sc, y_tr, w_tr, X_val=Xval_sc, y_val=y_val, val_weight=w_val)
        oof[val_i] = model.predict(Xval_sc)

    return oof


# ==== cell 23 ====
def sample_mlp_params(rng):
    if QUICK_MODE:
        hidden_options = [(32,), (64, 32)]
        max_iters = [120, 180]
    elif FAST_MODE:
        hidden_options = [(64, 32), (128, 64), (128, 64, 32), (256, 128)]
        max_iters = [250, 350]
    else:
        hidden_options = [(64, 32), (128, 64), (128, 64, 32), (256, 128), (256, 128, 64)]
        max_iters = [300, 450, 650]
    return {
        "hidden_layer_sizes": hidden_options[int(rng.randint(len(hidden_options)))],
        "alpha": float(rng.choice([1e-6, 1e-5, 1e-4, 1e-3])),
        "learning_rate_init": float(rng.choice([1e-4, 3e-4, 5e-4, 1e-3, 2e-3])),
        "batch_size": int(rng.choice([32, 64, 128])),
        "max_iter": int(rng.choice(max_iters)),
    }


def build_mlp(params):
    return MLPRegressor(
        random_state=SEED,
        activation="relu",
        solver="adam",
        early_stopping=True,
        n_iter_no_change=12,
        validation_fraction=0.1,
        **params
    )



def _sample_max_features(rng):
    options = ["sqrt", "log2", None, 0.6, 0.8]
    return options[int(rng.randint(len(options)))]

def sample_rf_params(rng):
    max_feat = _sample_max_features(rng)
    if FAST_MODE:
        n_estimators = rng.choice([300, 500, 800, 1200])
        max_depth = rng.choice([None, 10, 14, 18])
    else:
        n_estimators = rng.choice([500, 800, 1200, 1800])
        max_depth = rng.choice([None, 10, 14, 18, 24])
    return {
        "n_estimators": int(n_estimators),
        "max_depth": max_depth,
        "min_samples_leaf": int(rng.choice([1, 2, 3, 4])),
        "max_features": max_feat,
        "bootstrap": bool(rng.choice([True, False])),
    }


def build_rf(params):
    return RandomForestRegressor(
        random_state=SEED,
        n_jobs=1,
        **params
    )


def sample_et_params(rng):
    max_feat = _sample_max_features(rng)
    if FAST_MODE:
        n_estimators = rng.choice([300, 500, 800, 1200])
        max_depth = rng.choice([None, 10, 14, 18])
    else:
        n_estimators = rng.choice([500, 800, 1200, 1800])
        max_depth = rng.choice([None, 10, 14, 18, 24])
    return {
        "n_estimators": int(n_estimators),
        "max_depth": max_depth,
        "min_samples_leaf": int(rng.choice([1, 2, 3, 4])),
        "max_features": max_feat,
    }



def build_et(params):
    return ExtraTreesRegressor(
        random_state=SEED,
        n_jobs=1,
        **params
    )


def sample_gb_params(rng):
    return {
        "n_estimators": int(rng.choice([100, 200, 300])),
        "learning_rate": float(rng.choice([0.03, 0.05, 0.1])),
        "max_depth": int(rng.choice([2, 3, 4])),
        "min_samples_leaf": int(rng.choice([1, 2, 4])),
        "subsample": float(rng.choice([0.8, 1.0])),
    }


def build_gb(params):
    return GradientBoostingRegressor(
        loss="absolute_error",
        random_state=SEED,
        **params
    )


def sample_dt_params(rng):
    return {
        "max_depth": rng.choice([None, 6, 10, 14, 18]),
        "min_samples_leaf": int(rng.choice([1, 2, 4])),
        "min_samples_split": int(rng.choice([2, 5, 10])),
    }


def build_dt(params):
    return DecisionTreeRegressor(random_state=SEED, **params)




# ==== cell 25 ====
def sample_xgb_params(rng):
    if QUICK_MODE:
        n_est_options = [700, 900, 1200]
        max_depth_options = [6, 7, 8]
        lr_options = [0.01, 0.015, 0.02]
    elif FAST_MODE:
        n_est_options = [900, 1200, 1600, 2000]
        max_depth_options = [6, 7, 8]
        lr_options = [0.01, 0.012, 0.015, 0.02]
    else:
        n_est_options = [900, 1200, 1600, 2000, 2600]
        max_depth_options = [4, 5, 6, 7, 8, 9]
        lr_options = [0.008, 0.01, 0.012, 0.015, 0.02]
    return {
        "n_estimators": int(rng.choice(n_est_options)),
        "max_depth": int(rng.choice(max_depth_options)),
        "learning_rate": float(rng.choice(lr_options)),
        "subsample": float(rng.choice([0.75, 0.8, 0.9, 1.0])),
        "colsample_bytree": float(rng.choice([0.75, 0.8, 0.9, 1.0])),
        "min_child_weight": float(rng.choice([2.0, 3.0, 5.0, 8.0])),
        "reg_lambda": float(rng.choice([0.3, 0.5, 1.0, 2.0, 5.0])),
        "reg_alpha": float(rng.choice([0.0, 0.05, 0.1, 0.5, 1.0])),
        "gamma": float(rng.choice([0.0, 0.05, 0.1, 0.3, 0.8])),
    }


def build_xgb(params):
    if xgb is None:
        raise ImportError("xgboost not installed. Run: pip install xgboost")
    base = {
        "random_state": SEED,
        "n_jobs": -1,
        "objective": "reg:pseudohubererror",
        "eval_metric": "mae",
        "tree_method": "hist",
    }
    if USE_GPU:
        base["device"] = "cuda"
    return xgb.XGBRegressor(**base, **params)




# ==== cell 27 ====
def sample_cb_params(rng):
    iters = [400, 600, 800] if FAST_MODE else [600, 800, 1000]
    return {
        "iterations": int(rng.choice(iters)),
        "depth": int(rng.choice([4, 6, 8, 10])),
        "learning_rate": float(rng.choice([0.03, 0.05, 0.08, 0.1])),
        "l2_leaf_reg": float(rng.choice([1.0, 3.0, 5.0, 7.0])),
    }


def build_cb(params):
    if CatBoostRegressor is None:
        raise ImportError("catboost not installed. Run: pip install catboost")
    task_type = "GPU" if USE_GPU else "CPU"
    eval_metric = "RMSE" if USE_GPU else "MAE"
    return CatBoostRegressor(
        loss_function="MAE",
        eval_metric=eval_metric,
        random_seed=SEED,
        thread_count=-1,
        allow_writing_files=False,
        verbose=False,
        task_type=task_type,
        **params
    )



# ==== cell 29 ====
def tune_sklearn_model(name, build_fn, sample_fn, X, y, w, groups, n_trials=20, n_splits=3, scale=False, splits=None):
    rng = np.random.RandomState(SEED)
    best = {"mae": 1e9, "std": None, "params": None}
    X_values = X.values

    for _ in range(n_trials):
        params = sample_fn(rng)
        mae, std = cv_mae_sklearn(
            build_fn, params, X, y, w, groups,
            n_splits=n_splits, scale=scale,
            splits=splits, X_values=X_values
        )
        if mae < best["mae"]:
            best = {"mae": mae, "std": std, "params": params}

    return best

def train_final_sklearn(build_fn, params, X, y, w, scale=False):
    scaler = None
    X_fit = X.values
    if scale:
        scaler = StandardScaler()
        X_fit = scaler.fit_transform(X.values)

    model = build_fn(params)
    # Keep the returned estimator in case fit_with_weights switches backend (e.g., GPU->CPU fallback).
    model = fit_with_weights(model, X_fit, y, w)
    return model, scaler


# ==== cell 31 ====
def plot_feature_importance(feature_names, scores, topk=15, title="Feature importance", save_path=None):
    if scores is None:
        print("No importance scores available.")
        return None

    fi = (
        pd.DataFrame({"Feature": feature_names, "Score": scores})
        .sort_values("Score", ascending=False)
        .head(topk)
    )

    plt.figure(figsize=(9, 5))
    plt.barh(fi["Feature"][::-1], fi["Score"][::-1])
    plt.xlabel("Importance")
    plt.title(title)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    return fi

def permutation_importance_generic(model, X, y, feature_names, scaler=None, is_nn=False, n_repeats=5, max_samples=3000):
    if len(X) > max_samples:
        rng = np.random.RandomState(SEED)
        idx = rng.choice(len(X), size=max_samples, replace=False)
        X_use = X.iloc[idx]
        y_use = y[idx]
    else:
        X_use = X
        y_use = y

    class _Wrapper:
        def __init__(self, model, scaler, is_nn):
            self.model = model
            self.scaler = scaler
            self.is_nn = is_nn

        # sklearn>=1.6 validates that estimators implement fit.
        # This wrapper is inference-only because the underlying model is already trained.
        def fit(self, X_in, y_in=None):
            return self

        def predict(self, X_in):
            Xp = self.scaler.transform(X_in) if self.scaler is not None else X_in
            if self.is_nn:
                return self.model.predict(Xp, verbose=0).ravel()
            return self.model.predict(Xp)

    def neg_mae(estimator, X_in, y_in):
        pred = estimator.predict(X_in)
        return -mean_absolute_error(y_in, clip01(pred))

    wrapper = _Wrapper(model, scaler, is_nn)
    result = permutation_importance(
        wrapper,
        X_use.values,
        y_use,
        scoring=neg_mae,
        n_repeats=n_repeats,
        random_state=SEED
    )
    return result.importances_mean


# ==== cell 36 ====
df, problems_dict = load_data()
X, y, w, groups = build_dataset(df, problems_dict)

print(f"Samples: {len(X)} | Features: {X.shape[1]}")

MODELS_TO_TUNE = ["XGBoost", "RandomForest", "ExtraTrees", "MLP"]


# ==== cell 38 ====
if FAST_MODE:
    if QUICK_MODE:
        TRIALS_RF = 2
        TRIALS_ET = 2
        TRIALS_XGB = 6
        TRIALS_MLP = 2
        TUNE_SPLITS = 2
        FINAL_SPLITS = 3
        PERM_REPEATS = 1
        PERM_SAMPLES = 600
        FEATURE_SELECTION_TOPK = None
    else:
        TRIALS_RF = 3
        TRIALS_ET = 3
        TRIALS_XGB = 12
        TRIALS_MLP = 3
        TUNE_SPLITS = 3
        FINAL_SPLITS = 5
        PERM_REPEATS = 2
        PERM_SAMPLES = 1500
        FEATURE_SELECTION_TOPK = None
else:
    TRIALS_RF = 8
    TRIALS_ET = 8
    TRIALS_XGB = 24
    TRIALS_MLP = 10
    TUNE_SPLITS = 3
    FINAL_SPLITS = 5
    PERM_REPEATS = 4
    PERM_SAMPLES = 2500
    FEATURE_SELECTION_TOPK = None

if WEIGHT_MODE == "none":
    w_model = np.ones_like(w, dtype=float)
elif WEIGHT_MODE == "raw":
    w_model = w.astype(float)
elif WEIGHT_MODE == "sqrt":
    w_model = np.sqrt(np.clip(w, EPS, None))
elif WEIGHT_MODE == "clip10":
    w_model = np.clip(w, 1.0, 10.0)
else:
    raise ValueError("WEIGHT_MODE must be one of: none/raw/sqrt/clip10")

print(
    f"Weight mode: {WEIGHT_MODE} | "
    f"min={w_model.min():.3f}, median={np.median(w_model):.3f}, max={w_model.max():.3f}"
)
print(
    f"Mode: FAST={FAST_MODE}, QUICK={QUICK_MODE} | "
    f"Trials (RF/ET/XGB/MLP) = {TRIALS_RF}/{TRIALS_ET}/{TRIALS_XGB}/{TRIALS_MLP} | "
    f"Splits (tune/final) = {TUNE_SPLITS}/{FINAL_SPLITS}"
)


# ==== cell 40 ====
MODEL_REGISTRY = {
    "RandomForest": {"build": build_rf, "sample": sample_rf_params, "scale": False, "trials": TRIALS_RF},
    "ExtraTrees": {"build": build_et, "sample": sample_et_params, "scale": False, "trials": TRIALS_ET},
    "XGBoost": {"build": build_xgb, "sample": sample_xgb_params, "scale": False, "trials": TRIALS_XGB},
    "MLP": {"build": build_mlp, "sample": sample_mlp_params, "scale": True, "trials": TRIALS_MLP},
}

missing = []
if "XGBoost" in MODELS_TO_TUNE and xgb is None:
    missing.append("xgboost")
if missing:
    raise ImportError("Missing packages: " + ", ".join(missing) + ". Run: pip install " + " ".join(missing))


# ==== cell 43 ====
FEATURE_SET = "compact"  # "compact" or "all"
COMPACT_FEATURES = [
    "EV_raw_Diff",
    "Lb",
    "pHb",
    "EV_B_raw",
    "EV_A_raw",
    "Hb",
    "La",
    "Ha",
    "LotShapeB",
    "LotNumB",
    "Amb",
    "pHa",
    "Block",
    "EV_Diff_Abs",
    "EV_Diff",
    "P_B_better_A",
    "Entropy_Diff_Abs",
    "Num_Out_Diff",
    "Num_Out_B",
    "Amb_x_SD_Diff",
    "Kurt_A",
    "SD_Diff_Abs",
    "Psych_EV_Diff_Abs",
    "Psych_EV2_B",
    "Min_Diff",
    "Entropy_Diff",
    "Entropy_B",
    "EV_A",
    "Mean_Abs_A",
    "EV_B",
    "Feedback",
    "Amb_x_Range_Diff",
]

if FEATURE_SET == "compact":
    selected_features = [f for f in COMPACT_FEATURES if f in X.columns]
else:
    selected_features = X.columns.tolist()

# ==== cell 44 ====
if xgb is not None and FEATURE_SELECTION_TOPK is not None and FEATURE_SELECTION_TOPK < X.shape[1]:
    selector_params = {
        "n_estimators": 900,
        "max_depth": 6,
        "learning_rate": 0.015,
        "subsample": 0.8,
        "colsample_bytree": 1.0,
        "min_child_weight": 2.0,
        "reg_lambda": 1.0,
        "reg_alpha": 2.0,
        "gamma": 0.3,
    }
    selector = build_xgb(selector_params)
    selector = fit_with_weights(selector, X.values, y, w_model)
    imp = np.asarray(getattr(selector, "feature_importances_", np.ones(X.shape[1])), dtype=float)
    order = np.argsort(imp)[::-1]
    topk = max(1, min(FEATURE_SELECTION_TOPK, X.shape[1]))
    selected_features = [X.columns[i] for i in order[:topk]]

X_model = X[selected_features].copy()
print(f"Using {X_model.shape[1]} selected features out of {X.shape[1]}")


# ==== cell 46 ====
from sklearn.model_selection import KFold, GroupKFold

RUN_SWEEP = True
SWEEP_K_LIST = [10, 20, 30, 40, 60]
SWEEP_SPLITS = 5
SWEEP_CV = ["groupkfold", "kfold"]
SWEEP_RANKING = "global"  # "global" (fast) or "foldwise" (slow but leakage-free)
SWEEP_MODEL = "xgb"  # "xgb" or "et"
SWEEP_N_ESTIMATORS = 400
SWEEP_MAX_DEPTH = 6
SWEEP_LEARNING_RATE = 0.05
SWEEP_ET_ESTIMATORS = 200

def _get_splits(strategy):
    if strategy == "groupkfold":
        return list(GroupKFold(n_splits=SWEEP_SPLITS).split(np.zeros(len(y)), y, groups=groups))
    if strategy == "kfold":
        return list(KFold(n_splits=SWEEP_SPLITS, shuffle=True, random_state=SEED).split(X))
    raise ValueError("Unknown strategy")

def _rank_features_global(X_in, y_in, w_in):
    if SWEEP_MODEL == "xgb" and xgb is not None:
        params = {
            "n_estimators": int(SWEEP_N_ESTIMATORS),
            "max_depth": int(SWEEP_MAX_DEPTH),
            "learning_rate": float(SWEEP_LEARNING_RATE),
            "subsample": 0.8,
            "colsample_bytree": 0.9,
            "min_child_weight": 3.0,
            "reg_lambda": 1.0,
            "reg_alpha": 0.0,
            "gamma": 0.0,
        }
        model = build_xgb(params)
        model = fit_with_weights(model, X_in.values, y_in, w_in)
        imp = np.asarray(getattr(model, "feature_importances_", np.ones(X_in.shape[1])), dtype=float)
    else:
        model = ExtraTreesRegressor(
            n_estimators=int(SWEEP_ET_ESTIMATORS),
            max_depth=14,
            min_samples_leaf=2,
            max_features="sqrt",
            random_state=SEED,
            n_jobs=1
        )
        model.fit(X_in.values, y_in, sample_weight=w_in)
        imp = model.feature_importances_
    order = np.argsort(imp)[::-1]
    return order

def _eval_k_global(order, k, splits):
    feats = X.columns[order[:k]]
    Xk = X[feats]
    if SWEEP_MODEL == "xgb" and xgb is not None:
        params = {
            "n_estimators": int(SWEEP_N_ESTIMATORS),
            "max_depth": int(SWEEP_MAX_DEPTH),
            "learning_rate": float(SWEEP_LEARNING_RATE),
            "subsample": 0.8,
            "colsample_bytree": 0.9,
            "min_child_weight": 3.0,
            "reg_lambda": 1.0,
            "reg_alpha": 0.0,
            "gamma": 0.0,
        }
        oof = cv_oof_sklearn(build_xgb, params, Xk, y, w_model, groups, n_splits=SWEEP_SPLITS, scale=False, splits=splits, X_values=Xk.values)
    else:
        params = {
            "n_estimators": int(SWEEP_ET_ESTIMATORS),
            "max_depth": 14,
            "min_samples_leaf": 2,
            "max_features": "sqrt",
        }
        oof = cv_oof_sklearn(build_et, params, Xk, y, w_model, groups, n_splits=SWEEP_SPLITS, scale=False, splits=splits, X_values=Xk.values)
    mae, rmse, r2 = metrics(y, oof)
    return mae, rmse, r2, list(feats)

def _eval_k_foldwise(k, splits):
    oof = np.zeros_like(y, dtype=float)
    for tr_i, val_i in splits:
        order = _rank_features_global(X.iloc[tr_i], y[tr_i], w_model[tr_i])
        feats = X.columns[order[:k]]
        X_tr = X.iloc[tr_i][feats]
        X_val = X.iloc[val_i][feats]
        if SWEEP_MODEL == "xgb" and xgb is not None:
            params = {
                "n_estimators": int(SWEEP_N_ESTIMATORS),
                "max_depth": int(SWEEP_MAX_DEPTH),
                "learning_rate": float(SWEEP_LEARNING_RATE),
                "subsample": 0.8,
                "colsample_bytree": 0.9,
                "min_child_weight": 3.0,
                "reg_lambda": 1.0,
                "reg_alpha": 0.0,
                "gamma": 0.0,
            }
            model = build_xgb(params)
            model = fit_with_weights(model, X_tr.values, y[tr_i], w_model[tr_i], X_val=X_val.values, y_val=y[val_i], val_weight=w_model[val_i])
            oof[val_i] = model.predict(X_val.values)
        else:
            params = {
                "n_estimators": int(SWEEP_ET_ESTIMATORS),
                "max_depth": 14,
                "min_samples_leaf": 2,
                "max_features": "sqrt",
            }
            model = build_et(params)
            model = fit_with_weights(model, X_tr.values, y[tr_i], w_model[tr_i], X_val=X_val.values, y_val=y[val_i], val_weight=w_model[val_i])
            oof[val_i] = model.predict(X_val.values)
    mae, rmse, r2 = metrics(y, oof)
    return mae, rmse, r2

if RUN_SWEEP:
    sweep_rows = []
    for strategy in SWEEP_CV:
        splits = _get_splits(strategy)
        if SWEEP_RANKING == "global":
            order = _rank_features_global(X, y, w_model)
            for k in SWEEP_K_LIST:
                mae, rmse, r2, feats = _eval_k_global(order, k, splits)
                sweep_rows.append({"cv": strategy, "ranking": "global", "k": k, "mae": mae, "rmse": rmse, "r2": r2})
        else:
            for k in SWEEP_K_LIST:
                mae, rmse, r2 = _eval_k_foldwise(k, splits)
                sweep_rows.append({"cv": strategy, "ranking": "foldwise", "k": k, "mae": mae, "rmse": rmse, "r2": r2})

    sweep_df = pd.DataFrame(sweep_rows).sort_values(["cv", "mae"]).reset_index(drop=True)
    display(sweep_df)
    ARTIFACTS_DIR = Path("artifacts")
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    sweep_df.to_csv(ARTIFACTS_DIR / "feature_sweep_results.csv", index=False)
    for strategy in SWEEP_CV:
        sub = sweep_df[sweep_df["cv"] == strategy]
        if len(sub) > 0:
            best = sub.iloc[0]
            print(f"Best for {strategy}: K={int(best['k'])} | MAE={best['mae']:.6f}")

# ==== cell 48 ====
ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)

# Build a per-feature rationale table from feature names
feature_rationale_rules = [
    (r"^EV_", "Expected value related feature (central tendency)."),
    (r"^SD_", "Risk/variability feature (standard deviation)."),
    (r"^Var_", "Dispersion feature (variance)."),
    (r"^Min_", "Worst outcome feature."),
    (r"^Max_", "Best outcome feature."),
    (r"^Range_", "Outcome spread feature."),
    (r"^P_Gain", "Probability of gain feature."),
    (r"^P_Loss", "Probability of loss feature."),
    (r"^P_Zero", "Probability of zero outcome feature."),
    (r"^EV_Gain", "Contribution of gains to EV."),
    (r"^EV_Loss", "Contribution of losses to EV."),
    (r"^Mean_Gain", "Average gain conditional on gain."),
    (r"^Mean_Loss", "Average loss conditional on loss."),
    (r"^Mean_Abs", "Average absolute outcome magnitude."),
    (r"^Max_Gain", "Extreme gain size."),
    (r"^Max_Loss", "Extreme loss size."),
    (r"^Skew", "Asymmetry of outcomes."),
    (r"^Kurt", "Tail heaviness of outcomes."),
    (r"^Entropy", "Uncertainty/complexity of the lottery."),
    (r"^Num_Out", "Number of outcomes (structure)."),
    (r"^Psych_EV", "Subjective value (prospect-style transform)."),
    (r"^CV_", "Risk relative to EV magnitude (SD/|EV|)."),
    (r"^EV_Ratio", "Relative expected value (B vs A)."),
    (r"^SD_Ratio", "Relative risk (B vs A)."),
    (r"^Range_Ratio", "Relative spread (B vs A)."),
    (r"^P_Gain_Ratio", "Relative probability of gain (B vs A)."),
    (r"^P_Loss_Ratio", "Relative probability of loss (B vs A)."),
    (r"^Entropy_Ratio", "Relative uncertainty (B vs A)."),
    (r"^P_B_better_A", "Probability that B payoff exceeds A."),
    (r"^Amb$", "Ambiguity condition indicator."),
    (r"^Corr$", "Correlation condition indicator."),
    (r"^Feedback$", "Feedback condition indicator."),
    (r"^LotShapeB$", "Lottery shape of option B."),
    (r"^LotNumB$", "Number of outcomes in option B."),
    (r"^Block$", "Block index (experimental sequence)."),
    (r"^Ha$|^La$|^pHa$|^Hb$|^Lb$|^pHb$", "Raw lottery parameters (if present)."),
    (r"^EV_A_raw$|^EV_B_raw$|^EV_raw_Diff$", "Raw EV from parameters and its difference."),
    (r"_Diff$", "Difference between B and A for the same statistic."),
    (r"_A$|_B$", "Statistic for option A or B (absolute level)."),
    (r"_Abs$", "Absolute magnitude of the difference (sign removed)."),
    (r"_x_", "Interaction term between design and risk/return."),
]

import re
rows = []
if "selected_features" not in globals():
    if "X_model" in globals():
        selected_features = list(X_model.columns)
    elif "X" in globals():
        selected_features = list(X.columns)
    else:
        raise RuntimeError("selected_features not available yet")
for feat in selected_features:
    rationale = "(no match)"
    for pattern, desc in feature_rationale_rules:
        if re.search(pattern, feat):
            rationale = desc
            break
    rows.append({"feature": feat, "rationale": rationale})

feature_rationale_df = pd.DataFrame(rows)
display(feature_rationale_df)
feature_rationale_df.to_csv(ARTIFACTS_DIR / "feature_rationale_table.csv", index=False)

# ==== cell 50 ====
X_values = X_model.values
tune_splits = list(GroupKFold(n_splits=TUNE_SPLITS).split(np.zeros(len(y)), y, groups=groups))
final_splits = list(GroupKFold(n_splits=FINAL_SPLITS).split(np.zeros(len(y)), y, groups=groups))
XGB_OOF_SEEDS = [SEED] if QUICK_MODE else [SEED, SEED + 1337, SEED + 2024]
print(f"XGBoost OOF seed ensemble: {XGB_OOF_SEEDS}")

def cv_oof_xgb_bagged(params, X_values, y, w, splits, seeds):
    oof = np.zeros_like(y, dtype=float)
    for tr_i, val_i in splits:
        X_tr = X_values[tr_i]
        X_val = X_values[val_i]
        y_tr, y_val = y[tr_i], y[val_i]
        w_tr = w[tr_i]
        w_val = w[val_i]

        pred_sum = np.zeros(len(val_i), dtype=float)
        for rs in seeds:
            model = build_xgb(params)
            try:
                model.set_params(random_state=int(rs))
            except Exception:
                pass
            model = fit_with_weights(model, X_tr, y_tr, w_tr, X_val=X_val, y_val=y_val, val_weight=w_val)
            pred_sum += model.predict(X_val)

        oof[val_i] = pred_sum / float(len(seeds))
    return oof


# ==== cell 52 ====
results = []
best_params = {}
oof_preds = {}

for name in MODELS_TO_TUNE:
    cfg = MODEL_REGISTRY[name]
    best = tune_sklearn_model(
        name=name,
        build_fn=cfg["build"],
        sample_fn=cfg["sample"],
        X=X_model, y=y, w=w_model, groups=groups,
        n_trials=cfg["trials"],
        n_splits=TUNE_SPLITS,
        scale=cfg["scale"],
        splits=tune_splits
    )
    if name == "XGBoost":
        # Anchor candidates from preliminary runs (top-12 features).
        xgb_anchor_params = [
            {
                "n_estimators": 1600,
                "max_depth": 7,
                "learning_rate": 0.012,
                "subsample": 0.75,
                "colsample_bytree": 0.8,
                "min_child_weight": 8.0,
                "reg_lambda": 0.3,
                "reg_alpha": 2.0,
                "gamma": 0.1,
            },
            {
                "n_estimators": 1200,
                "max_depth": 7,
                "learning_rate": 0.012,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "min_child_weight": 2.0,
                "reg_lambda": 2.0,
                "reg_alpha": 0.0,
                "gamma": 0.05,
            },
            {
                "n_estimators": 1200,
                "max_depth": 7,
                "learning_rate": 0.012,
                "subsample": 0.9,
                "colsample_bytree": 0.9,
                "min_child_weight": 3.0,
                "reg_lambda": 2.0,
                "reg_alpha": 1.0,
                "gamma": 0.05,
            },
        ]
        for p in xgb_anchor_params:
            mae_p, std_p = cv_mae_sklearn(
                cfg["build"], p, X_model, y, w_model, groups,
                n_splits=TUNE_SPLITS, scale=cfg["scale"],
                splits=tune_splits, X_values=X_values
            )
            if mae_p < best["mae"]:
                best = {"mae": mae_p, "std": std_p, "params": p}
    if name == "XGBoost":
        oof = cv_oof_xgb_bagged(best["params"], X_values, y, w_model, final_splits, XGB_OOF_SEEDS)
    else:
        oof = cv_oof_sklearn(
            build_fn=cfg["build"],
            params=best["params"],
            X=X_model, y=y, w=w_model, groups=groups,
            n_splits=FINAL_SPLITS,
            scale=cfg["scale"],
            splits=final_splits,
            X_values=X_values
        )
    mae, rmse, r2 = metrics(y, oof)
    results.append((name, mae, rmse, r2, best["params"]))
    oof_preds[name] = oof
    best_params[name] = best

res_df = (
    pd.DataFrame(results, columns=["Model", "CV_MAE", "CV_RMSE", "CV_R2", "Best_Params"])
    .sort_values("CV_MAE")
    .reset_index(drop=True)
)

display(res_df)


# ==== cell 54 ====
best_model = str(res_df.iloc[0]["Model"])
best_mae = float(res_df.iloc[0]["CV_MAE"])
print(f"Best model: {best_model} | MAE={best_mae:.6f}")

# Final training on full data
cfg = MODEL_REGISTRY[best_model]
final_model, final_scaler = train_final_sklearn(
    cfg["build"], best_params[best_model]["params"], X_model, y, w_model, scale=cfg["scale"]
)

# Feature importance plot (saved + displayed)
ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)

fi_save = ARTIFACTS_DIR / f"feature_importance_{best_model.lower()}.png"
if hasattr(final_model, "feature_importances_"):
    scores = final_model.feature_importances_
    fi = plot_feature_importance(selected_features, scores, topk=15, title=f"{best_model} feature importance", save_path=fi_save)
elif hasattr(final_model, "coef_"):
    scores = np.abs(np.asarray(final_model.coef_).ravel())
    fi = plot_feature_importance(selected_features, scores, topk=15, title=f"{best_model} |coef|", save_path=fi_save)
else:
    scores = permutation_importance_generic(
        final_model, X_model, y, selected_features,
        scaler=final_scaler, is_nn=False, n_repeats=PERM_REPEATS, max_samples=PERM_SAMPLES
    )
    fi = plot_feature_importance(selected_features, scores, topk=15, title=f"Permutation importance ({best_model})", save_path=fi_save)


# Save and display top features
if "fi" in locals() and fi is not None:
    display(fi)
    fi.to_csv(ARTIFACTS_DIR / "feature_importance_top15.csv", index=False)

# OOF report and plots
best_oof = oof_preds[best_model]
best_oof = clip01(best_oof)
mae, rmse, r2 = metrics(y, best_oof)
feature_selection_topk = None if FEATURE_SELECTION_TOPK is None else int(FEATURE_SELECTION_TOPK)

plt.figure(figsize=(5.5, 5.5))
plt.scatter(y, best_oof, s=10, alpha=0.5)
plt.plot([0, 1], [0, 1], "k--", linewidth=1)
plt.xlabel("True bRate")
plt.ylabel("OOF Pred")
plt.title(f"OOF Predictions ({best_model})")
plt.tight_layout()
plt.savefig(ARTIFACTS_DIR / "oof_scatter.png", dpi=150, bbox_inches="tight")
plt.show()

errors = best_oof - y
plt.figure(figsize=(6, 4))
plt.hist(errors, bins=40, alpha=0.8)
plt.xlabel("Prediction Error (pred - true)")
plt.ylabel("Count")
plt.title("OOF Error Distribution")
plt.tight_layout()
plt.savefig(ARTIFACTS_DIR / "oof_error_hist.png", dpi=150, bbox_inches="tight")
plt.show()

# Save artifacts
res_df.to_csv(ARTIFACTS_DIR / "cv_results.csv", index=False)

oof_df = pd.DataFrame({"Problem": groups, "y_true": y, "oof_pred": best_oof})
oof_df.to_csv(ARTIFACTS_DIR / "oof_predictions.csv", index=False)

report = {
    "best_model": best_model,
    "cv_mae": float(mae),
    "cv_rmse": float(rmse),
    "cv_r2": float(r2),
    "n_samples": int(len(y)),
    "n_features_total": int(X.shape[1]),
    "n_features_used": int(X_model.shape[1]),
    "weight_mode": WEIGHT_MODE,
    "feature_selection_topk": feature_selection_topk,
    "seed": int(SEED),
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "best_params": best_params[best_model]["params"],
}
with open(ARTIFACTS_DIR / "report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

artifact = {
    "model": final_model,
    "scaler": final_scaler,
    "selected_features": selected_features,
    "best_model": best_model,
    "best_params": best_params[best_model]["params"],
    "weight_mode": WEIGHT_MODE,
    "feature_selection_topk": feature_selection_topk,
    "seed": SEED,
}
joblib.dump(artifact, ARTIFACTS_DIR / "best_model.joblib")

print(f"Artifacts saved in: {ARTIFACTS_DIR.resolve()}")

# ==== cell 57 ====
print(f"Best MAE (CV): {best_mae:.6f}")

