# Define global variables
RunStatus = None
MainMixAndPark = 1
Exit_Program = 2
#------------------------------------------------------------------------------------
#---- ------Operational parameters ---------------
Total_NumberOfSamplings = 2    # This is the total number of samplings for the test, each with 6 readings per
NumOfReadings = 6              # Number of sensor reading per measurement (i.e. per sampling)
ReadNum = 0
AllowableDev = 150              # Allowable deviation between the 6 readings before including the reading
#---------- Sensor parameters----------#
Gain = 16
Integration_time = 700
MainLED_Current = 25
IndLED_Current = 1
#---- Pre-Mix & Main-Mix: Run times
PreMix_RunTimeAtFullSpeed = 5     # Time in seconds of the amount of time the pre-mix cycle will run for.
MainMix_RunTimeAtFullSpeed = 30    # Set amount of time the main-mix cycle will run for.
#---- Pre-Mix & Main-Mix: Parking Speeds *** that should not be changed without discussion ****
PreMix_RunTimeAtParkingSpeed = 3   # Time in seconds of the time (likley minimum) needed to rampdown to park speed
MainMix_RunTimeAtParkingSpeed = 3  # Set the time (likley minimum) needed to rampdown to park speed 
#-----------------------------------------------------------------------------------------------------
#---- Define firmware elements for mixing
#-----------------------------------------  
MixMotor_Enable = 13               # GPIO 13 - This enables the mixing motor, speed is set by the motor controller on the front of unit.
Mixing_On = 1
Mixing_Off = 0
ParkDetPin = 23                    # GPIO 23 - This is the signal from Optics show movement is in park position.
PWM_Freq = 100                     # This is always 100
FullSpeed = 25
# This is always 100
ParkingSpeed = 7
#--------------------------------------------------------#

#----------------------------------------------------------------------#
#--------- Define firmware elements for Mux Chips------------#
#----------------------------------------------------------------------#

MuxAddress = 0x70     # Defines the Mux chip                     (mux not used on single cuvette box)
CommandRegVal = 0x01  # Defines which channel to use on Mux chip (mux not used on single cuvette box)  

