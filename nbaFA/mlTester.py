import pandas as pd
import testing as t

def getPlayers():
    url = "https://www.basketball-reference.com/contracts/players.html"
    db = pd.read_html(url)
    lst = []
    for info in db[0].values:
        if not pd.isna(info[1]) and info[1] != "Player":
            lst.append(info[1])

    return lst

def calc(nameOfPlayer: str, numOfGames: int):
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

    ptsArr = ds['PTS'].head(numOfGames).to_numpy()
    rebArr = ds['TRB'].head(numOfGames).to_numpy()
    astArr = ds['AST'].head(numOfGames).to_numpy()
    stlArr = ds['STL'].head(numOfGames).to_numpy()
    blkArr = ds['BLK'].head(numOfGames).to_numpy()
    tovArr = ds['TOV'].head(numOfGames).to_numpy()
    tpmArr = ds['3P'].head(numOfGames).to_numpy()
    ftmArr = ds['FT'].head(numOfGames).to_numpy()
    fgArr = ds['FG'].head(numOfGames).to_numpy()
    ftaArr = ds['FTA'].head(numOfGames).to_numpy()
    fgaArr = ds['FGA'].head(numOfGames).to_numpy()

    statVals = {}
    for i in [-2, -1, 1, 2, 4]:
        statVals[i] = []

    statVals[-2].append(tovArr)
    statVals[-1].extend([fgaArr, ftaArr])
    statVals[1].extend([ptsArr, rebArr, tpmArr, ftmArr, fgArr])
    statVals[2].append(astArr)
    statVals[4].extend([stlArr, blkArr])

    return t.calculateFantasyAvg(statVals, ptsArr)

lst = getPlayers()
print(calc(lst[0], 5))