from python_elo.data_cleaner import MatchDataProvider
from python_elo.elo_calc import EloCalc
from python_elo.team import Team
import pandas as pd


class Season:
    def __init__(self, league: str, season: int, initial_elo: float = 1500.0):
        self.league = league
        self.season = season
        self.initial_elo = initial_elo
        self.teams: dict[str, Team] = {}
        self.matches: pd.DataFrame | None = None
        self.timeline: list[dict] = []

    def ensure_team(self, name: str) -> Team:
        if name not in self.teams:
            self.teams[name] = Team(name=name, rating=self.initial_elo)
        return self.teams[name]

    def load_matches(self):
        provider = MatchDataProvider(self.league, self.season)
        df = provider.read()
        df = provider.clean(df)
        # Should be sorted already but let's try this
        self.matches = df.sort_values(["matchweek", "date"]).reset_index(drop=True)

    def run(self, k_factor: float = 20.0):
        calc = EloCalc(k_factor=k_factor)
        if self.matches is None:
            self.load_matches()
        for _, m in self.matches.iterrows():
            home = self.ensure_team(m["home_team"]) if "home_team" in m else self.ensure_team(m["home"])  # provider normalization
            away = self.ensure_team(m["away_team"]) if "away_team" in m else self.ensure_team(m["away"])  
            # handle column names based on cleaned schema
            home_name = home.name
            away_name = away.name
            hg = int(m.get("home_goals", m.get("HTG", 0)))
            ag = int(m.get("away_goals", m.get("ATG", 0)))
            result = m.get("result", m.get("FTR"))
            odds = (m.get("avgH", m.get("AvgH")), m.get("avgD", m.get("AvgD")), m.get("avgA", m.get("AvgA")))
            mw = int(m.get("matchweek", m.get("MW", 0)))
            date = m.get("date", m.get("Date"))

            elo_before_home = home.rating
            elo_before_away = away.rating

            delta = calc.elo_delta(elo_before_home, elo_before_away, result, odds)

            home.rating = elo_before_home + delta
            away.rating = elo_before_away - delta

            home.record(mw, date, elo_before_home, home.rating)
            away.record(mw, date, elo_before_away, away.rating)

            self.timeline.append({
                "date": date,
                "matchweek": mw,
                "home": home_name,
                "away": away_name,
                "home_goals": hg,
                "away_goals": ag,
                "result": result,
                "avgH": odds[0],
                "avgD": odds[1],
                "avgA": odds[2],
                "home_elo_before": elo_before_home,
                "away_elo_before": elo_before_away,
                "home_elo_after": home.rating,
                "away_elo_after": away.rating,
                "home_elo_change": delta,
                "away_elo_change": -delta,
            })

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.timeline)

    def save_csv(self, path: str):
        self.to_dataframe().to_csv(path, index=False)


def run_premier_league_2425() -> pd.DataFrame:
    season = Season("ENG-Premier League", 24)
    season.run(k_factor=20.0)
    # Save a season-level CSV snapshot
    season.save_csv("elo_ENG_Premier_2024_25.csv")
    return season.to_dataframe()

# write tests for the main functionalities
# write documentation for the main module
# update readme file
# implement error handling and logging
# visualise Elo rating changes over time as graph and as table
# optimise code for performance if necessary
