import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import threading
import time
import json
import sys

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering

class dcMotor(threading.Thread):
    client = mqtt.Client()
    def __init__(self):
        threading.Thread.__init__(self)
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.subscribe("biogas_/park_/start_/")
        self.requestIs = False
        self.FullSpeedDutyCycle = 25
        self.LowSpeedDutyCycle = 10
        self.CreepSpeedDutyCycle = 3
        self.NormalPWMFreq = 100
        self.CreepPWMFreq = 33
        #----DC Motor Pin assignment
        self.MotorControllerPin_In1 = 12 # GPIO(12), Pi Pin 32
        self.MotorControllerPin_In2 = 13 # GPIO(13), Pi Pin 33
        # call back function parameters
        self.ParkDetPin = 23
        #Park Sensor Status's
        self.firstHit = 1
        self.secondFirstHit = 2
        self.secondHit = 3
        self.parkSensorStatus = 0
        GPIO.setup(self.ParkDetPin,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Park sensor Pin initialize
        # - DC Motor Controller GPIO's as outpts
        GPIO.setup(self.MotorControllerPin_In2, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
        GPIO.setup(self.MotorControllerPin_In1, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
        # ---- Setup PMW
        self.PWM1 = GPIO.PWM(self.MotorControllerPin_In2,self.NormalPWMFreq) # 100Hz
        self.PWM1.start(0)
        pass   # end of dcMotor constructor
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        pass   # end of on_connect function
    def on_message(self,client, userdata, msg):
        print("subscribed")
        print(f"Message Topic is : {msg.topic}")
        self.parsedJson = json.loads(msg.payload)
        self.requestIs = self.parsedJson['request']
        pass    # end of om_message function
    def func(self):
        if self.requestIs is True:
            print("Starting Point:")
            self.rampUpToFullSpeedNormalPWM()
            self.rampDownToLowSpeedNormalPWM()
            GPIO.add_event_detect(self.ParkDetPin, GPIO.FALLING, callback = self.ParkFlag_callback, bouncetime = 50)#Setup the hardware
            print("Jog Reached Start Waiting For Sensor 1st Time.....")
            dataWaiting1 = {"Step":"Waiting For First Hit of Sensor"}
            self.pubLish(dataWaiting1)
            while True:
                if self.parkSensorStatus == self.firstHit:
                    print("Park Sensor Hitted For First Time!!!")
                    dataHit1 = {"Step":"Park Sensor Hitted First Time, Motor Go in Creep Speed!!!"}
                    self.pubLish(dataHit1)
                    for Duty in range(self.LowSpeedDutyCycle,self.CreepSpeedDutyCycle,-1):
                        self.PWM1.ChangeDutyCycle(Duty)
                        time.sleep(0.2)
                    self.PWM1.ChangeDutyCycle(self.CreepSpeedDutyCycle)
                    self.PWM1.ChangeFrequency(self.CreepPWMFreq)
                    print("Start Waiting For Sensor 2nd Time.....")
                    dataWaiting2 = {"Step":"Waiting For Second Hit of Sensor"}
                    self.pubLish(dataWaiting2)
                    while True:
                        if self.parkSensorStatus == self.secondHit:
                            print("Park Sensor Hitted For Second Time!!!")
                            self.PWM1.ChangeFrequency(self.NormalPWMFreq)
                            self.PWM1.ChangeDutyCycle(0)
                            self.parkSensorStatus = 0
                            self.requestIs = False
                            print("Motor Stop.....!!!")
                            dataHit2 = {"Step":"Park Sensor Hitted Second Time, Motor Stop!!!"}
                            self.pubLish(dataHit2)
                            print("Ending Point:")
                            GPIO.remove_event_detect(self.ParkDetPin)# delete event for use next time again
                            return
        pass   # end of func function
    def run(self):
        print("thread is running")
        self.client.loop_forever()
        pass   # end of run function which is running for mqtt thread
    def pubLish(self,data):
        jsonData = json.dumps(data)
        self.client.publish("biogas_/park_/sequence_/",jsonData)
        pass   # end of pubLish function
    def ParkFlag_callback(self,Pin):
        if self.parkSensorStatus == 0 and GPIO.input(self.ParkDetPin) == GPIO.LOW:
            self.parkSensorStatus = self.firstHit
            print("First Hit")
            time.sleep(1)
            return
        elif self.parkSensorStatus == self.firstHit and GPIO.input(self.ParkDetPin) == GPIO.LOW:
            self.parkSensorStatus = self.secondHit
            print("Second Hit")
            return
    def rampUpToFullSpeedNormalPWM(self):
        # ---- Ramp Up to Full Speed
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        self.PWM1.ChangeDutyCycle(0)
        print('Seq: Reached Run Speed For 5 Second')
        data = {"Step":"Ramp Up To Full Speed"}
        self.pubLish(data)
        for Duty in range(0,self.FullSpeedDutyCycle, 1):
            self.PWM1.ChangeDutyCycle(Duty)
            time.sleep(0.2)
        time.sleep(5)
        #self.PWM1.ChangeDutyCycle(0)
        pass   # end of rampUptoFullSpeed5Sec function
    def rampDownToLowSpeedNormalPWM(self):
        # ---- Ramp Dn to Low Speed
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        self.PWM1.ChangeDutyCycle(0)
        print('Seq: Ramp Down to Jog')
        data = {"Step":"Ramp Down To Low Speed"}
        self.pubLish(data)
        for Duty in range(self.FullSpeedDutyCycle,self.LowSpeedDutyCycle,-1):
            self.PWM1.ChangeDutyCycle(Duty)
            time.sleep(0.2)
        #time.sleep(5)
        #self.PWM1.ChangeDutyCycle(0)
        pass   # end of rampDownToLowSpeedNormalPWM function
    def rampDownToCreepSpeedDutyAndCreepPWM(self):
        # ---- Ramp Dn to Creep Speed
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        self.PWM1.ChangeDutyCycle(0)
        print('Seq5: Ramp Dn to Creep Speed, run 5sec')
        for Duty in range(self.LowSpeedDutyCycle,self.CreepSpeedDutyCycle,-1):
            self.PWM1.ChangeDutyCycle(Duty)
            time.sleep(0.2)
        self.PWM1.ChangeFrequency(self.CreepPWMFreq)
        time.sleep(5)
        self.PWM1.ChangeDutyCycle(0)
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        pass   # end of rampDownToCreepSpeedDutyAndCreepPWM function
    pass   # end of dcMotor class

if __name__ == "__main__":
    dcMotor = dcMotor()
    dcMotor.start()
    while True:
        dcMotor.func()
    
