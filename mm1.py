"""
'This code is so ugly it hurts my eyes.'
Mathias Hillesheim, this code's father
"""

import random
from datetime import datetime
from queue import Queue

import numpy as np
import matplotlib.pyplot as plt


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


    def __init__(self):
        print("Initing MM1 queue...")
        self.IDLE = 0
        self.BUSY = 1
        self.DEPARTURE_REFERENCE = random.getrandbits(128)

        self.state = self.IDLE
        self.state_audit = []
        self._queue = Queue()

    def plot_result_array(self, array_to_plot, title="Unnamed", xlabel="X", ylabel="Y"):
        n, bins, patches = plt.hist(array_to_plot, 50, normed=1, facecolor='green', alpha=0.75)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        #plt.axis([40, 160, 0, 0.03])
        plt.grid(True)

        plt.show()

    def set_state(self, state):
        self.state = state
        self.state_audit.append(state)

    def run_simulation(self, _lambda, _mi, max_requests):

        simulation_start_time = datetime.now()

        rng1 = NumberGen(_lambda=_lambda)
        rng2 = NumberGen(_mi=_mi)

        arrives = []
        departures = []
        all_tasks = []

        simulation_requests = 0.0
        next_departure = self.DEPARTURE_REFERENCE
        next_arrival = rng1.get_exp();
        arrives.append(next_arrival)

        while (simulation_requests < max_requests):
            if(next_arrival < next_departure):
                print("New arrival!")
                simulation_requests = next_arrival
                if (self.state == self.IDLE):
                    self.set_state(self.BUSY)
                    print("Queue is now BUSY!")
                    next_departure = simulation_requests + rng2.get_exp()
                    departures.append(next_departure)
                else:
                    new_task = Task()
                    all_tasks.append(new_task)
                    print("Inserting task on queue")
                    self._queue.put(new_task)
                next_arrival = simulation_requests + rng1.get_exp()
                arrives.append(next_arrival)
            else:
                simulation_requests = next_departure
                if (self._queue.empty()):
                    self.set_state(self.IDLE)
                    print("Queue is now IDLE!")
                    next_departure = self.DEPARTURE_REFERENCE
                else:
                    self._queue.get()
                    print("Departuring task on queue")
                    next_departure = simulation_requests + rng2.get_exp()
                    departures.append(next_departure)

        simulation_end_time = datetime.now()
        simulation_total_time = simulation_end_time - simulation_start_time
        print("Simulation took %s to be completed." % simulation_total_time)

        self.plot_result_array(departures)
        self.plot_result_array(arrives)

def main():
    mm1 = MM1()
    mm1.run_simulation(1, 2, 1000)

if __name__ == '__main__':
    main()
