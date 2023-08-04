"""NBA team information"""

import sys

import bbref


class Team:
    def __init__(self, team_name):
        """Creates a new Team object.

        :param str team_name: Team name.
        """

        self.name = check_name(team_name)
        self.abbreviation = get_abbreviation(self.name)
        self.conference = get_conference(self.name)
        self.roster = bbref.get_roster(self.abbreviation)
        self.standings = bbref.get_standings(self.conference)
        self.schedule = bbref.get_schedule(self.abbreviation)


def check_name(name):
    """Checks that the team name is valid, and if so, returns it
    
    :param str name: Team name.
    """

    # Handle any capitalization, e.g. sPuRs -> Spurs
    name = name.capitalize()
    team_names = {"Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavaliers", 
                  "Pistons", "Pacers", "Heat", "Bucks", "Knicks", "Magic", 
                  "76ers", "Raptors", "Wizards", "Mavericks", "Nuggets", 
                  "Warriors", "Rockets", "Clippers", "Lakers", "Grizzlies", 
                  "Timberwolves", "Pelicans", "Thunder", "Suns", 
                  "Trail Blazers", "Kings", "Spurs", "Jazz"}
    if name not in team_names:
        sys.exit(f"class Team __init__(): Unrecognized team name: '{name}'")
    return name


def get_abbreviation(team_name):
    """Returns the team's abbreviation.

    :param str team_name: Team name.
    """

    if team_name == "Hawks":
        return 'ATL'
    elif team_name == "Celtics":
        return 'BOS'
    elif team_name == "Nets":
        return 'BRK'
    elif team_name == "Hornets":
        return 'CHO'
    elif team_name == "Bulls":
        return 'CHI'
    elif team_name == "Cavaliers":
        return 'CLE'
    elif team_name == "Pistons":
        return 'DET'
    elif team_name == "Pacers":
        return 'IND'
    elif team_name == "Heat":
        return 'MIA'
    elif team_name == "Bucks":
        return 'MIL'
    elif team_name == "Knicks":
        return 'NYK'
    elif team_name == "Magic":
        return 'ORL'
    elif team_name == "76ers":
        return 'PHI'
    elif team_name == "Raptors":
        return 'TOR'
    elif team_name == "Wizards":
        return 'WAS'
    elif team_name == "Mavericks":
        return 'DAL'
    elif team_name == "Nuggets":
        return 'DEN'
    elif team_name == "Warriors":
        return 'GSW'
    elif team_name == "Rockets":
        return 'HOU'
    elif team_name == "Clippers":
        return 'LAC'
    elif team_name == "Lakers":
        return 'LAL'
    elif team_name == "Grizzlies":
        return 'MEM'
    elif team_name == "Timberwolves":
        return 'MIN'
    elif team_name == "Pelicans":
        return 'NOP'
    elif team_name == "Thunder":
        return 'OKC'
    elif team_name == "Suns":
        return 'PHO'
    elif team_name == "Trail Blazers":
        return 'POR'
    elif team_name == "Kings":
        return 'SAC'
    elif team_name == "Spurs":
        return 'SAS'
    elif team_name == "Jazz":
        return 'UTA'
    else:
        sys.exit(f"get_abbreviation(): Unrecognized team name: '{team_name}'")


def get_conference(team_name):
    """Returns the team's conference
            
    :param str team_name: Team name.
    """
    
    eastern_teams = {"Hawks", "Celtics", "Nets", "Hornets", "Bulls", 
                     "Cavaliers", "Pistons", "Pacers", "Heat", "Bucks", 
                     "Knicks", "Magic", "76ers", "Raptors", "Wizards"}
    western_teams = {"Mavericks", "Nuggets", "Warriors", "Rockets", "Clippers", 
                     "Lakers", "Grizzlies", "Timberwolves", "Pelicans", 
                     "Thunder", "Suns", "Trail Blazers", "Kings", "Spurs", 
                     "Jazz"}
    if team_name in eastern_teams:
        return "east"
    elif team_name in western_teams:
        return "west"
    else:
        sys.exit(f"get_conference(): Unrecognized team name: '{team_name}'")
