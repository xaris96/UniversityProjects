
# -----------------------------
# 1) Load data
# -----------------------------
def load_data():
    df = pd.read_csv("c13k_selections.csv")
    with open("c13k_problems.json", "r") as f:
        problems_dict = json.load(f)
    return df, problems_dict
