import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json

CLIENT_ID = '5hnntk0cimpssub89b2ge6n5s3' #Gametime client ID
CLIENT_SECRET = 'l9varf6j9jc62chmvvf4e7mr5aiitdflhkliq6iga6397grot8s'

def get_secret_hash(username):
    username = str(username)
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
    
def lambda_handler(event, context):
    for field in ["phone", "email", "password", "firstname", "lastname"]:
        if not event.get(field):
            return {"error": False, "success": True, 'message': f"{field} is missing", "data": None}
    phone = event['phone']
    email = event["email"]
    password = event['password']
    firstname = event["firstname"]
    lastname = event["lastname"]
    
    client = boto3.client('cognito-idp')
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(phone),
            Username=str(phone),
            Password=password, 
            UserAttributes=[
            {
                'Name': "phone_number",
                'Value': phone
            },
            {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "given_name",
                'Value': firstname
            },
            {
                'Name': "family_name",
                'Value': lastname
            }], 
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            }
        ])
    
    except client.exceptions.UsernameExistsException as e:
        return {"error": False, 
               "success": True, 
               "message": "This phone number already exists", 
               "data": None}
               
    except client.exceptions.InvalidPasswordException as e:
        return {"error": False, 
               "success": True, 
               "message": "Password should have Caps,\
                          Special chars, Numbers", 
               "data": None}
               
    except client.exceptions.UserLambdaValidationException as e:
        return {"error": False, 
               "success": True, 
               "message": "Email already exists", 
               "data": None}
    
    except Exception as e:
        return {"error": False, 
                "success": True, 
                "message": str(e), 
               "data": None}
    
    return {"error": False, 
            "success": True, 
            "message": "Check Verification Email", 
            "data": None}