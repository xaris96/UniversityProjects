import json, warnings
warnings.filterwarnings("ignore")

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
USE_GPU = True     # set False if no GPU / CUDA
EARLY_STOPPING_ROUNDS = 20 if FAST_MODE else 40


def load_data():
    df = pd.read_csv("c13k_selections.csv")
    with open("c13k_problems.json", "r") as f:
        problems_dict = json.load(f)
    return df, problems_dict

def safe_div(a, b):
    return float(a / (b + EPS))

def get_gamble_stats(outcomes):
    probs = np.array([o[0] for o in outcomes], dtype=float)
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

def psych_ev(outcomes, alpha=0.88, gamma=0.65):
    probs = np.array([o[0] for o in outcomes], dtype=float)
    pays  = np.array([o[1] for o in outcomes], dtype=float)

    subj_pays = np.sign(pays) * (np.abs(pays) ** alpha)
    probs_clipped = np.clip(probs, EPS, 1.0)
    weighted_probs = np.exp(-(-np.log(probs_clipped)) ** gamma)

    return float(np.sum(weighted_probs * subj_pays))

def prob_B_better_than_A(outA, outB):
    pA = np.array([o[0] for o in outA], dtype=float)
    xA = np.array([o[1] for o in outA], dtype=float)
    pB = np.array([o[0] for o in outB], dtype=float)
    xB = np.array([o[1] for o in outB], dtype=float)

    mat = (xB[:, None] > xA[None, :]).astype(float)
    return float(np.sum((pB[:, None] * pA[None, :]) * mat))

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

            base["EV_Ratio"] = safe_div(sB["EV"], sA["EV"])
            base["SD_Ratio"] = safe_div(sB["SD"], sA["SD"])
            base["Range_Ratio"] = safe_div(sB["Range"], sA["Range"])
            base["P_Gain_Ratio"] = safe_div(sB["P_Gain"], sA["P_Gain"])
            base["P_Loss_Ratio"] = safe_div(sB["P_Loss"], sA["P_Loss"])
            base["Entropy_Ratio"] = safe_div(sB["Entropy"], sA["Entropy"])

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

def clip01(a):
    return np.clip(np.asarray(a, dtype=float), 0, 1)

