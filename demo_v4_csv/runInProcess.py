from basicEntryAndPrepForReading import BasicEntryAndPrepForReading
from adafruit_as726x import AS726x_I2C
from config import *
import smbus
import board
import time
import csv

class RunInProcess:
    def __init__(self):
        self.prepCsv = BasicEntryAndPrepForReading()
        self.prepCsv.makeCsvFile()
        self.SampleCnt = 0
        self.bus = 1
        self.ReadNum = 1
        self.Show_Measurement_Details = True
        self.full_test_str = ""
        #---- Define firmware elements for sensor---------#
        #---- Sensor Arrays
        self.Raw_List_Vio = []
        self.Raw_List_Blu = []
        self.Raw_List_Grn = []
        self.Raw_List_Yel = []
        self.Raw_List_Org = []
        self.Raw_List_Red = []
        pass  # end of runInPRocess class constructor
    def inProcess(self):
        print("[INFO] : Start Point....")
        if self.SampleCnt < Total_NumberOfSamplings:
            # - Start loop to gather 6 readings
            while self.ReadNum <= NumOfReadings:
                startTime = time.time()
                try:
                    # Prep for measurement
                    #self.SampleCnt = self.SampleCnt+1
                    i2c = board.I2C()
                    self.Bus = smbus.SMBus(self.bus)
                    # --- below sets up the Mux for a single chip only,

                    #    defualted to channel 1
                    # - This is the more flexible version ... self.Bus.write_byte_data(MuxAddress,0x04,CommandRegVal)
                    # - The five channels are 0x01, 0x02, 0x04, 0x08, 0x10
                    self.Bus.write_byte_data(0x70,0x04,0x10)
                    sensor = AS726x_I2C(i2c)                #Create the sensor object and point it at the I2C self.Bus
                    sensor.driver_led_current = MainLED_Current  # Drive Current of External LED
                    sensor.indicator_led_current = IndLED_Current  # Drive current of onboard LED
                    sensor.gain = Gain
                    sensor.integration_time = Integration_time
                    
                    # ---- Read the sample
                    # - Retrieve chip temperature first
                    ChipTemperture = sensor.temperature
                    sensor.driver_led = True
                    # time.sleep(1) #On 1s min before read
                    sensor.start_measurement()
                    time.sleep(.5) #On 500ms min before read
                    while not sensor.data_ready:
                        time.sleep(.1)
                    sensor.driver_led = False
                    time.sleep(.25)
                    #---- Get the readings from sensor chip
                    self.Raw_List_Vio.append(sensor.violet)
                    self.Raw_List_Blu.append(sensor.blue)
                    self.Raw_List_Grn.append(sensor.green)
                    self.Raw_List_Yel.append(sensor.yellow)
                    self.Raw_List_Org.append(sensor.orange)
                    self.Raw_List_Red.append(sensor.red)
                    print(f"Color Data With Read Number {self.ReadNum} is Done",end=' ')
                    
                    self.ReadNum = self.ReadNum+1
                except Exception as error:
                    print(f"Colors values error : {error}")
            # - Display message to user showing the measurement is in-process
            self.SampleCnt = self.SampleCnt+1
            print('Reading Sample '+ str(self.SampleCnt) +' Done ',end=' ')   
            #-----------------------------------------------------------------
            # - Evaluate the array of samples, and retain the "viable" samples
            # ---- VIOLET
            Good_List_Vio = []
            
            for Outer_i, RefDataPtr in enumerate (self.Raw_List_Vio):
                CountOfCloseOnes = 0
                for Inner_i, TestDataPtr in enumerate(self.Raw_List_Vio):
                    if Outer_i != Inner_i:
                        if abs(RefDataPtr - TestDataPtr) < AllowableDev:
                            # Good one, count it
                            CountOfCloseOnes += 1
                if CountOfCloseOnes >= 3:
                    Good_List_Vio.append(RefDataPtr)
            # ---- BLUE
            Good_List_Blu = []
            for Outer_i, RefDataPtr in enumerate (self.Raw_List_Blu):
                CountOfCloseOnes = 0
                for Inner_i, TestDataPtr in enumerate(self.Raw_List_Blu):
                    if Outer_i != Inner_i:
                        if abs(RefDataPtr - TestDataPtr) < AllowableDev:
                            # Good one, count it
                            CountOfCloseOnes += 1
                if CountOfCloseOnes >= 3:
                    Good_List_Blu.append(RefDataPtr)
            # ---- GREENExit_Program
            Good_List_Grn = []
            for Outer_i, RefDataPtr in enumerate (self.Raw_List_Grn):
                CountOfCloseOnes = 0
                for Inner_i, TestDataPtr in enumerate(self.Raw_List_Grn):
                    if Outer_i != Inner_i:
                        if abs(RefDataPtr - TestDataPtr) < AllowableDev:
                            # Good one, count it
                            CountOfCloseOnes += 1
                if CountOfCloseOnes >= 3:
                    Good_List_Grn.append(RefDataPtr)
            # ---- YELLOW
            Good_List_Yel = []
            for Outer_i, RefDataPtr in enumerate (self.Raw_List_Yel):
                CountOfCloseOnes = 0
                for Inner_i, TestDataPtr in enumerate(self.Raw_List_Yel):
                    if Outer_i != Inner_i:
                        if abs(RefDataPtr - TestDataPtr) < AllowableDev:
                            # Good one, count it
                            CountOfCloseOnes += 1
                if CountOfCloseOnes >= 3:
                    Good_List_Yel.append(RefDataPtr)
            # ---- ORANGE
            Good_List_Org = []
            for Outer_i, RefDataPtr in enumerate (self.Raw_List_Org):
                CountOfCloseOnes = 0
                for Inner_i, TestDataPtr in enumerate(self.Raw_List_Org):
                    if Outer_i != Inner_i:
                        if abs(RefDataPtr - TestDataPtr) < AllowableDev:
                            # Good one, count it
                            CountOfCloseOnes += 1
                if CountOfCloseOnes >= 3:
                    Good_List_Org.append(RefDataPtr)
            # ---- RED
            Good_List_Red = []
            for Outer_i, RefDataPtr in enumerate (self.Raw_List_Red):
                CountOfCloseOnes = 0
                for Inner_i, TestDataPtr in enumerate(self.Raw_List_Red):
                    if Outer_i != Inner_i:
                        if abs(RefDataPtr - TestDataPtr) < AllowableDev:
                            # Good one, count it
                            CountOfCloseOnes += 1
                if CountOfCloseOnes >= 3:
                    Good_List_Red.append(RefDataPtr)

            #-----------------------------------------------------------------
            # - Average the remaining "good" ones
            # ---- VIOLET
            AvgOfGood_Vio = 0
            GoodListLength_Vio = len(Good_List_Vio)
            if GoodListLength_Vio >= 1:
                #Sum the Array
                SumOfValues = 0
                for GoodValue in Good_List_Vio:
                    SumOfValues = SumOfValues + GoodValue
                AvgOfGood_Vio = SumOfValues/GoodListLength_Vio
            # ---- BLUE
            AvgOfGood_Blu = 0
            GoodListLength_Blu = len(Good_List_Blu)
            if GoodListLength_Blu >= 1:
                #Sum the Array
                SumOfValues = 0
                for GoodValue in Good_List_Blu:
                    SumOfValues = SumOfValues + GoodValue
                AvgOfGood_Blu = SumOfValues/GoodListLength_Blu
            # ---- GREEN
            AvgOfGood_Grn = 0
            GoodListLength_Grn = len(Good_List_Grn)
            if GoodListLength_Grn >= 1:
                #Sum the Array
                SumOfValues = 0
                for GoodValue in Good_List_Grn:
                    SumOfValues = SumOfValues + GoodValue
                AvgOfGood_Grn = SumOfValues/GoodListLength_Grn
            # ---- YELLOW
            AvgOfGood_Yel = 0
            GoodListLength_Yel = len(Good_List_Yel)
            if GoodListLength_Yel >= 1:
                #Sum the Array
                SumOfValues = 0
                for GoodValue in Good_List_Yel:
                    SumOfValues = SumOfValues + GoodValue
                AvgOfGood_Yel = SumOfValues/GoodListLength_Yel
            # ---- ORANGE
            AvgOfGood_Org = 0
            GoodListLength_Org = len(Good_List_Org)
            if GoodListLength_Org >= 1:
                #Sum the Array
                SumOfValues = 0
                for GoodValue in Good_List_Org:
                    SumOfValues = SumOfValues + GoodValue
                AvgOfGood_Org = SumOfValues/GoodListLength_Org
            # ---- RED
            AvgOfGood_Red = 0
            GoodListLength_Red = len(Good_List_Red)
            if GoodListLength_Red >= 1:
                #Sum the Array
                SumOfValues = 0
                for GoodValue in Good_List_Red:
                    SumOfValues = SumOfValues + GoodValue
                AvgOfGood_Red = SumOfValues/GoodListLength_Red
            #-----------------------------------------------------------------
            # - Calculate Elapsed Time
            endTime = time.time()
            elapsedTime = endTime - startTime
            #-----------------------------------------------------------------
            # - Format & Round all the floating values to 2 decimal places
            # ---- VIOLET
            self.Raw_List_Vio_rounded  = ['%.2f' % elem for elem in self.Raw_List_Vio]
            Good_List_Vio_rounded = ['%.2f' % elem for elem in Good_List_Vio]
            AvgOfGood_Vio_rounded = '%.2f' % AvgOfGood_Vio
            # ---- BLUE
            self.Raw_List_Blu_rounded  = ['%.2f' % elem for elem in self.Raw_List_Blu]
            Good_List_Blu_rounded = ['%.2f' % elem for elem in Good_List_Blu]
            AvgOfGood_Blu_rounded = '%.2f' % AvgOfGood_Blu
            # ---- GREEN
            self.Raw_List_Grn_rounded  = ['%.2f' % elem for elem in self.Raw_List_Grn]
            Good_List_Grn_rounded = ['%.2f' % elem for elem in Good_List_Grn]
            AvgOfGood_Grn_rounded = '%.2f' % AvgOfGood_Grn
            # ---- YELLOW
            self.Raw_List_Yel_rounded  = ['%.2f' % elem for elem in self.Raw_List_Yel]
            Good_List_Yel_rounded = ['%.2f' % elem for elem in Good_List_Yel]
            AvgOfGood_Yel_rounded = '%.2f' % AvgOfGood_Yel
            # ---- ORANGE
            self.Raw_List_Org_rounded  = ['%.2f' % elem for elem in self.Raw_List_Org]
            Good_List_Org_rounded = ['%.2f' % elem for elem in Good_List_Org]
            AvgOfGood_Org_rounded = '%.2f' % AvgOfGood_Org
            # ---- RED
            self.Raw_List_Red_rounded  = ['%.2f' % elem for elem in self.Raw_List_Red]
            Good_List_Red_rounded = ['%.2f' % elem for elem in Good_List_Red]
            AvgOfGood_Red_rounded = '%.2f' % AvgOfGood_Red
            # ---- Elapsed Time only
            elapsedTime_rounded = '%.2f' % elapsedTime
            #-----------------------------------------------------------------
            print ('- 600nm Result :' + str(AvgOfGood_Org_rounded))
            if self.Show_Measurement_Details == True:
                Run_Title = "[INFO]: My Testing"
                print ('               -------------------------------------------------------------------------------------')
                print ('                  Run Title = \''+ Run_Title + '\'')
                print ('                  Sample Number = ' + str(self.SampleCnt))
                print ('                  Temperature: {0}C'.format(ChipTemperture))
                # ---- VIOLET Detail
                print ('                  List Length Vio = ' + str(GoodListLength_Vio))
                print (f'                  Raw List Vio = {self.Raw_List_Vio_rounded}')
                print (f'                  Good List Vio =     {Good_List_Vio_rounded}')
                # ---- BLUE Detail
                print ('                  List Length Blu = ' + str(GoodListLength_Blu))
                print (f'                  Raw List Blu = {self.Raw_List_Blu_rounded}')
                print (f'                  Good List Blu =     {Good_List_Blu_rounded}')
                # ---- GREEN Detail
                print ('                  List Length Grn = ' + str(GoodListLength_Grn))
                print (f'                  Raw List Grn = {self.Raw_List_Grn_rounded}')
                print (f'                  Good List Grn =     {Good_List_Grn_rounded}')
                # ---- YELLOW Detail
                print ('                  List Length Yel = ' + str(GoodListLength_Yel))
                print (f'                  Raw List Yel = {self.Raw_List_Yel_rounded}')
                print (f'                  Good List Yel =     {Good_List_Yel_rounded}')
                # ---- ORANGE Detail
                print ('                  List Length Org = ' + str(GoodListLength_Org))
                print (f'                  Raw List Org = {self.Raw_List_Org_rounded}')
                print (f'                  Good List Org =     {Good_List_Org_rounded}')
                # ---- RED Detail
                print ('                  List Length Red = ' + str(GoodListLength_Red))
                print (f'                  Raw List Red = {self.Raw_List_Red_rounded}')
                print (f'                  Good List Red =     {Good_List_Red_rounded}')
                # ---- Averages next to each other
                print ('                  Average Value Vio (450nm) = ' + str(AvgOfGood_Vio_rounded))
                print ('                  Average Value Blu (500nm) = ' + str(AvgOfGood_Blu_rounded))
                print ('                  Average Value Grn (550nm) = ' + str(AvgOfGood_Grn_rounded))
                print ('                  Average Value Yel (570nm) = ' + str(AvgOfGood_Yel_rounded))
                print ('                  Average Value Org (600nm) = ' + str(AvgOfGood_Org_rounded))
                print ('                  Average Value Red (650nm) = ' + str(AvgOfGood_Red_rounded))
                print ('                  Elapsed Time = ' + str(elapsedTime_rounded))
                        
                # ----------------------------------------------------------------------------
                # ---- Save the data to a String Var, which will then be appended to actual file.               
                # - Write the header info - Gain, Integration Time, Allowable Deviation, Samples Count, Temperture, Elapsed time, to the string 1st
                # - After above write all the data to the file.
                # - Append Gain to file
                if self.full_test_str == "":
                    ### print('build first part of data string.')
                    self.full_test_str = str(Gain)
                else:
                    self.full_test_str = self.full_test_str + ', ' + str(Gain)
                # - Append Integration time to file
                self.full_test_str = self.full_test_str + ', ' + str(Integration_time)            # ---- Clear items for the next reading
                # - Append Allowable Deviation to file
                self.full_test_str = self.full_test_str + ', ' + str(AllowableDev)
                #---- Append Sample Number to file
                self.full_test_str = self.full_test_str + ', ' + str(self.SampleCnt)
                #---- Append Temperture Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(ChipTemperture)
                #---- Append Time to acquire Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(elapsedTime_rounded)
                #--------------------------------------------------------------
                #----                      VIOLET                          ----
                #--------------------------------------------------------------
                #---- Append Number of Good Readings Selected to file
                self.full_test_str = self.full_test_str + ', ' + str(GoodListLength_Vio) +' of '+ str(NumOfReadings)
                #---- Append the Original List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in self.Raw_List_Vio_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append the Good List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in Good_List_Vio_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append Average Value of Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(AvgOfGood_Vio_rounded)
                #--------------------------------------------------------------
                #----                      BLUE                            ----
                #--------------------------------------------------------------
                #---- Append Number of Good Readings Selected to file
                self.full_test_str = self.full_test_str + ', ' + str(GoodListLength_Blu) +' of '+ str(NumOfReadings)
                #---- Append the Original List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in self.Raw_List_Blu_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append the Good List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in Good_List_Blu_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append Average Value of Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(AvgOfGood_Blu_rounded)
                #--------------------------------------------------------------
                #----                      GREEN                           ----
                #--------------------------------------------------------------
                #---- Append Number of Good Readings Selected to file
                self.full_test_str = self.full_test_str + ', ' + str(GoodListLength_Grn) +' of '+ str(NumOfReadings)
                #---- Append the Original List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in self.Raw_List_Grn_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append the Good List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in Good_List_Grn_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append Average Value of Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(AvgOfGood_Grn_rounded)
                #--------------------------------------------------------------
                #----                      YELLOW                          ----
                #--------------------------------------------------------------
                #---- Append Number of Good Readings Selected to file
                self.full_test_str = self.full_test_str + ', ' + str(GoodListLength_Yel) +' of '+ str(NumOfReadings)
                #---- Append the Original List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in self.Raw_List_Yel_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append the Good List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in Good_List_Yel_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append Average Value of Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(AvgOfGood_Yel_rounded)
                #--------------------------------------------------------------
                #----                      ORANGE                          ----
                #--------------------------------------------------------------
                #---- Append Number of Good Readings Selected to file
                self.full_test_str = self.full_test_str + ', ' + str(GoodListLength_Org) +' of '+ str(NumOfReadings)
                #---- Append the Original List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in self.Raw_List_Org_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append the Good List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in Good_List_Org_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append Average Value of Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(AvgOfGood_Org_rounded)
                #--------------------------------------------------------------
                #----                      RED                             ----
                #--------------------------------------------------------------
                #---- Append Number of Good Readings Selected to file
                self.full_test_str = self.full_test_str + ', ' + str(GoodListLength_Red) +' of '+ str(NumOfReadings)
                #---- Append the Original List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in self.Raw_List_Red_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append the Good List to one cell in file
                ListToStr = ''
                ListToStr = ' / '.join(str(elem) for elem in Good_List_Red_rounded)
                self.full_test_str = self.full_test_str + ', ' + ListToStr
                #---- Append Average Value of Reading to file
                self.full_test_str = self.full_test_str + ', ' + str(AvgOfGood_Red_rounded)
                #----------------------------------------------------------------------------
                #---- Add the data gather in the last run to the log file for this run
                ts = time.localtime()
                ts = time.strftime("%Y-%m-%d_%H-%M-%S", ts)
                with open("./Matrix_Data/" + self.prepCsv.logname, 'a') as file:
                    #print('inside with statement inside add_results_to_file, writing to file')
                    writer = csv.writer(file)
                    file.write(ts + "," + self.full_test_str + '\n')
                    #print('add_results_to_file, close file')
                    file.close()
                # Clear the string for the next row of data
                self.full_test_str = ""
                # - All information written to the file.
                # ---- Prep to end this sample and go to the next.
                sensor.driver_led = False
                self.Raw_List_Vio = []
                self.Raw_List_Blu = []
                self.Raw_List_Grn = []
                self.Raw_List_Yel = []
                self.Raw_List_Org = []
                self.Raw_List_Red = []                    
                print ('        --------------------------------------------------------------------------------------------')              
                #-----------------------------------------
                #-------- Check to see if this run is complete, loop to next pass via the RunStatus
                #-----------------------------------------
            print("[INFO] : Going Good...")
            #self.SampleCnt = self.SampleCnt+1
        pass   # end of inProcess function
    pass   # end of runInProcess class

if __name__ == "__main__":
    main = RunInProcess()
    main.inProcess()

            