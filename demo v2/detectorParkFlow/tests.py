import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering

class dcMotor:
    def __init__(self):
        self.FullSpeedDutyCycle = 25
        self.LowSpeedDutyCycle = 10
        self.CreepDutyCycle = 3
        self.NormalPWMFreq = 100
        self.CreepPWMFreq = 33
        self.NormalPWMFreq = 100
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
        # - DC Motor Controller GPIO's as outpts
        GPIO.setup(self.MotorControllerPin_In2, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
        GPIO.setup(self.MotorControllerPin_In1, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
        # ---- Setup PMW
        self.PWM1 = GPIO.PWM(self.MotorControllerPin_In2,self.NormalPWMFreq) # 100Hz
        self.PWM1.start(0)
        pass   # end of dcMotor constructor
    def func(self):
        self.rampUpToFullSpeedNormalPWM()
        self.rampDownToLowSpeedNormalPWM()
        GPIO.setup(self.ParkDetPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.ParkDetPin, GPIO.FALLING, callback = self.ParkFlag_callback, bouncetime = 50)#Setup the hardware
        print("Setup park sensor for first interrupt detection")
        while True:
            if self.parkSensorStatus == self.firstHit:
                print("Park sensor hitted for first interrupt!!!")
                for Duty in range(self.LowSpeedDutyCycle,self.CreepDutyCycle,-1):
                    self.PWM1.ChangeDutyCycle(Duty)
                    time.sleep(0.2)
                self.PWM1.ChangeFrequency(self.CreepPWMFreq)
                self.parkSensorStatus = 0
                print("Setup sensor for first interrupt detection in second loop")
                while True:
                    if self.parkSensorStatus == self.firstHit:
                        print("Park sensor hitted for first interrupt!!!")
                        print("Waiting for second interrupt")
                    elif self.parkSensorStatus == self.secondHit:
                        print("Sensor hitted second time and motor stopped")
                        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
                        self.PWM1.ChangeDutyCycle(0)
                        return
                #self.parkSensorStatus = 0
                #print("Setup park sensor for second first interrupt detection")
            #elif self.parkSensorStatus == self.firstHit:
                #print("First Hitted for second setup and waiting for second Hit")
            #elif self.parkSensorStatus == self.secondHit:
                #self.PWM1.ChangeFrequency(self.NormalPWMFreq)
                #self.PWM1.ChangeDutyCycle(0)
                #break
        pass   # end of func function
    def ParkFlag_callback(self,Pin):
        if self.parkSensorStatus == 0 and GPIO.input(self.ParkDetPin) == GPIO.LOW:
            self.parkSensorStatus = self.firstHit
            print("First Hit")
            return
        elif self.parkSensorStatus == self.firstHit and GPIO.input(self.ParkDetPin) == GPIO.LOW:
            self.parkSensorStatus = self.secondHit
            print("Second Hit")
            return
    def rampUpToFullSpeedNormalPWM(self):
        # ---- Ramp Up to Full Speed
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        self.PWM1.ChangeDutyCycle(0)
        print('Seq: Ramp Up to Full Speed, Normal PWM')
        for Duty in range(0,self.FullSpeedDutyCycle, 1):
            self.PWM1.ChangeDutyCycle(Duty)
            time.sleep(0.2)
        time.sleep(5)
        self.PWM1.ChangeDutyCycle(0)
        pass   # end of rampUptoFullSpeed5Sec function
    def rampDownToLowSpeedNormalPWM(self):
        # ---- Ramp Dn to Low Speed
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        self.PWM1.ChangeDutyCycle(0)
        print('Seq4: Ramp Dn to Low Speed, run 5sec')
        for Duty in range(self.FullSpeedDutyCycle,self.LowSpeedDutyCycle,-1):
            self.PWM1.ChangeDutyCycle(Duty)
            time.sleep(0.2)
        time.sleep(5)
        self.PWM1.ChangeDutyCycle(0)
        pass   # end of rampDownToLowSpeedNormalPWM function
    def rampDownToCreepSpeedDutyAndCreepPWM(self):
        # ---- Ramp Dn to Creep Speed
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        self.PWM1.ChangeDutyCycle(0)
        print('Seq5: Ramp Dn to Creep Speed, run 5sec')
        for Duty in range(self.LowSpeedDutyCycle,self.CreepDutyCycle,-1):
            self.PWM1.ChangeDutyCycle(Duty)
            time.sleep(0.2)
        self.PWM1.ChangeFrequency(self.CreepPWMFreq)
        time.sleep(5)
        self.PWM1.ChangeDutyCycle(0)
        self.PWM1.ChangeFrequency(self.NormalPWMFreq)
        pass   # end of rampDownToCreepSpeedDutyAndCreepPWM function
    pass   # end of dcMotor class

if __name__ == "__main__":
    print("Starting Point:")
    dcmotor = dcMotor()
    dcmotor.func()
    print("Ending Point:")
    
