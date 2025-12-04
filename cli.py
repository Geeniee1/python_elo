#!/usr/bin/env python3
import argparse
from python_elo.main import Season
import pandas as pd
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Run Elo ratings for a league/season.")
    parser.add_argument("--league", default="ENG-Premier League", help="League key (e.g., ENG-Premier League)")
    parser.add_argument("--season", type=int, default=24, help="Season code (e.g., 24 for 2024/25)")
    parser.add_argument("--k", type=float, default=20.0, help="K-factor")
    parser.add_argument("--scale", type=float, default=400.0, help="Scale (c)")
    parser.add_argument("--home-advantage", type=float, default=0.0, help="Home advantage shift")
    parser.add_argument("--out", default="elo_results.csv", help="Output CSV path")
    parser.add_argument("--plot-team", dest="plot_team", default=None, help="Optional team name to plot Elo progression")
    parser.add_argument("--show", action="store_true", help="Show plot window if plotting")
    args = parser.parse_args()

    season = Season(args.league, args.season)
    season.run(k_factor=args.k, home_advantage=args.home_advantage)
    season.save_csv(args.out)
    print(f"Saved Elo timeline to {args.out}")

    if args.plot_team:
        df = season.to_dataframe()
        sub = df[(df["home"] == args.plot_team) | (df["away"] == args.plot_team)].copy()
        if sub.empty:
            print(f"No matches found for team: {args.plot_team}")
        else:
            sub["elo_after"] = sub.apply(
                lambda r: r["home_elo_after"] if r["home"] == args.plot_team else r["away_elo_after"], axis=1
            )
            sub = sub.sort_values("matchweek")
            plt.figure(figsize=(10, 4))
            plt.plot(sub["matchweek"], sub["elo_after"], marker="o")
            plt.title(f"Elo progression: {args.plot_team}")
            plt.xlabel("Matchweek")
            plt.ylabel("Elo")
            plt.grid(True)
            plt.tight_layout()
            if args.show:
                plt.show()
            else:
                out_png = f"elo_{args.plot_team.replace(' ', '_')}.png"
                plt.savefig(out_png)
                print(f"Saved plot to {out_png}")


if __name__ == "__main__":
    main()
