from tokenize import String
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

def mean(df: pd.DataFrame, column: str) -> float:
    #TODO function to calculate mean of columns for odds
    pass

def read_match_data(leagues = "ENG-Premier League", seasons = 24) -> pd.DataFrame:
    # Example function to read match data
    data = sd.MatchHistory(leagues="ENG-Premier League", seasons=24)
    return data.read_games()

def clean_match_data(df: pd.DataFrame) -> pd.DataFrame:
    # Example function to clean match data
    # HTG = Home Team Goals, ATG = Away Team Goals, FTR = Full Time Result
    # TODO Add clause for retrieving odds data
    # mean_home = mean()
    # mean_away = mean()
    # mean_draw = mean()
    df = df[['home_team', 'away_team','HTG', 'ATG', 'FTR']]
    return df

df = read_match_data() # read math data for 24/25 premier league
df = clean_match_data(df) # clean the data to only save the teams playing in the game, and result

# Teams Elo calculation (does not work for players)
def elo_calculation_unbiased(team1: team, team2: team, result: str, odds: tuple, weighted: bool = False) -> tuple:
    ''' Calculate Elo only taking into account the result of the game'''
    
    return (team1.rating, team2.rating)
# Teams Elo calculation (does not work for players)
def elo_calculation_biased(team1: team, team2: team, result: str, bias: float, odds: tuple, weighted: bool = False) -> tuple:
    ''' Calculate Elo ratings with bias for home team advantage and match score. Inspired by
    https://stanislav-stankovic.medium.com/elo-rating-system-6196cc59941e'''
    
    return (team1.rating, team2.rating)

# write a function to update Elo ratings based on match results
# write a function to display current Elo ratings
# write tests for the main functionalities
# write documentation for the main module
# update readme file
# implement error handling and logging
# visualise Elo rating changes over time as graph and as table
# optimise code for performance if necessary
