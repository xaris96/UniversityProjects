df, problems_dict = load_data()
X, y, w, groups = build_dataset(df, problems_dict)

print(f"Samples: {len(X)} | Features: {X.shape[1]}")

# Exactly 3 classical ML methods + 1 neural network method
MODELS_TO_TUNE = ["XGBoost", "RandomForest", "ExtraTrees", "MLP"]

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
        FEATURE_SELECTION_TOPK = 12
    else:
        TRIALS_RF = 3
        TRIALS_ET = 3
        TRIALS_XGB = 14 if COMPETITION_MODE else 12
        TRIALS_MLP = 3
        TUNE_SPLITS = 3
        FINAL_SPLITS = 5
        PERM_REPEATS = 2
        PERM_SAMPLES = 1500
        FEATURE_SELECTION_TOPK = 12
else:
    TRIALS_RF = 8
    TRIALS_ET = 8
    TRIALS_XGB = 24
    TRIALS_MLP = 10
    TUNE_SPLITS = 3
    FINAL_SPLITS = 5
    PERM_REPEATS = 4
    PERM_SAMPLES = 2500
    FEATURE_SELECTION_TOPK = 28

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
print(f"Competition mode: {COMPETITION_MODE}")

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

selected_features = X.columns.tolist()
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

results = []
best_params = {}

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
        # Deterministic anchor candidates discovered to work well with top-12 features.
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
    best_params[name] = best

res_df = (
    pd.DataFrame(results, columns=["Model", "CV_MAE", "CV_RMSE", "CV_R2", "Best_Params"])
    .sort_values("CV_MAE")
    .reset_index(drop=True)
)

display(res_df)

best_model = str(res_df.iloc[0]["Model"])
best_mae = float(res_df.iloc[0]["CV_MAE"])
print(f"Best model: {best_model} | MAE={best_mae:.6f}")

cfg = MODEL_REGISTRY[best_model]
final_model, final_scaler = train_final_sklearn(
    cfg["build"], best_params[best_model]["params"], X_model, y, w_model, scale=cfg["scale"]
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

