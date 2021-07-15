from mainScraper import *

# TESTS ---------------------------------------------------------------------------------------------------------------------------

#getTeams tests ------------------------------------

#df = getTeams(team_names = ['University of Pittsburgh', 'University of Louisville'])
#print(df.head())

#df1 = getTeams(conference_names = ['ACC', 'Ivy'])
#print(df1)

#df2 = getTeams(division_names = ['Division 1'])
#print(df2.head())

#getPowerIndex tests ----------------------------------------
#invalid swimmer_ID
#print(getPowerIndex(3834))

#print(getPowerIndex(433591))

#test two people with the same name -
#print(getPowerIndex(295739))
#print(getPowerIndex(501834))

#getRoster tests -----------------------------------------------

#check invalid team tame
#penn_roster = getRoster(team = 'Universit of Pennsylvania', team_ID = 300, gender = 'M')

#pitt_roster = getRoster(team = 'University of Pittsburgh', gender = 'F', year = 2020)
#bc_roster = getRoster(team = 'Boston College', gender = 'M', season_ID = 22)

#print(penn_roster)
#print(pitt_roster)
#print(bc_roster)

#test on a country's team

#japan_roster = getRoster(team = 'Japan', team_ID = 10008082, gender = 'M', year = 2020)

#print(japan_roster)

#print(getSwimmerTimes(japan_roster[0]['swimmer_ID'], '50 Individual'))
#print(getSwimmerTimes(japan_roster[1]['swimmer_ID'], '50 Back'))


#getSwimmerEvents tests ---------------------------------------------

#check invalid swimmer
#print(getSwimmerEvents(1815112121))

#get a list of all events that swimmer #362091 (Blaise Vera) has participated in
#event_list = getSwimmerEvents(362091)

#loop through all of his events, and get all of his times in each event
#for event_name in event_list:
#	print(event_name)
#	print(getSwimmerTimes(362091, event_name)[0]) #- just print out first time to check

#check invalid swimemrTimes
#print(getSwimmerTimes(1815112121, '100 Free'))

#getTeamMeetList tests -----------------------------------------------------

#pitt_meet_list = getTeamMeetList(team_name = 'University of Pittsburgh', year = 2019)
#print(pitt_meet_list[8])

#USA_meet_list = getTeamMeetList(team_name = '', team_ID = 10008158, season_ID = 23)
#print(USA_meet_list)

#getCollegeMeetResults tests -----------------------------------------------------------

#check invalid meet_ID
#i = getCollegeMeetResults(1111111111, '100 Free', 'F')

#r = getCollegeMeetResults(190690, '100 Free', 'F')

#print(r[0])
#print(r[3])

#getHSRecruitRankings tests -------------------------------------------------

#recruits_2018 = getHSRecruitRankings(2018, 'M', state = 'Hawaii')

#print(recruits_2018[0])
#print(recruits_2018[49])

#getMeetSimulator tests ---------------------------------------------------

#times = getMeetSimulator([405,394], 'F', event_name = '100 Free')

#for time in times:
#	print(time)

#test for US olympic swimmer Nathan Adrian----------------
#event_list = getSwimmerEvents(257824)

#loop through all of his events, and get all of his times in each event
#for event_name in event_list:
#	print(event_name)
#	print(getSwimmerTimes(257824, event_name)[0]) #- just print out first time

#print(getSwimmerTimes(257824, '', 150))

#getProMeetResults tests----------------------------------------------

#test for USA olympic team trials - wave 1
#r = getProMeetResults(2020, '400 Free', 'M')

#print(r)

#olympic_200_Free_men_results = getProMeetResults(106117, event_name = '200 Free', gender = 'M')
#print(olympic_200_Free_men_results)

#olympic_400_medley_relay_women_results = getProMeetResults(106117, event_name = '400 Medley Relay', gender = 'F')
#print(olympic_400_medley_relay_women_results)


#getMeetEventList tests ----------------------------------------------------

#invalid meet
#print(getMeetEventList(-1))

#2012 olympic games:
#olympics_event_list_2012 = getMeetEventList(196380)
#check getProMeetResults with event_href input from event_list
#print(getProMeetResults(196380, event_name = '', gender = 'M', event_href = olympics_event_list_2012[0]['event_href']))


#college test - pitt vs UVA - 2018
#print(getMeetEventList(132606))
#print(getCollegeMeetResults(132606, event_name = '', gender = 'F', event_ID = 7200))


#check on swimmer Jeff Rouse who competed for USA in 1992 and 1996 olympics
#print(getSwimmerTimes(1447896, '100 Back'))
