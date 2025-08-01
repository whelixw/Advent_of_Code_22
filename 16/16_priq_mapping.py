#todo: fix dummy node and cases. pruning should be done before combinations are built and should not allow to go to previous node
from collections import deque
from itertools import product
import copy
import queue as que
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

useful_valves=set()
with(open(file)) as f:
    for line in f:
        line = line.split(" ")
        name = line[1]
        flow_rate = int(line[4][5:-1])
        edges = [i.strip(",").strip() for i in line[9:]]
        print(name, flow_rate,edges)
        graph[name] = Node(flow_rate, edges)
        if flow_rate > 0:
            useful_valves.add(name+"o")




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
            path2+["%%"],
            ("%%","%%")
        )])
        print(queue)
        return queue

    def estimate_trajectory(current_released, current_flow, current_time, target_time):
        return current_released+(current_flow*(target_time-current_time))

    def estimate_best_case(current_released, current_flow, current_time, target_time, ultimate_flow):
        return current_released+current_flow+(ultimate_flow*(target_time-current_time-1))

    # The queue stores the state for each path being explored.
    # State: (time, pos_1, pos_2, current_flow, current_released, open_valves, gates, path1, path2)
    #queue = deque([(0, start_node, start_node, 0, 0, frozenset(), base_gates])
    queue = que.PriorityQueue()
    iteration = 0
    queue.put((0,(0, start_node, start_node, 0, 0, frozenset(), [base_gates, base_gates], list(), list(), ("00","00"))))
    final_state = False
    ultimate_flow = 81
    max_released = 0
    max_flow = 0
    max_state = []
    max_history = []
    max_trajectory = 0
    # A 'visited' dictionary is used for pruning. It stores the maximum
    # flow achieved for a given state (location, open_valves).
    visited = {}
    last_time = 0
    debug = False
    while queue.qsize() != 0:
        """        (
            time,
             current_pos_1,
             current_pos_2,
             current_flow,
             current_released,
             open_valves,
             gates  
        ) = queue.popleft()"""
        _, (
            time,
            current_pos_1,
            current_pos_2,
            current_flow,
            current_released,
            open_valves,
            gates,
            path1,
            path2,
            last_actions
        ) = queue.get()
        iteration += 1
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
            print("length of queue: ", queue.qsize())
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

            #actions_1 = [current_pos_1]+graph[current_pos_1].edges
            #actions_2 = [current_pos_2]+graph[current_pos_2].edges
            valves_1=set()
            valves_2=set()
            if current_pos_1+"o" not in open_valves:
                valves_1.add(current_pos_1+"o")
            if current_pos_2+"o" not in open_valves:
                valves_2.add(current_pos_2+"o")


            actions_1 = set(set(graph[current_pos_1].edges)
                            - set(last_actions[0]).union(set(gates[0]))).union(valves_1)
            actions_2 = set(set(graph[current_pos_2].edges)
                            - set(last_actions[1]).union(set(gates[1]))).union(valves_2)

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
                #print(action_pair)
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
                    #print(action)
                    if index == 0:
                        current_pos = current_pos_1
                    elif index == 1:
                        current_pos = current_pos_2
                    if action in {"DD", "BB"}:
                        #print(path1, path2, action, index)
                        #print(action_pairs, "\n")
                        pass
                    if action[-1] == "o":
                        if (
                            graph[action[:-1]].flow > 0
                            and action not in new_open_valves
                        ):
                            new_open_valves = new_open_valves | {action}
                            new_flow = new_flow + graph[action[:-1]].flow

                            reset_gates = True
                            new_states.append(action[:-1])

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
                    '''elif (new_flow == ultimate_flow and old_released == old_max):
                    final_state = True
                    queue = break_with_dummy_node(new_time, new_flow,
                                                  new_released,
                                                  new_open_valves, new_gates,
                                                  path1 + [new_states[0]],
                                                  path2 + [new_states[1]])'''
                else:
                    if verbose:
                        #print("added state: ", new_states)
                        pass
                    trajectory = estimate_trajectory(new_released, new_flow, new_time, max_time)
                    best_case = estimate_best_case(new_released, new_flow, new_time, max_time, ultimate_flow)
                    if best_case < max_trajectory:
                        #print("bc is worse than max_trajectory")
                        if iteration % 10000 == 0:
                            print(queue.qsize(), max_released)
                        pass
                        #continue

                    elif trajectory > max_trajectory:
                        max_trajectory = trajectory
                    priority = -trajectory

                    queue.put(
                    (priority,
                    (
                        new_time,
                        new_states[0],
                        new_states[1],
                        new_flow,
                        new_released,
                        new_open_valves,
                        new_gates,
                        path1+[new_states[0]],
                        path2+[new_states[1]],
                        tuple(new_states)
                    )
                    )
                    )
                    #print(queue)
    print("queue is empty")
    return max_released, max_flow, max_state

#print(bfs_with_flow("AA", graph, 26))
#print(bfs_with_flow("AA", graph, 26, verbose=True))

a,b,c = (bfs_with_flow("AA", graph, 5),bfs_with_flow("AA", graph, 6),
          bfs_with_flow("AA", graph, 7))

print(a,b,c)