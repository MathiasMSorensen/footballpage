# import pandas as pd
# import numpy as np
# from urllib.request import urlopen
# import json
# from datetime import datetime, timedelta
# from difflib import get_close_matches
# import os 
# from utils import team_forecast, player_forecast, get_BPS_rank, calculate_BPS, calculate_expected_points
# from Pulp_optimization import Pulp_optimization
# from dictionaries import dict_players_rev, team_lookup, dict_players, team_lookup_num, team_lookup_num_reverse, position_lookup
# import requests
# from assumptions import current_round , forecast_window , discount_factor , sub_1_discount , sub_2_discount , sub_3_discount ,sub_gk_discount ,cash, date
# import math
import pandas as pd
import os 

APP_ROOT = os.path.dirname(os.path.abspath('__file__'))

# #%% Load data:

# ### FPL fantasy data:
# url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
# response = urlopen(url)
  
# data_json = json.loads(response.read())

# data_df = pd.DataFrame(data_json["elements"])

# col_list = ['first_name',
#             'second_name',
#             'team',
#             'element_type',
#             'now_cost',
#             'selected_by_percent',
#             'transfers_in',
#             'transfers_out',
#             'web_name',
#             'chance_of_playing_next_round']

# data_df = data_df[col_list]

# data_df['Player'] = data_df['first_name'] + ' ' + data_df['second_name']

# fpl = data_df[['Player', 'team', 'element_type', 'now_cost','web_name']].copy(deep=True)

# ### Rotowire:

# import mechanize
# from http.cookiejar import LWPCookieJar
# import requests
# import json

# browser = mechanize.Browser()
# cj = LWPCookieJar()
# browser.set_cookiejar(cj)
# browser.set_handle_equiv(True)
# browser.set_handle_redirect(True)
# browser.set_handle_robots(False)
# browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# browser.open('http://www.rotowire.com/users/loginnow.htm')
# browser.select_form(nr = 0)
# browser.form['username'] = 'mklarskov'
# browser.form['password'] = 'mads1234'
# browser.submit()
# url = browser.open('https://www.rotowire.com/soccer/tables/projections.php?position=All&league=EPL&type=weekly&myLeagueID=0')
# json_file_rw = url.read()

# js_read = json.loads(json_file_rw.decode('utf-8'))
# rw_data = pd.DataFrame(js_read)

# rw = rw_data[['player', 'team',  'opp','position', 'minutes', 'goals', 'assists', 'shots', 'sog', 'chancecreated',\
#          'passes', 'totalpasses', 'crosses', 'accucrosses', 'aerials','dribbles', 'dispossessed','int','tackles',\
#          'tackleswon', 'blocks','clearances', 'cleansheet', 'goalsconc', 'saves', 'fouldrawn','foulscommit', 'yellowcard', 'redcard']]

# rw.columns = ['Player', 'Team', 'Opp', 'Pos', 'MIN', 'G', 'A', 'S', 'SOG', 'CC', 'P',
#        'AP', 'CR', 'ACR', 'AW', 'DR', 'DSP', 'INT', 'TKL', 'TKLW', 'BLK', 'CL',
#        'CS', 'GC', 'SV', 'FS', 'FC', 'Y', 'R']

# # APP_ROOT = os.path.dirname(os.path.abspath('__file__'))
# # rw1 = pd.read_excel(os.path.join(APP_ROOT, 'soccer-projections.xlsx'), header=1)
# rw_teams = pd.DataFrame(rw.Team.unique(), columns=['Team'])
### FiveThirtyEight:
# For automation
# url="https://projects.fivethirtyeight.com/soccer-api/club/spi_matches_latest.csv"
# fte=pd.read_csv(url)
# fte=fte[((fte['league']=='Barclays Premier League') & (fte['season']==2021))]
# fte = fte[['date', 'league_id', 'league', 'team1', 'team2', 'spi1', 'spi2',
#        'prob1', 'prob2', 'probtie', 'proj_score1', 'proj_score2']]
# fte = fte.reset_index(drop=True)
# # fte = pd.read_excel(os.path.join(APP_ROOT, 'FiveThirtyEight.xlsx')).columns
# fte['date'] = pd.to_datetime(fte['date'])
# fte['round'] = None
# for i in range(0,len(fte)):
#     if(i==0):
#         fte.loc[i,'round'] = 1
#     else:
#         if(fte.loc[i,'date'] - fte.loc[i-1,'date'] > timedelta(days=2)):
#             fte.loc[i,'round'] = fte.loc[i-1,'round'] + 1
#         else:
#             fte.loc[i,'round'] = fte.loc[i-1,'round']

