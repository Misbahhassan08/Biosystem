import sys
import pigpio
from PyQt5 import QtCore, QtGui, QtWidgets
from motor import Ui_MainWindow
from PigpioStepperMotor import StepperMotor
import threading

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
             
class _main(threading.Thread):
    pi = pigpio.pi()
    def __init__(self):
        threading.Thread.__init__(self)
        self.motor_speed = 5
        self.total_steps = 1
        self.gui = MainWindow()
        self.gui.showFullScreen()
        self.motor = StepperMotor(self.pi, 6, 13, 19, 26)
        self.gui.move_right.clicked.connect(self.move_Right)
        self.gui.move_left.clicked.connect(self.move_Left)
        self.gui.verticalScrollBar.sliderMoved.connect(self.sliderval)
        
        pass
    def sliderval(self):
        self.motor_speed = self.gui.verticalScrollBar.value()
        pass
    def move_Right(self):
        self.total_steps = self.gui.textEdit.toPlainText()
        self.gui.plainTextEdit.appendPlainText(f"##########  Direction : Right #########  Counts : {self.total_steps} ###########")
        print(self.total_steps)
        for i in range(int(self.total_steps)):    
            self.motor.doСlockwiseStep(self.motor_speed)
        pass
    def move_Left(self):
        self.total_steps = self.gui.textEdit.toPlainText()
        self.gui.plainTextEdit.appendPlainText(f"##########  Direction : Left ##########  Counts : {self.total_steps} ###########")
        for i in range(int(self.total_steps)):
            self.motor.doСounterclockwiseStep(self.motor_speed)
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = _main()
    w.start()
    sys.exit(app.exec_())
    pass
       
         

if __name__ == "__main__":
    
    main()
    pass