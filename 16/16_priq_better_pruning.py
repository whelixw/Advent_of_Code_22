#((105, 44, (['DD', 'DD', 'EE', 'EE'], ['II', 'JJ', 'JJ', 'II'])), (156, 54, (['DD', 'DD', 'AA', 'BB', 'BB'], ['II', 'JJ', 'JJ', 'II', 'AA'])), (210, 54, (['DD', 'DD', 'AA', 'BB', 'BB', 'AA'], ['II', 'JJ', 'JJ', 'II', 'AA', 'DD'])), (266, 56, (['DD', 'DD', 'AA', 'BB', 'BB', 'CC', 'CC'], ['II', 'JJ', 'JJ', 'II', 'AA', 'DD', 'AA'])), (338, 76, (['DD', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG'], ['BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA'])), (414, 76, (['DD', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'HH'], ['BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA', 'DD'])))
#1540 is too low
#todo: figure out what is going on. Jailed has weird interactions with the rest, especially opening valves
from collections import deque
from heapq import heappush, heappop
from itertools import product
import copy
import time
start_time = time.time()

#import numpy as np
#import heapq
file = "16/test.txt"



from sortedcontainers import SortedList
graph = {}
#max_flow = {}

class Node:
    def __init__(self, flow, edges, edge_costs = {}):
        self.flow = flow
        self.edges = edges
        self.edge_costs = edge_costs

    def calculate_distance_to_node(self, target, own_name, depth=0):
        queue = deque([(own_name, depth, "00")])
        while queue:
            origin_node, depth, direction=queue.popleft()
            if depth == 1:
                direction = origin_node
            if origin_node == target:
                return depth, origin_node, direction
            else:
                for node in graph[origin_node].edges:
                    queue.append((node, depth+1, direction))



    def calculate_direct_paths(self, valves, own_name):
        paths = []
        for key in valves:
            #print(key)
            depth, node, direction = self.calculate_distance_to_node(key, own_name)
            paths.append((key,depth))
        self.paths = paths


class SortedContainersExcluder:
    def __init__(self, data):
        self._data = data
        # Values are stored in a sorted list from the start
        self._sorted_values = SortedList(data.values())[::-1]

    def get_sorted_values_excluding(self, keys_to_exclude):
        # Make a copy to avoid modifying the original
        result = self._sorted_values.copy()

        values_to_remove = [
            self._data[key] for key in keys_to_exclude if key in self._data
        ]

        for value in values_to_remove:
            # remove() is efficient in SortedList: O(log N)
            result.remove(value)

        return list(result)


valves_dict = dict()
valve_names = list()
useful_valves=set()
ultimate_flow = 0
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
            ultimate_flow+=flow_rate
            valve_names.append(name)
            valves_dict[name+"o"] = flow_rate

#graph["FR"].calculate_distance_to_node("WG", "FR")

#graph["FR"].calculate_direct_paths(valve_names, "FR")

simple_graph = {}

for valve in (["AA"]+ valve_names):
    graph[valve].calculate_direct_paths(valve_names, valve)
    simple_graph[valve] = Node(graph[valve].flow, list(dict(graph[valve].paths).keys()), dict(graph[valve].paths))

sorted_valves = SortedContainersExcluder(valves_dict)

print("ultimate_flow:", ultimate_flow)




base_gates=frozenset()

