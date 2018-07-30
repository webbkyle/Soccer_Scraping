from CLUB import club
from LEAGUE import league
from Gen_funcs import Collect_driver_data as cdd
import numpy as np
import pandas as pd

# File will enact all webscrapers from the classes

# Inputs for classes
clubName = 'Liverpool'
Seasons = range(2017, 2012, -1)


'''df = pd.DataFrame.from_dict(map(dict,df_list))


def flat_file():
    league_data = []
    for season in Seasons:
        ind = Seasons.index(season)
        fetch_data_functions1 = [league(season).gather_results, league(season).spending]
        for i in fetch_data_functions1:
            league_data.append(cdd(i))
        league_data()'''



# Names of all functions used from each of the classes with inputs assigned appropriately
fetch_data_functions1 = [club(clubName, Season).gather_roster,
               #club(clubName, Season).gather_squawka_club,
               league(Season).gather_results,
               league(Season).spending,
               club(clubName, Season).stadium]

# empty array where all data will be stored
all_data = []

for i in fetch_data_functions:
    all_data.append(cdd(i))








