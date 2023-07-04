"""NBA team subreddit manager"""

import yaml

import nba
import reddit


def main():
    """Update the subreddit."""

    config = yaml.safe_load(open("config.yml"))
    team_name = config['team']
    team = nba.Team(team_name)
    reddit.update_sidebar(config, team)


if __name__ == "__main__":
    main()