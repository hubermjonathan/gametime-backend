from flask import Blueprint, jsonify, request, abort, Response
from ..db import fundraising as db
from ..db import users as userdb
from ..db import teams as teamdb
from . import schema
import boto3
from flask_login import login_required, current_user
from .. import auth
from os import environ
from datetime import datetime
from jsonschema import validate
from . import schema
import csv
from io import StringIO, BytesIO

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

    try:
        teamId = body['teamId']
        startTime = body['startTime']
        endTime = body['endTime']
        goal = body['goal']
        description = body['description']

        isTeam = body['isTeam']
    except:
        return "missing field", 400

    user = current_user.user_id

    try:
        int(goal)
        float(startTime)
        float(endTime)
    except:
        return "number value incorrect", 400

    ret = ""
    if isTeam == "True":
        if not auth.isOwner(user, teamId):
            return "is not owner of team", 401
        ret = db.start_teams_fundraiser(
            teamId, startTime, endTime, goal, description)[0], 200
    else:
        if not auth.isPlayer(user, teamId):
            return "is not player in team", 401
        ret = db.start_users_fundraiser(
            current_user.user_id, teamId, startTime, endTime, goal, description)[0], 200

    if ret[0].find("invalid") != -1:
        return "fund not found", 404

    return "fund started", 200


@fundraisingbp.route('/fundraising/edit', methods=['POST'])
@login_required
def editFundraisingInfo():
    body = request.get_json()

    try:
        teamId = body['teamId']
        endTime = body['endTime']
        goal = body['goal']
        description = body['description']
        current = body['current']

        isTeam = body['isTeam']
    except Exception as e:
        print(e)
        return "missing field", 400

    user = current_user.user_id

    try:
        int(goal)
        float(endTime)
    except:
        return "number value incorrect", 400

    ret = ""
    if isTeam == "True":
        if not auth.isOwner(user, teamId):
            return "is not owner of team", 401
        ret = db.edit_teams_fundraiser(
            teamId, goal, current, description, endTime)[0], 200
    else:
        if not auth.isPlayer(user, teamId):
            return "is not player in team", 401
        ret = db.edit_users_fundraiser(
            current_user.user_id, teamId, goal, current, description, endTime)[0], 200

    if ret[0].find("invalid") != -1:
        return "fund not found", 404

    return "found edited", 200


@fundraisingbp.route('/fundraising/template', methods=['GET', 'POST'])
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

    try:
        recipient = body['recipient']
        subject = body['subject']
        emailBody = body['body']
    except:
        return "missing field", 400

    try:
        client = boto3.client('ses',
                              aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
                              aws_secret_access_key=environ.get(
                                  'AWS_SECRET_ACCESS_KEY'),
                              region_name='us-east-1')
    except:
        return "cannot access cloud", 500

    try:
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
    except:
        return "invalid fields in body", 400

    return "Email sent", 200


@fundraisingbp.route('/fundraising/report', methods=['POST'])
@login_required
def generate_report():
    # POST, create an item
    if request.method == 'POST':
        body = request.get_json()

        try:
            validate(body, schema=schema.generate_report_schema)
        except:
            return jsonify({'message': 'Bad Request'}), 400

        team_id = body['team_id']

        Check permissions
        if not auth.isAdmin(current_user.user_id, team_id) and not auth.isOwner(current_user.user_id, team_id):
            return jsonify({'message': 'Unauthorized'}), 401

        message, error, data = db.get_teams_fundraiser_report(team_id)
        if error:
            return jsonify({'message': 'Failed to create item'}), 400

        csv_file = StringIO()
        fieldnames = ['buyer_email', 'amount',
                      'time_purchased', 'transaction_id']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writerow({
            'buyer_email': 'Donater Email',
            'amount': 'Amount Donated',
            'time_purchased': 'Time of Donation',
            'transaction_id': 'Donation ID',
        })

        for transaction in data['transactions']:
            transaction['amount'] = f"${transaction['amount']}"
            transaction['time_purchased'] = transaction['time_purchased'].strftime(
                "%Y-%m-%d %H:%M:%S")
            writer.writerow(transaction)

        return Response(
            csv_file.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=report.csv"})
