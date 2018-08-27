from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup as BS
import requests
import urllib2
from collections import OrderedDict
import datetime
from Gen_funcs import search_google_query, season_2_option, get_page, check_table_contents, tell_text
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException



# Class to define a club and to search websites for club data
class club:
    def __init__(self, Name, season, close=True):
        self.Name = Name
        self.season = season
        self.Stadium = "undefined"
        self.url_name_1 = "http://www2.squawka.com/teams/" + Name.lower() + "/stats#performance-score#english-barclays-premier-league#season-" + str(season) + "/" + str(season+1) + "#"
        self.url_name_2 = "#all-matches#1-38#by-match"
        self.close = close

    # webscraper to go to squawka site by club and pull performance scores for each club by match
    #   Description of performance scores: http://www.squawka.com/en/squawka-performance-score
    def gather_squawka_club(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        squawk_url = season_2_option(self.season, self.url_name_1, self.url_name_2)
        #squawk_url = season_2_option(2012, "http://www2.squawka.com/teams/arsenal/stats#performance-score#english-barclays-premier-league#season-2012/2013#", "#all-matches#1-38#by-match")
        m_table = "//div[@aria-label='A tabular representation of the data in the chart.']/table"
        get_page(driver, squawk_url, xpath = m_table)
        try:
            element = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, m_table))
            )
        finally:
            driver.find_element_by_id('stat-1_cumulative').click()
            time.sleep(2)
        match_table = driver.find_element_by_xpath(m_table)
        day, month, year, attacking, possession, defensive, overall, match_data = ([] for i in range(8))
        attacking_cum, possession_cum, defensive_cum, overall_cum = ([0] for j in range(4))
        valid = False
        while(valid == False):
            valid = check_table_contents(match_table)
        tag_table = match_table.find_elements_by_tag_name('td')
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        for row in tag_table:
            A = tell_text(row)
            while(A == False):
                A = tell_text(row)
            row_data = row.get_attribute('textContent')
            match_data.append(str(row_data))
        count_prev = 0
        count = 5
        while count<=len(match_data):
            cur_dat = match_data[count_prev:count]
            dateN = cur_dat[0].replace("/", ".")
            date_n = dateN.split(".")
            day.append(date_n[0])
            month.append(date_n[1])
            year.append(date_n[2])
            attacking.append(float(cur_dat[1]))
            possession.append(float(cur_dat[2]))
            defensive.append(float(cur_dat[3]))
            overall.append(float(cur_dat[4]))
            if count_prev != 0:
                attacking_cum.append(sum(attacking))
                possession_cum.append(sum(possession))
                defensive_cum.append(sum(defensive))
                overall_cum.append(sum(overall))
            count_prev += 5
            count += 5

        dat = pd.DataFrame(data=OrderedDict([(('Day'), day),
                                             (('Month'), month),
                                             (('Year'), year),
                                             (('Attacking'), attacking),
                                             (('Attacking_Cumulative'), attacking_cum),
                                             (('Possession'), possession),
                                             (('Possession_Cumulative'), possession_cum),
                                             (('Defensive'), defensive),
                                             (('Defensive_Cumuluative'), defensive_cum),
                                             (('Overall'), overall),
                                             (('Overall_Cumulative'), overall_cum)]))

        if self.close == True: driver.close()

        return dat

    # webscraper for pulling names of players on the club, their position, their number, their country of origin,
    #   and whether they are on hold with another club or not
    def gather_roster(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        search_google_query(driver, self.Name + " FC wiki")
        driver.find_element_by_xpath('(//h3)[1]/a').click()
        name, number, position, country, on_hold = ([] for i in range(5))
        for row in driver.find_elements_by_css_selector("tr.vcard.agent"):
            playerName = row.find_elements_by_tag_name("td")[3].text
            name.append(playerName.split('(')[0])
            number.append(row.find_elements_by_tag_name("td")[0].text)
            position.append(row.find_elements_by_tag_name("td")[2].text)
            flags = row.find_elements_by_tag_name("td")[1]
            countryLink =  str(flags.find_element_by_css_selector('a').get_attribute('href'))
            result = re.search('https://en.wikipedia.org/wiki/(.*)', countryLink)
            country.append(result.group(1))
            on_hold.append(1 if 'at ' in playerName or 'on loan ' in playerName else 0)

        dat = pd.DataFrame(data=OrderedDict([(('Name'), name),
                                             (('Position'), position),
                                             (('Number'), number),
                                             (('Country'), country),
                                             (('On_Hold'), on_hold)]))

        if self.close == True: driver.close()

        return dat

    # webscraper that searches google for the club's stadium name and returns it
    def stadium(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        search_google_query(driver, "stadium " + self.Name + " FC")
        Stadium = driver.find_element_by_class_name('Z0LcW').text

        if self.close == True: driver.close()

        return str(Stadium)

    '''
    def spending(self):

    def description(self):

    def tournaments(self):

    def history(self):'''



