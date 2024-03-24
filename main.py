import match_parser as mp
import result_table_builder as rtb
import dewis_api as dewis
import user_input_parser as ip
from models import Match, TeamConfig, Config
from config import config
from utils import strip_multiline_text

def main():
    teams, rounds = ip.get_user_seclection(config.teams)
    _process(config, teams, rounds)
        

def _process(config: Config, teams: list[TeamConfig] = [], rounds: list[int] = []):
    club_zps_dict = dewis.get_club_zps(config.zps_region_code)
    if len(teams) == 0:
        teams = config.teams

    with open(config.result_file_name, "w") as file:
        for team in teams:
            print("Processing {}...".format(team.name))
            file.write("###### " + team.name + " ######")
            file.write("\n\n")
            if len(rounds) == 0:
                _process_all_rounds(team, file, club_zps_dict)
            else:
                _process_rounds(team, rounds, file, club_zps_dict)
    print("Finish!")

def _process_rounds(team: TeamConfig, rounds: list[int], file, nrw_club_zps_dict):
    for round in rounds:
        print("Creating table for round {}...".format(round))
        match, result_table = _generate_for_team_and_round(team, round, nrw_club_zps_dict)
        if (match is None):
            print("Round {} data is not valid. Skipping...".format(round))
            continue
        file.write("Round " + str(round) + ":\n") 
        file.write(strip_multiline_text(result_table))
        file.write("\n\n")
            
def _process_all_rounds(team: TeamConfig, file, nrw_club_zps_dict):
    round = 1
    match = None
    while round == 1 or match is not None:
        print("Creating table for round {}...".format(round))
        match, result_table = _generate_for_team_and_round(team, round, nrw_club_zps_dict)
        if match is None:
            print("Round {} data is not valid. Continue with next team.".format(round))
            return
        file.write("Round " + str(round) + ":\n") 
        file.write(strip_multiline_text(result_table))
        file.write("\n\n")
        round += 1

def _generate_for_team_and_round(team: TeamConfig, round: int, nrw_club_zps_dict: dict[str, int]) -> tuple[Match, str]:
    url = team.base_url + "&rd=" + str(round)
    match = mp.parse_match_from_url(url, team.key, nrw_club_zps_dict)
    if match is None:
        return None, None
    result_table = rtb.build_result_table(match, team.key)
    return match, result_table

main()