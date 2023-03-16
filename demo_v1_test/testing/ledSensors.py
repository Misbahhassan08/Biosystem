import time
import smbus
import board
from adafruit_as726x import AS726x_I2C
class Testing:
    def __init__(self):
        self.LEDMag_PX_45ma_PotVal = {0:64,  1:64,  2:64,  3:64,  4:64} 
        self.LEDDet_PX_45ma_PotVal = {0:53,  1:64,  2:51,  3:64,  4:64}
        self.LEDMagPcb_MuxChn = { 0:0x01,  1:0x02,  2:0x04,  3:0x08,  4:0x10}
        self.LEDDetPcb_MuxChn = { 0:0x10,  1:0x08,  2:0x04,  3:0x02,  4:0x01}
        self.violetValues = 0
        self.blueValues = 0
        self.greenValues = 0
        self.yellowValues = 0
        self.orangeValues = 0
        self.redValues = 0
        self.Gain = 16
        self.Integration_time = 700
        self.MainLED_Current = 25
        self.IndLED_Current = 1
        self.bus = smbus.SMBus(1)
        self.Det_Board = 0x70
        self.Mag_Board = 0x71  
        self.i2c = board.I2C()
        pass   # end of function class constructor
    def getColorAvg(self,color,value,counts): # color name in string
        if color == "violet" and counts < 10:
            self.violetValues += value
            print(f"{color} color value is : {value}")
        elif color == "blue" and counts < 10:
            self.blueValues += value
            print(f"{color} color value is : {value}")
        elif color == "green" and counts < 10:
            self.greenValues += value
            print(f"{color} color value is : {value}")
        elif color == "yellow" and counts < 10:
            self.yellowValues += value
            print(f"{color} color value is : {value}")
        elif color == "orange" and counts < 10:
            self.orangeValues += value
            print(f"{color} color value is : {value}")
        elif color == "red" and counts < 10:
            self.redValues += value
            print(f"{color} color value is : {value}")
        if counts == 9 and color == "violet": 
            violetAvg = self.violetValues/10
            self.violetValues = 0
            return violetAvg
        elif counts == 9 and color == "blue": 
            blueAvg = self.blueValues/10
            self.blueValues = 0
            return blueAvg
        elif counts == 9 and color == "green": 
            greenAvg = self.greenValues/10
            self.greenValues = 0
            return greenAvg
        elif counts == 9 and color == "yellow": 
            yellowAvg = self.yellowValues/10
            self.yellowValues = 0
            return yellowAvg
        elif counts == 9 and color == "orange": 
            orangeAvg = self.orangeValues/10
            self.orangeValues = 0
            return orangeAvg
        elif counts == 9 and color == "red": 
            redAvg = self.redValues/10
            self.redValues = 0
            return redAvg
        else:
            return None
        
        pass   # end of colorAvg function
    def func(self,Position):
        countSamples = 0
        while countSamples < 10:
            try:
                print("Star: While Loop")
                # - Activate P0 LED on Mag PCB Side
                self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Position])
                time.sleep(.5)
                # - Set the value via Dictionary per specific PCB, later this needs to be in Non-Volatile Chip (Pot) Default Memory
                LED_CurrentSourcePot_Val = self.LEDMag_PX_45ma_PotVal[Position]
                self.bus.write_byte_data(0x2E,0x00, LED_CurrentSourcePot_Val) # Write to Wiper 0, Volatile
                time.sleep(.5)
                # - Be Safe, always disconnect the Mux until next use
                self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                time.sleep(.1)
                # Activate P0 LED on Det PCB Side
                self.bus.write_byte_data(self.Det_Board,0x04, self.LEDDetPcb_MuxChn[Position])
                time.sleep(.1)
                LED_CurrentSourcePot_Val = self.LEDDet_PX_45ma_PotVal[Position]
                self.bus.write_byte_data(0x2E,0x00, LED_CurrentSourcePot_Val) # Write to Wiper 0, Volatile
                time.sleep(.1)
                # - Read Sensor, Note: the Det Address/Mux is still selected for the proper board & position 
                sensor = AS726x_I2C(self.i2c)
                time.sleep(.1)
                sensor.conversion_mode = sensor.ONE_SHOT     #.MODE_2
                sensor.gain = 64
                sensor.driver_led_current = 100
                sensor.indicator_led_current = 8
                print("New Reading Started !!!!!!!")
                while not sensor.data_ready:
                    time.sleep(0.5)
                violet_cv = sensor.violet
                blue_cv = sensor.blue
                green_cv = sensor.green
                yellow_cv = sensor.yellow
                orange_cv = sensor.orange
                red_cv = sensor.red
                #---------------------------------------------------
                # - Be Safe, always disconnect the Mux until next use
                self.bus.write_byte_data(self.Det_Board,0x04,0x00)
                time.sleep(.1)
                #---------------------------------------------------
                # - Deactive BOTH Mag & Det PCB LEDs
                # - Turn OFF Mag 1st
                self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Position])
                time.sleep(.1)
                self.bus.write_byte_data(0x2E,0x00,0x00)
                time.sleep(.1)
                # - Be Safe, always disconnect the Mux until next use
                self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                 # - Turn OFF Det 2nd
                time.sleep(.1)
                self.bus.write_byte_data(self.Det_Board,0x04,self.LEDDetPcb_MuxChn[Position])
                time.sleep(.1)
                self.bus.write_byte_data(0x2E,0x00,0x00)
                time.sleep(.1)
                # - Be Safe, always disconnect the Mux until next use
                self.bus.write_byte_data(self.Det_Board,0x04,0x00)
                violet_Avg = self.getColorAvg("violet",violet_cv,countSamples)
                blue_Avg = self.getColorAvg("blue",blue_cv,countSamples)
                green_Avg = self.getColorAvg("green",green_cv,countSamples)
                yellow_Avg = self.getColorAvg("yellow",yellow_cv,countSamples)
                orange_Avg = self.getColorAvg("orange",orange_cv,countSamples)
                red_Avg = self.getColorAvg("red",red_cv,countSamples)
                if countSamples == 9:
                    print(f" Violet Color Average is : {violet_Avg}")
                    print(f" Blue Color Average is : {blue_Avg}")
                    print(f" Green Color Average is : {green_Avg}")
                    print(f" Yellow Color Average is : {yellow_Avg}")
                    print(f" Orange Color Average is : {orange_Avg}")
                    print(f" Red Color Average is : {red_Avg}")
                print("End : While Loop " + str(countSamples))
                countSamples += 1
            except Exception as error:
                print(error)
        pass   # end of func function
    pass # end of functions class

if __name__ == "__main__":
    testing = Testing()
    testing.func(0)

