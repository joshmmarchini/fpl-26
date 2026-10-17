# Read in 01_all_playermatchstats.csv

import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent   # C:\dev\fpl
DATA_PATH = PROJECT_ROOT / "data" / "01_all_playermatchstats_.csv"

data_raw = pd.read_csv(DATA_PATH)

print(data_raw.head())
print(data_raw.columns.tolist())

ID_COLS = ["gameweek", "player_id", "match_id"]

# successful_dribbles and big_chances_missed are never populated, so they are
# not selected here at all
cols = [
    "gameweek", "player_id", "match_id", "minutes_played", "goals", "assists",
    "total_shots", "xg", "xa", "shots_on_target",
    "touches_opposition_box", "touches",
    "accurate_passes", "accurate_passes_percent", "chances_created",
    "final_third_passes", "dribbled_past",
]

fwd = (
    data_raw
    .query("position == 'Forward' and tournament == 'prem'")
    .loc[:, cols]
)

# The feed only writes a count when it is non-zero, so NaN means the player
# recorded none of that event. accurate_passes_percent is excluded: it is a
# ratio, and 0 passes makes it undefined rather than 0.
count_cols = [c for c in cols if c not in ID_COLS + ["accurate_passes_percent"]]
fwd[count_cols] = fwd[count_cols].fillna(0)

# Every stat above is measured in the same match that produced the points, so
# it cannot be used to forecast that match. Shift each one onto later
# gameweeks to give each row only what was known beforehand.
stat_cols = [c for c in cols if c not in ID_COLS]
fwd = fwd.sort_values(["player_id", "gameweek"]).reset_index(drop=True)

prev = fwd.groupby("player_id")[stat_cols].shift(1)
roll3 = (
    prev
    .groupby(fwd["player_id"])
    .rolling(3, min_periods=1)
    .mean()
    .reset_index(level=0, drop=True)
)

# Players who miss a gameweek have no row for it, so "lag1" is their previous
# appearance rather than strictly the previous gameweek.
fwd[[f"{c}_lag1" for c in stat_cols]] = prev
fwd[[f"{c}_roll3" for c in stat_cols]] = roll3

print(fwd.head())
print(fwd.shape)



