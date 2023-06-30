"""NBA team subreddit manager"""

import sys

import nba
import reddit


def main():
    """Update the subreddit."""

    subreddit = sys.argv[1]
    team_name = sys.argv[2]
    team = nba.Team(team_name)
    reddit.update_sidebar(subreddit, team)


if __name__ == "__main__":
    main()