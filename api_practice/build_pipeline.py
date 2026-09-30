"""
PRACTICE PROBLEM #2 — "CI Build Order Resolver"
=================================================
Same interview shape: a provided client, paginated + messy responses,
three parts of increasing difficulty. This one uses a graph instead of
a heap for the final part — Kahn's algorithm for topological sort,
directly relevant to dependency-resolution / package-install-order
style questions.

Time budget: 40-45 min. Run it as you go — the messiness IS the problem.

===========================================================================
SCENARIO
===========================================================================
You work on internal CI tooling. `BuildPipelineClient` wraps a paginated
API that returns the set of build tasks registered for a project, each
with a list of task_ids it depends on. You need to figure out a valid
build order (dependencies before dependents), or detect that no valid
order exists.

You are given the client. Do not modify it. Implement the three
functions below it.

===========================================================================
PART 1 (Easy) — parse_page(response) -> list[dict]
===========================================================================
`client.get_tasks(cursor)` returns one page:

    {
        "tasks": [ <raw task dict>, ... ],
        "next_cursor": "<str>" | None
    }

Each raw task dict on a GOOD day:

    {"task_id": "compile", "name": "Compile", "depends_on": ["fetch_deps"]}

Real entries may:
  - be `None` entirely (dropped upstream)
  - have a non-string "task_id" (e.g. an int) — unrecoverable, skip the
    whole task
  - be missing "name" — default it to the task_id
  - be missing "depends_on" entirely — treat as []
  - have "depends_on" containing non-string entries (None, ints, etc.)
    — drop those individual entries, keep the task and its other valid
    dependencies

Return a clean list of:
    {"task_id": str, "name": str, "depends_on": [str, ...]}

===========================================================================
PART 2 (Medium) — build_dependency_graph(client) -> dict[str, list[str]]
===========================================================================
Paginate through ALL pages via `client.get_tasks(cursor)` / `next_cursor`
until it's None. Using your Part 1 parser, build a single adjacency map:
    {task_id: [depends_on task_ids]}

Rules:
  - A task_id may appear more than once across pages (the same task can
    get re-sent, e.g. after a retry). The LAST occurrence wins — replace
    the earlier entry entirely, don't merge dependency lists.
  - A depends_on entry may reference a task_id that never appears as its
    own task anywhere in the full dataset (e.g. an external/third-party
    dependency outside this system). Keep it in the list as-is here —
    Part 3 decides how to handle it. Part 2 is just "build the graph
    faithfully from what you saw."

===========================================================================
PART 3 (Medium) — topological_build_order(client) -> list[str] | None
===========================================================================
Using the graph from Part 2, compute a valid build order: every task
appears after all of its dependencies. Use Kahn's algorithm (in-degree
counting + a frontier of ready nodes), not DFS-based topo sort.

Rules:
  - Treat any depends_on id that never appears as its own task in the
    graph as already-satisfied — it should NOT block that task, and it
    should NOT appear in the output (it's outside the system).
  - When multiple tasks are simultaneously ready (in-degree 0) at the
    same step, break ties by picking the lexicographically smallest
    task_id first. Use a heap for this frontier, not just a list/deque
    — same reasoning as Part 3 of the last problem: deterministic
    output, and it generalizes if the frontier gets large.
  - If a cycle exists anywhere (including a task that depends on
    itself), a complete order is impossible. Return None in that case.

===========================================================================
THE CLIENT (do not modify — this simulates the provided SDK)
===========================================================================
"""

import heapq

class task:

    def __init__(self, task_id, name, depends_on):
        self.task_id = task_id
        self.name = name
        self.depends_on = depends_on

class tasks:

    def __init__(self):
        self.task_id_to_task = {}
    
