import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid

CLIENT_ID = #Add before putting on AWS
CLIENT_SECRET =  #Add before putting on AWS

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
    msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
    
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    username = event['email']
    password = event['password']
    code = event['code']
    
    try:
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            ConfirmationCode=code,
            ForceAliasCreation=False
        )
        
    except client.exceptions.UserNotFoundException:
        return {"error": True, "success": False, "message": "Username doesnt exists"}
        return event
    except client.exceptions.CodeMismatchException:
        return {"error": True, "success": False, "message": "Invalid Verification code"}
        
    except client.exceptions.NotAuthorizedException:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
        
    try:
        client.admin_add_user_to_group(
                UserPoolId='us-east-2_W0Etmdx4s',
                Username=username,
                GroupName='Player'
            )
            
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
      
    return {"error": False, 
            "success": True, 
            "message": "Account Confirmed", 
            "data": None}