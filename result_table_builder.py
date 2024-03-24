from models import GameResult, Match

_color_win = "#CCFFCC"
_color_lose = "#FFCCCC"
_color_draw = "#FFFFCC"
_color_player = "#CCFFFF"
_color_trans = "#00"

_result_table_header_template = """
<thead>
    <tr style="background-color: #80A7D9">
        <th colspan="10">{home_team} - {guest_team}</th>
    </tr>
</thead>
<tbody>
    <tr style="background-color: #80A7D9">
        <th>Brett</th>
        <th>{home_team}</th>
        <th style="text-align: right;">DWZ</th>
        <th style="width: 20px; text-align: center">-</th>
        <th>{guest_team}</th>
        <th style="text-align: right;">DWZ</th>
        <th>Ergebnis</th>
    </tr>
</tbody>"""

_result_table_game_template = """
<tr>
    <td style="text-align: center;">{board}</td>
    <td style="background-color:{home_player_bg}">{home_player_name}</td>
    <td style="text-align: right;">{home_player_rating}</td>
    <td style="text-align: center;">-</td>
    <td style="background-color:{guest_player_bg}">{guest_player_name}</td>
    <td style="text-align: right;">{guest_player_rating}</td>
    <td style="background-color:{result_bg}; text-align: center;">{result}</td>
</tr>"""

_result_table_summary_template = """
<tr>
    <td style="text-align: right;">&nbsp</td>
    <td>&nbsp</td>
    <td style="text-align: right;">&Oslash;{home_team_rating}</td>
    <td style="text-align: center;">&nbsp</td>
    <td>&nbsp</td>
    <td style="text-align: right;">&Oslash;{guest_team_rating}</td>
    <td style="background-color:{result_bg}; text-align: center;">
        <b>{result}</b>
    </td>
</tr>"""

def build_result_table(match: Match, own_team_key: str) -> str:
    own_is_home_team = own_team_key.lower() in match.home_team.name.lower()
    result_table = '<table border="1" frame="border" rules="groups" style="text-align: left">'
    result_table += _result_table_header_template.format(home_team = match.home_team.name, guest_team = match.guest_team.name)
    result_table += "<tbody>"
    for i, game in enumerate(match.games):
        result_table += _result_table_game_template.format(board = i + 1, 
                                                          home_player_name = game.home_player.name,
                                                          home_player_rating = game.home_player.rating,
                                                          home_player_bg = _color_player if own_is_home_team else _color_trans,
                                                          guest_player_name = game.guest_player.name,
                                                          guest_player_rating = game.guest_player.rating,
                                                          guest_player_bg = _color_player if not own_is_home_team else _color_trans,
                                                          result = game.result.value,
                                                          result_bg = _get_result_color(game.result, own_is_home_team))
    if match.result.result is GameResult.UNKNOWN:
        match_result = match.result.parsed_result
    else:
        match_result = str(match.result.home_team_points) + " - " + str(match.result.guest_team_points)
    result_table += _result_table_summary_template.format(home_team_rating = match.home_team.avarage_rating,
                                                   guest_team_rating = match.guest_team.avarage_rating,
                                                   result = match_result,
                                                   result_bg = _get_result_color(match.result.result, own_is_home_team))
    result_table += "</tbody></table>"
    return result_table

def _get_result_color(game_result: GameResult, own_is_home_team: bool) -> str:
    home_team_win = game_result is GameResult.HOME_TEAM_WIN or game_result is GameResult.HOME_TEAM_DEFAULT_WIN
    guest_team_win = game_result is GameResult.GUEST_TEAM_WIN or game_result is GameResult.GUEST_TEAM_DEFAULT_WIN
    if game_result is GameResult.UNKNOWN:
        return _color_trans
    elif game_result is GameResult.DRAW:
        return _color_draw
    elif (home_team_win and own_is_home_team) or (guest_team_win and not own_is_home_team):
        return _color_win
    else:
        return _color_lose