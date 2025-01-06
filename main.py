import config
import http.client
import json

conn = http.client.HTTPSConnection("nfl-api-data.p.rapidapi.com")

headers = {
    'x-rapidapi-key': config.api_key,
    'x-rapidapi-host': "nfl-api-data.p.rapidapi.com"
}

#######################
## GET INFO FROM API ##
#######################
def get_info(url):
    conn.request("GET", url, headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    return json.loads(data)

######################################
## GET BASIC TEAM INFO OF ALL TEAMS ##
######################################
def get_all_teams_info():
    return get_info("/nfl-team-list")

#############################
## OBTAIN RAPIDAPI TEAM ID ##
#############################
def get_team_id(team_name):
    json_data = get_all_teams_info()
    for i in range(0, 32):
        nickname = json_data['teams'][i]['nickname']
        if nickname == team_name:
            break
    return json_data['teams'][i]['id']

###################################################
## GET MORE SPECIFIC TEAM INFO OF CURRENT SEASON ##
###################################################
def get_team_info(team_name):
    team_id = get_team_id(team_name)
    get_info(f"/nfl-team-info?id={team_id}")

##################################################
## GET SPECIFIC TEAM RECORDS FOR A GIVEN SEASON ##
##################################################
def get_team_records_info(team_name, season):
    team_id = get_team_id(team_name)
    json_data = get_info(f"/nfl-team-record?id={team_id}&year={season}")
    return json_data

#######################################################
## GET WIN-LOSS RECORD FOR A TEAM FOR A GIVEN SEASON ##
#######################################################
def get_team_win_loss_record(team_name, season):
    json_data = get_team_records_info(team_name, season)
    return json_data['items'][0]['summary']

#######################################################
## PRINT A TEAM'S WIN-LOSS RECORD FOR A GIVEN SEASON ##
#######################################################
def print_team_win_loss_record(team_name, season):
    record = get_team_win_loss_record(team_name, season)
    print(f"\nThe {team_name}' record in the {season}-{season+1} season was {record}.")

#################################################
## GET # OF WINS FOR A TEAM FOR A GIVEN SEASON ##
#################################################
def get_team_wins(team_name, season):
    json_data = get_team_records_info(team_name, season)
    return json_data['items'][0]['stats'][19]['value']

###################################################
## PRINT # OF WINS FOR A TEAM FOR A GIVEN SEASON ##
###################################################
def print_team_wins(team_name, season):
    wins = get_team_wins(team_name, season)
    print(f"\nThe {team_name}' won {wins} games in the {season}-{season+1} season.")

###################################################
## GET # OF LOSSES FOR A TEAM FOR A GIVEN SEASON ##
###################################################
def get_team_losses(team_name, season):
    json_data = get_team_records_info(team_name, season)
    return json_data['items'][0]['stats'][10]['value']

#####################################################
## PRINT # OF LOSSES FOR A TEAM FOR A GIVEN SEASON ##
#####################################################
def print_team_losses(team_name, season):
    losses = get_team_losses(team_name, season)
    print(f"\nThe {team_name}' lost {losses} games in the {season}-{season+1} season.")

######################################################################
## GET SPECIFIC INFO ABOUT A TEAM's SCHEDULE FOR THE CURRENT SEASON ##
######################################################################
def get_team_schedule_info(team_name):
    team_id = get_team_id(team_name)
    json_data = get_info(f"/nfl-team-schedule?id={team_id}")
    return json_data

####################################################################
## GET THE OPPONENT'S NAME FOR A GIVEN WEEK IN THE CURRENT SEASON ##
####################################################################
def get_opponent_name(team_name, week):
    json_data = get_team_schedule_info(team_name)
    bye_week = json_data['byeWeek']
    if week >= int(bye_week):
        week -= 1

    opponent = json_data['events'][week-1]['competitions'][0]['competitors'][0]['team']['nickname']
    if opponent == team_name:
        opponent = json_data['events'][week-1]['competitions'][0]['competitors'][1]['team']['nickname']
    return opponent

######################################################################
## PRINT THE OPPONENT'S NAME FOR A GIVEN WEEK IN THE CURRENT SEASON ##
######################################################################
def print_opponent_name(team_name, week): 
    opponent = get_opponent_name(team_name, week)
    print(f"\nThe {team_name}' week {week} opponent is the {opponent}")

#########################################################
## GET A TEAM'S WEEKLY SCHEDULE FOR THE CURRENT SEASON ##
#########################################################
def get_team_schedule(team_name):
    json_data = get_team_schedule_info(team_name)
    bye_week = json_data['byeWeek']

    current_week = 1
    schedule = []

    for i in range(0, 17):
        opp = (json_data['events'][i]['competitions'][0]['competitors'][0]['team']['nickname'])
        if opp == team_name:
            opp = json_data['events'][i]['competitions'][0]['competitors'][1]['team']['nickname']
        schedule.append(opp)
        
        current_week += 1
        if current_week == int(bye_week):
            schedule.append("BYE")
            current_week += 1
    return schedule

###########################################################
## PRINT A TEAM'S WEEKLY SCHEDULE FOR THE CURRENT SEASON ##
###########################################################
def print_team_schedule(team_name): 
    schedule = get_team_schedule(team_name)
    print(f"\nPrinting the team schedule for the {team_name}...")
    for i in range(0,18):
        print(f"Week {i+1}: {schedule[i]}")


## The above functions should all be moved into their own files for project organization...
######################################################################################################################################################

###########################
## USEFUL FUNCTION CALLS ##
###########################
# team_win_loss_record = get_team_win_loss_record(team_name, year)
# team_wins = get_team_wins(team_name, year)
# team_losses = get_team_losses(team_name, year)
# print_opponent_name("Patriots", 12)
# print_team_schedule("Jets")
print_team_win_loss_record("Patriots", 2017)



#################################
## Valid team names to lookup: ##
#################################
"""
49ers         Giants
Bears         Jaguars
Bengals       Jets
Bills         Lions
Broncos       Packers
Browns        Panthers
Buccs         Patriots
Buccaneers    Raiders
Cardinals     Rams
Chargers      Ravens
Chiefs        Saints
Colts         Seahawks
Commanders    Steelers
Cowboys       Texans
Eagles        Titans
Falcons       Vikings
 
"""