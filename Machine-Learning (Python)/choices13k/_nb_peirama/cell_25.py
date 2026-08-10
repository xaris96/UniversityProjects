# 1) RICH run
print("\n" + "="*60)
print("RUNNING: RICH mode")
print("="*60)
out_R = run_mode(mode="rich", n_trials=25)

# 2) RICH CV table
print("\n--- CV RESULTS (RICH) ---")
display(out_R["cv_table"])

# 3) RICH tuning summary
print("\n--- TUNING (RICH) ---")
print(f"Best tuned XGB CV MAE = {out_R['best_xgb']['mae']:.5f} ± {out_R['best_xgb']['std']:.5f}")
print("Best params:", out_R["best_xgb"]["params"])

# 4) RICH plots
print("\n--- PLOTS (RICH) ---")
plot_feature_importance(out_R["final_booster"], "rich")
plot_parity(out_R["y"], out_R["oof_default_xgb"], "rich")

# 5) Final winner summary
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
