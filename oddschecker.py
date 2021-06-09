from typing import Dict
from soccerapi.api import ApiUnibet
import pandas as pd
import numpy as np
import os
from difflib import get_close_matches

import urllib.request, json

## Odds
url = "https://dh-api-production.herokuapp.com/football/euros/stages"

response = urllib.request.urlopen(url)

data = json.loads(response.read())
data = pd.DataFrame.from_dict(data)
# Note, index 0 = Group stage 
print(data)

data1 = pd.DataFrame.from_dict(dict(data.iloc[0,0]))

game_day = []
home_team = []
away_team = []
homeTeamWin = []
awayTeamWin = []
draw = []
homeTeamCleanSheet = []
awayTeamCleanSheet = []

for i in range(len(data1)):
    temp_data = pd.DataFrame.from_dict(dict(data1.iloc[i,1]))
    game_day.append(temp_data['date'][0])
    home_team.append(temp_data['homeTeamName'][0])
    away_team.append(temp_data['awayTeamName'][0])

    temp_data_2 = dict(temp_data['odds'])   
    temp_data_3 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in temp_data_2.items() ]))

    temp_data_4 = dict(temp_data_3['homeTeamWin'])
    temp_data_5 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in temp_data_4.items() ])).dropna(axis=1,how='all').transpose()
    homeTeamWin.append(float(temp_data_5['odds'][max(temp_data_5['lastUpdated']) == temp_data_5['lastUpdated']]))
    
    temp_data_4 = dict(temp_data_3['awayTeamWin'])
    temp_data_5 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in temp_data_4.items() ])).dropna(axis=1,how='all').transpose()
    awayTeamWin.append(float(temp_data_5['odds'][max(temp_data_5['lastUpdated']) == temp_data_5['lastUpdated']]))

    temp_data_4 = dict(temp_data_3['draw'])
    temp_data_5 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in temp_data_4.items() ])).dropna(axis=1,how='all').transpose()
    draw.append(float(temp_data_5['odds'][max(temp_data_5['lastUpdated']) == temp_data_5['lastUpdated']]))

    temp_data_4 = dict(temp_data_3['homeTeamCleanSheet'])
    temp_data_5 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in temp_data_4.items() ])).dropna(axis=1,how='all').transpose()
    homeTeamCleanSheet.append(float(temp_data_5['odds'][max(temp_data_5['lastUpdated']) == temp_data_5['lastUpdated']]))

    temp_data_4 = dict(temp_data_3['awayTeamCleanSheet'])
    temp_data_5 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in temp_data_4.items() ])).dropna(axis=1,how='all').transpose()
    awayTeamCleanSheet.append(float(temp_data_5['odds'][max(temp_data_5['lastUpdated']) == temp_data_5['lastUpdated']]))

data = pd.DataFrame(
    {'game_day': game_day,
     'home_team': home_team,
     'away_team': away_team,
     'homeTeamWin': homeTeamWin,
     'awayTeamWin': awayTeamWin,
     'draw': draw,
     'homeTeamCleanSheet': homeTeamCleanSheet,
     'awayTeamCleanSheet': awayTeamCleanSheet
    })

paybackpercent = 1/(1/data['homeTeamWin']+1/data['awayTeamWin']+1/data['draw'])

data['homeTeamWin'] = paybackpercent/data['homeTeamWin']
data['awayTeamWin'] = paybackpercent/data['awayTeamWin']
data['draw'] = paybackpercent/data['draw']
data['homeTeamCleanSheet'] = paybackpercent/data['homeTeamCleanSheet']
data['awayTeamCleanSheet'] = paybackpercent/data['awayTeamCleanSheet']

odds_teams = data

## Lineups
url = "https://dh-api-production.herokuapp.com/football/euros/players"

response = urllib.request.urlopen(url)

data = json.loads(response.read())
data = pd.DataFrame.from_dict(data)
players = []

for i in range(len(data)):
    players.append(pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.iloc[i,0].items() ])))

players = pd.concat(players)

players.loc[players['teamName']=='Denmark']

## Teams and stats
paybackpercent = 0.95

url = 'https://dh-api-production.herokuapp.com/football/euros/teams'

response = urllib.request.urlopen(url)

data = json.loads(response.read())
data = pd.DataFrame.from_dict(data)
teams = []

for i in range(len(data)):
    teams.append(pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.iloc[i,0].items() ])))

teams = pd.concat(teams)
teams['oddsToWin'] = paybackpercent/teams['oddsToWin']
teams['oddsToQualifyGroup'] = paybackpercent/teams['oddsToQualifyGroup']
teams['oddsToWinGroup'] = paybackpercent/teams['oddsToWinGroup']

players.loc[players['teamName']=='Denmark']

## Holdet.dk
APP_ROOT = os.path.dirname(os.path.abspath('__file__'))
holdet = pd.read_csv(os.path.join(APP_ROOT, 'holdet.csv'))


