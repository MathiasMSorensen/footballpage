import os 
import pandas as pd
import numpy as np
import random

Data = pd.read_excel(os.path.join(APP_ROOT, 'Model_v6.xlsx'), 'Expected Wins')
Games = pd.read_excel(os.path.join(APP_ROOT, 'Model_v6.xlsx'), 'Games')

teams = Data[['Team', 'Win all']].iloc[0:16]
Games = Games[['home_team','away_team','homeTeamWin','awayTeamWin','draw']]
Games 
# 1/8 Finals 
win_list = []

for i in range(len(Games)):
    home_prop = Games['homeTeamWin'].iloc[i]+Games['draw'].iloc[i]*fulltime_prop(Games['homeTeamWin'].iloc[i])
    away_prop = Games['awayTeamWin'].iloc[i]+Games['draw'].iloc[i]*fulltime_prop(Games['awayTeamWin'].iloc[i])
    
    home_prop_adj = home_prop/(home_prop+away_prop)
    away_prop_adj = away_prop/(home_prop+away_prop)

    if random.uniform(0, 1) < home_prop_adj:
        win_list.append(Games['home_team'].iloc[i])
    else:
        win_list.append(Games['away_team'].iloc[i])

win_list = pd.DataFrame(win_list)
win_list[0]
# Quarter Finals 

Games = {'home_team':  [win_list[0].iloc[0], win_list[0].iloc[1],win_list[0].iloc[4],win_list[0].iloc[6]],
        'away_team': [win_list[0].iloc[2], win_list[0].iloc[3],win_list[0].iloc[5],win_list[0].iloc[7]]
        }

Games = pd.DataFrame(Games, columns = ['home_team','away_team'])









def fulltime_prop(prop):
    full_time_prop = 0.3735+prop*0.3467
    
    return full_time_prop