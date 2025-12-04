class elo_gainer:
    def __init__(self, rating: float, match_week: int):
        self.rating = rating
        self.match_week = match_week

    def elo_change(self, previous_elo: float) -> float:
        return self.rating - previous_elo