"""Problem: Print Job Queue with Cancellations

You're managing a shared office printer. Jobs come in with a priority (1 = lowest, 10 = highest — always print the highest-priority job next) and a unique job_id. Two operations need to be supported:

submit_job(job_id, priority) — a new job is added to the queue.
print_next() — pop and return the highest-priority job currently in the queue.

So far, this is just the max-heap pattern you've already built a few times. Here's the twist: there's a third operation.

cancel_job(job_id) — someone cancels a job before it's been printed. It needs to disappear from the queue entirely, even if it's buried in the middle of the heap somewhere, not sitting at the root.

This is where things get interesting. You already know a heap only gives you fast access to the top — finding and removing an arbitrary element buried inside it isn't something heapq supports directly, and there's no heapq.remove(item). Actually go check — try searching for whether heapq has a removal function for an arbitrary element. What are your options once you confirm it doesn't?"""

import heapq
class Job:

    def __init__(self, job_id: int, priority: int):
        self.job_id = job_id
        self.priority = priority

class PriorityQueue:

    def __init__(self):
        self.priorityqueue = []
        self.canceled_jobs = set()


    def submit_job(self, job_id, priority):

        new_job = Job(job_id, priority)

        heapq.heappush(self.priorityqueue, (-priority, job_id, new_job))


    def get_jobs(self):

        jobs = []

        for i in range(len(self.priorityqueue)):
            _,_,j = heapq.heappop(self.priorityqueue)
            jobs.append(j.job_id)

        print("jobs: ", jobs)


    def cancel_jobs(self, job_id):

        self.canceled_jobs.add(job_id)


    def print_next(self):

        try:

            valid_job_found = False

            # _,_,next_job = heapq.heappop(self.priorityqueue)
            while len(self.priorityqueue) > 0:
                _,_,next_job = heapq.heappop(self.priorityqueue)
                if next_job.job_id not in self.canceled_jobs:
                    print("next job: ", next_job.job_id)
                    valid_job_found = True
                    break


            if not valid_job_found:
                raise ValueError("there are no more jobs...")


        except ValueError as error:
            print("Error: ", error)

    

test = PriorityQueue()
test.submit_job(1,3)
# test.submit_job(2,3)
# test.submit_job(4,5)
# test.get_jobs()

print("-----------------")

test.cancel_jobs(1)
test.print_next()
test.print_next()
test.print_next()

# finished in 23 mins