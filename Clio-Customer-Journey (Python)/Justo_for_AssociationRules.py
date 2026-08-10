
# ==== cell 0 ====
#κελί 0
import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# ==== cell 1 ====
#κελί 1
# Config
# ------------------------
DATA_DIR = ".\\clio"  # επειδή το notebook είναι μέσα στον φάκελο clio
EVENTS_DIR = os.path.join(DATA_DIR, "events_data")
USERS_DIR  = os.path.join(DATA_DIR, "users_data")

MONTHS = ["2025-07", "2025-08", "2025-09", "2025-10"]  # July–Oct 2025

EVENT_FILES = [f"events_data_{m}.csv" for m in MONTHS]
USER_FILES  = [f"users_data_{m}.csv" for m in MONTHS]

TOURS_FILE = os.path.join(DATA_DIR, "tour_title_mapping.csv")
LANG_FILE  = os.path.join(DATA_DIR, "id_language_mapping.csv")

OUTPUT_FILE = os.path.join(DATA_DIR, "events_clean_july_oct_2025.csv")

# ==== cell 2 ====
#κελί 2
# Helpers: ασφαλής φόρτωση + ένωση μηνιαίων csv
# ------------------------
def read_monthly_csv(folder: str, filenames: list[str]) -> pd.DataFrame:
    missing = [f for f in filenames if not os.path.exists(os.path.join(folder, f))]
    if missing:
        raise FileNotFoundError(f"Missing files in '{folder}':\n" + "\n".join(missing))

    dfs = []
    for f in filenames:
        path = os.path.join(folder, f)

        # low_memory=False για σωστό type inference
        # audio columns ως string για να καθαριστούν μετά χωρίς warnings
        df = pd.read_csv(
            path,
            low_memory=False,
            dtype={"audio_time_played": "string", "audio_time_paused": "string"}
        )
        df["source_file"] = f
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

# ==== cell 3 ====
#κελί 3
# EXTRACT: φόρτωση events, users, mappings
# ------------------------
events = read_monthly_csv(EVENTS_DIR, EVENT_FILES)
users  = read_monthly_csv(USERS_DIR, USER_FILES)

tours = pd.read_csv(TOURS_FILE)
languages = pd.read_csv(LANG_FILE)

print("Loaded:")
print("events:", events.shape)
print("users :", users.shape)
print("tours :", tours.shape)
print("languages:", languages.shape)

# ==== cell 4 ====
#κελί 4
# TRANSFORM: ημερομηνίες / timestamps
# ------------------------
# event_date robust parsing (πχ 20250718 ή 2025-07-18)
raw_date = events["event_date"].astype(str).str.strip()
mask_ymd8 = raw_date.str.fullmatch(r"\d{8}", na=False)

parsed_date = pd.Series(pd.NaT, index=events.index)
parsed_date.loc[mask_ymd8] = pd.to_datetime(raw_date.loc[mask_ymd8], format="%Y%m%d", errors="coerce")
parsed_date.loc[~mask_ymd8] = pd.to_datetime(raw_date.loc[~mask_ymd8], errors="coerce", dayfirst=True)
events["event_date"] = parsed_date

# event_timestamp: δοκίμασε us vs ms και κράτα αυτό που βγάζει λογικά έτη
ts_us = pd.to_datetime(events["event_timestamp"], unit="us", errors="coerce")
ts_ms = pd.to_datetime(events["event_timestamp"], unit="ms", errors="coerce")

def score_ts(ts):
    non_null = ts.notna().sum()
    year_ok = (ts.dt.year >= 2020).sum()
    return (year_ok, non_null)

events["event_timestamp"] = ts_us if score_ts(ts_us) >= score_ts(ts_ms) else ts_ms

# users timestamps
users["user_first_touch_timestamp_micros"] = pd.to_datetime(
    users["user_first_touch_timestamp_micros"], unit="us", errors="coerce"
)
if "first_purchase_date" in users.columns:
    users["first_purchase_date"] = pd.to_datetime(users["first_purchase_date"], errors="coerce")

