import pandas as pd
import numpy as np

discount_factor = 0
N = len(data_master)

for i in range(N):
    data_master['BPS'][i] = calculate_BPS(data_master, data_master['name'][i], data_master['round'][i])
    data_master['bps_rank'][i] = get_BPS_rank(data_master, data_master['round'][i], \
                                               data_master['team'][i], data_master['opponent'][i], data_master['round'][i])
    data_master['expected_points'][i] = calculate_expected_points(data_master, data_master['name'][i], data_master['round'][i])
    data_master['expected_points_discounted'][i] =  data_master['expected_points'][i]/discount_factor^(data_master['round'][i]-1)

    if data_master['round'][i] == 1:
        data_master['expected_points_round1'][i] = data_master['expected_points'][i]



data_master[['first_name','second_name','expected_points_discounted']].groupby('first_name','second_name').sum()
data_master['position']

ExcludePlayers = []
IncludePlayers = []
ExcludeTeam = []
Budget = 0
PlayerList = []

Pulp_optimization(data_master['team'], N, data_master, data_master['TranferIn'], data_master['TranferOut'], \
                  data_master['expected_points_discounted'], data_master['position'], \
                  ExcludePlayers, IncludePlayers, ExcludeTeam, Budget, data_master['name'], data_master['expected_points'])

def get_BPS_rank(data_master, relevant_player, relevant_player_team, team_against, game):
    
    df = master_data 
    relevant_player = master_data.loc[i,'fpl_name']
    relevant_player_team = master_data.loc[i,'team']
    team_against = master_data.loc[i,'Opponent_num']
    game = master_data.loc[i,'round']

    df = data_master[data_master['round'] == game]
    df = df[(df['team'] == relevant_player_team) | (df['team'] == team_against)]
    bps_score = np.array(df['BPS'])
    ranks = pd.DataFrame((-bps_score).argsort().argsort()) + 1
    ranks = ranks[(df['fpl_name']==relevant_player).reset_index(drop=True)]
    bps_rank = ranks
    
    return int(np.array(bps_rank))

def calculate_BPS(data_master,game):
    
    df = data_master[data_master['round'] == game]
    bps = 0 

    if df['position'][game] == 'Goalkeeper':
        bps = bps + 6
        bps = bps + df['G'] * 12 
        bps = bps + df['A'] * 9 
        bps = bps + df['CS'] * 12
        bps = bps + df['SV'] * 2

    elif df['position'][game] == 'Defense':
        bps = bps + 6
        bps = bps + df['G'] * 12 
        bps = bps + df['A'] * 9 
        bps = bps + df['CS'] * 12

    elif df['position'][game] == 'Midfield':
        bps = bps + 6
        bps = bps + df['G'] * 18
        bps = bps + df['A'] * 9 

    elif df['position'][game] == 'Striker':
        bps = bps + 6
        bps = bps + df['G'] * 24 
        bps = bps + df['A'] * 9 
        

    bps = bps + df['CR'] * 1
    bps = bps + df['CC'] * 3
    bps = bps + int(df['BLK'] + df['CL'] + df['INT'])/2 * 1

    if (df['P']/df['AP'] > 0.7)[game] and (df['P']/df['AP']  <= 0.8)[game]:
        bps = bps + 2
    elif (df['P']/df['AP']  > 0.8)[game] and (df['P']/df['AP']  <= 0.9)[game]:
        bps = bps + 4
    elif (df['P']/df['AP']  > 0.9)[game]:
        bps = bps + 6

    bps = bps + df['Y'] * -3
    bps = bps + df['R']  * -9   
    
    return bps[game]

def calculate_expected_points(data_master, relevant_player, game,i):

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
            expected_points = expected_points - 2
    elif df['position'][i] == 'Defense':
        expected_points = expected_points + 2 # Points for playing the game
        expected_points = expected_points + df['G'] * 6
        expected_points = expected_points + df['A'] * 3
        expected_points = expected_points + df['CS'] * 4
        expected_points = expected_points + df['Y'] * -1
        expected_points = expected_points + df['R'] * -3
        if df['xG_against'][i] >= 2:
            expected_points = expected_points - 2
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
    
    if df['BPS_rank'][i] == 1:
        expected_points = expected_points + 3
    elif df['BPS_rank'][i] == 2:
        expected_points = expected_points + 2
    elif df['BPS_rank'][i] == 3:
        expected_points = expected_points + 1

    return expected_points[i]

