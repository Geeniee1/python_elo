class elo_gainer():
    def __init__(self, elo, match_week):
        self.elo = elo
        self.match_week = match_week
    
    def elo_change(self, previous_elo):
        return self.elo - previous_elo