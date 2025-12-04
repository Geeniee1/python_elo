from python_elo import data_cleaner, elo_calc


class main(data_cleaner):
    pass
    def __init__(self, league, season):
        self.league = league
        self.season = season
    
    def run_elo_system(self):
        df = data_cleaner.read_match_data(league, season) # read match data
        cleaned_df = data_cleaner.clean_match_data(df) # clean the data
        # odds_tuple = cleaned_df[['AvgH, avgD', 'avgA']]
        teams = ('Arsenal',
                'Aston Villa',
                'Bournemouth',
                'Brentford',
                'Brighton',
                'Chelsea',
                'Crystal Palace',
                'Everton',
                'Fulham',
                'Ipswich',
                'Leicester',
                'Liverpool',
                'Man City',
                'Man United',
                'Newcastle',
                "Nott'm Forest",
                'Southampton',
                'Tottenham',
                'West Ham',
                'Wolves')
        running_elo = {team: 1500 for team in teams} # initialise all teams with 1500 Elo
        for match in cleaned_df.itertuples():
            home_team = match.home_team
            away_team = match.away_team
            home_goals = match.HTG
            away_goals = match.ATG
            result = match.FTR
            odds = (match.AvgH, match.AvgD, match.AvgA)
            delta = elo_calc(home_team, away_team, result, odds)
            running_elo[home_team] += delta
            running_elo[away_team] -= delta
            
            # Here you would implement the Elo calculation logic
            # For example:
            # elo_calc.update_ratings(home_team, away_team, home_goals, away_goals, result, odds_tuple)
        
        
