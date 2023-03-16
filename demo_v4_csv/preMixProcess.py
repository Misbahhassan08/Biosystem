from config import *
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #To disable warnings

class PreMixProcess:
    def __init__(self):
        #-------- Prep global flag for callback: note needed due to threads
        self.WaitForParkPosition = None
        self.PWM1 = None
        pass   # end of preMixProcess class constructor
    def mixProcess(self):
        #-------- Prep global flag for callback: note needed due to threads
        self.WaitForParkPosition = False
        #---- Initialze hardware related to motor & Flag Detection
        #---- Note - this cannot be above other hardware being initialized; Flag doesn't work.
        #-----------------------------------------
        self.Mixing("Setup Park Detection")
        self.Mixing("Setup PWM") 
        #-------- Pre-Mix: Start Mixing at full speed (set by speed controller knob)
        #-------- Note - the PWM is only used to slow down for parking
        print ('        - Pre-Mix - In process', end='')
        #print("PreMix: RampUp To Full Speed") 
        self.Mixing("RampUp To Full Speed")  
        time.sleep(PreMix_RunTimeAtFullSpeed)
        #-----------------------------------------
        #-------- Pre-Mix: Drop to Park Speed
        #-----------------------------------------
        #print("PreMix: Ramp Down to Park Speed")   
        self.Mixing("RampDnToParkSpeed")
        time.sleep(PreMix_RunTimeAtParkingSpeed)
        #-----------------------------------------
        #-------- Pre-Mix: Stop on the next Park Flag Detection
        #-----------------------------------------
        self.WaitForParkPosition = True
        time.sleep(4)     # this is required to allow flag time to be found; no shorter than 2 sec.
        print ('        - Pre-Mix - Completed')
        pass   # end of mixProcess function
    def mainMixAndPark(self):
        #-------- Prep global flag for callback: note needed due to threads
        self.WaitForParkPosition = False
        #-------- Main_Mix: Start Mixing at full speed (set by speed controller knob)
        #-------- Note - the PWM is only used to slow down for parking
        print ('        - Main-Mix - In process', end='')
        #print("MainMix: RampUp To Full Speed")
        self.Mixing("RampUp To Full Speed")
        time.sleep(MainMix_RunTimeAtFullSpeed)
        #-----------------------------------------
        #-------- Main_Mix: Drop to Park Speed
        #-----------------------------------------
        #print("MainMix: Ramp Down to Park Speed")   
        self.Mixing("RampDnToParkSpeed")
        time.sleep(MainMix_RunTimeAtParkingSpeed)
        #-----------------------------------------
        #-------- Main_Mix: Stop on the next Park Flag Detection
        #-----------------------------------------
        self.WaitForParkPosition = True
        time.sleep(4)     # this is required to allow flag time to be found; no shorter than 2 sec.
        print ('        - Main-Mix - Completed')
        #-----------------------------------------
        #-------- Mixing is complete, begin next read
        #-----------------------------------------
        pass   # end of mainMixAndPark function
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
    pass   # end of preMixProcess Class

if __name__ == "__main__":
    main = PreMixProcess()
    main.mixProcess()
    main.mainMixAndPark()
            