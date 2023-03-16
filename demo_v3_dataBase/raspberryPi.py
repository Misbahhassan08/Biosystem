import paho.mqtt.client as mqtt
from dataBase import DataBase
from sensors import Sensor
import threading
import board
import smbus
import json
import time
import sys

class Main(threading.Thread):
    client = mqtt.Client()
    sensor = Sensor()
    dataBase = DataBase()
    def __init__(self):
        threading.Thread.__init__(self)
        self.sensor.start()
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.subscribe("biogas_/database_/request_")
        self.msgTopic = None
        self.parsedJson = None
        self.requestIs = False
        self.machineID = 0
        pass   # end of Main class constructor
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        pass   # end of on_connect function
    def on_message(self,client, userdata, msg):
        print("subscribed")
        self.msgTopic = msg.topic
        print(f"Message Topic : {self.msgTopic}")
        self.parsedJson = json.loads(msg.payload)
        if self.parsedJson["machineID"] == self.machineID:
            self.requestIs = self.parsedJson["request"]
        else:
            print("machineID is wrong!!!")
            pass
        self.msgTopic = None
        pass   # edn of on_message function
    def run(self):
        print("thread is running")
        self.client.loop_forever()
        pass   # end of run function for mqtt forever loop threading
    def func(self):
        while True:
            if self.requestIs is True:
                self.dataBase.fetchData()
                time.sleep(1)
                LED0 = self.dataBase.updatedResult0
                LED1 = self.dataBase.updatedResult1
                LED2 = self.dataBase.updatedResult2
                LED3 = self.dataBase.updatedResult3
                LED4 = self.dataBase.updatedResult4
                data = [
                        {"LED0":self.dataStructure(LED0)},
                        {"LED1":self.dataStructure(LED1)},
                        {"LED2":self.dataStructure(LED2)},
                        {"LED3":self.dataStructure(LED3)},
                        {"LED4":self.dataStructure(LED4)}
                       ]
                data = json.dumps(data)
                self.client.publish("biogas_/database_/response_",data)
                print("Data Published!!!!!!!!!!!!!!!!!!!!!")
                self.dataBase.updateResul0 = None
                self.dataBase.updateResul1 = None
                self.dataBase.updateResul2 = None
                self.dataBase.updateResul3 = None
                self.dataBase.updateResul4 = None
                self.requestIs = False
            else:
                pass
        pass   # end of dataBase function
    def dataStructure(self,LED):
        setIn = ["Violet","Blue","Green","Yellow","Orange","Red","Temperature","Timestamp"]
        dic = {}
        arry = []
        for i in range(0,len(LED)):
            Led = LED[i]
            z=0
            for j in range(1,len(Led)):
                dic[setIn[z]] = Led[j]
                z += 1
            arry.append(dic)
        return arry
        pass   # end of dataStructure function
    pass  # end of Main class

if __name__ == "__main__":
    main = Main()
    main.start()
    main.func()