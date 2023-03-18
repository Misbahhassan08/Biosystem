from datetime import datetime
import time
import csv

class BasicEntryAndPrepForReading:
    def __init__(self):
        self.logname = None
        pass  # end of basicEntryAndPrepForReading class constructor
    def makeCsvFile(self):
        print('----------------------------------------------------------------------------------')
        print('--------                          New Run                                 --------')
        print('----------------------------------------------------------------------------------')            
        #-----------------------------------------
        #- Enter Title of log
        #----------------------------------------
        Run_Title = input ('>> Please enter a name for this test : ')
        if Run_Title == '':
            Run_Title = 'No Title Entered'
        #-----------------------------------------
        # Show the program is Ready for a run and needs a 1+Enter to begin it
        #-----------------------------------------
        EnteredValue = 'Nothing'
        while EnteredValue != '' and EnteredValue != '3':
            # ---- Check to see if the initial text message is needed, or short form (i.e. 1st pass or not)
            if EnteredValue == 'Nothing':     # First pass
                EnteredValue = input ('>> System is ready for a new run\n     >> press \'Enter\' Key to begin a run OR \'3+Enter\' to exit the program: ')
            else:
                EnteredValue = input()         # Not the first pass
            #---- Evaluate users entry
            if EnteredValue != ''and EnteredValue != '3':
                print ('        - Incorrect selection try \'Enter\' to begin, or \'3+Enter\' to exit the program: ', end='')
            elif EnteredValue == '3':
                print ('-------- User elected to END THE PROGRAM via entering \'3\'! --------')
                break
            elif EnteredValue == '':
                # Display message to user showing the process has started
                print ('        - \'Enter\' selected - creating a new file for the new series of measurements ')
                #---- Create a new blank file with the a name having (YY.MM.DD__Matrix_Data.HH.MM.SS): Example "21.06.18_Matrix_Data.02.30.59.csv"
                self.logname = datetime.now().strftime("%Y.%m.%d__Matrix_Data__%I.%M.%S%p.csv")
                with open("./Matrix_Data/" +self.logname, 'w') as file:
                    writer = csv.writer(file)
                    #file.write("---- Full Calibration Matrix Data ----\n")
                    TempTitle = ""
                    TempTitle = '-- '+ str(Run_Title) + ' --\n'
                    TempHeader = 'Run Time, Gain, Int Time, Allowable Dev, Sample Num, Temp, Time Per, ' +\
                                 'Count Used Vio, Raw Values Vio(450nm), Values Selected Vio(450nm), Avg Of Vio(450nm), ' +\
                                 'Count Used Blu, Raw Values Blu(500nm), Values Selected Blu(500nm), Avg Of Blu(500nm), ' +\
                                 'Count Used Grn, Raw Values Grn(550nm), Values Selected Grn(550nm), Avg Of Grn(550nm), ' +\
                                 'Count Used Yel, Raw Values Yel(570nm), Values Selected Yel(570nm), Avg Of Yel(570nm), ' +\
                                 'Count Used Org, Raw Values Org(600nm), Values Selected Org(600nm), Avg Of Org(600nm), ' +\
                                 'Count Used Red, Raw Values Red(650nm), Values Selected Red(650nm), Avg Of Red(650nm) \n'
                    file.write(TempTitle)
                    file.write(TempHeader)
                    file.close()
        pass   # end of makeCsvFile function          
    pass   # end of basicEntryAndPrepForReading class
            
if __name__ == "__main__":
    main = BasicEntryAndPrepForReading()
    main.makeCsvFile()