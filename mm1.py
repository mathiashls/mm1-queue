"""
'This code is so ugly it hurts my eyes.'
Mathias Hillesheim, this code's father
"""

import random
from datetime import datetime
from queue import Queue

import numpy as np
import matplotlib.pyplot as plt
from math import log


class Task(object):

    def __init__(self, simulation_time):
        self.simulation_time = simulation_time

    def get_time(self):
        return self.simulation_time


class NumberGen(object):

    def __init__(self, _lambda=None, _mi=None):
        if _lambda:
            self.rate = _lambda
        elif _mi:
            self.rate = _mi
        else:
            raise
        _seed = random.randint(1,10000)
        self._random = random.Random()
        self._random.seed(_seed)
        self._audit = []

    def get_uniform(self):
        uniform = self._random.random()
        return uniform

    def get_exp(self):
        uniform = self.get_uniform()
        ln_uniform = - np.log(uniform)
        result = ln_uniform / self.rate
        self._audit.append(result)
        return result

    def audit(self):
        return self._audit


class MM1(object):


    def __init__(self):
        print("Initing MM1 queue...")
        self.IDLE = 0
        self.BUSY = 1
        self.DEPARTURE_REFERENCE = random.getrandbits(128)

        self.state = self.IDLE
        self.state_audit = []
        self._queue = Queue()

    def plot_result_array(self, array_to_plot, figure, title="Unnamed", xlabel="X", ylabel="Y", block=False):
        plt.figure(figure)
        n, bins, patches = plt.hist(array_to_plot, 50, normed=1, facecolor='green', alpha=0.75)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)

        plt.show(block=block)

    def plot_queue_audit(self, queue_to_plot, figure, title="Unamed", xlabel="X", ylabel="Y", block=False):
        #formated_list = [(time, log(qsize)) for time, qsize in queue_audit]
        time_values = [time for (time, qsize) in queue_to_plot]
        qsize_values = [qsize for (time, qsize) in queue_to_plot]
        plt.figure(figure)
        plt.plot(time_values, qsize_values)
        plt.show(block=block)

    def set_state(self, state):
        self.state = state
        self.state_audit.append(state)

    def update_statistics(self):
        self.time_since_last_event = self.sim_time - self.last_event_time
        self.cumulated_queue_len = self._queue.qsize() * self.time_since_last_event

        if self.state == self.BUSY:
            self.total_busy_time += self.time_since_last_event

    def run_simulation(self, _lambda, _mi, max_requests):

        simulation_start_time = datetime.now()

        rng1 = NumberGen(_lambda=_lambda)
        rng2 = NumberGen(_mi=_mi)

        self.sim_time = 0
        self.last_event_time = 0
        self.total_busy_time = 0
        queue_audit = []
        next_departure = self.DEPARTURE_REFERENCE
        next_arrival = rng1.get_exp();

        self.update_statistics()

        while (self.sim_time < max_requests):
            if(next_arrival < next_departure):
                print("New arrival!")
                self.sim_time = next_arrival
                if (self.state == self.IDLE):
                    self.set_state(self.BUSY)
                    print("Queue is now BUSY!")
                    next_departure = self.sim_time + rng2.get_exp()
                else:
                    new_task = Task(self.sim_time)
                    print("Inserting task on queue")
                    self._queue.put(new_task)
                    queue_audit.append((self.sim_time, self._queue.qsize()))
                next_arrival = self.sim_time + rng1.get_exp()
            else:
                self.sim_time = next_departure
                if (self._queue.empty()):
                    self.set_state(self.IDLE)
                    print("Queue is now IDLE!")
                    next_departure = self.DEPARTURE_REFERENCE
                else:
                    self._queue.get()
                    print("Departuring task on queue")
                    next_departure = self.sim_time + rng2.get_exp()
            self.last_event_time = self.sim_time

        # Simulation total time
        simulation_end_time = datetime.now()
        simulation_total_time = simulation_end_time - simulation_start_time
        print("Simulation took %s to be completed." % simulation_total_time)

        avg_queue_length = self.cumulated_queue_len / self.sim_time;
        avg_utilization = self.total_busy_time / self.sim_time;
        print("The average queue lenght was %s and the average "
              "utilization was %s" % (avg_queue_length, avg_utilization))

        print(queue_audit)
        self.plot_queue_audit(queue_audit, 0)
        self.plot_result_array(rng1.audit(), 1, title="RNG1 Plot")
        self.plot_result_array(rng2.audit(), 2, title="RNG2 Plot", block=True)

def main():
    mm1 = MM1()
    mm1.run_simulation(1, 2, 1000)

if __name__ == '__main__':
    main()
