# -----------------------------
# 2) Feature functions
# -----------------------------
def get_gamble_stats(outcomes):
    probs = np.array([o[0] for o in outcomes], dtype=float)
    pays  = np.array([o[1] for o in outcomes], dtype=float)

    ev = float(np.sum(probs * pays))
    var = float(np.sum(probs * (pays - ev) ** 2))
    sd = float(np.sqrt(var))

    mn = float(np.min(pays))
    mx = float(np.max(pays))

    p_gain = float(np.sum(probs[pays > 0])) if np.any(pays > 0) else 0.0
    p_loss = float(np.sum(probs[pays < 0])) if np.any(pays < 0) else 0.0

    pclip = np.clip(probs, EPS, 1.0)
    ent = float(-np.sum(pclip * np.log(pclip)))
    return {"EV": ev, "SD": sd, "Min": mn, "Max": mx, "P_Gain": p_gain, "P_Loss": p_loss, "Entropy": ent}

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

def safe_div(a, b):
    return float(a / (b + EPS))


