import time
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, StaleElementReferenceException, NoSuchElementException

#some general webscraping functions

# given a driver, function to click on a web element by css selctor if visible. Ideal for looping through clickable html tables
def check_exists_by_css(d, css):
    try:
        d.find_element_by_css_selector(css).click()
    except ElementNotVisibleException:
        return False
    return True

def check_table_contents(tab):
    try:
        tab.find_elements_by_tag_name('td')
    except (ElementNotVisibleException, TimeoutException, StaleElementReferenceException) as e:
        return False
    return True

def tell_text(row):
    try:
        element = row.get_attribute('textContent')
    except:
        element = 0
    if isinstance(element, basestring):
        return True
    else:
        return False

# given a driver, function to submit search on google's main query
def search_google_query(d, searchString):
    d.get('http://www.google.com')
    body = d.find_element_by_name("q")
    body.send_keys(searchString)
    body.submit()

def get_page(d, url, id = 0, xpath = 0):
    delay = 3
    v = False
    while (v == False):
        if id!= 0:
            try:
                myElem = WebDriverWait(d, delay).until(
                    EC.presence_of_element_located((By.ID, id))
                )
            except (TimeoutException, NoSuchElementException):
                v = False
        else:
            try:
                myElem = WebDriverWait(d, delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            except (TimeoutException, NoSuchElementException):
                v = False
        v = True
    d.get(url)


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
'''def map_results(C, LS, LR):
    Data = pd.DataFrame(columns = LR.columns.append(C.columns[2:]).append(LS.columns[2:]))
    uni_years = LR.Year.unique()
    for year in uni_years:
        LR_sub_yr = LR.loc[LR.Year.isin(year)]
        for i in enumerate(len(LR_sub_yr)):
            month = str(LR_sub_yr.Month[i])
            home = str(LR_sub_yr.Home_Team[i])
            away = str(LR_sub_yr.Away_Team[i])
            sqsub_home = drill_down(C, year, month, home)
            sqsub_away = drill_down(C, year, month, away)
            if(month >= 8):
                season = year + '-' + str(int(year) + 1)
                spsub_home = drill_down_sp(LS, season, home)
                spsub_away = drill_down_sp(LS, season, away)
            else:
                season = str(int(year) - 1) + '-' + year
                spsub_home = drill_down_sp(LS, season, home)
                spsub_away = drill_down_sp(LS, season, away)
            sq_diff = sqsub_home.columns[2:] - sqsub_away.columns[2:]
            sp_diff = spsub_home.columns[2:] - spsub_away.columns[2:]
            Data.append(LR)



def drill_down(df, year, month, team):
    A = df.loc[df.Year.isin([str(year)])]
    B = A.loc[A.Month.isin([str(month)])]
    return B.loc[B.Club.isin([team])]

def drill_down_sp(df, season, team):
    A = df.loc[df.Season.isin([str(season)])]
    B = A.loc[A.Club.isin([str(team)])]
    return B

    uni_years = LR.Year.unique()
    uni_months = LR.Month.unique()





    for year in uni_years:
        squawk_sub_year = C.loc[C.Year.isin([year])]
        results_sub_year = LR.loc[LR.Year.isin([year])]
        for month in uni_months:
            squawk_sub_month = squawk_sub_year.loc[squawk_sub_year.Month.isin([month])]

            squawk_sub_month.loc[squawk_sub_month.Club.isin(['burnley']), squawk_sub_month.columns[2:]]



            lr_sub_date = LR.loc[C.Date.isin([date])]




        X.loc[X.Club.isin(['burnley']), X.columns[2:]]
        X.loc[X.Club.isin(['burnley']), X.columns[2:]] - X.loc[X.Club.isin(['bournemouth']), X.columns[2:]]
        df.loc[df['Club'].isin(some_values)]
        row = C[C.Home_Team.isin([home]) and C.Away_Team.isin([away]) and C.Date.isin([date])]
    else:
        r_temp = C[C.Home_Team.isin([home]) and C.Away_Team.isin([away])]
        yr1 = C.index(r_temp).Date.str.strip('.')[2]
        yr2 = Ls.Season.str.strip('-')[0]


        '''