"""NBA team subreddit manager"""

import bbref
import nba
import reddit


def main():
    """Update the subreddit."""

    team = nba.Team("Spurs")
    reddit.update_sidebar("SpursTest", team)


if __name__ == "__main__":
    main()