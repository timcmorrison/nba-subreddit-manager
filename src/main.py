import praw

import bbref
import bbref_helper

TEAM_ABBREVIATION = 'SAS'
TEAM_SUBREDDIT = 'SpursTest'


def main():
    year = bbref_helper.get_year()
    base_url = 'https://www.basketball-reference.com/'

    team_url = base_url +'teams/' + TEAM_ABBREVIATION + '/' + year + '.html'
    standings_url = base_url + 'leagues/NBA_' + year + '_standings.html'
    schedule_url = team_url.replace('.html', '_games.html')

    roster = bbref.get_roster(team_url)
    standings = bbref.get_standings(standings_url)
    schedule = bbref.get_schedule(schedule_url)
    bbref.update_sidebar(schedule + standings + roster)


def update_sidebar(new_content):
    reddit = praw.Reddit("Spurs Bot", user_agent="r/NBASpurs Bot")
    subreddit = reddit.subreddit(TEAM_SUBREDDIT)

    old_sidebar = subreddit.wiki["config/sidebar"]
    old_sidebar.edit(content=new_content)

    widgets = subreddit.widgets.sidebar
    new_styles = {"backgroundColor": "#FFFFFF", "headerColor": "#FF9900"}
    widgets[0] = widgets[0].mod.update(text=new_content, styles=new_styles)


if __name__ == "__main__":
    main()