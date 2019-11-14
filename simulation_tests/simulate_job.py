# simulate_job.py: simulate the jobs

import simulus
import numpy as np
from sys import path
path.append('..')
from parse_job import *
from job_scheduler import *

def regression(x_values, y_values, deg):
    # regression function to find the perfect fit, and corresponding co-efficients

    poly_coefficients = np.polyfit(x_values, y_values, deg)
    return poly_coefficients

def process_trace_jobs(file_path):
    # process the raw trace jobs and assign power values, etc 
    
    raw_jobs = workload_trace(file_path) # jobs directly from trace
    processed_jobs = list()              # jobs with added information (e.g., power, runtime)  

    # runtime, power, and frequency information from literature
    # quantum espresso
    profile_quantum_espresso = job_profile_trace('../data/app_quantum_espresso')
    freq_quantum_espresso = np.asarray(profile_quantum_espresso[0]); power_quantum_espresso = np.asarray(profile_quantum_espresso[1]); runtime_quantum_espresso = np.asarray(profile_quantum_espresso[2])
    
    # seissol
    profile_seissol = job_profile_trace('../data/app_seissol')
    freq_seissol = np.asarray(profile_seissol[0]); power_seissol = np.asarray(profile_seissol[1]); runtime_seissol = np.asarray(profile_seissol[2])
    
    # BT
    profile_bt = job_profile_trace('../data/app_bt')
    freq_bt = np.asarray(profile_bt[0]); power_bt = np.asarray(profile_bt[1]); runtime_bt = np.asarray(profile_bt[2])
    
    # Gadget
    profile_gadget = job_profile_trace('../data/app_gadget')
    freq_gadget = np.asarray(profile_gadget[0]); power_gadget = np.asarray(profile_gadget[1]); runtime_gadget = np.asarray(profile_gadget[2])
    
    num_jobs = 4        # available jobs with power and runtime information
    for i in range(num_jobs):
        raw_job = raw_jobs[i]
        if i%num_jobs == 0: #  application: quantum espresso
            freq = freq_quantum_espresso; power = power_quantum_espresso; runtime = runtime_quantum_espresso
        elif i%num_jobs == 1: #  application: seissol
            freq = freq_seissol; power = power_seissol; runtime = runtime_seissol
        elif i%num_jobs == 2: #  application: bt
            freq = freq_bt; power = power_bt; runtime = runtime_bt
        elif i%num_jobs == 3: #  application: gadget
            freq = freq_gadget; power = power_gadget; runtime = runtime_gadget
    
        # determine regression coefficients
        runtime_reg = regression(freq, runtime, 2)  # regression coefficients for runtime
        power_reg = regression(freq, power, 3)      # regression coefficients for power usage
        
        # whether the job arrived during a demand response period
        # values: True (arrived during demand response), False otherwise
        demand_response_arrival = True
        
        # create a job dictionary with the necessary job information
        job = {
            "job_id": raw_job["job_id"],
            "submit_time": raw_job["submit_time"],
            "num_req_processors": raw_job["num_req_processors"], #number of required processors
            "freq": freq,
            "regress_coeff_runtime": runtime_reg,
            "regress_coeff_power": power_reg,
            "dr_arrival": demand_response_arrival,
        }        
        processed_jobs.append(job)
    
    # instead of passing actual runtime as arguments, regression
    # coefficients is passed
    runtime_reg = regression(freq, runtime, 2)  # regression coefficients for runtime
    power_reg = regression(freq, power, 3)      # regression coefficients for power usage
    return processed_jobs

model_parameters = {
    "debug_options": set(["job_stat"]),
}

trace_file_path = "../data/UniLu-Gaia-2014-5K"
jobs = process_trace_jobs(trace_file_path)

sim = simulus.simulator()
JobScheduler(sim, jobs, model_parameters)
sim.run()
