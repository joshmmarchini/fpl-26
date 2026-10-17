"""
Combine every gameweek's playermatchstats.csv for a season into one file.

For each GW folder (GW1, GW2, ...) in FPL-Core-Insights/data/<season>/By Gameweek:
  - playermatchstats.csv  -> base rows (one per player per match)
  - players.csv           -> joined on player_id (all player info)
  - matches.csv           -> joined on match_id (home/away team, score, xG, tournament)
  - teams.csv             -> team codes mapped to team names

Output: data/01_all_playermatchstats_.csv

Run from anywhere:  python scripts/01_all_playermatchstats.py
"""
import re
from pathlib import Path

import pandas as pd

SEASON = "2026-2027"

ROOT = Path(__file__).resolve().parent.parent
GW_DIR = ROOT / "FPL-Core-Insights" / "data" / SEASON / "By Gameweek"
OUTPUT = ROOT / "data" / "01_all_playermatchstats_.csv"

MATCH_COLS = [
    "match_id",
    "kickoff_time",
    "tournament",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "home_expected_goals_xg",
    "away_expected_goals_xg",
    "finished",
]


def gw_number(path):
    return int(re.search(r"\d+", path.name).group())


def load_gameweek(gw_path):
    stats = pd.read_csv(gw_path / "playermatchstats.csv")
    if stats.empty:
        return None

    players = pd.read_csv(gw_path / "players.csv")
    matches = pd.read_csv(gw_path / "matches.csv", usecols=MATCH_COLS)
    teams = pd.read_csv(gw_path / "teams.csv", usecols=["code", "name"])
    team_names = teams.set_index("code")["name"]

    matches["home_team_name"] = matches["home_team"].map(team_names)
    matches["away_team_name"] = matches["away_team"].map(team_names)
    players["team_name"] = players["team_code"].map(team_names)

    df = (
        stats.merge(players, on="player_id", how="left", validate="many_to_one")
        .merge(matches, on="match_id", how="left", validate="many_to_one")
    )
    df.insert(0, "gameweek", gw_number(gw_path))
    return df


def main():
    gw_paths = sorted(
        (p for p in GW_DIR.iterdir() if p.is_dir() and re.fullmatch(r"GW\d+", p.name)),
        key=gw_number,
    )

    frames = []
    for gw_path in gw_paths:
        df = load_gameweek(gw_path)
        if df is None:
            print(f"{gw_path.name}: no player match stats yet, skipping")
            continue
        print(f"{gw_path.name}: {len(df)} rows")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    combined["season_identifier"] = SEASON

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(combined)} rows x {combined.shape[1]} cols to {OUTPUT}")


if __name__ == "__main__":
    main()

