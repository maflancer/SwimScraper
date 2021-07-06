import pandas as pd

teams = pd.read_csv('https://raw.githubusercontent.com/maflancer/CollegeSwimmingScraper/main/collegeSwimmingTeams.csv')

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
