from typing import Dict
import pandas as pd
from datetime import date, datetime, timedelta

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def calculate_past_n_games_fantasy(player_id: str, num_games: int) -> float:
    """
    Calculate a player's average fantasy score over their past N games.
    """
    url = f"https://www.basketball-reference.com/players/j/{player_id}/gamelog/2025"

    try:
        data = pd.read_html(url)
    except Exception:
        print(f"Error: Could not fetch data for {player_id}")
        return 0.0

    df = data[7]
    stats = {
        "PTS": 1, "TRB": 1, "AST": 2, "STL": 4, "BLK": 4,
        "TOV": -2, "3P": 1, "FT": 1, "FG": 1, "FTA": -1, "FGA": -1
    }

    stat_values = {k: df[k].tail(num_games).to_numpy() for k in stats if k in df.columns}
    return calculate_fantasy_avg(stats, stat_values)


def count_games(arr) -> int:
    """Count valid (numeric) game entries."""
    return sum(1 for x in arr if _is_number(x))


def sum_category(arr) -> int:
    """Sum numeric values in an array, skipping invalid entries."""
    return sum(int(x) for x in arr if _is_number(x))


def _is_number(x) -> bool:
    try:
        float(x)
        return True
    except (ValueError, TypeError):
        return False


def calculate_fantasy_avg(weights: Dict[str, int], stats: Dict[str, list]) -> float:
    """
    Compute average fantasy points per game given stat weights and values.
    """
    any_stat = next(iter(stats.values()))
    games = count_games(any_stat)
    if games == 0:
        return 0.0

    total = sum(weights[k] * sum_category(v) for k, v in stats.items())
    return total / games


def is_player_injured(player_name: str) -> bool:
    """Return True if the player is listed as injured on Basketball Reference."""
    url = "https://www.basketball-reference.com/friv/injuries.fcgi"
    data = pd.read_html(url)[0]["Player"]

    player_name = player_name.lower()
    return any(player_name in name.lower() for name in data)


def find_top_two_players(team: str) -> list[str]:
    """Return the top two players on the given team’s Basketball Reference page."""
    url = f"https://www.basketball-reference.com/teams/{team}/2025.html"
    data = pd.read_html(url)
    return list(data[1]["Player"][:2])


def get_team_rating(team: str) -> int:
    """Return a team's standing position (1-based rank)."""
    url = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"
    east, west = pd.read_html(url)[0]["Eastern Conference"], pd.read_html(url)[1]["Western Conference"]

    for i, name in enumerate(east):
        if team.lower() in name.lower():
            return i + 1
    for i, name in enumerate(west):
        if team.lower() in name.lower():
            return i + 1

    return -1


def get_next_opponents(team: str, start_date: date, num_days: int):
    """
    Return a list of the team's opponents within the next `num_days` from `start_date`.
    """
    url = f"https://www.basketball-reference.com/teams/{team}/2025_games.html"
    df = pd.read_html(url)[0]

    dates = df["Date"].dropna().reset_index(drop=True)
    opponents = df["Opponent"].reset_index(drop=True)

    # Skip headers or invalid entries
    valid_rows = [i for i, d in enumerate(dates) if "Date" not in str(d)]
    dates = dates.iloc[valid_rows].reset_index(drop=True)
    opponents = opponents.iloc[valid_rows].reset_index(drop=True)

    start_date_str = start_date.strftime("%b %-d, %Y")
    i = next((idx for idx, d in enumerate(dates) if start_date_str in d), len(dates))

    end_date = start_date + timedelta(days=num_days)
    beginning = i

    while i < len(dates) and datetime.strptime(dates[i][5:], "%b %d, %Y").date() < end_date:
        i += 1

    return opponents[beginning:i]


def get_player_bbref_id(player_name: str) -> str:
    """
    Convert a player's full name to their Basketball Reference ID format.
    Example: 'LeBron James' -> 'jamesle01'
    """
    first, last = player_name.lower().split()
    return f"{last[:5]}{first[:2]}01"


def main():
    """Simple CLI test."""
    player_name = input("Enter player name: ")
    num_games = int(input("Enter number of past games to examine: ")) + 1
    player_id = get_player_bbref_id(player_name)

    score = calculate_past_n_games_fantasy(player_id, num_games)
    print(f"Average fantasy score over last {num_games - 1} games: {score:.2f}")


if __name__ == "__main__":
    main()
