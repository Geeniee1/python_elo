import pandas as pd
import soccerdata as sd


class MatchDataProvider:
    def __init__(self, league: str = "ENG-Premier League", season: int = 24):
        self.league = league
        self.season = season

    def read(self) -> pd.DataFrame:
        mh = sd.MatchHistory(leagues=self.league, seasons=self.season)
        return mh.read_games()

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        return df[[
            'home_team', 'away_team', 'HTG', 'ATG', 'FTR', 'AvgH', 'AvgD', 'AvgA', 'Date', 'MW'
        ]].rename(columns={
            'HTG': 'home_goals',
            'ATG': 'away_goals',
            'FTR': 'result',
            'AvgH': 'avgH',
            'AvgD': 'avgD',
            'AvgA': 'avgA',
            'Date': 'date',
            'MW': 'matchweek'
        })
