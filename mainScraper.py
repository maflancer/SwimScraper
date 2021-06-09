import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time as _time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

teams = pd.read_csv('https://raw.githubusercontent.com/maflancer/CollegeSwimmingScraper/main/collegeSwimmingTeams.csv')
events = {'25 Free' : 125, '25 Back' : 225, '25 Breast' : 325, '25 Fly' : 425, '50 Free' : 150, '75 Free' : 175, '100 Free' : 1100, '125 Free' : 1125, '200 Free' : 1200, '400 Free' : 1400, '500 Free' : 1500, '800 Free' : 1800, '1000 Free' : 11000, '1500 Free' : 11500, '1650 Free' : 11650, '50 Back' : 250, '100 Back': 2100, '200 Back' : 2200, '50 Breast' : 350, '100 Breast' : 3100, '200 Breast' : 3200, '50 Fly' : 450, '100 Fly' : 4100, '200 Fly' : 4200, '100 IM' : 5100, '200 IM' : 5200, '400 IM' : 5400, '200 Free Relay' : 6200, '400 Free Relay' : 6400, '800 Free Relay' : 6800, '200 Medley Relay' : 7200, '400 Medley Relay' : 7400, '1 M Diving' : 'H1', '3 M Diving' : 'H3', 'Platform Diving' : 'H2'}

#HELPER FUNCTIONS -------------------------------------

#changes name from (last, first) to (first last)
def cleanName(webName):
	nameList = webName.split(', ')
	last_name = nameList[0]
	first_name = nameList[1]

	return first_name + ' ' +  last_name

#extracts id from href
def getID(href):
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


#for data from a html table (data), find the indexes where meet name, date, year, and improvement are
#returns an array [meet_name_index, date_index, imp_index]
def getIndexes(data):
	meet_name_index = -1
	date_index = -1
	imp_index = -1
	indexes = []

	i = 0
	for td in data:
		if td.has_attr('class') and td['class'][0] == 'hidden-xs':
			meet_name_index = i
		elif td.has_attr('class') and td['class'][0] == 'u-text-truncate':
			date_index = i
		elif td.has_attr('class') and td['class'][0] == 'u-text-end':
			imp_index = i

		i = i + 1

	indexes.append(meet_name_index)
	indexes.append(date_index)
	indexes.append(imp_index)

	return indexes

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
		swimmer_ID = getID(idArray[0]['href'])
		numbers = row.find_all('td')
		state = getState(numbers[2].text.strip())
		city = getCity(numbers[2].text.strip())
		grade = numbers[3].text.strip()
		HS_power_index = getPowerIndex(swimmer_ID)

		roster.append({'swimmer_name': swimmer_name, 'swimmer_ID' : swimmer_ID, 'grade' : grade, 'hometown_state': state, 'hometown_city' : city, 'HS_power_index' : HS_power_index})

	return roster

