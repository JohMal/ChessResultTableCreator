import requests
import xml.etree.ElementTree as ET
from utils import build_full_name
from bs4 import BeautifulSoup, SoupStrainer, Tag

_dewis_api_url = "https://www.schachbund.de/php/dewis/verein.php?format=xml"
_clubs_zps_url = "https://www.schachbund.de/verein/{zps_region_code}.html"

def get_dwz_dict(zps_list: list[int]) -> dict[str, int]:
    player_dwz_dict = {}
    for zps in zps_list:
        response = requests.get(_dewis_api_url + "&zps=" + str(zps))
        parsed_player_data = ET.fromstring(response.text).findall('Spieler')   
        for player in parsed_player_data:
            first_name = player.find('vorname').text
            last_name = player.find('nachname').text
            title = player.find('titel').text
            rating = int(player.find('dwz').text) if player.find('dwz').text is not None else 0
            player_dwz_dict[build_full_name(title, first_name, last_name)] = rating
    return player_dwz_dict

def get_club_zps(zps_region_code: int) -> dict[str, int]:
    response = requests.get(_clubs_zps_url.format(zps_region_code=zps_region_code))
    parsed_content = BeautifulSoup(response.text, "html.parser", parse_only=SoupStrainer("table"))
    zps_entry = parsed_content.find(string='ZPS')
    if zps_entry is None:
        return None
    zps_table = zps_entry.find_parent('table')
    if zps_table is None:
        return None
    zps_dict = {}
    for entry in zps_table.find_all('tr'):
        zps: Tag = entry.find('td')
        if zps is not None:
            club_name: Tag = zps.find_next_sibling('td')
        if zps is not None and club_name is not None:
            zps_dict[str(club_name.string)] = int(zps.string)
    if len(zps_table) == 0:
        return None
    return zps_dict

def find_potential_zps(club_name: str, zps_dict: dict[str, int]) -> list[int]:
    search_term = max(club_name.split(), key=len)
    return [zps_dict[name] for name in zps_dict.keys() if search_term in name]