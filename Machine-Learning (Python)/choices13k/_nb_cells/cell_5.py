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

