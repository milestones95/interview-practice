"""
Problem: Driver Dispatch System

A rideshare app needs to match incoming ride requests to available drivers.

Part 1 — add_driver(driver_id, rating, eta_minutes)
Adds a driver to the pool of available drivers. Drivers should be dispatchable by best combination of ETA and rating — lower ETA is better, but among drivers with similar ETA, higher rating should win. Design the priority however you think is defensible, but be ready to justify it.

Part 2 — dispatch_driver()
Removes and returns the single best available driver for a new ride request. O(log n).

Part 3 — update_driver_status(driver_id, eta_minutes)
A driver's ETA changes in real time (traffic, reroute, etc.) while they're still sitting in the available pool. Update their priority without scanning the whole heap for them. This is the interesting part: a plain heapq has no O(1) way to find an arbitrary element by id, and no efficient way to change a priority in place.

Part 4 — remove_driver(driver_id)
A driver goes offline (logs out, phone dies) while sitting in the pool. Remove them specifically, not just whatever's on top.
"""

import heapq

class driver:

    def __init__(self, driver_id, eta_minutes, rating):
        self.driver_id = driver_id
        self.eta_minutes = eta_minutes
        self.rating = rating


class driver_dispatch:

    def __init__(self):
        self.drivers = []
        self.count = 0
        self.driver_id_to_driver = {}


    def add_driver(self, eta_minutes: int, rating: float) :

        # lower ETA is better than higher ETA so we can use a min heap
        # higher rating is better so we can negate that
        driver_id = self.count + 1
        new_driver = driver(driver_id, eta_minutes, rating)

        heapq.heappush(self.drivers, (new_driver.eta_minutes, -new_driver.rating, driver_id, new_driver)) # we are assuming that the eta mins and ratings won't be exatly equal. keeping it simple for this problem
        self.driver_id_to_driver[new_driver.driver_id] = new_driver
        self.count+=1

    def dispatch_driver(self):

        try:
            if len(self.drivers) < 1:
                raise ValueError("there are no more available drivers")

            valid_driver_found = False
            while True and len(self.drivers) > 0:
                _,_,_,next_driver = heapq.heappop(self.drivers)
                existing_driver = self.driver_id_to_driver[next_driver.driver_id]

                if existing_driver.eta_minutes == float('-inf'):
                    continue

                if existing_driver.eta_minutes == next_driver.eta_minutes:
                    del self.driver_id_to_driver[next_driver.driver_id]
                    valid_driver_found = True
                    break

            if valid_driver_found:
                return next_driver

            return None
        except ValueError as error:
            print(error)

    
    def update_driver_status(self, driver_id, eta_minutes):

        """we do not want to scan every item in the heap to search for the driver and update their eta. And we don't have to. We can add this new entry as a new driver (although this takes up more space)
        we can have a hashmap that tracks the latest eta for a driver. As we pop, if the eta_minutes for a driver id doesn't match
        what's in the hashmap, skip it and pop it again. if it does match, we can delete the entry after we pop a valid matching driver
        """

        # account for if the driver isn't already in the hashmap
        #!!!!

        try:
            if driver_id not in self.driver_id_to_driver:
                raise ValueError("driver doesn't exist")

            existing_driver = self.driver_id_to_driver[driver_id]
            new_driver = driver(driver_id, eta_minutes, existing_driver.rating)

            heapq.heappush(self.drivers, (new_driver.eta_minutes, -new_driver.rating, self.count+1, new_driver)) # we are assuming that the eta mins and ratings won't be exatly equal. keeping it simple for this problem
            self.driver_id_to_driver[new_driver.driver_id] = new_driver

        except ValueError as error:
            print(error)


    def remove_driver(self, driver_id):

        driver = self.driver_id_to_driver[driver_id]
        driver.eta_minutes = float('-inf')
        self.driver_id_to_driver[driver_id] = driver



test = driver_dispatch()
test.add_driver(4, 4.8)
test.add_driver(2, 2.3)
test.add_driver(8, 4.7)
test.update_driver_status(9, 7)
test.add_driver(10, 2.7)

test.remove_driver(1)


# print("drivers: ", test.drivers)
next_driver = test.dispatch_driver()

print("next driver: ", next_driver.driver_id, " eta: ", next_driver.eta_minutes)

next_driver = test.dispatch_driver()

print("next driver: ", next_driver.driver_id, " eta: ", next_driver.eta_minutes)

next_driver = test.dispatch_driver()

print("next driver: ", next_driver.driver_id, " eta: ", next_driver.eta_minutes)

print("drivers: ", test.drivers)

# next_driver = test.dispatch_driver()



# finished part 1,2,3 by 35 min mark. updating status and thinking that through took the longest