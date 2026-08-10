
# ==== cell 0 ====
#κελί  0
import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns




# ==== cell 2 ====
#κελί  1
# Config
DATA_DIR = ".\\clio"  # επειδη το εχω μέσα στον φάκελο clio
EVENTS_DIR = os.path.join(DATA_DIR, "events_data")
USERS_DIR  = os.path.join(DATA_DIR, "users_data")

MONTHS = ["2025-07", "2025-08", "2025-09", "2025-10"]  # July–Oct 2025

EVENT_FILES = [f"events_data_{m}.csv" for m in MONTHS]
USER_FILES  = [f"users_data_{m}.csv" for m in MONTHS]

TOURS_FILE = os.path.join(DATA_DIR, "tour_title_mapping.csv")
LANG_FILE  = os.path.join(DATA_DIR, "id_language_mapping.csv")

OUTPUT_FILE = os.path.join(DATA_DIR, "events_clean_july_oct_2025.csv")

# ==== cell 4 ====
#κελί 2
# Helpers
def read_monthly_csv(folder: str, filenames: list[str]) -> pd.DataFrame:
    missing = [f for f in filenames if not os.path.exists(os.path.join(folder, f))]
    if missing:
        raise FileNotFoundError(
            f"Missing files in '{folder}':\n" + "\n".join(missing)
        )
    dfs = []
    for f in filenames:
        path = os.path.join(folder, f)

        # low_memory=False για να μη σπάει types σε chunks (σταματάει τα DtypeWarning)
        # dtype για audio columns ως string ώστε να καθαριστούν σωστά μετά (mixed types fix)
        df = pd.read_csv(
            path,
            low_memory=False,
            dtype={
                "audio_time_played": "string",
                "audio_time_paused": "string",
            }
        )

        df["source_file"] = f  # helpful for debugging
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

# ==== cell 6 ====
#κελί 3
# EXTRACT
events = read_monthly_csv(EVENTS_DIR, EVENT_FILES)
users  = read_monthly_csv(USERS_DIR, USER_FILES)

tours = pd.read_csv(TOURS_FILE)
languages = pd.read_csv(LANG_FILE)

print("Loaded:")
print("events:", events.shape)
print("users :", users.shape)
print("tours :", tours.shape)
print("languages:", languages.shape)

# ==== cell 8 ====
# κελι 4
# TRANSFORM - dates/timestamps
# event_date robust parsing χωρίς .loc assigns
raw_date = events["event_date"].astype(str).str.strip()

mask_ymd8 = raw_date.str.fullmatch(r"\d{8}", na=False)

parsed_date = pd.Series(pd.NaT, index=events.index)

parsed_date.loc[mask_ymd8] = pd.to_datetime(
    raw_date.loc[mask_ymd8],
    format="%Y%m%d",
    errors="coerce"
)

parsed_date.loc[~mask_ymd8] = pd.to_datetime(
    raw_date.loc[~mask_ymd8],
    errors="coerce",
    dayfirst=True
)

events["event_date"] = parsed_date

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

# ==== cell 10 ====
# κελι 5
# TRANSFORM - filter July–Oct 2025
start_date = pd.Timestamp("2025-07-01")
end_date   = pd.Timestamp("2025-10-31")

before = len(events)

# Πρώτα πέτα NaT dates (αν υπάρχουν λίγα)
events = events.dropna(subset=["event_date"]).copy()

events = events[(events["event_date"] >= start_date) & (events["event_date"] <= end_date)].copy()

print("Rows before filter:", before)
print("Rows after  filter:", len(events))

# ==== cell 12 ====
#κελί 6
# TRANSFORM - missingness + duplicates
print("\nMissingness (top 10):")
print(events.isna().mean().sort_values(ascending=False).head(10))

# Αφαιρώ events που δεν έχουν βασικά IDs ή event_name/timestamp (συνήθως άχρηστα για analysis)
critical_cols = ["event_timestamp", "event_name"]
id_cols = ["user_id", "user_pseudo_id"]
key_cols = [c for c in (critical_cols + id_cols) if c in events.columns]

events_before = len(events)
events = events.dropna(subset=critical_cols)  # κρατάω events που έχουν τύπο & χρόνο
print(f"\nDropped {events_before - len(events)} rows with missing critical cols: {critical_cols}")

# Dedup με λογικό subset (όχι όλο το row) για να μη χάνεις χρήσιμα events από μικρές διαφορές
dedup_subset = [c for c in ["event_timestamp", "event_name", "user_id", "user_pseudo_id", "tour_id", "story_id"] if c in events.columns]

dups = events.duplicated(subset=dedup_subset).sum()
print(f"\nDuplicates (by {dedup_subset}): {dups}")

events = events.drop_duplicates(subset=dedup_subset).copy()

# ==== cell 14 ====
# cell 6.5
# Audio columns -> parse "mm:ss" / "hh:mm:ss" to seconds
for c in ["audio_time_played", "audio_time_paused"]:
    if c in events.columns:
        raw = events[c].astype("string").str.strip()

        # Most values are mm:ss (example: 00:45). Convert to 00:mm:ss.
        hhmmss = raw.where(raw.str.count(":") == 2, "00:" + raw)

        events[c + "_sec"] = pd.to_timedelta(hhmmss, errors="coerce").dt.total_seconds()

