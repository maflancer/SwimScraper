import pandas as pd

teams = pd.read_csv('https://raw.githubusercontent.com/maflancer/CollegeSwimmingScraper/main/collegeSwimmingTeams.csv')

events = {'25 Free' : 125, '25 Back' : 225, '25 Breast' : 325, '25 Fly' : 425, '50 Free' : 150, '75 Free' : 175, '100 Free' : 1100, '125 Free' : 1125, '200 Free' : 1200, '400 Free' : 1400, '500 Free' : 1500, '800 Free' : 1800, '1000 Free' : 11000, '1500 Free' : 11500, '1650 Free' : 11650, '50 Back' : 250, '100 Back': 2100, '200 Back' : 2200, '50 Breast' : 350, '100 Breast' : 3100, '200 Breast' : 3200, '50 Fly' : 450, '100 Fly' : 4100, '200 Fly' : 4200, '100 IM' : 5100, '200 IM' : 5200, '400 IM' : 5400, '200 Free Relay' : 6200, '400 Free Relay' : 6400, '800 Free Relay' : 6800, '200 Medley Relay' : 7200, '400 Medley Relay' : 7400, '1 M Diving' : 'H1', '3 M Diving' : 'H3', 'Platform Diving' : 'H2'}

#HELPER FUNCTIONS -------------------------------------

#changes name from (last, first) to (first last)
def cleanName(webName):
	nameList = webName.split(', ')
	last_name = nameList[0]
	first_name = nameList[1]

	return first_name + ' ' +  last_name

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

#gets corresponding year for a specified season_ID
def getYear(season_ID):
    return season_ID + 1996

def getEventName(event_ID):
    return list(events.keys())[list(events.values()).index(event_ID)]

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
