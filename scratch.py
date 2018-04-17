import random
import numpy as np
from queue import Queue


class Task(object):
    pass

def get_exp(_lambda, u):
    x = (np.log(1 - u)) / _lambda
    return x

IDLE = 'idle'
BUSY = 'busy'
HUGE_VAL = random.getrandbits(128)

_queue = Queue()

server_state = IDLE
sim_time = 0.0
next_departure = HUGE_VAL

#XXX
next_arrival = get_exp(_lambda, U1);

while(sim_time < T_MAX):
    if (next_arrival < next_departure):
        sim_time = next_arrival
        if (server_state == IDLE):
            server_state = BUSY
            next_departure = sim_time + get_exp(_lambda, U2)
        else:
            # XXX
            new_task = Task()
            _queue.put(new_task)
