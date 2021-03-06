## Team function

import pandas as pd
import numpy as np
from dictionaries import team_lookup, team_lookup_num, position_lookup
from player_predictions import data_final

def team_forecast(team, fte, current_round, forecast_window):
    Output = pd.DataFrame(index=range(current_round, current_round + forecast_window), 
                            columns = ['xG', 'xG_against', 'xCS', 'xWin', 'Opponent'])
    team_fte = team_lookup[team]
    
    matches = fte.loc[(fte.team1==team_fte) | (fte.team2==team_fte)]
    current_match = matches.loc[fte['round']==current_round]
    
    if(current_match.team1.values==team_fte):
        xG = float(current_match.proj_score1)
        xG_against = float(current_match.proj_score2)
        xCS = float(np.exp(-current_match.proj_score2))
        xWin = float(current_match.prob1)
    else:
        xG = float(current_match.proj_score2)
        xG_against = float(current_match.proj_score1)
        xCS = float(np.exp(-current_match.proj_score1))
        xWin = float(current_match.prob2)
    
    for i in range(current_round , current_round + forecast_window):
        if(matches.team1.loc[fte['round']==i].values==team_fte):
            Output.loc[i,'xG'] = float(matches.loc[matches['round']==i].proj_score1)/xG
            Output.loc[i,'xG_against'] = float(matches.loc[matches['round']==i].proj_score2)/xG_against
            Output.loc[i,'xCS'] = float(np.exp(-matches.loc[matches['round']==i].proj_score2))/xCS
            Output.loc[i,'xWin'] = float(matches.loc[matches['round']==i].prob1)/xWin
            Output.loc[i,'Opponent'] = matches.loc[matches['round']==i].team2.iloc[0]
        else:
            Output.loc[i,'xG'] = float(matches.loc[matches['round']==i].proj_score2)/xG
            Output.loc[i,'xG_against'] = float(matches.loc[matches['round']==i].proj_score1)/xG_against
            Output.loc[i,'xCS'] = float(np.exp(-matches.loc[matches['round']==i].proj_score1))/xCS
            Output.loc[i,'xWin'] = float(matches.loc[matches['round']==i].prob2)/xWin
            Output.loc[i,'Opponent'] = matches.loc[matches['round']==i].team1.iloc[0]
    return Output
       
## Player function
def player_forecast(player, fte, current_round, forecast_window, team_lookup):
    Output = pd.DataFrame(index=range(current_round, current_round + forecast_window),
                          columns=player.index.values[5:])
    Output['Opponent'] = None
    team = player['Team']
    forecast = team_forecast(team, fte, current_round, forecast_window)
    
    Output.loc[current_round,:] = player.loc[player.index.values[5:]]
    Output.loc[current_round,'Opponent'] = team_lookup[player.loc['Opp']]
    Output.loc[current_round,'xG'] = forecast.loc[current_round,'xG']
    Output.loc[current_round,'xG_against'] = forecast.loc[current_round,'xG_against']
    Output.loc[current_round,'xCS'] = forecast.loc[current_round,'xCS']
    Output.loc[current_round,'xWin'] = forecast.loc[current_round,'Opponent']


    for i in range(current_round + 1, current_round + forecast_window):
        Output.loc[i,['G', 'A', 'S', 'SOG', 'CC']] = pd.to_numeric(player.loc[['G', 'A', 'S', 'SOG', 'CC']]) * forecast.loc[i, 'xG']
        Output.loc[i,['TKL', 'TKLW', 'BLK', 'CL', 'GC', 'SV']] = pd.to_numeric(player.loc[['TKL', 'TKLW', 'BLK', 'CL', 'GC', 'SV']]) * forecast.loc[i, 'xG_against']
        Output.loc[i,['CS']] = pd.to_numeric(player.loc[['CS']]) * forecast.loc[i, 'xCS']
        Output.loc[i,['P', 'AP', 'CR', 'ACR', 'AW', 'DR', 'INT', 'FS']] = pd.to_numeric(player.loc[['P', 'AP', 'CR', 'ACR', 'AW', 'DR', 'INT', 'FS']]) * forecast.loc[i, 'xWin']
        Output.loc[i,['DSP', 'FC', 'Y', 'R']] = pd.to_numeric(player.loc[['DSP', 'FC', 'Y', 'R']]) / forecast.loc[i, 'xWin']
        Output.loc[i,'Opponent'] = forecast.loc[i,'Opponent']
        Output.loc[i,'xG'] = forecast.loc[i,'xG']
        Output.loc[i,'xG_against'] = forecast.loc[i,'xG_against']
        Output.loc[i,'xCS'] = forecast.loc[i,'xCS']
        Output.loc[i,'xWin'] = forecast.loc[i,'Opponent']

    Output['round'] = Output.index
    return Output

