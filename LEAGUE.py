from selenium import webdriver
import time
import pandas as pd
from collections import OrderedDict
from Gen_funcs import check_exists_by_css
import numpy as np
import re
import unicodedata


# Class to define a league and to search websites for league data
class league:
    def __init__(self, season, Name = 'English Premier League', close = True):
        self.Name = Name
        self.close = close
        self.season = season

    # webscraper for season fixtures including date and time of match, results, home and away teams
    def gather_results(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        driver.get('https://www.flashscore.com/football/england/premier-league-' + ''.join([str(self.season),'-',str(self.season+1)]) + '/results/')
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
                date_cur += str(self.season + 1)
            else:
                # date_cur += str(self.season)
                date_cur += str(self.season)
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
                                             (('Home_Team'), home_team),
                                             (('Away_Team'), away_team),
                                             (('Home_Team_Goals'), home_team_score),
                                             (('Away_Team_Goals'), away_team_score),
                                             (('Home_Team_Result'), home_team_result)]))

        if self.close == True: driver.close()

        return dat

    # webscraper for premier league transfer market data, count of players on squad, distinguishing foreign players too
    def spending(self):
        driver = webdriver.Chrome(executable_path=r"/Users/kylewebb/Downloads/chromedriver 5")
        #driver.get('https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/')
        driver.get('https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=' + str(self.season))
        time.sleep(3)
        table = driver.find_element_by_class_name('items')
        club, Seasons, squadTotal, avgAge, foreignPlayers, totalmrkt, avgmrkt = ([] for i in range(7))
        Seasons = np.repeat(str(self.season) + '-' + str(self.season + 1), 20)
        for row in table.find_elements_by_tag_name('tr')[2:22]:
            markettab = row.text.split()
            #print markettab
            club.append(str(' '.join(markettab[0:-5])))
            squadTotal.append(int(markettab[-5]))
            avgAge.append(float(str(markettab[-4]).replace(',', '.')))
            foreignPlayers.append(int(markettab[-3]))
            #totStr = markettab[-2].encode('ascii', 'xmlcharrefreplace')
            #avgStr = markettab[-1].encode('ascii', 'xmlcharrefreplace')
            totStr = markettab[-2][1:]
            avgStr = markettab[-1][1:]
            totStr = filter(lambda x: x.isdigit() or '.' in x, totStr)
            avgStr = filter(lambda x: x.isdigit() or '.' in x, avgStr)
            totalmrkt.append(float(totStr))
            avgmrkt.append(float(avgStr))
        #print club, squadTotal, avgAge, foreignPlayers, totalmrkt, avgmrkt
        dat = pd.DataFrame(data=OrderedDict([(('Club'), club),
                                             (('Season'), Seasons[:]),
                                             (('Squad_Total'), squadTotal),
                                             (('Average_Age'), avgAge),
                                             (('Foreign_Players'), foreignPlayers),
                                             (('Total_Market_Value'), totalmrkt),
                                             (('Average_Market_Value'), avgmrkt)]))

        # closes the browser
        if self.close == True: driver.close()

        return dat



    '''
    def history(self):

    def club_names(self):'''