import time
import RPi.GPIO as GPIO

 class StepperDriver(object):
    pin1 = None
    pin2 = None
    pin3 = None
    pin4 = None
    stepCount = 8
    seq = range(0, self.stepCount)

     def __init__(pin1, pin2, pin3, pin4):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4

        self.seq[0] = [0,1,0,0]
        self.seq[1] = [0,1,0,1]
        self.seq[2] = [0,0,0,1]
        self.seq[3] = [1,0,0,1]
        self.seq[4] = [1,0,0,0]
        self.seq[5] = [1,0,1,0]
        self.seq[6] = [0,0,1,0]
        self.seq[7] = [0,1,1,0]
 
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        GPIO.setup(pin3, GPIO.OUT)
        GPIO.setup(pin4, GPIO.OUT)

    def setStep(self, w1, w2, w3, w4):
        GPIO.output(pin1, w1)
        GPIO.output(pin2, w2)
        GPIO.output(pin3, w3)
        GPIO.output(pin4, w4)

    def forward(self, delay, steps):
        for i in range(steps):
            for j in range(self.stepCount):
                self.setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                time.sleep(delay)
    
    def backwards(self, delay, steps):
        for i in range(steps):
            for j in reversed(range(self.stepCount)):
                self.setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                time.sleep(delay)

 
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    m = StepperDriver(12, 16, 18, 22)
    h = StepperDriver(7, 11, 13, 15)
    while True:
        delay = raw_input("Time Delay (ms)?")
        steps = raw_input("How many steps forward? ")
        m.forward(int(delay) / 1000.0, int(steps))
        steps = raw_input("How many steps backwards? ")
        m.backwards(int(delay) / 1000.0, int(steps))