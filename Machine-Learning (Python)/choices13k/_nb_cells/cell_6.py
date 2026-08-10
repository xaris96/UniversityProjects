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
