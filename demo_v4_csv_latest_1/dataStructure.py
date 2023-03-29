import sys
import csv
from Csv import CSV
class DataStructure:
    def __init__(self):
        self.Csv = CSV()
        self.Csv.createFile()
        self.allowableDev = 150
        self.Good_List_Vio = []
        self.Good_List_Blu = []
        self.Good_List_Grn = []
        self.Good_List_Yel = []
        self.Good_List_Org = []
        self.Good_List_Red = []
        self.AvgOfGood_Vio = 0
        self.AvgOfGood_Blu = 0
        self.AvgOfGood_Grn = 0
        self.AvgOfGood_Yel = 0
        self.AvgOfGood_Org = 0
        self.AvgOfGood_Red = 0
        self.rowData = ""
        self.countBufferFullAckn = 0
        pass  # end of DataStructure class constructor
    # - Evaluate the array of samples, and retain the "viable" samples
    def allowableDevWithAvg(self,Raw_List_Of,NumOfReadings,color):   # Write (Raw_List_(Color),str(Color)) 
        # ---- All Color ---- #
        print(f" Loop For Reading Number : {NumOfReadings}")
        for Outer_i, RefDataPtr in enumerate (Raw_List_Of):
            CountOfCloseOnes = 0
            for Inner_i, TestDataPtr in enumerate(Raw_List_Of):
                if Outer_i != Inner_i:
                    if abs(RefDataPtr - TestDataPtr) < self.allowableDev:
                        # Good one, count it
                        CountOfCloseOnes += 1
            if CountOfCloseOnes >= 3:
                if color == "Vio":
                    RefDataPtr_rounded = round(RefDataPtr,2)
                    self.Good_List_Vio.append(RefDataPtr_rounded)
                elif color == "Blu":
                    RefDataPtr_rounded = round(RefDataPtr,2)
                    self.Good_List_Blu.append(RefDataPtr_rounded)
                elif color == "Grn":
                    RefDataPtr_rounded = round(RefDataPtr,2)
                    self.Good_List_Grn.append(RefDataPtr_rounded)
                elif color == "Yel":
                    RefDataPtr_rounded = round(RefDataPtr,2)
                    self.Good_List_Yel.append(RefDataPtr_rounded)
                elif color == "Org":
                    RefDataPtr_rounded = round(RefDataPtr,2)
                    self.Good_List_Org.append(RefDataPtr_rounded)
                elif color == "Red":
                    RefDataPtr_rounded = round(RefDataPtr,2)
                    self.Good_List_Red.append(RefDataPtr_rounded)
        print("Starting Average")
        # For Loop for get rounded values of Raw_List_Of
        Raw_List_Of_Rounded = []
        for raw in Raw_List_Of:
            Raw_List_Of_Rounded.append(round(raw,2))
        if color == "Vio":
            self.avgOfColor(self.Good_List_Vio,Raw_List_Of_Rounded,NumOfReadings,"Vio")
            self.Good_List_Vio = []
        elif color == "Blu":
            self.avgOfColor(self.Good_List_Blu,Raw_List_Of_Rounded,NumOfReadings,"Blu")
            self.Good_List_Blu = []
        elif color == "Grn":
            self.avgOfColor(self.Good_List_Grn,Raw_List_Of_Rounded,NumOfReadings,"Grn")
            self.Good_List_Grn = []
        elif color == "Yel":
            self.avgOfColor(self.Good_List_Yel,Raw_List_Of_Rounded,NumOfReadings,"Yel")
            self.Good_List_Yel = []
        elif color == "Org":
            self.avgOfColor(self.Good_List_Org,Raw_List_Of_Rounded,NumOfReadings,"Org")
            self.Good_List_Org = []
        elif color == "Red":
            self.avgOfColor(self.Good_List_Red,Raw_List_Of_Rounded,NumOfReadings,"Red")
            self.Good_List_Red = []
        self.countBufferFullAckn += 1
        if self.countBufferFullAckn == 6:
            with open("./Matrix_Data/" + self.Csv.logname, 'a') as file:
                    #print('inside with statement inside add_results_to_file, writing to file')
                    writer = csv.writer(file)
                    file.write(self.rowData + '\n')
                    print("Result Added in Below File")
                    print(self.Csv.logname)
                    file.close()
            self.rowData = ""
            self.countBufferFullAckn = 0
        #print(f"After Allowable Deviation : {self.Good_List_Vio}")
        pass  # end of allowableDeviation function
    # - Average the remaining "good" ones
    def avgOfColor(self,Good_List_Of,Raw_List_Of_Rounded,NumOfReadings,color):
        GoodListLength_Of = len(Good_List_Of)
        print(f"Here is lenth of goods values : {GoodListLength_Of}")
        if GoodListLength_Of >= 1:
            #Sum the Array
            SumOfValues = 0
            for GoodValue in Good_List_Of:
                SumOfValues = SumOfValues + GoodValue
            if color == "Vio":
                self.rowData = self.rowData + ", " + str(GoodListLength_Of) + " of " + str(NumOfReadings)
                ListToStr = ""
                ListToStr = '/'.join(str(elem) for elem in Raw_List_Of_Rounded) # 1
                self.rowData = self.rowData + ", " + ListToStr # 2
                ListToStr = "" # 3
                ListToStr = '/'.join(str(elem) for elem in Good_List_Of) # 4
                self.rowData = self.rowData + ", " + ListToStr # 5
                ListToStr = ""
                self.AvgOfGood_Vio = SumOfValues/GoodListLength_Of
                self.AvgOfGood_Vio_Rounded = round(self.AvgOfGood_Vio,2)
                self.rowData = self.rowData + ", " + str(self.AvgOfGood_Vio_Rounded)
                print(f"Avrg of Vio is : {self.AvgOfGood_Vio_Rounded}")
            elif color == "Blu":
                self.rowData = self.rowData + "," + str(GoodListLength_Of) + " of " + str(NumOfReadings)
                ListToStr = ""
                ListToStr = '/'.join(str(elem) for elem in Raw_List_Of_Rounded) # 1
                self.rowData = self.rowData + ", " + ListToStr # 2
                ListToStr = "" # 3
                ListToStr = '/'.join(str(elem) for elem in Good_List_Of) # 4
                self.rowData = self.rowData + ", " + ListToStr # 5
                ListToStr = ""
                self.AvgOfGood_Blu = SumOfValues/GoodListLength_Of
                self.AvgOfGood_Blu_Rounded = round(self.AvgOfGood_Blu,2)
                self.rowData = self.rowData + ", " + str(self.AvgOfGood_Vio_Rounded)
                print(f"Avrg of Blu is : {self.AvgOfGood_Blu_Rounded}")
            elif color == "Grn":
                self.rowData = self.rowData + "," + str(GoodListLength_Of) + " of " + str(NumOfReadings)
                ListToStr = ""
                ListToStr = '/'.join(str(elem) for elem in Raw_List_Of_Rounded) # 1
                self.rowData = self.rowData + ", " + ListToStr # 2
                ListToStr = "" # 3
                ListToStr = '/'.join(str(elem) for elem in Good_List_Of) # 4
                self.rowData = self.rowData + ", " + ListToStr # 5
                ListToStr = ""
                self.AvgOfGood_Grn = SumOfValues/GoodListLength_Of
                self.AvgOfGood_Grn_Rounded = round(self.AvgOfGood_Grn,2)
                self.rowData = self.rowData + ", " + str(self.AvgOfGood_Vio_Rounded)
                print(f"Avrg of Grn is : {self.AvgOfGood_Grn_Rounded}")
            elif color == "Yel":
                self.rowData = self.rowData + "," + str(GoodListLength_Of) + " of " + str(NumOfReadings)
                ListToStr = ""
                ListToStr = '/'.join(str(elem) for elem in Raw_List_Of_Rounded) # 1
                self.rowData = self.rowData + ", " + ListToStr # 2
                ListToStr = "" # 3
                ListToStr = '/'.join(str(elem) for elem in Good_List_Of) # 4
                self.rowData = self.rowData + ", " + ListToStr # 5
                ListToStr = ""
                self.AvgOfGood_Yel = SumOfValues/GoodListLength_Of
                self.AvgOfGood_Yel_Rounded = round(self.AvgOfGood_Yel,2)
                self.rowData = self.rowData + ", " + str(self.AvgOfGood_Vio_Rounded)
                print(f"Avrg of Yel is : {self.AvgOfGood_Yel_Rounded}")
            elif color == "Org":
                self.rowData = self.rowData + "," + str(GoodListLength_Of) + " of " + str(NumOfReadings)
                ListToStr = ""
                ListToStr = '/'.join(str(elem) for elem in Raw_List_Of_Rounded) # 1
                self.rowData = self.rowData + ", " + ListToStr # 2
                ListToStr = "" # 3
                ListToStr = '/'.join(str(elem) for elem in Good_List_Of) # 4
                self.rowData = self.rowData + ", " + ListToStr # 5
                ListToStr = ""
                self.AvgOfGood_Org = SumOfValues/GoodListLength_Of
                self.AvgOfGood_Org_Rounded = round(self.AvgOfGood_Org,2)
                self.rowData = self.rowData + ", " + str(self.AvgOfGood_Vio_Rounded)
                print(f"Avrg of Org is : {self.AvgOfGood_Org_Rounded}")
            elif color == "Red":
                self.rowData = self.rowData + "," + str(GoodListLength_Of) + " of " + str(NumOfReadings)
                ListToStr = ""
                ListToStr = '/'.join(str(elem) for elem in Raw_List_Of_Rounded) # 1
                self.rowData = self.rowData + ", " + ListToStr # 2
                ListToStr = "" # 3
                ListToStr = '/'.join(str(elem) for elem in Good_List_Of) # 4
                self.rowData = self.rowData + ", " + ListToStr # 5
                ListToStr = ""
                self.AvgOfGood_Red = SumOfValues/GoodListLength_Of
                self.AvgOfGood_Red_Rounded = round(self.AvgOfGood_Red,2)
                self.rowData = self.rowData + ", " + str(self.AvgOfGood_Vio_Rounded)
                print(f"Avrg of Red is : {self.AvgOfGood_Red_Rounded}")
        pass   # end of avgOfColor function
    def basicInfo(self,basicData):
        i=0 # For Skipp first , in row of csv file
        for data in basicData:
            if i==0:
                self.rowData = self.rowData + str(data)
                i += 1
            else:
                self.rowData = self.rowData + "," + str(data)
        pass   # end of basicInfo
    pass   # end of DataStructure class