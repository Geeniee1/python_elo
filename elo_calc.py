# from bdb import effective
# from matplotlib.pyplot import margins
from python_elo.team import Team

class EloCalc:
    def __init__(self, k_factor: float = 20.0, scale: float = 400.0, home_advantage: float = 0.0):
        self.k = k_factor
        self.scale = scale
        self.h0 = home_advantage

    def expected_result(self, rating1: float, rating2: float) -> float:
        '''Formula for expected_result according to chess elos '''
        qa = 10 ** (rating1 / self.scale)
        qb = 10 ** (rating2 / self.scale)
        expected_result = qa / (qa + qb)
        return expected_result
    # Teams Elo calculation (does not work for players)

    def score_bias(self, home_goals: int, away_goals: int) -> float:
        ''' Calculate bias based on match score'''
        if home_goals + away_goals == 0:
            return 0.5 # Neutral bias for 0-0 draws
        return home_goals / (home_goals + away_goals) # values near 1 for big home wins, near 0 for big losses

    def home_bias(self, result: str) -> float:
        ''' Coefficient for home advantage bias.'''
        gamma = 0.2
        if result == 'H':
            return 1 - gamma
        elif result == 'D':
            return 1
        else: return 1 + gamma

    def score_bias(self, home_goals: int, away_goals: int) -> float:
        ''' Calculate bias based on match score'''
        goal_difference = abs(home_goals - away_goals)
        if goal_difference == 0:
            return 1 # Neutral bias for 0-0 draws
        alpha = 0.2 # can change, let's figure what is best later
        return 1 + alpha * (goal_difference - 1) # greaters difference leads to greater scaling factor. alpha scales

    def odds_bias(self, odds: tuple, SH: float) -> float:
        try:
            home_odds =1/odds[0]
            draw_odds = 1/odds[1]
            away_odds = 1/odds[2]
        except ZeroDivisionError:
            return 1 # neutral bias if odds are zero
        Q = home_odds + draw_odds + away_odds
        home_prob = home_odds/Q
        draw_prob = draw_odds/Q
        away_prob = away_odds/Q
        books_expected_score = home_prob + draw_prob * 0.5 # home_prob * 1, away_prob * 0
        # surprise measure in the sense of how much the result deviated from what bookmakers predicted
        surprise_measure = abs(SH - books_expected_score) # SH is calculated in elo_calc, it is = 1 if home wins, 0 if away wins, 0.5 if draw
        beta = 1 # scaling factor
        return 1 + beta * surprise_measure

    def elo_delta(self, home_rating: float, away_rating: float, result: str, goals: tuple, odds: tuple | None = None) -> float:
        ''' Calculate Elo ratings with bias for home team advantage and match score. Inspired by
        https://stanislav-stankovic.medium.com/elo-rating-system-6196cc59941e. Returns tuple
        (new_home_rating, new_away_rating, delta) where delta is the change in rating for home team.'''

        rh = home_rating + self.h0
        ra = away_rating
        result_value = {'H': 1.0, 'D': 0.5, 'A': 0.0}[result]
        home_expected = self.expected_result(rh, ra) # 1/(1 + 10^((RA - RH')/scale))
        effective_delta = self.k * (result_value - home_expected)

        loc_bias = self.home_bias(result)
        home_goals, away_goals = int(goals[0]), int(goals[1])
        margin_bias = self.score_bias(home_goals, away_goals)# 1.0  # basic; can plug score-based multiplier later
        odds_b = self.odds_bias(odds, result_value) if odds else 1.0

        delta = effective_delta * loc_bias * odds_b * margin_bias
        return delta
