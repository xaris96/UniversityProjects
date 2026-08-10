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
