
import time
import RPi.GPIO as GPIO

class StepperDriver(object):
    seq = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
    revolution = 512 # steps

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

    def backwards(self, steps):
        for i in range(steps):
            for j in reversed(range(len(self.seq))):
                self.setStep(self.seq[j])
                time.sleep(self.delay)

    def forwardAngle(self, degrees):
        self.forward(int(self.revolution*degrees/360))

    def backwardsAngle(self, degrees):
        self.backwards(int(self.revolution*degrees/360))


class Hand(StepperDriver):

	def __init__(self, minAngle, maxAngle, speed, positions):
		""" Speed defines the number of steps needed to move from minAngle to maxAngle.
			Positions defines how many distinc angles can be set.
		"""
		self.minAngle = minAngle
		self.maxAngle = maxAngle
		self.speed = speed
		self.steps = 0

	def step(self):
		self.steps += 1
		angle = self.minAngle + self.steps*(self.maxAngle-self.minAngle)/self.speed
		if (self.steps/self.speed*(self.maxAngle-self.minAngle))%((self.maxAngle-self.minAngle)*self.positions) == 0:
			# make step
			self.forwardAngle((self.maxAngle-self.minAngle)/self.positions)



if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    m = StepperDriver(12, 16, 18, 22)
    h = StepperDriver(7, 11, 13, 15)
    hh = Hand(0, 90, 12*60, 12*4)
    mh = Hand(0, 270, 60, 60)

    print(m.pins)
    print(h.pins)
    while True:
        steps = input("How many steps forward? ")
        m.forward(int(steps))
        h.forward(int(steps))
        steps = input("How many steps backwards? ")
        m.backwards(int(steps))
        h.backwards(int(steps))
