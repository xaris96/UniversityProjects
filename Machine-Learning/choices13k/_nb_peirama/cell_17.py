
# -----------------------------
# 8) Run: compute everything, but DO NOT print inside
# -----------------------------
def run_mode(mode="theory", n_trials=25):
    df, problems_dict = load_data()
    X, y, w, groups = build_dataset(df, problems_dict, mode=mode)

    res_df, oof_preds = cv_eval_models(X, y, w, groups, n_splits=5)

    # tuning
    rng = np.random.RandomState(SEED)
    best = {"mae": 1e9, "std": None, "params": None}
    for _ in range(n_trials):
        params = sample_xgb_params(rng)
        mae_mean, mae_std = xgb_cv_mae_tuned(X, y, w, groups, params)
        if mae_mean < best["mae"]:
            best = {"mae": mae_mean, "std": mae_std, "params": params}

    # train final tuned booster (for feature importance)
    d_all = xgb.DMatrix(X, label=y, weight=w)
    final_params = {
        "objective":"reg:squarederror",
        "eval_metric":"mae",
        "tree_method":"hist",
        "seed":SEED,
        **best["params"]
    }
    final_booster = xgb.train(final_params, d_all, num_boost_round=3000, verbose_eval=False)

    return {
        "mode": mode,
        "X": X, "y": y, "w": w, "groups": groups,
        "cv_table": res_df,
        "oof_default_xgb": clip01(oof_preds["XGBoost (default)"]),
        "best_xgb": best,
        "final_booster": final_booster
    }
