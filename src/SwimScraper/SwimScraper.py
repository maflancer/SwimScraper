import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import time as _time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

teams = pd.read_csv('https://raw.githubusercontent.com/maflancer/SwimScraper/main/src/SwimScraper/collegeSwimmingTeams.csv')

events = {'25 Y Free' : '125Y', '25 Y Back' : '225 Y', '25 Y Breast' : '325Y', '25 Y Fly' : '425Y', '50 Y Free' : '150Y', '75 Y Free' : '175Y', '100 Y Free' : '1100Y', '125 Y Free' : '1125Y', '200 Y Free' : '1200Y', '400 Y Free' : '1400Y', '500 Y Free' : '1500Y', '800 Y Free' : '1800Y', '1000 Y Free' : '11000Y', '1500 Y Free' : '11500Y', '1650 Y Free' : '11650Y', '50 Y Back' : '250Y', '100 Y Back': '2100Y', '200 Y Back' : '2200Y', '50 Y Breast' : '350Y', '100 Y Breast' : '3100Y', '200 Y Breast' : '3200Y', '50 Y Fly' : '450Y', '100 Y Fly' : '4100Y', '200 Y Fly' : '4200Y', '100 Y IM' : '5100Y', '200 Y IM' : '5200Y', '400 Y IM' : '5400Y', '200 Free Relay' : 6200, '400 Free Relay' : 6400, '800 Free Relay' : 6800, '200 Medley Relay' : 7200, '400 Medley Relay' : 7400, '1 M Diving' : 'H1', '1 M Diving (6 dives)' : 'H16', '3 M Diving ' : 'H3', '3 M Diving (6 dives)' : 'H36', '7M Diving' : 'H75', '7M Diving (5 dives)' : 'H75Y','Platform Diving' : 'H2', '50 Individual' : 'H50', '100 Individual' : 'H100', '200 Individual' : 'H200', 
'25 S Free' : '125S', '25 S Back' : '225 S', '25 S Breast' : '325S', '25 S Fly' : '425S', '50 S Free' : '150S', '75 S Free' : '175S', '100 S Free' : '1100S', '125 S Free' : '1125S', '200 S Free' : '1200S', '400 S Free' : '1400S', '500 S Free' : '1500S', '800 S Free' : '1800S', '1000 S Free' : '11000S', '1500 S Free' : '11500S', '1650 S Free' : '11650S', '50 S Back' : '250S', '100 S Back': '2100S', '200 S Back' : '2200S', '50 S Breast' : '350S', '100 S Breast' : '3100S', '200 S Breast' : '3200S', '50 S Fly' : '450S', '100 S Fly' : '4100S', '200 S Fly' : '4200S', '100 S IM' : '5100S', '200 S IM' : '5200S', '400 S IM' : '5400S',
'50 L Free' : '150L', '100 L Free' : '1100L', '200 L Free' : '1200L', '400 L Free' : '1400L', '500 L Free' : '1500L', '800 L Free' : '1800L', '1000 L Free' : '11000L', '1500 L Free' : '11500L', '1650 L Free' : '11650L', '50 L Back' : '250L', '100 L Back': '2100L', '200 L Back' : '2200L', '50 L Breast' : '350L', '100 L Breast' : '3100L', '200 L Breast' : '3200L', '50 L Fly' : '450L', '100 L Fly' : '4100L', '200 L Fly' : '4200L', '100 L IM' : '5100L', '200 L IM' : '5200L', '400 L IM' : '5400L'}


us_states = {
	'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
	'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
	'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
	'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV','Wisconsin': 'WI',
	'Wyoming': 'WY'
}

#HELPER FUNCTIONS -------------------------------------

#changes name from (last, first) to (first last)
def cleanName(webName):
	nameList = webName.split(', ')
	last_name = nameList[0]
	first_name = nameList[1]

	return first_name + ' ' +  last_name

#gets corresponding team number for a specified team
def getTeamID(team_name):
	team_number = -1

	#search for the specified team
	for index, row in teams.iterrows():
		if row['team_name'] == team_name:
			team_number = row['team_ID']
	return team_number

#gets corresponding team name for a specified team_ID
def getTeamName(team_ID):
    team_name = ''

    for index, row in teams.iterrows():
        if row['team_ID'] == team_ID:
            team_name = row['team_name']
    return team_name

