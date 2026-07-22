
# -----------------------------
# 5) Metrics
# -----------------------------
def clip01(a): 
    return np.clip(np.asarray(a, dtype=float), 0, 1)

def metrics(y_true, y_pred):
    y_pred = clip01(y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2
