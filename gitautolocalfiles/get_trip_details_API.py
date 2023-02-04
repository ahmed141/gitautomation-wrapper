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
    else:
        statusCode = 200
        message = "Requested trip id do not have any driver record"
        
        response['driver_id'] = myresult1[0][0]
        response['driver_name'] = myresult1[0][1]
        response['trip_fare'] = myresult1[0][2]
        response['ride_capacity']= myresult1[0][3]
        response['trip_source'] =  myresult1[0][6]
        response['trip_destination'] =  myresult1[0][7]
        response['trip_datetime'] =  str(myresult1[0][4])
        response['driver_picture'] = myresult1[0][5]
        query2 = "SELECT AVG(REVIEW_SCORE) AS AVERAGE, COUNT(0) AS COUNT from trip_review WHERE TRIP_ID IN (SELECT t2.TRIP_ID FROM user AS t1, trip AS t2 WHERE t1.USER_ID = t2.DRIVER_ID AND t2.DRIVER_ID = {}) GROUP BY TRIP_ID;".format(response['driver_id'])
        mycursor.execute(query2)
        myresult2 = mycursor.fetchall()
        if len(myresult2) > 0:
            statusCode = 201
            response['driver_rating'] = float(myresult2[0][0])
            response['driver_trips_count'] = myresult2[0][1]
            message = "Successfully retrieved results for requested trip and driver id"
    
    return {
        'statusCode': statusCode,
        'body': json.dumps({'response': response, 'message': message})
    }
    