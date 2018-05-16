"""
'Only God can judge me.'
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from math import log
from beautifultable import BeautifulTable
from datetime import datetime
from queue import Queue

class Task(object):

    def __init__(self, simulation_time):
        self.simulation_time = simulation_time

    def get_time(self):
        return self.simulation_time

    def __repr__(self):
        return ("Task created at %s" % self.simulation_time)


class NumberGen(object):

    def __init__(self, _seed=None, _lambda=None, _mi=None):
        if _lambda:
            self.rate = _lambda
        elif _mi:
            self.rate = _mi
        else:
            raise
        if _seed:
            self._seed = _seed
        else:
            self._seed = random.randint(1,250)
        self._random = random.Random()
        self._random.seed(self._seed)
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
        self.IDLE = 0
        self.BUSY = 1
        self.DEPARTURE_REFERENCE = random.getrandbits(128)

        self.state = self.IDLE
        self.state_audit = []
        self._queue = Queue()

    def plot_result_array(self, array_to_plot, figure, title="Unnamed", xlabel="X", ylabel="Y", block=False):
        plt.figure(figure)
        n, bins, patches = plt.hist(array_to_plot, 50, density=1, facecolor='green', alpha=0.75)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.show(block=block)

    def plot_queue_audit(self, queue_to_plot, figure, title="Unamed", xlabel="X", ylabel="Y", block=False):
        time_values = [time for (time, qsize) in queue_to_plot]
        qsize_values = [qsize for (time, qsize) in queue_to_plot]
        plt.figure(figure)
        plt.plot(time_values, qsize_values)
        plt.grid(True)
        plt.show(block=block)

    def set_state(self, state):
        self.state = state
        self.state_audit.append(state)

    def update_statistics(self):
        self.time_since_last_event = self.sim_time - self.last_event_time
        self.cumulated_queue_len += self._queue.qsize() * self.time_since_last_event

        if self.state == self.BUSY:
            self.total_busy_time += self.time_since_last_event

    def run_simulation(self, _lambda, _mi, max_requests, _seed_lambda=None, _seed_mi=None, _table=None):

        rng1 = NumberGen(_seed=_seed_lambda,_lambda=_lambda)
        rng2 = NumberGen(_seed=_seed_mi,_mi=_mi)

        simulation_start_time = 0
        self.sim_size = 0
        self.sim_time = 0
        self.cumulated_queue_len = 0
        self.last_event_time = 0
        self.total_busy_time = 0
        queue_audit = []
        next_departure = simulation_start_time
        next_arrival = rng1.get_exp();

        while (self.sim_size < max_requests):
            if(next_arrival < next_departure):
                self.sim_size += 1
                self.sim_time = next_arrival
                self.update_statistics()
                queue_audit.append((self.sim_time, self._queue.qsize()))
                if (self.state == self.IDLE):
                    self.set_state(self.BUSY)
                    next_departure = self.sim_time + rng2.get_exp()
                else:
                    new_task = Task(self.sim_time)
                    self._queue.put(new_task)
                queue_audit.append((self.sim_time, self._queue.qsize()))
                next_arrival = self.sim_time + rng1.get_exp()
            else:
                self.sim_time = next_departure
                self.update_statistics()
                if (self._queue.empty()):
                    self.set_state(self.IDLE)
                    next_departure = self.DEPARTURE_REFERENCE
                else:
                    self._queue.get()
                    next_departure = self.sim_time + rng2.get_exp()
                    queue_audit.append((self.sim_time, self._queue.qsize()+1))
            self.last_event_time = self.sim_time
            queue_audit.append((self.sim_time, self._queue.qsize()))

        # Simulation total time
        simulation_end_time = self.last_event_time
        simulation_total_time = simulation_end_time - simulation_start_time

        avg_queue_length = self.cumulated_queue_len / self.sim_time;
        avg_utilization = self.total_busy_time / self.sim_time;

        _table.append_row([max_requests, _seed_mi, _seed_lambda, round(simulation_total_time,2),
            avg_queue_length, avg_utilization])

        # Uncomment to plot random exponential variables graph and queue graph
        # self.plot_queue_audit(queue_audit, 0)
        # self.plot_result_array(rng1.audit(), 1, title="RNG1 Plot")
        # self.plot_result_array(rng2.audit(), 2, title="RNG2 Plot", block=True)

def main():
    mm1 = MM1()
    table = BeautifulTable()
    table.column_headers = ["Number of Tasks", "Seed A", "Seed B",
        "Sim Total Time", "Avg Queue lenght", "Avg Utilization"]

    mi_A=1
    lambda_S=1/0.9

    # Running simulation with same values as the ones used in the slides
    mm1.run_simulation(mi_A, lambda_S, 10, _seed_mi=17, _seed_lambda=23, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 100, _seed_mi=17, _seed_lambda=23, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 1000, _seed_mi=17, _seed_lambda=23, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 10000, _seed_mi=17, _seed_lambda=23, _table=table)

    mm1.run_simulation(mi_A, lambda_S, 10, _seed_mi=89, _seed_lambda=25, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 100, _seed_mi=89, _seed_lambda=25, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 100, _seed_mi=89, _seed_lambda=25, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 1000, _seed_mi=89, _seed_lambda=25, _table=table)

    mm1.run_simulation(mi_A, lambda_S, 10, _seed_mi=11, _seed_lambda=167, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 100, _seed_mi=11, _seed_lambda=167, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 1000, _seed_mi=11, _seed_lambda=167, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 10000, _seed_mi=11, _seed_lambda=167, _table=table)

    mm1.run_simulation(mi_A, lambda_S, 10, _seed_mi=21, _seed_lambda=235, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 100, _seed_mi=21, _seed_lambda=235, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 1000, _seed_mi=21, _seed_lambda=235, _table=table)
    mm1.run_simulation(mi_A, lambda_S, 10000, _seed_mi=21, _seed_lambda=235, _table=table)

    print(table)

if __name__ == '__main__':
    main()
