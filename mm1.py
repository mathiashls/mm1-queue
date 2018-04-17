import random
import numpy as np
from datetime import datetime
from queue import Queue


class Task(object):

    def __init__(self):
        self.arrivel_time = datetime.now()

    def get_time(self):
        return self.arrivel_time


class NumberGen(object):

    def __init__(self, _lambda=None, _mi=None):
        if _lambda:
            self.rate = _lambda
        elif _mi:
            self.rate = _mi
        else:
            raise
        self._seed = random.randint(1,10000)

    def get_uniform(self):
        _random = random.Random()
        _random.seed(self._seed)
        return _random.random()

    def get_exp(self):
        uniform = self.get_uniform()
        ln_uniform = - np.log(uniform)
        result = ln_uniform / self.rate
        return result


class MM1(object):


    def __init__(self, max_requests):
        print("Initing MM1 queue...")
        self.IDLE = 'idle'
        self.BUSY = 'busy'
        self.DEPARTURE_REFERENCE = random.getrandbits(128)

        self.state = self.IDLE
        self._queue = Queue()

    def run_simulation(self, _lambda, _mi, max_requests):

        rng1 = NumberGen(_lambda=_lambda)
        rng2 = NumberGen(_mi=_mi)

        simulation_time = 0.0
        next_departure = self.DEPARTURE_REFERENCE
        next_arrival = rng1.get_exp();

        while (simulation_time < max_requests):
            if(next_arrival < next_departure):
                print("New arrival!")
                simulation_time = next_arrival
                if (self.state == self.IDLE):
                    self.state = self.BUSY
                    print("Queue is now BUSY!")
                    next_departure = simulation_time + rng2.get_exp()
                else:
                    new_task = Task()
                    print("Inserting task on queue")
                    self._queue.put(new_task)
                next_arrival = simulation_time + rng1.get_exp()
            else:
                simulation_time = next_departure
                if (self._queue.empty()):
                    self.state = self.IDLE
                    print("Queue is now IDLE!")
                    next_departure = self.DEPARTURE_REFERENCE
                else:
                    self._queue.pop()
                    print("Departuring task on queue")
                    next_departure = simulation_time + rng2.get_exp()

def main():
    mm1 = MM1(100)
    mm1.run_simulation(1, 2, 100)

if __name__ == '__main__':
    main()
