import pandas as pd
import os
import numpy as np
import testing as t
import time
import random
from unidecode import unidecode

f = open('/Users/ankul/Documents/myPlayers0.csv', 'a')
url = "https://www.basketball-reference.com/leagues/NBA_2025_totals.html"
plays = pd.read_html(url)[0]
plays = plays[plays["Team"] != "2TM"]
plays = plays[plays["Team"] != "3TM"]
plays = plays[plays["Player"] != "Player"]
plays = plays[["Player", "Team"]]
plays = plays.drop_duplicates(subset="Player", keep="first")[:250]
for play in range(len(plays)):
    plays.iloc[play].values[0] = unidecode(plays.iloc[play].values[0])

playerDic = dict(zip(plays["Player"], plays["Team"]))

dicTeamsStrength = {}
url = "https://www.basketball-reference.com/leagues/NBA_2025.html"
tab = pd.read_html(url)[10]
for i in tab.values[:len(tab.values) - 1]:
    dicTeamsStrength[i[1].replace("*", "")] = [i[11], i[23], i[24], i[25], i[26]]

nba_teams = {
        "ATL": "Atlanta Hawks",
        "BOS": "Boston Celtics",
        "BKN": "Brooklyn Nets",
        "CHA": "Charlotte Hornets",
        "CHI": "Chicago Bulls",
        "CLE": "Cleveland Cavaliers",
        "DAL": "Dallas Mavericks",
        "DEN": "Denver Nuggets",
        "DET": "Detroit Pistons",
        "GSW": "Golden State Warriors",
        "HOU": "Houston Rockets",
        "IND": "Indiana Pacers",
        "LAC": "Los Angeles Clippers",
        "LAL": "Los Angeles Lakers",
        "MEM": "Memphis Grizzlies",
        "MIA": "Miami Heat",
        "MIL": "Milwaukee Bucks",
        "MIN": "Minnesota Timberwolves",
        "NOP": "New Orleans Pelicans",
        "NYK": "New York Knicks",
        "OKC": "Oklahoma City Thunder",
        "ORL": "Orlando Magic",
        "PHI": "Philadelphia 76ers",
        "PHX": "Phoenix Suns",
        "POR": "Portland Trail Blazers",
        "SAC": "Sacramento Kings",
        "SAS": "San Antonio Spurs",
        "TOR": "Toronto Raptors",
        "UTA": "Utah Jazz",
        "WAS": "Washington Wizards"
    }

def getTeamFromPlayer(player: str):
    return getTeamName(playerDic[player])

def getTeamAdvStats(team: str):
    return dicTeamsStrength[team]

def addStuff(player, team, val):
    bbn = t.getPlayerBBName(player)

    offset = 0

    url = f"https://www.basketball-reference.com/players/j/{bbn}/gamelog/2025"
    data = pd.read_html(url)
    ds = data[7]
    ds = ds[ds['Team'] != 'Team']
    ds = ds[ds['PTS'] != 'Inactive']
    ds = ds[ds['PTS'] != 'Not With Team']
    ds = ds[ds['PTS'] != 'Did Not Dress']

    url = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"
    voodoo = pd.read_html(url)
    dataEast = voodoo[0]['Eastern Conference']
    dataWest = voodoo[1]['Western Conference']

    opps = ds['Opp']
    opps = opps[opps != 'Opp']
    opps = opps.replace('PHO', 'PHX')
    opps = opps.replace('BRK', 'BKN')
    opps = opps.replace('CHO', 'CHA')

    for i in range(20):
        ptsArr = ds['PTS'].to_numpy()[offset:offset + val]
        rebArr = ds['TRB'].to_numpy()[offset:offset + val]
        astArr = ds['AST'].to_numpy()[offset:offset + val]
        stlArr = ds['STL'].to_numpy()[offset:offset + val]
        blkArr = ds['BLK'].to_numpy()[offset:offset + val]
        tovArr = ds['TOV'].to_numpy()[offset:offset + val]
        tpmArr = ds['3P'].to_numpy()[offset:offset + val]
        ftmArr = ds['FT'].to_numpy()[offset:offset + val]
        fgArr = ds['FG'].to_numpy()[offset:offset + val]
        ftaArr = ds['FTA'].to_numpy()[offset:offset + val]
        fgaArr = ds['FGA'].to_numpy()[offset:offset + val]

        statVals = {}
        for i in [-2, -1, 1, 2, 4]:
            statVals[i] = []

        statVals[-2].append(tovArr)
        statVals[-1].extend([fgaArr, ftaArr])
        statVals[1].extend([ptsArr, rebArr, tpmArr, ftmArr, fgArr])
        statVals[2].append(astArr)
        statVals[4].extend([stlArr, blkArr])

        calculated = t.calculateFantasyAvg(statVals, ptsArr)

        ptsArr = ds['PTS'].to_numpy()[offset + val]
        rebArr = ds['TRB'].to_numpy()[offset + val]
        astArr = ds['AST'].to_numpy()[offset + val]
        stlArr = ds['STL'].to_numpy()[offset + val]
        blkArr = ds['BLK'].to_numpy()[offset + val]
        tovArr = ds['TOV'].to_numpy()[offset + val]
        tpmArr = ds['3P'].to_numpy()[offset + val]
        ftmArr = ds['FT'].to_numpy()[offset + val]
        fgArr = ds['FG'].to_numpy()[offset + val]
        ftaArr = ds['FTA'].to_numpy()[offset + val]
        fgaArr = ds['FGA'].to_numpy()[offset + val]

        statVals = {}
        for i in [-2, -1, 1, 2, 4]:
            statVals[i] = []

        statVals[-2].append(tovArr)
        statVals[-1].extend([fgaArr, ftaArr])
        statVals[1].extend([ptsArr, rebArr, tpmArr, ftmArr, fgArr])
        statVals[2].append(astArr)
        statVals[4].extend([stlArr, blkArr])

        calcOne = t.calculateFantasyAvg(statVals, [1])

        tot = 0
        for j in range(val):
            gang = offset + j
            voodd = getTeamName(opps.iloc[gang])
            tot += gtt(voodd, dataEast, dataWest)
        tot /= val
        s = f"{player},{calculated},{val},{gtt(team, dataEast, dataWest)},{tot},{calcOne}"
        s += "\n"
        f.write(s)

        offset += 2

