import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time

teams = pd.read_csv('https://raw.githubusercontent.com/maflancer/CollegeSwimmingScraper/main/collegeSwimmingTeams.csv')

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

#changes name from (last, first) to (first last)
def cleanName(webName):
	nameList = webName.split(', ')
	last_name = nameList[0]
	first_name = nameList[1]

	return first_name + ' ' +  last_name

#extracts swimmer id from href
def getSwimmerID(href):
	return href.split('/')[-1]

#function that takes a team and gender, and either a season_ID or year as an input and returns the team's roster from that year
#example function call - getRoster(team = "University of Pittsburgh", gender = "M") - if no season or year -> returns one dataframe with roster for each season from 2010 - 2021
#                      - getRoster(team = "University of Pittsburgh", gender = "F", year = 2020) - roster for 2020-2021 team corresponds to season #24
def getRoster(team, gender, season_ID = -1, year = -1):
	team_row = teams[teams['team_name'] == team]

	#team_number = (team_row['team_ID'].str.split())[1]

	#print(team_number)

	roster_url = 'https://www.swimcloud.com/team/' + str(405) +  '/roster/?page=1&gender=' + gender + '&season_id=' + str(24)

	url = requests.get(roster_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:] #finds table of player names

	for row in data:
		print(cleanName(row.find('a').text.strip()))
		idArray = row.find_all('a') 				 #returns array of length 1 which contains swimmer ID
		swimmer_id = getSwimmerID(idArray[0]['href'])
		numbers = row.find_all('td')
		grade = numbers[3].text.strip()

		print(swimmer_id)
		print(grade)


#tests
#df = getTeams(team_names = ['University of Pittsburgh', 'University of Louisville'])
#print(df.head())

#df1 = getTeams(conference_names = ['ACC', 'Ivy'])
#print(df1)

#df2 = getTeams(division_names = ['Division 1'])
#print(df2.head())

getRoster(team = "University of Pittsburgh", gender = "M", year = 2020)