print(
    "audio_time_played raw non-null rate:",
    events["audio_time_played"].notna().mean() if "audio_time_played" in events.columns else "N/A",
)
print(
    "audio_time_paused raw non-null rate:",
    events["audio_time_paused"].notna().mean() if "audio_time_paused" in events.columns else "N/A",
)
print(
    "audio_time_played_sec non-null rate:",
    events["audio_time_played_sec"].notna().mean() if "audio_time_played_sec" in events.columns else "N/A",
)
print(
    "audio_time_paused_sec non-null rate:",
    events["audio_time_paused_sec"].notna().mean() if "audio_time_paused_sec" in events.columns else "N/A",
)

# ==== cell 16 ====
#κελί 7
# TRANSFORM - merges (safe)
# mapping tables έχουν μοναδικά keys πριν κάνεις merge
if "tour_id" in tours.columns:
    tours = tours.drop_duplicates(subset=["tour_id"])
if "lang_id" in languages.columns:
    languages = languages.drop_duplicates(subset=["lang_id"])

# Merge tours
if "tour_id" in events.columns and "tour_id" in tours.columns:
    events = events.merge(tours, on="tour_id", how="left")

# Merge languages
if "lang_id" in events.columns and "lang_id" in languages.columns:
    events = events.merge(languages, on="lang_id", how="left")

# ==== cell 18 ====
#κελί 8
# QUICK EDA (prints)
print("\nEvent types (top 20):")
print(events["event_name"].value_counts().head(20))

print("\nUnique users:", events["user_id"].nunique() if "user_id" in events.columns else "no user_id")
print("Unique tours:", events["tour_id"].nunique() if "tour_id" in events.columns else "no tour_id")

if "tour_title" in events.columns and "story_id" in events.columns:
    print("\nStories per tour (top 15):")
    print(events.groupby("tour_title")["story_id"].nunique().sort_values(ascending=False).head(15))

# ==== cell 20 ====
#κελί 9
# LOAD - save cleaned dataset
events_clean = events.copy()
events_clean.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved cleaned events to: {OUTPUT_FILE}")
print("Final shape:", events_clean.shape)

# ==== cell 22 ====
# cell 10 (memory-safe, self-contained)
# Keep only columns needed by Q1/Q2/Q3 to reduce memory pressure.
analysis_cols = [
    "user_id",
    "user_pseudo_id",
    "event_timestamp",
    "platform",
    "event_name",
    "tour_id",
    "story_id",
    "tour_title",
    "channel",
]

available_cols = None
if "events_clean" in globals():
    available_cols = [c for c in analysis_cols if c in events_clean.columns]
    analysis_events = events_clean[available_cols]
else:
    from pathlib import Path
    default_clean_path = Path("./clio/events_clean_july_oct_2025.csv")
    clean_path = Path(OUTPUT_FILE) if "OUTPUT_FILE" in globals() else default_clean_path
    sample_df = pd.read_csv(clean_path, nrows=1)
    available_cols = [c for c in analysis_cols if c in sample_df.columns]
    analysis_events = pd.read_csv(clean_path, usecols=available_cols, low_memory=False)

analysis_events["event_timestamp"] = pd.to_datetime(analysis_events["event_timestamp"], errors="coerce")
analysis_events["event_name"] = analysis_events["event_name"].astype("string")

# Keep only events used downstream (Q1/Q2/Q3).
analysis_event_names = {
    "start_tour",
    "story_start",
    "story_listened_20",
    "story_listened_40",
    "story_listened_60",
    "story_listened_80",
    "story_completed",
    "pause",
    "play",
    "forward_10",
    "backward_10",
    "next_story",
    "previous_story",
    "click_progress_bar",
    "click_story",
    "tour_item_clicked",
}

analysis_events = analysis_events.loc[
    analysis_events["event_name"].isin(analysis_event_names)
]

# Stable user key: prefer logged-in user_id, fallback to pseudo id
uid = pd.to_numeric(analysis_events["user_id"], errors="coerce").astype("Int64").astype("string")
pid = analysis_events["user_pseudo_id"].astype("string")

analysis_events["user_key"] = uid.radd("uid_")
mask_uid_missing = uid.isna()
analysis_events.loc[mask_uid_missing, "user_key"] = pid[mask_uid_missing].radd("pid_")

analysis_events["tour_id"] = pd.to_numeric(analysis_events["tour_id"], errors="coerce").astype("Int64")
analysis_events["story_id"] = pd.to_numeric(analysis_events["story_id"], errors="coerce").astype("Int64")
analysis_events["platform"] = analysis_events["platform"].astype("string").str.upper()

valid_mask = (
    analysis_events["event_name"].notna()
    & analysis_events["event_timestamp"].notna()
    & analysis_events["user_key"].notna()
)
analysis_events = analysis_events.loc[valid_mask]

# Drop raw IDs after user_key derivation to release memory.
analysis_events = analysis_events.drop(columns=["user_id", "user_pseudo_id"], errors="ignore")

# Compact dtypes for repeated strings.
for col in ["event_name", "platform", "channel"]:
    if col in analysis_events.columns:
        analysis_events[col] = analysis_events[col].astype("category")

analysis_events = analysis_events.reset_index(drop=True)

