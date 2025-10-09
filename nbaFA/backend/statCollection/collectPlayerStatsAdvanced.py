import pandas as pd
from unidecode import unidecode
from backend.statCollection import getCurrSeasonStats as t

# --- File paths ---
PLAYERS_CSV_PATH = "/Users/ankul/Documents/myPlayers0.csv"
PLAYERS_INPUT_PATH = "/Users/ankul/Documents/myPlayers.csv"
OUTPUT_PATH = "/Users/ankul/Documents/myPlayersNewCol0.csv"

# --- URLs ---
TOTALS_URL = "https://www.basketball-reference.com/leagues/NBA_2025_totals.html"
STATS_URL = "https://www.basketball-reference.com/leagues/NBA_2025.html"
STANDINGS_URL = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"
CONTRACTS_URL = "https://www.basketball-reference.com/contracts/players.html"

# --- Initialize ---
with open(PLAYERS_CSV_PATH, "a") as f:
    plays = pd.read_html(TOTALS_URL)[0]
    plays = plays[~plays["Team"].isin(["2TM", "3TM"])]
    plays = plays[plays["Player"] != "Player"]
    plays = plays[["Player", "Team"]].drop_duplicates(subset="Player", keep="first")[:250]
    plays["Player"] = plays["Player"].apply(unidecode)

playerDic = dict(zip(plays["Player"], plays["Team"]))

# --- Team Strengths ---
dicTeamsStrength = {}
tab = pd.read_html(STATS_URL)[10]

for row in tab.values[:-1]:
    team_name = row[1].replace("*", "")
    dicTeamsStrength[team_name] = [row[11], row[23], row[24], row[25], row[26]]

# --- Team abbreviations ---
nba_teams = {
    "ATL": "Atlanta Hawks", "BOS": "Boston Celtics", "BKN": "Brooklyn Nets",
    "CHA": "Charlotte Hornets", "CHI": "Chicago Bulls", "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks", "DEN": "Denver Nuggets", "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors", "HOU": "Houston Rockets", "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers", "LAL": "Los Angeles Lakers", "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat", "MIL": "Milwaukee Bucks", "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans", "NYK": "New York Knicks", "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic", "PHI": "Philadelphia 76ers", "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers", "SAC": "Sacramento Kings", "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors", "UTA": "Utah Jazz", "WAS": "Washington Wizards"
}


# --- Utility functions ---
def getTeamFromPlayer(player: str) -> str:
    """Get team full name from player name."""
    return getTeamName(playerDic[player])


def getTeamAdvStats(team: str):
    """Return advanced stats for a given team."""
    return dicTeamsStrength[team]


def getPlayers():
    """Return list of all player names from contracts page."""
    db = pd.read_html(CONTRACTS_URL)[0]
    return [row[1] for row in db.values if not pd.isna(row[1]) and row[1] != "Player"]


def gtt(team: str, dataEast, dataWest) -> int:
    """Return team rank based on standings."""
    for i, name in enumerate(dataEast):
        if team.lower() in name.lower():
            return i + 1
    for i, name in enumerate(dataWest):
        if team.lower() in name.lower():
            return i + 1
    return -1


def getTeamName(abbr: str) -> str:
    """Convert abbreviation to full team name."""
    return nba_teams.get(abbr, abbr)


def addStuff(player, team, val):
    """
    Compute fantasy averages for a player based on recent games and write to CSV.
    """
    bbn = t.getPlayerBBName(player)
    url = f"https://www.basketball-reference.com/players/j/{bbn}/gamelog/2025"
    data = pd.read_html(url)
    ds = data[7]

    # Filter valid games
    ds = ds[~ds["Team"].isin(["Team"])]
    ds = ds[~ds["PTS"].isin(["Inactive", "Not With Team", "Did Not Dress"])]

    # Load standings
    voodoo = pd.read_html(STANDINGS_URL)
    dataEast = voodoo[0]["Eastern Conference"]
    dataWest = voodoo[1]["Western Conference"]

    # Clean opponent abbreviations
    opps = ds["Opp"].replace({"PHO": "PHX", "BRK": "BKN", "CHO": "CHA"})
    opps = opps[opps != "Opp"]

    offset = 0
    with open(PLAYERS_CSV_PATH, "a") as f:
        for _ in range(20):
            # Prepare game slices
            stats = {k: [] for k in [-2, -1, 1, 2, 4]}
            stat_cols = ["PTS", "TRB", "AST", "STL", "BLK", "TOV", "3P", "FT", "FG", "FTA", "FGA"]

            arrs = {col: ds[col].to_numpy()[offset:offset + val] for col in stat_cols}

            stats[-2].append(arrs["TOV"])
            stats[-1].extend([arrs["FGA"], arrs["FTA"]])
            stats[1].extend([arrs["PTS"], arrs["TRB"], arrs["3P"], arrs["FT"], arrs["FG"]])
            stats[2].append(arrs["AST"])
            stats[4].extend([arrs["STL"], arrs["BLK"]])

            calculated = t.calculateFantasyAvg(stats, arrs["PTS"])

            # Next game stats (target)
            arrs_next = {col: ds[col].to_numpy()[offset + val] for col in stat_cols}
            stats_next = {k: [] for k in [-2, -1, 1, 2, 4]}
            stats_next[-2].append(arrs_next["TOV"])
            stats_next[-1].extend([arrs_next["FGA"], arrs_next["FTA"]])
            stats_next[1].extend([arrs_next["PTS"], arrs_next["TRB"], arrs_next["3P"], arrs_next["FT"], arrs_next["FG"]])
            stats_next[2].append(arrs_next["AST"])
            stats_next[4].extend([arrs_next["STL"], arrs_next["BLK"]])

            calc_one = t.calculateFantasyAvg(stats_next, [1])

            # Compute opponent rank average
            total_rank = 0
            for j in range(val):
                opponent_team = getTeamName(opps.iloc[offset + j])
                total_rank += gtt(opponent_team, dataEast, dataWest)
            avg_rank = total_rank / val

            f.write(f"{player},{calculated},{val},{gtt(team, dataEast, dataWest)},{avg_rank},{calc_one}\n")

            offset += 2


# --- Advanced Stat Arrays ---
arrDRTG, arrDEFG, arrDTOV, arrDDREB, arrDFTFGA = [], [], [], [], []

# --- Attach empty advanced columns (placeholder arrays) ---
playerCSV = pd.read_csv(PLAYERS_INPUT_PATH)
playerCSV["DRTG"] = arrDRTG
playerCSV["DTOV"] = arrDTOV
playerCSV["DEFG"] = arrDEFG
playerCSV["DDREB"] = arrDDREB
playerCSV["DFTFGA"] = arrDFTFGA

# Reorder columns for better readability
cols = playerCSV.columns.tolist()
new_order = ["DRTG", "DTOV", "DEFG", "DDREB", "DFTFGA"]
for i, col in enumerate(new_order, start=5):
    cols.insert(i, cols.pop(cols.index(col)))

playerCSV = playerCSV[cols]
playerCSV.to_csv(OUTPUT_PATH, index=False)
