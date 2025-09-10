from typing import Dict
import pandas as pd
from datetime import date, datetime, timedelta

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

    for i in range(len(arr) - 1):
        try:
            float(arr[i])
            games += 1
        except:
            continue

    return games

def sumCategory(arr):
    cat = 0

    for i in range(len(arr) - 1):
        try:
            val = float(arr[i])
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

def getNextOpponents(team: str):
    games = []
    url = f"https://www.basketball-reference.com/teams/{team}/2025_games.html"
    dates = pd.read_html(url)[0]['Date']
    for i in range(len(dates)):
        if 'Date' in dates[i]:
            dates.drop(index=i)
    print(len(dates))



def bibimbap():
    nameOfPlayer = input("Enter name of player: ")

    nameOfPlayer = nameOfPlayer.lower().split(" ")
    numOfGames = input("Enter number of past games to examine: ")
    numOfGames = int(numOfGames) + 1
    start = ""
    start += nameOfPlayer[1][:5]
    start += nameOfPlayer[0][:2]
    start += "01"
    print(calculatePastNGamesFantasy(start, numOfGames))

"""
url = "https://www.basketball-reference.com/teams/OKC/2025_games.html"
data = pd.read_html(url)
print(len(data[0]['Date']))
x = data[0]['Date'][0][5:]
myDate = datetime.strptime(x, "%b %d, %Y").date()
print(myDate.strftime("%b %d, %Y"))
"""

getNextOpponents("OKC")