#gets corresponding season ID for a specified year
def getSeasonID(year):
	return year - 1996

#gets corresponding year for a specified season_ID
def getYear(season_ID):
    return season_ID + 1996

def getEventName(event_ID):
    return list(events.keys())[list(events.values()).index(event_ID)]

def getEventID(event_name):
	return events.get(event_name)

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

#converts a time of the format minutes:seconds (1:53.8) to seconds (113.8)
def convertTime(display_time):
    if ':' in displayTime:
        timeArray = displayTime.split(':')
        seconds = float(timeArray[0]) * 60
        seconds += float(timeArray[1])

        return seconds
    elif displayTime.isalpha():
        pass
    else:
        return float(displayTime)

#for the header of an html table including events
#returns a dictionary [meet_name_index, date_index, time_index]
def getIndexes(data):
	meet_name_index = -1
	date_index = -1
	additional_info_index = -1
	print(len(data))
	i = 0
	for td in data:
		if td.text.strip() == 'Meet':
			meet_name_index = i
		elif td.text.strip() == 'Date':
			date_index = i
		elif td.text.strip() == '' and td.has_attr('class') and 'c-table-clean__col-fit' in td['class']:
			additional_info_index = i

		i = i + 1

	indexes = {'meet_name_index': meet_name_index, 'date_index': date_index, 'additional_info_index': additional_info_index}

	return indexes


#SCRAPING FUNCTIONS ------------------------------------

#function that takes as an input any number of team names, a division, or a conference and returns the teams that match the input
#example function call - getTeams(conference = "ACC") - returns a list with all teams in the ACC conference
def getCollegeTeams(team_names = ['NONE'], conference_names = ['NONE'], division_names = ['NONE']):
	team_df = pd.DataFrame()
	if(team_names != ['NONE']):
		team_df = teams[teams['team_name'].isin(team_names)].reset_index(drop = True)
	elif(division_names != ['NONE']):
		team_df = teams[teams['team_division'].isin(division_names)].reset_index(drop = True)
	elif(conference_names != ['NONE']):
		team_df = teams[teams['team_conference'].isin(conference_names)].reset_index(drop = True)
	else:
		team_df = teams

	return team_df.to_dict('records')

#function that takes a gender and season_ID as an input and returns a list of top 50 countries from that year
def getTeamRankingsList(gender, season_ID = -1, year = -1):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	teams = list()

	if(gender != 'M' and gender != 'F'):
		print('ERROR: need to input either M or F for gender')
		return

	if(year != -1):
		season_ID = getSeasonID(year)
	elif(season_ID == -1 and year == -1):
		season_ID = 24 #most recent season

	page_url = 'https://swimcloud.com/team/rankings/?eventCourse=L?gender=' + gender + '&page=1&region&seasonId=' + str(season_ID)

	driver.get(page_url)

	_time.sleep(3)

	html = driver.page_source

	soup = bs(html, 'html.parser')

	teams_list = soup.find('table', attrs = {'class' : 'c-table-clean'}).find('tbody').find_all('tr')

	for team in teams_list:
		data = team.find_all('td')

		team =  data[1].find('strong').text.strip()
		team_ID = data[1].find('a')['href'].split('/')[-1]

		swimcloud_points = data[2].find('a').text.strip()

		teams.append({'team_name' : team, 'team_ID' : team_ID, 'swimcloud_points' : swimcloud_points})

	return teams

