from PySignal import Signal
from threading import Thread
from time import sleep

class Sender(Thread):
    sendSignal = Signal()
    def __init__(self):
        Thread.__init__(self)
        pass   # end of Sender class constructor
    def run(self):
        while True:
            print("Sender Thread is Running")
            sleep(1)
            self.sendSignal.emit("Hi I am Your Best Signal..........................................")
            
        pass   # end of send function
    pass  # end of Sender class
if __name__ == "__main__":
    sender = Sender()
    sender.start()
    