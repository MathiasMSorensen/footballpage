def Pulp_optimization(username,poa):

    import mechanize
    from http.cookiejar import LWPCookieJar
    import requests
    import json
    import pandas as pd
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
    browser.form['password'] = 'Stor66126612'
    browser.submit()
    try:
        url = browser.open('https://fantasy.premierleague.com/api/my-team/4651465/')
        data_json = json.loads(url.read())
        data_df = pd.DataFrame(data_json["picks"])
    except:
        data_df = 0

    return data_df