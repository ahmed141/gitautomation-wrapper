import json
import os
import mysql.connector
import boto3
import random

sns = boto3.client('sns')

mydb = mysql.connector.connect(
  host=os.environ['DB_ENDPOINT'],
  user=os.environ['MASTER_USERNAME'],
  passwd=os.environ['MASTER_PASSWORD'],
  database=os.environ['DB_NAME']
)

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    number = request_body['phone']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT USER_ID, USER_PHONE, USER_PASSWORD, USER_NAME FROM user WHERE USER_PHONE = " + number)
    myresult = mycursor.fetchall()
    
    if (len(myresult) == 0):
        
        otp_code = random.randrange(1000, 9999, 1)
        sns_response = sns.publish(PhoneNumber = number, Message='rode: ' + str(otp_code) + ' is your 4-digit code to verify your phone number.')
        if sns_response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                    'statusCode': 401,
                    'body': json.dumps({'response': -1, 'message': "Error occured while sending OTP"}),
                    
                    }
        # Chalo ji kesa dia? nai dia acha?
            
    # another else gone...
    # what? oopsie