#takes as an input a swimmer's ID # and returns a list of each indivudal time for the specified event
def getSwimmerTimes(swimmer_ID, event_name):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('./chromedriver.exe', options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	time_list = list()
	event_ID = events.get(event_name)

	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'
	dropdownCheck = True
	eventCheck = True

	driver.get(swimmer_URL)

	tabs = driver.find_elements_by_css_selector('li.c-tabs__item')

	_time.sleep(1) #makes sure the event tab pops up on website

	for tab in tabs: #finds correct tab on swimmer's profile and clicks on it
		if(tab.text == 'Event'):
			tab.click()

	wait = WebDriverWait(driver, 10, ignored_exceptions = ignored_exceptions)

	try:
		event_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'byEventDropDownList'))) #waits for the event drop down list to show up
		event_dropdown.click()
	except TimeoutException: #if there is no event drop down
		dropdownCheck = False

	if dropdownCheck:

		swimmer_XPATH = '//a[@href="/swimmer/' + str(swimmer_ID)  + '/times/byevent/?event_id=' +  str(event_ID) + '"]'

		#print(swimmer_XPATH) #debug

		try:
			event = wait.until(EC.presence_of_element_located((By.XPATH, swimmer_XPATH)))
			event.click()
		except TimeoutException: #if a swimmer does not have the event listed in the dropdown
			eventCheck = False

		if eventCheck: #if the event is listed

			_time.sleep(1)

			html = driver.page_source

			soup = bs(html, 'html.parser')

			table = soup.find('table', attrs = {'class' : 'c-table-clean'})

			try:
				times = table.find_all('tr')[1:]
			except AttributeError:
				times = []

			for time in times:
				data = time.find_all('td')

				indexes = getIndexes(data) #this function finds the correct indexes for the meet name, date, year, and improvement, as they are different for some swimmers

				time = data[0].text.strip()

				if(indexes[0] == -1): #if no meet name was found
					meet = 'NA'
				else:
					meet = data[indexes[0]].text.strip()

				if(indexes[1] == -1): #if no date was found
					date = 'NA'
					year = 'NA'
				else:
					date = data[indexes[1]].text.strip()
					year = date.split(',')[-1]

				if(indexes[2] == -1): #if no imp was found
					imp = 'NA'
				else:
					imp = data[indexes[2]].text.strip()

				if(imp == '–'): #this character gets encoded weird in an excel doc so just set to NA
					imp = 'NA'

				time_list.append({'Swimmer_ID' : swimmer_ID, 'Event': event_name, 'Time' : time, 'Meet' : meet, 'Year' : year, 'Date' : date, 'Imp' : imp})

	return time_list

#takes as an input a swimmer's ID and returns a list of all events that they have participated in
def getSwimmerEvents(swimmer_ID):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('./chromedriver.exe', options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	events = []
	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'

	driver.get(swimmer_URL)

	tabs = driver.find_elements_by_css_selector('li.c-tabs__item')

	_time.sleep(1) #makes sure the event tab pops up on website

	for tab in tabs: #finds correct tab on swimmer's profile and clicks on it
		if(tab.text == 'Event'):
			tab.click()

	wait = WebDriverWait(driver, 10, ignored_exceptions = ignored_exceptions)

	try:
		event_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'byEventDropDownList'))) #waits for the event drop down list to show up
		event_dropdown.click()

		#find which events the swimmer has participated in
		html = driver.page_source
		soup = bs(html, 'html.parser')
		event_list = soup.find('ul', attrs = {'aria-labelledby' : 'byEventDropDownList'}).find_all('li')

		for event_li in event_list:
			events.append(event_li.text.strip())

	except TimeoutException: #if there are no events found for the swimmer
		return []

	return events

