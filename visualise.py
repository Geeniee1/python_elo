from matplotlib import pyplot as plt
import pandas as pd


class Visualise:
    def season_table(self, df: pd.DataFrame, matchweek: int) -> pd.DataFrame:
        snap = df[df["matchweek"] == matchweek][["home", "home_elo_after", "away", "away_elo_after"]]
        teams = pd.concat([
            snap[["home", "home_elo_after"]].rename(columns={"home": "team", "home_elo_after": "elo"}),
            snap[["away", "away_elo_after"]].rename(columns={"away": "team", "away_elo_after": "elo"})
        ])
        return teams.groupby("team", as_index=False)["elo"].last().sort_values("elo", ascending=False)

    def elo_progression(self, df: pd.DataFrame, team_name: str):
        team_rows = df[(df["home"] == team_name) | (df["away"] == team_name)].copy()
        team_rows["team_elo_after"] = team_rows.apply(
            lambda r: r["home_elo_after"] if r["home"] == team_name else r["away_elo_after"], axis=1
        )
        plt.figure(figsize=(10, 4))
        plt.plot(team_rows["matchweek"], team_rows["team_elo_after"], marker="o")
        plt.title(f"Elo progression: {team_name}")
        plt.xlabel("Matchweek")
        plt.ylabel("Elo")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def elo_progression_all_teams(self, df: pd.DataFrame, teams: list[str]):
        plt.figure(figsize=(12, 6))
        for t in teams:
            team_rows = df[(df["home"] == t) | (df["away"] == t)].copy()
            if team_rows.empty:
                continue
            team_rows["team_elo_after"] = team_rows.apply(
                lambda r: r["home_elo_after"] if r["home"] == t else r["away_elo_after"], axis=1
            )
            plt.plot(team_rows["matchweek"], team_rows["team_elo_after"], label=t, alpha=0.7)
        plt.title("Elo progression: all teams")
        plt.xlabel("Matchweek")
        plt.ylabel("Elo")
        plt.grid(True)
        plt.legend(ncol=2, fontsize=8)
        plt.tight_layout()
        plt.show()