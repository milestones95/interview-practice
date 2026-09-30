"""
Priority Task Scheduler with Cancellation

You're building a job scheduler for a system that processes background tasks (think: a simplified version of what powers a task queue at a company like yours). Requirements:

schedule(job_id, priority) — adds a job to the queue
run_next() — pops and returns the highest-priority job to execute
cancel(job_id) — a job can be cancelled at any time before it runs (a user closes a request, a dependency fails, etc.) — cancelled jobs should never be returned by run_next()
Jobs can also have their priority changed after being scheduled (e.g., a job gets escalated because it's blocking something urgent)
"""

# finished and tested it in 24 mins

import heapq

class Job:
    def __init__(self, job_id, priority, seq):
        self.job_id = job_id
        self.priority = priority
        self.sequence_id = seq


class JobQueue:

    def __init__(self):
        self.job_list = []
        self.job_id_to_job = {}
        self.count = 0


    def schedule(self, job_id, priority):

        new_job = Job(job_id, priority, self.count + 1)

        heapq.heappush(self.job_list, (priority, new_job.sequence_id, new_job))

        # add the job to the hashmap as well

        self.job_id_to_job[job_id] = new_job
        self.count+=1


    def cancel(self, job_id):
        
        # set the job to None so we know that any other node with this job id, to skip it
        self.job_id_to_job[job_id] = None

    def update_priority(self, job_id, priority):

        new_job = Job(job_id, priority, self.count+1)
        self.job_id_to_job[job_id] = new_job

        heapq.heappush(self.job_list, (new_job.priority, new_job.sequence_id, new_job))

        self.count+=1

    
    def run_next(self):

        try:

            while True:
                if len(self.job_list) <=0:
                    raise ValueError("there are no more jobs left to run")

                # get the next job
                _,_,next_job = heapq.heappop(self.job_list)

                # if the jobs don't match, then skip this job because it's stale
                if self.job_id_to_job[next_job.job_id] is None or self.job_id_to_job[next_job.job_id].sequence_id != next_job.sequence_id:
                    continue

                else:
                    return next_job

            return None

        except ValueError as error:
            print(error)

            








test = JobQueue()
test.schedule(1, 2)
test.schedule(3, 5)
test.schedule(6, 9)
test.schedule(2, 1)

test.cancel(1)
test.schedule(8, 5)

test.update_priority(2, 8)



print("tasks: ", test.job_list)

next_job = test.run_next()
print("next job: ", next_job.job_id)

next_job = test.run_next()
print("next job: ", next_job.job_id)
next_job = test.run_next()
print("next job: ", next_job.job_id)
next_job = test.run_next()
print("next job: ", next_job.job_id)
# next_job = test.run_next()
