from flask import Blueprint, jsonify, request, abort
from ..db import fundraising as db
from . import schema
from flask_login import login_required, current_user

groupsbp = Blueprint('fundraisingbp', __name__)

@fundraisingsbp.route('/fundraising/user', methods=['GET'])
def getUserFundId(id):
    user = request.args.get('user')
    team = request.args.get('team')

    res = db.get_user_fund_id(user, team)

    return res

@fundraisingsbp.route('/fundraising/team', methods=['GET'])
def getTeamFundId(id):
    team = request.args.get('team')

    res = db.get_team_fund_id(team)

    return res


@fundraisingsbp.route('/fundraising/<id>', methods=['GET'])
def getFundraisingInfo(id):
    # Check if res was valid because we do not know which table
    # this fundraiser is in
    try:
        res = db.get_teams_fundraiser(id)
    except:
        res = db.get_users_fundraiser(id)
        
@fundraisingsbp.route('/fundraising/start', methods=['POST'])
def startFundraiser():
    fundId = body['fundId']
    endTime = body['endTime']

    try:
        db.start_teams_fundraiser(fundId, endTime)
    except:
        db.start_users_fundraiser(fundId, endTime)

@fundraisingsbp.route('/fundraising/edit', methods=['POST'])
@login_required
def getFundraisingInfo():
    fundId = body['fundId']
    goal = body['goal']
    current = body['current']
    description = body['description']

    # Verify user has permission for that team/userteam
    try:
        db.edit_teams_fundraiser(fundId, goal, current, description)
    except:
        db.edit_users_fundraiser(fundId, goal, current, description)

@fundraisingsbp.route('/fundraising/template', methods=['GET','POST'])
@login_required
def emailInfo():

    if request.method == 'GET':
        # return call to db function to retrive it
    else if request.method == 'POST':
        

@fundraisingsbp.route('/fundraising/email', methods=['GET'])
@login_required
def sendEmail():
