#RSL - created this program 7/12/22
# this module reads the rainfall gauge
# the count (button pressed) only increments on the "up" of the water arm


from gpiozero import Button
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
    print (tip_count * BUCKET_SIZE)
    return

rain_sensor.when_pressed = bucket_tipped





 