# sanity checks
print("event_date dtype:", events["event_date"].dtype)
print("event_date null rate:", events["event_date"].isna().mean())
print("event_date min/max:", events["event_date"].min(), events["event_date"].max())
print("event_timestamp min/max:", events["event_timestamp"].min(), events["event_timestamp"].max())

# ==== cell 5 ====
#κελί 5
# TRANSFORM: φίλτρο July–Oct 2025
# ------------------------
start_date = pd.Timestamp("2025-07-01")
end_date   = pd.Timestamp("2025-10-31")

before = len(events)
events = events.dropna(subset=["event_date"]).copy()
events = events[(events["event_date"] >= start_date) & (events["event_date"] <= end_date)].copy()

print("Rows before filter:", before)
print("Rows after  filter:", len(events))

# ==== cell 6 ====
#κελί 6
# TRANSFORM: missingness + duplicates
# ------------------------
print("\nMissingness (top 10):")
print(events.isna().mean().sort_values(ascending=False).head(10))

critical_cols = ["event_timestamp", "event_name"]
events_before = len(events)
events = events.dropna(subset=critical_cols)
print(f"\nDropped {events_before - len(events)} rows with missing critical cols: {critical_cols}")

dedup_subset = [c for c in ["event_timestamp","event_name","user_id","user_pseudo_id","tour_id","story_id"] if c in events.columns]
dups = events.duplicated(subset=dedup_subset).sum()
print(f"\nDuplicates (by {dedup_subset}): {dups}")

events = events.drop_duplicates(subset=dedup_subset).copy()

# ==== cell 7 ====
#κελί 7
# TRANSFORM: καθαρισμός audio_time_* σε numeric (δευτερόλεπτα όπου γίνεται)
# ------------------------
for c in ["audio_time_played", "audio_time_paused"]:
    if c in events.columns:
        events[c] = (
            events[c].astype("string")
            .str.replace(",", ".", regex=False)
            .str.strip()
        )
        events[c] = pd.to_numeric(events[c], errors="coerce")

print("audio_time_played null rate:", events["audio_time_played"].isna().mean() if "audio_time_played" in events.columns else "N/A")
print("audio_time_paused null rate:", events["audio_time_paused"].isna().mean() if "audio_time_paused" in events.columns else "N/A")

# ==== cell 8 ====
#κελί 8
# TRANSFORM: merges με mapping tables (tour title, language)
# ------------------------
if "tour_id" in tours.columns:
    tours = tours.drop_duplicates(subset=["tour_id"])
if "lang_id" in languages.columns:
    languages = languages.drop_duplicates(subset=["lang_id"])

if "tour_id" in events.columns and "tour_id" in tours.columns:
    events = events.merge(tours, on="tour_id", how="left")

if "lang_id" in events.columns and "lang_id" in languages.columns:
    events = events.merge(languages, on="lang_id", how="left")

# ==== cell 9 ====
#κελί 9
# QUICK EDA + save cleaned
# ------------------------
print("\nEvent types (top 20):")
print(events["event_name"].value_counts().head(20))

print("\nUnique users (user_id):", events["user_id"].nunique() if "user_id" in events.columns else "no user_id")
print("Unique tours:", events["tour_id"].nunique() if "tour_id" in events.columns else "no tour_id")

events_clean = events.copy()
events_clean.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved cleaned events to: {OUTPUT_FILE}")
print("Final shape:", events_clean.shape)

# ==== cell 10 ====
#κελί 10
# Σταθερό user_key (χρησιμοποιούμε user_pseudo_id για να μην μετριέται διπλά ο ίδιος χρήστης)
# ------------------------
events_clean["user_key"] = events_clean["user_pseudo_id"].astype("string")

print("Unique user_id:", events_clean["user_id"].nunique())
print("Unique user_pseudo_id:", events_clean["user_pseudo_id"].nunique())
print("Unique user_key:", events_clean["user_key"].nunique())

