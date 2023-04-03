#RSL - created this program 7/13/22
# this module reads the wind speed as a button each turn

# NOTE: I found that with no adjustment value, my meter was giving
# the expected values, but the project suggests that an adjustment
# of 1.18 may be needed to compensate for wind energy loss

import math
import time
import statistics

store_speeds = []

CM_PER_KM = 100000.0
SECS_PER_HR = 3600

RADIUS = 9.0  #radius of anemometer for wind speed calcuation
CIRCUM = (2* math.pi) * RADIUS
wind_interval = 5  # how often to report in secs - this is for calculating a gust
speed_interval = 60 # how often to clear the array so wind speed isnt' measured over an infinite window

from gpiozero import Button
wind_count = 0


wind_speed_sensor = Button(5)

def reset_wind():
     global wind_count
     wind_count =0
     print ("wind RESET")
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

speed_start_time = time.time()

# Infinite loop to calculate gust and windspeed
# NOTE: the gust is over 5 secs
# NOTE: the wind speed is the mean of ALL values in the array which seems
#       like it's wrong to me - i.e., if the meter stops, then speed
#       will never calculate to zero no matter how long it is stopped
#       OR bascially not wrong - it just uses an infitnie window for calulating the wind speed
#       and then a 5 sec window for gust speed
#      TODO: won't using an infinite window cause and out of memory issue since we are grwoing the array forever?
while True:

    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        time.sleep(wind_interval)
        final_speed = calc_wind_speed(wind_interval)
        store_speeds.append(final_speed)

    wg = max(store_speeds)
    if wg > wind_gust: wind_gust = wg
    
    wind_speed = statistics.mean(store_speeds)
    print("wind speed= ", wind_speed, "gust= ", wind_gust, "km/hr")

    #RSL: adding some code to clear out the store_speeds array periodically
    #to 1. prevent overflow and also to define a widow for calc of wind speed instead of infinite window
    if time.time() - speed_start_time >= speed_interval:
       store_speeds.clear()
       speed_start_time = time.time()
       print("reset speed window")
       



     
     







 