#function that takes a team and gender, and either a season_ID or year as an input and returns the team's roster from that year
#example function call - getRoster(team = "University of Pittsburgh", gender = "M") - if no season or year -> returns roster for current season - season #24
#                      - getRoster(team = "University of Pittsburgh", gender = "F", year = 2020) - roster for 2020-2021 team corresponds to season #24
def getRoster(team, gender, team_ID = -1, season_ID = -1, year = -1, pro = False):
	roster = list()

	if(gender != 'M' and gender != 'F'):
		print('ERROR: need to input either M or F for gender')
		return

	if(team_ID != -1):
		team_number = team_ID
		team = getTeamName(team_ID)
	else:
		team_number = getTeamID(team)

	if(year != -1):
		season_ID = getSeasonID(year)

	#if no season_ID or year is specified, return the roster for the most current season - might change later
	if(season_ID == -1 and year == -1):
		season_ID = 24

	roster_url = 'https://www.swimcloud.com/team/' + str(team_number) +  '/roster/?page=1&gender=' + gender + '&season_id=' + str(season_ID)

	url = requests.get(roster_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	try:
		data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:] #finds table of player names
	except AttributeError:
		print('An invalid team was entered, causing the following error:')
		raise

	for row in data:
		swimmer_name = cleanName(row.find('a').text.strip())
		idArray = row.find_all('a')  #returns array of length 1 which contains swimmer ID
		swimmer_ID = (idArray[0]['href']).split('/')[-1]
		numbers = row.find_all('td')
		state = getState(numbers[2].text.strip())
		city = getCity(numbers[2].text.strip())
		if(pro == False):
			grade = numbers[3].text.strip()
			HS_power_index = getPowerIndex(swimmer_ID)
		else:
			grade = 'None'
			HS_power_index = -1

		roster.append({'swimmer_name': swimmer_name, 'swimmer_ID' : swimmer_ID, 'team_name' : team, 'team_ID' : team_number, 'grade' : grade, 'hometown_state': state, 'hometown_city' : city, 'HS_power_index' : HS_power_index})

	return roster

#only from 2017 - current year   -    currently gets top 200 recruits
#takes as an input a year and gender and optionally a state or state_abbreviation and returns list of the top 50 HS recruits for that year with recruiting score, hometown info, team_info
def getHSRecruitRankings(class_year, gender, state = 'none', state_abbreviation = 'none', international = False):
	recruits = list()

	if(state != 'none'):
		state_abbreviation = us_states.get(state)

	if(gender != 'M' and gender != 'F'):
		print('ERROR: need to input either M or F for gender')
		return

	#if only international recruits are wanted
	if(international == True):
		recruiting_url = 'https://www.swimcloud.com/recruiting/rankings/' + str(class_year) + '/' + str(gender) + '/2/'
	#if recruits from a certain state are wanted
	elif(state_abbreviation != 'none'):
		recruiting_url = 'https://www.swimcloud.com/recruiting/rankings/' + str(class_year) + '/' + str(gender) + '/1/' + state_abbreviation + '/'
	elif(state != 'none'):
		recruiting_url = 'https://www.swimcloud.com/recruiting/rankings/' + str(class_year) + '/' + str(gender) + '/1/'  + us_states.get(state) + '/'
	#if rankings are wanted for US and international
	else:
		recruiting_url = 'https://www.swimcloud.com/recruiting/rankings/' + str(class_year) + '/' + str(gender) + '/'

	for page in range(1, 5):
		page_url = recruiting_url + '?page=' + str(page)

		url = requests.get(page_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

		url.encoding = 'utf-8'

		soup = bs(url.text, 'html.parser')

		recruit_list = (soup.find('div', attrs = {'class' : 'c-table-clean--responsive'}).find_all('tr'))[1:]

		for recruit in recruit_list:
			swimmer_name = recruit.find('a', attrs = {'class' : 'u-text-semi'}).text.strip()
			swimmer_ID = (recruit.find('a', attrs = {'class' : 'u-text-semi'})['href']).split('/')[-1]

			hometown_info = recruit.find('td', attrs = {'class' : 'u-color-mute'}).text.strip()
			state = getState(hometown_info)
			city = getCity(hometown_info)

			power_index = recruit.find('td', attrs = {'class' : 'u-text-end'}).text.strip()

			try:
				team_info = recruit.find('a', attrs = {'class' : 'u-inline-block'})
				team_name = team_info.find('img')['alt'].split(' ')
				team_name.pop() #removes logo from the end of the team name
				team = ' '.join([t.strip() for t in team_name])
				team_ID = (team_info['href']).split('/')[-1]
			except (TypeError, AttributeError) as e: #if no team is listed for the recruit
				team = 'None'
				team_ID = 'None'

			recruits.append({'swimmer_name' : swimmer_name, 'swimmer_ID' : swimmer_ID, 'team_name' : team, 'team_ID' : team_ID, 'hometown_state' : state, 'hometown_city' : city, 'HS_power_index' : power_index})

	return recruits

#given a swimmer's ID, return their high school power index -> this is an index used for recruiting
#returns -1 if no swimmer found
def getPowerIndex(swimmer_ID):
	swimmer_url = 'https://swimcloud.com/swimmer/' + str(swimmer_ID)

	url = requests.get(swimmer_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})
	url.encoding = 'utf-8'
	
	if url.status_code == 404:
		raise ValueError(f"The swimmer {swimmer_ID} was not found")

	soup = bs(url.text, 'html.parser')
	

	data_array = soup.find_all('li', {'class' : 'c-list-bar__item'}) # returns the container items containing headers for recruiting stats
	for d in data_array:
		if d.find(class_='c-list-bar__subheader').get('title') == 'Power index':
				return float(d.find(class_='c-list-bar__description').text.strip())

	swimmer_name = soup.find('h1', {'class' : 'c-toolbar__title'}).text.strip()

	swimmer_name_url = 'https://swimcloud.com/recruiting/rankings/?name=' + swimmer_name.replace(' ', '+')

	name_url = requests.get(swimmer_name_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	name_url.encoding = 'utf-8'

	name_soup = bs(name_url.text, 'html.parser')

	swimmer_list = name_soup.find('tbody').find_all('tr')
	
	for swimmer in swimmer_list:
		#check if this is the correct swimmer by looking to see if the link matches their id
		name = swimmer.find(class_='u-text-semi')
		swimmer_link = name['href'] if name else ''
		if(swimmer_link == "/swimmer/" + str(swimmer_ID)):
			#a power index was found for the specified swimmer_ID!
			return float(name_soup.find('td', {'class' : 'u-text-end'}).text.strip())

	return -1 #if no swimmer is found with the correct swimmer ID #, return -1

#takes as an input a swimmer's ID and returns a list of all events that they have participated in
def getSwimmerEvents(swimmer_ID):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	events = []
	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'

	# checks to see if the swimmer exists	
	url = requests.get(swimmer_URl, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})
	url.encoding = 'utf-8'
	
	if url.status_code == 404:
		raise ValueError(f"The swimmer {swimmer_ID} was not found")
	
	driver.get(swimmer_URL)

	if url.status_code == 404:
		raise ValueError(f"The swimmer {swimmer_ID} was not found")
	
	tabs = driver.find_elements(By.CSS_SELECTOR, 'li.c-tabs__item')

	_time.sleep(1) #makes sure the event tab pops up on website

	for tab in tabs: #finds correct tab on swimmer's profile and clicks on it
		if(tab.text == 'EVENT PROGRESSION'):
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

	driver.close()
	return events

