#RSL - created this program 7/28/22
# this module reads the wind speed as a button each turn

# NOTE: I found that with no adjustment value, my meter was giving
# the expected values, but the project suggests that an adjustment
# of 1.18 may be needed to compensate for wind energy loss

import database
import math
import time
from datetime import datetime
from datetime import date
import pytz  #for time conversions
import statistics
from gpiozero import Button
from gpiozero import MCP3008
import bme280_sensor
#import vane_test.py - putting code inline here
import statistics
import ds18b20_therm

def print_time():
     today = date.today()
     # Textual month, day and year	
     d2 = today.strftime("%B %d, %Y")
     tz_LA = pytz.timezone('America/Los_Angeles') 
     datetime_LA = datetime.now(tz_LA)
     print("Los Angeles date/time:", d2, datetime_LA.strftime("%H:%M:%S"))
     return

# These are key values for controlling collection intervals
wind_interval = 5  # how often to report in secs - this is for calculating a gust
speed_interval = 10 # how often to clear the array so wind speed isnt' measured over an infinite window
overall_interval = 15 # how often to write to file and clear all stats

#rain fall values
tip_count = 0
BUCKET_SIZE= 0.2794  #the amount of water in mm to make it tip
rain_sensor = Button(6)

def reset_rainfall():
     global tip_count
     tip_count = 0
     return

def bucket_tipped():
    global tip_count
    tip_count +=1
    # print (tip_count * BUCKET_SIZE) 
    return

#this is for winddirection sensor
adc = MCP3008(channel=0)  

#wind speed
store_speeds = []

# Wind direction
# N=270, E=0, S=90, W=180 - i think ! - these are gueses, I didnt actually check
# with a real compass, so maybe all are rotated
str_directions = {0.4: "East",
         1.4: "ES-1",
         1.2: "ES-2",
         2.8: "ES-3",
         2.7: "South",
         2.9: "SW-1",
         2.2: "SW-2",
         2.5: "SW-3",
         1.8: "West",
         2.0: "WN-1",
         0.7: "WN-2",
         0.8: "WN-3",
         0.1: "North",
         0.3: "NE-1",
         0.2: "NE-2",
         0.6: "NE-3"}

CM_PER_KM = 100000.0
SECS_PER_HR = 3600

RADIUS = 9.0  #radius of anemometer for wind speed calcuation
CIRCUM = (2* math.pi) * RADIUS

from gpiozero import Button
wind_count = 0


wind_speed_sensor = Button(5)

def reset_wind():
     global wind_count
     wind_count =0
     # print ("wind RESET")
     return

def spin():
    global wind_count
    wind_count +=1
    # print ("wind spin ", wind_count)
    return

def calc_wind_speed(time_secs):
     global wind_count
     rotations = wind_count / 2.0   # there are 2 button activations per rotation
     dist = (CIRCUM * rotations) / CM_PER_KM
     speed = (dist / time_secs) * SECS_PER_HR
     return speed


wind_speed_sensor.when_pressed = spin
wg = 0
wind_gust = 0

temp_probe = ds18b20_therm.DS18B20()
rain_sensor.when_pressed = bucket_tipped  #initiate collection of rain
speed_start_time = time.time()

#connect to DB to store out data
db = database.weather_database()

# Infinite loop to calculate gust and windspeed

print ("Welcome to Weather Station - Beginning Data Collection")
print_time()
print ("-------------------------------------------------------")
print ("Collection interval is ", overall_interval/60, " mins.")
print ("Wind gust interval is ", round(wind_interval/60,2), " mins.")
print ("Wind speed interval is ", round(speed_interval/60,2), " mins.")
print ("-------------------------------------------------------")
print(" ")
while True:

     collection_time = time.time()
     #print ("*****")
     #print ("Beginning new collection period.")
     #print ("*****")
     while time.time() - collection_time <= overall_interval:
         
         start_time = time.time()
         while time.time() - start_time <= wind_interval:
             reset_wind()
             time.sleep(wind_interval)
             final_speed = calc_wind_speed(wind_interval)
             store_speeds.append(final_speed)

         wg = max(store_speeds)
         if wg > wind_gust: wind_gust = wg
         
         

         
     print ("*****")
     print ("Ended collection period...writing values to file and clearing")
     print_time()
     #Now write the values for the current collection period to the database
     #and clear all values


     #calculate the values for the period
     wind_speed = statistics.mean(store_speeds)
     wind_direction = round(adc.value*3.3,1)
     rain_fall = tip_count * BUCKET_SIZE
     hum, pres, temp = bme280_sensor.read_all()
     temperature = temp_probe.read_temp()

     #Print the values for the period
     print("wind speed (km/hr)= ", wind_speed, "gust= ", wind_gust)
     
     if wind_direction in str_directions:
         print("wind dir val= ", wind_direction, "  wind dir: ", str_directions[wind_direction])
     else:
         print("Undefined wind direction")
         
     print("rainfail (in) = ", rain_fall)

     print("hum= ", round(hum,2), " pres= ", round(pres,2), " temp= ", round(temp,2))

     print ("gnd temp (C)= ", temperature)

     #write values for the period to database
     db.insert(temp, temperature, 0, pres, hum, wind_direction, wind_speed, wind_gust, rain_fall)



     #clear values to start next period
     #adding some code to clear out the store_speeds array periodically
     #to 1. prevent overflow and also to define a window for calc of wind speed instead of infinite window
     if time.time() - speed_start_time >= speed_interval:
            store_speeds.clear()
            speed_start_time = time.time()
            # print("reset speed window")
     
     wind_gust = 0
     reset_rainfall()
     print ("Successfully saved data and reset for new period.")
     print("*****")
     print(" ")

     
     
     



     
     







 

