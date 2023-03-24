#Import relevent packages
import requests
import json
import time
from datetime import datetime 
import traceback
from IPython.display import clear_output
from pprint import pprint
import pandas as pd
import mysql.connector

#API details including key and URI.
API = '2e9610b5e4e6707b43826d0aeba532d4b4c30e87'
Name = 'Dublin'
URI = 'https://api.jcdecaux.com/vls/v1/stations'

#Connect to dBikes database.   'mycursor' used to execute database commands.
mydb = mysql.connector.connect(
  host="dbbikes.cpwzqhmscagf.eu-west-1.rds.amazonaws.com",
  user="group20",
  password="30830Group20",
  database="dBikes"
)
mycursor = mydb.cursor()

#Create a table for Stations and Bikes data if one does not already exist
mycursor.execute("CREATE TABLE IF NOT EXISTS Station (Address VARCHAR(255), Bike_Stands INT, Number INT, Banking VARCHAR(255), Bonus VARCHAR(255), Latitude VARCHAR(255), Longitude VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Bikes (Address VARCHAR(255), Available_Bikes INT, Available_Stands INT, Updated INT, Status VARCHAR(255))")

#Function that takes a list as an argument and will insert each element of the list into the Station table.   7 values in the list to be inserted into the table
def insertStation(list1):
    #Check number of rows in 'Station' table
    mycursor.execute("SELECT COUNT(*) FROM Station")
    myresult = mycursor.fetchall()

    #Only write to 'Stations' table if number of rows equals the number of stations in existence (110)
    if (myresult[0][0] <= 109):
        sql = "INSERT INTO Station (Address, Bike_Stands, Number, Banking, Bonus, Latitude, Longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, list1)
        mydb.commit()
    else:
        pass
    return

#Function that takes a list as an argument and will insert each element of the list into the Bikes table.   5 values in the list to be inserted into the table
def insertBikes(list1):
    sql = "INSERT INTO Bikes (Address, Available_Bikes, Available_Stands, Updated, Status) VALUES (%s, %s, %s, %s, %s)"

    mycursor.execute(sql, list1)

    mydb.commit()
    return


#Main function that will request data from the API and sleep for 2 minutes.
def main():
    
    #Code commented out below is to clear the output in case any data was checked by printing to the output.
    #clear_output(wait=True)
    try:
        #Requests data from JCDecaux API using the URI, API key and contract name.
        r = requests.get(URI, params = {"apiKey":API, "contract":Name})
        stations=json.loads(r.text)
            
        #For loop that takes only the data we need from the returned JSON data of each station and stores in the lists 'static' or 'dynamic'. 
        for station in stations:
            static=(station.get('address'), station.get('bike_stands'), station.get('number'), station.get('banking'), station.get('bonus'), station.get('position').get('lat'), station.get('position').get('lng'))
            dynamic=(station.get('address'), station.get('available_bikes'), station.get('available_bike_stands'), int(station.get('last_update')/1000), station.get('status'))
                
            #Calls functions to write 'static' list to 'Station' table and 'dynamic' list to 'Bikes' table
            insertBikes(dynamic)
            insertStation(static)
                
        #break
        #Sleep for 2 minutes until While Loop starts again
        #time.sleep(2*60)
        
    except:
        print(traceback.format_exc())
        
    return

main()