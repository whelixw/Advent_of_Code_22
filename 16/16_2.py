#todo: fix dummy node and cases. pruning should be done before combinations are built and should not allow to go to previous node
from collections import deque
from itertools import product
import copy
file = "16/test.txt"
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

def bfs_with_flow(start_node, graph, max_time, verbose = False):

    def break_with_dummy_node(new_time, new_flow,
                              new_released,
                              new_open_valves, gates,
                              path1, path2):

        #if (len(queue) == 0 and new_time < max_time) and pair_index == action_pair_len-1:
        print("something is going wrong")

        #queue = deque()
        queue= deque([(
            new_time,
            "%%",
            "%%",
            new_flow,
            new_released,
            new_open_valves,
            gates,
            path1+["%%"],
            path2+["%%"]
        )])
        print(queue)
        return queue

    # The queue stores the state for each path being explored.
    # State: (time, pos_1, pos_2, current_flow, current_released, open_valves, gates, path1, path2)
    #queue = deque([(0, start_node, start_node, 0, 0, frozenset(), base_gates])
    queue = deque([(0, start_node, start_node, 0, 0, frozenset(), [base_gates, base_gates], list(), list())])
    final_state = False
    ultimate_flow = 81
    max_released = 0
    max_flow = 0
    max_state = []
    max_history = []
    # A 'visited' dictionary is used for pruning. It stores the maximum
    # flow achieved for a given state (location, open_valves).
    visited = {}
    last_time = 0
    debug = False
    while queue:
        """        (
            time,
             current_pos_1,
             current_pos_2,
             current_flow,
             current_released,
             open_valves,
             gates
        ) = queue.popleft()"""
        (
            time,
            current_pos_1,
            current_pos_2,
            current_flow,
            current_released,
            open_valves,
            gates,
            path1,
            path2
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
            old_max = max_released
            print("time advanced to: ", time)
            print("max flow: ", max_flow)
            print("max released : ", max_released)
            max_history.append(max_released)
            last_time = time
        old_released = current_released
        current_released += current_flow
        if current_released > max_released:
            max_released = current_released
            max_flow = current_flow
            max_state = path1, path2
            #max_valves = open_valves

        if final_state: #and time >= max_time:
            queue = break_with_dummy_node(time+1, current_flow, current_released,
                                                       new_open_valves, gates, path1, path2)
            print("queue")
            print(queue)
        else:

            actions_1 = [current_pos_1]+graph[current_pos_1].edges
            actions_2 = [current_pos_2]+graph[current_pos_2].edges

            #actions_1 = [1,2,3]
            #actions_2 = [1,2,3]
            action_pairs = (tuple(combo)
                     for combo in product(actions_1, actions_2))
            #print(tuple(action_pairs))
            action_pairs = tuple(action_pairs)
            #print(path1,path2)
            #for action_pair in action_pairs: #todo: gates should only be set for one cursor
            for pair_index in range(len(action_pairs)):
                action_pair = action_pairs[pair_index]
                reset_gates = False
                new_time = time + 1
                new_flow = current_flow
                new_states = list()
                new_released = current_released
                new_open_valves = open_valves
                #print("gates: ", gates, time)
                new_gates = copy.deepcopy(gates)
                #print(path1+[action_pair[0]], path2+[action_pair[1]])
                for index in range(len(action_pair)):
                    prune = True
                    action = action_pair[index]
                    if index == 0:
                        current_pos = current_pos_1
                    elif index == 1:
                        current_pos = current_pos_2
                    if action in {"DD", "BB"}:
                        #print(path1, path2, action, index)
                        #print(action_pairs, "\n")
                        pass
                    if action == current_pos:
                        if (
                            graph[action].flow > 0
                            and action not in new_open_valves
                        ):
                            new_open_valves = new_open_valves | {action}
                            new_flow = new_flow + graph[action].flow

                            reset_gates = True
                            new_states.append(action)

                        else:
                            if verbose:
                                pass
                                print("prune action ", action, "valves illegal")

                            break
                    else:
                        #print(gates," ",[path1, path2])
                        if action not in gates[index] or reset_gates: #this line seems wierd to me
                            if time > 3:
                                if max_history[time-3] < current_released:
                                    prune = False
                            else:
                                prune = False
                            if not prune:
                                #print("adding to gates: ", action)
                                new_gates[index] = new_gates[index] | {action}
                                new_states.append(action)
                        if prune:
                            if verbose:
                                paths = [path1, path2]
                                paths[index] = paths[index]+[action]
                                print("pruned, ", action, " due to gates or time ", paths)
                                #print(gates, index)


                            break


                if reset_gates:
                    new_gates = [base_gates, base_gates]
                    debug = False
                if len(new_states) != 2:
                    if verbose:
                        print("err: new states: ", new_states, path1, path2)
                        pass

                    pass
                elif (new_flow == ultimate_flow and old_released == old_max):
                    final_state = True
                    queue = break_with_dummy_node(new_time, new_flow,
                                                  new_released,
                                                  new_open_valves, new_gates,
                                                  path1 + [new_states[0]],
                                                  path2 + [new_states[1]])
                else:
                    if verbose:
                        #print("added state: ", new_states)
                        pass
                    queue.append(
                    (
                        new_time,
                        new_states[0],
                        new_states[1],
                        new_flow,
                        new_released,
                        new_open_valves,
                        new_gates,
                        path1+[new_states[0]],
                        path2+[new_states[1]]
                    )
                )
    return max_released, max_flow, max_state

print(bfs_with_flow("AA", graph, 26))

