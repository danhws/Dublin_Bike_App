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

#API details including key, URI, Latitude and Longitude for Dublin.   Celcius variable used to convert results to degrees celcius
API = '7c6a9517ebcc29b881e9240866300f38'
Lat = '53.344'
Lon = '-6.2672'
URI = 'https://api.openweathermap.org/data/2.5/forecast' 
Celcius = 'metric'

#Connect to dBikes database.   'mycursor' used to execute database commands.
mydb = mysql.connector.connect(
  host="dbbikes.cpwzqhmscagf.eu-west-1.rds.amazonaws.com",
  user="group20",
  password="30830Group20",
  database="dBikes"
)
mycursor = mydb.cursor()

#Create a table for Weather data if one does not already exist
mycursor.execute("CREATE TABLE IF NOT EXISTS Weather (Name VARCHAR(255), Updated INT, Temperature VARCHAR(255), Max_Temp VARCHAR(255), Min_Temp VARCHAR(255), Weather VARCHAR(255), WeatherID INT)")

#Function that takes a list as an argument and will insert each element of the list into the Weather table.   7 values in the list to be inserted into the table
def insertWeather(list1):

    sql = "INSERT INTO Weather (Name, Updated, Temperature, Max_Temp, Min_temp, Weather, WeatherID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, list1)
    mydb.commit()
    return

#Main function that will request data from the API and sleep for 30 minutes.
def main():

    try:
        #Requests data from Weather API using the URI, API key, longitude, latitude and units.
        r = requests.get(URI, params = {"appid":API, "lat":Lat, "lon":Lon, "units":Celcius})
        weather=json.loads(r.text)
            
        #Takes only the data we need from the returned JSON data and stores in the list 'current'.
        current=(weather.get('city').get('name'), weather.get('list')[0].get('dt'), weather.get('list')[0].get('main').get('temp'), weather.get('list')[0].get('main').get('temp_max'), weather.get('list')[0].get('main').get('temp_min'), weather.get('list')[0].get('weather')[0].get('description'), weather.get('list')[0].get('weather')[0].get('id'))
            
        #Calls the insertWeather function using the 'current' list as the argument.
        insertWeather(current)

        #Sleep for 30 minutes until While Loop starts again
        #time.sleep(30*60)
        
        
    except:
        print(traceback.format_exc())
    
    return
    

main()


