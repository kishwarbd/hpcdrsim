# job_scheduler.py:- starts the submitted job and allocates resources
# (i.e., optimal processor frequency)

import simulus
import numpy as np
from collections import deque
from optimization import *

job_buffer = deque()
resource_optimizer = Optimizer()

class JobScheduler(object):
    def __init__(self, sim, jobs, model_params):
        job_buffer_avail = sim.semaphore(len(jobs))
        job_buffer_occupy = sim.semaphore(0)
        sim.process(job_submit_process, sim, jobs, job_buffer_avail, job_buffer_occupy, model_params)
        sim.process(job_execution_process, sim, job_buffer_avail, job_buffer_occupy, model_params)

def job_submit_process(sim, jobs, job_buffer_avail, job_buffer_occupy, model_params):
    # process to handle job submission 
    for job in jobs:
        job_buffer.append(job)
        sim.sleep(job["submit_time"]-sim.now) # sleep the process to advance simulation until the time job was submitted
        if "job_stat" in model_params["debug_options"]:
            print("%f: job[%d] submitted"%(sim.now, job["job_id"]))
        job_buffer_avail.wait()
        job_buffer_occupy.signal()

def job_execution_process(sim, job_buffer_avail, job_buffer_occupy, model_params):
    # process to start the job and execute it to completion
    while True:
        job_buffer_occupy.wait()
        job_buffer_avail.signal()
        job = job_buffer.popleft()      # take the first job in the queue to start executing
        reg_runtime = job["regress_coeff_runtime"]
        reg_power = job["regress_coeff_power"]
        if job["dr_arrival"] == True:      # job arrived during demand response period
            min_freq = np.amin(job["freq"])
            max_freq = np.amax(job["freq"])
            freq = resource_optimizer.find_opt_freq(reg_runtime, reg_power, min_freq, max_freq) 
        else:   # assign maximum processor frequency to the incoming job 
            freq = np.amax(job["freq"])
        if "job_stat" in model_params["debug_options"]:
            print("%f: job[%d] started with processor frequnecy: %f"%(sim.now, job["job_id"], freq))
        # determine the execution time, power, and energy
        poly_runtime = np.poly1d(reg_runtime)
        poly_power = np.poly1d(reg_power)
        runtime = poly_runtime(freq)
        power = poly_power(freq)
        energy = (job["num_req_processors"]*power*runtime)/1000 # in KJ
        sim.sleep(runtime)
        if "job_stat" in model_params["debug_options"]:
            print("%f: job[%d] finished. Energy consumed: %f (KJ)"%(sim.now, job["job_id"], energy))
