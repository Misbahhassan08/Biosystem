from dataStructure import DataStructure
from sensors import Sensor
import threading
import datetime
import keyboard
import board
import smbus
import json
import time
import sys

class Main:
    #---------classes Objects----------#
    dataStruct = DataStructure() # make Data structure class object
    sensor = Sensor() # make sensor class object
    
    def __init__(self):
        self.sensor.ColorDataSignal.connect(self.ColorData)
        self.sensor.GenDataSignal.connect(self.GenData)
        self.sensor.AckSignal.connect(self.AckFunc)
        self.init_parameters()
        pass   # end of Main class constructor
    def init_parameters(self):
        
        self.Raw_List_Vio = []
        self.Raw_List_Blu = []
        self.Raw_List_Grn = []
        self.Raw_List_Yel = []
        self.Raw_List_Org = []
        self.Raw_List_Red = []
        
        self.Cal_List_Vio = []
        self.Cal_List_Blu = []
        self.Cal_List_Grn = []
        self.Cal_List_Yel = []
        self.Cal_List_Org = []
        self.Cal_List_Red = []
        
        self.genData = []
        self.Raw = "Raw"
        self.Cal = "Cal"
        self.ack_is = False
        pass   # end of init_parameters function
    
    def ColorData(self,data,color,Type): # data = list[Data] , color = colorName , Type = Raw|Cal|Gen
        if color == "Vio":
            if Type == self.Raw:
                self.Raw_List_Vio = data
                print(f"Vio Raw : {self.Raw_List_Vio}")
            elif Type == self.Cal:
                self.Cal_List_Vio = data
                print(f"Vio Cal : {self.Cal_List_Vio}")
        elif color == "Blu":
            if Type == self.Raw:
                self.Raw_List_Blu = data
                print(f"Blu Raw : {self.Raw_List_Blu}")
            elif Type == self.Cal:
                self.Cal_List_Blu = data
                print(f"Blu Cal : {self.Cal_List_Blu}")
        elif color == "Grn":
            if Type == self.Raw:
                self.Raw_List_Grn = data
                print(f"Grn Raw : {self.Raw_List_Grn}")
            elif Type == self.Cal:
                self.Cal_List_Grn = data
                print(f"Grn Cal : {self.Cal_List_Grn}")
        elif color == "Yel":
            if Type == self.Raw:
                self.Raw_List_Yel = data
                print(f"Yel Raw : {self.Raw_List_Yel}")
            elif Type == self.Cal:
                self.Cal_List_Yel = data
                print(f"Yel Cal : {self.Cal_List_Yel}")
        elif color == "Org":
            if Type == self.Raw:
                self.Raw_List_Org = data
                print(f"Org Raw : {self.Raw_List_Org}")
            elif Type == self.Cal:
                self.Cal_List_Org = data
                print(f"Org Cal : {self.Cal_List_Org}")
        elif color == "Red":
            if Type == self.Raw:
                self.Raw_List_Red = data
                print(f"Red Raw : {self.Raw_List_Red}")
            elif Type == self.Cal:
                self.Cal_List_Red = data
                print(f"Red Cal : {self.Cal_List_Red}")
        #print(f"data is : {data}")
        #print(f"name is : {name}")
        #print(f"name is : {Type}")
        pass   # end of colorData Function
    def GenData(self,genData): # data = list[Data] , color = colorName , Type = Raw|Cal|Gen
        self.genData = genData
        #print(f"General Data is : {self.genData}")
        pass   # end of GenData Function
    def AckFunc(self,Bool):
        self.ack_is = Bool
        pass   # end of AckFunc function
    
    def func(self):
        print("...........................................................Main Thread is ruuning ......")
        while True:
            if self.ack_is:
                self.dataStructureFunc()
                self.ack_is = False
            pass
        pass   # end of func function
    def dataStructureFunc(self):
        self.dataStruct.basicInfo(self.genData)
        print(f"General Data to data Structure : {self.genData}")
        
        #-----------------Raw Lists And Cal Lists To Formula And Save in csv File-----------------#
        self.dataStruct.RawFormulas(self.Raw_List_Vio,"Vio")
        print(f"Vio Raw data Structure : {self.Raw_List_Vio}")
        
        self.dataStruct.CalFormulas(self.Cal_List_Vio,"Vio")
        print(f"Vio Call data Structure : {self.Cal_List_Vio}")
        
        self.dataStruct.RawFormulas(self.Raw_List_Blu,"Blu")
        print(f"Blu Raw data Structure : {self.Raw_List_Blu}")
        
        self.dataStruct.CalFormulas(self.Cal_List_Blu,"Blu")
        print(f"Blu Call data Structure : {self.Cal_List_Blu}")
        
        self.dataStruct.RawFormulas(self.Raw_List_Grn,"Grn")
        print(f"Blu Raw data Structure : {self.Raw_List_Grn}")
        
        self.dataStruct.CalFormulas(self.Cal_List_Grn,"Grn")
        print(f"Grn Call data Structure : {self.Cal_List_Grn}")
        
        self.dataStruct.RawFormulas(self.Raw_List_Yel,"Yel")
        print(f"Yel Raw data Structure : {self.Raw_List_Yel}")
        
        self.dataStruct.CalFormulas(self.Cal_List_Yel,"Yel")
        print(f"Yel Call data Structure : {self.Cal_List_Yel}")
        
        self.dataStruct.RawFormulas(self.Raw_List_Org,"Org")
        print(f"Org Raw data Structure : {self.Raw_List_Org}")
        
        self.dataStruct.CalFormulas(self.Cal_List_Org,"Org")
        print(f"Org Call data Structure : {self.Cal_List_Org}")
        
        self.dataStruct.RawFormulas(self.Raw_List_Red,"Red")
        print(f"Red Raw data Structure : {self.Raw_List_Red}")
        
        self.dataStruct.CalFormulas(self.Cal_List_Red,"Red")
        print(f"Red Call data Structure : {self.Cal_List_Red}")
        
        pass  # end of dataStructureFunc function
    def clearAll(self):
        self.genData = []
        
        self.Raw_List_Vio = []
        self.Raw_List_Blu = []
        self.Raw_List_Grn = []
        self.Raw_List_Yel = []
        self.Raw_List_Org = []
        self.Raw_List_Red = []
        
        self.Cal_List_Vio = [] 
        self.Cal_List_Blu = []
        self.Cal_List_Grn = []
        self.Cal_List_Yel = []
        self.Cal_List_Org = []
        self.Cal_List_Red = []
        
        pass   # end of clearAll function
    
    pass  # end of Main class

if __name__ == "__main__":
    main = Main()
    main.func()