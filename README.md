# CollegeSwimmingScraper

Python scraper for college swimming data. - all data is from Swimcloud.com

**In progress**

getTeamList.py - scrapes all swimcloud.com/team pages to get list of all college swimming teams - outputs collegeSwimmingTeams.csv

mainScraper.py - 
* **getTeams(team_names, division_names, conference_names)** takes as an input either a list of teams, a list of divisions, or a list of conferences -> based on the inputs, returns a data frame with the specfified teams.
* **getRoster(team, gender, season_ID, year)** takes as an input a team's name, a gender (M or F), and either a season_ID or year -> returns a list of the team's roster for specified season -> includes swimmer_name, swimmer_ID, grade, and hometown information.
* **getPowerIndex(swimmer_ID)** takes as an input a swimmer's ID # and returns their high school power index which is an index used for recruiting - the scale is from 1-100 with 1 being the best power index and 100 being the worst.
* **getSwimmerTimes(swimmer_ID,  event_name)** takes as an input a swimmer's ID # and an event name and returns a list of all of the swimmer's times in the specified event.
* **getSwimmerEvents(swimmer_ID)** takes as an input a swimmer's ID # and returns a list of all of the event names that the swimmer has participated in.
* **getTeamMeetList(team_name, team_ID, season_ID, year)** takes as an input either a team's name or ID # and returns a list of all the meets the team has competed in for the specififed season or year.
* **getMeetEventList(meet_ID)** takes as an input a meet_ID and returns a list of which events took place at the specified meet
* **getCollegeMeetResults(meet_ID, event_name, gender)** used for college meets - takes as an input a meet id# and an event name and gender and returns a list of all times for the specified event.
* **getProMeetResults(meet_ID, event_name, gender)** used for professional meets - takes as an input a meet id# and an event name and gender and returns a list of all times for the specified event. This function is specifically set up to scrape the US olympic team trials meets
* **getHSRecruitRankings(year, gender, state, state_abbreviation, international)** takes as an input a year and gender and optionally a state or state_abbreviation and returns the top 50 HS recruits from the specified year
* **getMeetSimulator(teams, gender, event_name, year, event_ID)** takes as an input any number of team ID #s, a gender and event_name and optionally a year and event_ID and returns a list of top times in the simulated event

collegeSwimmingTeams.csv - team_name, team_ID (unique ID used on swimcloud), team_state (location), team_division (e.g., Division 1, Division 2), team_division_ID (unique division ID), team_conference (e.g., ACC, Ivy), team_conference_ID (unique confernce ID)
