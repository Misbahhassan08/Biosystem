from adafruit_as726x import AS726x_I2C
from dataBase import DataBase
import threading
import datetime
import board
import smbus
import json
import time
import sys

class Sensor(threading.Thread):
    dataBase = DataBase()
    def __init__(self):
        threading.Thread.__init__(self)
        self.machineID = 0
        self.dataBaseTable = {0:"LED0", 1:"LED1", 2:"LED2", 3:"LED3", 4:"LED4"}
        self.LEDDet_PX_45ma_PotVal = {0:53,  1:64,  2:51,  3:64,  4:64}
        self.LEDMagPcb_MuxChn = { 0:0x01,  1:0x02,  2:0x04,  3:0x08,  4:0x10}
        self.LEDDetPcb_MuxChn = { 0:0x10,  1:0x08,  2:0x04,  3:0x02,  4:0x01}
        self.Gain = 64
        self.Integration_time = 700
        self.MainLED_Current = 100
        self.IndLED_Current = 8
        self.bus = smbus.SMBus(1)
        self.Det_Board = 0x70
        self.Mag_Board = 0x71  
        self.i2c = board.I2C()
        pass   # end of function class constructor
    def run(self):
        while True:
            Sensor = 0
            brightness = 127
            while Sensor < 5:
                try:
                    print("Star: While Loop")
                    # - Activate P0 LED on Mag PCB Side
                    self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Sensor])
                    time.sleep(.1)
                    # - Set the value via Dictionary per specific PCB, later this needs to be in Non-Volatile Chip (Pot) Default Memory
                    self.bus.write_byte_data(0x2E,0x00, brightness) # Write to Wiper 0, Volatile
                    time.sleep(.1)
                    Vol_Wiper0 = self.bus.read_word_data(0x2E,0x0C) # Addr = 0h in Read Mode
                    time.sleep(.1)
                    print(f"LED {Sensor} Current Changed With Acknowledge Register Vol_wiper0", Vol_Wiper0)
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                    time.sleep(0.25)
                    # Activate P0 LED on Det PCB Side
                    self.bus.write_byte_data(self.Det_Board,0x04, self.LEDDetPcb_MuxChn[Sensor])
                    time.sleep(0.25)
                    LED_CurrentSourcePot_Val = self.LEDDet_PX_45ma_PotVal[Sensor]
                    self.bus.write_byte_data(0x2E,0x00, LED_CurrentSourcePot_Val) # Write to Wiper 0, Volatile
                    time.sleep(0.25)
                    # - Read Sensor, Note: the Det Address/Mux is still selected for the proper board & position 
                    sensor = AS726x_I2C(self.i2c)
                    time.sleep(.1)
                    sensor.conversion_mode = sensor.ONE_SHOT     #.MODE_2
                    sensor.gain = self.Gain
                    sensor.driver_led_current = self.MainLED_Current
                    sensor.indicator_led_current = self.IndLED_Current
                    print("New Reading Started !!!!!!!")
                    while not sensor.data_ready:
                        time.sleep(0.3)
                    Violet = sensor.violet
                    Blue = sensor.blue
                    Green = sensor.green
                    Yellow = sensor.yellow
                    Orange = sensor.orange
                    Red = sensor.red
                    Temperature = sensor.temperature
                    Timestamp = datetime.datetime.now() # get time spam
                    #---------------------------------------------------
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Det_Board,0x04,0x00)
                    time.sleep(.025)
                    #---------------------------------------------------
                    # - Deactive BOTH Mag & Det PCB LEDs
                    # - Turn OFF Mag 1st
                    self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Sensor])
                    time.sleep(.1)
                    self.bus.write_byte_data(0x2E,0x00,0x00)
                    time.sleep(.025)
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                     # - Turn OFF Det 2nd
                    time.sleep(.025)
                    self.bus.write_byte_data(self.Det_Board,0x04,self.LEDDetPcb_MuxChn[Sensor])
                    time.sleep(.025)
                    self.bus.write_byte_data(0x2E,0x00,0x00)
                    time.sleep(.025)
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Det_Board,0x04,0x00)
                    time.sleep(1)
                    self.dataBase.insertData(Violet,Blue,Green,Yellow,Orange,Red,Temperature,Timestamp,self.dataBaseTable[Sensor])
                    print(f"Table Name is : {self.dataBaseTable[Sensor]}")
                    print(f"End : While Loop {Sensor}")
                    print(Timestamp)
                    Timestamp = None
                    Sensor += 1
                except Exception as error:
                    print(error)
        pass   # end of func function
    pass # end of detectorSensor class

if __name__ == "__main__":
    sensor = Sensor()
    sensor.start()