##Rotowire
rWire = pd.read_excel(os.path.join(APP_ROOT, 'rotowire-stats.xlsx'))
rWire1 = pd.read_excel(os.path.join(APP_ROOT, 'rotowire-stats (1).xlsx'))
rWire2 = pd.read_excel(os.path.join(APP_ROOT, 'rotowire-stats (2).xlsx'))
rWire3 = pd.read_excel(os.path.join(APP_ROOT, 'rotowire-stats (3).xlsx'))
rWire4 = pd.read_excel(os.path.join(APP_ROOT, 'rotowire-stats (4).xlsx'))
rWire5 = pd.read_excel(os.path.join(APP_ROOT, 'rotowire-stats (5).xlsx'))

rWire = pd.concat([rWire,rWire1,rWire2,rWire3,rWire4,rWire5])

players['fullname'] = ''
players['rwirename'] = ''
players['fullname'] = np.where(players['firstName'].isna() == False,players['firstName'] +" "+ players['lastName'],players['lastName'])
players['goals'] = ''
players['assists'] = ''
players['saves'] = ''
players['cs'] = '' 
players['min'] = '' 
players['SOG'] = ''
players['Yellow'] = '' 
players['Red'] = '' 

for i in range(len(players['fullname'])):
    if players['fullname'].iloc[i] == 'Thiago':
        players['fullname'].iloc[i] = 'Thiago Alcantara'
    elif players['fullname'].iloc[i] == 'Rodri':
        players['fullname'].iloc[i] = 'Rodrigo Hernandez'
    elif players['fullname'].iloc[i] == 'Pedri':
        players['fullname'].iloc[i] = 'Pedri Gonzalez Lopez'

check = []

for i in range(len(players['fullname'])):
    players['rwirename'].iloc[i] = get_close_matches(players['fullname'].iloc[i],rWire['Player Name'],n=1)
    if players['rwirename'].iloc[i] != []:
        players['goals'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['G']) 
        players['assists'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['A'])  
        players['saves'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['SV']) 
        players['cs'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['CS']) 
        players['min'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['MIN']) 
        players['SOG'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['SOG'])
        players['Red'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['R'])
        players['Yellow'].iloc[i] = sum(rWire[players['rwirename'].iloc[i][0] == rWire['Player Name']]['Y'])
        players['rwirename'].iloc[i] = players['rwirename'].iloc[i][0]
    else:
        check.append(i)
    

players['team'] = ''
players['postion'] = ''
players['value'] = ''
players['popularity'] = ''
players['holdetname'] = ''

check = []
players['fullname'].iloc[i]
for i in range(len(players['fullname'])):
    players['holdetname'].iloc[i] = get_close_matches(players['fullname'].iloc[i],holdet['player'],n=1)
    if players['holdetname'].iloc[i] != []:
        players['team'].iloc[i] = holdet[players['holdetname'].iloc[i][0] == holdet['player']]['team'].to_string(index=False)  
        players['postion'].iloc[i] = holdet[players['holdetname'].iloc[i][0] == holdet['player']]['postion'].to_string(index=False)   
        players['value'].iloc[i] = int((holdet[players['holdetname'].iloc[i][0] == holdet['player']]['value'].values)[0].replace('.', ''))
        players['popularity'].iloc[i] = (holdet[players['holdetname'].iloc[i][0] == holdet['player']]['popularity'].values)[0].replace('.', '')
        players['holdetname'].iloc[i] = players['holdetname'].iloc[i][0]
    else:
        check.append(i)
    

map(float((holdet[players['holdetname'].iloc[i][0] == holdet['player']]['value'].values)[0].split('.')))

players.to_excel("fantasyAnalyticsplayers.xlsx",sheet_name='Sheet_name_1')  
odds_teams.to_excel("fantasyAnalyticsodds_teams.xlsx",sheet_name='Sheet_name_1') 
teams.to_excel("fantasyAnalyticsteams.xlsx",sheet_name='Sheet_name_1') 

sum((players['goals'].loc[players['lineupStatus']=='expected'] == '')*1)

myDict = {'Denmark': 'Danmark',
          'Scotland': 'Skotland',
          'Netherlands': 'Holland',
          'Austria': 'Østrig',
          'Russia': 'Rusland',
          'Germany': 'Tyskland',
          'Finland': 'Finland',
          'Sweden': 'Sverige',
          'Wales': 'Wales',
          'Switzerland': 'Schweiz',
          'North Macedonia': 'Nordmakedonien',
          'France': 'Frankrig',
          'Slovakia': 'Slovakiet',
          'Hungary': 'Ungarn',
          'England': 'England',
          'Poland': 'Polen',
          'Turkey': 'Tyrkiet',
          'Czech Republic': 'Tjekkiet',
          'Italy': 'Italien',
          'Spain': 'Spanien',
          'Belgium': 'Belgien',
          'Portugal': 'Portugal',
          'Croatia': 'Kroatien',
          'Ukraine': 'Ukraine'}

