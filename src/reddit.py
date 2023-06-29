"""Reddit utilities"""
    
import pandas as pd
import praw

TEAM_SUBREDDIT = 'SpursTest'

    
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


def update_sidebar(new_content):
    """Updates the sidebar.
    
    :param str new_content: Sidebar text.
    """
    reddit = praw.Reddit("Spurs Bot", user_agent="r/NBASpurs Bot")
    subreddit = reddit.subreddit(TEAM_SUBREDDIT)

    old_sidebar = subreddit.wiki["config/sidebar"]
    old_sidebar.edit(content=new_content)

    widgets = subreddit.widgets.sidebar
    new_styles = {"backgroundColor": "#FFFFFF", "headerColor": "#FF9900"}
    widgets[0] = widgets[0].mod.update(text=new_content, styles=new_styles)