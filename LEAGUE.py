from selenium import webdriver
import time
import pandas as pd
from collections import OrderedDict
from General_functions import check_exists_by_css
import re
import unicodedata


# Class to define a league and to search websites for league data
class league:
    def __init__(self, Name = 'English Premier League', close = True, season = 2017):
        self.Name = Name
        self.Stadium = "undefined"
        self.close = close
        self.season = season

    def gather_results(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        driver.get('https://www.flashscore.com/football/england/premier-league-' + ''.join([str(self.season),'-',str(self.season+1)]) + '/results/')
        '''driver.get('https://www.flashscore.com/football/england/premier-league-' + ''.join
            ([str(2017), '-', str(2017 + 1)]) + '/results/')'''
        table = driver.find_element_by_id('fs-results')
        while(check_exists_by_css(driver, '#tournament-page-results-more') == True):
            # check_exists_by_css(driver, '#tournament-page-results-more')
            time.sleep(4)
        date, sched_time, home_team, away_team, home_team_score, away_team_score, home_team_result = ([] for i in range(7))
        for row in table.find_elements_by_tag_name('tr')[2:]:
            fix_dat = row.text.splitlines()
            if len(fix_dat) < 2:
                continue
            date_cur = fix_dat[0].split()[0]
            date_month = int(date_cur.split('.')[1])
            if date_month >= 1 and date_month < 7:
                # date_cur += str(self.season + 1)
                date_cur += str(2017 + 1)
            else:
                # date_cur += str(self.season)
                date_cur += str(2017)
            date.append(date_cur)
            sched_time.append(fix_dat[0].split()[1])
            home_team.append(fix_dat[1])
            away_team.append(fix_dat[2])
            home_res = fix_dat[3].split()[0]
            home_team_score.append(int(home_res))
            away_res = fix_dat[3].split()[2]
            away_team_score.append(int(away_res))
            if home_res == away_res:
                home_team_result.append('D')
            elif home_res > away_res:
                home_team_result.append('W')
            else:
                home_team_result.append('L')

        dat = pd.DataFrame(data=OrderedDict([(('Date'), date),
                                             (('Time'), sched_time),
                                             (('Home Team'), home_team),
                                             (('Away Team'), away_team),
                                             (('Home Team Goals'), home_team_score),
                                             (('Away Team Goals'), away_team_score),
                                             (('Home Team Result'), home_team_result)]))

        if self.close == True: driver.close()

        return dat


    def spending(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        #driver.get('https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/')
        driver.get('https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=' + str(self.season))
        time.sleep(3)
        '''
        driver.find_element_by_id('sel2LI_chzn').click()
        seasonStr = str(season)[2:]
        dropDown = driver.find_element_by_css_selector('#selBPP_chzn')
        search = driver.find_element_by_class_name('chzn-search')
        search.click()
        search = driver.find_element_by_id('chzn-results')
        for row in search.find_elements_by_xpath('//ul[contains(@class,"chzn-results")]/li'):
            test = str(row.get_attribute('textContent'))[:2]
            if seasonStr == test:
                driver.find_element_by_id('sel2LI_chzn').click()
                row.click()
                driver.find_element_by_xpath('//*[@id="wettbewerbsstartseite"]/div[1]/div[1]/div[2]/form/div/div/table/tbody/tr/td[3]/input').click()
                break
                '''
        table = driver.find_element_by_class_name('items')
        club, squadTotal, avgAge, foreignPlayers, totalmrkt, avgmrkt = ([] for i in range(6))
        for row in table.find_elements_by_tag_name('tr')[2:22]:
            markettab = row.text.split()
            #print markettab
            club.append(str(' '.join(markettab[0:-5])))
            squadTotal.append(int(markettab[-5]))
            avgAge.append(float(str(markettab[-4]).replace(',', '.')))
            foreignPlayers.append(int(markettab[-3]))
            totStr = markettab[-2].encode('ascii', 'xmlcharrefreplace')
            avgStr = markettab[-1].encode('ascii', 'xmlcharrefreplace')
            totStr = filter(lambda x: x.isdigit() or '.' in x, totStr)[2:]
            avgStr = filter(lambda x: x.isdigit() or '.' in x, avgStr)[2:]
            totalmrkt.append(float(totStr))
            avgmrkt.append(float(avgStr))
        #print club, squadTotal, avgAge, foreignPlayers, totalmrkt, avgmrkt
        dat = pd.DataFrame(data=OrderedDict([(('Club'), club),
                                             (('Squad Total'), squadTotal),
                                             (('Average Age'), avgAge),
                                             (('Foreign Players'), foreignPlayers),
                                             (('Total Market Value'), totalmrkt),
                                             (('Average Market Value'), avgmrkt)]))

        if self.close == True: driver.close()

        return dat



    '''
    def history(self):

    def club_names(self):'''