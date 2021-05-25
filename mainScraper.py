import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time

teams = pd.read_csv('https://raw.githubusercontent.com/maflancer/CollegeSwimmingScraper/main/collegeSwimmingTeams.csv')

#HELPER FUNCTIONS -------------------------------------

#changes name from (last, first) to (first last)
def cleanName(webName):
	nameList = webName.split(', ')
	last_name = nameList[0]
	first_name = nameList[1]

	return first_name + ' ' +  last_name

#extracts swimmer id from href
def getSwimmerID(href):
	return href.split('/')[-1]

#gets corresponding team number for a specified team
def getTeamNumber(team_name):
	team_number = -1

	#search for the specified team
	for index, row in teams.iterrows():
		if row['team_name'] == team_name:
			team_number = row['team_ID']
	return team_number

#gets corresponding season ID for a specified year
def getSeasonID(year):
	return year - 1996

#extracts state or country from hometown
def getState(hometown):
	home = hometown.split(',')[-1].strip()
	if(home.isalpha()):
		return home
	else:
		return 'NONE'

#extracts city from hometown
def getCity(hometown):
	home = hometown.split(',')
	home.pop() #removes state or country to isolate the city

	city = ' '.join([c.strip() for c in home])

	return city

#SCRAPING FUNCTIONS ------------------------------------

#function that takes as an input team names, a division, or a conference and returns the teams that match the input
#example function call - getTeams(conference = "ACC") - returns a list with all teams in the ACC conference
def getTeams(team_names = ['NONE'], division_names = ['NONE'], conference_names = ['NONE']):
	team_df = pd.DataFrame()
	if(team_names != ['NONE']):
		team_df = teams[teams['team_name'].isin(team_names)].reset_index(drop = True)
	elif(division_names != ['NONE']):
		team_df = teams[teams['team_division'].isin(division_names)].reset_index(drop = True)
	elif(conference_names != ['NONE']):
		team_df = teams[teams['team_conference'].isin(conference_names)].reset_index(drop = True)
	else:
		team_df = teams

	return team_df

#given a swimmer's ID, return their high school power index -> this is an index used for recruiting
def getPowerIndex(swimmer_ID):
	swimmer_url = 'https://swimcloud.com/swimmer/' + str(swimmer_ID)

	url = requests.get(swimmer_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	data_array = soup.find_all('a', {'class' : 'c-list-bar__description'}) #this gets an array of 4 data points for the swimmer -> team, power_index, state rank, yearly rank

	try:
		return data_array[1].text.strip() #second data point in the array is the swimmer's power index
	except IndexError:
		return -1

#function that takes a team and gender, and either a season_ID or year as an input and returns the team's roster from that year
#example function call - getRoster(team = "University of Pittsburgh", gender = "M") - if no season or year -> returns roster for current season - season #24
#                      - getRoster(team = "University of Pittsburgh", gender = "F", year = 2020) - roster for 2020-2021 team corresponds to season #24
def getRoster(team, gender, season_ID = -1, year = -1):
	roster = list()

	team_number = getTeamNumber(team)

	if(year != -1):
		season_ID = getSeasonID(year)

	#if no season_ID or year is specified, return the roster for the most current season - might change later
	if(season_ID == -1 and year == -1):
		season_ID = 24

	roster_url = 'https://www.swimcloud.com/team/' + str(team_number) +  '/roster/?page=1&gender=' + gender + '&season_id=' + str(season_ID)

	url = requests.get(roster_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:] #finds table of player names

	for row in data:
		swimmer_name = cleanName(row.find('a').text.strip())
		idArray = row.find_all('a')  #returns array of length 1 which contains swimmer ID
		swimmer_ID = getSwimmerID(idArray[0]['href'])
		numbers = row.find_all('td')
		state = getState(numbers[2].text.strip())
		city = getCity(numbers[2].text.strip())
		grade = numbers[3].text.strip()
		HS_power_index = getPowerIndex(swimmer_ID)

		roster.append({'swimmer_name': swimmer_name, 'swimmer_ID' : swimmer_ID, 'grade' : grade, 'hometown_state': state, 'hometown_city' : city, 'HS_power_index' : HS_power_index})

	return roster


#tests ------------------------------------
df = getTeams(team_names = ['University of Pittsburgh', 'University of Louisville'])
print(df.head())

df1 = getTeams(conference_names = ['ACC', 'Ivy'])
print(df1)

df2 = getTeams(division_names = ['Division 1'])
print(df2.head())

penn_roster = getRoster(team = "University of Pennsylvania", gender = "M")
pitt_roster = getRoster(team = "University of Pittsburgh", gender = "F", year = 2015)

print(penn_roster)
print(pitt_roster)