def metrics(y_true, y_pred):
    y_pred = clip01(y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2

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

def sample_mlp_params(rng):
    if FAST_MODE:
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


def sample_rf_params(rng):
    max_feat_options = ["sqrt", "log2", None, 0.6, 0.8]
    max_feat = max_feat_options[int(rng.randint(len(max_feat_options)))]
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
    max_feat_options = ["sqrt", "log2", None, 0.6, 0.8]
    max_feat = max_feat_options[int(rng.randint(len(max_feat_options)))]
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



def sample_xgb_params(rng):
    if FAST_MODE:
        n_est_options = [700, 1000, 1400, 1800, 2400]
        max_depth_options = [5, 6, 7, 8]
        lr_options = [0.008, 0.01, 0.015, 0.02, 0.03]
    else:
        n_est_options = [1000, 1400, 1800, 2400, 3200]
        max_depth_options = [4, 5, 6, 7, 8, 9]
        lr_options = [0.005, 0.008, 0.01, 0.015, 0.02, 0.03]
    return {
        "n_estimators": int(rng.choice(n_est_options)),
        "max_depth": int(rng.choice(max_depth_options)),
        "learning_rate": float(rng.choice(lr_options)),
        "subsample": float(rng.choice([0.7, 0.8, 0.9, 1.0])),
        "colsample_bytree": float(rng.choice([0.7, 0.8, 0.9, 1.0])),
        "min_child_weight": float(rng.choice([1.0, 2.0, 3.0, 5.0, 8.0, 12.0])),
        "reg_lambda": float(rng.choice([0.3, 1.0, 2.0, 5.0, 10.0])),
        "reg_alpha": float(rng.choice([0.0, 0.05, 0.1, 0.5, 1.0, 2.0])),
        "gamma": float(rng.choice([0.0, 0.05, 0.1, 0.3, 0.8, 1.5])),
    }


def build_xgb(params):
    if xgb is None:
        raise ImportError("xgboost not installed. Run: pip install xgboost")
    base = {
        "random_state": SEED,
        "n_jobs": 1,
        "objective": "reg:squarederror",
        "eval_metric": "mae",
        "tree_method": "hist",
    }
    if USE_GPU:
        base["device"] = "cuda"
    return xgb.XGBRegressor(**base, **params)



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

def plot_feature_importance(feature_names, scores, topk=15, title="Feature importance"):
    if scores is None:
        print("No importance scores available.")
        return

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
    plt.show()

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

df, problems_dict = load_data()
X, y, w, groups = build_dataset(df, problems_dict)

print(f"Samples: {len(X)} | Features: {X.shape[1]}")

# Exactly 3 classical ML methods + 1 neural network method
MODELS_TO_TUNE = ["XGBoost", "RandomForest", "ExtraTrees", "MLP"]
ENABLE_ENSEMBLE = False

if FAST_MODE:
    TRIALS_RF = 5
    TRIALS_ET = 5
    TRIALS_XGB = 12
    TRIALS_MLP = 6
    TUNE_SPLITS = 3
    FINAL_SPLITS = 5
    PERM_REPEATS = 2
    PERM_SAMPLES = 1500
    FEATURE_SELECTION_TOPK = 18
else:
    TRIALS_RF = 8
    TRIALS_ET = 8
    TRIALS_XGB = 20
    TRIALS_MLP = 10
    TUNE_SPLITS = 3
    FINAL_SPLITS = 5
    PERM_REPEATS = 4
    PERM_SAMPLES = 2500
    FEATURE_SELECTION_TOPK = 24

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

# Feature pruning helps this dataset: many engineered columns are noisy/redundant.
selected_features = X.columns.tolist()
if xgb is not None and FEATURE_SELECTION_TOPK < X.shape[1]:
    selector_params = {
        "n_estimators": 1400,
        "max_depth": 6,
        "learning_rate": 0.03,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 5.0,
        "reg_lambda": 5.0,
        "reg_alpha": 0.1,
        "gamma": 0.3,
    }
    selector = build_xgb(selector_params)
    selector = fit_with_weights(selector, X.values, y, w)
    imp = np.asarray(getattr(selector, "feature_importances_", np.ones(X.shape[1])), dtype=float)
    order = np.argsort(imp)[::-1]
    topk = max(1, min(FEATURE_SELECTION_TOPK, X.shape[1]))
    selected_features = [X.columns[i] for i in order[:topk]]

X_model = X[selected_features].copy()
print(f"Using {X_model.shape[1]} selected features out of {X.shape[1]}")

X_values = X_model.values
tune_splits = list(GroupKFold(n_splits=TUNE_SPLITS).split(np.zeros(len(y)), y, groups=groups))
final_splits = list(GroupKFold(n_splits=FINAL_SPLITS).split(np.zeros(len(y)), y, groups=groups))

results = []
best_params = {}
oof_preds = {}

for name in MODELS_TO_TUNE:
    cfg = MODEL_REGISTRY[name]
    best = tune_sklearn_model(
        name=name,
        build_fn=cfg["build"],
        sample_fn=cfg["sample"],
        X=X_model, y=y, w=w, groups=groups,
        n_trials=cfg["trials"],
        n_splits=TUNE_SPLITS,
        scale=cfg["scale"],
        splits=tune_splits
    )
    oof = cv_oof_sklearn(
        build_fn=cfg["build"],
        params=best["params"],
        X=X_model, y=y, w=w, groups=groups,
        n_splits=FINAL_SPLITS,
        scale=cfg["scale"],
        splits=final_splits,
        X_values=X_values
    )
    mae, rmse, r2 = metrics(y, oof)
    results.append((name, mae, rmse, r2, best["params"]))
    best_params[name] = best
    oof_preds[name] = oof

if ENABLE_ENSEMBLE:
    ens_candidates = []
    ens_names = [n for n in ["XGBoost", "ExtraTrees", "RandomForest", "MLP"] if n in oof_preds]
    weights = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    for i in range(len(ens_names)):
        for j in range(i + 1, len(ens_names)):
            a = ens_names[i]
            b = ens_names[j]
            for wgt in weights:
                ens = wgt * oof_preds[a] + (1 - wgt) * oof_preds[b]
                mae, rmse, r2 = metrics(y, ens)
                ens_candidates.append((mae, rmse, r2, f"{a}:{wgt:.2f}+{b}:{1-wgt:.2f}"))
    if ens_candidates:
        best_ens = min(ens_candidates, key=lambda x: x[0])
        results.append(("Ensemble_best2", best_ens[0], best_ens[1], best_ens[2], best_ens[3]))

res_df = (
    pd.DataFrame(results, columns=["Model", "CV_MAE", "CV_RMSE", "CV_R2", "Best_Params"])
    .sort_values("CV_MAE")
    .reset_index(drop=True)
)

display(res_df)

valid_df = res_df[~res_df["Model"].str.startswith("Ensemble")].reset_index(drop=True)

best_model = str(valid_df.iloc[0]["Model"])
best_mae = float(valid_df.iloc[0]["CV_MAE"])
print(f"Best model: {best_model} | MAE={best_mae:.6f}")

cfg = MODEL_REGISTRY[best_model]
final_model, final_scaler = train_final_sklearn(
    cfg["build"], best_params[best_model]["params"], X_model, y, w, scale=cfg["scale"]
)

if hasattr(final_model, "feature_importances_"):
    scores = final_model.feature_importances_
    plot_feature_importance(selected_features, scores, topk=15, title=f"{best_model} feature importance")
elif hasattr(final_model, "coef_"):
    scores = np.abs(np.asarray(final_model.coef_).ravel())
    plot_feature_importance(selected_features, scores, topk=15, title=f"{best_model} |coef|")
else:
    scores = permutation_importance_generic(
        final_model, X_model, y, selected_features,
        scaler=final_scaler, is_nn=False, n_repeats=PERM_REPEATS, max_samples=PERM_SAMPLES
    )
    plot_feature_importance(selected_features, scores, topk=15, title=f"Permutation importance ({best_model})")

print(f"Best MAE (CV): {best_mae:.6f}")

