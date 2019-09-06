
import time
import RPi.GPIO as GPIO
import sys
import requests

class StepperDriver(object):
    seq = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
    revolution = 512 # steps
    pins = [None, None, None, None]
    delay = 0
    remainder = 0.0

    def __init__(self, pin1, pin2, pin3, pin4, delay=10.0/1000.0):
        """Delay is best between 5 and 20 ms"""
        self.pins = [pin1, pin2, pin3, pin4]
        self.delay = delay

        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

    def setStep(self, w):
        for i in range(4):
            GPIO.output(self.pins[i], w[i])

    def forward(self, steps):
        for i in range(steps):
            for j in range(len(self.seq)):
                self.setStep(self.seq[j])
                time.sleep(self.delay)

    def backward(self, steps):
        for i in range(steps):
            for j in reversed(range(len(self.seq))):
                self.setStep(self.seq[j])
                time.sleep(self.delay)

    def forwardAngle(self, degrees):
        if degrees >= 0:
            self.remainder += (self.revolution*degrees/360)%1
            self.forward(int(self.revolution*degrees/360) + int(self.remainder))
        else:
            self.remainder += (self.revolution*degrees/360)%(-1)
            self.backward(int(self.revolution*(-degrees)/360) + int(self.remainder))
        self.remainder = self.remainder%(1 if self.remainder >= 0 else -1)

    def backwardsAngle(self, degrees):
        self.forwardAngle(-degrees)

class Hand(StepperDriver):

    def __init__(self, name, minValue, maxValue, minAngle, maxAngle, value, pin1, pin2, pin3, pin4, delay=10.0/1000.0):
        """ Speed defines the number of steps needed to move from minAngle to maxAngle.
            Positions defines how many distinc angles can be set.
        """
        super().__init__(pin1, pin2, pin3, pin4, delay)
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.minValue = minValue
        self.maxValue = maxValue
        self.name = name
        self.value = value
        self.k = (self.maxAngle - self.minAngle)/(self.maxValue - self.minValue)

    def value(self, val):
        self.forwardAngle(self.k*(val - self.value))
        self.value = val

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    i = StepperDriver(7, 11, 13, 15)
    f = StepperDriver(12, 16, 18, 22)
    ih = Hand("integer", 18.0, 28.0, 0, 120, 21.0, 7, 11, 13, 15)
    fh = Hand("fraction", 0, 1.0, 0, 120, 0.82, 12, 16, 18, 22)

    print(m.pins)
    print(h.pins)
    if (len(sys.argv) >= 3):
        i.forwardAngle(int(sys.argv[1]))
        f.forwardAngle(int(sys.argv[2]))
    while True:
        ih.value(21.0)
        fh.step(0.82)
        time.sleep(20.0/1000.0)