#takes as an input a swimmer's ID # and returns a list of each indivudal time for the specified event
def getSwimmerTimes(swimmer_ID, event_name, event_ID = ''):
	#used chromedriver to interact with the swimcloud website and click on different dropdown menus

	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	time_list = list()
	if(event_ID == ''):
		event_ID = events.get(event_name)
	if(event_name == ''):
		event_name = getEventName(event_ID)
		#event_name = list(events.keys())[list(events.values()).index(event_ID)]

	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'
	dropdownCheck = True
	eventCheck = True

	driver.get(swimmer_URL)

	tabs = driver.find_elements(By.CSS_SELECTOR, 'li.c-tabs__item')

	_time.sleep(1) #makes sure the event tab pops up on website

	for tab in tabs: #finds correct tab on swimmer's profile and clicks on it
		if(tab.text == 'EVENT PROGRESSION'):
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

			tables = soup.find_all('table', attrs = {'class' : 'c-table-clean'})

			# Two tables on the page. Second table from the EVENT PROGRESSION tab and contains the times.
			try:
				header = tables[1].find_all('tr')[0:1]
				times = tables[1].find_all('tr')[1:]
			except AttributeError:
				header = []
				times = []

			columns = header[0].find_all('th')
			indexes = getIndexes(columns) #this function finds the correct indexes for the meet name, date, year, and improvement, as they are different for some swimmers
			
			for time in times:
				data = time.find_all('td')

				time = data[0].text.strip()

				if(indexes['meet_name_index'] == -1): #if no meet name was found
					meet = 'NA'
				else:
					meet = data[indexes['meet_name_index']].text.strip()

				if(indexes['date_index'] == -1): #if no date was found
					date = 'NA'
					year = 'NA'
				else:
					date = data[indexes['date_index']].text.strip()
					year = date.split(',')[-1]

				if(indexes['additional_info_index'] == -1): #if no additional info column was found
					additional_info = []
				else:
					td = data[indexes['additional_info_index']]
					spans = td.find_all('span')
					additional_info = [span['title'] for span in spans if span.has_attr('title')] # a list of the additional info provided for an event

				time_list.append({'swimmer_ID' : swimmer_ID, 'event': event_name, 'event_ID' : event_ID, 'time' : time, 'meet_name' : meet, 'year' : year, 'date' : date, 'additional_info': additional_info})


	driver.close()
	return time_list

