"""
PRACTICE PROBLEM — "Device Telemetry Dashboard"
=================================================
Format: same shape as your real interview — a provided client you call,
then you transform the raw response. Part 1 = LC-Easy-ish (parse/clean),
Parts 2-3 = LC-Medium-ish (aggregate across pages, then rank with a heap).

Time budget: 40-45 min total. Don't skip running it — the client returns
intentionally messy data, and the parsing IS the problem, same as your
real one.

===========================================================================
SCENARIO
===========================================================================
You work on a fleet-monitoring backend. `DeviceTelemetryClient` wraps a
paginated internal API that returns sensor readings from IoT devices.
The API is a bit gross (nulls, mixed types, inconsistent nesting) because
it's aggregated from three different hardware generations. That's real.

You are given the client. Do not modify it. Implement the three
functions below it.

===========================================================================
PART 1 (Easy) — parse_page(response) -> list[dict]
===========================================================================
`client.get_events(cursor)` returns one page:

    {
        "events": [ <raw event dict>, ... ],
        "next_cursor": "<str>" | None
    }

Each raw event dict looks like this on a GOOD day:

    {
        "id": "evt_001",
        "device": {"id": "dev_12", "site": "atl-01"},
        "timestamp": "2026-08-20T14:03:00Z",
        "readings": [{"metric": "temp_c", "value": 41.2}, ...]
    }

But real entries may:
  - be missing "device" entirely, or have "device": None
  - have "timestamp" as None or a malformed string
  - have "readings" containing non-numeric "value" fields (e.g. "value": "ERR")
  - have "readings" missing entirely
  - occasionally the whole event dict is None (dropped by upstream)

Write `parse_page(response)` that returns a clean list of dicts:

    {"event_id": str, "device_id": str, "timestamp": datetime,
     "readings": [{"metric": str, "value": float}, ...]}

Rules:
  - Skip the event entirely if device_id or timestamp is unrecoverable. 
  - Within a kept event, drop individual readings whose value isn't a
    valid number (don't drop the whole event for one bad reading).
  - An event with zero valid readings after filtering is still kept
    (readings=[]) — a device can legitimately report nothing.

===========================================================================
PART 2 (Medium) — average_by_device(client) -> dict[str, float]
===========================================================================
Paginate through ALL pages via `client.get_events(cursor)` /
`next_cursor` until it's None. Using your Part 1 parser on each page,
compute the average of ALL reading values (across all metrics, pooled)
per device_id, rounded to 2 decimals.

Return {device_id: avg_value}. Devices with zero valid readings across
the whole fetch should be excluded from the result (avoid div by zero).

===========================================================================
PART 3 (Medium) — top_k_hottest_devices(client, k, threshold) -> list[str]
===========================================================================
Using the same fully-paginated, parsed data: find the top `k` device_ids
ranked by how many individual readings exceeded `threshold` (a raw
value, e.g. 40.0 — comparable to temp_c readings, don't worry about
units/metric-mixing for this exercise).

  - Rank by count of over-threshold readings, descending.
  - Tie-break by device_id ascending (lexicographic).
  - Return just the list of device_ids, length <= k.
  - You have < k qualifying devices? Return all of them.

Use a heap (heapq) for the top-k selection — don't just sort everything
and slice, even though it'd pass on this input size. Be ready to say
why: sort is O(n log n), a size-k heap is O(n log k), and if this were
streaming (readings arriving continuously) the heap approach doesn't
need the whole dataset in memory at once the way a full sort does.

===========================================================================
THE CLIENT (do not modify — this simulates the provided SDK)
===========================================================================
"""

from datetime import datetime, timezone
import heapq

class HeapEntry:

    def __init__(self, device_id, count):
        self.count = count
        self.device_id = device_id


    def __lt__(self, other):

        if self.count != other.count:
            return self.count < other.count

        return self.device_id > other.device_id

class Device:

    def __init__(self, id):
        self.device_id = id
        self.reading_count = 0
        self.value_total = 0


