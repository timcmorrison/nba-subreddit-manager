"""NBA team information"""

import sys

class Team:
    def __init__(self, name):
        """Creates a new Team object.

        :param str name: Team name.
        """

        self.name = check_name(name)
        self.abbreviation = get_abbreviation(self.name)
        self.conference = get_conference(self.name)


def check_name(name):
    """Checks that the team name is valid, and if so, returns it
    
    :param str name: Team name.
    """

    # Handle any capitalization, e.g. sPuRs -> Spurs
    name = name.capitalize()

    if name not in {"Hawks", "Celtics", "Nets", "Hornets", "Bulls",
                 "Cavaliers", "Pistons", "Pacers", "Heat", "Bucks", "Knicks",
                 "Magic", "76ers", "Raptors", "Wizards", "Mavericks", "Nuggets",
                 "Warriors", "Rockets", "Clippers", "Lakers", "Grizzlies",
                 "Timberwolves", "Pelicans", "Thunder", "Suns", "Trail Blazers",
                 "Kings", "Spurs", "Jazz"}:
            sys.exit("class Team __init__(): Unrecognized team name: \'" +
                    name + "\'")
    return name


def get_abbreviation(name):
    """Returns the team's abbreviation.

    :param str name: Team name.
    """

    if name == "Hawks":
        return 'ATL'
    elif name == "Celtics":
        return 'BOS'
    elif name == "Nets":
        return 'BRK'
    elif name == "Hornets":
        return 'CHO'
    elif name == "Bulls":
        return 'CHI'
    elif name == "Cavaliers":
        return 'CLE'
    elif name == "Pistons":
        return 'DET'
    elif name == "Pacers":
        return 'IND'
    elif name == "Heat":
        return 'MIA'
    elif name == "Bucks":
        return 'MIL'
    elif name == "Knicks":
        return 'NYK'
    elif name == "Magic":
        return 'ORL'
    elif name == "76ers":
        return 'PHI'
    elif name == "Raptors":
        return 'TOR'
    elif name == "Wizards":
        return 'WAS'
    elif name == "Mavericks":
        return 'DAL'
    elif name == "Nuggets":
        return 'DEN'
    elif name == "Warriors":
        return 'GSW'
    elif name == "Rockets":
        return 'HOU'
    elif name == "Clippers":
        return 'LAC'
    elif name == "Lakers":
        return 'LAL'
    elif name == "Grizzlies":
        return 'MEM'
    elif name == "Timberwolves":
        return 'MIN'
    elif name == "Pelicans":
        return 'NOP'
    elif name == "Thunder":
        return 'OKC'
    elif name == "Suns":
        return 'PHO'
    elif name == "Trail Blazers":
        return 'POR'
    elif name == "Kings":
        return 'SAC'
    elif name == "Spurs":
        return 'SAS'
    elif name == "Jazz":
        return 'UTA'
    else:
        sys.exit("get_abbreviation(): Unrecognized team name: \'" + name + 
                 "\'" )


def get_conference(name):
    """Returns the team's conference
            
    :param str name: Team name.
    """
    
    if name in {"Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavaliers",
            "Pistons", "Pacers", "Heat", "Bucks", "Knicks", "Magic", "76ers",
            "Raptors", "Wizards"}:
        return "east"
    
    elif name in {"Mavericks", "Nuggets", "Warriors", "Rockets", "Clippers",
            "Lakers", "Grizzlies", "Timberwolves", "Pelicans", "Thunder",
            "Suns", "Trail Blazers", "Kings", "Spurs", "Jazz"}:
        return "west"
    else:
        sys.exit("get_conference(): Unrecognized team name: \'" + name + "\'")
