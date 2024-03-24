import re
from bs4 import BeautifulSoup, SoupStrainer, Tag
from models import GameResult, Game, Player
from utils import build_full_name

def extract_table_rows(html_content: str, own_team_key: str) -> tuple[Tag, Tag]:
    parsed_content = BeautifulSoup(html_content, "html.parser", parse_only=SoupStrainer("table"))
    own_team_element = parsed_content.find('th', string=re.compile('.*{}.*'.format(own_team_key)))
    if own_team_element is None:
        return None, None
    header_row = own_team_element.parent
    game_rows = []
    currentRow = header_row
    while currentRow == header_row or currentRow.find(['th', 'td']).name == 'td':
        currentRow = currentRow.find_next_sibling('tr')
        if currentRow is None:
            break
        if currentRow.find(['th', 'td']).name == 'td':
            game_rows.append(currentRow)
    return header_row, game_rows

def find_team_names(header_row: Tag) -> tuple[str, str]:
    entries: list[Tag] = header_row.find_all('th', recursive=False)
    home_team_name = str(entries[2].string).strip()
    guest_team_name = str(entries[6].string).strip()
    return home_team_name, guest_team_name

def find_match_result(header_row: Tag) -> str:
    entries: list[Tag] = header_row.find_all('th', recursive=False)
    if entries[8].string is None:
        return GameResult.UNKNOWN.value
    return str(entries[8].string)

def extract_game(game_row: Tag, dwz_dict: dict[str, int]) -> Game:
    entries: list[Tag] = game_row.find_all('td', recursive=False)    
    home_player_name = _extract_player_name(entries[2])
    home_player = Player(
        name=home_player_name,
        rating=_extract_player_rating(entries[3], home_player_name, dwz_dict)
    )
    guest_player_name = _extract_player_name(entries[6])
    guest_player = Player(
        name=guest_player_name,
        rating=_extract_player_rating(entries[7], guest_player_name, dwz_dict)
    )
    return Game(
        home_player=home_player,
        guest_player=guest_player,
        result=_extract_game_result(entries[8])
    )

def _extract_player_name(name_row: Tag) -> str:
    player_name = str(name_row.find(string=True).string).strip()
    name_parts = player_name.split(",")
    title = None
    first_name = None
    last_name = None
    if len(name_parts) > 0:
        last_name = name_parts[0]
    if len(name_parts) > 1:
        first_name = name_parts[1]
    if len(name_parts) > 2:
        title = name_parts[2]
    return build_full_name(title, first_name, last_name)

def _extract_player_rating(rating_row: Tag, player_name: str, dwz_dict: dict[str, int]) -> str:
    if dwz_dict.get(player_name) is None:
        print("Could not find rating for player {}. Taking rating from chess-results instead.".format(player_name))
        return str(rating_row.string)
    return dwz_dict[player_name]

def _extract_game_result(result_row: Tag) -> GameResult:
    if result_row.string is None:
        return GameResult.UNKNOWN
    return GameResult(str(result_row.string))