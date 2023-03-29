from sender import Sender
from time import sleep

class Main:
    sender = Sender()
    def __init__(self):
        self.sender.sendSignal.connect(self.Test)
        self.sender.start()
        pass   # end of Main class constructor
    def func(self):
        while True:
            pass
        pass   # end of func function
    def Test(self,msg):
        print(f"Received Message is : {msg}")
        pass   # end of Test function
    pass   # end of Main class

if __name__ == "__main__":
    main = Main()
    main.func()