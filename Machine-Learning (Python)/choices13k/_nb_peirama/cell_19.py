# -----------------------------
# 9) Plot helpers
# -----------------------------
def plot_feature_importance(final_booster, mode):
    score = final_booster.get_score(importance_type="gain")
    fi = pd.DataFrame({"Feature": list(score.keys()), "Gain": list(score.values())}) \
           .sort_values("Gain", ascending=False).head(15)

    plt.figure(figsize=(9,5))
    plt.barh(fi["Feature"][::-1], fi["Gain"][::-1])
    plt.title(f"Top-15 feature importance (XGBoost tuned) — {mode.upper()}")
    plt.xlabel("Gain")
    plt.tight_layout()
    plt.show()

def plot_parity(y, pred, mode):
    plt.figure(figsize=(6,6))
    plt.scatter(y, pred, alpha=0.25)
    plt.plot([0,1],[0,1], linestyle="--")
    plt.xlim(0,1); plt.ylim(0,1)
    plt.xlabel("True bRate")
    plt.ylabel("Predicted bRate (OOF, XGB default)")
    plt.title(f"OOF Parity plot — {mode.upper()}")
    plt.tight_layout()
    plt.show()
