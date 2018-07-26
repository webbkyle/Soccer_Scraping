from CLUB import club
from LEAGUE import league
import pandas as pd



clubName = 'Liverpool'
season = 2017


def Collect_driver_data(f):
    var = pd.DataFrame()
    while len(var) == 0:
        var = f()
    return var

fetch_data = [club(clubName, season).gather_roster,
               club(clubName, season).gather_squawka_club,
               league().gather_results,
               league().spending,
               club(clubName, season).stadium]

all_data = []

for i in fetch_data:
    all_data.append(Collect_driver_data(i))















