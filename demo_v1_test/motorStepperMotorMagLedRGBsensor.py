from adafruit_as726x import AS726x_I2C
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import threading
import random
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
        self.dcmotor = dcMotor()
        self.nlmotor = nLmotor()
        self.RGBsensor = RGB_Sensor()
        self.client = mqtt.Client()
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.subscribe("biogas/dcMotor_/test_/")
        self.client.subscribe("biogas/stepper_/test_/")
        self.client.subscribe("biogas/rgbSensor_/setValue_/")
        self.parsed_json = None
        self.msgTopic = None
        self.Sensor = None
        self.Brightness = None
        #self.start()
        pass   # end of ledControl class constructor
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        pass   # end of on_connect function
    def on_message(self,client, userdata, msg):
        print("subscribed")
        self.msgTopic = msg.topic
        print(self.msgTopic)
        self.parsed_json = json.loads(msg.payload)
        if self.msgTopic == "biogas/dcMotor_/test_/":
            print("motor data received")
            self.dcmotor.varSpeedDutyCycle = self.parsed_json["speed"]
            self.dcmotor.motor_is_start =  self.parsed_json["Motor"]
            if self.parsed_json["Motor"]:
                print("Motor is ON")
            else:
                print("Motor is OFF")
            self.msgTopic = None
        elif self.msgTopic == "biogas/stepper_/test_/":
            self.nlmotor.rotvalue = self.parsed_json["stepper"]
            self.nlmotor.check = True
        elif self.msgTopic == "biogas/rgbSensor_/setValue_/":
            self.Sensor = self.parsed_json["Sensor"]
            self.Brightness = self.parsed_json["Brightness"]
            self.msgTopic = None
        else:
            pass
        pass   # end of on_message function
    def run(self):
        print("thread is running")
        self.client.loop_forever()
        pass   # end of run function
    def functions(self):
        self.dcmotor.motor()
        self.dcmotor.oldSensorState
        if self.dcmotor.oldSensorState:
            data = {'MagnetSensor' :'ON'}
            sensorStatus = json.dumps(data)
            self.client.publish("biogas/magnet_/sensor_/",sensorStatus)
            self.dcmotor.oldSensorState = False
        elif self.nlmotor.check:
            self.nlmotor.func()
        elif self.Sensor is not None:
            Sensor = self.Sensor
            Brightness = self.Brightness
            self.RGBsensor.func(Sensor,Brightness)
            color = self.RGBsensor.getAvgColorData()
            color = json.dumps(color)
            self.client.publish("biogas/color_/sensor_/",color)
            self.Brightness = None
            self.Sensor = None
    pass   # end of function function loop
