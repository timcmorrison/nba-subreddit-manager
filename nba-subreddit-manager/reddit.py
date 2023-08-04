"""Reddit utilities"""
    
import sys

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
    return f'\n\n|{table_heading}|\n|:--:|\n\n{df}'


def update_sidebar(config, team):
    """Updates the sidebar.
    
    :param dict config: config.yml.

    :param Team team: NBA team to update sidebar with.
    """

    subreddit_name = config['subreddit']
    calendar_id = config['calendar']
    colors = config['colors']
    reddit = praw.Reddit("Spurs Bot", user_agent="r/NBASpurs Bot")
    subreddit = reddit.subreddit(subreddit_name)

    try:
        update_old_reddit(subreddit, team)
        update_new_reddit(subreddit, team, calendar_id, colors)
    except Exception as e:
        sys.exit("update_sidebar(): " + str(e))


def update_old_reddit(subreddit, team):
    """Updates the old layout, old.reddit.com.
    
    :param Subreddit subreddit: Subreddit to update.

    :param Team team: NBA team to update sidebar with.
    """

    roster = make_old_roster(team.roster)
    standings = make_old_standings(team.standings)
    schedule = make_old_schedule(team.schedule)    
    old_sidebar = subreddit.wiki["config/sidebar"]
    old_sidebar.edit(content=schedule+standings+roster)


def update_new_reddit(subreddit, team, calendar_id, colors):
    """Updates redesigned layout, new.reddit.com.
    
    :param Subreddit subreddit: Subreddit to update.

    :param Team team: NBA team to update sidebar with.

    :param str calendar_id: Google Calendar ID for team schedule.

    :param dict colors: Widget header color hex codes.
    """

    widgets = subreddit.widgets
    sidebar = widgets.sidebar
    schedule_style = {
        "backgroundColor": "#FFFFFF",
        "headerColor": colors['schedule']
    }
    standings_style = {
        "backgroundColor": "#FFFFFF",
        "headerColor": colors['standings']
    }
    roster_style = {
        "backgroundColor": "#FFFFFF",
        "headerColor": colors['roster']
    }
    update_new_schedule(widgets, sidebar, calendar_id, schedule_style)
    update_new_standings(widgets, sidebar, team, standings_style)
    update_new_roster(widgets, sidebar, team, roster_style)


def make_old_roster(roster):
    """Returns the roster table formatted for old reddit

    :param DataFrame roster: Roster.
    """

    roster = create_table(roster, "ROSTER")
    # Players without numbers will have "nan". Trying to handle it with pandas 
    # introduced other issues, this ended up being easier.
    roster = roster.replace("nan", "")
    return roster


def make_old_standings(standings):
    """Returns the standings table formatted for old reddit

    :param DataFrame standings: Standings.
    """

    return create_table(standings, "STANDINGS")


def make_old_schedule(schedule):
    """Returns the schedule table formatted for old reddit

    :param DataFrame schedule: Schedule.
    """

    return create_table(schedule, "SCHEDULE")


def make_new_roster(widgets, style, table):
    """Creates a new widget with the team's roster.
    
    :param SubredditWidgets widgets: Subreddit widgets.

    :param dict style: Widget style. 

    :param str table: Roster Markdown table.
    """

    widgets.mod.add_text_area(short_name="Roster", styles=style, text=table)  


def make_new_standings(widgets, style, table):
    """Creates a new widget with the team's standings.
    
    :param SubredditWidgets widgets: Subreddit widgets.

    :param dict style: Widget style. 

    :param str table: Standings Markdown table.
    """

    widgets.mod.add_text_area(short_name="Standings", styles=style, text=table)    


def make_new_schedule(widgets, style, calendar_id):
    """Creates a new widget with the team's schedule.
    
    :param SubredditWidgets widgets: Subreddit widgets.

    :param dict style: Widget style. 

    :param str calendar_id: Google Calendar ID.
    """

    config = {
        "numEvents": 10,
        "showDate": True,
        "showDescription": True,
        "showLocation": True,
        "showTime": True,
        "showTitle": True,
    }
    widgets.mod.add_calendar(
        short_name="Schedule",
        google_calendar_id=calendar_id,
        requires_sync=True,
        configuration=config,
        styles=style,
    )


def update_new_roster(widgets, sidebar, team, style):
    """Updates roster widget if it exists, else creates one.
    
    :param SubredditWidgets widgets: Subreddit widgets.

    :param list sidebar: Subreddit sidebar.

    :param Team team: NBA team.

    :param dict style: Widget style. 
    """

    roster = find_widget(sidebar, "Roster")
    table = team.roster.to_markdown().replace("nan", "")
    if roster is None:
        make_new_roster(widgets, style, table)
    else:
        roster.mod.update(text=table)
    

def update_new_standings(widgets, sidebar, team, style):
    """Updates standings widget if it exists, else creates one.
    
    :param SubredditWidgets widgets: Subreddit widgets.

    :param list sidebar: Subreddit sidebar.

    :param Team team: NBA team.

    :param dict style: Widget style. 
    """

    standings = find_widget(sidebar, "Standings")
    table = team.standings.to_markdown()
    if standings is None:
        make_new_standings(widgets, style, table)
    else:
        standings.mod.update(text=table)


def update_new_schedule(widgets, sidebar, calendar, style):
    """Updates schedule widget if it exists, else creates one.
    
    :param SubredditWidgets widgets: Subreddit widgets.

    :param list sidebar: Subreddit sidebar.

    :param str calendar: Google Calendar ID.

    :param dict style: Widget style. 
    """

    schedule = find_widget(sidebar, "Schedule")
    if schedule is None:
        make_new_schedule(widgets, style, calendar)


def find_widget(sidebar, short_name):
    """ Returns the first widget with the matching shortName.

    :param list sidebar: Subreddit sidebar.

    :param str short_name: Widget shortName.
    """

    for widget in sidebar:
        if widget.shortName == short_name:
            return widget
    return None
