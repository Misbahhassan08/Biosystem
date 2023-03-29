from adafruit_as726x import AS726x_I2C
import board
import smbus
import time
import sys

class Sensor:
    def __init__(self):
        self.dataBaseTable = {0:"LED0", 1:"LED1", 2:"LED2", 3:"LED3", 4:"LED4"}
        self.LEDDet_PX_45ma_PotVal = {0:53,  1:64,  2:51,  3:64,  4:64}
        self.LEDMagPcb_MuxChn = { 0:0x01,  1:0x02,  2:0x04,  3:0x08,  4:0x10}
        self.LEDDetPcb_MuxChn = { 0:0x10,  1:0x08,  2:0x04,  3:0x02,  4:0x01}
        #-------Sensors Arry Cal--------#
        self.Cal_List_Vio = []
        self.Cal_List_Blu = []
        self.Cal_List_Grn = []
        self.Cal_List_Yel = []
        self.Cal_List_Org = []
        self.Cal_List_Red = []
        self.Temp = []
        #------ Sensors Arry Raw -------#
        self.Raw_List_Vio = []
        self.Raw_List_Blu = []
        self.Raw_List_Grn = []
        self.Raw_List_Yel = []
        self.Raw_List_Org = []
        self.Raw_List_Red = []
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
        pass   # end of function class constructor
    def func(self):
        Sensor = 0
        brightness = 127
        while Sensor < 1:
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
                    time.sleep(0.3)
                # ------ Calibrated Values ------ #
                self.Cal_List_Vio.append(round(sensor.violet,2))
                self.Cal_List_Blu.append(round(sensor.blue,2))
                self.Cal_List_Grn.append(round(sensor.green,2))
                self.Cal_List_Yel.append(round(sensor.yellow,2))
                self.Cal_List_Org.append(round(sensor.orange,2))
                self.Cal_List_Red.append(round(sensor.red,2))
                self.Temp.append(sensor.temperature)
                # ----------Raw Values ---------- #
                self.Raw_List_Vio.append(round(sensor.raw_violet,2))
                self.Raw_List_Blu.append(round(sensor.raw_blue,2))
                self.Raw_List_Grn.append(round(sensor.raw_green,2))
                self.Raw_List_Yel.append(round(sensor.raw_yellow,2))
                self.Raw_List_Org.append(round(sensor.raw_orange,2))
                self.Raw_List_Red.append(round(sensor.raw_red,2))
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
                print(f"[INFO] : Reading Done With Sensor Number : {Sensor}")
                Sensor += 1
            except Exception as error:
                print(error)
        print("Calibrated Values.............................................................")
        print(f"Violet : {self.Cal_List_Vio}")
        print(f"Blue : {self.Cal_List_Blu}")
        print(f"Green : {self.Cal_List_Grn}")
        print(f"Yellow : {self.Cal_List_Yel}")
        print(f"Orange : {self.Cal_List_Org}")
        print(f"Red : {self.Cal_List_Red}")
        print("Raw Values.....................................................................")
        print(f"Violet : {self.Raw_List_Vio}")
        print(f"Blue : {self.Raw_List_Blu}")
        print(f"Green : {self.Raw_List_Grn}")
        print(f"Yellow : {self.Raw_List_Yel}")
        print(f"Orange : {self.Raw_List_Org}")
        print(f"Red : {self.Raw_List_Red}")
        print("Temperature Values.....................................................................")
        print(self.Temp)
        pass   # end of func function
    pass # end of detectorSensor class

if __name__ == "__main__":
    sensor = Sensor()
    sensor.func()
