# parse_job.py :- parse the job trace file and return the jobs as a
# list format

# Information on the workload trace file format can be found at:
# http://www.cs.huji.ac.il/labs/parallel/workload/ 

import sys

# the following method reads the file line-by-line
# Workload format:
# job_id submit_time wait_time run_time num_allocated_processors avg_cpu_time_used

def workload_trace(folder):
    workloads = list() 
    #NOTE: check the file/folder name; if doesn't exist throw exception
    #print("folder name: %s" %(folder))
    with open("%s" % (folder)) as f:
        for line in f:
            # Note: lstrip() removes leading spaces (if any) 
            if line.lstrip().startswith(';') or len(line) == 0: # comment or empty line
                continue

            fields = line.split()
            assert len(fields) == 18
           
            job_id = int(fields[0])
            submit_time = int(fields[1])
            wait_time = int(fields[2]) 
            run_time = float(fields[3]) 
            num_allocated_processors = int(fields[4])
            avg_cpu_time_used = float(fields[5])
            used_memory = int(fields[6])
            num_req_processors = int(fields[7])
            req_time = int(fields[8])
            req_mem = int(fields[9])
            status = int(fields[10])
            user_id = int(fields[11])
            group_id = int(fields[12])
            executable_num = int(fields[13])
            queue_num = int(fields[14])
            partition_num = int(fields[15])
            preceding_job_num = int(fields[16])
            think_time_from_preceding_job = int(fields[17])

            workload = {
                "job_id" : int(fields[0]),
                "submit_time" : int(fields[1]),
                "wait_time" : int(fields[2]), 
                "run_time" : float(fields[3]), 
                "num_allocated_processors" : int(fields[4]),
                "avg_cpu_time_used" : float(fields[5]),
                "used_memory" : int(fields[6]),
                "num_req_processors" : int(fields[7]),
                "req_time" : int(fields[8]),
                "req_mem" : int(fields[9]),
                "status" : int(fields[10]),
                "user_id" : int(fields[11]),
                "group_id" : int(fields[12]),
                "executable_num" : int(fields[13]),
                "queue_num" : int(fields[14]),
                "partition_num" : int(fields[15]),
                "preceding_job_num" : int(fields[16]),
                "think_time_from_preceding_job" : int(fields[17]),
            }

            workloads.append(workload)
        return workloads

def job_profile_trace(folder):
    # returns the processor frequency, power, and execution time from trace
    frequencies = list(); power = list(); runtime = list()
    job_profile_data = list()
    with open("%s" % (folder)) as f:
        for line in f:
            fields = line.split()
            frequencies.append(float(fields[0]))
            power.append(float(fields[1]))
            runtime.append(float(fields[2]))
        job_profile_data.append(frequencies)
        job_profile_data.append(power)
        job_profile_data.append(runtime)
        return job_profile_data

