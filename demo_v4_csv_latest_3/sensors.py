from adafruit_as726x import AS726x_I2C
from PySignal import Signal
from config import *
import threading
import datetime
import board
import smbus
import json
import time
import sys

class Sensor(threading.Thread):
    ColorDataSignal = Signal()
    GenDataSignal = Signal()
    AckSignal = Signal()
    def __init__(self):
        threading.Thread.__init__(self)
        print("..........................................................Sensor thread is running ....")
        #--------Other's Parameters--------#
        self.machineID = 0
        self.sampleNum = 0
        #-------Sensor's Selection --------#
        self.dataBaseTable = {0:"LED0", 1:"LED1", 2:"LED2", 3:"LED3", 4:"LED4"}
        self.LEDDet_PX_45ma_PotVal = {0:53,  1:64,  2:51,  3:64,  4:64}
        self.LEDMagPcb_MuxChn = { 0:0x01,  1:0x02,  2:0x04,  3:0x08,  4:0x10}
        self.LEDDetPcb_MuxChn = { 0:0x10,  1:0x08,  2:0x04,  3:0x02,  4:0x01}
        #-------Sensors Arry For Raw --------#
        self.Raw_List_Vio = []
        self.Raw_List_Blu = []
        self.Raw_List_Grn = []
        self.Raw_List_Yel = []
        self.Raw_List_Org = []
        self.Raw_List_Red = []
        #-------Sensors Arry For Cal --------#
        self.Cal_List_Vio = []
        self.Cal_List_Blu = []
        self.Cal_List_Grn = []
        self.Cal_List_Yel = []
        self.Cal_List_Org = []
        self.Cal_List_Red = []
        self.genData = []  # Data_Point,Sample_Num,Time_Stamp,Time_Per,Temp,Gain,Int_Time,Allowable_Dev
        #-----Sensor Parameter's-------#
        self.Gain = 64
        self.Integration_time = 700
        self.MainLED_Current = 100
        self.IndLED_Current = 8
        #------Bus's Initialization-------#
        self.bus = smbus.SMBus(1)
        self.Det_Board = 0x70
        self.Mag_Board = 0x71  
        self.i2c = board.I2C()
        self.start()  # start thread
        pass   # end of function class constructor
    def func(self):
        Sensor = 0
        self.sampleNum += 1
        brightness = 127
        while Sensor < 5:
            NumOfReadings = 0
            startTime = time.time()
            Temperature = 0
            while NumOfReadings < 6:
                try:
                    print("[INFO] : Star While Loop")
                    # - Activate P0 LED on Mag PCB Side
                    self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Sensor])
                    # - Set the value via Dictionary per specific PCB, later this needs to be in Non-Volatile Chip (Pot) Default Memory
                    self.bus.write_byte_data(0x2E,0x00, brightness) # Write to Wiper 0, Volatile
                    Vol_Wiper0 = self.bus.read_word_data(0x2E,0x0C) # Addr = 0h in Read Mode
                    print(f"LED {Sensor} Current Changed With Acknowledge Register Vol_wiper0", Vol_Wiper0)
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                    # Activate P0 LED on Det PCB Side
                    self.bus.write_byte_data(self.Det_Board,0x04, self.LEDDetPcb_MuxChn[Sensor])
                    LED_CurrentSourcePot_Val = self.LEDDet_PX_45ma_PotVal[Sensor]
                    self.bus.write_byte_data(0x2E,0x00, LED_CurrentSourcePot_Val) # Write to Wiper 0, Volatile
                    # - Read Sensor, Note: the Det Address/Mux is still selected for the proper board & position 
                    sensor = AS726x_I2C(self.i2c)
                    sensor.conversion_mode = sensor.ONE_SHOT     #.MODE_2
                    sensor.gain = self.Gain
                    sensor.driver_led_current = self.MainLED_Current
                    sensor.indicator_led_current = self.IndLED_Current
                    print("New Reading Started !!!!!!!")
                    while not sensor.data_ready:
                        time.sleep(0.1)
                    # ------- Get raw values ----- #
                    self.Raw_List_Vio.append(round(sensor.raw_violet,2))
                    self.Raw_List_Blu.append(round(sensor.raw_blue,2))
                    self.Raw_List_Grn.append(round(sensor.raw_green,2))
                    self.Raw_List_Yel.append(round(sensor.raw_yellow,2))
                    self.Raw_List_Org.append(round(sensor.raw_orange,2))
                    self.Raw_List_Red.append(round(sensor.raw_red,2))
                    # ------- Get Cal values -----#
                    self.Cal_List_Vio.append(round(sensor.violet,2))
                    self.Cal_List_Blu.append(round(sensor.blue,2))
                    self.Cal_List_Grn.append(round(sensor.green,2))
                    self.Cal_List_Yel.append(round(sensor.yellow,2))
                    self.Cal_List_Org.append(round(sensor.orange,2))
                    self.Cal_List_Red.append(round(sensor.red,2))
                    Temperature = sensor.temperature
                    #---------------------------------------------------
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Det_Board,0x04,0x00)
                    #time.sleep(.025)
                    #---------------------------------------------------
                    # - Deactive BOTH Mag & Det PCB LEDs
                    # - Turn OFF Mag 1st
                    self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Sensor])
                    self.bus.write_byte_data(0x2E,0x00,0x00)
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                     # - Turn OFF Det 2nd
                    self.bus.write_byte_data(self.Det_Board,0x04,self.LEDDetPcb_MuxChn[Sensor])
                    self.bus.write_byte_data(0x2E,0x00,0x00)
                    # - Be Safe, always disconnect the Mux until next use
                    self.bus.write_byte_data(self.Det_Board,0x04,0x00)
                    print(f"[INFO] : Reading Done With Sample Number : {NumOfReadings}")
                    NumOfReadings += 1
                except Exception as error:
                    print(error)
            # - Calculate Elapsed Time
            endTime = time.time()
            elapsedTime = endTime - startTime
            elapsedTime = round(elapsedTime,2)
            Timestamp = datetime.datetime.now() # get time spam
            print(f"Time Stamp is : {Timestamp}")
            print(f"Elapsed Time : {elapsedTime}")
            print(f"Sensor Number : {Sensor}")
            print(f"Allowable Deviation : {allowableDev}")
            self.genData.append(Sensor)  # Data_Point
            self.genData.append(self.sampleNum)  # sampleNum
            self.genData.append(str(Timestamp))  # Time Stamp
            self.genData.append(elapsedTime)  # Elapsed Time
            self.genData.append(Temperature)  # Temperature
            self.genData.append(self.Gain)  # Gain
            self.genData.append(self.Integration_time)  # Intergation Time 
            self.genData.append(allowableDev) # allowableDev
            # Print All data here
            print("Data in sensor loop......")
            print(f"General Data is : {self.genData}")
            print(f"Vio Raw : {self.Raw_List_Vio}")
            print(f"Vio Cal : {self.Cal_List_Vio}")
            print(f"Blu Raw : {self.Raw_List_Blu}")
            print(f"Blu Cal : {self.Cal_List_Blu}")
            print(f"Grn Raw : {self.Raw_List_Grn}")
            print(f"Grn Cal : {self.Cal_List_Grn}")
            print(f"Yel Raw : {self.Raw_List_Yel}")
            print(f"Yel Cal : {self.Cal_List_Yel}")
            print(f"Org Raw : {self.Raw_List_Org}")
            print(f"Org Cal : {self.Cal_List_Org}")
            print(f"Red Raw : {self.Raw_List_Red}")
            print(f"Red Cal : {self.Cal_List_Red}")
            # Send basic data to main thread in form of (self.genData)
            print("Data in main loop......")
            self.GenDataSignal.emit(self.genData)
            
            # Send Violet Raw Data
            self.ColorDataSignal.emit(self.Raw_List_Vio,"Vio","Raw")
            # Send Violet Cal Data
            self.ColorDataSignal.emit(self.Cal_List_Vio,"Vio","Cal")
            # Send Blue Raw Data
            self.ColorDataSignal.emit(self.Raw_List_Blu,"Blu","Raw")
            # Send Blue Cal Data
            self.ColorDataSignal.emit(self.Cal_List_Blu,"Blu","Cal")
            # Send Green Raw Data
            self.ColorDataSignal.emit(self.Raw_List_Grn,"Grn","Raw")
            # Send Green Cal Data
            self.ColorDataSignal.emit(self.Cal_List_Grn,"Grn","Cal")
            # Send Yellow Raw Data
            self.ColorDataSignal.emit(self.Raw_List_Yel,"Yel","Raw")
            # Send Yellow Cal Data
            self.ColorDataSignal.emit(self.Cal_List_Yel,"Yel","Cal")
            # Send Orange Raw Data
            self.ColorDataSignal.emit(self.Raw_List_Org,"Org","Raw")
            # Send Orange Cal Data
            self.ColorDataSignal.emit(self.Cal_List_Org,"Org","Cal")
            # Send Red Raw Data
            self.ColorDataSignal.emit(self.Raw_List_Red,"Red","Raw")
            # Send Red Cal Data
            self.ColorDataSignal.emit(self.Cal_List_Red,"Red","Cal")
            # Acknowledge Execution for save data in csv file
            self.AckSignal.emit(True)
            
            
            print(f"Reading is done with sensor number {Sensor} ...................................")
            self.genData = []
            #----------------------Clear Lists --------------------------#
            self.Raw_List_Vio = []
            self.Raw_List_Blu = []
            self.Raw_List_Grn = []
            self.Raw_List_Yel = []
            self.Raw_List_Org = []
            self.Raw_List_Red = []
            self.Cal_List_Vio = []
            self.Cal_List_Blu = []
            self.Cal_List_Grn = []
            self.Cal_List_Yel = []
            self.Cal_List_Org = []
            self.Cal_List_Red = []
            # -----------------------------------------------------#
            NumOfReadings = 0 # initialize for next reading start with reading number
            Sensor += 1    
        pass   # end of func function
    def run(self):
        while True:
            self.func()
        pass   # end of run function which is runing for thread
    pass # end of detectorSensor class

if __name__ == "__main__":
    sensor = Sensor()