# ==== cell 11 ====
#κελί 11
# Funnel: ορισμός σταδίων
# ------------------------
funnel_events = {
    "Ξεκίνησε ξενάγηση": ["start_tour"],
    "Ξεκίνησε ιστορία": ["story_start"],
    "Άκουσε ≥20% ιστορίας": ["story_listened_20"],
    "Ολοκλήρωσε ιστορία": ["story_completed"],
}

# ==== cell 12 ====
#κελί 12
# Funnel: υπολογισμός (μοναδικοί χρήστες ανά στάδιο)
# ------------------------
funnel_results = []
for stage, event_list in funnel_events.items():
    users_at_stage = events_clean[events_clean["event_name"].isin(event_list)]["user_key"].nunique()
    funnel_results.append({"Στάδιο": stage, "Χρήστες": users_at_stage})

funnel_df = pd.DataFrame(funnel_results)
funnel_df["Drop-off %"] = (1 - funnel_df["Χρήστες"] / funnel_df["Χρήστες"].shift(1)) * 100
funnel_df.loc[0, "Drop-off %"] = 0
funnel_df

# ==== cell 13 ====
#κελί 13
# Funnel: γράφημα
# ------------------------
plt.figure(figsize=(8, 5))
plt.bar(funnel_df["Στάδιο"], funnel_df["Χρήστες"])
plt.xticks(rotation=30, ha="right")
plt.title("Drop-off Χρηστών κατά τη Διάρκεια της Ξενάγησης")
plt.ylabel("Αριθμός Χρηστών")
plt.xlabel("Στάδιο Funnel")
plt.tight_layout()
plt.show()

# ==== cell 14 ====
#κελί 14
# Depth (milestones): μέγιστο βάθος ακρόασης ανά χρήστη + κατηγορίες + "Δεν έφτασε στο 20%"
# (Memory-friendly: χωρίς μεγάλο .copy())
# ------------------------
depth_map = {
    "story_listened_20": 20,
    "story_listened_40": 40,
    "story_listened_60": 60,
    "story_listened_80": 80,
    "story_completed": 100
}

# 1) Κράτα ΜΟΝΟ τις στήλες που χρειάζεσαι (μικρότερο dataframe)
tmp = events_clean.loc[:, ["user_key", "event_name"]]

# 2) Φιλτράρισμα σε milestones + mapping σε depth ΧΩΡΙΣ .copy()
mask = tmp["event_name"].isin(depth_map)
tmp2 = tmp.loc[mask]

# 3) Map event_name -> depth και max ανά χρήστη
#    (το map γυρνάει series, δεν χρειάζεται να κρατήσεις ολόκληρο tmp2 μετά)
depth_series = tmp2["event_name"].map(depth_map)

user_max_depth = (
    pd.DataFrame({"user_key": tmp2["user_key"].values, "depth": depth_series.values})
    .groupby("user_key", as_index=False)["depth"]
    .max()
)

# 4) Κατηγοριοποίηση
def depth_label(d):
    if d == 100:
        return "Ολοκλήρωσε ιστορία (100%)"
    else:
        return f"Έφτασε έως {int(d)}%"

user_max_depth["Depth Category"] = user_max_depth["depth"].apply(depth_label)

# 5) Κατανομή (μόνο όσων έχουν milestone)
order_depth = [
    "Έφτασε έως 20%",
    "Έφτασε έως 40%",
    "Έφτασε έως 60%",
    "Έφτασε έως 80%",
    "Ολοκλήρωσε ιστορία (100%)"
]

depth_distribution = (
    user_max_depth["Depth Category"]
    .value_counts()
    .reindex(order_depth, fill_value=0)
    .reset_index()
)
depth_distribution.columns = ["Βάθος Ακρόασης", "Χρήστες"]

# 6) Πρόσθεσε "Δεν έφτασε στο 20%"
total_users = events_clean["user_key"].nunique()
users_with_depth = user_max_depth["user_key"].nunique()
no_depth_users = total_users - users_with_depth

depth_distribution_full = pd.concat([
    pd.DataFrame({"Βάθος Ακρόασης": ["Δεν έφτασε στο 20%"], "Χρήστες": [no_depth_users]}),
    depth_distribution
], ignore_index=True)

