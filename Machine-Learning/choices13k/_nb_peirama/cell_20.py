# -----------------------------
# 10) MAIN: print in the order you want
# -----------------------------
df, _ = load_data()
print("df shape:", df.shape, "| missing:", int(df.isnull().sum().sum()))
display(df.head())

# 1) First: CV tables
out_T = run_mode(mode="theory", n_trials=25)
out_R = run_mode(mode="rich",  n_trials=25)

print("\n==============================")
print("CV RESULTS — THEORY")
print("==============================")
display(out_T["cv_table"])

print("\n==============================")
print("CV RESULTS — RICH")
print("==============================")
display(out_R["cv_table"])

# 2) Then: tuning summaries
print("\n==============================")
print("TUNING SUMMARY")
print("==============================")
print(f"THEORY tuned XGB: CV MAE = {out_T['best_xgb']['mae']:.5f} ± {out_T['best_xgb']['std']:.5f}")
print("THEORY best params:", out_T["best_xgb"]["params"])
print()
print(f"RICH  tuned XGB: CV MAE = {out_R['best_xgb']['mae']:.5f} ± {out_R['best_xgb']['std']:.5f}")
print("RICH best params:", out_R["best_xgb"]["params"])

# 3) Then: plots (THEORY then RICH)
print("\n==============================")
print("PLOTS — THEORY")
print("==============================")
plot_feature_importance(out_T["final_booster"], "theory")
plot_parity(out_T["y"], out_T["oof_default_xgb"], "theory")

print("\n==============================")
print("PLOTS — RICH")
print("==============================")
plot_feature_importance(out_R["final_booster"], "rich")
plot_parity(out_R["y"], out_R["oof_default_xgb"], "rich")

# 4) Final winner summary
best_overall = min(out_T["best_xgb"]["mae"], out_R["best_xgb"]["mae"])
best_tag = "THEORY" if out_T["best_xgb"]["mae"] <= out_R["best_xgb"]["mae"] else "RICH"

print("\n" + "="*70)
print("FINAL (properly cross-validated) RESULTS")
print("="*70)
print(f"THEORY tuned XGB: CV MAE = {out_T['best_xgb']['mae']:.5f} ± {out_T['best_xgb']['std']:.5f}")
print(f"RICH  tuned XGB: CV MAE = {out_R['best_xgb']['mae']:.5f} ± {out_R['best_xgb']['std']:.5f}")
print("\nBEST MAE (properly cross-validated):", f"{best_overall:.5f}", f"({best_tag})")
print("="*70)

print("\nBEST_MAE_CV =", float(best_overall))
