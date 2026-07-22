# 0) Data check
df, _ = load_data()
print("df shape:", df.shape, "| missing:", int(df.isnull().sum().sum()))
display(df.head(3))

# 1) THEORY run
print("\n" + "="*60)
print("RUNNING: THEORY mode")
print("="*60)
out_T = run_mode(mode="theory", n_trials=25)

# 2) THEORY CV table
print("\n--- CV RESULTS (THEORY) ---")
display(out_T["cv_table"])

# 3) THEORY tuning summary
print("\n--- TUNING (THEORY) ---")
print(f"Best tuned XGB CV MAE = {out_T['best_xgb']['mae']:.5f} ± {out_T['best_xgb']['std']:.5f}")
print("Best params:", out_T["best_xgb"]["params"])

# 4) THEORY plots
print("\n--- PLOTS (THEORY) ---")
plot_feature_importance(out_T["final_booster"], "theory")
plot_parity(out_T["y"], out_T["oof_default_xgb"], "theory")
