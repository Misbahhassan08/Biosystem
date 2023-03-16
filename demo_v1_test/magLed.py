import paho.mqtt.client as mqtt
import threading
import random
import smbus
import json
import time


class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.leds = LEDs()
        self.client = mqtt.Client()
        self.client.connect("broker.emqx.io", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.start()
        pass   # end of ledControl class constructor
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe("biogas/led/brightness/")
        pass   # end of on_connect function
    def on_message(self,client, userdata, msg):
        print("subscribed")
        parsed_json = json.loads(msg.payload)
        ack = self.leds.selectAndSet(parsed_json["LED"],parsed_json["Value"])
        if ack is not None:
            self.client.publish("biogas/ledsensor/",ack)
        pass   # end of on_message function
    def run(self):
        print("thread is running")
        self.client.loop_forever()
        pass   # end of run function
class LEDs:
    bus = smbus.SMBus(1)
    def __init__(self,):
        self.BoardAndChipAddress = 0x71
        pass # end of LEDs class Constructor
    def selectAndSet(self,ledNum,LED_Current_Val):
        randInt = random.randint(0, 255)
        if ledNum == 0:
            PosSel = 0x01
            data = {
                    "Sensor": 0,
                    "Value": randInt
                    }
        elif ledNum == 1:
            PosSel = 0x02
            data = {
                    "Sensor": 1,
                    "Value": randInt
                    }
        elif ledNum == 2:
            PosSel = 0x04
            data = {
                    "Sensor": 2,
                    "Value": randInt
                    }
        elif ledNum == 3:
            PosSel = 0x08
            data = {
                    "Sensor": 3,
                    "Value": randInt
                    }
        elif ledNum == 4:
            PosSel = 0x10
            data = {
                    "Sensor": 4,
                    "Value": randInt
                    }
        else:
            data = {
                    "Sensor": "Wrong LED Select",
                    "Value": "No Value"
                    }
            json_string = json.dumps(data)
            #self.client.publish("biogas/ledsensor/",json_string)
            return json_string
        self.writeOnLed(ledNum,PosSel,LED_Current_Val)
        json_string = json.dumps(data)
        return json_string
        #self.client.publish("biogas/ledsensor/",json_string)
        pass   # end of selectAndSet function
    def writeOnLed(self,ledNum,PosSel,LED_Current_Val):
        time.sleep(.1)  
        self.bus.write_byte_data(self.BoardAndChipAddress,0x04,PosSel) # LED-Detector pcb address
        time.sleep(.2)
        self.bus.write_byte_data(0x2E,0x00,LED_Current_Val) # Write to Wiper 0, Volatile
        time.sleep(.1)
        #---- Vol Wiper 0 Register read
        Vol_Wiper0 = self.bus.read_word_data(0x2E,0x0C) # Addr = 0h in Read Mode
        time.sleep(0.1)
        print(f"LED {ledNum} Current Changed With Acknowledge Register Vol_wiper0", Vol_Wiper0)
        pass  # end of writeOnLed function
    pass   # end of LEDs class

class dcMotor:
    def __init__(self):
        pass# end of dcMotor class constructor
    pass   # end of dcMotor class
        
if __name__ == "__main__":
    main = Main()
    """
    val = 0
    pin = 0
    while i<5:
        ledcontrol.selectAndSet(pin,val)
        pin += 1
        """

