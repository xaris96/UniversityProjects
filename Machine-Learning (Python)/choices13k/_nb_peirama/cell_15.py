# -----------------------------
# 7) Hyperparameter tuning (XGB random search + GroupKFold)
# -----------------------------
def sample_xgb_params(rng):
    return {
        "max_depth": int(rng.choice([3,4,5,6,7])),
        "min_child_weight": float(rng.choice([1,3,5,8,12])),
        "subsample": float(rng.choice([0.6,0.8,1.0])),
        "colsample_bytree": float(rng.choice([0.6,0.8,1.0])),
        "gamma": float(rng.choice([0.0,0.1,0.3,0.8])),
        "reg_alpha": float(rng.choice([0.0,0.1,0.5,1.0])),
        "reg_lambda": float(rng.choice([0.5,1.0,2.0,5.0])),
        "eta": float(rng.choice([0.01,0.02,0.03,0.05])),
    }

def xgb_cv_mae_tuned(X, y, w, groups, params, n_splits=5, num_boost_round=8000, early_stopping_rounds=200):
    gkf = GroupKFold(n_splits=n_splits)
    fold_maes = []

    for tr_i, val_i in gkf.split(X, y, groups=groups):
        X_tr, X_val = X.iloc[tr_i], X.iloc[val_i]
        y_tr, y_val = y[tr_i], y[val_i]
        w_tr = w[tr_i]

        dtr  = xgb.DMatrix(X_tr,  label=y_tr, weight=w_tr)
        dval = xgb.DMatrix(X_val, label=y_val)

        native_params = {
            "objective": "reg:squarederror",
            "eval_metric": "mae",
            "tree_method": "hist",
            "seed": SEED,
            **params
        }

        booster = xgb.train(
            params=native_params,
            dtrain=dtr,
            num_boost_round=num_boost_round,
            evals=[(dval,"val")],
            early_stopping_rounds=early_stopping_rounds,
            verbose_eval=False
        )

        pred = clip01(booster.predict(dval))
        fold_maes.append(mean_absolute_error(y_val, pred))

    return float(np.mean(fold_maes)), float(np.std(fold_maes, ddof=1))
