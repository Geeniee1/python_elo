from tokenize import String
from python_elo.player import player
from python_elo.team import team
import pandas as pd
import soccerdata as sd # Dunno why pylance is complaining

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

# TODO add biases to elo calculations
# Teams Elo calculation (does not work for players)

def expected_result(rating1: float, rating2: float, c: float = 400) -> int:
    '''Formula for expected_result according to chess elos '''
    qa = 10 ** (rating1 / c)
    qb = 10 ** (rating2 / c)
    expected_result = qa / (qa + qb)
    return expected_result
# Teams Elo calculation (does not work for players)

def score_bias(home_goals: int, away_goals: int) -> float:
    ''' Calculate bias based on match score'''
    if home_goals + away_goals == 0:
        return 0.5 # Neutral bias for 0-0 draws
    return home_goals / (home_goals + away_goals) # values near 1 for big home wins, near 0 for big losses

def elo_calculation_biased(team1: team, team2: team, result: str, bias: float, odds: tuple, weighted: bool = False) -> tuple:
    ''' Calculate Elo ratings with bias for home team advantage and match score. Inspired by
    https://stanislav-stankovic.medium.com/elo-rating-system-6196cc59941e. Returns tuple
    (new_home_rating, new_away_rating, delta) where delta is the change in rating for home team.'''
    
    rh = team1.rating
    ra = team2.rating
    home_advantage = 0 if not weighted else bias
    c = 400 # scale factor
    expected_result = expected_result(rh + home_advantage, ra, c) # SH
    K = 32 # K-factor
    result_value = {'H': 1, 'D': 0.5, 'A': 0}[result] # Convert result to 1, 0, 0.5
    new_home_rating = rh + K * (result_value - expected_result)
    delta = new_home_rating - rh
    
    return (team1.rating + delta, team2.rating + delta, delta)

# write a function to display current Elo ratings
# write tests for the main functionalities
# write documentation for the main module
# update readme file
# implement error handling and logging
# visualise Elo rating changes over time as graph and as table
# optimise code for performance if necessary
