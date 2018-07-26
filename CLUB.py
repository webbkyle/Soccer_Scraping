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
from General_functions import search_google_query


# Class to define a club and to search websites for club data
class club:
    def __init__(self, Name = 'Liverpool', season = 2017, close = True):
        self.Name = Name
        self.Stadium = "undefined"
        self.url_name = "http://www2.squawka.com/teams/" + Name.lower() + "/stats#performance-score#english-barclays-premier-league#season-2017/2018#819#all-matches#1-38#by-match"
        self.data_links = []
        self.close = close
        self.season = season

    def gather_squawka_club(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        driver.get(self.url_name)
        #driver.get("http://www2.squawka.com/teams/" + 'chelsea' + "/stats#performance-score#english-barclays-premier-league#season-2017/2018#819#all-matches#1-38#by-match")
        #elems = driver.find_elements_by_xpath("//*[@href]")
        driver.find_element_by_id('stat-1_cumulative').click()
        match_table = driver.find_element_by_xpath("//div[@aria-label='A tabular representation of the data in the chart.']/table")
        date, attacking, possession, defensive, overall, match_data = ([] for i in range(6))
        attacking_cum, possession_cum, defensive_cum, overall_cum = ([0] for j in range(4))
        for row in match_table.find_elements_by_tag_name('td'):
             match_data.append(row.get_attribute('textContent'))
        count_prev = 0
        count = 5
        while count<=len(match_data):
            cur_dat = match_data[count_prev:count]
            dateN = cur_dat[0].replace("/",".")
            date.append(dateN)
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

        dat = pd.DataFrame(data=OrderedDict([(('Date'), date),
                                             (('Attacking'), attacking),
                                             (('Attacking Cumulative'), attacking_cum),
                                             (('Possession'), possession),
                                             (('Possession Cumulative'), possession_cum),
                                             (('Defensive'), defensive),
                                             (('Defensive Cumuluative'), defensive_cum),
                                             (('Overall'), overall),
                                             (('Overall Cumulative'), overall_cum)]))

        if self.close == True: driver.close()

        return dat

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
                                             (('On Hold'), on_hold)]))

        if self.close == True: driver.close()

        return dat

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



