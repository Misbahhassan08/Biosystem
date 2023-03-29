from sensors import Sensor             
import datetime
import keyboard
import board
import smbus
import json
import time
import sys

class Main:
    sensor = Sensor()
    def __init__(self):
        self.machineID = 0
        pass   # end of Main class constructor
    def func(self):
        self.sensor.func()
        pass  # end of Main class

if __name__ == "__main__":
    main = Main()
    main.func()