def bfs_with_flow(start_node, graph, max_time, verbose = False):

    def estimate_trajectory(current_released, current_flow, current_time, target_time):
        return current_released+(current_flow*(target_time-current_time))

    def fast_best_case(current_released, current_flow, current_time, target_time, ultimate_flow):
        return current_released+current_flow+(ultimate_flow*(target_time-current_time-1))

    def estimate_best_case(current_released, current_flow, current_time,
                           target_time, sorted_valves, current_valves):
        remaining_valves = sorted_valves.get_sorted_values_excluding(list(current_valves))
        simulated_time = current_time+1
        simulated_flow = current_flow
        simulated_released = current_released+current_flow
        valves_reached = 0
        skip = False
        while (simulated_time < target_time):
            #if valves_reached < len(remaining_valves):
            if not skip:
                difference = len(remaining_valves) - valves_reached
                if difference > 1:
                    simulated_flow += remaining_valves[valves_reached]
                    simulated_flow += remaining_valves[valves_reached+1]
                    valves_reached += 2
                elif difference == 1:
                    simulated_flow += remaining_valves[valves_reached]
                    valves_reached += 1
                skip = True
                #print("added", remaining_valves[valves_reached])
            else:
                skip = False
            simulated_released += simulated_flow
            simulated_time += 1
            #print(simulated_time, simulated_released)
        return simulated_released

    '''def estimate_best_case(current_released, current_flow, current_time,
                           target_time, sorted_valves, current_valves):
        remaining_valves = sorted_valves.get_sorted_values_excluding(list(current_valves))
        simulated_time = current_time+1
        simulated_flow = current_flow
        simulated_released = current_released+current_flow
        valves_reached = 0
        while (simulated_time < target_time):
            if valves_reached < len(remaining_valves):
                simulated_flow += remaining_valves[valves_reached]
                #print("added", remaining_valves[valves_reached])
                valves_reached += 1
            simulated_released += simulated_flow
            simulated_time += 1
        return simulated_released'''

        #return current_released+current_flow+(ultimate_flow*(target_time-current_time-1))


    def break_with_dummy_node(new_time, new_flow,
                              new_released, target_time,
                              ultimate_flow,
                              new_open_valves, gates,
                              path1, path2):

        #if (len(queue) == 0 and new_time < max_time) and pair_index == action_pair_len-1:
        #print("something is going wrong")

        priority = -fast_best_case(new_released, new_flow, new_time, target_time, ultimate_flow)
        #queue = deque()
        heappush(queue,
        (priority,
        (
            new_time,
            "%%",
            "%%",
            new_flow,
            new_released,
            new_open_valves,
            gates,
            path1+["%%"],
            path2+["%%"],
            ("%%","%%"),
            [0,0]
        )))


        #print(queue)
        return queue



    # The queue stores the state for each path being explored.
    # State: (time, pos_1, pos_2, current_flow, current_released, open_valves, gates, path1, path2)
    #queue = deque([(0, start_node, start_node, 0, 0, frozenset(), base_gates])
    queue = []
    iteration = 0
    heappush(queue,
             (0,(0, start_node, start_node, 0, 0, frozenset(), [base_gates, base_gates],
                 list(), list(), ("AA","AA"),
                 [0,0])))
    final_state = False
    max_released = 0
    max_flow = 0
    max_state = []
    max_history = []
    max_trajectory = 0
    prune_count = 0
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
        _, (
            current_time,
            current_pos_1,
            current_pos_2,
            current_flow,
            current_released,
            open_valves,
            gates,
            path1,
            path2,
            last_actions,
            jail_times
        ) = heappop(queue)
        iteration += 1
        jailed = [False, False]
        if jail_times[0] > 0:
            jailed[0] = True
        if jail_times[1] > 0:
            jailed[1] = True

        print(jailed, jail_times)
        print(last_actions)
        #decision = True
        #if path[:24] == test_path[:time]:
            #debug = True
            #pass
        if current_time >= max_time:
            if debug:
                pass
                #print(path, current_flow, current_released)
            continue #leaves iteration
        if current_time == last_time+1:
            old_max = max_released
            print("time advanced to: ", current_time)
            print("max flow: ", max_flow)
            print("max released : ", max_released)
            print("length of queue: ", len(queue))
            max_history.append(max_released)
            last_time = current_time
        old_released = current_released
        current_released += current_flow
        if current_released > max_released:
            max_released = current_released
            max_flow = current_flow
            max_state = path1, path2
            max_valves = open_valves

        if final_state: #and time >= max_time:
            queue = break_with_dummy_node(current_time+1, current_flow, current_released,
                                                       new_open_valves, gates, path1, path2)
            print("queue")
            print(queue)
        else:



            #actions_1 = [current_pos_1]+graph[current_pos_1].edges
            #actions_2 = [current_pos_2]+graph[current_pos_2].edges
            valves_1=set()
            valves_2=set()
            #if not jailed[0]:
            if (current_pos_1 + "o" not in open_valves) and (current_pos_1 + "o" in useful_valves):
                valves_1.add(current_pos_1+"o")
            #if not jailed[1]: #not the issue
            if (current_pos_2 + "o" not in open_valves) and (current_pos_2 + "o" in useful_valves):
                valves_2.add(current_pos_2+"o")
            '''print(
                (
                    current_time,
                    current_pos_1,
                    current_pos_2,
                    current_flow,
                    current_released,
                    open_valves,
                    gates,
                    path1,
                    path2,
                    last_actions,
                    jail_times)
            )'''
            if open_valves == useful_valves:
                pass
                '''queue = break_with_dummy_node(current_time + 1, current_flow, current_released, max_time,
                                              ultimate_flow,
                                              open_valves, gates, path1, path2)'''


            else:
                if jailed[0]:
                    actions_1 = set([current_pos_1])
                    #print(actions_1, "jailed for t: ", jail_times[0])
                else:
                    actions_1 = set(set(simple_graph[current_pos_1].edges) #fix graph
                                - set(last_actions[0]).union(set(gates[0]))).union(valves_1)
                if jailed[1]:
                    actions_2 = set([current_pos_2])
                    #print(actions_2, "jailed for t: ", jail_times[1])
                else:
                    actions_2 = set(set(simple_graph[current_pos_2].edges) #fix graph
                                - set(last_actions[1]).union(set(gates[1]))).union(valves_2)

                #actions_1 = [1,2,3]
                #actions_2 = [1,2,3]
                action_pairs = (tuple(combo)
                         for combo in product(actions_1, actions_2))
                #print(jailed)
                action_pairs = tuple(action_pairs)
                if (jailed[0] or jailed[1]):
                    pass
                print(jailed, action_pairs)
                if len(action_pairs) == 1:
                    pass
                    #decision = False
                #print(path1,path2)
                #for action_pair in action_pairs: #todo: gates should only be set for one cursor
                for pair_index in range(len(action_pairs)):
                    action_pair = action_pairs[pair_index]

                    #print(action_pair)
                    reset_gates = False
                    new_time = current_time + 1
                    new_flow = current_flow
                    new_states = list()
                    new_released = current_released
                    new_open_valves = open_valves
                    #print("gates: ", gates, current_time)
                    new_gates = copy.deepcopy(gates)
                    #print(path1+[action_pair[0]], path2+[action_pair[1]])
                    #print(actions_1, actions_2)
                    #print(action_pairs)
                    #print(pair_index)
                    new_jail_times = [0,0]
                    for index in range(len(action_pair)):
                        prune = True
                        action = action_pair[index]
                        if action == "JJo":
                            print(
                                (
                                    current_time,
                                    current_pos_1,
                                    current_pos_2,
                                    current_flow,
                                    current_released,
                                    open_valves,
                                    gates,
                                    path1,
                                    path2,
                                    last_actions,
                                    jail_times))
                        if action[-1] == "o":
                            #print(last_actions, action)
                            if jail_times[index] > 0:
                                pass
                                print("wierd")
                                print(jailed)
                                print(jail_times)
                                print(action_pair)
                                print(path1,path2)
                                continue
                            if not jailed[index]:
                                new_jail_times[index] = 1
                            else:
                                print("wtf")
                                new_jail_times[index] = jail_times[index]
                        else:
                            if not jailed[index]:
                                new_jail_times[index] = simple_graph[last_actions[index]].edge_costs[action]
                            else:
                                print("wtf2", jail_times, path1, path2, action_pair)
                                new_jail_times[index] = jail_times[index]
                        #print(action)
                        if index == 0:
                            current_pos = current_pos_1
                        elif index == 1:
                            current_pos = current_pos_2
                        if action in {"HHo"}:
                            print(path1, path2, action, index, jail_times)
                            #print(action_pairs, "\n")
                            pass
                        if action[-1] == "o":
                            if jail_times[index] > 0:
                                print("something wrong: ", action, jail_times[index])
                            if (
                                simple_graph[action[:-1]].flow > 0 #fix_graph
                                and action not in new_open_valves
                            ):
                                new_open_valves = new_open_valves | {action}
                                new_flow = new_flow + simple_graph[action[:-1]].flow #fix_graph

                                reset_gates = True
                                #print(action[:-1])
                                new_states.append(action[:-1])

                            else:
                                if verbose:
                                    pass
                                    print("prune action ", action, "valves illegal")

                                break
                        else:
                            #print(gates," ",[path1, path2])
                            if action not in gates[index] or reset_gates: #this line seems wierd to me
                                if current_time > 3:
                                    if max_history[current_time-3] < current_released:
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
                        #test = time.perf_counter()
                        best_case = estimate_best_case(new_released, new_flow, new_time, max_time, sorted_valves,
                                                       new_open_valves)
                        '''end = time.perf_counter()
                        elapsed = end - test
                        print(f'Time taken: {elapsed:.6f} seconds')
                        test = time.perf_counter()'''
                        #best_case= fast_best_case(new_released, new_flow, new_time, max_time, ultimate_flow)
                        '''end = time.perf_counter()
                        elapsed = end - test
                        print(f'Time taken: {elapsed:.6f} seconds')'''
                        #print(best_case)
                        if iteration % 10000 == 0:
                            print(new_released, new_flow, new_time, max_time, sorted_valves.get_sorted_values_excluding(""), new_open_valves)
                            print(best_case, max_trajectory)
                            print(iteration)
                        if best_case < max_trajectory:
                            #print("bc is worse than max_trajectory")

                            prune_count+=1
                            pass
                            continue

                        if trajectory > max_trajectory:
                            max_trajectory = trajectory

                        priority = -trajectory
                        if new_jail_times[0] > 0:
                            new_jail_times[0]  -= 1
                        if new_jail_times[1] > 0:
                            new_jail_times[1] -= 1
                        heappush(queue,
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
                            tuple(new_states),
                            list(new_jail_times)
                        )
                        )
                        )
                        #print(queue)
    #print("queue is empty")

    print(prune_count, iteration)
    print(best_case)
    return max_released, max_flow, max_state, max_trajectory, max_valves

print(bfs_with_flow("AA", graph, 5))
print("--- %s seconds ---" % (time.time() - start_time))
#print(bfs_with_flow("AA", graph, 26, verbose=True))

'''a,b,c = (bfs_with_flow("AA", graph, 5),bfs_with_flow("AA", graph, 6),
          bfs_with_flow("AA", graph, 7))

print(a,b,c)'''

'''results = (bfs_with_flow("AA", graph, 5),bfs_with_flow("AA", graph, 6),
          bfs_with_flow("AA", graph, 7), bfs_with_flow("AA", graph, 8),
            bfs_with_flow("AA", graph, 9), bfs_with_flow("AA", graph, 10))

print(results)'''

'''test1 = (136, 35, 6, 14, [22, 21, 20, 13, 3, 2], frozenset({'BBo', 'DDo', 'CCo'}))
valves_dict
sorted_valves = SortedContainersExcluder(valves_dict)

estimate_best_case(136, 35, 6, 14, sorted_valves, frozenset({'BBo', 'DDo', 'CCo'}))'''
#sorted_valves._data
'''#T=6, TARGET= 14
136+35+(35+22)+(35+22+21)+(35+22+21+3)+(35+22+21+3+2)*4
7       8        9              10          11'''