# fte_to_web_xg = []
# fte_to_web_xw = []
# fte_to_web_cs = []
# for team in fte['team1'].unique():
    
#     fte_temp = fte[((fte['team1']==team) | (fte['team2']==team))][0:6].reset_index(drop=True)
#     fte_temp = fte_temp[fte_temp['round'].isin(range(current_round,current_round+6,1))]
#     temp_xg = []
#     temp_xw = []
#     temp_cs = []
    
#     for i in range(6):
#         temp_xw.append(np.where(fte_temp['team1']==team,round(fte_temp['prob1'],2),round(fte_temp['prob2'],2)).tolist()[i])
#         temp_xg.append(np.where(fte_temp['team1']==team,round(fte_temp['proj_score1'],2),round(fte_temp['proj_score2'],2)).tolist()[i])
#         temp_cs.append(np.where(fte_temp['team1'][i]==team,round(math.exp(-1*fte_temp['proj_score2'][i]),2), round(math.exp(-1*fte_temp['proj_score1'][i]),2)).tolist())

#     temp_xg.append(team)
#     temp_xw.append(team)
#     temp_cs.append(team)
    
#     fte_to_web_xg.append(temp_xg)
#     fte_to_web_xw.append(temp_xw)
#     fte_to_web_cs.append(temp_cs)

# fte_to_web_xg = pd.DataFrame(fte_to_web_xg).sort_values(by=6)
# fte_to_web_xw = pd.DataFrame(fte_to_web_xw).sort_values(by=6)
# fte_to_web_cs = pd.DataFrame(fte_to_web_cs).sort_values(by=6)

# fte_to_web_xg.to_csv('fte_to_web_xg')
# fte_to_web_xw.to_csv('fte_to_web_xw')
# fte_to_web_cs.to_csv('fte_to_web_cs')

fte_to_web_xg = pd.read_csv(os.path.join(APP_ROOT, 'fte_to_web_xg'))
fte_to_web_xw = pd.read_csv(os.path.join(APP_ROOT, 'fte_to_web_xw'))
fte_to_web_cs = pd.read_csv(os.path.join(APP_ROOT, 'fte_to_web_cs'))

# # #%% Merge data:
# # #merge with fpl data

# for i in range(len(rw)):
#     df_player = player_forecast(rw.iloc[i,:], fte, current_round, forecast_window, team_lookup)
#     avoid_bps = 0
#     df_player['BPS'] = None
#     if rw.loc[i,:]['Player'] in dict_players_rev.values():
#         df_player['fpl_name'] = dict_players[rw.loc[i,:]['Player']]
#         df_player['position'] = position_lookup[int(fpl['element_type'][fpl['Player'] == df_player['fpl_name'][1]])]
#         df_player['cost'] = int(fpl['now_cost'][fpl['Player'] == df_player['fpl_name'][1]])
#         df_player['team'] = int(fpl['team'][fpl['Player'] == df_player['fpl_name'][1]])
#     else:
#         avoid_bps = 1

#     if avoid_bps == 0:
#         for j in range(len(df_player)):
#             df_player.loc[j+1,'BPS']= calculate_BPS(df_player,j+1)

#         if i == 0:
#             master_data = df_player
#         else: 
#             master_data = pd.concat([master_data,df_player], axis = 0)

# master_data.iloc[:,0:24] = master_data.iloc[:,0:24].astype('float')
# master_data = master_data.reset_index()
# master_data['BPS_rank'] = None
# master_data['Opponent_num'] = None
# master_data['Expected_Points'] = None
# master_data['Expected_Points_discounted'] = None
# master_data['Expected_Points_round1'] = None

