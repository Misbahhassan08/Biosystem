import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import threading
import random
import smbus
import json
import time

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering

class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.leds = LEDs()
        self.dcmotor = dcMotor()
        self.client = mqtt.Client()
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.subscribe("biogas/led/brightness/")
        self.client.subscribe("biogas/motor/speed_/")
        self.parsed_json = None
        self.msgTopic = None
        #self.start()
        pass   # end of ledControl class constructor
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        pass   # end of on_connect function
    def on_message(self,client, userdata, msg):
        print("subscribed")
        self.msgTopic = msg.topic
        print(self.msgTopic)
        _payload = msg.payload.decode('utf-8')
        self.parsed_json = json.loads(_payload)
        if self.msgTopic == "biogas/led/brightness/":
            print("led brightness data received")
            ack = self.leds.selectAndSet(self.parsed_json["LED"],self.parsed_json["Value"])
            if ack is not None:
                self.client.publish("biogas/ledsensor/",ack)
            self.msgTopic = None
        elif self.msgTopic == "biogas/motor/speed_/":
            print("motor data received")
            self.dcmotor.varSpeedDutyCycle = self.parsed_json["speed"]
            self.dcmotor.motor_is_start =  self.parsed_json["Motor"]
            if self.parsed_json["Motor"]:
                print("Motor is ON")
            else:
                print("Motor is OFF")
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
            data = {'MagnetSensor' : 'ON'}
            sensorStatus = json.dumps(data)
            self.client.publish("/testtopic/sensor",sensorStatus)
            self.dcmotor.oldSensorState = False
    pass   # end of function function loop
class LEDs:
    bus = smbus.SMBus(1)
    def __init__(self):
        self.BoardAndChipAddress = 0x71
        pass # end of LEDs class Constructor
    def selectAndSet(self,ledNum,LED_Current_Val):
        randInt = random.randint(0, 255)
        if ledNum == 0:
            PosSel = 0x01
            data = {
                    "Sensor": 0,
                    "Value": randInt
                    }
        elif ledNum == 1:
            PosSel = 0x02
            data = {
                    "Sensor": 1,
                    "Value": randInt
                    }
        elif ledNum == 2:
            PosSel = 0x04
            data = {
                    "Sensor": 2,
                    "Value": randInt
                    }
        elif ledNum == 3:
            PosSel = 0x08
            data = {
                    "Sensor": 3,
                    "Value": randInt
                    }
        elif ledNum == 4:
            PosSel = 0x10
            data = {
                    "Sensor": 4,
                    "Value": randInt
                    }
        else:
            data = {
                    "Sensor": "Wrong LED Select",
                    "Value": "No Value"
                    }
            json_string = json.dumps(data)
            #self.client.publish("biogas/ledsensor/",json_string)
            return json_string
        self.writeOnLed(ledNum,PosSel,LED_Current_Val)
        time.sleep(0.1)
        json_string = json.dumps(data)
        return json_string
        #self.client.publish("biogas/ledsensor/",json_string)
        pass   # end of selectAndSet function
    def writeOnLed(self,ledNum,PosSel,LED_Current_Val):
        time.sleep(.2)  
        self.bus.write_byte_data(self.BoardAndChipAddress,0x04,PosSel) # LED-Detector pcb address
        time.sleep(.2)
        self.bus.write_byte_data(0x2E,0x00,LED_Current_Val) # Write to Wiper 0, Volatile
        time.sleep(.2)
        #---- Vol Wiper 0 Register read
        Vol_Wiper0 = self.bus.read_word_data(0x2E,0x0C) # Addr = 0h in Read Mode
        time.sleep(0.2)
        print(f"LED {ledNum} Current Changed With Acknowledge Register Vol_wiper0", Vol_Wiper0)
        pass  # end of writeOnLed function
    pass   # end of LEDs class

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
        
if __name__ == "__main__":
    main = Main()
    main.start()
    while True:
        main.functions()




