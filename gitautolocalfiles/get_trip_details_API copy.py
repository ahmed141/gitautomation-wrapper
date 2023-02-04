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
    request_body = event["queryStringParameters"]
    
    query1 = """SELECT t1.DRIVER_ID, t2.USER_NAME, t1.FARE, t1.SEATS_COUNT, t1.START_DATETIME, t2.AVATAR_URL, 
    (SELECT CITY_NAME FROM city WHERE CITY_ID = t1.FROM_ID) as FROM_CITY,
    (SELECT CITY_NAME FROM city WHERE CITY_ID = t1.TO_ID) as TO_CITY
    
    FROM trip as t1, user as t2 WHERE (t1.DRIVER_ID = t2.USER_ID) AND (t1.TRIP_ID= {})
    ;""".format(int(request_body['trip_id']))
    
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
    