from datetime import datetime
import time
import csv

class CSV:
    def __init__(self):
        self.logname = None
        self.Title = ""
        self.TempTitle = ""
        pass  # end of basicEntryAndPrepForReading class constructor
    def createFile(self):           
        self.Title = input ('>> Please enter a name for this test : ')
        if self.Title == "":
            self.Title = 'No Title Entered'
            print("You Don't Have Entered Title Name")
        else:
            print(f"You Entered Title Name is : {self.Title}")
        self.logname = datetime.now().strftime("%Y.%m.%d__Matrix_Data__%I.%M.%S%p.csv")
        with open("./Matrix_Data/" +self.logname, 'w') as file:
            writer = csv.writer(file)
            #file.write("---- Full Calibration Matrix Data ----\n")
            
            self.TempTitle = '-- '+ str(self.Title) + ' --\n'
            TempHeader = 'Data_Point, Sample_Num, Time_Stamp, Time_Per, Temp, Gain, Int_Time, Allowable_Dev,' +\
                         'Count Used Vio, Raw Values Vio(450nm), Values Selected Vio(450nm), Avg Of Vio(450nm), ' +\
                         'Count Used Blu, Raw Values Blu(500nm), Values Selected Blu(500nm), Avg Of Blu(500nm), ' +\
                         'Count Used Grn, Raw Values Grn(550nm), Values Selected Grn(550nm), Avg Of Grn(550nm), ' +\
                         'Count Used Yel, Raw Values Yel(570nm), Values Selected Yel(570nm), Avg Of Yel(570nm), ' +\
                         'Count Used Org, Raw Values Org(600nm), Values Selected Org(600nm), Avg Of Org(600nm), ' +\
                         'Count Used Red, Raw Values Red(650nm), Values Selected Red(650nm), Avg Of Red(650nm) \n'
            file.write(self.TempTitle)
            file.write(TempHeader)
            file.close()
            print(f"File Made With Name : {self.logname}")
        pass   # end of makeCsvFile function          
    pass   # end of basicEntryAndPrepForReading class
            
if __name__ == "__main__":
    main = CSV()
    main.createFile()
