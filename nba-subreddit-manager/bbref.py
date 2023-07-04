"""Basketball-Reference utilities"""

import re
import sys
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_record(team):
    """Returns the team's record.

    :param str team: The team abbreviation.
    """

    url = get_team_url(team)
    team_html = requests.get(url).text
    team_info = BeautifulSoup(team_html, 'html.parser').find(id="info")
    team_record = team_info.find_all("p")[2].text
    team_record = remove_whitespace(team_record)
    return team_record


def get_roster(team):
    """Returns the team's roster.
    
    :param str team: The team abbreviation.
    """

    url = get_team_url(team)
    roster = get_html(url, 0)
    # Only want number, name, and position (the first 3 columns) so it fits
    # in sidebar.
    roster = roster.iloc[:, :3]
    roster = roster.set_index('No.')
    return roster


def get_standings(conference):
    """Returns standings of team's conference.

    :param str conference: The team conference.
    """

    url = get_standings_url()
    if conference == "east":
        standings = get_html(url, 0)
    elif conference == "west":
        standings = get_html(url, 1)
    else:
        sys.exit("get_standings(): Unrecognized conference: \'" + conference 
                 + "\'")
    # Drop unneeded columns (mostly due to sidebar width).
    standings = standings.drop(['W/L%', 'PS/G', 'PA/G', 'SRS'], axis=1)
    standings.columns = ['Team', 'W', 'L', 'GB']
    standings.index += 1
    standings.index.name = 'Seed'

    # Having the seed in parentheses is redundant, just use index.
    # It makes more sense to have seed to the left of the team name anyway.
    standings['Team'] = [re.sub(r'\([^)]*\)', '',
                                str(x)) for x in standings['Team']]
    return standings


def get_schedule(team):
    """ Returns the team's schedule.

    :param str team: The team abbreviation.
    """

    url = get_schedule_url(team)
    schedule = get_html(url, 0)
    # The schedule DataFrame columns are as follows:
    # [0] Game
    # [1] Date
    # [2] Start (ET)
    # [3] BLANK
    # [4] Box Score Link
    # [5] @
    # [6] Opponent
    # [7] W/L
    # [8] OT
    # [9] Team Score
    # [10] Opponent Score
    # [11] Win counter
    # [12] Loss counter
    # [13] Streak
    # [14] Notes

    # Table repeats the headings every 20 games, so get rid of those headings.
    schedule = schedule.drop([20, 41, 62, 83])
    schedule = schedule.reset_index(drop=True)
    index = get_game_index(schedule)
    schedule = schedule.iloc[index:index+10]
    # Now create the columns for the schedule table.
    # 1st column: Full date and start time.
    schedule.iloc[:, 1] = schedule.iloc[:, 1].str[:-6]
    schedule['Date'] = schedule['Date'].apply(to_ordinal)
    schedule.iloc[:, 1] = schedule.iloc[:, 1] + '; ' + schedule.iloc[:, 2] + 'm'
    # 2nd column: Team (vs. OR @) Opponent.
    schedule.iloc[:, 5] = schedule.iloc[:, 5].fillna('vs.')
    schedule.iloc[:, 2] = schedule.iloc[:, 5] + ' ' + schedule.iloc[:, 6]
    # 3rd column: Team score - Opponent score -- W/L.
    schedule.iloc[:, 3] = schedule.iloc[:, 9] + ' - ' + schedule.iloc[:, 10] + \
        ' ' + '**' + schedule.iloc[:, 7] + '**'
    schedule = schedule.fillna("")
    # Columns are prepared - drop the rest and make it Reddit-ready.
    schedule = schedule.drop(
        schedule.columns[[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]],
        axis=1)
    schedule.columns = ['G', 'Date & Time (ET)', 'Opponent', 'Score']
    schedule = schedule.set_index('G')
    return schedule


def get_year():
    """Returns the current season year."""

    # Season year will either be current year or next year, e.g. the 2013-2014
    # season should return 2014. So try next year first, and if that page
    # can't be found, use the current year instead.
    year = datetime.today().year + 1
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + \
        '.html'
    if check_404(url):
        year = year - 1
    return year


def to_ordinal(date):
    """Returns the ordinal representation of the date.

    :param str date: The date to be converted.
    
    E.g. Janurary 1 -> January 1st.
    """
    day = int(date[-2:])
    ones_place = int(date[-1:])

    if 10 < day < 20:
        return date + 'th'
    
    if ones_place == 1:
        return date + 'st'
    elif ones_place == 2:
        return date + 'nd'
    elif ones_place == 3:
        return date + 'rd'
    else:
        return date + 'th'


def get_game_index(schedule):
    """Returns the index for the first game to be displayed on the schedule.
    
    :param DataFrame schedule: The schedule.

    Generally, we want to show the previous 5 games and their result, as well as
    the next 5 upcoming games.
    
    If at the beginning of the season, (i.e., there aren't 5 previous games)
    display the first 10 games.
    
    If at the end of the season, (i.e., there aren't 5 upcoming games) display
    the last 10 games.
    """

    nan_values = schedule[schedule['Tm'].isna()]
    if nan_values.empty:
        return 72
    index = nan_values.index[0] - 5
    if index <= 0:
        return 0
    if index >= 72:
        return 72
    return index


def remove_whitespace(string):
    """Returns a string with excess whitespace removed.
    
    :param str string: The string.
    
    Words are still separated by a single space, but leading and trailing
    whitespace is removed, as are any other spaces, tabs, and newlines.
    """
    string = re.sub('\\s+', ' ', string)
    return string.strip()


def get_team_url(team):
    """Returns the URL to the team's page.
    
    param str team: Team abbreviation.
    """

    base = 'https://www.basketball-reference.com/'
    return base + 'teams/' + team + '/' + str(get_year()) + '.html'


def get_standings_url():
    """Returns the URL to the NBA standings page."""

    base = 'https://www.basketball-reference.com/'
    return base + 'leagues/NBA_' + str(get_year()) + '_standings.html'


def get_schedule_url(team):
    """Returns the URL to the team's schedule page.
    
    param str team: Team abbreviation.
    """

    base = 'https://www.basketball-reference.com/'
    return base + 'teams/' + team + '/' + str(get_year()) + '_games.html'


def get_html(url, index):
    """ Reads the html from url and makes sure the page can be found.

    :param str url: URL of page to be read.

    :param int index: HTML table index.
    """

    html = pd.read_html(url)[index]
    if check_404(url):
        sys.exit("get_html(): \'" + url + "\' can't be found")
    return html


def check_404(url):
    """Returns True if page returns status code 404, False if not.
    
    :param str url: Page URL.
    """

    return requests.get(url).status_code == 404