class DeviceAnalytics:

    def __init__(self):
        self.device_id_to_device = {} # we can look up the device and append a new event to it's list, we can increment the total.
        # we can get the average by dividing the total by the length of the events
        # we will skip and not include malformed events


    def average_by_device(self, client) -> dict:
    # TODO: Part 2

        cursor = None
        valid_events = []

        valid_events = ingest(client)

        print("events: ", valid_events)
        # look at each event and get the device Id
        for evt in valid_events:
            # print("evt: ", evt)
            device_id = evt['device_id']
            if device_id not in self.device_id_to_device:
                device = Device(device_id)

            else:
                device = self.device_id_to_device[device_id]

            for r in evt['readings']:
                # print("r: ", r)
                device.value_total += r['value']
                device.reading_count +=1


            self.device_id_to_device[device_id] = device

        
        average_per_device = {}

        for k,v in self.device_id_to_device.items():
            if v.reading_count > 0:
                print("dev count: ", v.reading_count, " device total value: ", v.value_total)
                avg = round((v.value_total / v.reading_count),2)
                average_per_device[k] = avg

        print("average per device: ",average_per_device )

        return average_per_device

    def top_k_hottest_devices(self, client, k, threshold):

        device_id_to_threshold_count = {}
        valid_events = ingest(client)

        for evt in valid_events:
            device_id = evt.get('device_id')
            
            for reading in evt.get("readings"):

                if reading.get('value') > threshold:
                    device_id_to_threshold_count[device_id] = device_id_to_threshold_count.get(device_id,0) + 1


        print("devices above k: ", device_id_to_threshold_count)

        # now let's put the results in a min heap
        sorted_top_k = []
        for dev_k, dev_count in device_id_to_threshold_count.items():

            new_device = HeapEntry(dev_k, dev_count)
            # existing_device = HeapEntry(dev_k, dev_count)

            if len(sorted_top_k) < k:
                heapq.heappush(sorted_top_k, new_device)

            else:
                print("sorted_top_k[0].count", sorted_top_k[0].count)
                existing_device= sorted_top_k[0]
                if new_device.count > existing_device.count:
                    heapq.heappushpop(sorted_top_k, new_device)

        
        sorted_devices = []

        sorted_devices = sorted(sorted_top_k, key=lambda d: (-d.count, d.device_id))

        sorted_device_ids = []

        for s_dev in sorted_devices:
            sorted_device_ids.append(s_dev.device_id)

        print("sorted_device_ids: ", sorted_device_ids)

        return sorted_device_ids












class DeviceTelemetryClient:

    """Simulates a paginated internal telemetry API. 3 pages, deliberately messy."""

    _PAGES = [
        {
            "events": [
                {"id": "evt_001", "device": {"id": "dev_12", "site": "atl-01"},
                 "timestamp": "2026-08-20T14:03:00Z",
                 "readings": [{"metric": "temp_c", "value": 41.2},
                              {"metric": "temp_c", "value": 39.8}]},
                {"id": "evt_002", "device": {"id": "dev_07", "site": "atl-01"},
                 "timestamp": "2026-08-20T14:03:05Z",
                 "readings": [{"metric": "temp_c", "value": "ERR"},
                              {"metric": "temp_c", "value": 22.5}]},
                None,  # dropped upstream event
                {"id": "evt_004", "device": None,
                 "timestamp": "2026-08-20T14:03:10Z",
                 "readings": [{"metric": "temp_c", "value": 55.0}]},
                {"id": "evt_005", "device": {"id": "dev_12", "site": "atl-01"},
                 "timestamp": "2026-08-20T14:03:15Z",
                 "readings": [{"metric": "temp_c", "value": 44.4}]},
            ],
            "next_cursor": "page2",
        },
        {
            "events": [
                {"id": "evt_006", "device": {"id": "dev_31", "site": "nyc-03"},
                 "timestamp": None,
                 "readings": [{"metric": "temp_c", "value": 30.0}]},
                {"id": "evt_007", "device": {"id": "dev_07", "site": "atl-01"},
                 "timestamp": "2026-08-20T14:04:00Z",
                 "readings": None},
                {"id": "evt_008", "device": {"id": "dev_31", "site": "nyc-03"},
                 "timestamp": "2026-08-20T14:04:05Z",
                 "readings": [{"metric": "temp_c", "value": 41.0},
                              {"metric": "temp_c", "value": "n/a"},
                              {"metric": "temp_c", "value": 43.9}]},
                {"id": "evt_009", "device": {"id": "dev_12", "site": "atl-01"},
                 "timestamp": "not-a-real-timestamp",
                 "readings": [{"metric": "temp_c", "value": 40.0}]},
            ],
            "next_cursor": "page3",
        },
        {
            "events": [
                {"id": "evt_010", "device": {"id": "dev_99", "site": "nyc-03"},
                 "timestamp": "2026-08-20T14:05:00Z",
                 "readings": [{"metric": "temp_c", "value": 41.5},
                              {"metric": "temp_c", "value": 42.5}]},
                {"id": "evt_011", "device": {"id": "dev_07", "site": "atl-01"},
                 "timestamp": "2026-08-20T14:05:10Z",
                 "readings": [{"metric": "temp_c", "value": 20.0}]},
                {"id": "evt_012", "device": {"id": "dev_31", "site": "nyc-03"},
                 "timestamp": "2026-08-20T14:05:20Z",
                 "readings": []},
            ],
            "next_cursor": None,
        },
    ]

    def get_events(self, cursor=None):
        if cursor is None:
            return self._PAGES[0]
        idx = {"page2": 1, "page3": 2}.get(cursor)
        if idx is None:
            raise ValueError(f"invalid cursor: {cursor}")
        return self._PAGES[idx]


            


