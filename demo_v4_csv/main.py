from config import *
import time
from setup import Setup
from basicEntryAndPrepForReading import BasicEntryAndPrepForReading
from preMixProcess import PreMixProcess
from runInProcess import RunInProcess
class Main:
    def __init__(self):
        self.setup = Setup()
        self.preMixProcess = PreMixProcess()
        self.runInProcess = RunInProcess()
        #self.entry = BasicEntryAndPrepForReading()
        pass   # end of Main class constructor
    def func(self):
        self.setup.Mixing("Setup PWM")
        self.setup.Mixing("RampUp To Full Speed")
        time.sleep(5)  # motor run for 5 second
        self.setup.Mixing("RampDnToParkSpeed")
        pass  # end of func function
    pass  # end of Main class

if __name__ == "__main__":
    main = Main()
    main.func()