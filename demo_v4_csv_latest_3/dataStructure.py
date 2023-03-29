import sys
import csv
from Csv import CSV
import statistics
from config import *
import pandas as pd

class DataStructure:
    def __init__(self):
        self.Csv = CSV()
        self.Csv.createFile()
        #--------------------------------------Raw-------------------------------------------------#
        # ----- Raw_Used Lists ------#
        self.Raw_Used_Vio = []
        self.Raw_Used_Blu = []
        self.Raw_Used_Grn = []
        self.Raw_Used_Yel = []
        self.Raw_Used_Org = []
        self.Raw_Used_Red = []
        # ----- Raw_Values Lists ------#
        self.Raw_Values_Vio_450nm = []
        self.Raw_Values_Blu_500nm = []
        self.Raw_Values_Grn_550nm = []
        self.Raw_Values_Yel_570nm = []
        self.Raw_Values_Org_600nm = []
        self.Raw_Values_Red_650nm = []
        # ----- Raw Selected Values Lists ------#
        self.Raw_Selected_Vio_450nm = []
        self.Raw_Selected_Blu_500nm = []
        self.Raw_Selected_Grn_550nm = []
        self.Raw_Selected_Yel_570nm = []
        self.Raw_Selected_Org_600nm = []
        self.Raw_Selected_Red_650nm = []
        # ----- Avergae of Raw Selected Values ------#
        self.Raw_Avg_Vio_450nm = 0
        self.Raw_Avg_Blu_500nm = 0
        self.Raw_Avg_Grn_550nm = 0
        self.Raw_Avg_Yel_570nm = 0
        self.Raw_Avg_Org_600nm = 0
        self.Raw_Avg_Red_650nm = 0
        # ----- Raw StdDev Values ------#
        self.Raw_StdDev_Vio_450nm = 0
        self.Raw_StdDev_Blu_500nm = 0
        self.Raw_StdDev_Grn_550nm = 0
        self.Raw_StdDev_Yel_570nm = 0
        self.Raw_StdDev_Org_600nm = 0
        self.Raw_StdDev_Red_650nm = 0
        #-------------------------------------------- Cal ------------------------------------------#
        # ----- Cal_Used Lists ------#
        self.Cal_Used_Vio = []
        self.Cal_Used_Blu = []
        self.Cal_Used_Grn = []
        self.Cal_Used_Yel = []
        self.Cal_Used_Org = []
        self.Cal_Used_Red = []
        # ----- CAl_Values Lists ------#
        self.Cal_Values_Vio_450nm = []
        self.Cal_Values_Blu_500nm = []
        self.Cal_Values_Grn_550nm = []
        self.Cal_Values_Yel_570nm = []
        self.Cal_Values_Org_600nm = []
        self.Cal_Values_Red_650nm = []
        # ----- Cal Selected Values Lists ------#
        self.Cal_Selected_Vio_450nm = []
        self.Cal_Selected_Blu_500nm = []
        self.Cal_Selected_Grn_550nm = []
        self.Cal_Selected_Yel_570nm = []
        self.Cal_Selected_Org_600nm = []
        self.Cal_Selected_Red_650nm = []
        # ----- Avergae of Cal Selected Values ------#
        self.Cal_Avg_Vio_450nm = 0
        self.Cal_Avg_Blu_500nm = 0
        self.Cal_Avg_Grn_550nm = 0
        self.Cal_Avg_Yel_570nm = 0
        self.Cal_Avg_Org_600nm = 0
        self.Cal_Avg_Red_650nm = 0
        # ----- Cal StdDev Values ------#
        self.Cal_StdDev_Vio_450nm = 0
        self.Cal_StdDev_Blu_500nm = 0
        self.Cal_StdDev_Grn_550nm = 0
        self.Cal_StdDev_Yel_570nm = 0
        self.Cal_StdDev_Org_600nm = 0
        self.Cal_StdDev_Red_650nm = 0
        # ----- General data ------#
        self.df = None
        self.genData = ""
        self.rowNum = 0
        self.columnNum = 0
        pass  # end of DataStructure class constructor
    # - Evaluate the array of samples, and retain the "viable" samples
    def RawFormulas(self,Raw_List_Of,color):   # Write (Raw_List_(Color),str(Color)) 
        # ---- All Color ---- #
        # --- For round Values ----#
        Raw_List_Of_Rounded = []
        for raw in Raw_List_Of:
            Raw_List_Of_Rounded.append(round(raw,2))
        Raw_List_Of = Raw_List_Of_Rounded
        #---------------------------------------------------------------------#
        for Outer_i, RefDataPtr in enumerate (Raw_List_Of):
            CountOfCloseOnes = 0
            for Inner_i, TestDataPtr in enumerate(Raw_List_Of):
                if Outer_i != Inner_i:
                    if abs(RefDataPtr - TestDataPtr) < allowableDev:
                        # Good one, count it
                        CountOfCloseOnes += 1
            if CountOfCloseOnes >= 3:
                if color == "Vio":
                    self.Raw_Used_Vio.append(round(RefDataPtr,2))
                    self.Raw_Values_Vio_450nm = Raw_List_Of
                    self.Raw_Selected_Vio_450nm.append(round(RefDataPtr,2))
                    
                elif color == "Blu":
                    self.Raw_Used_Blu.append(round(RefDataPtr,2))
                    self.Raw_Values_Blu_500nm = Raw_List_Of
                    self.Raw_Selected_Blu_500nm.append(round(RefDataPtr,2))
                    
                elif color == "Grn":
                    self.Raw_Used_Grn.append(round(RefDataPtr,2))
                    self.Raw_Values_Grn_550nm = Raw_List_Of
                    self.Raw_Selected_Grn_550nm.append(round(RefDataPtr,2))
                    
                elif color == "Yel":
                    self.Raw_Used_Yel.append(round(RefDataPtr,2))
                    self.Raw_Values_Yel_570nm = Raw_List_Of
                    self.Raw_Selected_Yel_570nm.append(round(RefDataPtr,2))
                    
                elif color == "Org":
                    self.Raw_Used_Org.append(round(RefDataPtr,2))
                    self.Raw_Values_Org_600nm = Raw_List_Of
                    self.Raw_Selected_Org_600nm.append(round(RefDataPtr,2))
                    
                elif color == "Red":
                    self.Raw_Used_Red.append(round(RefDataPtr,2))
                    self.Raw_Values_Red_650nm = Raw_List_Of
                    self.Raw_Selected_Red_650nm.append(round(RefDataPtr,2))
        #-------------------------------------Average --------------------------------------------#
        if color == "Vio":
            self.RawAvg(self.Raw_Selected_Vio_450nm,color)
            
        elif color == "Blu":
            self.RawAvg(self.Raw_Selected_Blu_500nm,color)
        elif color == "Grn":
            self.RawAvg(self.Raw_Selected_Grn_550nm,color)
        elif color == "Yel":
            self.RawAvg(self.Raw_Selected_Yel_570nm,color)
        elif color == "Org":
            self.RawAvg(self.Raw_Selected_Org_600nm,color)
        elif color == "Red":
            self.RawAvg(self.Raw_Selected_Red_650nm,color)
            
        pass  # end of allowableDeviation function
    def RawAvg(self,Raw_Selected,color):
        Raw_Selected_len = len(Raw_Selected)
        if Raw_Selected_len >= 1:
            #Sum the Array
            SumOfValues = 0
            for GoodValue in Raw_Selected:
                SumOfValues = SumOfValues + GoodValue
            if color == "Vio":
                self.Raw_Avg_Vio_450nm = SumOfValues/Raw_Selected_len
                self.Raw_Avg_Vio_450nm = round(self.Raw_Avg_Vio_450nm,2)
                self.RawStdDev(Raw_Selected,color)
                
            elif color == "Blu":
                self.Raw_Avg_Blu_500nm = SumOfValues/Raw_Selected_len
                self.Raw_Avg_Blu_500nm = round(self.Raw_Avg_Blu_500nm,2)
                self.RawStdDev(Raw_Selected,color)
                
            elif color == "Grn":
                self.Raw_Avg_Grn_550nm = SumOfValues/Raw_Selected_len
                self.Raw_Avg_Grn_550nm = round(self.Raw_Avg_Grn_550nm,2)
                self.RawStdDev(Raw_Selected,color)
                
            elif color == "Yel":
                self.Raw_Avg_Yel_570nm = SumOfValues/Raw_Selected_len
                self.Raw_Avg_Yel_570nm = round(self.Raw_Avg_Yel_570nm,2)
                self.RawStdDev(Raw_Selected,color)
                
            elif color == "Org":
                self.Raw_Avg_Org_600nm = SumOfValues/Raw_Selected_len
                self.Raw_Avg_Org_600nm = round(self.Raw_Avg_Org_600nm,2)
                self.RawStdDev(Raw_Selected,color)
                
            elif color == "Red":
                self.Raw_Avg_Red_650nm = SumOfValues/Raw_Selected_len
                self.Raw_Avg_Red_650nm = round(self.Raw_Avg_Red_650nm,2)
                self.RawStdDev(Raw_Selected,color)
                
        pass   # end of RawAvg function
    def RawStdDev(self,Raw_Selected,color):
        if color == "Vio":
            self.Raw_StdDev_Vio_450nm = statistics.stdev(Raw_Selected)
            self.Raw_StdDev_Vio_450nm = round(self.Raw_StdDev_Vio_450nm,2)
            
        elif color == "Blu":
            self.Raw_StdDev_Blu_500nm = statistics.stdev(Raw_Selected)
            self.Raw_StdDev_Blu_500nm = round(self.Raw_StdDev_Blu_500nm,2)
            
        elif color == "Grn":
            self.Raw_StdDev_Grn_550nm = statistics.stdev(Raw_Selected)
            self.Raw_StdDev_Grn_550nm = round(self.Raw_StdDev_Grn_550nm,2)
            
        elif color == "Yel":
            self.Raw_StdDev_Yel_570nm = statistics.stdev(Raw_Selected)
            self.Raw_StdDev_Yel_570nm = round(self.Raw_StdDev_Yel_570nm,2)

        elif color == "Org":
            self.Raw_StdDev_Org_600nm = statistics.stdev(Raw_Selected)
            self.Raw_StdDev_Org_600nm = round(self.Raw_StdDev_Org_600nm,2)
            
        elif color == "Red":
            self.Raw_StdDev_Red_650nm = statistics.stdev(Raw_Selected)
            self.Raw_StdDev_Red_650nm = round(self.Raw_StdDev_Red_650nm,2)
            
        
        pass   # end of StdDev function
    def CalFormulas(self,Cal_List_Of,color):   # Write (Cal_List_(Color),str(Color)) 
        # ---- All Color ---- #
        # --- For round Values ----#
        Cal_List_Of_Rounded = []
        for Cal in Cal_List_Of: # loop for get round values
            Cal_List_Of_Rounded.append(round(Cal,2))
        Cal_List_Of = Cal_List_Of_Rounded
        #---------------------------------------------------------------------#
        for Outer_i, RefDataPtr in enumerate (Cal_List_Of):
            CountOfCloseOnes = 0
            for Inner_i, TestDataPtr in enumerate(Cal_List_Of):
                if Outer_i != Inner_i:
                    if abs(RefDataPtr - TestDataPtr) < allowableDev:
                        # Good one, count it
                        CountOfCloseOnes += 1
            if CountOfCloseOnes >= 3:
                if color == "Vio":
                    self.Cal_Used_Vio.append(round(RefDataPtr,2))
                    self.Cal_Values_Vio_450nm = Cal_List_Of
                    self.Cal_Selected_Vio_450nm.append(round(RefDataPtr,2))
                    
                elif color == "Blu":
                    self.Cal_Used_Blu.append(round(RefDataPtr,2))
                    self.Cal_Values_Blu_500nm = Cal_List_Of
                    self.Cal_Selected_Blu_500nm.append(round(RefDataPtr,2))
                    
                elif color == "Grn":
                    self.Cal_Used_Grn.append(round(RefDataPtr,2))
                    self.Cal_Values_Grn_550nm = Cal_List_Of
                    self.Cal_Selected_Grn_550nm.append(round(RefDataPtr,2))
                    
                elif color == "Yel":
                    self.Cal_Used_Yel.append(round(RefDataPtr,2))
                    self.Cal_Values_Yel_570nm = Cal_List_Of
                    self.Cal_Selected_Yel_570nm.append(round(RefDataPtr,2))
                    
                elif color == "Org":
                    self.Cal_Used_Org.append(round(RefDataPtr,2))
                    self.Cal_Values_Org_600nm = Cal_List_Of
                    self.Cal_Selected_Org_600nm.append(round(RefDataPtr,2))
                    
                elif color == "Red":
                    self.Cal_Used_Red.append(round(RefDataPtr,2))
                    self.Cal_Values_Red_650nm = Cal_List_Of
                    self.Cal_Selected_Red_650nm.append(round(RefDataPtr,2))
        #-------------------------------------Average --------------------------------------------#
        if color == "Vio":
            self.CalAvg(self.Cal_Selected_Vio_450nm,color)
            
        elif color == "Blu":
            self.CalAvg(self.Cal_Selected_Blu_500nm,color)
            
        elif color == "Grn":
            self.CalAvg(self.Cal_Selected_Grn_550nm,color)
            
        elif color == "Yel":
            self.CalAvg(self.Cal_Selected_Yel_570nm,color)
            
        elif color == "Org":
            self.CalAvg(self.Cal_Selected_Org_600nm,color)
            
        elif color == "Red":
            self.CalAvg(self.Cal_Selected_Red_650nm,color)
            
        pass  # end of allowableDeviation function
    def CalAvg(self,Cal_Selected,color):
        Cal_Selected_len = len(Cal_Selected)
        if Cal_Selected_len >= 1:
            #Sum the Array
            SumOfValues = 0
            for GoodValue in Cal_Selected:
                SumOfValues = SumOfValues + GoodValue
            if color == "Vio":
                self.Cal_Avg_Vio_450nm = SumOfValues/Cal_Selected_len
                self.Cal_Avg_Vio_450nm = round(self.Cal_Avg_Vio_450nm,2)
                self.CalStdDev(Cal_Selected,color)
            elif color == "Blu":
                self.Cal_Avg_Blu_500nm = SumOfValues/Cal_Selected_len
                self.Cal_Avg_Blu_500nm = round(self.Cal_Avg_Blu_500nm,2)
                self.CalStdDev(Cal_Selected,color)
            elif color == "Grn":
                self.Cal_Avg_Grn_550nm = SumOfValues/Cal_Selected_len
                self.Cal_Avg_Grn_550nm = round(self.Cal_Avg_Grn_550nm,2)
                self.CalStdDev(Cal_Selected,color)
            elif color == "Yel":
                self.Cal_Avg_Yel_570nm = SumOfValues/Cal_Selected_len
                self.Cal_Avg_Yel_570nm = round(self.Cal_Avg_Yel_570nm,2)
                self.CalStdDev(Cal_Selected,color)
            elif color == "Org":
                self.Cal_Avg_Org_600nm = SumOfValues/Cal_Selected_len
                self.Cal_Avg_Org_600nm = round(self.Cal_Avg_Org_600nm,2)
                self.CalStdDev(Cal_Selected,color)
            elif color == "Red":
                self.Cal_Avg_Red_650nm = SumOfValues/Cal_Selected_len
                self.Cal_Avg_Red_650nm = round(self.Cal_Avg_Red_650nm,2)
                self.CalStdDev(Cal_Selected,color)
        pass   # end of CalAvg function
    def CalStdDev(self,Cal_Selected,color):
        if color == "Vio":
            self.Cal_StdDev_Vio_450nm = statistics.stdev(Cal_Selected)
            self.Cal_StdDev_Vio_450nm = round(self.Cal_StdDev_Vio_450nm,2)
            self.PrintInCsvData(color)
            
        elif color == "Blu":
            self.Cal_StdDev_Blu_500nm = statistics.stdev(Cal_Selected)
            self.Cal_StdDev_Blu_500nm = round(self.Cal_StdDev_Blu_500nm,2)
            self.PrintInCsvData(color)
            
        elif color == "Grn":
            self.Cal_StdDev_Grn_550nm = statistics.stdev(Cal_Selected)
            self.Cal_StdDev_Grn_550nm = round(self.Cal_StdDev_Grn_550nm,2)
            self.PrintInCsvData(color)
            
        elif color == "Yel":
            self.Cal_StdDev_Yel_570nm = statistics.stdev(Cal_Selected)
            self.Cal_StdDev_Yel_570nm = round(self.Cal_StdDev_Yel_570nm,2)
            self.PrintInCsvData(color)
            
        elif color == "Org":
            self.Cal_StdDev_Org_600nm = statistics.stdev(Cal_Selected)
            self.Cal_StdDev_Org_600nm = round(self.Cal_StdDev_Org_600nm,2)
            self.PrintInCsvData(color)
            
        elif color == "Red":
            self.Cal_StdDev_Red_650nm = statistics.stdev(Cal_Selected)
            self.Cal_StdDev_Red_650nm = round(self.Cal_StdDev_Red_650nm,2)
            self.PrintInCsvData(color)
            
        pass   # end of StdDev function

    def basicInfo(self,genData):
        self.genData = genData
        print(f"Basic Data : {self.genData}")
        pass   # end of basicInfo
    def openCsv(self):
        self.df = pd.read_csv("./Matrix_Data/" +self.Csv.logname)
        self.columnNum = 0
        self.rowNum += 1
        pass   # end of openCsv function
    def closeCsv(self):
        self.df.to_csv("./Matrix_Data/" +self.Csv.logname,index=False)
        pass   # end of openCsv function
    
    def PrintInCsvData(self,color):    
        if color == "Vio":
            self.openCsv() # Read the existing CSV file into a DataFrame as self.df object
            # ------ Enter General Data in csv File -------#
            for i in range(0,len(self.genData)):
                self.columnNum = i
                self.df.at[self.rowNum,column[self.columnNum]] = self.genData[self.columnNum]
            # ------ Enter Raw Vio Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Used_Vio
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Values_Vio_450nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Selected_Vio_450nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Avg_Vio_450nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_StdDev_Vio_450nm
            # ------ Enter Cal Vio Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Used_Vio
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Values_Vio_450nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Selected_Vio_450nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Avg_Vio_450nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_StdDev_Vio_450nm
            # ------------Printing General Data --------------#
            print(f"General Data : {self.genData}")
            #------------ Printing Violet Raw Data -----------#
            print(f"Raw_Used_Vio : {self.Raw_Used_Vio}")
            print(f"Raw_Values_Vio_450nm : {self.Raw_Values_Vio_450nm}")
            print(f"Raw_Selected_Vio_450nm : {self.Raw_Selected_Vio_450nm}")
            print(f"Raw_Avg_Vio_450nm : {self.Raw_Avg_Vio_450nm}")
            print(f"Raw StdDev of Selected Violet value is : {self.Raw_StdDev_Vio_450nm}")
            #------------ Printing Violet Cal Data -----------#
            print(f"Cal_Used_Vio : {self.Cal_Used_Vio}")
            print(f"Cal_Values_Vio_450nm : {self.Cal_Values_Vio_450nm}")
            print(f"Cal_Selected_Vio_450nm : {self.Cal_Selected_Vio_450nm}")
            print(f"Cal_Avg_Vio_450nm : {self.Cal_Avg_Vio_450nm}")
            print(f"Cal StdDev of Selected Violet value is : {self.Cal_StdDev_Vio_450nm}")
        elif color == "Blu":
            # ------ Enter Cal Blu Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Used_Blu
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Values_Blu_500nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Selected_Blu_500nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Avg_Blu_500nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_StdDev_Blu_500nm
            # ------ Enter Cal Blu Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Used_Blu
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Values_Blu_500nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Selected_Blu_500nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Avg_Blu_500nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_StdDev_Blu_500nm
            #------------ Printing Blue Raw Data -----------#
            print(f"Raw_Used_Blu : {self.Raw_Used_Blu}")
            print(f"Raw_Values_Blu_500nm : {self.Raw_Values_Blu_500nm}")
            print(f"Raw_Selected_Blu_500nm : {self.Raw_Selected_Blu_500nm}")
            print(f"Raw_Avg_Blu_500nm : {self.Raw_Avg_Blu_500nm}")
            print(f"Raw StdDev of Selected Blue value is : {self.Raw_StdDev_Blu_500nm}")
            #------------ Printing Blue Cal Data -----------#
            print(f"Cal_Used_Blu : {self.Cal_Used_Blu}")
            print(f"Cal_Values_Blu_500nm : {self.Cal_Values_Blu_500nm}")
            print(f"Cal_Selected_Blu_500nm : {self.Cal_Selected_Blu_500nm}")
            print(f"Cal_Avg_Blu_500nm : {self.Cal_Avg_Blu_500nm}")
            print(f"Cal StdDev of Selected Blue value is : {self.Cal_StdDev_Blu_500nm}")
        elif color == "Grn":
            # ------ Enter Cal Green Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Used_Grn
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Values_Grn_550nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Selected_Grn_550nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Avg_Grn_550nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_StdDev_Grn_550nm
            # ------ Enter Cal Green Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Used_Grn
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Values_Grn_550nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Selected_Grn_550nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Avg_Grn_550nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_StdDev_Grn_550nm
            #------------ Printing Green Raw Data -----------#
            print(f"Raw_Used_Grn : {self.Raw_Used_Grn}")
            print(f"Raw_Values_Grn_550nm : {self.Raw_Values_Grn_550nm}")
            print(f"Raw_Selected_Grn_550nm : {self.Raw_Selected_Grn_550nm}")
            print(f"Raw_Avg_Grn_550nm : {self.Raw_Avg_Grn_550nm}")
            print(f"Raw StdDev of Selected Green value is : {self.Raw_StdDev_Grn_550nm}")
            #------------ Printing Green Cal Data -----------#
            print(f"Cal_Used_Grn : {self.Cal_Used_Grn}")
            print(f"Cal_Values_Grn_550nm : {self.Cal_Values_Grn_550nm}")
            print(f"Cal_Selected_Grn_550nm : {self.Cal_Selected_Grn_550nm}")
            print(f"Cal_Avg_Grn_550nm : {self.Cal_Avg_Grn_550nm}")
            print(f"Cal StdDev of Selected Green value is : {self.Cal_StdDev_Grn_550nm}")
        elif color == "Yel":
            # ------ Enter Cal Yellow Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Used_Yel
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Values_Yel_570nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Selected_Yel_570nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Avg_Yel_570nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_StdDev_Yel_570nm
            # ------ Enter Cal Green Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Used_Yel
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Values_Yel_570nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Selected_Yel_570nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Avg_Yel_570nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_StdDev_Yel_570nm
            #------------ Printing Yellow Raw Data -----------#
            print(f"Raw_Used_Yel : {self.Raw_Used_Yel}")
            print(f"Raw_Values_Yel_570nm : {self.Raw_Values_Yel_570nm}")
            print(f"Raw_Selected_Yel_570nm : {self.Raw_Selected_Yel_570nm}")
            print(f"Raw_Avg_Yel_570nm : {self.Raw_Avg_Yel_570nm}")
            print(f"Raw StdDev of Selected Yellow value is : {self.Raw_StdDev_Yel_570nm}")
            #------------ Printing Yellow Cal Data -----------#
            print(f"Cal_Used_Yel : {self.Cal_Used_Yel}")
            print(f"Cal_Values_Yel_570nm : {self.Cal_Values_Yel_570nm}")
            print(f"Cal_Selected_Yel_570nm : {self.Cal_Selected_Yel_570nm}")
            print(f"Cal_Avg_Yel_570nm : {self.Cal_Avg_Yel_570nm}")
            print(f"Cal StdDev of Selected Yellow value is : {self.Cal_StdDev_Yel_570nm}")
        elif color == "Org":
            # ------ Enter Cal Orange Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Used_Org
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Values_Org_600nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Selected_Org_600nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Avg_Org_600nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_StdDev_Org_600nm
            # ------ Enter Cal Orange Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Used_Org
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Values_Org_600nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Selected_Org_600nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Avg_Org_600nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_StdDev_Org_600nm
            #------------ Printing Orange Raw Data -----------#
            print(f"Raw_Used_Org : {self.Raw_Used_Org}")
            print(f"Raw_Values_Org_600nm : {self.Raw_Values_Org_600nm}")
            print(f"Raw_Selected_Org_600nm : {self.Raw_Selected_Org_600nm}")
            print(f"Raw_Avg_Org_600nm : {self.Raw_Avg_Org_600nm}")
            print(f"Raw StdDev of Selected Orange value is : {self.Raw_StdDev_Org_600nm}")
            #------------ Printing Orange Cal Data -----------#
            print(f"Cal_Used_Org : {self.Cal_Used_Org}")
            print(f"Cal_Values_Org_600nm : {self.Cal_Values_Org_600nm}")
            print(f"Cal_Selected_Org_600nm : {self.Cal_Selected_Org_600nm}")
            print(f"Cal_Avg_Org_600nm : {self.Cal_Avg_Org_600nm}")
            print(f"Cal StdDev of Selected Orange value is : {self.Cal_StdDev_Org_600nm}")
        elif color == "Red":
            # ------ Enter Cal Red Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Used_Red
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Values_Red_650nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Selected_Red_650nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_Avg_Red_650nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Raw_StdDev_Red_650nm
            # ------ Enter Cal Red Data in csv File -------#
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Used_Red
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Values_Red_650nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Selected_Red_650nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_Avg_Red_650nm
            self.columnNum += 1
            self.df.at[self.rowNum,column[self.columnNum]] = self.Cal_StdDev_Red_650nm
            #------------ Printing Red Raw Data -----------#
            print(f"Raw_Used_Red : {self.Raw_Used_Red}")
            print(f"Raw_Values_Red_650nm : {self.Raw_Values_Red_650nm}")
            print(f"Raw_Selected_Red_650nm : {self.Raw_Selected_Red_650nm}")
            print(f"Raw_Avg_Red_650nm : {self.Raw_Avg_Red_650nm}")
            print(f"Raw StdDev of Selected Red value is : {self.Raw_StdDev_Red_650nm}")
            #------------ Printing Red Cal Data -----------#
            print(f"Cal_Used_Red : {self.Cal_Used_Red}")
            print(f"Cal_Values_Red_650nm : {self.Cal_Values_Red_650nm}")
            print(f"Cal_Selected_Red_650nm : {self.Cal_Selected_Red_650nm}")
            print(f"Cal_Avg_Red_650nm : {self.Cal_Avg_Red_650nm}")
            print(f"Cal StdDev of Selected Red value is : {self.Cal_StdDev_Red_650nm}")
            self.closeCsv()
            self.ClearAll()
        pass   # end of Print function
    def ClearAll(self):
        #---------- Clear All Data From Violet Raw Lists --------#
        self.Raw_Used_Vio = []
        self.Raw_Values_Vio_450nm = []
        self.Raw_Selected_Vio_450nm = []
        self.Raw_Avg_Vio_450nm = 0
        self.Raw_StdDev_Vio_450nm = 0
        #---------- Clear All Data From Blue Raw Lists --------#
        self.Raw_Used_Blu = []
        self.Raw_Values_Blu_500nm = []
        self.Raw_Selected_Blu_500nm = []
        self.Raw_Avg_Blu_500nm = 0
        self.Raw_StdDev_Blu_500nm = 0
        #---------- Clear All Data From Green Raw Lists --------#
        self.Raw_Used_Grn = []
        self.Raw_Values_Grn_550nm = []
        self.Raw_Selected_Grn_550nm = []
        self.Raw_Avg_Grn_550nm = 0
        self.Raw_StdDev_Grn_550nm = 0
        #---------- Clear All Data From Yellow Raw Lists --------#
        self.Raw_Used_Yel = []
        self.Raw_Values_Yel_570nm = []
        self.Raw_Selected_Yel_570nm = []
        self.Raw_Avg_Yel_570nm = 0
        self.Raw_StdDev_Yel_570nm = 0
        #---------- Clear All Data From Orange Raw Lists --------#
        self.Raw_Used_Org = []
        self.Raw_Values_Org_600nm = []
        self.Raw_Selected_Org_600nm = []
        self.Raw_Avg_Org_600nm = 0
        self.Raw_StdDev_Org_600nm = 0
        #---------- Clear All Data From Red Raw Lists --------#
        self.Raw_Used_Red = []
        self.Raw_Values_Red_650nm = []
        self.Raw_Selected_Red_650nm = []
        self.Raw_Avg_Red_650nm = 0
        self.Raw_StdDev_Red_650nm = 0
        # -------------------------------------------------------------------------------------------#
        #---------- Clear All Data From Violet Cal Lists --------#
        self.Cal_Used_Vio = []
        self.Cal_Values_Vio_450nm = []
        self.Cal_Selected_Vio_450nm = []
        self.Cal_Avg_Vio_450nm = 0
        self.Cal_StdDev_Vio_450nm = 0
        #---------- Clear All Data From Blue Cal Lists --------#
        self.Cal_Used_Blu = []
        self.Cal_Values_Blu_500nm = []
        self.Cal_Selected_Blu_500nm = []
        self.Cal_Avg_Blu_500nm = 0
        self.Cal_StdDev_Blu_500nm = 0
        #---------- Clear All Data From Green Cal Lists --------#
        self.Cal_Used_Grn = []
        self.Cal_Values_Grn_550nm = []
        self.Cal_Selected_Grn_550nm = []
        self.Cal_Avg_Grn_550nm = 0
        self.Cal_StdDev_Grn_550nm = 0
        #---------- Clear All Data From Yellow Cal Lists --------#
        self.Cal_Used_Yel = []
        self.Cal_Values_Yel_570nm = []
        self.Cal_Selected_Yel_570nm = []
        self.Cal_Avg_Yel_570nm = 0
        self.Cal_StdDev_Yel_570nm = 0
        #---------- Clear All Data From Orange Cal Lists --------#
        self.Cal_Used_Org = []
        self.Cal_Values_Org_600nm = []
        self.Cal_Selected_Org_600nm = []
        self.Cal_Avg_Org_600nm = 0
        self.Cal_StdDev_Org_600nm = 0
        #---------- Clear All Data From Red Cal Lists --------#
        self.Cal_Used_Red = []
        self.Cal_Values_Red_650nm = []
        self.Cal_Selected_Red_650nm = []
        self.Cal_Avg_Red_650nm = 0
        self.Cal_StdDev_Red_650nm = 0
        # ------------Cear General Data -----------#
        self.genData = ""
        pass   # end of Clear function
    pass   # end of DataStructure class

if __name__ == "__main__":
    data = DataStructure()
    data.basicInfo([0,1,"Time Stamp",9.5,34,64,700,150])
    data.basicInfo([0,1,"Time Stamp",9.5,34,64,700,150])