from python_elo import elo_gainer


class Team(elo_gainer):
    def __init__(self, name: str, rating: float = 1500.0):
        super().__init__(rating, match_week=0)
        self.name = name
        self.history = []  # [{matchweek, date, elo_before, elo_after, delta}]

    def record(self, matchweek: int, date, elo_before: float, elo_after: float):
        self.history.append({
            "matchweek": matchweek,
            "date": date,
            "elo_before": elo_before,
            "elo_after": elo_after,
            "delta": elo_after - elo_before,
        })

    def elo_at(self, matchweek: int) -> float:
        if not self.history:
            return self.rating
        last = self.rating
        for h in self.history:
            if h["matchweek"] > matchweek:
                break
            last = h["elo_after"]
        return last