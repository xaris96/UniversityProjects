def build_dataset(df, problems_dict):
    raw_cols = ["Ha","La","pHa","Hb","Lb","pHb"]
    have_raw = all(c in df.columns for c in raw_cols)
    have_std = "bRate_std" in df.columns
    has_n = "n" in df.columns

    feats, y, w, groups = [], [], [], []

    stat_keys = [
        "EV","SD","Var","Min","Max","Range",
        "P_Gain","P_Loss","P_Zero",
        "EV_Gain","EV_Loss","Mean_Gain","Mean_Loss",
        "Mean_Abs","Max_Gain","Max_Loss",
        "Skew","Kurt","Entropy","Num_Out"
    ]

    problem_cache = {}

    for row in df.itertuples(index=False):
        pid = str(row.Problem)
        base = problem_cache.get(pid)
        if base is None:
            prob = problems_dict.get(pid)
            if prob is None:
                continue

            outA = prob["A"]
            outB = prob["B"]

            sA = get_gamble_stats(outA)
            sB = get_gamble_stats(outB)

            peA = psych_ev(outA)
            peB = psych_ev(outB)
            peA2 = psych_ev(outA, alpha=0.70, gamma=0.90)
            peB2 = psych_ev(outB, alpha=0.70, gamma=0.90)

            base = {}
            for k in stat_keys:
                base[f"{k}_A"] = sA[k]
                base[f"{k}_B"] = sB[k]
                base[f"{k}_Diff"] = sB[k] - sA[k]

            base["Psych_EV_A"] = peA
            base["Psych_EV_B"] = peB
            base["Psych_EV_Diff"] = peB - peA

            base["Psych_EV2_A"] = peA2
            base["Psych_EV2_B"] = peB2
            base["Psych_EV2_Diff"] = peB2 - peA2

            base["CV_A"] = safe_div(sA["SD"], abs(sA["EV"]) + 1e-6)
            base["CV_B"] = safe_div(sB["SD"], abs(sB["EV"]) + 1e-6)
            base["CV_Diff"] = base["CV_B"] - base["CV_A"]

            base["EV_Ratio"] = safe_div(sB["EV"], sA["EV"])
            base["SD_Ratio"] = safe_div(sB["SD"], sA["SD"])
            base["Range_Ratio"] = safe_div(sB["Range"], sA["Range"])
            base["P_Gain_Ratio"] = safe_div(sB["P_Gain"], sA["P_Gain"])
            base["P_Loss_Ratio"] = safe_div(sB["P_Loss"], sA["P_Loss"])
            base["Entropy_Ratio"] = safe_div(sB["Entropy"], sA["Entropy"])

            base["P_B_better_A"] = prob_B_better_than_A(outA, outB)

            problem_cache[pid] = base

        rec = base.copy()

        rec.update({
            "Amb": int(bool(row.Amb)),
            "Corr": int(row.Corr),
            "Feedback": int(bool(row.Feedback)),
            "LotShapeB": int(row.LotShapeB),
            "LotNumB": int(row.LotNumB),
            "Block": int(row.Block),
        })

        if have_raw:
            rec.update({
                "Ha": float(row.Ha),
                "La": float(row.La),
                "pHa": float(row.pHa),
                "Hb": float(row.Hb),
                "Lb": float(row.Lb),
                "pHb": float(row.pHb),
            })
            rec["EV_A_raw"] = float(row.pHa * row.Ha + (1 - row.pHa) * row.La)
            rec["EV_B_raw"] = float(row.pHb * row.Hb + (1 - row.pHb) * row.Lb)
            rec["EV_raw_Diff"] = rec["EV_B_raw"] - rec["EV_A_raw"]

        rec["Amb_x_SD_Diff"] = rec["Amb"] * rec["SD_Diff"]
        rec["Feedback_x_EV_Diff"] = rec["Feedback"] * rec["EV_Diff"]
        rec["Amb_x_Range_Diff"] = rec["Amb"] * rec["Range_Diff"]
        rec["Feedback_x_PGain_Diff"] = rec["Feedback"] * rec["P_Gain_Diff"]

        rec["EV_Diff_Abs"] = abs(rec["EV_Diff"])
        rec["SD_Diff_Abs"] = abs(rec["SD_Diff"])
        rec["Entropy_Diff_Abs"] = abs(rec["Entropy_Diff"])
        rec["Psych_EV_Diff_Abs"] = abs(rec["Psych_EV_Diff"])

        n = float(row.n) if has_n else 1.0
        if have_std:
            std = float(row.bRate_std)
            noise_factor = 1.0 / (std*std + 1e-4)
            noise_factor = min(noise_factor, 50.0)
            w.append(n * noise_factor)
        else:
            w.append(n)

        feats.append(rec)
        y.append(float(row.bRate))
        groups.append(pid)

    X = pd.DataFrame(feats)
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    y = np.array(y, dtype=float)
    w = np.array(w, dtype=float)
    groups = np.array(groups)
    return X, y, w, groups
