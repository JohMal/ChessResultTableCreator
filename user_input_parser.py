from models import TeamConfig

def get_user_seclection(all_teams: list[TeamConfig]) -> tuple[list[TeamConfig], list[int]]: 
    teams = _get_team_selection(all_teams)
    rounds = _get_round_selection()
    return teams, rounds

def _get_team_selection(all_teams: list[TeamConfig]) -> list[TeamConfig]:
    print("Select Team:")
    print("  (0) All teams")
    for i, team in enumerate(all_teams):
        print("  ({}) {}".format(i+1, team.name))
    while True:
        inp = input()
        if inp.isdecimal():
            team_input = int(inp)
            if team_input == 0:
                return all_teams
            elif team_input in range(1, len(all_teams) + 1):
                return [all_teams[team_input - 1]]
        print("Please select a number beetween 0 and {}.".format(len(all_teams)))

def _get_round_selection() -> list[int]:
    print("Select Round:")
    print("  (0) All rounds")
    for i in range(1, 4):
        print("  ({0}) Round {0}".format(i))
    print("  ...")
    print("  (n) Round n")
    while True:
        inp = input()
        if inp.isdecimal():
            if int(inp) == 0:
                return []
            elif int(inp) >= 0:
                return [int(inp)]
        print("Please select a round number > 0")
        