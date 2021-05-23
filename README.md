# CollegeSwimmingScraper

Python scraper for college swimming data. 

**In progress**

getTeamList.py - scrapes all swimcloud.com/team pages to get list of all college swimming teams - outputs collegeSwimmingTeams.csv

mainScraper.py - 
* getTeams() takes as an input either a list of teams, a list of divisions, or a list of conferences -> based on the inputs, returns a data frame with the specfified teams
* getRoster() takes as an input a team's name, a gender (M or F), and either a season_ID or year -> returns a list of the team's roster for specified season -> includes swimmer_name, swimmer_ID, grade, and hometown information

collegeSwimmingTeams.csv - team_name, team_ID (unique ID used on swimcloud), team_state (location), team_division (e.g., Division 1, Division 2), team_division_ID (unique division ID), team_conference (e.g., ACC, Ivy), team_conference_ID (unique confernce ID)
