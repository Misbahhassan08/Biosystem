import smbus
class LEDs:
    bus = smbus.SMBus(1)
    def __init__(self):
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
        time.sleep(0.1)
        json_string = json.dumps(data)
        return json_string
        #self.client.publish("biogas/ledsensor/",json_string)
        pass   # end of selectAndSet function
    def writeOnLed(self,ledNum,PosSel,LED_Current_Val):
        time.sleep(.2)  
        self.bus.write_byte_data(self.BoardAndChipAddress,0x04,PosSel) # LED-Detector pcb address
        time.sleep(.2)
        self.bus.write_byte_data(0x2E,0x00,LED_Current_Val) # Write to Wiper 0, Volatile
        time.sleep(.2)
        #---- Vol Wiper 0 Register read
        Vol_Wiper0 = self.bus.read_word_data(0x2E,0x0C) # Addr = 0h in Read Mode
        time.sleep(0.2)
        print(f"LED {ledNum} Current Changed With Acknowledge Register Vol_wiper0", Vol_Wiper0)
        pass  # end of writeOnLed function
    pass   # end of LEDs class