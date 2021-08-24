
#%% Dictionaries
import pandas as pd
import os 

APP_ROOT = os.path.dirname(os.path.abspath('__file__'))

dict_players = pd.read_excel(os.path.join(APP_ROOT, 'Player_dictionary_final.xlsx'))[['FPL','RW']]
dict_players = dict_players.set_index('FPL')['RW'].to_dict()
dict_players = {v: k for k, v in dict_players.items()}
dict_players_rev  = {v: k for k, v in dict_players.items()}

team_lookup = dict({'ARS': 'Arsenal',
                    'AVL': 'Aston Villa',
                    'BHA': 'Brighton and Hove Albion',
                    'BRE': 'Brentford',
                    'BRN': 'Burnley',
                    'CHE': 'Chelsea',
                    'CRY': 'Crystal Palace',
                    'EVE': 'Everton',
                    'LEE': 'Leeds United',
                    'LEI': 'Leicester City',
                    'LIV': 'Liverpool',
                    'MCI': 'Manchester City',
                    'MUN': 'Manchester United',
                    'NEW': 'Newcastle',
                    'NOR': 'Norwich City',
                    'SOU': 'Southampton',
                    'TOT': 'Tottenham Hotspur',
                    'WAT': 'Watford',
                    'WHU': 'West Ham United',
                    'WOL': 'Wolverhampton'})

team_lookup_num = dict({1: 'Arsenal',
                    2: 'Aston Villa',
                    3: 'Brighton and Hove Albion',
                    4: 'Brentford',
                    5: 'Burnley',
                    6: 'Chelsea',
                    7: 'Crystal Palace',
                    8: 'Everton',
                    9: 'Leicester City',
                    10: 'Leeds United',
                    11: 'Liverpool',
                    12: 'Manchester City',
                    13: 'Manchester United',
                    14: 'Newcastle',
                    15: 'Norwich City',
                    16: 'Southampton',
                    17: 'Tottenham Hotspur',
                    18: 'Watford',
                    19: 'West Ham United',
                    20: 'Wolverhampton'})

team_lookup_num_reverse = {v: k for k, v in team_lookup_num.items()}
team_lookup_reverse  = {v: k for k, v in team_lookup.items()}
position_lookup = dict({1: 'Goalkeeper',
                    2: 'Defense',
                    3: 'Midfield',
                    4: 'Striker'})
