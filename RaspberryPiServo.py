#!/usr/bin/env python3

from gpiozero import Servo
from time import sleep
import pyrebase

"""
    Get motion changes from Firebase database and move the camera accordingly 
"""


def get_angles(database, pos_x, pos_y):
    new_pos_x, new_pos_y = database.child("RotateX").get().val() - 90, database.child("RotateY").get().val() - 90

    if -100 <= (new_pos_x * 100) <= 100 and -100 <= (new_pos_y * 100) <= 100:
        pos_x, pos_y = new_pos_x, new_pos_y

    return pos_y, pos_x


if __name__ == '__main__':

    servo_top = Servo(17, 0)
    servo_dwn = Servo(27, 0)

    config = {
        "apiKey": "AIzaSyAtqUNvc_wjSdkxpQEdB51VkjIbbNLorfI",
        "authDomain": "followhead-162c7.firebaseapp.com",
        "databaseURL": "https://followhead-162c7.firebaseio.com/",
        "storageBucket": "followhead-162c7.appspot.com",
        "serviceAccount": "followhead-162c7-a18ea1a607e5.json"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    sleep(1) # Needed with our hardware for the initial setup

    while True:
        prev_y, prev_x = servo_top.value, servo_dwn.value
        new_y, new_x = get_angles(db, prev_x, prev_y)
        if new_y != prev_y:
            servo_top.value = new_y
        if new_x != prev_x:
            servo_dwn.value = new_x
        sleep(0.5)
