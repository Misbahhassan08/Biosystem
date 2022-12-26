import pigpio
from PigpioStepperMotor import StepperMotor

pi = pigpio.pi()
motor = StepperMotor(pi, 6, 13, 19, 26)
for i in range(1000):
    motor.doСlockwiseStep()


