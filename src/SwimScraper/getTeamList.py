import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time

TEAM_PAGE_RANGE = 32

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

team_list = list()

#function that scrapes the swimcloud.com team list to get all college swimming teams - gets each team's name, ID, state, division, conference
def getTeamList():
	for page in range(1, TEAM_PAGE_RANGE): #this is set to the number of pages on swimcloud.com/team
		team_list_url = 'https://www.swimcloud.com/team/?page=' + str(page)
		
		url = requests.get(team_list_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

		url.encoding = 'utf-8'

		soup = bs(url.text, 'html.parser')

		teams = soup.find_all('div', attrs = {'class' : 'top-box'}) #each top-box corresponds to a single team

		for team in teams:
			team_info = team.find_all('a', attrs = {'class' : 'top-box-title'})[0] #contains the team's id # and the team's name

			team_ID = team_info['href'].split('/')[-1] 
			team_name = team_info.text.splitlines()[3]
			team_state = team.find('div', attrs = {'class' : 'top-box-points'}).text.strip()

			if(team_state in states): #currently only for colleges in the US - the teams from Canada do not have an about page

				team_url = 'https://www.swimcloud.com/team/' + team_ID + '/about/' #page that has division and conference information

				url = requests.get(team_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

				time.sleep(10) #10 second delay between requests

				url.encoding = 'utf-8'

				soup = bs(url.text , 'html.parser')

				#catches Attribute error when ul is not found - cant call find_all on a NoneType Object
				try:
					infoList = soup.find('ul', attrs = {'class' : 'o-list-inline--dotted'}).find_all('li')[:3]   #each li in infoList will hold either a division name or conference name 
				except: 
					infoList = []  #if no ul is found then set infoList to empty


				if(len(infoList) > 1 and 'division' in infoList[0].find('a')['href'] and 'division' in infoList[1].find('a')['href']): #some teams have two divisions listed 
					twoDivisionsListed = True
				else:
					twoDivisionsListed = False


				if(len(infoList) > 0): 
					if(infoList[0].find('a').get('title')):  #if the team has a division listed 
						isDivision = True
					else:
						isDivision = False
				else:
					isDivision = False

				if(len(infoList) > 1 and not twoDivisionsListed): #only one division listed so we only need to set conference
					if(infoList[1].find('a').get('title')):  #if the team has a conference listed 
						isConference = True
					else:
						isConference = False
				elif(len(infoList) > 2 and twoDivisionsListed): #if there are two divisions listed we set the second division and then the conference
					if(infoList[1].find('a').get('title')):  #if a second division is listed
						isDivisonOther = True
					else:
						isDivisonOther = False
					if(infoList[2].find('a').get('title')):
						isConference = True
					else:
						isConference = False
				else:
					isConference = False

				if(isDivision):
					team_division = infoList[0].find('a')['title'].strip()
					team_division_ID = infoList[0].find('a')['href'].split('/')[-2]    #sets division and division_ID
				else:
					team_division = 'NONE'
					team_division_ID = 'NONE'

				if(twoDivisionsListed):
					if(isDivisonOther):
						team_division_other = infoList[1].find('a')['title'].strip()
						team_division_other_ID = infoList[1].find('a')['href'].split('/')[-2]    #sets second division and second division's ID
					else:
						team_division_other = 'NONE'
						team_division_other_ID = 'NONE'
					if(isConference):
						team_conference = infoList[2].find('a')['title'].strip()
						team_conference_ID = infoList[2].find('a')['href'].split('/')[-2]   #sets conference and conference ID
					else:
						team_conference = 'NONE'
						team_conference_ID = 'NONE'
				else: #only one division is listed so we only need to set conference
					if(isConference):
						team_conference = infoList[1].find('a')['title'].strip()
						team_conference_ID = infoList[1].find('a')['href'].split('/')[-2]
					else:
						team_conference = 'NONE'
						team_conference_ID = 'NONE'

					team_division_other = 'NONE'
					team_division_other_ID = 'NONE'

				team_list.append({'team_ID' : team_ID, 'team_name' : team_name, 'team_state' : team_state, 'team_division' : team_division, 'team_division_ID' : team_division_ID, 'team_division_other' : team_division_other, 'team_division_other_ID' : team_division_other_ID, 'team_conference' : team_conference, 'team_conference_ID' : team_conference_ID})

			else: #team is not in the US so set division and conference data to INTERNATIONAL
				team_list.append({'team_ID' : team_ID, 'team_name' : team_name, 'team_state' : team_state, 'team_division' : 'INTERNATIONAL', 'team_division_ID' : 'INTERNATIONAL', 'team_division_other' : 'INTERNATIONAL', 'team_division_other_ID' : 'INTERNATIONAL', 'team_conference' : 'INTERNATIONAL', 'team_conference_ID' : 'INTERNATIONAL'})



def teamListToCSV():
	file_name = 'collegeSwimmingTeams.csv'

	file = open(file_name,'w', newline = '', encoding ='utf-8')  
	
	writer = csv.writer(file)

	#writer.writerow(['team_name','team_ID','team_state','team_division','team_division_ID','team_division_other','team_division_other_ID','team_conference','team_conference_ID'])
	writer.writerow(['team_name','team_ID','team_state','team_division','team_division_ID','team_conference','team_conference_ID'])


	for i in range(len(team_list)):
		#writer.writerow([team_list[i]['team_name'], team_list[i]['team_ID'], team_list[i]['team_state'], team_list[i]['team_division'], team_list[i]['team_division_ID'], team_list[i]['team_division_other'], team_list[i]['team_division_other_ID'], team_list[i]['team_conference'], team_list[i]['team_conference_ID']])
		writer.writerow([team_list[i]['team_name'], team_list[i]['team_ID'], team_list[i]['team_state'], team_list[i]['team_division'], team_list[i]['team_division_ID'], team_list[i]['team_conference'], team_list[i]['team_conference_ID']])
	file.close()



#MAIN FUNCTION -----------------------
getTeamList()
teamListToCSV()