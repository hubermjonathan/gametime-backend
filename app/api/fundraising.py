from flask import Blueprint, jsonify, request, abort
from ..db import fundraising as db
from . import schema
import json
from flask_login import login_required, current_user

fundraisingbp = Blueprint('fundraisingbp', __name__)

@fundraisingbp.route('/fundraising/test', methods=['GET'])
def test():
    res = db.print_all_team_fundraisers()
    db.print_all_user_fundraisers()

    return res

@fundraisingbp.route('/fundraising/user', methods=['GET'])
def getUserFundId():
    user = request.args.get('user')
    team = request.args.get('team')

    res = db.get_user_fund_id(user, team)

    return res

@fundraisingbp.route('/fundraising/team', methods=['GET'])
def getTeamFundId():
    team = request.args.get('team')

    res = db.get_team_fund_id(team)

    return res


@fundraisingbp.route('/fundraising/id/<id>', methods=['GET'])
def getFundraisingInfo(id):
    # Check if res was valid because we do not know which table
    # this fundraiser is in
    res = db.get_teams_fundraiser(id)

    # Check if dictionary is empty
    if bool(res[2]):
        data = res[2]
        print(data)
        ret = {
            "first_name": "TBD",
            "last_name": "TBD",
            "team_name": "TBD",
            "donation_total": data.get('fund_current'),
            "donation_goal": data.get('fund_goal'),
            "description":  data.get('fund_desc'),
            "start_timestamp":  data.get('fund_start'),
            "end_timestamp":  data  .get('fund_end')
        }

        return ret
    else:
        res = db.get_users_fundraiser(id)

        data = res[2]
        ret = {
            "first_name": "TBD",
            "last_name": "TBD",
            "team_name": "TBD",
            "donation_total": data.get('fund_current'),
            "donation_goal": data.get('fund_goal'),
            "description":  data.get('fund_desc'),
            "start_timestamp":  data.get('fund_start'),
            "end_timestamp":  data  .get('fund_end')
        }

        return ret
        
@fundraisingbp.route('/fundraising/start', methods=['POST'])
def startFundraiser():
    body = request.get_json()

    fundId = body['fundId']
    endTime = body['endTime']

    try:
        print(db.start_teams_fundraiser(fundId, endTime))
    except:
        print(db.start_users_fundraiser(fundId, endTime))


    return "Done"

@fundraisingbp.route('/fundraising/edit', methods=['POST'])
@login_required
def editFundraisingInfo():
    body = request.get_json()
    
    fundId = body['fundId']
    goal = body['goal']
    current = body['current']
    description = body['description']

    # Verify user has permission for that team/userteam
    try:
        db.edit_teams_fundraiser(fundId, goal, current, description)
    except:
        db.edit_users_fundraiser(fundId, goal, current, description)

@fundraisingbp.route('/fundraising/template', methods=['GET','POST'])
@login_required
def emailInfo():

    if request.method == 'GET':
        # return call to db function to retrive it
        print("Get")
    elif request.method == 'POST':
        # return call to db function to set it
        print("Post")
        

@fundraisingbp.route('/fundraising/email', methods=['GET'])
@login_required
def sendEmail():
    print("Send")