import re

import pandas as pd
import praw
import requests
from bs4 import BeautifulSoup

import bbref_helper

TEAM_ABBREVIATION = 'SAS'
TEAM_SUBREDDIT = 'SpursTest'


# Seems redundant with standings table so not used currently...
def get_record(url):
    team_html = requests.get(url).text
    team_info = BeautifulSoup(team_html, 'html.parser').find(id="info")

    # Get only the text containing the team record
    team_record = team_info.find_all("p")[2].text

    # Remove unwanted newlines & tabs, make text a Markdown heading
    team_record = re.sub('\\s+', ' ', team_record)
    team_record = '#' + team_record.strip() + '\n\n'
    return team_record


def get_roster(url):
    roster = pd.read_html(url)[0]

    # Due to width of reddit sidebars, only want number, name, and position
    # (the first 3 columns)
    roster = roster.iloc[:, :3]

    # Players without numbers probably don't need to be included
    # (two-way players who have never gotten minutes, etc.)
    roster = roster.dropna()

    roster = roster.set_index('No.')
    roster = roster.to_markdown()
    roster = "\n\n|ROSTER|\n|:--:|\n\n" + roster
    return roster


def get_standings(url):
    eastern_conference = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DET',
                          'IND', 'MIA', 'MIL', 'NYK', 'ORL', 'PHI', 'TOR',
                          'WAS']

    western_conference = ['DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL', 'MEM',
                          'MIN', 'NOP', 'OKC', 'PHO', 'POR', 'SAC', 'SAS',
                          'UTA']

    if TEAM_ABBREVIATION in eastern_conference:
        standings = pd.read_html(url)[0]
    elif TEAM_ABBREVIATION in western_conference:
        standings = pd.read_html(url)[1]
    else:
        return "ERROR: get_standings() TEAM_ABBREVIATION"

    # Drop unneeded columns (mostly due to sidebar width)
    standings.drop(['W/L%', 'PS/G', 'PA/G', 'SRS'], axis=1, inplace=True)

    standings.columns = ['Team', 'W', 'L', 'GB']
    standings.index += 1
    standings.index.name = 'Seed'

    # Having the seed in parentheses is redundant, just use index
    # It makes more sense to have seed to the left of the team name anyway
    standings['Team'] = [re.sub(r'\([^)]*\)', '',
                                str(x)) for x in standings['Team']]

    standings = standings.to_markdown()
    standings = "\n\n|STANDINGS|\n|:--:|\n\n" + standings
    return standings


def get_schedule(url):
    schedule = pd.read_html(url)[0]
    # [0] Game; [1] Date; [2] Start (ET); [3] BLANK; [4] Box Score Link; [5] @;
    # [6] Opponent; [7] W/L; [8] OT; [9] Team Score; [10] Opponent Score;
    # [11] Win counter; [12] Loss counter; [13] Streak; [14] Notes

    # Table repeats the headings every 20 games
    schedule.drop([20, 41, 62, 83], inplace=True)

    index = bbref_helper.get_game_index(schedule)
    schedule = schedule.iloc[index:index+10]

    # FIRST COLUMN: Full date and start time
    schedule.iloc[:, 1] = schedule.iloc[:, 1].str[:-6]
    schedule['Date'] = schedule['Date'].apply(bbref_helper.to_ordinal)
    schedule.iloc[:, 1] = schedule.iloc[:, 1] + '; ' + schedule.iloc[:, 2] + 'm'

    # SECOND COLUMN: Team (vs. OR @) Opponent
    schedule.iloc[:, 5].fillna('vs.', inplace=True)
    schedule.iloc[:, 2] = schedule.iloc[:, 5] + ' ' + schedule.iloc[:, 6]

    # THIRD COLUMN: Team score - Opponent score -- W/L
    schedule.iloc[:, 3] = schedule.iloc[:, 9] + ' - ' + schedule.iloc[:, 10] + \
        ' ' + '**' + schedule.iloc[:, 7] + '**'
    schedule = schedule.fillna("")

    # Columns are prepared - drop the rest and make it Reddit-ready
    schedule.drop(schedule.columns[[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]],
                  axis=1, inplace=True)
    schedule.columns = ['G', 'Date & Time (ET)', 'Opponent', 'Score']
    schedule = schedule.to_markdown(index=False)
    schedule = "\n\n|SCHEDULE|\n|:--:|\n\n" + schedule
    return schedule


def update_sidebar(new_content):
    reddit = praw.Reddit("Spurs Bot", user_agent="r/NBASpurs Bot")
    subreddit = reddit.subreddit(TEAM_SUBREDDIT)

    old_sidebar = subreddit.wiki["config/sidebar"]
    old_sidebar.edit(content=new_content)

    widgets = subreddit.widgets.sidebar
    new_styles = {"backgroundColor": "#FFFFFF", "headerColor": "#FF9900"}
    widgets[0] = widgets[0].mod.update(text=new_content, styles=new_styles)
