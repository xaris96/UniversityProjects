def load_data():
    df = pd.read_csv("c13k_selections.csv")
    with open("c13k_problems.json", "r") as f:
        problems_dict = json.load(f)
    return df, problems_dict

def safe_div(a, b):
    return float(a / (b + EPS))

def get_gamble_stats(outcomes):
    probs = np.array([o[0] for o in outcomes], dtype=float)
    pays  = np.array([o[1] for o in outcomes], dtype=float)

    ev = float(np.sum(probs * pays))
    var = float(np.sum(probs * (pays - ev) ** 2))
    sd = float(np.sqrt(var))

    mn = float(np.min(pays))
    mx = float(np.max(pays))
    rng = float(mx - mn)

    p_gain = float(np.sum(probs[pays > 0])) if np.any(pays > 0) else 0.0
    p_loss = float(np.sum(probs[pays < 0])) if np.any(pays < 0) else 0.0
    p_zero = float(np.sum(probs[pays == 0])) if np.any(pays == 0) else 0.0

    ev_gain = float(np.sum(probs[pays > 0] * pays[pays > 0])) if np.any(pays > 0) else 0.0
    ev_loss = float(np.sum(probs[pays < 0] * pays[pays < 0])) if np.any(pays < 0) else 0.0

    mean_gain = safe_div(ev_gain, p_gain) if p_gain > 0 else 0.0
    mean_loss = safe_div(ev_loss, p_loss) if p_loss > 0 else 0.0

    abs_pays = np.abs(pays)
    mean_abs = float(np.sum(probs * abs_pays))
    max_gain = float(np.max(pays[pays > 0])) if np.any(pays > 0) else 0.0
    max_loss = float(np.min(pays[pays < 0])) if np.any(pays < 0) else 0.0

    if sd > 0:
        z = (pays - ev) / sd
        skew = float(np.sum(probs * z**3))
        kurt = float(np.sum(probs * z**4))
    else:
        skew = 0.0
        kurt = 0.0

    pclip = np.clip(probs, EPS, 1.0)
    ent = float(-np.sum(pclip * np.log(pclip)))

    return {
        "EV": ev,
        "SD": sd,
        "Var": var,
        "Min": mn,
        "Max": mx,
        "Range": rng,
        "P_Gain": p_gain,
        "P_Loss": p_loss,
        "P_Zero": p_zero,
        "EV_Gain": ev_gain,
        "EV_Loss": ev_loss,
        "Mean_Gain": mean_gain,
        "Mean_Loss": mean_loss,
        "Mean_Abs": mean_abs,
        "Max_Gain": max_gain,
        "Max_Loss": max_loss,
        "Skew": skew,
        "Kurt": kurt,
        "Entropy": ent,
        "Num_Out": float(len(outcomes)),
    }

def psych_ev(outcomes, alpha=0.88, gamma=0.65):
    probs = np.array([o[0] for o in outcomes], dtype=float)
    pays  = np.array([o[1] for o in outcomes], dtype=float)

    subj_pays = np.sign(pays) * (np.abs(pays) ** alpha)
    probs_clipped = np.clip(probs, EPS, 1.0)
    weighted_probs = np.exp(-(-np.log(probs_clipped)) ** gamma)

    return float(np.sum(weighted_probs * subj_pays))

def prob_B_better_than_A(outA, outB):
    pA = np.array([o[0] for o in outA], dtype=float)
    xA = np.array([o[1] for o in outA], dtype=float)
    pB = np.array([o[0] for o in outB], dtype=float)
    xB = np.array([o[1] for o in outB], dtype=float)

    mat = (xB[:, None] > xA[None, :]).astype(float)
    return float(np.sum((pB[:, None] * pA[None, :]) * mat))
