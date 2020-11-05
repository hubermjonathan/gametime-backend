from flask import Blueprint, jsonify, request, abort
from ..db import fundraising as db
from ..db import users as userdb
from ..db import teams as teamdb
from . import schema
import boto3
from flask_login import login_required, current_user
from os import environ
from datetime import datetime

fundraisingbp = Blueprint('fundraisingbp', __name__)

@fundraisingbp.route('/fundraising/test', methods=['GET'])
def test():
    res = db.print_all_team_fundraisers()
    db.print_all_user_fundraisers()

    print(res)

    return res[2], 200

@fundraisingbp.route('/fundraising/user', methods=['GET'])
def getUserFundId():
    user = request.args.get('user')
    team = request.args.get('team')

    res = db.get_user_fund_id(user, team)

    return res[2], 200

@fundraisingbp.route('/fundraising/team', methods=['GET'])
def getTeamFundId():
    team = request.args.get('team')

    res = db.get_team_fund_id(team)

    return res[2], 200


@fundraisingbp.route('/fundraising/id/<teamid>/<userid>', methods=['GET'])
def getUserFundraisingInfo(teamid, userid):
    # Check if res was valid because we do not know which table
    # this fundraiser is in
    try:
        fund = db.get_users_fundraiser(userid, teamid)
        user = userdb.get_user(userid)
        team = teamdb.get_team(teamid)

        data = fund[2]
        if not bool(data):
            return "fund does not exist", 404

        ret = {
            "first_name": user[2].get('first_name'),
            "last_name": user[2].get('last_name'),
            "team_name": team[2].get('name'),
            "donation_total": data.get('fund_current'),
            "donation_goal": data.get('fund_goal'),
            "description":  data.get('fund_desc'),
            "start_timestamp":  data.get('fund_start').timestamp(),
            "end_timestamp":  data.get('fund_end').timestamp()
        }

        return ret, 200
    
    except AttributeError:
        return "fund does not exist", 404
    except Exception:
        return "Server error", 500

@fundraisingbp.route('/fundraising/id/<teamid>', methods=['GET'])
def getTeamFundraisingInfo(teamid):
    try:
        fund = db.get_teams_fundraiser(teamid)

        data = fund[2]
        if not bool(data):
            return "fund does not exist", 404

        ret = {
            "team_name": data.get('name'),
            "donation_total": data.get('fund_current'),
            "donation_goal": data.get('fund_goal'),
            "description":  data.get('fund_desc'),
            "start_timestamp":  data.get('fund_start').timestamp(),
            "end_timestamp":  data.get('fund_end').timestamp()
        }

        print(ret)

        return ret
    except AttributeError:
        return "fund does not exist", 404
    except Exception:
        return "Server error", 500
        
@fundraisingbp.route('/fundraising/start', methods=['POST'])
@login_required
def startFundraiser():
    body = request.get_json()

    teamId = body['teamId']
    startTime = body['startTime']
    endTime = body['endTime']
    goal = body['goal']
    description = body['description']

    if goal.find(',') != -1:
        return "comma in goal value", 400

    isTeam = body['isTeam']
    print(teamId)
    if isTeam == "True":
        print(teamId)
        return db.start_teams_fundraiser(teamId, startTime, endTime, goal, description)[0], 200
    else:
        return db.start_users_fundraiser(current_user.user_id, teamId, startTime, endTime, goal, description)[0], 200

    #Note 404

@fundraisingbp.route('/fundraising/edit', methods=['POST'])
@login_required
def editFundraisingInfo():
    body = request.get_json()
    print(body)

    teamId = body['teamId']
    endTime = body['endTime']
    goal = body['goal']
    current = body['current']
    description = body['description']

    isTeam = body['isTeam']

    # Verify user has permission for that team/userteam
    if isTeam == "True":
        print(teamId)
        return db.edit_teams_fundraiser(teamId, goal, current, description, endTime)[0],200
    else:
        return db.edit_users_fundraiser(current_user.user_id, teamId, goal, current, description, endTime)[0], 200

@fundraisingbp.route('/fundraising/template', methods=['GET','POST'])
@login_required
def emailInfo():

    if request.method == 'GET':
        # return call to db function to retrive it
        print("Get")
    elif request.method == 'POST':
        # return call to db function to set it
        print("Post")
        

@fundraisingbp.route('/fundraising/email', methods=['POST'])
@login_required
def sendEmail():
    body = request.get_json()

    recipient = body['recipient']
    subject = body['subject']
    emailBody = body['body']

    client = boto3.client('ses',
        aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-1')
    
    response = client.send_email(
    Source='gametimefundraising@gmail.com',
    Destination={
        'ToAddresses': [
            recipient,
        ]
    },
    Message={
        'Subject': {
            'Data': subject,
            'Charset': 'utf-8'
        },
        'Body': {
            'Text': {
                'Data': emailBody,
                'Charset': 'utf-8'
            }
        }
    })

    return "Email sent"
