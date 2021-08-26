## Team function

import pandas as pd
import numpy as np
from dictionaries import team_lookup, team_lookup_num

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

def calculate_BPS(df_player,game):
    
    df = df_player[df_player['round'] == game]
    bps = 0 

    if df['position'][game] == 'Goalkeeper':
        bps = bps + 6
        bps = bps + float(df['G']) * 12 
        bps = bps + float(df['A']) * 9 
        bps = bps + float(df['CS']) * 12
        bps = bps + float(df['SV']) * 2

    elif df['position'][game] == 'Defense':
        bps = bps + 6
        bps = bps + float(df['G']) * 12 
        bps = bps + float(df['A']) * 9 
        bps = bps + float(df['CS']) * 12

    elif df['position'][game] == 'Midfield':
        bps = bps + 6
        bps = bps + float(df['G']) * 18
        bps = bps + float(df['A']) * 9 

    elif df['position'][game] == 'Striker':
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
        buy_list_team = list(Output[Output['new_old']=="New"]['Names'])
        buy_list_xPoints = list(Output[Output['new_old']=="New"]['TotalPoints'])

        sell_bool = np.where(pd.DataFrame(PlayerList)[0].isin(Output['Names']), False, True)
        sell_list_names = pd.DataFrame(PlayerList)[sell_bool].reset_index(drop = True)
        sell_list_bool = data_final['fpl_name'].isin(sell_list_names.astype('str')[0])
        sell_list = list(data_final['fpl_name'][sell_list_bool])
        sell_list_position = list(data_final['position'][sell_list_bool]) 

        sell_list_team = []
        sell_list_xPoints = []
        sell_list_team_temp = list(data_final['team'][sell_list_bool])
        sell_list_xPoints_temp = list(data_final['Expected_Points_round1'][sell_list_bool])
        for i in range(len(sell_list_team_temp)):
            sell_list_team.append(team_lookup_num[sell_list_team_temp[i]])
            sell_list_xPoints.append(int(sell_list_xPoints_temp[i]))
        
        New = list(Output['new_old']) 

        return New, Squad, Squad_Position, Squad_Team, Squad_xPoints, Squad_Captain, Expected_points, buy_list, buy_list_position, buy_list_team, buy_list_xPoints, sell_list, sell_list_team, sell_list_position, sell_list_xPoints
    else:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0