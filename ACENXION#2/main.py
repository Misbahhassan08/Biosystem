import sys
import pigpio
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from motor import Ui_mainScreen
from splashscreen import Ui_splashScreen
from PigpioStepperMotor import StepperMotor
from cassettle import Cassettle

class Main_screen(QtWidgets.QMainWindow, Ui_mainScreen):
    def __init__(self):
        super(Main_screen, self).__init__()
        self.setupUi(self)
        pass  # end of init function
    pass   # end of Main Class

class Splash_screen(QtWidgets.QMainWindow, Ui_splashScreen):
    def __init__(self):
        super(Splash_screen, self).__init__()
        self.setupUi(self)
        pass  # end of init function
    pass   # end of Main Class

class main(threading.Thread):
    pi = pigpio.pi()
    def __init__(self):
        threading.Thread.__init__(self)
        self.init()
        self.cassettle = Cassettle()
        self.main_screen = Main_screen()
        self.splash_screen = Splash_screen()
        self.splash_screen.showFullScreen()
        self.motor = StepperMotor(self.pi, 6, 13, 19, 26) 
        self.buttons_functions()
        pass    # end of init function
    def buttons_functions(self):
        self.splash_screen.pushButton.clicked.connect(self.main_screen_open)
        self.main_screen.back_btn.clicked.connect(self.back_To_splash_Screen)
        self.main_screen.open_door_2.clicked.connect(self.openDoor_1)
        self.main_screen.close_door_2.clicked.connect(self.closeDoor_1)
        self.main_screen.eject_cassettle_2.clicked.connect(self.cassettle.eject)
        self.main_screen.insert_cassettle_2.clicked.connect(self.cassettle.insert)
        pass    # end of buttons_functions
    
    def init(self):
        self.motor_speed = 5
        self.total_steps = 1000
        pass   # end of init function
    
    def cassettle_eject(self):
        self.cassettle._eject()
        pass   # end of cassettle_eject function
    
    def cassettle_close(self):
        self.cassettle._close()
        pass   # end of cassettle_eject function
    
    def back_To_splash_Screen(self):
        self.main_screen.close()
        self.splash_screen.showFullScreen()
        pass   #back_To_splash_Screen
    
    def openDoor_1(self):
        for i in range(self.total_steps):    
            self.motor.doСlockwiseStep(self.motor_speed)
        pass   # end of move right
    
    def closeDoor_1(self):
        for i in range(self.total_steps):
            self.motor.doСounterclockwiseStep(self.motor_speed)
        pass    # end of mive left
    
    def main_screen_open(self):
        self.splash_screen.close()
        self.main_screen.showFullScreen()
        pass   # end of main_screen_open
    
def _main():
    app = QtWidgets.QApplication(sys.argv)
    w = main()
    w.start()
    sys.exit(app.exec_())
    
    pass   # end of _main function
if __name__ == "__main__":
    _main()
    pass   # end of  __main__