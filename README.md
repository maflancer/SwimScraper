# SwimScraper

* Python scraping package for college and professional swimming data -  all data is from https://swimcloud.com. 
* The package can be found on https://pypi.org/project/SwimScraper/.

## Installation
* You can install SwimScraper using pip:
```pip install SwimScraper```
* An example of one way to use the scraping functions:
```
from SwimScraper import SwimScraper as ss

#gets Pitt men roster for 2020
pitt_M_roster_2020 = ss.getRoster(team = 'University of Pittsburgh', team_ID = 405, gender = 'M', year = 2020)

#gets list of all meets that Pitt participated in for 2020
pitt_meetlist_2020 = ss.getTeamMeetList(team_name = 'University of Pittsburgh', team_ID = 405, year = 2020)
```

## Scraping Functions

**Getting Team Data**

* **getCollegeTeams(team_names, conference_names, division_names)** -> returns list of teams where each team has a team_name, team_ID, team_state, team_division, team_division_ID, team_conference, team_conference_ID
  * **Select one of the three inputs:**
  * team_names - ```team_list = ss.getCollegeTeams(team_names = ['University of Pittsburgh', 'University of Louisville'])```
  * conference_names - ```ACC_teams = ss.getCollegeTeams(conference_names = ['ACC'])```
  * division_names - ```d1_teams = ss.getCollegeTeams(division_names = ['Division 1'])```
* **getTeamRankingsList(gender, season_ID, year)** -> returns list of top 50 countries where each team has a team_name, team_ID, and swimcloud_points (score given by swimcloud.com based on team's fastest times)
  * **Select a gender and either a season_ID (e.g., 19 for the 2015-16 season, 24 for the 2020-21 season) or year**
  * season_ID - ```male_rankings_2015 = ss.getTeamRankingsList('M', season_ID = 19)```
  * year - ```female_rankings_2019 = ss.getTeamRankingsList('F', year = 2019)```

**Getting Roster Data**

* **getRoster(team, gender, team_ID, season_ID, year, pro)** -> returns list of swimmers where each swimmer has a swimmer_name, swimmer_ID, team_name, team_ID, grade, hometown_state, hometown_city, HS_power_index (a score given to high school students for recruiting - scale is from 1.00 (best) to 100.00)
  * **Select a gender, a team name or team_ID, a season_ID or year, and set pro = True for non-College teams**
  * team - ```pitt_F_roster_2020 = ss.getRoster(team = 'University of Pittsburgh', gender = 'F', year = 2020)```
  * team_ID - ```boston_college_M_roster_2018 = ss.getRoster(team = '', team_ID = 228, gender = 'M', season_ID = 22)```
  * pro - ```japan_M_roster_2020 = ss.getRoster(team = 'Japan', team_ID = 10008082, gender = 'M', year = 2020, pro = True)```
* **getHSRecruitRankings(class_year, gender, state, state_abbreviation, international)** -> returns list of the top 200 High School recruits from the specified class where each swimmer has a swimmer_name, swimmer_ID, team_name, team_ID, hometown_state, hometown_city, HS_power_index
  * **Select a year, gender, a state or state_abbreviation, and set international = True for international HS students**
  * ```male_recruits_2018 = ss.getHSRecruitRankings(2018, 'M')```
  * state - ```female_recruits_2020_Hawaii = ss.getHSRecruitRankings(2020, 'F', state = 'Hawaii')```
  * state_abbreviation - ```female_recruits_2020_Hawaii = ss.getHSRecruitRankings(2020, 'F', state_abbreviation = 'HI')```

**Getting Swimmer Data**

* **getPowerIndex(swimmer_ID)** -> returns a swimmer's HS recruiting power index
  * ```swimmer_433591_power_index = ss.getPowerIndex(433591)```
* **getSwimmerEvents(swimmer_ID)** -> returns a list of all events that the specified swimmer has participated in
  * ```swimmer_362091_event_list = ss.getSwimmerEvents(362091)``` 
* **getSwimmerTimes(swimmer_ID,  event_name, event_ID)** -> returns a list of all of the swimmer's times in the specified event where each time has a swimmer_ID, pool_type, event, event_ID, time, meet_name, year, date, improvement (improvement from last time)
  * event_name - ```swimmer_257824_50free_times = ss.getSwimmerTimes(257824, '50 Free')```
  * event_ID - ```swimmer_257824_50free_times = ss.getSwimmerTimes(257824, '', event_ID = 150)```

**Getting Meet Data**

* **getTeamMeetList(team_name, team_ID, season_ID, year)** -> returns a list of all the meets the team has competed in for the specififed season or year where each meet has a team_ID, meet_ID, meet_name, meet_date, meet_location
  * ```pitt_2019_meet_list = ss.getTeamMeetList(team_name = 'University of Pittsburgh', year = 2019)```
  * ```USA_2019_meet_list = ss.getTeamMeetList(team_name = '', team_ID = 10008158, season_ID = 23)```
* **getMeetEventList(meet_ID)** -> returns a list of which events took place at the specified meet where each event has an event_name, event_ID and an event_href which can be used as an input in the following functions that get meet results
  * ```olympics_2012_event_list = ss.getMeetEventList(196380)``` 
* **getCollegeMeetResults(meet_ID, event_name, gender, event_ID, event_href)** -> returns a list of all times for the specified event where each time has a meet_ID, swimmer_name, swimmer_ID, team_name, team_ID, event_name, event_ID, event_type (prelims, finals,...), time, score, and improvement
  * event_name - ```pitt_army_100free_results = ss.getCollegeMeetResults(190690,'100 Free', 'F')```
  * event_ID - ```pitt_army_100free_results = ss.getCollegeMeetResults(190690, '', 'F', event_ID = 1100)```
  * event_href (from getMeetEventList) - ```pitt_army_100free_results = ss.getCollegeMeetResults(190690, '', 'F', event_href = '/results/190690/event/17/')```
* **getProMeetResults(meet_ID, event_name, gender, event_ID, event_href)** -> returns a list of all times for the specified event where each time has a meet_ID, swimmer_name, swimmer_ID, team_name, team_ID, event_name, event_ID, event_type (prelims, finals,...), time, FINA_score, and improvement
  * ```olympics2016_200free_male_times = ss.getProMeetResults(106117, event_name = '200 Free', gender = 'M')```
  * ```olympics2016_400medleyrelay_women_times = ss.getProMeetResults(106117, event_name = '', gender = 'F', event_ID = 7400)```
  * ```olympics2012_50free_women_times = ss.getProMeetResults(196380, event_name = '', gender = 'F', event_href = '/results/196380/event/1/')```


## Other Helper Functions

* **getTeamID(team_name)** - gets corresponding team_ID for the specified team   ***currently only for college teams**
* **getTeamName(team_ID)** - gets team_name for the specified team_ID   ***currently only for college teams**
* **getSeasonID(year)** - gets season ID for a specified year
* **getYear(season_ID)** - gets year for a specified season_ID
* **getEventID(event_name)** - gets event_ID for a specified event_name
* **getEventName(event_ID)** - gets event_name for a specified event_ID
* **convertTime(display_time)** - converts a time of the format minutes:seconds (1:53.8) to seconds (113.8)