class RGB_Sensor:
    def __init__(self):
        #self.LEDMag_PX_45ma_PotVal = {0:64,  1:64,  2:64,  3:64,  4:64} 
        self.LEDDet_PX_45ma_PotVal = {0:53,  1:64,  2:51,  3:64,  4:64}
        self.LEDMagPcb_MuxChn = { 0:0x01,  1:0x02,  2:0x04,  3:0x08,  4:0x10}
        self.LEDDetPcb_MuxChn = { 0:0x10,  1:0x08,  2:0x04,  3:0x02,  4:0x01}
        self.dicColorData = None
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
    def getAvgColorData(self):
        tempData = self.dicColorData
        self.dicColorData = None
        return tempData
        pass   # ejnd of getAvgColorData() function
    def getColorAvg(self,color,value,counts): # color name in string
        if color == "violet" and counts < 10:
            self.violetValues += value
            print(f"{color} color value is : {value}")
        elif color == "blue" and counts < 10:
            self.blueValues += value
            #print(f"{color} color value is : {value}")
        elif color == "green" and counts < 10:
            self.greenValues += value
            #print(f"{color} color value is : {value}")
        elif color == "yellow" and counts < 10:
            self.yellowValues += value
            #print(f"{color} color value is : {value}")
        elif color == "orange" and counts < 10:
            self.orangeValues += value
            #print(f"{color} color value is : {value}")
        elif color == "red" and counts < 10:
            self.redValues += value
            #print(f"{color} color value is : {value}")
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
    def func(self,Sensor,brightness):
        countSamples = 0
        while countSamples < 10:
            try:
                print("Star: While Loop")
                # - Activate P0 LED on Mag PCB Side
                self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Sensor])
                time.sleep(.5)
                # - Set the value via Dictionary per specific PCB, later this needs to be in Non-Volatile Chip (Pot) Default Memory
                self.bus.write_byte_data(0x2E,0x00, brightness) # Write to Wiper 0, Volatile
                time.sleep(.5)
                Vol_Wiper0 = self.bus.read_word_data(0x2E,0x0C) # Addr = 0h in Read Mode
                time.sleep(0.2)
                print(f"LED {Sensor} Current Changed With Acknowledge Register Vol_wiper0", Vol_Wiper0)
                # - Be Safe, always disconnect the Mux until next use
                self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                time.sleep(.1)
                # Activate P0 LED on Det PCB Side
                self.bus.write_byte_data(self.Det_Board,0x04, self.LEDDetPcb_MuxChn[Sensor])
                time.sleep(.1)
                LED_CurrentSourcePot_Val = self.LEDDet_PX_45ma_PotVal[Sensor]
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
                    time.sleep(0.2)
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
                self.bus.write_byte_data(self.Mag_Board,0x04,self.LEDMagPcb_MuxChn[Sensor])
                time.sleep(.1)
                self.bus.write_byte_data(0x2E,0x00,0x00)
                time.sleep(.1)
                # - Be Safe, always disconnect the Mux until next use
                self.bus.write_byte_data(self.Mag_Board,0x04,0x00)
                 # - Turn OFF Det 2nd
                time.sleep(.1)
                self.bus.write_byte_data(self.Det_Board,0x04,self.LEDDetPcb_MuxChn[Sensor])
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
                    
                    self.dicColorData = {
                                   "Violet":violet_Avg,
                                   "Blue":blue_Avg,
                                   "Green":green_Avg,
                                   "Yellow":yellow_Avg,
                                   "Orange":orange_Avg,
                                   "Red":red_Avg
                                    }
                    
                print("End : While Loop " + str(countSamples))
                countSamples += 1
            except Exception as error:
                print(error)
        pass   # end of func function
    pass # end of functions class

