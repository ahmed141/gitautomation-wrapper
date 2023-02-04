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
    statusCode = None
    response = {}
    message = None
    
    request_body = event["queryStringParameters"]
    
    query1 = "SELECT USER_NAME, USER_CNIC, USER_EMAIL, USER_DOB, AVATAR_URL FROM user WHERE USER_ID = {};".format(int(request_body['user_id']))
    query2 = "SELECT AVG(REVIEW_SCORE) AS AVERAGE, COUNT(0) AS COUNT from trip_review WHERE TRIP_ID IN (SELECT t2.TRIP_ID FROM user AS t1, trip AS t2 WHERE t1.USER_ID = t2.DRIVER_ID AND t2.DRIVER_ID = {}) GROUP BY TRIP_ID;".format(int(request_body['user_id']))

    mycursor = mydb.cursor()
    mycursor.execute(query1)
    myresult1 = mycursor.fetchall()
    
    
    
    if len(myresult1) == 0:
            response = -1
            message = "No record found for requested user id"
            statusCode = 400
    # Else gon- Chaloo ji
    
    return {
        'statusCode': statusCode,
        'body': json.dumps({'response': response, 'message': message})
    }
    