# ===========================================================================
# YOUR CODE BELOW
# ===========================================================================

def valid_timestamp(timestamp_str: str) -> bool:
    try:
        if timestamp_str is None:
            raise ValueError("timestamp is none")
        return datetime.fromisoformat(timestamp_str)

    except (ValueError, TypeError):
        return None

def is_valid_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def parse_page(response: dict) -> list[dict]:
    # TODO: Part 1

    events = response['events']
    valid_events = []

    for evt in events:
        # print("evt: ", evt)
        # if device id is missing, device is None, skip the event
        if not evt:
            continue
        if not evt.get("device") or not evt.get("device").get("id"):
            continue

        # if timestamp is malformed, skip
        new_ts = valid_timestamp(evt['timestamp'])
        if not new_ts:
            continue
        
        readings = evt.get('readings') or []
        valid_readings = []
        for r in readings:
            if is_valid_number(r['value']):
                valid_readings.append(r)
        new_evt = {

            "event_id": evt["id"],
            "timestamp": new_ts,
            "device_id": evt.get('device').get('id'),
            "readings": valid_readings
        }
        # evt['readings'] = valid_readings
        valid_events.append(new_evt)
    # print("valid: events: ", valid_events)


    return valid_events

def ingest(client):
    valid_events = []
    cursor = None
    while True:
        page = client.get_events(cursor)
        page_events = parse_page(page)
        valid_events += page_events
        cursor = page.get("next_cursor")
        if cursor is None:
            break

    return valid_events

# if readings value property is not a number, drop the readings
# keep an event that has an empty reading






    # raise NotImplementedError


    # def top_k_hottest_devices(self, client: DeviceTelemetryClient, k: int, threshold: float) -> list:
    #     # TODO: Part 3
    #     raise NotImplementedError


# ===========================================================================
# TEST HARNESS — run this file directly to check your work
# ===========================================================================

def _run_tests():
    client = DeviceTelemetryClient()

    # --- Part 1 ---
    page1 = client.get_events()
    parsed = parse_page(page1)
    ids = sorted(e["event_id"] for e in parsed)
    print("Part 1 parsed event_ids:", ids)
    # evt_003 is None (dropped upstream), evt_004 has device=None (unrecoverable device_id)
    # -> both should be excluded. evt_001/002/005 have valid device_id + timestamp.
    assert set(ids) == {"evt_001", "evt_002", "evt_005"}, \
        f"expected evt_001/002/005 kept, got {ids}"
    evt002 = next(e for e in parsed if e["event_id"] == "evt_002")
    assert len(evt002["readings"]) == 1, "evt_002 has one bad reading (\"ERR\") that should be dropped, one good"
    print("Part 1: looks right\n")

    # --- Part 2 ---
    analytics_client = DeviceAnalytics()
    averages = analytics_client.average_by_device(client)
    print("Part 2 averages_by_device:", averages)
    assert "dev_12" in averages
    print("Part 2: spot-check the numbers above by hand against the fixture\n")

    # # --- Part 3 ---
    top2 = analytics_client.top_k_hottest_devices(client, k=2, threshold=40.0)
    # print("Part 3 top_k_hottest_devices(k=2, threshold=40.0):", top2)
    # print("Part 3: spot-check ranking above by hand against the fixture\n")


if __name__ == "__main__":
    _run_tests()



# most of the trouble came from parsing the objects from teh response correct. accessing it by property string name instead of using dot notation to access the object