class BuildPipelineClient:
    """Simulates a paginated internal CI task registry. 3 pages, deliberately messy."""

    _PAGES = [
        {
            "tasks": [
                {"task_id": "fetch_deps", "name": "Fetch Dependencies", "depends_on": []},
                {"task_id": "lint", "name": "Lint", "depends_on": []},
                None,  # dropped upstream
                {"task_id": "compile", "name": "Compile", "depends_on": ["fetch_deps"]},
                {"task_id": 42, "name": "Bad ID Task", "depends_on": []},  # non-string task_id
            ],
            "next_cursor": "page2",
        },
        {
            "tasks": [
                {"task_id": "seed_db", "depends_on": ["fetch_deps"]},  # no "name"
                {"task_id": "unit_test", "name": "Unit Tests",
                 "depends_on": ["compile", None, 5]},  # bad deps mixed with good
                {"task_id": "compile", "name": "Compile (retry)",
                 "depends_on": ["fetch_deps", "lint"]},  # duplicate task_id, later wins
                {"task_id": "integration_test", "name": "Integration Tests",
                 "depends_on": ["compile", "seed_db", "external_service"]},  # external_service never defined
            ],
            "next_cursor": "page3",
        },
        {
            "tasks": [
                {"task_id": "package", "name": "Package",
                 "depends_on": ["unit_test", "integration_test", "lint"]},
                {"task_id": "deploy", "name": "Deploy", "depends_on": ["package"]},
                {"task_id": "flaky", "name": "Flaky Self-Loop", "depends_on": ["flaky"]},
            ],
            "next_cursor": None,
        },
    ]

    def get_tasks(self, cursor=None):
        if cursor is None:
            return self._PAGES[0]
        idx = {"page2": 1, "page3": 2}.get(cursor)
        if idx is None:
            raise ValueError(f"invalid cursor: {cursor}")
        return self._PAGES[idx]


# ===========================================================================
# YOUR CODE BELOW
# ===========================================================================

def parse_page(response: dict) -> list:
    # TODO: Part 1

    # {"task_id": str, "name": str, "depends_on": [str, ...]}

    print(" response of page 1: ", response)
    # get the tasks. 
    # !!! also address if 'tasks' property is missing

#     Real entries may:
#   - be `None` entirely (dropped upstream)
#   - have a non-string "task_id" (e.g. an int) — unrecoverable, skip the
#     whole task
#   - be missing "name" — default it to the task_id
#   - be missing "depends_on" entirely — treat as []
#   - have "depends_on" containing non-string entries (None, ints, etc.)
#     — drop those individual entries, keep the task and its other valid
#     dependencies

    tasks = response.get("tasks")
    valid_tasks = []

    for task in tasks:

        if task is None:
            continue

        if not (is_valid_string(task.get('task_id'))):
            continue

        print("hello")
        task_id = task.get('task_id')
        name = task.get('name', task_id)
        depends_on = task.get('depends_on') or []

        updated_deps = []
        for dp in depends_on:

            if is_valid_string(dp):
                updated_deps.append(dp)

        
        new_task_list = {
            'task_id': task_id,
            'name': name,
            'depends_on': updated_deps
        }

        valid_tasks.append(new_task_list)

    print("------------------------------")
    print("new task list: ", valid_tasks)

    return valid_tasks




    
def is_valid_string(task_id):

    return isinstance(task_id, str)


def build_dependency_graph(client) -> dict:
    # TODO: Part 2

    cursor = None
    task_id_to_dependencies = {}
    while True:
        current_page = client.get_tasks(cursor)
        print("current_page: ", current_page)
        cursor = current_page.get('next_cursor')
        # print("cursor: ", cursor)

        tasks = parse_page(current_page)

        for t in tasks:
            task_id_to_dependencies[t['task_id']] = t['depends_on']

        if cursor is None:
            break

    print("task_id_to_dependencies: " , task_id_to_dependencies)
    return task_id_to_dependencies

    # raise NotImplementedError




def topological_build_order(client):
    # TODO: Part 3


    raise NotImplementedError


# ===========================================================================
# TEST HARNESS — run this file directly to check your work
# ===========================================================================

def _run_tests():
    client = BuildPipelineClient()

    # --- Part 1 ---
    page1 = client.get_tasks()
    parsed = parse_page(page1)
    ids = sorted(t["task_id"] for t in parsed)
    print("Part 1 parsed task_ids:", ids)
    assert set(ids) == {"fetch_deps", "lint", "compile"}, \
        f"expected fetch_deps/lint/compile kept (None entry and int task_id dropped), got {ids}"
    print("Part 1: looks right\n")

    # # --- Part 2 ---
    graph = build_dependency_graph(client)
    print("Part 2 graph:", graph)
    assert graph.get("compile") == ["fetch_deps", "lint"], \
        f"expected compile's LATER definition (page 2) to win, got {graph.get('compile')}"
    assert graph.get("unit_test") == ["compile"], \
        f"expected unit_test's bad deps (None, 5) dropped, got {graph.get('unit_test')}"
    print("Part 2: spot-check the graph above by hand against the fixture\n")

    # # --- Part 3 ---
    # order = topological_build_order(client)
    # print("Part 3 topological_build_order:", order)
    # print("Part 3: 'flaky' depends on itself -> no valid total order exists, "
    #       "so this should print None. If you get a list instead, check your "
    #       "cycle-detection condition.\n")


if __name__ == "__main__":
    _run_tests()


# got part 1 and 2 in 50 mins. I wasted a lot of time trying to figure out how to know if a variable is a string or not