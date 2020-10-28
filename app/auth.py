import jwt
from jwt.algorithms import RSAAlgorithm

import os
import json

from app.db import teams as db

public_keys = {}

def decodeJWK():
    # Check if empty
    if public_keys:
        return False

    # Private key may not load in correctly
    try:
        jwks = json.load(open("app/.jsonKey", "r"))
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    except Exception as e:
        print("Loading Cognito Public Key failed")
        print(e)

def decodeJWT(access_token_enc):
    kid = jwt.get_unverified_header(access_token_enc)['kid']
    key = public_keys[kid]
    return jwt.decode(access_token_enc, public_keys[kid], algorithms='RS256')

def isPlayer(username, team_id):
    permLevel = db.get_users_permission_level_for_team(username, team_id)
    return permLevel >= 0

def isAdmin(username, team_id):
    permLevel = db.get_users_permission_level_for_team(username, team_id)
    return permLevel >= 1

def isOwner(username, team_id):
    permLevel = db.get_users_permission_level_for_team(username, team_id)
    return permLevel >= 2