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
    print(event)
    statusCode = None
    response = {}
    message = None
    # request_body = event["queryStringParameters"]
    
    query1 = 'Halwa tey nai na fer'
    
    #query gone - hun theek en?
  
    mycursor = mydb.cursor()
    mycursor.execute(query1)
    myresult1 = mycursor.fetchall()  
    
    if len(myresult1) == 0:
            response = -1
            message = "No record found for requested trip id"
            statusCode = 400
    # else gone? ok?
    
    return {
        'statusCode': statusCode,
        'body': json.dumps({'response': response, 'message': message})
    }
    