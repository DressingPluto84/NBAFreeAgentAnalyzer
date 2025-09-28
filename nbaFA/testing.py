from typing import Dict
import pandas as pd
from datetime import date, datetime, timedelta


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def calculatePastNGamesFantasy(nameOfPlayer: str, numOfGames: int):
    try:
        url = f"https://www.basketball-reference.com/players/j/{nameOfPlayer}/gamelog/2025"
    except:
        print("Incorrect Player Name")
        return
    try:
        data = pd.read_html(url)
    except:
        return

    ds = data[7]

    ptsArr = ds['PTS'].tail(numOfGames).to_numpy()
    rebArr = ds['TRB'].tail(numOfGames).to_numpy()
    astArr = ds['AST'].tail(numOfGames).to_numpy()
    stlArr = ds['STL'].tail(numOfGames).to_numpy()
    blkArr = ds['BLK'].tail(numOfGames).to_numpy()
    tovArr = ds['TOV'].tail(numOfGames).to_numpy()
    tpmArr = ds['3P'].tail(numOfGames).to_numpy()
    ftmArr = ds['FT'].tail(numOfGames).to_numpy()
    fgArr = ds['FG'].tail(numOfGames).to_numpy()
    ftaArr = ds['FTA'].tail(numOfGames).to_numpy()
    fgaArr = ds['FGA'].tail(numOfGames).to_numpy()

    statVals = {}
    for i in [-2, -1, 1, 2, 4]:
        statVals[i] = []

    statVals[-2].append(tovArr)
    statVals[-1].extend([fgaArr, ftaArr])
    statVals[1].extend([ptsArr, rebArr, tpmArr, ftmArr, fgArr])
    statVals[2].append(astArr)
    statVals[4].extend([stlArr, blkArr])

    return calculateFantasyAvg(statVals, ptsArr)



def countGames(arr):
    games = 0

    for i in range(len(arr)):
        try:
            float(arr[i])
            games += 1
        except:
            continue

    return games

def sumCategory(arr):
    cat = 0

    for i in range(len(arr)):
        try:
            val = int(arr[i])
            cat += val
        except:
            continue

    return cat

def calculateFantasyAvg(dic: Dict, arr):
    total = 0
    games = countGames(arr)
    for i in dic:
        for j in dic[i]:
            total += int(i) * sumCategory(j)

    if games == 0:
        return 0
    return total / games

def isPlayerInjured(player: str):
    player = player.lower()
    url = "https://www.basketball-reference.com/friv/injuries.fcgi"
    data = pd.read_html(url)[0]['Player']

    for i in data:
        if player in i.lower():
            return True

    return False

def findTopTwoPlayers(team: str):
    url = f"https://www.basketball-reference.com/teams/{team}/2025.html"
    data = pd.read_html(url)
    topTwo = [data[1]['Player'][0], data[1]['Player'][1]]
    return topTwo

def getTeamRating(team: str):
    url = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"
    dataEast = pd.read_html(url)[0]['Eastern Conference']
    dataWest = pd.read_html(url)[1]['Western Conference']
    for i in range(len(dataEast)):
        if team.lower() in dataEast[i].lower():
            return i + 1

    for i in range(len(dataWest)):
        if team.lower() in dataWest[i].lower():
            return i + 1

    return -1

def getNextOpponents(team: str, start: date, numDays: int):
    url = f"https://www.basketball-reference.com/teams/{team}/2025_games.html"
    general = pd.read_html(url)[0]
    dates = pd.read_html(url)[0]['Date']
    toDrop = []
    for i in range(len(dates)):
        if 'Date' in dates[i]:
            toDrop.append(i)
    dates.drop(index=toDrop, inplace=True)
    general.drop(index=toDrop, inplace=True)
    dates = dates.reset_index(drop=True)
    general = general.reset_index(drop=True)

    i = 0
    while i < len(dates) and start.strftime("%b %-d, %Y") not in dates[i]:
        i += 1
    start += timedelta(days=numDays)
    beginning = i
    while i < len(dates) and datetime.strptime(dates[i][5:], "%b %d, %Y").date() < start:
        i += 1
    games = general['Opponent'][beginning:i]

    return games

def getPlayerBBName(nameOfPlayer):
    nameOfPlayer = nameOfPlayer.lower().split(" ")
    start = ""
    start += nameOfPlayer[1][:5]
    start += nameOfPlayer[0][:2]
    start += "01"
    return start

def mainTestLoop():
    nameOfPlayer = input("Enter name of player: ")
    numOfGames = input("Enter number of past games to examine: ")
    numOfGames = int(numOfGames) + 1
    start = getPlayerBBName(nameOfPlayer)
    print(calculatePastNGamesFantasy(start, numOfGames))

"""
url = "https://www.basketball-reference.com/teams/OKC/2025_games.html"
data = pd.read_html(url)
print(len(data[0]['Date']))
x = data[0]['Date'][0][5:]
myDate = datetime.strptime(x, "%b %d, %Y").date()
print(myDate.strftime("%b %d, %Y"))
"""

#myDate = datetime.strptime("Dec 19, 2024", "%b %d, %Y").date()
#print(getNextOpponents("OKC", myDate, 5))
