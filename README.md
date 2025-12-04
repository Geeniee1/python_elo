# Python Elo — Premier League 2024/25

## Project Status
- Purpose: compute Elo ratings for Premier League 2024/25 using match results and odds fetched via `soccerdata`.
- Current: core class skeleton (`Team`, `EloCalc`, `Season`, `MatchDataProvider`) and notebook examples. The pipeline ingests EPL 24/25 with `MatchHistory`, computes per‑match Elo deltas, builds a timeline DataFrame, and can export CSV.
- Next: CLI to run from terminal, richer visualizations, support for players and other leagues/sports, configurable constants (K, scale), and persistent stores (CSV/Parquet/SQLite/JSON).

## Vision
- Reusable Elo engine for teams/players across seasons, leagues, and sports.
- Clean CLI to fetch data, run ratings, and visualize tables/graphs.
- Persist per‑matchweek snapshots so Elo at any time is queryable.
- Base class (`EloEntity`) with `Team`/`Player` inheritance to keep logic consistent.

## Setup
On macOS (zsh), use a virtual environment and install dependencies:

```bash
cd /Users/edwind/Desktop/python_elo
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install soccerdata pandas matplotlib
```

Notes:
- `soccerdata` aggregates multiple sources; the `MatchHistory` provider uses football-data.co.uk.
- Ensure VS Code selects the `.venv` interpreter (`Python: Select Interpreter`).

## Run
From Python or VS Code:

```python
from python_elo.main import run_premier_league_2425
df = run_premier_league_2425()
print(df.head())
```

Outputs:
- `elo_ENG_Premier_2024_25.csv` — per‑match Elo changes and snapshots (date, matchweek, teams, goals, odds, before/after ratings, deltas).

CLI:
```bash
python -m python_elo.cli --league "ENG-Premier League" --season 24 --k 20 --home-advantage 0 --out elo_ENG_Premier_2024_25.csv
```
This will run the season and save the timeline CSV to the path you specify.

## Data Sources
- `MatchHistory` reference: https://www.football-data.co.uk/
- `soccerdata` docs: https://soccerdata.readthedocs.io/en/latest/reference/index.html
- League key used: `ENG-Premier League`, season `24` for 2024/25.

## Credits
- `soccerdata` (Pieter Robberechts et al.): data ingestion wrappers and provider integrations.
- `MatchHistory`: EPL data aligned with football-data.co.uk.
- Elo methodology inspiration: Stanislav Stankovic — https://stanislav-stankovic.medium.com/elo-rating-system-6196cc59941e
- Community libraries (`pandas`, `requests`, etc.) used transitively via `soccerdata`.

## Licensing
- This project: MIT License (see `../LICENSE`).
- `soccerdata` licensing: Apache License 2.0 — you may not use their files except in compliance with that License. See their docs/repo for full terms.

## Roadmap
- CLI: `python -m python_elo` with flags `--league`, `--season`, `--k`, `--scale`, `--home-advantage`.
- Players: add `Player(EloEntity)` and mixed-entity support.
- Multi‑league/sport: adapter layer to normalize different provider schemas; Elo logic remains the same.
- Visualization: season tables, single/all‑team progression plots.
- Storage: CSV/Parquet snapshots; optional SQLite for fast queries across seasons.
# python_elo
Elo rating system for top sports leagues across seasons*
