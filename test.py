import re
from datetime import datetime

import pandas as pd
import praw
import requests
from bs4 import BeautifulSoup

TEAM_ABBREVIATION = 'SAS'
TEAM_SUBREDDIT = 'SpursTest'
TEAM_NAME = 'San Antonio Spurs'

url = "https://www.basketball-reference.com/teams/SAS/2023.html"
team_html = requests.get(url).text
team_info = BeautifulSoup(team_html, 'html.parser').find(id="info")

# Get only the text containing the team record
team_record = team_info.find_all("p")[2].text
print(team_record)