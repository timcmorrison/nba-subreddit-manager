# NBA Team Subreddit Manager

<img src="https://styles.redditmedia.com/t5_2qo4s/styles/communityIcon_1podsfdai4301.png" alt="NBA Reddit Logo" align="right" width=100>

Automatically update a subreddit's sidebar with useful information about your favorite team. Originally made for [r/NBASpurs](https://reddit.com/r/NBASpurs).

### Current Features
Running ```main.py``` updates the specified subreddit with information about the chosen team. Three Markdown tables are created in the sidebar:
1. Schedule: Previous 5 games as well as the next 5 upcoming games - includes the game number (out of 82), date & time, the opponent, and the score & result if the game has already happened
2. Standings: Standings of the team's conference - includes each team's seed, record, and games behind
3. Roster: Current players on the team - includes their jersey number and position

### To-do
* Automatically run at a specified time
* Containerize
* Work on stylesheet
* Add team logos instead of name
* Add playoff and tank mode
* Make compatible with RES nightmode
* Generate config from Docker and/or Flask web app UI
* Embed new and old reddit pages or show screenshots
* Indicate time of last update and if updated successfully
