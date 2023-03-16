from adafruit_as726x import AS726x_I2C
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import threading
import datetime
import board
import smbus
import json
import time
import sys

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering

class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.detectorsensor = detectorSensor()
        self.client = mqtt.Client()
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.subscribe("biogas_/detectorFlow_/test_/")
        self.machineId = 0
        self.brightness = None
        self.parsed_json = None
        self.msgTopic = None
        pass   # end of Main class constructor
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        pass   # end of on_connect function
    def on_message(self,client, userdata, msg):
        print("subscribed")
        self.msgTopic = msg.topic
        self.parsed_json = json.loads(msg.payload)
        if self.parsed_json['ID'] == self.machineId:
            self.brightness = self.parsed_json['Brightness']
            print(self.brightness)
            #time.sleep(0.01)
        pass    # end of om_message function
    def func(self):
        while True:
            if self.msgTopic == "biogas_/detectorFlow_/test_/":
                sensor=4
                while sensor < 5:
                    startTime = datetime.datetime.now() # get start time
                    t1 = startTime.timestamp()
                    self.detectorsensor.func(sensor,self.brightness)  # brightness van be very between 0-127
                    endTime = datetime.datetime.now() # get end time
                    t2 = endTime.timestamp()
                    executTime = t2-t1
                    if self.detectorsensor.dicColorData is not None:
                        color = self.detectorsensor.dicColorData
                        color["Time"] = executTime # add time in json file
                        color = json.dumps(color)
                        self.client.publish("biogas_/color_/data_/",color)
                    sensor += 1
                self.brightness = None
                self.msgTopic = None
            else:
                pass
        pass   # end of func function
    def run(self):
        print("thread is running")
        self.client.loop_forever()
        pass   # end of run function which is running in thread for mqtt
    pass   # end of Main class
"""
class dcMotor:
    def __init__(self):
        pass   # end of dcMotor class constructor
    pass   # end of dcMotor class
"""
class detectorSensor:
    def __init__(self):
        #self.LEDMag_PX_45ma_PotVal = {0:64,  1:64,  2:64,  3:64,  4:64}
        self.machineId = 0
        self.LEDDet_PX_45ma_PotVal = {0:53,  1:64,  2:51,  3:64,  4:64}
        self.LEDMagPcb_MuxChn = { 0:0x01,  1:0x02,  2:0x04,  3:0x08,  4:0x10}
        self.LEDDetPcb_MuxChn = { 0:0x10,  1:0x08,  2:0x04,  3:0x02,  4:0x01}
        self.dicColorData = None
        self.violet_Avg = 0
        self.blue_Avg = 0
        self.green_Avg = 0
        self.yellow_Avg = 0
        self.orange_Avg = 0
        self.red_Avg = 0
        self.Gain = 64
        self.Integration_time = 700
        self.MainLED_Current = 100
        self.IndLED_Current = 8
        self.bus = smbus.SMBus(1)
        self.Det_Board = 0x70
        self.Mag_Board = 0x71  
        self.i2c = board.I2C()
        pass   # end of function class constructor
    def func(self,Sensor,brightness):
        countSamples = 0
        while countSamples < 6:
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
                violet_cv = sensor.violet
                blue_cv = sensor.blue
                green_cv = sensor.green
                yellow_cv = sensor.yellow
                orange_cv = sensor.orange
                red_cv = sensor.red
                temperature = sensor.temperature
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
                self.violet_Avg += violet_cv
                self.blue_Avg += blue_cv
                self.green_Avg += green_cv
                self.yellow_Avg += yellow_cv
                self.orange_Avg += orange_cv
                self.red_Avg += red_cv
                if countSamples == 5:
                    self.violet_Avg = self.violet_Avg/6
                    self.blue_Avg = self.blue_Avg/6
                    self.green_Avg = self.green_Avg/6
                    self.yellow_Avg = self.yellow_Avg/6
                    self.orange_Avg = self.orange_Avg/6
                    self.red_Avg = self.red_Avg/6
                    # making dic for json conversion
                    self.dicColorData = {
                                   "MachineID":self.machineId,
                                   "Sensor":Sensor,
                                   "Chip Temperature":temperature,
                                   "Time":0,
                                   "Violet":self.violet_Avg,
                                   "Blue":self.blue_Avg,
                                   "Green":self.green_Avg,
                                   "Yellow":self.yellow_Avg,
                                   "Orange":self.orange_Avg,
                                   "Red":self.red_Avg
                                    }
                    ## set values to default value
                    self.violet_Avg = 0
                    self.blue_Avg = 0
                    self.green_Avg = 0
                    self.yellow_Avg = 0
                    self.orange_Avg = 0
                    self.red_Avg = 0
                print("End : While Loop " + str(countSamples))
                countSamples += 1
            except Exception as error:
                print(error)
        pass   # end of func function
    pass # end of detectorSensor class

if __name__ == "__main__":
    main = Main()
    main.start()
    main.func()