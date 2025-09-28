import pandas as pd
import testing as t
import time

url = "https://www.basketball-reference.com/players/j/bridgmi01/gamelog/2025"
data = pd.read_html(url)
ds = data[7]

url = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"
voodoo = pd.read_html(url)
dataEast = voodoo[0]['Eastern Conference']
dataWest = voodoo[1]['Western Conference']

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

def getPlayers():
    url = "https://www.basketball-reference.com/contracts/players.html"
    db = pd.read_html(url)
    lst = []
    for info in db[0].values:
        if not pd.isna(info[1]) and info[1] != "Player":
            lst.append(info[1])

    return lst

def calc(offset: int):
    ptsArr = ds['PTS'].to_numpy()[offset:offset+3]
    rebArr = ds['TRB'].to_numpy()[offset:offset+3]
    astArr = ds['AST'].to_numpy()[offset:offset+3]
    stlArr = ds['STL'].to_numpy()[offset:offset+3]
    blkArr = ds['BLK'].to_numpy()[offset:offset+3]
    tovArr = ds['TOV'].to_numpy()[offset:offset+3]
    tpmArr = ds['3P'].to_numpy()[offset:offset+3]
    ftmArr = ds['FT'].to_numpy()[offset:offset+3]
    fgArr = ds['FG'].to_numpy()[offset:offset+3]
    ftaArr = ds['FTA'].to_numpy()[offset:offset+3]
    fgaArr = ds['FGA'].to_numpy()[offset:offset+3]

    statVals = {}
    for i in [-2, -1, 1, 2, 4]:
        statVals[i] = []

    statVals[-2].append(tovArr)
    statVals[-1].extend([fgaArr, ftaArr])
    statVals[1].extend([ptsArr, rebArr, tpmArr, ftmArr, fgArr])
    statVals[2].append(astArr)
    statVals[4].extend([stlArr, blkArr])

    return t.calculateFantasyAvg(statVals, ptsArr)

def calcOne(offset: int):
    ptsArr = ds['PTS'].to_numpy()[offset+3]
    rebArr = ds['TRB'].to_numpy()[offset+3]
    astArr = ds['AST'].to_numpy()[offset+3]
    stlArr = ds['STL'].to_numpy()[offset+3]
    blkArr = ds['BLK'].to_numpy()[offset+3]
    tovArr = ds['TOV'].to_numpy()[offset+3]
    tpmArr = ds['3P'].to_numpy()[offset+3]
    ftmArr = ds['FT'].to_numpy()[offset+3]
    fgArr = ds['FG'].to_numpy()[offset+3]
    ftaArr = ds['FTA'].to_numpy()[offset+3]
    fgaArr = ds['FGA'].to_numpy()[offset+3]

    statVals = {}
    for i in [-2, -1, 1, 2, 4]:
        statVals[i] = []

    statVals[-2].append(tovArr)
    statVals[-1].extend([fgaArr, ftaArr])
    statVals[1].extend([ptsArr, rebArr, tpmArr, ftmArr, fgArr])
    statVals[2].append(astArr)
    statVals[4].extend([stlArr, blkArr])


    return t.calculateFantasyAvg(statVals, [1])

def gtt(team: str):

    for i in range(len(dataEast)):
        if team.lower() in dataEast[i].lower():
            return i + 1

    for i in range(len(dataWest)):
        if team.lower() in dataWest[i].lower():
            return i + 1

    return -1

def getTeamName(abb):
    return nba_teams[abb]

def getOpps():
    return ds['Opp']

lst = getPlayers()
opps = getOpps()
opps = opps[opps.notna()]
opps = opps[opps != 'Opp']
opps = opps.replace('PHO', 'PHX')
opps = opps.replace('BRK', 'BKN')
opps = opps.replace('CHO', 'CHA')
with open('/Users/ankul/Documents/myPlayers0.csv', 'a') as f:
    off = 0
    for i in range(20):
        tot = 0
        for j in range(3):
            gang = off + j
            voodd = getTeamName(opps.iloc[gang])
            tot += gtt(voodd)
        tot /= 3
        calcL = calcOne(off)
        s = f"Zach Lavine, {calc(off)}, {gtt('Chicago Bulls')}, {tot}, {calcL},"
        s += "\n"
        f.write(s)
        off += 3
    f.close()


tot = 0
off = 7
for j in range(3):
    gang = off + j
    voodd = getTeamName(opps.iloc[gang])
    tot += gtt(voodd)
tot /= 3
print(calc(off))
print(gtt('Charlotte Hornets'))
print(tot)
print(calcOne(off))