# Lightweight compatibility alias for downstream ad-hoc checks.
# Note: this is filtered to analysis events/columns, not the full raw table.
events_clean = analysis_events
import gc
gc.collect()

key_events = [
    "start_tour",
    "story_start",
    "story_listened_20",
    "story_listened_40",
    "story_listened_60",
    "story_listened_80",
    "story_completed",
]

instrumentation_check = (
    analysis_events[analysis_events["event_name"].isin(key_events)]
    .groupby(["platform", "event_name"], observed=True)["user_key"]
    .nunique()
    .unstack(fill_value=0)
)

print("Shape analysis_events:", analysis_events.shape)
instrumentation_check

# ==== cell 24 ====
# cell 11 (tour-session journeys for Q1/Q2)
depth_event_to_pct = {
    "story_listened_20": 20,
    "story_listened_40": 40,
    "story_listened_60": 60,
    "story_listened_80": 80,
    "story_completed": 100,
}

story_evidence_events = ["story_start"] + list(depth_event_to_pct.keys())
strong_control_events = [
    "forward_10",
    "backward_10",
    "next_story",
    "previous_story",
    "click_progress_bar",
]

q12_event_names = set(story_evidence_events + strong_control_events)
q12_cols = ["user_key", "tour_id", "story_id", "event_name", "event_timestamp", "platform", "tour_title"]

q12_events = (
    analysis_events[
        analysis_events["tour_id"].notna()
        & analysis_events["event_name"].isin(q12_event_names)
    ][q12_cols]
    .copy()
)

q12_events["tour_id"] = q12_events["tour_id"].astype("Int64")
q12_events["story_id"] = q12_events["story_id"].astype("Int64")
q12_events = q12_events.sort_values(["user_key", "tour_id", "event_timestamp"]).reset_index(drop=True)

# Journey split rule: new tour-journey after 30 minutes inactivity within same user+tour.
gap_min = (
    q12_events
    .groupby(["user_key", "tour_id"])["event_timestamp"]
    .diff()
    .dt.total_seconds()
    .div(60)
)
new_journey = gap_min.isna() | (gap_min > 30)
q12_events["journey_idx"] = (
    new_journey.groupby([q12_events["user_key"], q12_events["tour_id"]]).cumsum().astype("Int64")
)

journey_keys = ["user_key", "tour_id", "journey_idx"]

journey_platform = (
    q12_events
    .groupby(journey_keys, as_index=False)["platform"]
    .first()
    .rename(columns={"platform": "journey_platform"})
)

controls_q12 = q12_events[q12_events["event_name"].isin(strong_control_events)]
journey_controls = (
    controls_q12
    .groupby(journey_keys, as_index=False)
    .size()
    .rename(columns={"size": "strong_control_events"})
)

story_events_q12 = q12_events[
    q12_events["event_name"].isin(story_evidence_events)
    & q12_events["story_id"].notna()
].copy()
story_events_q12["depth_pct"] = story_events_q12["event_name"].map(depth_event_to_pct).fillna(0).astype(int)

story_progress_journey = (
    story_events_q12
    .groupby(journey_keys + ["story_id"], as_index=False)
    .agg(
        max_depth=("depth_pct", "max"),
        first_story_ts=("event_timestamp", "min"),
    )
)

journey_depth = (
    story_progress_journey
    .groupby(journey_keys, as_index=False)
    .agg(
        max_depth=("max_depth", "max"),
        first_event_ts=("first_story_ts", "min"),
        stories_touched=("story_id", "nunique"),
        stories_completed=("max_depth", lambda s: int((s == 100).sum())),
    )
)
journey_depth["completion_share_pct"] = (
    journey_depth["stories_completed"] / journey_depth["stories_touched"] * 100
).round(2)

# Canonical story order per tour from median position across sessions.
session_sequences_q12 = (
    story_progress_journey
    .sort_values(journey_keys + ["first_story_ts"])
    .groupby(journey_keys, as_index=False)["story_id"]
    .agg(list)
    .rename(columns={"story_id": "story_seq"})
)

seq_exploded_q12 = session_sequences_q12.explode("story_seq").rename(columns={"story_seq": "story_id"})
seq_exploded_q12["position"] = seq_exploded_q12.groupby(journey_keys).cumcount() + 1

canonical_positions_q12 = (
    seq_exploded_q12
    .groupby(["tour_id", "story_id"], as_index=False)["position"]
    .median()
    .sort_values(["tour_id", "position", "story_id"])
)
canonical_positions_q12["canonical_rank"] = canonical_positions_q12.groupby("tour_id").cumcount() + 1

final_rank_by_tour = (
    canonical_positions_q12
    .groupby("tour_id", as_index=False)["canonical_rank"]
    .max()
    .rename(columns={"canonical_rank": "final_canonical_rank"})
)

story_progress_journey = story_progress_journey.merge(
    canonical_positions_q12[["tour_id", "story_id", "canonical_rank"]],
    on=["tour_id", "story_id"],
    how="left",
)

story_progress_journey["canonical_rank"] = story_progress_journey["canonical_rank"].fillna(0).astype(int)
story_progress_journey["canonical_rank_endlike"] = np.where(
    story_progress_journey["max_depth"] >= 80,
    story_progress_journey["canonical_rank"],
    0,
)

