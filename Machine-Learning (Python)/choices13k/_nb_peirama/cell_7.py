# -----------------------------
# 3) Build dataset (THEORY or RICH)
# -----------------------------
def build_dataset(df, problems_dict, mode="theory"):
    raw_cols = ["Ha","La","pHa","Hb","Lb","pHb"]
    have_raw = all(c in df.columns for c in raw_cols)
    have_std = "bRate_std" in df.columns

    feats, y, w, groups = [], [], [], []

    for _, row in df.iterrows():
        pid = str(row["Problem"])
        if pid not in problems_dict:
            continue

        outA = problems_dict[pid]["A"]
        outB = problems_dict[pid]["B"]

        sA = get_gamble_stats(outA)
        sB = get_gamble_stats(outB)

        peA = psych_ev(outA)
        peB = psych_ev(outB)

        rec = {
            "EV_Diff": sB["EV"] - sA["EV"],
            "SD_Diff": sB["SD"] - sA["SD"],
            "Min_Diff": sB["Min"] - sA["Min"],
            "Max_Diff": sB["Max"] - sA["Max"],
            "Psych_EV_Diff": peB - peA,

            "Amb": int(bool(row["Amb"])),
            "Corr": int(row["Corr"]),
            "Feedback": int(bool(row["Feedback"])),
            "LotShapeB": int(row["LotShapeB"]),
            "LotNumB": int(row["LotNumB"]),
            "Block": int(row["Block"]),
        }

        if mode == "rich":
            rec.update({
                "Entropy_Diff": sB["Entropy"] - sA["Entropy"],
                "P_Gain_Diff": sB["P_Gain"] - sA["P_Gain"],
                "P_Loss_Diff": sB["P_Loss"] - sA["P_Loss"],
                "CV_Diff": (safe_div(sB["SD"], abs(sB["EV"]) + 1e-6) - safe_div(sA["SD"], abs(sA["EV"]) + 1e-6)),
                "P_B_better_A": prob_B_better_than_A(outA, outB),
            })

            if have_raw:
                rec.update({
                    "Ha": float(row["Ha"]),
                    "La": float(row["La"]),
                    "pHa": float(row["pHa"]),
                    "Hb": float(row["Hb"]),
                    "Lb": float(row["Lb"]),
                    "pHb": float(row["pHb"]),
                })

            rec["Amb_x_SD"] = rec["Amb"] * rec["SD_Diff"]
            rec["Feedback_x_EV"] = rec["Feedback"] * rec["EV_Diff"]

        n = float(row["n"]) if "n" in df.columns else 1.0
        if mode == "rich" and have_std:
            std = float(row["bRate_std"])
            noise_factor = 1.0 / (std*std + 1e-4)
            noise_factor = min(noise_factor, 50.0)
            w.append(n * noise_factor)
        else:
            w.append(n)

        feats.append(rec)
        y.append(float(row["bRate"]))
        groups.append(pid)

    X = pd.DataFrame(feats)
    y = np.array(y, dtype=float)
    w = np.array(w, dtype=float)
    groups = np.array(groups)

    return X, y, w, groups