#takes as an input a team_name or team_ID and either a season_ID or year ->   getTeamMeetList('University of Pittsburgh', season_ID = 23)
def getTeamMeetList(team_name = '', team_ID = -1, season_ID = -1, year = -1):
	meet_list = list()

	if(team_name != ''):
		team_number = getTeamID(team_name)
	elif(team_ID != -1):
		team_number = team_ID

	if(season_ID != -1):
		year = getYear(season_ID)

	#if no season_ID or year is specified, return the roster for the most current season - might change later
	if(season_ID == -1 and year == -1):
		year = 2021

	team_url = 'https://www.swimcloud.com/team/' + str(team_number) +  '/results/?page=1&name=&meettype=&year=' + str(year)

	url = requests.get(team_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	#finds the list of meets which includes meet name, meet ID#
	try:
		meets = soup.find('section', attrs = {'class' : 'c-list-grid'}).find_all('a', attrs = {'class' : 'c-list-grid__item'})
	except AttributeError:
		print('An invalid team was entered, causing the following error:')
		raise

	for meet in meets:
		meet_ID = (meet['href']).split('/')[-1] #extracts the meet_ID from the link's href

		meet_name = meet.find('article').find('h3').text.strip()

		meet_date = meet.find('time').text.strip()

		meet_location = (meet.find_all('li')[-1]).text.strip()

		meet_list.append({'team_ID': team_number, 'meet_ID' : meet_ID, 'meet_name' : meet_name, 'meet_date' : meet_date, 'meet_location' : meet_location})

	return meet_list

#takes as an input a meet's ID# and returns a list of all events from the specified meet
def getMeetEventList(meet_ID):
	meet_event_list = list()

	meet_url = 'https://swimcloud.com/results/' + str(meet_ID)

	url = requests.get(meet_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	try:
		event_list = soup.find('ul', attrs = {'class' : 'c-sticky-filters__list'}).find_all('li')
	except AttributeError:
		print('An invalid meet_ID was entered, causing the following error:')
		raise

	for event in event_list:
		event_name = event.find('div', attrs = {'class' : 'o-media__body'}).text.strip()
		event_href = event.find('a')['href']

		meet_event_list.append({'event_name' : event_name, 'event_ID' : events.get(' '.join(event_name.split(' ')[:-1])),'event_href' : event_href})

	return meet_event_list

#takes as an input a meet's ID # and an event's name and a gender and returns a list of all times for the specified event
def getCollegeMeetResults(meet_ID, event_name, gender, event_ID = -1, event_href = 'None'):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	results = list()

	if(gender != 'M' and gender != 'F'):
		print('ERROR: need to input either M or F for gender')
		return

	if(event_ID != -1):
		event_name = getEventName(event_ID)

	if(event_ID == -1):
		event_ID = events.get(event_name)

	if('Women' not in event_name and 'Men' not in event_name): #if men or women are not already in the event name
		if(gender == 'M'):
			full_event_name = event_name + ' Men'
		else:
			full_event_name = event_name + ' Women'

	if(event_href =='None'):
		results_url = 'https://www.swimcloud.com/results/' + str(meet_ID) + '/event/1/'
		event_url = 'none'

		driver.get(results_url)

		html = driver.page_source

		soup = bs(html, 'html.parser')

		#events are numbered starting from 1 so we need to find out the correct event number for the specified event name
		try:
			event_list = soup.find('ul', attrs = {'class' : 'c-sticky-filters__list'}).find_all('li')
		except AttributeError:
			print('An invalid meet_ID was entered, causing the following error:')
			raise

		for event in event_list:
			web_event_name = event.find('div', attrs = {'class' : 'o-media__body'}).text.strip()
			event_href = event.find('a')['href']

			#check if this event in the list is the event that we want results for
			if(web_event_name == full_event_name):
				event_url = 'https://www.swimcloud.com' + event_href
	else:
		event_url = 'https://www.swimcloud.com' + event_href

	#now we have the correct page for the specified event
	driver.get(event_url)

	html = driver.page_source

	soup = bs(html, 'html.parser')

	if(event_name == ''):
		event_name = soup.find('li', attrs = {'class' : 'active'}).find('a').text.strip()
		event_ID = events.get(event_name)

	event_groups = soup.find_all('div', attrs = {'class' : 'o-table-group'})

	#loop through each event group (A Final, B final, Semi-final, Preliminaries)
	for group in event_groups:
		group_label = group.find('caption', attrs = {'class' : 'c-table-clean__caption'}).text.strip()

		times_list = soup.find('div', attrs = {'class' : 'c-table-clean--responsive'}).find('tbody').find_all('tr')

		for time in times_list:
			if 'Relay' not in full_event_name:
				data = time.find_all('td')

				swimmer_name = data[1].text.strip()
				swimmer_ID = data[1].find('a')['href'].split('/')[-2]

				team = data[2].text.strip()
				team_ID = data[2].find('a')['href'].split('/')[-2]

				swim_time = data[3].text.strip()
				score = data[5].text.strip()
				imp = data[7].text.strip()

				results.append({'meet_ID': meet_ID, 'swimmer_name' : swimmer_name, 'swimmer_ID' : swimmer_ID, 'team_name' : team, 'team_ID' : team_ID, 'event_name' : event_name, 'event_ID' : event_ID, 'event_type' : group_label, 'time' : swim_time, 'score' : score, 'Improvement' : imp})

			else: #page is in a different format for relay events
				try: #skip over the rows with no data
					team = time.find('td', attrs = {'class' : 'u-nowrap'}).find('a').text.strip()
					team_ID = time.find('td', attrs = {'class' : 'u-nowrap'}).find('a')['href'].split('/')[-2]

					swim_info = time.find_all('td', attrs = {'class' : 'u-text-end'})
					swim_time = swim_info[0].text.strip()
					score = swim_info[1].text.strip()

					results.append({'meet_ID' : meet_ID, 'team_name' : team, 'team_ID' : team_ID, 'event_name' : event_name, 'event_ID' : event_ID, 'event_type' : group_label.split('\n')[0], 'time' : swim_time, 'score' : score})
				except AttributeError:
					pass

	driver.close()
	return results

def getProMeetResults(meet_ID, event_name, gender, event_ID = -1, event_href = 'None'):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	results = list()

	if(gender != 'M' and gender != 'F'):
		print('ERROR: need to input either M or F for gender')
		return

	if(event_ID != -1):
		event_name = getEventName(event_ID)

	if(event_ID == -1):
		event_ID = events.get(event_name)

	if('Women' not in event_name and 'Men' not in event_name):
		if(gender == 'M'):
			full_event_name = event_name + ' Men'
		else:
			full_event_name = event_name + ' Women'

	if(event_href == 'None'):
		results_url = 'https://www.swimcloud.com/results/' + str(meet_ID) + '/event/1/'
		event_url = 'none'

		driver.get(results_url)

		html = driver.page_source

		soup = bs(html, 'html.parser')

		#events are numbered starting from 1 so we need to find out the correct event number for the specified event name
		try:
			event_list = soup.find('ul', attrs = {'class' : 'c-sticky-filters__list'}).find_all('li')
		except AttributeError:
			print('An invalid meet_ID was entered, causing the following error:')
			raise

		for event in event_list:
			web_event_name = event.find('div', attrs = {'class' : 'o-media__body'}).text.strip()
			event_href = event.find('a')['href']

			#check if this event in the list is the event that we want results for
			if(web_event_name == full_event_name):
				event_url = 'https://www.swimcloud.com' + event_href
	else:
		event_url = 'https://www.swimcloud.com' + event_href

	#now we have the correct page for the specified event
	driver.get(event_url)

	html = driver.page_source

	soup = bs(html, 'html.parser')

	if(event_name == ''):
		event_name = soup.find('li', attrs = {'class' : 'active'}).find('a').text.strip()
		event_ID = events.get(event_name)

	event_groups = soup.find_all('div', attrs = {'class' : 'o-table-group'})

	#loop through each event group (A Final, B final, Semi-final, Preliminaries)
	for group in event_groups:
		group_label = group.find('caption', attrs = {'class' : 'c-table-clean__caption'}).text.strip()

		times_list = group.find('tbody').find_all('tr')

		for time in times_list:
			if 'Relay' not in full_event_name:
				data = time.find_all('td')

				swimmer_name = data[1].find('a').text.strip()
				swimmer_ID = (data[1].find('a')['href']).split('/')[-2]

				team = data[2].find('span').text.strip()
				try:
					team_ID = (data[2].find('a')['href']).split('/')[-2]
				except TypeError:
					team_ID = -1

				swim_time = data[3].text.strip()
				swim_FINA_score = data[5].text.strip()
				imp = data[6].text.strip()

				results.append({'meet_ID' : meet_ID, 'swimmer_name' : swimmer_name, 'swimmer_ID' : swimmer_ID, 'team_name' : team, 'team_ID' : team_ID, 'event_name' : event_name, 'event_ID' : event_ID, 'event_type' : group_label, 'time' : swim_time, 'FINA_score' : swim_FINA_score, 'Improvement' : imp})
			else: #relay events are different format
				try:
					team = time.find('td', attrs = {'class' : 'u-nowrap'}).find('a').text.strip()
					team_ID = time.find('td', attrs = {'class' : 'u-nowrap'}).find('a')['href'].split('/')[-2]

					swim_info = time.find_all('td', attrs = {'class' : 'u-text-end'})
					swim_time = swim_info[0].text.strip()
					FINA_score = swim_info[1].text.strip()

					results.append({'meet_ID' : meet_ID, 'team_name' : team, 'team_ID' : team_ID, 'event_name' : event_name, 'event_ID' : event_ID, 'event_type' : group_label.split('\n')[0], 'time' : swim_time, 'FINA_score' : FINA_score})
				except AttributeError:
					pass
	driver.close()
	return results


#--------- stil in progress ----------------

#takes any number of teams as an input and returns the "simulated" results of the inputted event based on times from the specified year
def getMeetSimulator(teams, gender, event_name, year = -1, event_ID = -1):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	times = list()

	if(gender != 'M' and gender != 'F'):
		print('ERROR: need to input either M or F for gender')
		return

	if(event_ID == -1):
		event_ID = events.get(event_name)

	meet_url = 'https://www.swimcloud.com/meetsimulator/?event=' + str(event_ID) + 'Y/&teams=' + ','.join(str(team) for team in teams)

	driver.get(meet_url)

	#make sure all javascript is run on page so times show up
	_time.sleep(5)

	#if we need to change the gender
	if(gender == 'F'):
		pass #TODO
	#if we need to change the date range to get times from
	if(year != -1):
		pass #TODO

	#select the specified event from the dropdown
	event_select = Select(driver.find_element(By.ID, 'select_2'))
	event_select.select_by_visible_text(event_name)

	html = driver.page_source

	soup = bs(html, 'html.parser')

	times_table = soup.find_all('table', attrs = {'class' : 'c-table-clean'})[1]

	times_list = times_table.find('tbody').find_all('tr')

	for time in times_list:
		if 'Relay' not in event_name:
			swimmer_info = time.find('div', attrs = {'class' : 'u-text-truncate'}).find('a')
			swimmer_name = cleanName(swimmer_info.text.strip())
			swimmer_ID = swimmer_info['href'].split('/')[-2]

			team_info = time.find('td', attrs = {'class' : 'u-text-center'})
			team_name = team_info.find('img')['alt']
			team_ID = team_info.find('a')['href'].split('/')[-2]

			swimmer_time = time.find('input')['value']
			swimmer_points = time.find_all('td', attrs = {'class': 'u-text-end'})[1].text.strip()
			swimmer_entries = time.find('button').text.strip()

			times.append({'swimmer_name' : swimmer_name, 'swimmer_ID' : swimmer_ID, 'team_name' : team_name, 'team_ID' : team_ID, 'time' : swimmer_time, 'points' : swimmer_points, 'entries' : swimmer_entries})
		else: #different format for relay events
			team_info = time.find('div', attrs = {'class' : 'u-flex'}).find('a')
			team = team_info.text.strip()
			team_ID = team_info['href'].split('/')[-2]

			time_info = time.find_all('td', attrs = {'class' : 'u-text-end'})
			team_time = time_info[0].text.strip()
			team_points = time_info[1].text.strip()

			times.append({'team_name' : team, 'team_ID' : team_ID, 'time' : team_time, 'points' : team_points})

	driver.close()
	return times
