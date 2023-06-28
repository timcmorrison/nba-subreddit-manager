"""NBA team subreddit manager"""

import bbref
import reddit

TEAM_ABBREVIATION = 'SAS'


def main():
    """Update the subreddit."""

    year = str(bbref.get_year())
    base_url = 'https://www.basketball-reference.com/'

    team_url = base_url +'teams/' + TEAM_ABBREVIATION + '/' + year + '.html'
    standings_url = base_url + 'leagues/NBA_' + year + '_standings.html'
    schedule_url = team_url.replace('.html', '_games.html')

    roster = bbref.get_roster(team_url)
    standings = bbref.get_standings(standings_url)
    schedule = bbref.get_schedule(schedule_url)
    reddit.update_sidebar(schedule + standings + roster)


if __name__ == "__main__":
    main()