## BPS
def get_BPS_rank(master_data, relevant_player, relevant_player_team, team_against, game):
    
    df = master_data 

    df = master_data[master_data['round'] == game]
    df = df[(df['team'] == relevant_player_team) | (df['team'] == team_against)]
    bps_score = np.array(df['BPS'])
    ranks = pd.DataFrame((-bps_score).argsort().argsort()) + 1
    bps_score_quad = np.where(ranks[0].isin(np.array(range(6))+1),bps_score**3,0)
    bps_score_final = bps_score_quad/sum(bps_score_quad)*6
    bps_score_final = bps_score_final[(df['fpl_name']==relevant_player).reset_index(drop=True)]
    
    return float(bps_score_final)

def calculate_BPS(df_player,game, index):
    
    df = df_player[df_player['round'] == game]
    bps = 0 

    if df['position'][index] == 'Goalkeeper':
        bps = bps + 6
        bps = bps + float(df['G']) * 12 
        bps = bps + float(df['A']) * 9 
        bps = bps + float(df['CS']) * 12
        bps = bps + float(df['SV']) * 2

    elif df['position'][index] == 'Defense':
        bps = bps + 6
        bps = bps + float(df['G']) * 12 
        bps = bps + float(df['A']) * 9 
        bps = bps + float(df['CS']) * 12

    elif df['position'][index] == 'Midfield':
        bps = bps + 6
        bps = bps + float(df['G']) * 18
        bps = bps + float(df['A']) * 9 

    elif df['position'][index] == 'Striker':
        bps = bps + 6
        bps = bps + float(df['G']) * 24 
        bps = bps + float(df['A']) * 9 
        

    bps = bps + float(df['CR']) * 1
    bps = bps + float(df['CC']) * 3
    bps = bps + int(float(df['BLK']) + float(df['CL']) + float(df['INT']))/2 * 1

    if (float(df['P'])/float(df['AP']) > 0.7) and (float(df['P'])/float(df['AP'])  <= 0.8):
        bps = bps + 2
    elif (float(df['P'])/float(df['AP'])  > 0.8)and (float(df['P'])/float(df['AP'])  <= 0.9):
        bps = bps + 4
    elif (float(df['P'])/float(df['AP'])  > 0.9):
        bps = bps + 6

    bps = bps + float(df['Y']) * -3
    bps = bps + float(df['R'])  * -9   
    
    return bps

## Expected points
def calculate_expected_points(data_master, relevant_player, game, i):

    df = data_master[data_master['round'] == game]
    df = df[df['fpl_name'] == relevant_player]
    expected_points = 0

    if df['position'][i] == 'Goalkeeper':
        expected_points = expected_points + 2 # Points for playing the game
        expected_points = expected_points + df['G'] * 6 
        expected_points = expected_points + df['A'] * 3
        expected_points = expected_points + df['CS'] * 4
        expected_points = expected_points + int(df['SV'])/3 * 1 # every third shot saved by a keeper is awarded
        expected_points = expected_points + df['Y'] * -1
        expected_points = expected_points + df['R'] * -3
        if df['xG_against'][i] >= 2:
            expected_points = expected_points - 1
    elif df['position'][i] == 'Defense':
        expected_points = expected_points + 2 # Points for playing the game
        expected_points = expected_points + df['G'] * 6
        expected_points = expected_points + df['A'] * 3
        expected_points = expected_points + df['CS'] * 4
        expected_points = expected_points + df['Y'] * -1
        expected_points = expected_points + df['R'] * -3
        if df['xG_against'][i] >= 2:
            expected_points = expected_points - 1
    elif df['position'][i] == 'Midfield':
        expected_points = expected_points + 2 # Points for playing the game
        expected_points = expected_points + df['G'] * 5
        expected_points = expected_points + df['A'] * 3
        expected_points = expected_points + df['CS'] * 1
        expected_points = expected_points + df['Y'] * -1
        expected_points = expected_points + df['R'] * -3            
    elif df['position'][i] == 'Striker':
        expected_points = expected_points + 2 # Points for playing the game
        expected_points = expected_points + df['G'] * 4
        expected_points = expected_points + df['A'] * 3
        expected_points = expected_points + df['Y'] * -1
        expected_points = expected_points + df['R'] * -3

    else:
        expected_points = 0
    
    expected_points = df['BPS_rank'][i] + expected_points
    
    return expected_points[i]

