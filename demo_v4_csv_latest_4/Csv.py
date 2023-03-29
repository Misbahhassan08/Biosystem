from datetime import datetime
import time
import pandas as pd
from config import *

class CSV:
    def __init__(self):
        self.logname = None
        self.Title = ""
        self.df = None
        pass  # end of basicEntryAndPrepForReading class constructor
    def createFile(self):           
        self.logname = datetime.now().strftime("%Y.%m.%d__Matrix_Data__%I.%M.%S%p.csv")
        self.df = pd.DataFrame(columns=column)
        for columNum in range(0,len(column)):
            self.df = self.df.astype({column[columNum]:dataType[columNum]})
            #print(f"column name : {column[columNum]} And DataType : {dataType[columNum]}")
        self.df.to_csv("./Matrix_Data/" +self.logname,index=False)
        print(f"File Made With Name : {self.logname}")
        pass   # end of makeCsvFile function          
    pass   # end of basicEntryAndPrepForReading class
            
if __name__ == "__main__":
    main = CSV()
    main.createFile()
