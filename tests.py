import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from mainScraper import *

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
#	print(getSwimmerTimes(362091, event_name)[0]) #- just print out first time to check


#getTeamMeetList tests -----------------------------------------------------

#pitt_meet_list = getTeamMeetList(team_name = 'University of Pittsburgh', year = 2019)

#print(pitt_meet_list[8])

#getMeetResults tests -----------------------------------------------------------

#r = getMeetResults(136218, '100 Free', 'F')

#print(r[0])
#print(r[3])

#getHSRecruitRankings tests -------------------------------------------------

#recruits_2018 = getHSRecruitRankings(2018, 'M')

#print(recruits_2018[0])
#print(recruits_2018[23])

#getMeetSimulator tests ---------------------------------------------------

#times = getMeetSimulator([405,394], 'M', event_name = '100 Free')

#for time in times:
#	print(time)

#test for US olympic swimmer Nathan Adrian----------------
#event_list = getSwimmerEvents(257824)

#loop through all of his events, and get all of his times in each event
#for event_name in event_list:
#	print(event_name)
#	print(getSwimmerTimes(257824, event_name)[0]) #- just print out first time

#getTrialResults tests----------------------------------------------

#test for USA olympic team trials - wave 1
r = getTrialResults(2020, '400 Free', 'M')

print(r[1])
