import json
import os
import mysql.connector

mydb = mysql.connector.connect(
  host=os.environ['DB_ENDPOINT'],
  user=os.environ['MASTER_USERNAME'],
  passwd=os.environ['MASTER_PASSWORD'],
  database=os.environ['DB_NAME']
)

def lambda_handler(event, context):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT USER_ID, USER_PHONE, USER_PASSWORD, USER_NAME FROM user WHERE USER_PHONE = " + event['phone'])
    myresult = mycursor.fetchall()
    
    if (len(myresult) == 1):
        if (event['password'] == myresult[0][2]):
            return {
                    'statusCode': 200,
                    'body': json.dumps({'user_id': myresult[0][0], 'user_name': myresult[0][-1]}),
                    'message': "Login Successful"
                    }
        # this is not 1 else
    # this is without other else; abb theek hai?