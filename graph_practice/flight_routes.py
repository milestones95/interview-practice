"""
Flight Route Network

You're building a tool for an airline alliance that needs to answer connectivity questions across all member carriers' route maps.

The SDK
python
class FlightAPI:
    def get_routes(self, page_token=None):

Routes are directed (a route from JFK→LAX doesn't imply LAX→JFK exists unless it's returned separately). Assume a few hundred pages, ~500 routes per page.

Part 1 (Easy) — Build the graph

Write build_route_graph(api) that paginates through all routes and builds an adjacency structure. Handle:

Missing/None origin or destination → drop the record
Self-loops (origin == destination) → drop the record
Duplicate routes from different airlines between the same origin/destination → collapse into one edge, but track which airlines fly it

Return the graph plus a count of distinct airports and total valid unique routes.

Part 2 (Easy–Medium) — Minimum layovers

Write min_layovers(graph, origin, destination) — BFS to find the minimum number of layovers (not distance) to get from origin to destination. Return -1 if unreachable. Note this is a directed graph, so reachability isn't symmetric.
"""

from collections import deque

class routes:

    def __init__(self):
        self.origin_to_destination_map = {}
        self.unique_cities = set()

    def build_route_graph(self,client, route_list):

        cursor = None
        seen_routes = set()

        while True:
            page = client.get_routes(cursor)

            route_arr = page.get('routes')
            valid_routes = parse_routes(route_arr, seen_routes)
            # print("valid_ routes: ", valid_routes)


            for r in valid_routes['routes']:

                if r['origin'] not in self.unique_cities:
                    self.unique_cities.add(r['origin'])

                if r['destination'] not in self.unique_cities:
                    self.unique_cities.add(r['destination'])

                if r['origin'] not in self.origin_to_destination_map:
                    self.origin_to_destination_map[r['origin']] = []

                self.origin_to_destination_map[r['origin']].append(r['destination'])
                


            cursor = page.get('next_cursor')

            if cursor is None:
                break
            # print("routes: ", page)

        print("routes: ", self.origin_to_destination_map)
        unique_route_count = unique_routes(self.origin_to_destination_map)

        return {
            "routes": self.origin_to_destination_map,
            "unique_route_count": unique_route_count,
            "airport_count": len(self.unique_cities)
        }


def parse_routes(routes_arr, seen_routes):

    # routes_arr = route_obj['routes']
    valid_routes = []
    for r in routes_arr:

        origin = r.get('origin', None)
        destination = r.get('destination', None)
        key = (origin, destination)
        if origin is None or destination is None or origin == destination or (key) in seen_routes:
            continue

        seen_routes.add((origin, destination))
        valid_routes.append(r)

    return {
        "routes": valid_routes
    }




# we probably should use breadth first search for this
def unique_routes(route_map):
    count = 0
    for k,v in route_map.items():
        count+= len(v)

    return count

def min_layovers(graph, origin, destination):

    visited = set() # create visited set

    queue = deque() # create the queue

    queue.append(origin) # start with the origin

    trips = 0 # use this counter to count how many layers we go from origin to get to destination

    while len(queue) > 0:

        for i in range(len(queue)): # finish looping in current queue
            city = queue.popleft()
            if city == destination: 
                return trips - 1
            destinations = graph.get(city, []) # get the list of destinations the origin goes to
            for dst in destinations: # go through each destination and if we haven't seen it, add it to the queue and mark it as visited
                if dst not in visited:
                    queue.append(dst)
                    visited.add(dst)

        trips+=1 # increment the trips seen

    return -1




    # def unique_routes_helper(self, origin)
        

class route_client:

    ROUTE_DATA = [
        {
            "routes": [
                {
                "origin": "LAX",
                "destination": "SEA",
                "route_id": "12"
                },
                {
                "origin": "PORT",
                "destination": "SEA",
                "route_id": "87"
                },
                {
                "origin": "ATL",
                "destination": "JFK",
                "route_id": "723"
                },
                {
                "origin": "LGA",
                "destination": "ORD",
                "route_id": "11"
                }
            ],
            "next_cursor": "page2"
        },
        {
            "routes": [
                {
                "origin": "EWR",
                "destination": "LGA",
                "route_id": "54"
                },
                {
                "origin": "DFW",
                "destination": "LGA",
                "route_id": "34"
                },
                {
                "origin": "LAX",
                "destination": "DFW",
                "route_id": "984"
                },
                {
                "origin": "DFW",
                "destination": "SFO",
                "route_id": "734"
                },
                {
                "origin": "SEA",
                "destination": "OAK",
                "route_id": "7232"
                },
                {
                "origin": "OAK",
                "destination": "CAL",
                "route_id": "3248"
                },
                {
                "origin": "CAL",
                "destination": "VAN",
                "route_id": "2341"
                }
            ],
            "next_cursor": "page3"
        },
        {
            "routes": [
                {
                "origin": "MIA",
                "destination": "LAX",
                "route_id": "345"
                },
                {
                "origin": "MIA",
                "destination": "ATL",
                "route_id": "743"
                },
                {
                "origin": "ATL",
                "destination": "STL",
                "route_id": "234"
                },
                {
                "origin": "DEN",
                "destination": "ORD",
                "route_id": "963"
                }
            ],
            "next_cursor": None
        }
    ]

    def get_routes(self, cursor=None):

        if cursor is None:
            return self.ROUTE_DATA[0]

        idx = { "page1": 0, "page2": 1, "page3": 2}.get(cursor)

        if idx is None:
            raise ValueError("page doesn't exist")

        return self.ROUTE_DATA[idx]

        


test_client = route_client()
test_route = routes()

response = test_route.build_route_graph(test_client, None)

# unique_route_count = test_route.unique_routes()
print("response: " , response)

# took 30 mins to create teh test data, and create the client to get the data by page

# created the main graph by 34 min mark. finished part 1 in 59 mins. didn't add the parse logic though
# took 16 mins for layover part

min_trips = min_layovers(test_route.origin_to_destination_map, "MIA", "VAN")

print("min layovers: ", min_trips)

# 09/02/2026