journey_rank_progress = (
    story_progress_journey
    .groupby(journey_keys, as_index=False)
    .agg(
        max_canonical_rank_seen=("canonical_rank", "max"),
        max_canonical_rank_endlike=("canonical_rank_endlike", "max"),
    )
)

journey_progress = (
    journey_depth
    .merge(journey_platform, on=journey_keys, how="left")
    .merge(journey_controls, on=journey_keys, how="left")
    .merge(journey_rank_progress, on=journey_keys, how="left")
    .merge(final_rank_by_tour, on="tour_id", how="left")
)

journey_progress["strong_control_events"] = journey_progress["strong_control_events"].fillna(0).astype(int)
journey_progress["max_canonical_rank_seen"] = journey_progress["max_canonical_rank_seen"].fillna(0).astype(int)
journey_progress["max_canonical_rank_endlike"] = journey_progress["max_canonical_rank_endlike"].fillna(0).astype(int)

journey_progress["reached_last_story"] = (
    journey_progress["max_canonical_rank_seen"] >= journey_progress["final_canonical_rank"]
)
journey_progress["reached_tour_end"] = (
    journey_progress["max_canonical_rank_endlike"] >= journey_progress["final_canonical_rank"]
)

journey_progress["controls_per_story"] = np.where(
    journey_progress["stories_touched"] > 0,
    journey_progress["strong_control_events"] / journey_progress["stories_touched"],
    0,
)
journey_progress["controls_per_story"] = journey_progress["controls_per_story"].round(3)

# Active rule: >=2 strong controls OR >=0.2 controls/story.
journey_progress["listening_mode"] = np.where(
    (journey_progress["strong_control_events"] >= 2)
    | (journey_progress["controls_per_story"] >= 0.2),
    "Active listening",
    "Passive play",
)
journey_progress["journey_status"] = np.where(
    journey_progress["reached_tour_end"],
    "Reached tour end",
    "Abandoned before end",
)

print("Tour journeys (30-min sessions):", len(journey_progress))
journey_progress.head()

# ==== cell 26 ====
# cell 12 (Q1)
q1_journey_dist = (
    journey_progress["journey_status"]
    .value_counts()
    .rename_axis("journey_status")
    .reset_index(name="tour_journeys")
)
q1_journey_dist["share_pct"] = (
    q1_journey_dist["tour_journeys"] / q1_journey_dist["tour_journeys"].sum() * 100
).round(2)

q1_user_status = (
    journey_progress
    .groupby("user_key", as_index=False)
    .agg(
        journeys=("tour_id", "size"),
        any_reached_end=("reached_tour_end", "any"),
    )
)
q1_user_status["user_status"] = np.where(
    q1_user_status["any_reached_end"],
    "Reached end (at least once)",
    "Only abandoned",
)

q1_user_dist = (
    q1_user_status["user_status"]
    .value_counts()
    .rename_axis("user_status")
    .reset_index(name="users")
)
q1_user_dist["share_pct"] = (q1_user_dist["users"] / q1_user_dist["users"].sum() * 100).round(2)

q1_total_users = int(len(q1_user_status))
q1_reached_users = int(q1_user_status["any_reached_end"].sum())
q1_abandoned_only_users = q1_total_users - q1_reached_users

print("Q1 journey outcomes:")
print(q1_journey_dist)
print("")
print("Q1 user outcomes:")
print(q1_user_dist)

q1_journey_dist

# ==== cell 27 ====
# cell 13 (Q1)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.barplot(
    data=q1_journey_dist,
    x="journey_status",
    y="share_pct",
    ax=axes[0],
    color="#1f77b4",
)
axes[0].set_title("Q1: Journey outcomes")
axes[0].set_xlabel("Journey status")
axes[0].set_ylabel("Share of tour journeys (%)")
axes[0].tick_params(axis="x", rotation=20)

sns.barplot(
    data=q1_user_dist,
    x="user_status",
    y="share_pct",
    ax=axes[1],
    color="#2ca02c",
)
axes[1].set_title("Q1: User outcomes")
axes[1].set_xlabel("User status")
axes[1].set_ylabel("Share of users (%)")
axes[1].tick_params(axis="x", rotation=20)

plt.tight_layout()
plt.show()

q1_user_status["journeys"].describe(percentiles=[0.25, 0.5, 0.75]).round(2)

