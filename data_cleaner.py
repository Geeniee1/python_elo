from tokenize import String
from python_elo.player import player
from python_elo.team import team
import pandas as pd
import soccerdata as sd # Dunno why pylance is complaining
from python_elo.elo_calc import elo_calc

class data_cleaner(player, team):
    class league():
        def __init__(self, name: str, teams: list, mathweek: int):
            self.name = name
            self.teams = teams
            self.matchweek = mathweek
    def __init__(self, league, season):
        self.league = league
        self.season = season
        # Additional initialization code can be added here

    # TODO Let's start with season 24/25
    # load data using soccerdata

    def read_match_data(leagues = "ENG-Premier League", seasons = 24) -> pd.DataFrame:
        # Example function to read match data
        data = sd.MatchHistory(leagues="ENG-Premier League", seasons=24)
        return data.read_games()

    def clean_match_data(df: pd.DataFrame) -> pd.DataFrame:
        # HTG = Home Team Goals, ATG = Away Team Goals, FTR = Full Time Result
        # mean_home = AvgH
        # mean_away = AvgA
        # mean_draw = AvgD

        df = df[['home_team', 'away_team','HTG', 'ATG', 'FTR', 'AvgH', 'AvgD', 'AvgA']]
        return df

    df = read_match_data() # read math data for 24/25 premier league
    df = clean_match_data(df) # clean the data to only save the teams playing in the game, and result

    def print_elo(self, mathweek: int) -> str:
        ''' Function to print Elo ratings for all teams after a given matchweek'''
        for team in league.teams:
            print(f"Matchweek {self.matchweek}: Team {team.name} has Elo rating {team.rating}")
        
    
    



# write tests for the main functionalities
# write documentation for the main module
# update readme file
# implement error handling and logging
# visualise Elo rating changes over time as graph and as table
# optimise code for performance if necessary
