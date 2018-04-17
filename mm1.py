from random import random
from queue import Queue


class MM1(object):
    def __init__(self):
        self.STATES = dict(BUSY='busy', IDLE='idle')
        self.HUGE_VAL = random.getrandbits(128)

        self.rand1 = random.Random()
        self.rand1.seed(1234)

        self.rand2 = random.Random()
        self.rand2.seed(8276)
