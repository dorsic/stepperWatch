
import time
import RPi.GPIO as GPIO
import sys

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

    def __init__(self, name, minAngle, maxAngle, speed, positions, pin1, pin2, pin3, pin4, delay=10.0/1000.0):
        """ Speed defines the number of steps needed to move from minAngle to maxAngle.
            Positions defines how many distinc angles can be set.
        """
        super().__init__(pin1, pin2, pin3, pin4, delay)
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.speed = speed
        self.steps = 0
        self.positions = positions
        self.name = name

    def step(self):
        da = self.maxAngle - self.minAngle
        self.steps += 1
        angle = self.minAngle + self.steps*(da)/self.speed
        print(self.name + ": " + str(self.steps) + " - " + str(angle))
        if (angle >= self.maxAngle):
            print("Moving to initial position by " + str(-da))
            self.forwardAngle(-da*(1 if self.positions >= 0 else -1))
            self.steps = 0
        elif (self.steps % (self.speed/self.positions)) == 0:
        #if (self.steps/self.speed*(self.maxAngle-self.minAngle))%((self.maxAngle-self.minAngle)/pos) == 0:
            # make step
            self.forwardAngle(da/self.positions)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    h = StepperDriver(7, 11, 13, 15)
    m = StepperDriver(12, 16, 18, 22)
    hh = Hand("h", 0, 90, 12*60, 12*4, 7, 11, 13, 15)
    mh = Hand("m", 0, 270, 60, -60, 12, 16, 18, 22)

    print(m.pins)
    print(h.pins)
    if (len(sys.argv) >= 3):
        h.forwardAngle(int(sys.argv[1]))
        m.forwardAngle(int(sys.argv[2]))
    while True:
        mh.step()
        hh.step()
        time.sleep(20.0/1000.0)
        # steps = input("How many steps forward? ")
         #m.forward(int(steps))
        # h.forward(int(steps))
        # steps = input("How many steps backwards? ")
         #m.backward(int(steps))
        # h.backward(int(steps))
