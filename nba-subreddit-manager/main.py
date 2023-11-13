"""NBA team subreddit manager"""

import os
from pathlib import Path

import nba
import reddit
import yaml


def main():
    """Update the subreddit."""

    dir = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    config_path = str(Path(dir).parents[0]) + "/config.yml"
    config = yaml.safe_load(open(config_path))
    team_name = config['team']
    team = nba.Team(team_name)
    reddit.update_sidebar(config, team)


if __name__ == "__main__":
    main()