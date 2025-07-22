#((105, 44, (['DD', 'DD', 'EE', 'EE'], ['II', 'JJ', 'JJ', 'II'])), (156, 54, (['DD', 'DD', 'AA', 'BB', 'BB'], ['II', 'JJ', 'JJ', 'II', 'AA'])), (210, 54, (['DD', 'DD', 'AA', 'BB', 'BB', 'AA'], ['II', 'JJ', 'JJ', 'II', 'AA', 'DD'])), (266, 56, (['DD', 'DD', 'AA', 'BB', 'BB', 'CC', 'CC'], ['II', 'JJ', 'JJ', 'II', 'AA', 'DD', 'AA'])), (338, 76, (['DD', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG'], ['BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA'])), (414, 76, (['DD', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'HH'], ['BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA', 'DD'])))
#1540 is too low
#todo: figure out what is going on. Jailed has weird interactions with the rest, especially opening valves
from collections import deque
from heapq import heappush, heappop
from itertools import product, combinations
import copy
import time
from symbol import return_stmt

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

def bfs_with_flow(start_node, simple_graph, max_time, verbose = False):

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
    #most of these things can be redone. There is no reason to ever visit a node without opening it.
    #also if a node has been visited (and opened) before, it cannot be returned to
    def move_cursors(queue, state, max_time, max_released):
        #print("move_cursors")
        #print(queue, state, max_time, max_released)
        (current_time, last_actions, current_flow, current_released,
        open_valves, jail_times) = state
        actions = last_actions
        def advance_time(current_time, current_flow, current_released, jail_times, time_to_advance, max_released): #calculates released and reduces jail time
            #this could do all time advancements
            #print("advance_time")
            #print(current_time, current_flow, current_released, jail_times, time_to_advance, max_released)
            def update_best_state(current_released, max_released):
                #print( current_released, max_released)
                if current_released > max_released:
                    max_released = current_released
                return max_released


            current_released = current_released+(current_flow*time_to_advance)
            max_released = update_best_state(current_released, max_released)
            new_time = current_time + time_to_advance
            for time in jail_times:
                time -= time_to_advance
            #print("before_return")
            #print(current_released, jail_times, max_released, new_time)
            return current_released, jail_times, max_released, new_time

        def move_single_cursor(index, open_valves, current_pos): #calculates actions for one cursor
            if (current_pos + "o" not in open_valves):
                valves = set()
                valves.add(current_pos+"o")
                actions = set(set(simple_graph[current_pos].edges) #fix graph
                                - set(last_actions[index]).union(valves))
                if actions == set():
                    actions = set("%%")
                return actions

        def action_queuer(queue, action_pair, current_flow, open_valves, jail_times, max_time, max_released):# queues actions from action_pairs
            #print("action_queuer")
            #print(queue, action_pair, current_flow, open_valves, jail_times, max_time, max_released)
            def prune_actions():
                pass

            def open_valve(current_flow, open_valves):
                new_open_valves = open_valves.difference({action})
                new_flow = current_flow + simple_graph[action[:-1]].flow
                jail_time = -1
                new_pos = action[:-1]
                return new_pos, new_flow, new_open_valves, jail_time
            def move_to_position(last_action):
                jail_time = simple_graph[last_action].edge_costs[action]
                new_pos = action
                return new_pos, jail_time
            def dummy_action(current_time, jail_time, max_time):
                new_pos = action
                jail_time = max_time - current_time
                return new_pos, jail_time
            for index in range(len(action_pair)):
                action = action_pair[index]
                jail_time = jail_times[index]
                last_action = last_actions[index]
                if jail_time == 0:
                    if action[-1] == "o":
                        (action, new_flow, new_open_valves,
                         jail_time) = open_valve(flow_rate, open_valves)
                        open_valves = new_open_valves
                        current_flow = new_flow
                    elif action == "%%":
                        action = dummy_action(jail_time, max_time)
                    else:
                        action, jail_time = move_to_position(last_action)
            min_jail_time = min(jail_times)
            #print(current_time, current_flow, jail_times, min_jail_time, max_released)
            new_released, jail_times, max_released, new_time = advance_time(current_time, current_flow, current_released, jail_times,
                                                                            min_jail_time, max_released)
            #print("after", max_released)
            if min(jail_times) < max_time:
                priority = 1
                heappush(queue,
                         (priority,
                         (new_time, action_pair, current_flow, new_released,
                          open_valves, jail_times)))
            return queue, max_released

        print(state)

        print(actions)

        if jail_times[0] != jail_times[1]:
            index_min = min(range(len(jail_times)), key=jail_times.__getitem__)
            new_action = move_single_cursor(index_min)
            actions[index_min] = new_action
        else:
            actions = (move_single_cursor(0, open_valves, last_actions[0],),
                      move_single_cursor(1, open_valves, last_actions[1]))
            #print(actions)
        action_pairs = (tuple(combo)
                        for combo in product(actions[0], actions[1]))
        action_pairs = tuple(action_pairs)
        #print(action_pairs)
        #print(tuple(action_pairs))
        if len(tuple(action_pairs)) == 1:
            decision = False
        for action_pair in action_pairs:
            #print(action_pair)
            if action_pair[0] != action_pairs[1]:
                #print("max_released")
                #print(max_released)
                queue, max_released = action_queuer(queue, action_pair, current_flow, open_valves, jail_times, max_time, max_released)
        return queue, max_released

    max_released = 0
    queue = []
    heappush(queue,
             (0,
              (0, (start_node, start_node), 0, 0, frozenset(), [1, 1])))
    priority, state = heappop(queue)
    #print("huh")
    #print(queue, state, max_time, max_released)
    queue, max_released = move_cursors(queue, state, max_time, max_released)
    return queue

print(bfs_with_flow("AA", simple_graph, 5))
