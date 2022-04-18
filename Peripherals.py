import pigpio #importing GPIO library
import time
from spidev import SpiDev


class LeadScrew():

    __directionPin = None
    __speedPin = None
    __enablePin = None
    __pi = None
    __isEnabled = None
    __currentSpeed =  255
    __targetSpeed = 0;

    def __init__(self, pi, direction, step, enable) -> None:

        self.__pi = pi
        self.__directionPin = direction
        self.__speedPin = step
        self.__enablePin = enable

        self.__pi.write(self.__enablePin, 0)
        

        self.__pi.set_PWM_dutycycle(self.__speedPin, 127)

    def setSpeed(self, speed):

        tempSpeed = 400

        if speed > 20000:
            self.__targetSpeed = 11000

        elif speed <= 400:
            self.__targetSpeed = 11000
        else:

            self.__targetSpeed = speed


        if self.__targetSpeed > self.__currentSpeed:

            tempSpeed = self.__currentSpeed

            while tempSpeed < self.__targetSpeed:
                self.__pi.hardware_PWM(13, tempSpeed, 500000)
                tempSpeed = tempSpeed + 10
                time.sleep(.01)
        
            self.__currentSpeed = self.__targetSpeed
 
        if self.__targetSpeed < self.__currentSpeed:

            tempSpeed = self.__currentSpeed

            while tempSpeed > self.__targetSpeed:
                self.__pi.hardware_PWM(13, tempSpeed, 500000)
                tempSpeed = tempSpeed - 10
                print(tempSpeed)
                time.sleep(.02)
        
            self.__currentSpeed = self.__targetSpeed
        

        print(self.__pi.get_PWM_frequency(self.__speedPin))
        print(f"Set speed to: {self.__currentSpeed}")

    def increaseSpeed(self, amount):
        self.setSpeed(self.__currentSpeed + amount)

    def decreaseSpeed(self, amount):
        self.setSpeed(self.__currentSpeed - amount)

    def setDirection(self):

        if self.__pi.read(self.__directionPin) == 1:
            self.__targetSpeed = 400
            self.__currentSpeed = 400
            self.__pi.hardware_PWM(13, 400, 500000)
            print("Moving forward")
            self.__pi.write(self.__directionPin, 0)
            return

        if self.__pi.read(self.__directionPin) == 0:
            self.__targetSpeed = 400
            self.__currentSpeed = 400
            self.__pi.hardware_PWM(13, 400, 500000)
            print("Moving backwards")
            self.__pi.write(self.__directionPin, 1)
            return


    def getSpeed(self) -> int:
        return self.__currentSpeed

    def enable(self):
        print("LC: Enabling")


        if self.__pi.read(self.__enablePin) == 1:
            print("Disabling")
            self.__pi.write(self.__enablePin, 0)
            self.__pi.hardware_PWM(13, 400, 500000)
            self.__targetSpeed = 400
            self.__currentSpeed = 400
            return

        if self.__pi.read(self.__enablePin) == 0:
            print("enabling")
            self.__pi.write(self.__enablePin, 1)
            self.__pi.hardware_PWM(13, 400, 500000)
            self.__targetSpeed = 400
            self.__currentSpeed = 400
            return





class Motor():
    __dir = None
    __speed = None
    __pi = None
    __break = None
    __currSpeed = None

    def __init__(self, pi, sv, fr, brk):
        self.__pi = pi
        self.__speed = sv
        self.__dir = fr
        self.__break = brk
        self.__pi.set_mode(self.__dir, pigpio.OUTPUT)
        self.__pi.set_mode(self.__speed, pigpio.OUTPUT)
        self.__pi.set_mode(self.__break, pigpio.OUTPUT)
        self.__currSpeed = 0
        self.__pi.write(23, 0)

    def setSpeed(self, speed):
        if speed > 255:
            self.__currSpeed = 255
        elif speed <= 0:
            self.__currSpeed = 0
        else:
            self.__currSpeed = speed
        print(f"speed was set: {(self.__currSpeed / 255)}")
        self.__pi.set_PWM_dutycycle(self.__speed, self.__currSpeed)

    def speedUp(self, amount):
        self.setSpeed(self.__currSpeed + amount)

    def slowDown(self, amount):
        self.setSpeed(self.__currSpeed - amount)

    def forward(self):
        self.__pi.write(self.__dir, 0) #may need to swap
        print(f"direction: {self.__pi.read(self.__dir)}")

    def reverse(self):
        self.__pi.write(self.__dir, 1) #may need to swap
        print(f"direction: {self.__pi.read(self.__dir)}")

    def hardStop(self):
        curr = self.__pi.read(self.__break)
        self.__pi.write(self.__break, curr ^ 1)
        print(f"hard stop: {self.__pi.read(self.__break)}")

        self.__pi.write(23, curr^1)