# get optimzied results from optimzation
def get_optim_results(Output, PlayerList,data_final):
    if isinstance(Output, pd.DataFrame):
        Squad = list(Output['Names']) 
        Squad_Position = list(Output['Positions']) 
        Squad_Team = list(Output['Teams']) 
        Squad_xPoints = list(round(Output['TotalPoints'],2)) 
        Squad_Captain  = list(Output['Captain']) 
        Expected_points = sum(Output['TotalPoints'])
        buy_list = list(Output[Output['new_old']=="New"]['Names'])
        buy_list_position = list(Output[Output['new_old']=="New"]['Positions'])
        buy_list_Cost =  list(round(Output[Output['new_old']=="New"]['Cost']/10,1))
        buy_list_team = list(Output[Output['new_old']=="New"]['Teams'])
        buy_list_xPoints = list(round(Output[Output['new_old']=="New"]['TotalPoints'],2))
        print(buy_list_xPoints)
        print(Squad_xPoints)

        sell_bool = np.where(pd.DataFrame(PlayerList)[0].isin(Output['Names']), False, True)
        sell_list_names = pd.DataFrame(PlayerList)[sell_bool].reset_index(drop = True)
        sell_list_bool = data_final['fpl_name'].isin(sell_list_names.astype('str')[0])
        sell_list = list(data_final['fpl_name'][sell_list_bool])
        sell_list_position = list(data_final['position'][sell_list_bool]) 
        sell_list_Cost = list(round(data_final['cost'][sell_list_bool]/10,2)) 

        sell_list_team = []
        sell_list_xPoints = []
        sell_list_team_temp = list(data_final['team'][sell_list_bool])
        sell_list_xPoints_temp = list(data_final['Expected_Points_round1'][sell_list_bool])
        for i in range(len(sell_list_team_temp)):
            sell_list_team.append(team_lookup_num[sell_list_team_temp[i]])
            sell_list_xPoints.append(round(sell_list_xPoints_temp[i],1))
        
        New = list(Output['new_old']) 

        return New, Squad, Squad_Position, Squad_Team, Squad_xPoints, Squad_Captain, Expected_points, buy_list, buy_list_position, buy_list_team, buy_list_xPoints, buy_list_Cost, sell_list, sell_list_team, sell_list_position, sell_list_xPoints,sell_list_Cost 
    else:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def get_current_team(username,password):
    
    from dictionaries import team_lookup_num, position_lookup
    import mechanize
    from http.cookiejar import LWPCookieJar
    import requests
    import json
    import pandas as pd
    from urllib.request import urlopen

    print(1)
    browser = mechanize.Browser()
    cj = LWPCookieJar()
    browser.set_cookiejar(cj)
    browser.set_handle_equiv(True)
    browser.set_handle_redirect(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(False)
    browser.open('https://users.premierleague.com/')
    browser.select_form(nr = 0)
    print(username)
    print(password)
    browser.form['login'] = username
    browser.form['password'] = password
    browser.submit()
    try:
        url = browser.open('https://fantasy.premierleague.com/api/me/')
        data_json = json.loads(url.read())
        id_fpl = data_json["player"]['entry']
        
        url = browser.open("https://fantasy.premierleague.com/api/my-team/"+str(id_fpl)+"/")
        data_json = json.loads(url.read())
        data_df = pd.DataFrame(data_json["picks"])
        
        transfers = data_json["transfers"]['limit']
        if transfers == None:
            transfers = 1
        else:
            transfers = transfers
            
        url = browser.open("https://fantasy.premierleague.com/api/entry/"+str(id_fpl)+"/")
        data_json = json.loads(url.read())
        bank = data_json['last_deadline_bank']
        rank = data_json['summary_overall_rank']
        
        if bank == None:
            bank = 0
        else:
            bank = bank/10
        
        if rank == None:
            rank = 7000000
        else:
            rank = rank

        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        response = urlopen(url)
        data_json = json.loads(response.read())
        data_df_fpl = pd.DataFrame(data_json["elements"])
        data_df_fpl['Player'] = data_df_fpl['first_name'] + ' ' + data_df_fpl['second_name']
        
        data_df = data_df.sort_values(['element']).reset_index(drop = True)
        data_df_fpl = data_df_fpl.sort_values(['id']).reset_index(drop = True)

        logical  = pd.DataFrame(np.where(data_df_fpl['id'].isin(data_df['element']),data_df_fpl.index,np.nan))
        logical  = logical.dropna()
        data_df['player'] = data_df_fpl['Player'].loc[logical[0]].reset_index(drop=True)
        data_df['multiplier'] = np.where(data_df['multiplier'] >= 1,0,1)
        data_df['position'] = data_df_fpl['element_type'].loc[logical[0]].reset_index(drop=True)

        data_df = data_df.sort_values(['player']).reset_index(drop = True)
        logical = []
        for i in range(len(data_df)):
            logical.append(data_final.index[data_df['player'].loc[i]== data_final['fpl_name']])

        data_df['team'] = data_final['team'][list(pd.DataFrame(logical)[0])].reset_index(drop=True)
        data_df['Expected_Points_round1'] = round(data_final['Expected_Points_round1'][list(pd.DataFrame(logical)[0])].reset_index(drop=True),1)
        data_df['Captain'] = np.where(data_df['is_captain']==True,"Captain","")

        data_df = data_df.sort_values(['multiplier','position']).reset_index(drop = True)

        for i in range(len(data_df['team'])):
            data_df['team'].loc[i] = team_lookup_num[data_df['team'][i]]
            data_df['position'].loc[i] = position_lookup[data_df['position'][i]]     

    except:
        data_df = 0
        bank = 0
        rank = 0
        transfers = 0 
        
    return data_df, bank, rank, transfers
    