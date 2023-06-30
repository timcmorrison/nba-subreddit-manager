"""Reddit utilities"""
    
import sys

import bbref
import praw


def to_heading(heading, level):
    """Returns the string as a Markdown heading.
    
    :param str heading: String to become section heading.

    :param int level: The level of heading.
    """

    if 1 <= level <= 6:
        heading = ' ' + heading
        for i in range(1, level):
            heading = '#' + heading
    return heading + '\n\n'


def create_table(df, table_heading):
    """Converts DataFrame to Markdown table.

    :param DataFrame df: The DataFrame.

    :param str table_heading: Table heading.
    """
    df = df.to_markdown()
    return '\n\n|' + table_heading + '|\n|:--:|\n\n' + df


def update_sidebar(subreddit_name, team):
    """Updates the sidebar.
    
    :param str subreddit_name: Subreddit to update.

    :param Team team: NBA team to update sidebar with.
    """

    reddit = praw.Reddit("Spurs Bot", user_agent="r/NBASpurs Bot")
    subreddit = reddit.subreddit(subreddit_name)

    try:
        update_old_reddit(subreddit, team)
        update_new_reddit(subreddit, team)
    except:
        sys.exit("Can't update subreddit: \'" + subreddit_name + "\'.\n" + \
                 "Make sure it is spelled correctly, you have access, and" + \
                 " your praw.ini is configured correctly.")


def update_old_reddit(subreddit, team):
    """Updates the old layout, old.reddit.com.
    
    :param Subreddit subreddit: Subreddit to update.

    :param Team team: NBA team to update sidebar with.
    """

    roster_df = bbref.get_roster(team.abbreviation)
    standings_df = bbref.get_standings(team.conference)
    schedule_df = bbref.get_schedule(team.abbreviation)
    roster = make_old_roster(roster_df)
    standings = make_old_standings(standings_df)
    schedule = make_old_schedule(schedule_df)    
    old_sidebar = subreddit.wiki["config/sidebar"]
    old_sidebar.edit(content=schedule+standings+roster)


def update_new_reddit(subreddit, team):
    """Updates redesigned layout, new.reddit.com.
    
    :param Subreddit subreddit: Subreddit to update.

    :param Team team: NBA team to update sidebar with.
    """

    widgets = subreddit.widgets.sidebar
    new_styles = {"backgroundColor": "#FFFFFF", "headerColor": "#FF9900"}
    widgets[0] = widgets[0].mod.update(text="PLACEHOLDER", styles=new_styles)   


def make_old_roster(roster):
    """Returns the roster table formatted for old reddit

    :param DataFrame roster: roster.
    """

    roster = create_table(roster, "ROSTER")
    # Players without numbers will have "nan". Trying to handle it with pandas 
    # introduced other issues, this ended up being easier.
    roster = roster.replace("nan", "")
    return roster


def make_old_standings(standings):
    """Returns the standings table formatted for old reddit

    :param DataFrame standings: standings.
    """

    return create_table(standings, "STANDINGS")


def make_old_schedule(schedule):
    """Returns the schedule table formatted for old reddit

    :param DataFrame schedule: schedule.
    """

    return create_table(schedule, "SCHEDULE")