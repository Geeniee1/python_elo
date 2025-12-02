from python_elo.player import player
from python_elo.team import team
import pandas as pd
import soccerdata as sd

class main(player, team):
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
    # Example function to clean match data
    df = df[['home_team', 'away_team', 'FTR']]
    return df
df = read_match_data() # read math data for 24/25 premier league
df = clean_match_data(df) # clean the data to only save the teams playing in the game, and result

def elo_calculation(team1, team2, result):
    # Example function to calculate Elo ratings
    
    pass

# write a function to update Elo ratings based on match results
# write a function to display current Elo ratings
# write tests for the main functionalities
# write documentation for the main module
# update readme file
# implement error handling and logging
# visualise Elo rating changes over time as graph and as table
# optimise code for performance if necessary