order_full = ["Δεν έφτασε στο 20%"] + order_depth
depth_distribution_full["Βάθος Ακρόασης"] = pd.Categorical(
    depth_distribution_full["Βάθος Ακρόασης"],
    categories=order_full,
    ordered=True
)
depth_distribution_full = depth_distribution_full.sort_values("Βάθος Ακρόασης")

print("Total users:", total_users)
print("Users with any depth milestone (>=20% or completed):", users_with_depth)
print("Users with NO depth milestone:", no_depth_users)

depth_distribution_full

# ==== cell 15 ====
#κελί 15
# Depth: γράφημα κατανομής (με "Δεν έφτασε στο 20%")
# ------------------------
plt.figure(figsize=(9, 5))
plt.bar(depth_distribution_full["Βάθος Ακρόασης"], depth_distribution_full["Χρήστες"])
plt.xticks(rotation=30, ha="right")
plt.title("Κατανομή Βάθους Κατανάλωσης Περιεχομένου ανά Χρήστη")
plt.ylabel("Αριθμός Χρηστών")
plt.xlabel("Επίπεδο Ακρόασης")
plt.tight_layout()
plt.show()

# ==== cell 16 ====
#κελί 16
# Active vs Passive: ορισμός interaction events
# ------------------------
active_events = [
    "pause",
    "play",
    "forward_10",
    "backward_10",
    "next_story",
    "previous_story",
    "change_item"
]

# ==== cell 17 ====
#κελί 17
# Active vs Passive: χαρακτηρισμός χρηστών
# ------------------------
user_activity = (
    events_clean
    .assign(is_active_event=events_clean["event_name"].isin(active_events))
    .groupby("user_key")["is_active_event"]
    .any()
    .reset_index()
)
user_activity["Listening Type"] = np.where(user_activity["is_active_event"], "Active listener", "Passive listener")
user_activity["Listening Type"].value_counts()

