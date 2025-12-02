from python_elo import elo_gainer


class team(elo_gainer):
    def __init__(self, name, rating=1500):
        super().__init__(rating, match_week=0)
        self.name = name