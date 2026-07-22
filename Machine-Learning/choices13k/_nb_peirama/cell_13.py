

# -----------------------------
# 6) GroupKFold CV evaluation (returns OOF preds)
# -----------------------------
def cv_eval_models(X, y, w, groups, n_splits=5):
    gkf = GroupKFold(n_splits=n_splits)

    results = []
    oof_preds = {}

    base_oof = np.zeros_like(y, dtype=float)

    model_defs = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=400, max_depth=15, min_samples_leaf=4, random_state=SEED, n_jobs=-1),
        "ExtraTrees": ExtraTreesRegressor(n_estimators=400, max_depth=15, min_samples_leaf=4, random_state=SEED, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, loss="absolute_error", random_state=SEED),
        "NeuralNet": None,
        "XGBoost (default)": "xgb_default"
    }

    for name in model_defs.keys():
        oof_preds[name] = np.zeros_like(y, dtype=float)

    for tr_i, val_i in gkf.split(X, y, groups=groups):
        X_tr, X_val = X.iloc[tr_i], X.iloc[val_i]
        y_tr, y_val = y[tr_i], y[val_i]
        w_tr = w[tr_i]

        # baseline
        mu = float(np.average(y_tr, weights=w_tr))
        base_oof[val_i] = mu

        # scale for LR/NN
        scaler = StandardScaler()
        Xtr_sc = scaler.fit_transform(X_tr.values)
        Xval_sc = scaler.transform(X_val.values)

        # Linear
        lr = LinearRegression()
        lr.fit(Xtr_sc, y_tr, sample_weight=w_tr)
        oof_preds["LinearRegression"][val_i] = lr.predict(Xval_sc)

        # RF/ET/GB
        rf = RandomForestRegressor(**model_defs["RandomForest"].get_params())
        rf.fit(X_tr.values, y_tr, sample_weight=w_tr)
        oof_preds["RandomForest"][val_i] = rf.predict(X_val.values)

        et = ExtraTreesRegressor(**model_defs["ExtraTrees"].get_params())
        et.fit(X_tr.values, y_tr, sample_weight=w_tr)
        oof_preds["ExtraTrees"][val_i] = et.predict(X_val.values)

        gb = GradientBoostingRegressor(**model_defs["GradientBoosting"].get_params())
        gb.fit(X_tr.values, y_tr, sample_weight=w_tr)
        oof_preds["GradientBoosting"][val_i] = gb.predict(X_val.values)

        # NN
        tf.random.set_seed(SEED)
        nn = build_nn(Xtr_sc.shape[1])
        nn.fit(Xtr_sc, y_tr, sample_weight=w_tr, epochs=40, batch_size=32, verbose=0)
        oof_preds["NeuralNet"][val_i] = nn.predict(Xval_sc).flatten()

        # XGB default (native)
        dtr = xgb.DMatrix(X_tr, label=y_tr, weight=w_tr)
        dval = xgb.DMatrix(X_val, label=y_val)
        params = {"objective":"reg:squarederror", "eval_metric":"mae", "seed":SEED, "tree_method":"hist"}
        booster = xgb.train(params, dtr, num_boost_round=2000, evals=[(dval,"val")],
                            early_stopping_rounds=100, verbose_eval=False)
        oof_preds["XGBoost (default)"][val_i] = booster.predict(dval)

    # summarize table
    base_mae, base_rmse, base_r2 = metrics(y, base_oof)
    results.append(("Baseline (train-mean)", base_mae, base_rmse, base_r2))

    for name in ["LinearRegression","RandomForest","ExtraTrees","GradientBoosting","NeuralNet","XGBoost (default)"]:
        mae, rmse, r2 = metrics(y, oof_preds[name])
        results.append((name, mae, rmse, r2))

    res_df = pd.DataFrame(results, columns=["Model","CV_MAE","CV_RMSE","CV_R2"]).sort_values("CV_MAE").reset_index(drop=True)
    return res_df, oof_preds


