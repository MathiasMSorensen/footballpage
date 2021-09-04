

import mechanize
from http.cookiejar import LWPCookieJar
import requests
import json
import pandas as pd
import numpy as np

from urllib.request import urlopen
print(1)
browser = mechanize.Browser()
cj = LWPCookieJar()
browser.set_cookiejar(cj)
browser.set_handle_equiv(True)
browser.set_handle_redirect(True)
browser.set_handle_robots(False)
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
browser.open('https://users.premierleague.com/')
browser.select_form(nr = 0)
browser.form['login'] = 'mathias47@hotmail.com'
browser.form['password'] = 'Stor6612'
browser.submit()
try:
    url = browser.open('https://fantasy.premierleague.com/api/my-team/4651465/')
    data_json = json.loads(url.read())
    data_df = pd.DataFrame(data_json["picks"])
    
    transfers = data_json["transfers"]['limit']

    url = browser.open('https://fantasy.premierleague.com/api/entry/4651465/')
    data_json = json.loads(url.read())
    bank = data_json['last_deadline_bank']/10
    rank = data_json['summary_overall_rank']

    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_df_fpl = pd.DataFrame(data_json["elements"])
    data_df_fpl['Player'] = data_df_fpl['first_name'] + ' ' + data_df_fpl['second_name']
    
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_df_fpl = pd.DataFrame(data_json["elements"])
    data_df_fpl['Player'] = data_df_fpl['first_name'] + ' ' + data_df_fpl['second_name']
    
    logical  = data_df_fpl['id'].isin(data_df['element'])
    data_df['player'] = data_df_fpl['Player'][logical].reset_index(drop=True)
    data_df['multiplier'] = np.where(data_df['multiplier']>=1,0,1)
    data_df['position'] = data_df_fpl['element_type'][logical].reset_index(drop=True)

    logical  = data_final['fpl_name'].isin(data_df['player'])
    data_df['team'] = data_final['team'][logical].reset_index(drop=True)
    data_df['Expected_Points_round1'] = round(data_final['Expected_Points_round1'][logical].reset_index(drop=True)
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
    