#takes as an input a team_name or team_ID and either a season_ID or year ->   getTeamMeetList('University of Pittsburgh', season_ID = 23)
def getTeamMeetList(team_name = '', team_ID = -1, season_ID = -1, year = -1):
	meet_list = list()

	if(team_name != ''):
		team_number = getTeamNumber(team_name)
	elif(team_ID != -1):
		team_number = team_ID

	if(year != -1):
		season_ID = getSeasonID(year)

	#if no season_ID or year is specified, return the roster for the most current season - might change later
	if(season_ID == -1 and year == -1):
		season_ID = 24

	team_url = 'https://www.swimcloud.com/team/' + str(team_number) +  '/results/?page=1&name=&meettype=&season=' + str(season_ID)

	url = requests.get(team_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	#finds the list of meets which includes meet name, meet ID#
	meets = soup.find('section', attrs = {'class' : 'c-list-grid'}).find_all('a', attrs = {'class' : 'c-list-grid__item'})

	for meet in meets:
		meet_ID = (meet['href']).split('/')[-1] #extracts the meet_ID from the link's href

		meet_name = meet.find('article').find('h3').text.strip()

		meet_date = meet.find('time').text.strip()

		meet_location = (meet.find_all('li')[-1]).text.strip()

		meet_list.append({'meet_ID' : meet_ID, 'meet_name' : meet_name, 'meet_date' : meet_date, 'meet_location' : meet_location})

	return meet_list

#takes as an input a meet's ID # and an event's name and a gender and returns a list of all times for the specified event
def getMeetResults(meet_ID, event_name, gender):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('./chromedriver.exe', options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	results = list()

	if(gender == 'M'):
		full_event_name = event_name + ' Men'
	else:
		full_event_name = event_name + ' Women'

	results_url = 'https://www.swimcloud.com/results/' + str(meet_ID) + '/event/1/'
	event_url = 'none'

	driver.get(results_url)

	html = driver.page_source

	soup = bs(html, 'html.parser')

	#events are numbered starting from 1 so we need to find out the correct event number for the specified event name
	event_list = soup.find('ul', attrs = {'class' : 'c-sticky-filters__list'}).find_all('li')

	for event in event_list:
		web_event_name = event.find('div', attrs = {'class' : 'o-media__body'}).text.strip()
		event_href = event.find('a')['href']

		#check if this event in the list is the event that we want results for
		if(web_event_name == full_event_name):
			event_url = 'https://www.swimcloud.com' + event_href

	#now we have the correct url for the specified event
	driver.get(event_url)

	html = driver.page_source

	soup = bs(html, 'html.parser')

	times_list = soup.find('div', attrs = {'class' : 'c-table-clean--responsive'}).find('tbody').find_all('tr')

	for time in times_list:
		if 'Relay' not in full_event_name:
			data = time.find_all('td')

			swimmer_name = data[1].text.strip()
			swimmer_ID = getID(data[1].find('a')['href'])

			team = data[2].text.strip()
			team_ID = getID(data[2].find('a')['href'])

			swim_time = data[3].text.strip()
			score = data[5].text.strip()
			imp = data[7].text.strip()

			results.append({'swimmer_name' : swimmer_name, 'swimmer_ID' : swimmer_ID, 'team' : team, 'team_ID' : team_ID, 'time' : swim_time, 'score' : score, 'Improvement' : imp})
		else:
			team = time.find('td', attrs = {'class' : 'u-nowrap'}).find('a').text.strip()
			team_ID = getID(time.find('td', attrs = {'class' : 'u-nowrap'}).find('a')['href'])

			swim_info = time.find_all('td', attrs = {'class' : 'u-text-end'})
			swim_time = swim_info[0].text.strip()
			score = swim_info[1].text.strip()

			print(team)
			print(team_ID)
			print(swim_time)
			print(score)

			#THERE are more table rows than just the time rows so we need to skip the other rows where it just has the relay swimmer's names

			results.append({'team_name' : team, 'team_ID' : team_ID, 'time' : swim_time, 'score' : score})

	return results

# TESTS ---------------------------------------------------------------------------------------------------------------------------

#getTeams tests ------------------------------------

#df = getTeams(team_names = ['University of Pittsburgh', 'University of Louisville'])
#print(df.head())

#df1 = getTeams(conference_names = ['ACC', 'Ivy'])
#print(df1)

#df2 = getTeams(division_names = ['Division 1'])
#print(df2.head())

#getRoster tests -----------------------------------------------

#penn_roster = getRoster(team = 'University of Pennsylvania', gender = 'M')
#pitt_roster = getRoster(team = 'University of Pittsburgh', gender = 'F', year = 2015)
#bc_roster = getRoster(team = 'Boston College', gender = 'M', season_ID = 22)

#print(penn_roster)
#print(pitt_roster)
#print(bc_roster)

#getSwimmerEvents tests ---------------------------------------------

#get a list of all events that swimmer #362091 (Blaise Vera) has participated in
#event_list = getSwimmerEvents(362091)

#loop through all of his events, and get all of his times in each event
#for event_name in event_list:
#	print(event_name)
#	print(getSwimmerTimes(362091, event_name)[0]) - just print out first time to check


#getTeamMeetList tests -----------------------------------------------------

#pitt_meet_list = getTeamMeetList(team_name = 'University of Pittsburgh', year = 2019)

#print(pitt_meet_list[8])

#getMeetResults tests -----------------------------------------------------------

r = getMeetResults(189095, '200 Medley Relay', 'F')

print(r[0])
print(r[4])
