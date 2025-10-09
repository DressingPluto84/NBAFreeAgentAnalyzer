import pandas as pd
import getCurrSeasonStats as t

# --- Constants ---------------------------------------------------------------

NBA_TEAMS = {
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

# --- Data Loading ------------------------------------------------------------

PLAYER_URL = "https://www.basketball-reference.com/players/j/bridgmi01/gamelog/2025"
STANDINGS_URL = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"

# Load player game log
player_data = pd.read_html(PLAYER_URL)[7]

# Load standings
standings_data = pd.read_html(STANDINGS_URL)
east_teams = standings_data[0]['Eastern Conference']
west_teams = standings_data[1]['Western Conference']

# --- Helper Functions --------------------------------------------------------

def get_players() -> list[str]:
    """Return a list of player names from the contracts page."""
    url = "https://www.basketball-reference.com/contracts/players.html"
    db = pd.read_html(url)[0]
    players = [row[1] for row in db.values if not pd.isna(row[1]) and row[1] != "Player"]
    return players


def get_team_name(abbreviation: str) -> str:
    """Return full NBA team name from abbreviation."""
    return NBA_TEAMS.get(abbreviation, abbreviation)


def get_team_rank(team: str) -> int:
    """Return the team’s rank in standings."""
    team_lower = team.lower()
    for i, name in enumerate(east_teams):
        if team_lower in str(name).lower():
            return i + 1
    for i, name in enumerate(west_teams):
        if team_lower in str(name).lower():
            return i + 1
    return -1


def get_opponents() -> pd.Series:
    """Return opponent abbreviations from the player game log."""
    return player_data['Opp']


# --- Fantasy Stat Calculation ------------------------------------------------

def _get_stat_slice(offset: int, length: int = 3) -> dict[int, list]:
    """Extract stats for a given offset and length into the scoring structure."""
    ds = player_data
    slice_stats = {
        -2: [ds['TOV'].to_numpy()[offset:offset + length]],
        -1: [ds['FGA'].to_numpy()[offset:offset + length],
             ds['FTA'].to_numpy()[offset:offset + length]],
         1: [ds['PTS'].to_numpy()[offset:offset + length],
             ds['TRB'].to_numpy()[offset:offset + length],
             ds['3P'].to_numpy()[offset:offset + length],
             ds['FT'].to_numpy()[offset:offset + length],
             ds['FG'].to_numpy()[offset:offset + length]],
         2: [ds['AST'].to_numpy()[offset:offset + length]],
         4: [ds['STL'].to_numpy()[offset:offset + length],
             ds['BLK'].to_numpy()[offset:offset + length]]
    }
    return slice_stats


def calculate_window(offset: int, window_size: int = 3) -> float:
    """Calculate fantasy average for a window of games."""
    ds = player_data
    pts_array = ds['PTS'].to_numpy()[offset:offset + window_size]
    stats = _get_stat_slice(offset, window_size)
    return t.calculateFantasyAvg(stats, pts_array)


def calculate_single(offset: int, next_game_offset: int = 3) -> float:
    """Calculate fantasy points for a single game after a window."""
    ds = player_data
    idx = offset + next_game_offset
    slice_stats = {
        -2: [ds['TOV'].iloc[idx]],
        -1: [ds['FGA'].iloc[idx], ds['FTA'].iloc[idx]],
         1: [ds['PTS'].iloc[idx], ds['TRB'].iloc[idx], ds['3P'].iloc[idx],
             ds['FT'].iloc[idx], ds['FG'].iloc[idx]],
         2: [ds['AST'].iloc[idx]],
         4: [ds['STL'].iloc[idx], ds['BLK'].iloc[idx]]
    }
    return t.calculateFantasyAvg(slice_stats, [1])


# --- Example (commented) -----------------------------------------------------
#
# opps = get_opponents()
# opps = opps[opps.notna()]
# opps = opps[opps != 'Opp']
# opps = opps.replace({'PHO': 'PHX', 'BRK': 'BKN', 'CHO': 'CHA'})
#
# with open('/Users/ankul/Documents/myPlayers0.csv', 'a') as f:
#     offset = 0
#     for _ in range(20):
#         # Average opponent rank across next 3 games
#         avg_rank = sum(
#             get_team_rank(get_team_name(opps.iloc[offset + j]))
#             for j in range(3)
#         ) / 3
#
#         avg_stats = calculate_window(offset)
#         next_game_stats = calculate_single(offset)
#
#         row = f"Zach Lavine,{avg_stats},{get_team_rank('Chicago Bulls')},{avg_rank},{next_game_stats}\n"
#         f.write(row)
#
#         offset += 3
#
# print(calculate_window(7))
# print(get_team_rank('Charlotte Hornets'))
# print(calculate_single(7))