# ==== cell 18 ====
#κελί 18
# Active vs Passive: ποσοστά + γράφημα
# ------------------------
listening_dist = (
    user_activity["Listening Type"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index()
)
listening_dist.columns = ["Τύπος Ακρόασης", "Ποσοστό (%)"]
listening_dist

# ==== cell 19 ====
#κελί 19
plt.figure(figsize=(6, 5))
plt.bar(listening_dist["Τύπος Ακρόασης"], listening_dist["Ποσοστό (%)"])
plt.title("Active vs Passive Listening")
plt.ylabel("Ποσοστό Χρηστών (%)")
plt.xlabel("Τύπος Ακρόασης")
plt.tight_layout()
plt.show()

# ==== cell 20 ====
#κελί 20
# Active/Passive + Depth: merge και summary (mean/median)
# ------------------------
user_depth_activity = user_max_depth.merge(
    user_activity[["user_key", "Listening Type"]],
    on="user_key",
    how="left"
)

depth_summary = (
    user_depth_activity
    .groupby("Listening Type")["depth"]
    .agg(Μέσο_Βάθος="mean", Median_Βάθος="median", Χρήστες="count")
    .reset_index()
)
depth_summary

# ==== cell 21 ====
#κελί 21
# Completion rate (100%) για active vs passive
# ------------------------
completion_flag = user_max_depth.copy()
completion_flag["completed"] = completion_flag["depth"] == 100

completion_analysis = (
    completion_flag
    .merge(user_activity[["user_key", "Listening Type"]], on="user_key", how="left")
    .groupby("Listening Type")["completed"]
    .mean()
    .mul(100)
    .round(2)
    .reset_index()
)
completion_analysis.columns = ["Τύπος Ακρόασης", "Completion Rate (%)"]
completion_analysis

# ==== cell 22 ====
#κελί 22
# Γράφημα ΠΟΣΟΣΤΩΝ ανά στάδιο (όπως το grouped που ζήτησες) + πίνακας με % και counts
# ------------------------
totals_by_type = user_depth_activity.groupby("Listening Type")["user_key"].nunique().to_dict()

depth_percent_stage = (
    user_depth_activity
    .groupby(["Depth Category", "Listening Type"])["user_key"]
    .nunique()
    .reset_index()
)

depth_percent_stage["Ποσοστό (%)"] = depth_percent_stage.apply(
    lambda x: round(x["user_key"] / totals_by_type[x["Listening Type"]] * 100, 2),
    axis=1
)

# πίνακας (counts + ποσοστά)
depth_percent_stage["Τιμή"] = (
    depth_percent_stage["user_key"].astype(str)
    + " χρήστες ("
    + depth_percent_stage["Ποσοστό (%)"].astype(str)
    + "%)"
)

depth_table_stage = depth_percent_stage.pivot(
    index="Depth Category",
    columns="Listening Type",
    values="Τιμή"
).reindex(order_depth)

depth_table_stage

# ==== cell 23 ====
#κελί 23
# Γράφημα grouped με ποσοστά (Active vs Passive ανά στάδιο)
# ------------------------
plot_stage = depth_percent_stage.pivot(
    index="Depth Category",
    columns="Listening Type",
    values="Ποσοστό (%)"
).reindex(order_depth)

plot_stage.plot(kind="bar", figsize=(9, 6))
plt.title("Ποσοστό Χρηστών ανά Στάδιο Ακρόασης\nActive vs Passive")
plt.ylabel("Ποσοστό χρηστών (%)")
plt.xlabel("Επίπεδο Ακρόασης")
plt.xticks(rotation=30, ha="right")
plt.legend(title="Τύπος Ακρόασης")
plt.tight_layout()
plt.show()

# ==== cell 24 ====
#κελί 24
# Top tours με περισσότερους Active / περισσότερους Passive (absolute numbers) με threshold
# ------------------------
tour_user_activity = (
    events_clean
    .merge(user_activity[["user_key", "Listening Type"]], on="user_key", how="left")
    .groupby(["tour_title", "Listening Type"])["user_key"]
    .nunique()
    .reset_index()
)

tour_activity_pivot = (
    tour_user_activity
    .pivot(index="tour_title", columns="Listening Type", values="user_key")
    .fillna(0)
)

tour_activity_pivot["Total users"] = tour_activity_pivot["Active listener"] + tour_activity_pivot["Passive listener"]

MIN_USERS = 100
tour_activity_filtered = tour_activity_pivot[tour_activity_pivot["Total users"] >= MIN_USERS].copy()

top_active_tours = (
    tour_activity_filtered
    .sort_values("Active listener", ascending=False)
    .head(10)[["Active listener","Passive listener","Total users"]]
)

top_passive_tours = (
    tour_activity_filtered
    .sort_values("Passive listener", ascending=False)
    .head(10)[["Active listener","Passive listener","Total users"]]
)

print("Top 10 tours by #Active (min users =", MIN_USERS, ")")
display(top_active_tours)

print("\nTop 10 tours by #Passive (min users =", MIN_USERS, ")")
display(top_passive_tours)

# ==== cell 25 ====
#κελί 25
# Story Order: κρατάμε story_start και χτίζουμε sequence ανά user_key + tour
# + αφαιρούμε διαδοχικά duplicates (restart / ξανά πατάει)
# ------------------------
story_starts = (
    events_clean[events_clean["event_name"] == "story_start"]
    [["user_key", "tour_id", "tour_title", "story_id", "event_timestamp"]]
    .sort_values(["user_key", "tour_id", "event_timestamp"])
    .copy()
)

# αφαιρεί διαδοχικά ίδια story_id (π.χ. story_start ξανά στο ίδιο story)
story_starts["prev_story"] = story_starts.groupby(["user_key", "tour_id"])["story_id"].shift(1)
story_starts_dedup = story_starts[story_starts["story_id"] != story_starts["prev_story"]].copy()
story_starts_dedup.drop(columns=["prev_story"], inplace=True)

story_starts_dedup.head()

# ==== cell 26 ====
#κελί 26
# Story Order: ορισμός "ακολουθεί σειρά" (proxy: αύξουσα πορεία story_id)
# ------------------------
def follows_order(story_ids):
    diffs = np.diff(story_ids)
    return np.all(diffs >= 0)  # ποτέ δεν γυρίζει πίσω

order_check = (
    story_starts_dedup
    .groupby(["user_key", "tour_id", "tour_title"])["story_id"]
    .apply(list)
    .reset_index()
)

order_check["Follows intended order"] = order_check["story_id"].apply(follows_order)
order_check.head()

# ==== cell 27 ====
#κελί 27
# Story Order: ποσοστά + γράφημα
# ------------------------
order_summary = (
    order_check["Follows intended order"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index()
)
order_summary.columns = ["Ακολουθεί σειρά", "Ποσοστό (%)"]

order_summary["Συμπεριφορά"] = order_summary["Ακολουθεί σειρά"].map({
    True: "Ακολουθεί τη σειρά",
    False: "Πηδά μεταξύ ιστοριών"
})

order_summary

# ==== cell 28 ====
#κελί 28
plt.figure(figsize=(6, 5))
plt.bar(order_summary["Συμπεριφορά"], order_summary["Ποσοστό (%)"])
plt.title("Ακολουθούν οι χρήστες τη σειρά των ιστοριών;")
plt.ylabel("Ποσοστό χρηστών (%)")
plt.xlabel("Τύπος Συμπεριφοράς")
plt.tight_layout()
plt.show()

# ==== cell 29 ====
#κελί 29
# Sanity check: μοναδικοί χρήστες σε βασικά events (για να εξηγείς τα gaps)
# ------------------------
event_users = (
    events_clean
    .groupby("event_name")["user_key"]
    .nunique()
    .loc[["start_tour", "story_start", "story_listened_20"]]
    .reset_index()
)
event_users

# ==== cell 30 ====
#κελί 30
# Knowledge Mining: Association Rules πάνω σε βασικά journey events (user-level baskets)
# ------------------------
knowledge_events = [
    "start_tour",
    "story_start",
    "story_listened_20",
    "story_listened_40",
    "story_listened_60",
    "story_listened_80",
    "story_completed",
    "play",
    "pause",
    "forward_10",
    "backward_10",
    "next_story",
    "previous_story",
    "change_item",
    "click_story",
    "tour_item_clicked",
]

event_label_map = {
    "start_tour": "Έναρξη ξενάγησης",
    "story_start": "Έναρξη ιστορίας",
    "story_listened_20": "Ακρόαση 20%",
    "story_listened_40": "Ακρόαση 40%",
    "story_listened_60": "Ακρόαση 60%",
    "story_listened_80": "Ακρόαση 80%",
    "story_completed": "Ολοκλήρωση ιστορίας",
    "play": "Play",
    "pause": "Pause",
    "forward_10": "Forward 10s",
    "backward_10": "Backward 10s",
    "next_story": "Next story",
    "previous_story": "Previous story",
    "change_item": "Αλλαγή αντικειμένου",
    "click_story": "Click story",
    "tour_item_clicked": "Click tour item",
}

km = (
    events_clean.loc[events_clean["event_name"].isin(knowledge_events), ["user_key", "event_name"]]
    .dropna()
    .drop_duplicates()
)

# factorize user_key για μικρότερο memory footprint στο crosstab
user_codes = pd.factorize(km["user_key"], sort=False)[0]
basket = pd.crosstab(user_codes, km["event_name"]).astype("uint8")

n_users_km = int(basket.shape[0])
rules_result = pd.DataFrame(
    columns=[
        "Κανόνας",
        "Users with A",
        "Users with A and B",
        "Support (%)",
        "Confidence (%)",
        "Lift",
        "rule_from",
        "rule_to",
    ]
)

if n_users_km == 0 or basket.shape[1] < 2:
    print("Not enough data to compute association rules (need >=2 events and >=1 user).")
else:
    event_counts = basket.sum(axis=0).astype(int)
    co_counts = basket.T.dot(basket).astype(int)

    rules_rows = []
    for antecedent in basket.columns:
        count_a = int(event_counts[antecedent])
        support_a = count_a / n_users_km if n_users_km else np.nan
        for consequent in basket.columns:
            if antecedent == consequent:
                continue
            count_b = int(event_counts[consequent])
            count_ab = int(co_counts.loc[antecedent, consequent])

            support_b = count_b / n_users_km if n_users_km else np.nan
            support_ab = count_ab / n_users_km if n_users_km else np.nan
            confidence = (count_ab / count_a) if count_a else np.nan
            lift = (confidence / support_b) if support_b and not np.isnan(confidence) else np.nan

            rules_rows.append(
                {
                    "antecedent": antecedent,
                    "consequent": consequent,
                    "users_A": count_a,
                    "users_B": count_b,
                    "users_A_and_B": count_ab,
                    "support": support_ab,
                    "confidence": confidence,
                    "lift": lift,
                    "support_A": support_a,
                    "support_B": support_b,
                }
            )

    rules_df = pd.DataFrame(rules_rows)

    MIN_SUPPORT = 0.03
    MIN_CONFIDENCE = 0.35
    MIN_LIFT = 1.10

    rules_filtered = (
        rules_df[
            (rules_df["support"] >= MIN_SUPPORT)
            & (rules_df["confidence"] >= MIN_CONFIDENCE)
            & (rules_df["lift"] >= MIN_LIFT)
        ]
        .sort_values(["lift", "confidence", "support"], ascending=False)
        .copy()
    )

    if rules_filtered.empty:
        rules_filtered = (
            rules_df[rules_df["support"] >= 0.01]
            .sort_values(["lift", "confidence", "support"], ascending=False)
            .head(15)
            .copy()
        )
    else:
        rules_filtered = rules_filtered.head(15).copy()

    rules_filtered["Από"] = rules_filtered["antecedent"].map(event_label_map).fillna(rules_filtered["antecedent"])
    rules_filtered["Προς"] = rules_filtered["consequent"].map(event_label_map).fillna(rules_filtered["consequent"])
    rules_filtered["Κανόνας"] = rules_filtered["Από"] + " → " + rules_filtered["Προς"]
    rules_filtered["Support (%)"] = (rules_filtered["support"] * 100).round(2)
    rules_filtered["Confidence (%)"] = (rules_filtered["confidence"] * 100).round(2)
    rules_filtered["Lift"] = rules_filtered["lift"].round(3)

    print("Users analyzed (knowledge mining):", n_users_km)
    print("Distinct events analyzed:", len(basket.columns))

    rules_result = rules_filtered[
        [
            "Κανόνας",
            "users_A",
            "users_A_and_B",
            "Support (%)",
            "Confidence (%)",
            "Lift",
            "antecedent",
            "consequent",
        ]
    ].rename(
        columns={
            "users_A": "Users with A",
            "users_A_and_B": "Users with A and B",
            "antecedent": "rule_from",
            "consequent": "rule_to",
        }
    )

rules_result

# ==== cell 31 ====
#κελί 31
# Knowledge Mining: γράφημα Top κανόνων (βάσει Lift)
# ------------------------
plot_rules = rules_result.sort_values("Lift", ascending=True).tail(12)

if plot_rules.empty:
    print("No association rules to plot.")
else:
    plt.figure(figsize=(11, 6))
    plt.barh(plot_rules["Κανόνας"], plot_rules["Lift"], color=sns.color_palette("mako", n_colors=len(plot_rules)))
    plt.axvline(1.0, linestyle="--", linewidth=1)
    plt.title("Top Association Rules (Lift) σε user journeys")
    plt.xlabel("Lift ( >1 σημαίνει ισχυρή συσχέτιση )")
    plt.ylabel("Κανόνας")
    plt.tight_layout()
    plt.show()

# ==== cell 32 ====
#κελί 32
# Knowledge Mining: save rules + σύντομα insights
# ------------------------
RULES_OUTPUT_FILE = os.path.join(DATA_DIR, "knowledge_rules_july_oct_2025.csv")
rules_result.to_csv(RULES_OUTPUT_FILE, index=False)

print("Saved knowledge rules to:", RULES_OUTPUT_FILE)
print("\nTop 5 rules:")
display(rules_result.head(5))