myDict['Croatia']





rn = players['row_num'].loc[players['goals'].loc[players['lineupStatus']=='expected']

players['row_num'].loc[players['goals'].loc[players['lineupStatus']=='expected'] == '']

holdet.columns
'team','postion', 'value', 'popularity'
players
players[players['rwirename'] == players['rwirename'].iloc[96]]

print(i)


rWire.append(rWire1)



temp_data2 = pd.DataFrame.from_dict(temp_data1['Dataset']['Items'])
for i in range(len(temp_data2)):
    print(pd.DataFrame.from_dict(temp_data2['Values'][i]))
    print(pd.DataFrame.from_dict(temp_data2['Texts'][i]))

temp_data1.iloc[i,48:50]

game_day = []
home_team = []
away_team = []
homeTeamWin = []
awayTeamWin = []
draw = []
homeTeamCleanSheet = []
awayTeamCleanSheet = []




### trash 
from soccerapi.api import ApiUnibet
import pandas as pd
api = ApiUnibet()

url = 'https://www.unibet.com/betting/sports/filter/football/euro_2020/'

odds = api.odds(url)
odds = pd.DataFrame.from_dict(odds)
full_time_result = pd.DataFrame.from_dict(dict(odds['full_time_result'])).transpose()/1000
under_over = pd.DataFrame.from_dict(dict(odds['under_over'])).transpose()/1000
both_teams_to_score = pd.DataFrame.from_dict(dict(odds['both_teams_to_score'])).transpose()/1000

pd.concat([odds[['time','home_team','away_team']].reset_index(drop=True), full_time_result.reset_index(drop=True), \
            under_over.reset_index(drop=True), both_teams_to_score.reset_index(drop=True)], axis=1)

pd.DataFrame.from_dict(dict(odds['both_teams_to_score ']))
pd.DataFrame.from_dict({'1': 3250, 'X': 3150, '2': 2350} )

type(odds['full_time_result'])


pd.DataFrame(odds['full_time_result'])
print(odds)
for item in odds:
    print(item)

for item in json.dumps(odds):
    print(item)
# pd.DataFrame.from_dict(dict(data3['homeTeamWin'][0]))

print data

[('homeTeamWin', [{'bookmaker': 'WilliamHill', 'odds': 7.5, 'lastUpdated': '2021-06-04 23:01:44.000000'}, {'bookmaker': 'Betsson', 'odds': 7.05, 'lastUpdated': '2021-06-04 05:47:57.000000'}, {'bookmaker': 'bet365', 'odds': 7, 'lastUpdated': '2021-06-05 16:05:25.681335'}, {'bookmaker': 'Unibet', 'odds': 6.75, 'lastUpdated': '2021-05-31 07:14:12.000000'}]), ('awayTeamWin', [{'bookmaker': 'Unibet', 'odds': 1.62, 'lastUpdated': '2021-05-31 07:14:12.000000'}, {'bookmaker': 'Betsson', 'odds': 1.58, 'lastUpdated': '2021-06-04 05:47:57.000000'}, {'bookmaker': 'bet365', 'odds': 1.55, 'lastUpdated': '2021-06-05 16:05:25.681359'}, {'bookmaker': 'WilliamHill', 'odds': 1.55, 'lastUpdated': '2021-06-04 23:01:44.000000'}]), ('draw', [{'bookmaker': 'bet365', 'odds': 3.8, 'lastUpdated': '2021-06-05 16:05:25.681349'}, {'bookmaker': 'Betsson', 'odds': 3.8, 'lastUpdated': '2021-06-04 05:47:57.000000'}, {'bookmaker': 'WilliamHill', 'odds': 3.7, 'lastUpdated': '2021-06-04 23:01:44.000000'}, {'bookmaker': 'Unibet', 'odds': 3.55, 'lastUpdated': '2021-05-31 07:14:12.000000'}]), ('btts', [{'bookmaker': 'bet365', 'odds': 2.25, 'lastUpdated': '2021-06-05 16:05:25.681896'}]), ('noBtts', [{'bookmaker': 'bet365', 'odds': 1.57, 'lastUpdated': '2021-06-05 16:05:25.681907'}]), ('over2_5', [{'bookmaker': 'bet365', 'odds': 2.2, 'lastUpdated': '2021-06-05 16:05:25.681865'}]), ('under2_5', [{'bookmaker': 'bet365', 'odds': 1.67, 'lastUpdated': '2021-06-05 16:05:25.681876'}]), ('homeTeamCleanSheet', [{'bookmaker': 'bet365', 'odds': 5, 'lastUpdated': '2021-06-05 16:05:25.677135'}]), ('awayTeamCleanSheet', [{'bookmaker': 'bet365', 'odds': 1.83, 'lastUpdated': '2021-06-05 16:05:25.677168'}])])
>>> dict( A = np.array([1,2]), B = np.array([1,2,3,4]) )