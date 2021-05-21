import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time

#test

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

#function that takes a team and either a season_ID or year as an input and returns the team's roster from that year
def getRoster(team, season_ID = -1, year = -1):
	#TODO
	print('')


#tests
df = getTeams(team_names = ['University of Pittsburgh', 'University of Louisville'])
print(df.head())

df1 = getTeams(conference_names = ['ACC', 'Ivy'])
print(df1)

df2 = getTeams(division_names = ['Division 1'])
print(df2.head())
