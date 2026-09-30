"""
Problem: Hospital ER Patient Queue

You're building the intake system for an emergency room. Patients arrive continuously throughout the day — you never know the full list in advance. Each patient has a severity score (1 = minor, 10 = critical). At any moment, when a doctor becomes free, they need to treat the most severe patient currently waiting — not the one who's been waiting longest, not first-come-first-served.

So you need a structure that supports two operations happening continuously, in any order, forever:

A new patient walks in → add them to the waiting pool.
A doctor frees up → pull out and treat the single most urgent patient currently waiting.

This is a real thing hospitals actually model this way (usually a bit more complex — tie-breaking by wait time, re-triage as vitals change — but the core is this).

Before you write anything: which heap type fits, and why? Specifically — what would go wrong if you used a sorted list instead of a heap here, given that patients are constantly arriving (not a fixed batch you sort once)?

Once you've got the reasoning, try implementing an ERQueue with add_patient(name, severity) and treat_next() methods using heapq, and send it over — I'll stress-test it the same way we did with the heap class.
"""

### I think we need to use a max heap for this because the first item we want to see is the person with the most severity first
# a sorted list isn't ideal here because once you add a new person to the list you have to resort it which is nlogn every time vs it being o(logn) time 

import heapq

class patient:

    def __init__(self, patient_id, sev):
        self.patient_id = patient_id
        self.severity = sev

class emergency_room:

    def __init__(self):
        self.patients = []


    def add_patient(self, patient_id, severity):

        new_patient = patient(patient_id, -severity) # make the severity negative since we want to use a max heap so the highest severity is at the top

        heapq.heappush(self.patients, (new_patient.severity, new_patient.patient_id, new_patient))


    def treat_next(self):

        patient_object = heapq.heappop(self.patients)

        priority, patient_id, patient = patient_object
        priority = -1* priority

        print("next patient: ", patient_id, " priority: ", priority)


    


test = emergency_room()
test.add_patient(1, 2)
test.add_patient(3, 4)
test.add_patient(6, 5)
test.add_patient(5, 9)
test.add_patient(2, 6)
test.add_patient(8, 6)



for patient_object in test.patients:
   priority, patient_id, patient = patient_object
   print("patient: ", patient.patient_id, "  priority: ", -1*priority)


test.treat_next()

print("---------------")

for patient_object in test.patients:
   priority, patient_id, patient = patient_object
   print("patient: ", patient.patient_id, "  priority: ", -1*priority)



# finished the first pass in 19 mins. Need to fix bug when there's a tie
# needed to use the id of the patient to know the order