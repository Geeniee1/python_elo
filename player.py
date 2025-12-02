from python_elo import elo_gainer


class player(elo_gainer):
    def __init__(self, name, team, rating=1500):
        super().__init__(rating, match_week=0)
        self.name = name
        self.team = team