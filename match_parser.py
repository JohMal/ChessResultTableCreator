import requests
import chess_result_parser as crp
import dewis_api as dewis
from models import GameResult, Match, MatchResult, Team, Game

def parse_match_from_url(url: str, own_team_key: str, club_zps_dict: dict[str, int]) -> Match:
    response = requests.get(url)
    header_row, game_rows = crp.extract_table_rows(response.text, own_team_key)
    if header_row is None or game_rows is None:
        return None
    home_team_name, guest_team_name = crp.find_team_names(header_row)
    possible_zps = dewis.find_potential_zps(home_team_name, club_zps_dict) + dewis.find_potential_zps(guest_team_name, club_zps_dict)
    dwz_dict = dewis.get_dwz_dict(possible_zps)
    games = [crp.extract_game(row, dwz_dict) for row in game_rows]
    match_result = _get_match_result(games, crp.find_match_result(header_row))
    home_team_rating, guest_team_rating = _get_avarage_rating(games)
    return Match(home_team=Team(home_team_name, home_team_rating),
                 guest_team=Team(guest_team_name, guest_team_rating),
                 games=games,
                 result=match_result)

def _get_match_result(games: list[Game], parsed_result: str) -> MatchResult:
    home_points = 0.0
    guest_points = 0.0
    for game in games:      
        if game.result is GameResult.HOME_TEAM_WIN or game.result is GameResult.HOME_TEAM_DEFAULT_WIN:
            home_points += 1.0
        elif game.result is GameResult.GUEST_TEAM_WIN or game.result is GameResult.GUEST_TEAM_DEFAULT_WIN:
            guest_points += 1.0
        elif game.result is GameResult.DRAW:
            home_points += 0.5
            guest_points += 0.5
    if home_points == 0.0 and guest_points == 0.0:
        game_result = GameResult.UNKNOWN
    elif home_points > guest_points:
        game_result = GameResult.HOME_TEAM_WIN
    elif guest_points > home_points:
        game_result = GameResult.GUEST_TEAM_WIN
    else:
        game_result = GameResult.DRAW
    
    home_points = int(home_points) if home_points.is_integer() else home_points
    guest_points = int(guest_points) if guest_points.is_integer() else guest_points
    return MatchResult(home_points, guest_points, game_result, parsed_result)

def _get_avarage_rating(games: list[Game]) -> tuple[int, int]:
    home_ratings = []
    guest_ratings = []
    for game in games:
        if game.home_player.rating != 0:
            home_ratings.append(int(game.home_player.rating))
        if game.guest_player.rating != 0:
            guest_ratings.append(int(game.guest_player.rating))
    if len(home_ratings) == 0:
        home_avarage = 0
    else:
        home_avarage = round(sum(home_ratings) / len(home_ratings))
    if len(guest_ratings) == 0:
        guest_avarage = 0
    else:
        guest_avarage = round(sum(guest_ratings) / len(guest_ratings))
    return home_avarage, guest_avarage