# for i in range(len(master_data)):
#     master_data.loc[i, 'Opponent_num'] = team_lookup_num_reverse[master_data['Opponent'][i]]
#     master_data.loc[i, 'BPS_rank'] = get_BPS_rank(master_data, master_data.loc[i,'fpl_name'], master_data.loc[i,'team'], master_data.loc[i,'Opponent_num'], master_data.loc[i,'round'])
#     master_data.loc[i, 'Expected_Points'] = calculate_expected_points(master_data, master_data.loc[i,'fpl_name'], master_data.loc[i,'round'], i)
#     master_data.loc[i, 'Expected_Points_discounted'] = master_data.loc[i, 'Expected_Points']*(discount_factor**(int(master_data.loc[i,'round'])-1))
#     if master_data.loc[i,'round']==1:
#         master_data.loc[i, 'Expected_Points_round1'] = master_data.loc[i, 'Expected_Points']
#     else: 
#         master_data.loc[i, 'Expected_Points_round1'] = 0


# Player_stats = master_data[['fpl_name','Expected_Points','team','round']].groupby(['fpl_name','team','round']).sum()
# Player_stats.to_csv('Player_stats')
Player_stats = pd.read_csv(os.path.join(APP_ROOT, 'Player_stats'))
# master_data = master_data[['fpl_name','Expected_Points_discounted','team','cost','position','Expected_Points_round1']].groupby(['fpl_name','team','cost','position']).sum()
# master_data = master_data.reset_index()

# # make list of players not part of the RW
# residual_players = fpl
# residual_players['Expected_Points_discounted'] = 0 
# residual_players['Expected_Points_round1'] = 0 
# residual_players = residual_players[np.where(fpl['Player'].isin(master_data['fpl_name']), False, True)]
# residual_players = residual_players[['Player','team','now_cost','element_type','Expected_Points_discounted','Expected_Points_round1']]
# residual_players = residual_players.reset_index(drop=True)
# for i in range(len(residual_players)):
#     residual_players.loc[i,'element_type'] = position_lookup[residual_players.loc[i,'element_type']]

# residual_players.columns = master_data.columns
# data_final = pd.concat([master_data.reset_index(drop=True),residual_players.reset_index(drop=True)],axis=0).reset_index(drop=True)

# data_final.to_csv('data_final')
data_final = pd.read_csv(os.path.join(APP_ROOT, 'data_final'))
N = len(data_final)
# print(data_final.sort_values('Expected_Points_discounted',ascending=False)[0:30])

# %% optimize team

# squad_old_index = ['Alisson Ramses Becker', 'Benjamin Chilwell', 'Trent Alexander-Arnold', 'Vladimir Coufal', 'Mason Greenwood', 'Bruno Miguel Borges Fernandes', 'Daniel James', 'Diogo Jota', 'Harvey Barnes', 'Michail Antonio', 'Timo Werner', 'Ben Foster', 'Joël Veltman', 'Rodrigo Moreno', 'Daniel Amartey']

# included_players = ['']

# excluded_players = ['']

# cash = 1000 - sum(data_final['cost'][data_final['fpl_name'].isin(squad_old_index)])

# N = len(data_final)
# results = []
# for i in range(7):
#     n_transfers_loop = i 
#     try:
#         expected_points = Pulp_optimization(list(data_final['team']), N, data_final, list(data_final['cost']), list(data_final['cost']), \
#                                             list(data_final['Expected_Points_discounted']), list(data_final['position']), excluded_players, included_players, [], \
#                                             cash, list(data_final['fpl_name']), list(data_final['Expected_Points_discounted']), n_transfers_loop, \
#                                             squad_old_index, sub_1_discount, sub_2_discount,sub_3_discount, sub_gk_discount)
#     except:
#         expected_points = 0

#     results.append([n_transfers_loop,expected_points,int(np.where(n_transfers_loop>n_transfer,(expected_points)+(n_transfers_loop-n_transfer)*cost_of_transfer,expected_points))])

# results = pd.DataFrame(results)
# results.columns = ['n_transfers','total_points','with_transfer_cost']
# print(results)

# suggested_transfers = int(results.n_transfers[results.with_transfer_cost == max(results.with_transfer_cost)])

# #%%

# Output_list, cost_squad_list, nShare_list, Budget_list = Pulp_optimization(list(data_final['team']), N, data_final, list(data_final['cost']), list(data_final['cost']), \
#                                             list(data_final['Expected_Points_discounted']), list(data_final['position']), excluded_players, included_players, [], \
#                                             0, list(data_final['fpl_name']), list(data_final['Expected_Points_round1']), 1, \
#                                             squad_old_index, sub_1_discount, sub_2_discount,sub_3_discount, sub_gk_discount)
