from dataStructure import DataStructure
import paho.mqtt.client as mqtt
from sensors import Sensor
import threading
import datetime
import keyboard
import board
import smbus
import json
import time
import sys

class Main(threading.Thread):
    #---------classes Objects----------#
    dataStruct = DataStructure() # make Data structure class object
    sensor = Sensor() # make sensor class object
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.sensor.ColorDataToSignal.connect(self.ColorDataFromSignal) # signal for Color's Data
        self.sensor.GenDataToSignal.connect(self.GenDataFromSignal) # signal for General Data
        self.sensor.AckBoolToSignal.connect(self.AckBoolFromSignal) # signal for ack = true for save data in csv file
        self.init_parameters()
        self.client = mqtt.Client()
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.start() # start mqtt thread
        pass   # end of Main class constructor
    def init_parameters(self):
        # Define Raw parameters --------
        self.Raw_List_Vio = []
        self.Raw_List_Blu = []
        self.Raw_List_Grn = []
        self.Raw_List_Yel = []
        self.Raw_List_Org = []
        self.Raw_List_Red = []
        # Define Cal parameters ---------
        self.Cal_List_Vio = []
        self.Cal_List_Blu = []
        self.Cal_List_Grn = []
        self.Cal_List_Yel = []
        self.Cal_List_Org = []
        self.Cal_List_Red = []
        # Define General variables ---------
        self.generalData = []
        self.Raw = "Raw"
        self.Cal = "Cal"
        self.ack_is = False
        pass   # end of init_parameters function
    # Main loop ---------
    def func(self):
        print("...........................................................Main Thread is ruuning ......")
        while True:
            if self.ack_is:   # if ack is True then data save in csv file
                self.dataStructureFunc()  # Save Data in csv File
                selectLastRow = self.dataStruct.df.tail(1) # Get latest data from dataFrame
                ignoredIndexNo = selectLastRow.reset_index(drop=True) # set row number to 0
                dicdata = ignoredIndexNo.to_dict() # convert to dictionary
                jsondata = json.dumps(dicdata) # convert dictionary to json formate
                self.client.publish("biogas_/pandas_/dataframe_/",jsondata) # publish json data
                self.ack_is = False # ack False for next data getting
            pass
        pass   # end of func function
    
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        pass   # end of on_connect function
    def on_message(self,client, userdata, msg):
        print("subscribed")
        self.msgTopic = msg.topic
        print(self.msgTopic)
    
    def run(self):
        # here will be mqtt thread
        print("Mqtt thread is runing")
        self.client.loop_forever()
        pass   # end of run function
    def ColorDataFromSignal(self,data,color,Type): # data = list[Data] , color = colorName , Type = Raw|Cal|Gen
        if color == "Vio":
            if Type == self.Raw:
                self.Raw_List_Vio = data # save data in desired list
                #print(f"Vio Raw : {self.Raw_List_Vio}")
            elif Type == self.Cal:
                self.Cal_List_Vio = data # save data in desired list
                #print(f"Vio Cal : {self.Cal_List_Vio}")
        elif color == "Blu":
            if Type == self.Raw:
                self.Raw_List_Blu = data # save data in desired list
                #print(f"Blu Raw : {self.Raw_List_Blu}")
            elif Type == self.Cal:
                self.Cal_List_Blu = data # save data in desired list
                #print(f"Blu Cal : {self.Cal_List_Blu}")
        elif color == "Grn":
            if Type == self.Raw:
                self.Raw_List_Grn = data # save data in desired list
                #print(f"Grn Raw : {self.Raw_List_Grn}")
            elif Type == self.Cal:
                self.Cal_List_Grn = data # save data in desired list
                #print(f"Grn Cal : {self.Cal_List_Grn}")
        elif color == "Yel":
            if Type == self.Raw:
                self.Raw_List_Yel = data # save data in desired list
                #print(f"Yel Raw : {self.Raw_List_Yel}")
            elif Type == self.Cal:
                self.Cal_List_Yel = data # save data in desired list
                #print(f"Yel Cal : {self.Cal_List_Yel}")
        elif color == "Org":
            if Type == self.Raw:
                self.Raw_List_Org = data # save data in desired list
                #print(f"Org Raw : {self.Raw_List_Org}")
            elif Type == self.Cal:
                self.Cal_List_Org = data # save data in desired list
                #print(f"Org Cal : {self.Cal_List_Org}")
        elif color == "Red":
            if Type == self.Raw:
                self.Raw_List_Red = data # save data in desired list
                #print(f"Red Raw : {self.Raw_List_Red}")
            elif Type == self.Cal:
                self.Cal_List_Red = data # save data in desired list
                #print(f"Red Cal : {self.Cal_List_Red}")
        #print(f"data is : {data}")
        #print(f"name is : {name}")
        #print(f"name is : {Type}")
        pass   # end of ColorDataFromSignal Function
    def GenDataFromSignal(self,GenDataFromSignal): # data = list[Data] , color = colorName , Type = Raw|Cal|Gen
        self.generalData = GenDataFromSignal
        #print(f"General Data is : {self.generalData}")
        pass   # end of GenDataFromSignal Function
    def AckBoolFromSignal(self,Bool):
        self.ack_is = Bool
        pass   # end of AckBoolFromSignal function
    
    
    def dataStructureFunc(self):
        self.dataStruct.basicInfo(self.generalData)
        print(f"General Data to data Structure : {self.generalData}")
        
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
    # Function clearAll for clear all list's to default
    def clearAll(self):
        # Clear GenDataFromSignal list
        self.generalData = []
        # Clear Raw data list's
        self.Raw_List_Vio = []
        self.Raw_List_Blu = []
        self.Raw_List_Grn = []
        self.Raw_List_Yel = []
        self.Raw_List_Org = []
        self.Raw_List_Red = []
        # Clear Cal data list's
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
    main.func() # go to main while loop