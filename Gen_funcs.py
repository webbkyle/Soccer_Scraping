from selenium.common.exceptions import ElementNotVisibleException
import time
import pandas as pd
import numpy as np

#some general webscraping functions

# given a driver, function to click on a web element by css selctor if visible. Ideal for looping through clickable html tables
def check_exists_by_css(d, css):
    try:
        d.find_element_by_css_selector(css).click()
    except ElementNotVisibleException:
        return False
    return True

# given a driver, function to submit search on google's main query
def search_google_query(d, searchString):
    d.get('http://www.google.com')
    body = d.find_element_by_name("q")
    body.send_keys(searchString)
    body.submit()

# inputs list of class function webscrapers and provides wait mechanism until driver has closed so that next class webscraper can begin
def Collect_driver_data(F):
    all_dat = []
    if len(F) > 1:
        for f in F:
            var = pd.DataFrame()
            while len(var) == 0:
                var = f()
            all_dat.append(var)
    else:
        var = pd.DataFrame()
        while len(var) == 0:
            var = F[0]()
        all_dat.append(var)
    return all_dat

# funciton to create proper squawka url for webscraper in club class to drive to, provides option_value (web element) to correspond to season
def season_2_option(season, url1, url2):
    option_vals = [819, 641, 165, 126, 64, 2]
    seasons = range(2017,2011,-1)
    ind = seasons.index(season)
    new_url = url1 + str(option_vals[ind]) + url2
    return new_url

# creates flat file by linking all games in cleaned versions of C_squawks_data, L_results_data, and L_spending_data
'''def flatten(C, L1, L2):
    flat_file = pd.DataFrame()

    #independent variables
    Date = L1.Date
    Month = Date.str.split('-')[1]
    Time = L1.Time_t

    #map home team to gather home team squawka and club spending data differences

    #map away team to gather away team squawka and club spending data differences


    #response variables
    Home_team_goals = L1.Home_Team_Goals
    Away_team_goals = L1.Away_Team_Goals
    Home_team_result = L1.Home_Team_Result
'''

#maps a home and away team and their date of play from disparate datasets to obtain a row of differences
'''def map_teams(home, away, date = 0, C, Ls):
    if date not 0:
        row = C[C.Home_Team.isin([home]) and C.Away_Team.isin([away]) and C.Date.isin([date])]
    else:
        r_temp = C[C.Home_Team.isin([home]) and C.Away_Team.isin([away])]
        yr1 = C.index(r_temp).Date.str.strip('.')[2]
        yr2 = Ls.Season.str.strip('-')[0]
        row = Ls[Ls.


'''






