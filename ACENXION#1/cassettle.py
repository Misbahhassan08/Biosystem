# -*- coding: utf-8 -*-

from time import sleep                   #Para las pausas
import pigpio

class Cassettle:
    pi = pigpio.pi()
    def __init__(self):
        self.Dir = 20                     #Pin DIR
        self.Step = 21                    #Pin Step
        self.numSteps = 300                  #Númber of steps to be performmap
        self.microPausa = 0.005              #Number of pause time
        self.pi.set_mode(self.Dir, pigpio.OUTPUT)  # Set up pins as an output
        self.pi.set_mode(self.Step, pigpio.OUTPUT)
        pass    # end of  __init__ function
    def insert(self):
        self.pi.write(self.Dir, 0)  # Set direction clock wise
        for x in range(0,self.numSteps):
                self.pi.write(self.Step, True)
                sleep(self.microPausa)
                self.pi.write(self.Step, False)
                sleep(self.microPausa)
        pass   # end of close function
    def eject(self):
        self.pi.write(self.Dir, 1)          #Set direction counter clock wise
        for x in range(0,self.numSteps):
                self.pi.write(self.Step, True)
                sleep(self.microPausa)
                self.pi.write(self.Step, False)
                sleep(self.microPausa)
        pass   # end of eject function
    pass   # end of main class  Cassettle

if __name__ == "__main__":
    
    cassettle = Cassettle()
    cassettle.eject()
    sleep(1)
    cassettle.insert()
        
