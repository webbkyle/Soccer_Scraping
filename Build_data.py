from CLUB import club
from LEAGUE import league
import numpy as np
import pandas as pd
from Gen_funcs import Collect_driver_data as cdd
import time

#initiate timer to monitor code efficacy
start = time.time()

# Inputs for classes
clubNames = []
Seasons = range(2017, 2011, -1)

#run league results from 2012-2017 and fix, clean, and add data
league_results = [league(Season).gather_results for Season in Seasons]
L_results = cdd(league_results)
L_results_data = pd.concat(L_results)
L_results_data.Day = L_results_data.Day.str.lstrip('0')
L_results_data.Month = L_results_data.Month.str.lstrip('0')
time_t = L_results_data.Time.str.split(':')
time_t = [(lambda x: "".join([str(x[0]).lstrip('0'), str(float(x[1])/60).lstrip('0')]))(x) for x in time_t]
L_results_data.insert(3, 'Time_t', time_t)

def clean_teams(team_list):
    team_list = team_list.str.lower()
    team_list = team_list.str.strip(' ')
    team_list = team_list.str.replace(' ', '-')
    city_list = ['cardiff', 'leicester', 'newcastle', 'norwich', 'stoke', 'swansea']
    team_list = list(team_list)
    return_list = []
    for i in team_list:
        if i == 'brighton':
            return_list.append('brighton-and-hove-albion')
        elif any(i == s for s in city_list):
            return_list.append(i + '-city')
        elif i == 'huddersfield':
            return_list.append('huddersfield-town')
        elif i == 'QPR':
            return_list.append('queens-park-rangers')
        elif i == 'tottenham':
            return_list.append(i + '-hotspur')
        elif i == 'west-brom':
            return_list.append('west-bromwich-albion')
        elif i == 'west-ham':
            return_list.append(i + '-united')
        elif i == 'wigan':
            return_list.append(i + '-athletic')
        else:
            return_list.append(i)
    return return_list

L_results_data.Home_Team = clean_teams(L_results_data.Home_Team)
L_results_data.Away_Team = clean_teams(L_results_data.Away_Team)

L_results_data = L_results_data.reset_index(drop=True)

#run league spending scraper for 2012-2017 and fix, clean, and add data
league_spending = [league(Season).spending for Season in Seasons]
L_spending = cdd(league_spending)
L_spending_data = pd.concat(L_spending)
test = L_spending_data.Club.str.lower()
test = test.str.replace(' fc', '')
test = test.str.replace(' ', '-')
test = test.str.replace('afc-bournemouth', 'bournemouth')
test = test.str.replace('brighton-&', 'brighton-and')
test = test.str.replace('sunderland-afc', 'sunderland')
L_spending_data.Club = test
L_spending_data.insert(6, 'log_Total_Mkt', np.log(L_spending_data.Total_Market_Value))
L_spending_data['log_Avg_Mkt'] = np.log(L_spending_data.Average_Market_Value)

L_spending_data = L_spending_data.reset_index(drop=True)

#creating cleaned data for club names and seasons that will be fed into club.gather_squawka_data below
clubs_and_seasons = pd.DataFrame(data = {'Club': L_spending_data.Club,
                                         'Season': [i.split('-',1)[0] for i in L_spending_data.Season]})
club_squawk_data = pd.DataFrame()

#club_roster = [club(clubName, Season).gather_roster for clubName in Seasons]

all_club_data = []

for index, row in clubs_and_seasons.iterrows():
    c_name = str(row['Club'])
    cur_seas = int(row['Season'])
    print c_name
    print cur_seas
    club_squawks = [club(c_name, cur_seas).gather_squawka_club]
    squawks_dat = cdd(club_squawks)
    squawks_dat[0].insert(3, 'Club', [c_name]*len(squawks_dat[0].index))
    all_club_data.append(squawks_dat)
C_squawks_data = pd.concat(item[0] for item in all_club_data)

C_squawks_data = C_squawks_data.reset_index(drop=True)


end = time.time()

print str((end - start)/60) + ' minutes'





#C_squawks_data.to_csv("squawka_data.csv", sep=',')
#L_results_data.to_csv("league_results.csv", sep=',')
#L_spending_data.to_csv("spending_data.csv", sep=',')





'''Messages for Commits:

'''





