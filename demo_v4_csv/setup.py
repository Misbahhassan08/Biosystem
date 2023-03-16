from config import *
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #To disable warnings
class Setup:
    def __init__(self):
        self.WaitForParkPosition = None
        self.PWM1 = None
        pass   # end of Main class constructor
    def ParkFlag_callback(self,Pin):
        if self.WaitForParkPosition == True:
            self.Mixing("SpeedToZero")
            self.WaitForParkPosition = False
            print(" - Parked")
        pass  # end of ParkFlag_callback function
    def Mixing(self,Command, Pin = MixMotor_Enable, Freq=PWM_Freq, FullDuty=FullSpeed, ParkingDuty = ParkingSpeed):
        if Command == "SpeedToZero":
            # NOTE, NOTE, NOTE - using the stop(0) does not work, Duty Cycle set to 0 does!!!
            self.PWM1.ChangeDutyCycle(0)
        elif Command == "StartAtZero":
            self.PWM1.start(0)
        elif Command == "StartFullSpeed":
            self.PWM1.start(FullDuty)
        elif Command == "ShiftToParkingSpeed":
            self.PWM1.ChangeDutyCycle(ParkingDuty)
        elif Command == "RampDnToParkSpeed":
            for Duty in range(FullDuty,ParkingDuty,-1):
                self.PWM1.ChangeDutyCycle(Duty)
                time.sleep(0.02)
            #self.PWM1.ChangeDutyCycle(ParkingDuty)
        elif Command == "RampUp To Full Speed":
            self.PWM1.start(0)
            for Duty in range(0,FullDuty, 1):
                self.PWM1.ChangeDutyCycle(Duty)
                time.sleep(0.02)
        elif Command == "ChangeFreq":        
            self.PWM1.ChangeFrequency(Freq)
        elif Command == "Setup PWM":
            print("Setup Done")
            GPIO.setup(Pin, GPIO.OUT, initial = 0) # Initialize pin as an output as low state.
            self.PWM1 = GPIO.PWM(Pin,Freq)
        elif Command == "Setup Park Detection":
            self.WaitForParkPosition = False
            GPIO.setup(ParkDetPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)     #Setup the hardware
            GPIO.add_event_detect(ParkDetPin, GPIO.RISING,callback = self.ParkFlag_callback, bouncetime = 15)
    pass   # end of Main class
if __name__ == "__main__":
    main = Setup()
    main.Mixing("Setup PWM")
    main.Mixing("RampUp To Full Speed")
    time.sleep(2)
    main.Mixing("RampDnToParkSpeed")
    time.sleep(2)
    #main.Mixing("StartFullSpeed")

    
    