class dcMotor:  #(threading.Thread):
    def __init__(self):
        #threading.Thread.__init__(self)
        self.motor_is_start = False
        self.initialize()
        GPIO.setup(self.MotorControllerPin_In1, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
        GPIO.setup(self.MotorControllerPin_In2, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
        GPIO.setup(self.ParkDetPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)     #Setup the hardware
        GPIO.add_event_detect(self.ParkDetPin, GPIO.FALLING, callback = self.ParkFlag_callback, bouncetime = 50)
        #self.start()
        pass# end of dcMotor class constructor
    def initialize(self):
        self.varSpeedDutyCycle = 0
        self.oldSensorState = False
        self.sensorState = False
        # motor control pins
        self.MotorControllerPin_In1 = 12 # GPIO(12), Pi Pin 32
        self.MotorControllerPin_In2 = 13 # GPIO(13), Pi Pin 33
        # initializing parameters
        self.NormalPWMFreq = 100
        self.ParkDetPin = 23             # GPIO 23 - This is the signal from Hall Effect to detect the park position.
        pass   # end of initializing function
    def ParkFlag_callback(self,Pin):
        if GPIO.input(self.ParkDetPin) == GPIO.LOW:
            self.sensorState = True
            self.oldSensorState = self.sensorState
            self.sensorState = False
        pass   # end of callback function
    
    def motor(self):
        PWM1 = GPIO.PWM(self.MotorControllerPin_In2,self.NormalPWMFreq) # 100Hz
        PWM1.start(0)
        if self.motor_is_start:
            for Duty in range(0,self.varSpeedDutyCycle,1):
                PWM1.ChangeDutyCycle(Duty)
                time.sleep(0.2)
                if self.motor_is_start is False:
                    break
        pass   # end of motor_run
    pass   # end of dcMotor class

class nLmotor:
    bus = smbus.SMBus(0)
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.paramInit()
        # - Stepper Gearhead Motor Output for Cassette movement (insert/ Eject)
        GPIO.setup(self.PCB4_StepPulse_Pin, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
        # - Stepper Gearhead Motor Direction Output for Cassette movement (insert/ Eject)
        GPIO.setup(self.PCB4_Dir_Pin, GPIO.OUT, initial = 1) # Initialize pin as an output as low state.
        self.bus.write_byte_data(0x20, 0x06, 0x00)    # - Port 0 set to be all ouputs
        time.sleep(.1)
        self.bus.write_byte_data(0x20, 0x07, 0x00)    # - Port 1 set to be all ouputs
        time.sleep(.1)
        # - Initialize all the outputs to a high voltage (all's 1's)
        self.bus.write_byte_data(0x20, 0x02, 0xFF)    # - Port 0 set outputs all high
        time.sleep(.1)
        self.bus.write_byte_data(0x20, 0x03, 0xFF)    # - Port 1 set outputs all high
        time.sleep(.1)
        self.PCB4_Stepper_PWM = GPIO.PWM(self.PCB4_StepPulse_Pin, self.PCB4_StepPulse_Freq)
        self.PCB4_Stepper_PWM.start(0) # On, but zero DutyCycle thus not running
        pass   # end of nLmotor class constructor
    def paramInit(self):
        self.PCB4_StepPulse_Pin = 26     # GPIO(26), Pi Pin 37
        self.PCB4_Dir_Pin = 20           # GPIO(20), Pi Pin 38
        # - Fixed Parameters for Linear Motor
        self.PCB4_Run_DutyCycle = 50     # - Step pulse set to XX% dutycycle (note uses leading edge, not both edges)
        self.PCB4_StepPulse_Freq = 2400    # - Steps per second
        self.FullStep = 0
        self.CassetteInsert = 1         # - Cassette insert = 1 value on the direction pin
        self.CassetteEject = 0          # - Cassette Eject = 0 value on the direction pin
        self.check = False
        self.rotvalue = 0
        pass   # end of paramInit function
    def func(self):
        if self.check:
            self.rotvalue = self.rotvalue/19
            GPIO.output(self.PCB4_Dir_Pin, self.CassetteInsert) # - Default to the inward direction of movement (Cassette Insertion)
            # - Initialize PWM for Stepping Motor PWM, but leave not running
            self.bus.write_byte_data(0x20, 0x03, 0xF9)    # to run full step
            time.sleep(.1)
            self.bus.write_byte_data(0x20, 0x03, 0xF8)
            time.sleep(.1)
            self.PCB4_Stepper_PWM.ChangeDutyCycle(0)                  # - Stop the motor
            # - Run inward direction, Cassette Insertion
            GPIO.output(self.PCB4_Dir_Pin, self.CassetteInsert)
            self.PCB4_Stepper_PWM.ChangeDutyCycle(self.PCB4_Run_DutyCycle) # - its moving outward, Inserting Cassette
            time.sleep(self.rotvalue)                                        # - Run for fixed time period
            self.PCB4_Stepper_PWM.ChangeDutyCycle(0)                  # - Stop the motor
            time.sleep(.1)
            # - Initialize PCB4 to Disabled (/EN=1), Full Step (M1&M0=0,0), Awake (/SLP=1)
            self.bus.write_byte_data(0x20, 0x03, 0xF9)    # - 1111,1001
            time.sleep(.1)
            self.rotvalue = 0
            self.check = False
        else:
            return
        pass   # end of func function
    pass   # end of nLmotor class
        
if __name__ == "__main__":
    main = Main()
    main.start()
    while True:
        main.functions()



