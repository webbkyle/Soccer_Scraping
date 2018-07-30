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

# inputs class webscrapers and provides wait mechanism until driver has closed so that next class webscraper can begin
def Collect_driver_data(f):
    var = pd.DataFrame()
    while len(var) == 0:
        var = f()
    return var

# funciton to create proper squawka url for webscraper in club class to drive to, provides option_value (web element) to correspond to season
def season_2_option(season, url1, url2):
    option_vals = [819, 641, 165, 126, 64, 2]
    seasons = range(2017,2011,-1)
    ind = seasons.index(season)
    new_url = url1 + str(option_vals[ind]) + url2
    return new_url