# ==== cell 29 ====
# cell 14a (Q2)
q2_mode_dist = (
    journey_progress["listening_mode"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .rename_axis("listening_mode")
    .reset_index(name="share_pct")
)

q2_by_platform = (
    journey_progress
    .groupby(["journey_platform", "listening_mode"], as_index=False, observed=True)
    .size()
    .rename(columns={"size": "tour_journeys"})
)
q2_by_platform["share_pct"] = (
    q2_by_platform["tour_journeys"]
    / q2_by_platform.groupby("journey_platform", observed=True)["tour_journeys"].transform("sum")
    * 100
).round(2)

q2_completion = (
    journey_progress
    .groupby("listening_mode", as_index=False)
    .agg(
        reach_end_rate_pct=("reached_tour_end", lambda s: round(s.mean() * 100, 2)),
        avg_completion_share_pct=("completion_share_pct", lambda s: round(s.mean(), 2)),
        avg_controls_per_story=("controls_per_story", lambda s: round(s.mean(), 3)),
        tour_journeys=("tour_id", "size"),
    )
)

q2_user_mode = (
    journey_progress
    .groupby("user_key", as_index=False)
    .agg(
        any_active=("listening_mode", lambda s: (s == "Active listening").any()),
        any_passive=("listening_mode", lambda s: (s == "Passive play").any()),
    )
)
q2_user_mode["user_mode"] = np.select(
    [
        q2_user_mode["any_active"] & q2_user_mode["any_passive"],
        q2_user_mode["any_active"],
        q2_user_mode["any_passive"],
    ],
    ["Mixed (active + passive)", "Active only", "Passive only"],
    default="Unknown",
)

q2_user_dist = (
    q2_user_mode["user_mode"]
    .value_counts()
    .rename_axis("user_mode")
    .reset_index(name="users")
)
q2_user_dist["share_pct"] = (q2_user_dist["users"] / q2_user_dist["users"].sum() * 100).round(2)

q2_total_users = int(len(q2_user_mode))
q2_active_users = int(q2_user_mode["any_active"].sum())
q2_passive_only_users = int((~q2_user_mode["any_active"]).sum())

print("Q2 distribution (journeys):")
print(q2_mode_dist)
print("")
print("Q2 user distribution:")
print(q2_user_dist)
print("")
print("Q2 reach-end rate by mode:")
print(q2_completion)

# ==== cell 30 ====
# cell 14b (Q2)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

sns.barplot(
    data=q2_mode_dist,
    x="listening_mode",
    y="share_pct",
    ax=axes[0],
    color="#4c78a8",
)
axes[0].set_title("Q2: Active vs Passive (journeys)")
axes[0].set_xlabel("Listening mode")
axes[0].set_ylabel("Share of tour journeys (%)")
axes[0].tick_params(axis="x", rotation=20)

sns.barplot(
    data=q2_user_dist,
    x="user_mode",
    y="share_pct",
    ax=axes[1],
    color="#72b7b2",
)
axes[1].set_title("Q2: User activity profiles")
axes[1].set_xlabel("User mode")
axes[1].set_ylabel("Share of users (%)")
axes[1].tick_params(axis="x", rotation=20)

sns.barplot(
    data=q2_completion,
    x="listening_mode",
    y="reach_end_rate_pct",
    ax=axes[2],
    color="#f58518",
)
axes[2].set_title("Q2: Reached end rate by mode")
axes[2].set_xlabel("Listening mode")
axes[2].set_ylabel("Reached tour end (%)")
axes[2].tick_params(axis="x", rotation=20)

plt.tight_layout()
plt.show()

# ==== cell 31 ====
# cell 14c (Q2 summary)
q2_active_share = float(
    q2_mode_dist.loc[q2_mode_dist["listening_mode"] == "Active listening", "share_pct"].iloc[0]
)
q2_passive_share = float(
    q2_mode_dist.loc[q2_mode_dist["listening_mode"] == "Passive play", "share_pct"].iloc[0]
)

q2_summary = pd.DataFrame(
    {
        "metric": [
            "Q2 - Active journey share (%)",
            "Q2 - Passive journey share (%)",
            "Q2 - Users with >=1 active journey (%)",
            "Q2 - Users passive-only (%)",
            "Q2 - Reached-end rate (active journeys, %)",
            "Q2 - Reached-end rate (passive journeys, %)",
            "Q2 - Avg controls per story (active journeys)",
            "Q2 - Avg controls per story (passive journeys)",
        ],
        "value": [
            q2_active_share,
            q2_passive_share,
            round(q2_active_users / q2_total_users * 100, 2),
            round(q2_passive_only_users / q2_total_users * 100, 2),
            float(q2_completion.loc[q2_completion["listening_mode"] == "Active listening", "reach_end_rate_pct"].iloc[0]),
            float(q2_completion.loc[q2_completion["listening_mode"] == "Passive play", "reach_end_rate_pct"].iloc[0]),
            float(q2_completion.loc[q2_completion["listening_mode"] == "Active listening", "avg_controls_per_story"].iloc[0]),
            float(q2_completion.loc[q2_completion["listening_mode"] == "Passive play", "avg_controls_per_story"].iloc[0]),
        ],
    }
)

q2_summary

# ==== cell 33 ====
# cell 16 (Q3)
android_starts = (
    analysis_events[
        (analysis_events["platform"] == "ANDROID")
        & (analysis_events["event_name"] == "story_start")
        & analysis_events["tour_id"].notna()
        & analysis_events["story_id"].notna()
    ][["user_key", "tour_id", "tour_title", "story_id", "event_timestamp"]]
    .copy()
)

android_starts["tour_id"] = android_starts["tour_id"].astype("Int64")
android_starts["story_id"] = android_starts["story_id"].astype("Int64")


def unique_in_order(values):
    seen = set()
    out = []
    for value in values:
        if pd.isna(value):
            continue
        value = int(value)
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


session_sequences = (
    android_starts.sort_values(["user_key", "tour_id", "event_timestamp"])
    .groupby(["user_key", "tour_id", "tour_title"])["story_id"]
    .apply(unique_in_order)
    .reset_index(name="story_seq")
)

session_sequences["n_unique_stories"] = session_sequences["story_seq"].str.len()
session_sequences = session_sequences[session_sequences["n_unique_stories"] >= 2].reset_index(drop=True)
session_sequences["session_id"] = session_sequences.index

print("Android sessions with >=2 unique stories:", len(session_sequences))
session_sequences.head()

# ==== cell 34 ====
# cell 17 (Q3)
seq_exploded = session_sequences[["session_id", "tour_id", "story_seq"]].explode("story_seq")
seq_exploded["position"] = seq_exploded.groupby("session_id").cumcount() + 1
seq_exploded = seq_exploded.rename(columns={"story_seq": "story_id"})

canonical_positions = (
    seq_exploded
    .groupby(["tour_id", "story_id"], as_index=False)["position"]
    .median()
    .sort_values(["tour_id", "position", "story_id"])
)
canonical_positions["canonical_rank"] = canonical_positions.groupby("tour_id").cumcount() + 1

rank_map = {
    (int(row.tour_id), int(row.story_id)): int(row.canonical_rank)
    for row in canonical_positions.itertuples(index=False)
}


def map_to_ranks(tour_id, seq):
    tid = int(tour_id)
    return [rank_map[(tid, int(s))] for s in seq if (tid, int(s)) in rank_map]


def is_monotonic_increasing(values):
    return all(b > a for a, b in zip(values, values[1:]))


session_sequences["canonical_rank_seq"] = session_sequences.apply(
    lambda row: map_to_ranks(row["tour_id"], row["story_seq"]),
    axis=1,
)
session_sequences["follows_common_order"] = session_sequences["canonical_rank_seq"].apply(
    is_monotonic_increasing
)

order_summary = (
    session_sequences["follows_common_order"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .rename_axis("follows_common_order")
    .reset_index(name="share_pct")
)

order_summary

# ==== cell 35 ====
# cell 18 (Q3)
# Event-based jump indicator (secondary metric)
jump_events = ["previous_story", "next_story", "click_story", "tour_item_clicked"]

jump_sessions = (
    analysis_events[
        (analysis_events["platform"] == "ANDROID")
        & (analysis_events["event_name"].isin(jump_events))
        & analysis_events["tour_id"].notna()
    ][["user_key", "tour_id"]]
    .drop_duplicates()
    .assign(has_jump_event=True)
)

session_sequences = session_sequences.merge(
    jump_sessions,
    on=["user_key", "tour_id"],
    how="left",
)

session_sequences["has_jump_event"] = session_sequences["has_jump_event"].eq(True)

jump_summary = (
    session_sequences["has_jump_event"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .rename_axis("has_jump_event")
    .reset_index(name="share_pct")
)

jump_summary

# ==== cell 36 ====
# cell 19 (Q3)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.barplot(
    data=order_summary,
    x="follows_common_order",
    y="share_pct",
    ax=axes[0],
    color="#ff7f0e",
)
axes[0].set_title("Q3: Common order vs jumping (Android)")
axes[0].set_xlabel("Follows common order")
axes[0].set_ylabel("Session share (%)")

sns.barplot(
    data=jump_summary,
    x="has_jump_event",
    y="share_pct",
    ax=axes[1],
    color="#d62728",
)
axes[1].set_title("Q3: Use of jump navigation events")
axes[1].set_xlabel("Has jump events")
axes[1].set_ylabel("Session share (%)")

plt.tight_layout()
plt.show()

# ==== cell 38 ====
# cell 20a (Q3 cross-platform proxy)
proxy_entry_events = [
    "play",
    "pause",
    "forward_10",
    "backward_10",
    "previous_story",
    "click_progress_bar",
    "story_listened_20",
    "story_listened_40",
    "story_listened_60",
    "story_listened_80",
    "story_completed",
]

proxy_story_events = (
    analysis_events[
        analysis_events["event_name"].isin(proxy_entry_events)
        & analysis_events["tour_id"].notna()
        & analysis_events["story_id"].notna()
    ][["user_key", "tour_id", "tour_title", "story_id", "event_timestamp", "platform"]]
    .copy()
)

proxy_story_events["tour_id"] = proxy_story_events["tour_id"].astype("Int64")
proxy_story_events["story_id"] = proxy_story_events["story_id"].astype("Int64")

session_sequences_proxy = (
    proxy_story_events.sort_values(["user_key", "tour_id", "event_timestamp"])
    .groupby(["user_key", "tour_id", "tour_title"])["story_id"]
    .apply(unique_in_order)
    .reset_index(name="story_seq")
)

session_sequences_proxy["n_unique_stories"] = session_sequences_proxy["story_seq"].str.len()
session_sequences_proxy = session_sequences_proxy[
    session_sequences_proxy["n_unique_stories"] >= 2
].reset_index(drop=True)
session_sequences_proxy["session_id"] = session_sequences_proxy.index

# platform at first proxy touch for the journey
session_platform_proxy = (
    proxy_story_events.sort_values(["user_key", "tour_id", "event_timestamp"])
    .groupby(["user_key", "tour_id"], as_index=False)["platform"]
    .first()
    .rename(columns={"platform": "journey_platform"})
)

session_sequences_proxy = session_sequences_proxy.merge(
    session_platform_proxy,
    on=["user_key", "tour_id"],
    how="left",
)

seq_exploded_proxy = session_sequences_proxy[["session_id", "tour_id", "story_seq"]].explode("story_seq")
seq_exploded_proxy["position"] = seq_exploded_proxy.groupby("session_id").cumcount() + 1
seq_exploded_proxy = seq_exploded_proxy.rename(columns={"story_seq": "story_id"})

canonical_positions_proxy = (
    seq_exploded_proxy
    .groupby(["tour_id", "story_id"], as_index=False)["position"]
    .median()
    .sort_values(["tour_id", "position", "story_id"])
)
canonical_positions_proxy["canonical_rank"] = canonical_positions_proxy.groupby("tour_id").cumcount() + 1

rank_map_proxy = {
    (int(row.tour_id), int(row.story_id)): int(row.canonical_rank)
    for row in canonical_positions_proxy.itertuples(index=False)
}


def map_to_ranks_proxy(tour_id, seq):
    tid = int(tour_id)
    return [rank_map_proxy[(tid, int(s))] for s in seq if (tid, int(s)) in rank_map_proxy]


session_sequences_proxy["canonical_rank_seq"] = session_sequences_proxy.apply(
    lambda row: map_to_ranks_proxy(row["tour_id"], row["story_seq"]),
    axis=1,
)
session_sequences_proxy["follows_common_order_proxy"] = session_sequences_proxy[
    "canonical_rank_seq"
].apply(is_monotonic_increasing)

order_summary_proxy = (
    session_sequences_proxy["follows_common_order_proxy"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .rename_axis("follows_common_order_proxy")
    .reset_index(name="share_pct")
)

order_summary_proxy_by_platform = (
    session_sequences_proxy
    .groupby(["journey_platform", "follows_common_order_proxy"], as_index=False)
    .size()
    .rename(columns={"size": "sessions"})
)
order_summary_proxy_by_platform["share_pct"] = (
    order_summary_proxy_by_platform["sessions"]
    / order_summary_proxy_by_platform.groupby("journey_platform")["sessions"].transform("sum")
    * 100
).round(2)

print("Cross-platform proxy sessions (>=2 stories):", len(session_sequences_proxy))
print("Sessions by platform:")
print(session_sequences_proxy["journey_platform"].value_counts())
order_summary_proxy

# ==== cell 39 ====
# cell 20b (Q3 cross-platform proxy)
# Event-based jump indicator (secondary metric)
jump_events_proxy = ["previous_story", "next_story", "click_story", "tour_item_clicked"]

jump_sessions_proxy = (
    analysis_events[
        analysis_events["event_name"].isin(jump_events_proxy)
        & analysis_events["tour_id"].notna()
    ][["user_key", "tour_id"]]
    .drop_duplicates()
    .assign(has_jump_event_proxy=True)
)

session_sequences_proxy = session_sequences_proxy.merge(
    jump_sessions_proxy,
    on=["user_key", "tour_id"],
    how="left",
)
session_sequences_proxy["has_jump_event_proxy"] = session_sequences_proxy[
    "has_jump_event_proxy"
].eq(True)

jump_summary_proxy = (
    session_sequences_proxy["has_jump_event_proxy"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .rename_axis("has_jump_event_proxy")
    .reset_index(name="share_pct")
)

jump_summary_proxy_by_platform = (
    session_sequences_proxy
    .groupby(["journey_platform", "has_jump_event_proxy"], as_index=False)
    .size()
    .rename(columns={"size": "sessions"})
)
jump_summary_proxy_by_platform["share_pct"] = (
    jump_summary_proxy_by_platform["sessions"]
    / jump_summary_proxy_by_platform.groupby("journey_platform")["sessions"].transform("sum")
    * 100
).round(2)

q3_compare = pd.DataFrame(
    {
        "metric": [
            "Follows common order (%)",
            "Has jump event (%)",
            "Sessions analyzed",
        ],
        "Q3 strict (Android + story_start)": [
            float(order_summary.loc[order_summary["follows_common_order"] == True, "share_pct"].iloc[0]),
            float(jump_summary.loc[jump_summary["has_jump_event"] == True, "share_pct"].iloc[0]),
            int(len(session_sequences)),
        ],
        "Q3 proxy (Android + iOS)": [
            float(order_summary_proxy.loc[order_summary_proxy["follows_common_order_proxy"] == True, "share_pct"].iloc[0]),
            float(jump_summary_proxy.loc[jump_summary_proxy["has_jump_event_proxy"] == True, "share_pct"].iloc[0]),
            int(len(session_sequences_proxy)),
        ],
    }
)

q3_compare

# ==== cell 40 ====
# cell 20c (Q3 cross-platform proxy)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.barplot(
    data=order_summary_proxy,
    x="follows_common_order_proxy",
    y="share_pct",
    ax=axes[0],
    color="#1f77b4",
)
axes[0].set_title("Q3 proxy: Common order vs jumping (cross-platform)")
axes[0].set_xlabel("Follows common order (proxy)")
axes[0].set_ylabel("Session share (%)")

sns.barplot(
    data=jump_summary_proxy,
    x="has_jump_event_proxy",
    y="share_pct",
    ax=axes[1],
    color="#d62728",
)
axes[1].set_title("Q3 proxy: Use of jump navigation events")
axes[1].set_xlabel("Has jump events (proxy)")
axes[1].set_ylabel("Session share (%)")

plt.tight_layout()
plt.show()

# ==== cell 42 ====
# cell A1 (Appendix drop-off)
funnel_thresholds = [
    ("Started journey (>=0%)", 0),
    ("Reached 20%", 20),
    ("Reached 40%", 40),
    ("Reached 60%", 60),
    ("Reached 80%", 80),
    ("Completed (100%)", 100),
]

funnel_rows = []
for stage, threshold in funnel_thresholds:
    if threshold == 100:
        count = (journey_progress["max_depth"] == 100).sum()
    else:
        count = (journey_progress["max_depth"] >= threshold).sum()

    funnel_rows.append({"stage": stage, "tour_journeys": int(count)})

funnel_df = pd.DataFrame(funnel_rows)
funnel_df["dropoff_from_prev_pct"] = (
    1 - funnel_df["tour_journeys"] / funnel_df["tour_journeys"].shift(1)
).mul(100).round(2)
funnel_df.loc[0, "dropoff_from_prev_pct"] = 0.0

funnel_df

# ==== cell 43 ====
# cell A2 (Appendix drop-off)
plt.figure(figsize=(9, 5))
sns.barplot(data=funnel_df, x="stage", y="tour_journeys", color="#2ca02c")
plt.title("Appendix: Drop-off by listening stage")
plt.xlabel("Stage")
plt.ylabel("Tour journeys")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.show()

dropoff_peak = funnel_df.iloc[1:].sort_values("dropoff_from_prev_pct", ascending=False).head(1)
dropoff_peak

# ==== cell 44 ====
# cell 20 (final summary for 3 required questions)
q1_reached_journey_rate = round(journey_progress["reached_tour_end"].mean() * 100, 2)
q1_abandoned_journey_rate = round(100 - q1_reached_journey_rate, 2)
q1_reached_user_rate = round(q1_reached_users / q1_total_users * 100, 2)
q1_abandoned_user_rate = round(100 - q1_reached_user_rate, 2)

q2_active_share = float(
    q2_mode_dist.loc[q2_mode_dist["listening_mode"] == "Active listening", "share_pct"].iloc[0]
)
q2_passive_share = float(
    q2_mode_dist.loc[q2_mode_dist["listening_mode"] == "Passive play", "share_pct"].iloc[0]
)
q2_active_reach_end = float(
    q2_completion.loc[q2_completion["listening_mode"] == "Active listening", "reach_end_rate_pct"].iloc[0]
)
q2_passive_reach_end = float(
    q2_completion.loc[q2_completion["listening_mode"] == "Passive play", "reach_end_rate_pct"].iloc[0]
)

q3_strict_follow = float(
    order_summary.loc[order_summary["follows_common_order"] == True, "share_pct"].iloc[0]
)
q3_proxy_follow = float(
    order_summary_proxy.loc[order_summary_proxy["follows_common_order_proxy"] == True, "share_pct"].iloc[0]
)

summary = pd.DataFrame(
    {
        "metric": [
            "Q1 - Journeys reached tour end (%)",
            "Q1 - Journeys abandoned before end (%)",
            "Q1 - Users reached end at least once (%)",
            "Q1 - Users only abandoned (%)",
            "Q2 - Active journey share (%)",
            "Q2 - Passive journey share (%)",
            "Q2 - Users with >=1 active journey (%)",
            "Q2 - Users passive-only (%)",
            "Q2 - Reached-end rate (active journeys, %)",
            "Q2 - Reached-end rate (passive journeys, %)",
            "Q3 strict - Follow common order (Android + story_start, %)",
            "Q3 proxy - Follow common order (Android + iOS, %)",
            "Q3 strict - Sessions analyzed",
            "Q3 proxy - Sessions analyzed",
        ],
        "value": [
            q1_reached_journey_rate,
            q1_abandoned_journey_rate,
            q1_reached_user_rate,
            q1_abandoned_user_rate,
            q2_active_share,
            q2_passive_share,
            round(q2_active_users / q2_total_users * 100, 2),
            round(q2_passive_only_users / q2_total_users * 100, 2),
            q2_active_reach_end,
            q2_passive_reach_end,
            q3_strict_follow,
            q3_proxy_follow,
            int(len(session_sequences)),
            int(len(session_sequences_proxy)),
        ],
    }
)

summary

# ==== cell 45 ====
import pandas as pd

# Προσαρμοσέ τα αν έχεις άλλα dataframe names
dfs = {
    "events_clean": events_clean,
    # "bookings": bookings,   # αν υπάρχει
}

# Βάλε εδώ τις στήλες που θες να ελέγξουμε
cols_to_check = [
    "event_name",
    "platform",
    "language",
    "status",
    "booking_status",
    "product_type",
    "channel",
]

out_path = "unique_status_report.txt"

with open(out_path, "w", encoding="utf-8") as f:
    for df_name, df in dfs.items():
        f.write(f"\n=== {df_name} ===\n")
        for col in cols_to_check:
            if col in df.columns:
                f.write(f"\n-- {col} --\n")
                vc = df[col].astype("string").fillna("<NA>").value_counts(dropna=False)
                f.write(vc.to_string())
                f.write("\n")

print("Saved:", out_path)
