
#RSL: created this file 7-28-22 
#it is meant to just test the wind direction module to see if it's connected and working
#this is not the final program to determine wind direction

from gpiozero import MCP3008
import time
import math
adc = MCP3008(channel=0)

print("adc.value = ", adc.value)

values = []
count = 0

volts = {0.4: 0.0,
         1.4: 22.5,
         1.2: 45.0,
         2.8: 67.5,
         2.7: 90.0,
         2.9: 112.5,
         2.2: 135.0,
         2.5: 157.5,
         1.8: 180.0,
         2.0: 202.5,
         0.7: 225.0,
         0.8: 247.5,
         0.1: 270.0,
         0.3: 292.5,
         0.2: 315.0,
         0.6: 337.5}

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





while True:
  wind = round(adc.value*3.3,1)
  if not wind in volts:
     print ("unknown value: ", str(wind))
  else:
     print ("Match : ", str(wind), " ", str(volts[wind]), " Dir: ", str(str_directions[wind]))
     
   



