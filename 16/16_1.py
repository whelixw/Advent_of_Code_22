from collections import deque
file = "16/input.txt"
test_path = [
    "DD", "DD", "CC", "BB", "BB", "AA", "II", "JJ", "JJ", "II", "AA",
    "DD", "EE", "FF", "GG", "HH", "HH", "GG", "FF", "EE", "EE", "DD",
    "CC", "CC"
]


graph = {}
#max_flow = {}

class Node:
    def __init__(self, flow, edges):
        self.flow = flow
        self.edges = edges

with(open(file)) as f:
    for line in f:
        line = line.split(" ")
        name = line[1]
        flow_rate = int(line[4][5:-1])
        edges = [i.strip(",").strip() for i in line[9:]]
        print(name, flow_rate,edges)
        graph[name] = Node(flow_rate, edges)
base_gates=frozenset()

def bfs_with_flow(start_node, graph, max_time):
    # The queue stores the state for each path being explored.
    # State: (time, current_node, current_flow, current_released, open_valves, path, gates)
    queue = deque([(0, start_node, 0, 0, frozenset(), base_gates)])
    max_released = 0
    max_history = []
    # A 'visited' dictionary is used for pruning. It stores the maximum
    # flow achieved for a given state (location, open_valves).
    visited = {}
    last_time = 0
    debug = False
    while queue:
        (
            time,
             current_node,
             current_flow,
             current_released,
             open_valves,
             gates
        ) = queue.popleft()
        #if path[:24] == test_path[:time]:
            #debug = True
            #pass
        if time >= max_time:
            if debug:
                pass
                #print(path, current_flow, current_released)
            continue #leaves iteration
        if time == last_time+1:
            print("time advanced to: ", time)
            #print("current flow: ", current_flow)
            #print("max released : ", max_released)
            max_history.append(max_released)
            last_time = time
        current_released += current_flow
        if current_released > max_released:
            max_released = current_released
            #max_state = path
            #max_valves = open_valves



        for action in [current_node]+graph[current_node].edges:
            prune = True
            #print(action)
            if action == current_node:
                #print("c")
                if (
                    graph[current_node].flow > 0
                    and current_node not in open_valves
                ):
                    new_time = time + 1
                    new_released = current_released
                    new_flow = current_flow + graph[current_node].flow
                    new_open_valves = open_valves | {current_node}
                    #state_key = (current_node, new_open_valves)
                    #visited[state_key] = new_flow
                    debug=False
                    queue.append(
                        (
                            new_time,
                            current_node,
                            new_flow,
                            new_released,
                            new_open_valves,
                            base_gates
                        )
                    )
            else:
                new_time = time + 1
                new_released = current_released
                #state_key = (action, open_valves)
                #if debug and state_key in visited:
                    #print(state_key,current_flow, visited[state_key])
                #if (state_key not in visited or open_valves == frozenset({'EE', 'BB', 'HH', 'JJ', 'CC', 'DD'})):
                #if ((state_key not in visited or visited[state_key] <= current_flow)
                if action not in gates:
                    if time > 3:
                        if max_history[time-3] < current_released:
                            prune = False
                    else:
                        prune = False
                    if not prune:
                        #visited[state_key] = current_flow
                        debug=False
                        queue.append(
                            (
                                new_time,
                                action,
                                current_flow,
                                new_released,
                                open_valves,
                                gates|{action}
                            )
                        )
                    else:
                        pass
                        """print("wtf")
                        print(state_key, current_flow)
                        print(visited[state_key])"""
    return max_released

print(bfs_with_flow("AA", graph, 30))

#_,_,path = bfs_with_flow("AA",graph,30)

'''def calculate_max_released(path, graph, max_time, start_node="AA"):
    """
    Calculates the total pressure released for a given path of actions.

    This function simulates the passage of time and calculates the cumulative
    pressure released based on a predefined sequence of moves and valve openings.

    Args:
        path (list): A sequence of actions. An action is a node name (str).
                     If the action string is the same as the current node,
                     it's interpreted as opening the valve. Otherwise, it's a
                     move to the specified adjacent node.
        graph (dict): The graph structure, mapping node names to Node objects.
                      Each Node must have a 'flow' attribute.
        max_time (int): The total time available for the simulation.
        start_node (str, optional): The starting node. Defaults to "AA".

    Returns:
        int: The total pressure released over the entire duration.
    """
    time = 0
    current_node = start_node
    current_flow = 0
    total_released = 0

    # Create an iterator for the path to consume it one action at a time
    path_iterator = iter(path)

    # The main simulation loop runs for max_time minutes.
    while time < max_time:
        # At the beginning of each minute, the currently open valves release
        # pressure. This is added to the total.
        total_released += current_flow

        # An action is taken, which consumes one minute.
        time += 1

        # Get the next action from the path. If the path is exhausted,
        # action will be None, and we will just wait.
        action = next(path_iterator, None)

        if action is None:
            # No more actions in the path, so we just wait. The loop
            # continues, accumulating 'current_flow' each remaining minute.
            continue

        # Check if the action is to open the valve or to move.
        if action == current_node:
            # Action: Open the valve at the current location.
            # The flow from this valve will start contributing from the *next* minute.
            current_flow += graph[current_node].flow
        else:
            # Action: Move to a new node.
            current_node = action

    return total_released'''

#calculate_max_released(path,graph,30, "AA")





# Calculate the released pressure for that specific path
#calculated_release = calculate_max_released(test_path, graph, 30, "AA")
#print(calculated_release)

len(test_path)