def getPlayers():
    url = "https://www.basketball-reference.com/contracts/players.html"
    db = pd.read_html(url)
    lst = []
    for info in db[0].values:
        if not pd.isna(info[1]) and info[1] != "Player":
            lst.append(info[1])

    return lst


def gtt(team: str, dataEast, dataWest):
    for i in range(len(dataEast)):
        if team.lower() in dataEast[i].lower():
            return i + 1

    for i in range(len(dataWest)):
        if team.lower() in dataWest[i].lower():
            return i + 1

    return -1

def getTeamName(abb):
    return nba_teams[abb]




arrDRTG = []
arrDEFG = []
arrDTOV = []
arrDDREB = []
arrDFTFGA = []

# for play in playerDic:
#     try:
#         bbn = t.getPlayerBBName(play)
#         url = f"https://www.basketball-reference.com/players/j/{bbn}/gamelog/2025"
#         ds = pd.read_html(url)[7]
#         ds = ds[ds['Team'] != 'Team']
#         ds = ds[ds['PTS'] != 'Inactive']
#         ds = ds[ds['PTS'] != 'Not With Team']
#         ds = ds[ds['PTS'] != 'Did Not Dress']
#
#         opps = ds['Opp']
#         opps = opps[opps != 'Opp']
#         opps = opps.replace('PHO', 'PHX')
#         opps = opps.replace('BRK', 'BKN')
#         opps = opps.replace('CHO', 'CHA')
#
#         offset = 2
#         for i in range(20):
#             teamDLst = getTeamAdvStats(getTeamName(opps.to_numpy()[offset]))
#             arrDRTG.append(teamDLst[0])
#             arrDEFG.append(teamDLst[1])
#             arrDTOV.append(teamDLst[2])
#             arrDDREB.append(teamDLst[3])
#             arrDFTFGA.append(teamDLst[4])
#             offset += 2
#         time.sleep((random.random() + 1) * 4)
#     except Exception as e:
#         print(e)
#
# np.savez("/Users/ankul/Documents/saveArr.npz", DRTG=arrDRTG, DTOV=arrDTOV, DEFG=arrDEFG, DDREB=arrDDREB, DFTFGA=arrDFTFGA)

playerCSV = pd.read_csv("/Users/ankul/Documents/myPlayers.csv")
playerCSV['DRTG'] = arrDRTG
playerCSV['DTOV'] = arrDTOV
playerCSV['DEFG'] = arrDEFG
playerCSV['DDREB'] = arrDDREB
playerCSV['DFTFGA'] = arrDFTFGA

cols = playerCSV.columns.tolist()
cols.insert(5, cols.pop(cols.index("DRTG")))
cols.insert(6, cols.pop(cols.index("DTOV")))
cols.insert(7, cols.pop(cols.index("DEFG")))
cols.insert(8, cols.pop(cols.index("DDREB")))
cols.insert(9, cols.pop(cols.index("DFTFGA")))
playerCSV = playerCSV[cols]
playerCSV.to_csv("/Users/ankul/Documents/myPlayersNewCol0.csv", index=False)

# for player in playerDic:
#     if playerDic[player] == "PHO":
#         playerDic[player] = "PHX"
#     elif playerDic[player] == "BRK":
#         playerDic[player] = "BKN"
#     elif playerDic[player] == "CHO":
#         playerDic[player] = "CHA"
#
#     try:
#         addStuff(player, nba_teams[playerDic[player]], 3)
#     except:
#         continue
#     time.sleep((random.random() + 1.001) * 5)

# datF = pd.read_csv('/Users/ankul/Documents/myPlayers0.csv')
# datF.insert(2, "NumGames", "2")
# datF.to_csv('/Users/ankul/Documents/myPlayersNewCol0.csv', index=False)
