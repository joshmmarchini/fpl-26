# FPL Data & Analysis

## FPL-Core-Insights
Sourced from https://github.com/olbauday/FPL-Core-Insights.git
Run `scripts/fetch_data.sh` to download it locally.

## Defining the analytics Problem

### Problem Statement
I want to be able to get an idea of players, by position, I should consider adding or dropping based on their historical performance and upcoming fixtures over the next x game weeks. I also want to identify players with good value - cheap but performing well.

# Getting up to date data
- git pull FPL-Core-Insights
- Execute python script 01_all_playermatchstats.py. This creates 01_all_playermatchstats.csv
- Virtual environment
    - create it (once per project, inside your project folder)
    - Run: python -m venv .venv
    - activate it (every time you open a new terminal)
        - .venv\Scripts\activate           # Windows
    - now installs go into this project only
python -m pip install pandas

pip freeze > requirements.txt      # save what's installed
pip install -r requirements.txt    # reinstall it all elsewhere

pip list                     # what's installed
pip show pandas              # version and details
pip install --upgrade pandas # update to the latest
pip uninstall pandas         # remove it

## Data Dictionary - fwd
Built by `scripts/02_fwd.py` (Premier League forwards only).

| Column | Type | Notes |
| --- | --- |
| gameweek | int64 |
| player_id | int64 |
| match_id | object | First team is always home
| minutes_played | float64 |
| goals | float64 |
| assists | float64 |
| total_shots | float64 |
| xg | float64 |
| xa | float64 |
| shots_on_target | float64 |
| successful_dribbles | float64 | empty
| big_chances_missed | float64 | empty
| touches_opposition_box | float64 |
| touches | float64 |
| accurate_passes | float64 |
| accurate_passes_percent | float64 |
| chances_created | float64 |
| final_third_passes | float64 |
| dribbled_past | float64 |

## Backlog
- Add in trailing 1 gw, 3 gw columns 








