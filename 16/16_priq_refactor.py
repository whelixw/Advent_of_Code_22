#((105, 44, (['DD', 'DD', 'EE', 'EE'], ['II', 'JJ', 'JJ', 'II'])), (156, 54, (['DD', 'DD', 'AA', 'BB', 'BB'], ['II', 'JJ', 'JJ', 'II', 'AA'])), (210, 54, (['DD', 'DD', 'AA', 'BB', 'BB', 'AA'], ['II', 'JJ', 'JJ', 'II', 'AA', 'DD'])), (266, 56, (['DD', 'DD', 'AA', 'BB', 'BB', 'CC', 'CC'], ['II', 'JJ', 'JJ', 'II', 'AA', 'DD', 'AA'])), (338, 76, (['DD', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG'], ['BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA'])), (414, 76, (['DD', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'HH'], ['BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA', 'DD'])))
#1540 is too low
#todo: right now the queue keeps expanding. I need a way to fix that
# Aditionally, flow increase is improperly implemented. Flow should increase when jailed time moves to zero from more
# there is a problem with missing actions when pruning through move_single_cursor
from collections import deque
from heapq import heappush, heappop
from itertools import product, combinations
import copy
import time
from symbol import return_stmt, break_stmt

start_time = time.time()

#import numpy as np
#import heapq
file = "16/test.txt"
all_paths = []
best_states = []


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
            if key != own_name:
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

valve_set = set(valve_names)

base_gates=frozenset()

def bfs_with_flow(start_node, simple_graph, max_time, verbose = False):

    #most of these things can be redone. There is no reason to ever visit a node without opening it.
    #also if a node has been visited (and opened) before, it cannot be returned to
    def move_cursors(queue, state, max_time, max_released):
        #print("move_cursors")
        #print(queue, state, max_time, max_released)
        (current_time, actions, current_flow, current_released,
        open_valves, jail_times, valve_set, path1, path2) = state
        #print("tste", state)
        def heapq_action(queue, new_time, action_pair, current_flow, new_released, open_valves, jail_times, new_valve_set, path1, path2, priority = 1):
            #print(path1+[action_pair[0]])
            #print(path2+[action_pair[1]])
            heappush(queue,
                     (priority,
                      (new_time, action_pair, current_flow, new_released,
                       open_valves, jail_times, new_valve_set, path1+[action_pair[0]],path2+[action_pair[1]])))
            return queue

        def advance_time(current_time, current_flow, current_released, jail_times, time_to_advance, max_released,
                         max_time,  path1, path2, action_pair): #calculates released and reduces jail time
            #this could do all time advancements
            #print("advance_time")
            total_time =  current_time + time_to_advance
            if total_time > max_time:
                time_to_advance -= total_time-max_time
            #print(current_time, current_flow, current_released, jail_times, time_to_advance, max_released)
            def update_best_state(current_released, max_released, path1, path2, action_pair):
                #print("rel,", current_released, max_released)
                if current_released > max_released:
                    max_released = current_released
                    print("new_max_released:", max_released)
                    best_states.append(tuple([path1, path2, action_pair, valve_set]))
                    #print(path1, path2, action_pair, valve_set)
                return max_released


            current_released = current_released+(current_flow*time_to_advance)
            max_released = update_best_state(current_released, max_released, path1, path2, action_pair)
            new_time = current_time + time_to_advance
            #print(time_to_advance, jail_times)
            for i in range(len(jail_times)):
                jail_times[i] -= time_to_advance
            #print("new_jails", jail_times)
            #print("before_return")
            #print(current_released, jail_times, max_released, new_time)
            return current_released, jail_times, max_released, new_time

        def move_single_cursor(index, current_time, current_pos, valve_set, max_time): #calculates actions for one cursor
            #print(index, valve_set, current_pos)
            valves = set()
            '''if current_pos[-1] == "o":
                current_pos = current_pos[:-1]
            else:
                valves.add(current_pos+"o")'''
            #print(valve_set, current_pos)
            if current_time < max_time:
                actions = valve_set - set([current_pos]) #fix graph

            #print("odde;",current_pos, actions)
            actions_to_remove = set()
            for action in actions: #prune_actions
                if simple_graph[current_pos].edge_costs[action] + current_time > max_time:
                    print("no", action, current_time, simple_graph[current_pos].edge_costs[action], max_time)
                    actions_to_remove.add(action)
            actions = actions - actions_to_remove
            if actions == set():
                actions = set(["%%"])
            print(actions)
            return actions

        def action_queuer(queue, current_time, action_pair, current_flow, current_released, open_valves, jail_times, max_time, max_released, valve_set):# queues actions from action_pairs
            #print("action_queuer")
            #print(action_pair, current_flow, open_valves, jail_times, max_time, max_released)
            new_valve_set = valve_set
            new_jail_times = jail_times.copy()
            #current_released = current_released.copy() #are they needed
            #current_flow = current_flow.copy()
            def prune_actions():
                pass

            def open_valve(current_action, current_flow, current_released, jail_time, valve_set): #todo: add negative offset to current
                # released. serves to delay the flow
                print("open_valve")
                print(current_time, current_action, valve_set)
                new_valve_set = valve_set.difference(set([current_action]))
                #jail_time += 1
                if current_time + jail_time < max_time:

                    new_flow = current_flow + simple_graph[current_action].flow #increase flow
                    new_released = current_released - (simple_graph[current_action].flow*jail_time) #add offset
                    print("enough time:", current_time + jail_time, max_time, new_flow, new_released)
                else:
                    new_flow = current_flow
                    new_released = current_released
                #new_pos = action[:-1]
                #print(jail_time, new_valve_set, new_flow, new_released)
                return jail_time, new_valve_set, new_flow, new_released
            def move_to_position(last_action, current_action, current_flow, current_released, valve_set): #todo:tries to move to same position as it started
                #print("move_to_pos")
                #print(last_action,current_action)
                jail_time = simple_graph[last_action].edge_costs[current_action]
                #print("jt", jail_time)
                #print(valve_set)
                jail_time, new_valve_set, new_flow, new_released =  open_valve(current_action, current_flow, current_released, jail_time, valve_set)
                #print(new_valve_set)

                #new_pos = action
                return jail_time, new_valve_set, new_flow, new_released
            def dummy_action(current_time, max_time):
                print("dummy_action")
                #new_pos = action
                jail_time = max_time - current_time
                return jail_time

            #doe advance time belong here?

            for index in range(len(action_pair)):
                '''action = action_pair[index]
                jail_time = jail_times[index]
                print(jail_times)
                last_action = last_actions[index]'''
                if jail_times[index] == 0:
                    '''if action_pair[index][-1] == "o":
                        print("aaa")
                        (new_flow, new_open_valves,
                         jail_times[index]) = open_valve(flow_rate, open_valves)
                        open_valves = new_open_valves
                        current_flow = new_flow'''
                    if action_pair[index] == "%%":
                        new_jail_times[index] = dummy_action(jail_times[index], max_time)
                    elif action_pair[index] == actions[index]: #jailed
                        pass
                    else:
                        #print(actions[index], action_pair[index], current_flow, current_released, valve_set)
                        new_jail_times[index], new_valve_set, current_flow, current_released = move_to_position(actions[index], action_pair[index], current_flow, current_released, valve_set)
                        #print("j",jail_times[index])
                        #print(new_valve_set)
                #print(jail_times)

            min_jail_time = min(new_jail_times)
            if min_jail_time == 0:
                print("this should not happen. ")

                print(actions, action_pair,current_time, current_flow, current_released, jail_times, min_jail_time, max_released)

            #print("ctime:", current_time)
            #print(current_time, current_flow, jail_times, min_jail_time, max_released)


            current_released, new_jail_times, max_released, new_time = advance_time(current_time, current_flow,
                                                                            current_released, new_jail_times,
                                                                            min_jail_time, max_released, max_time,
                                                                            path1, path2, action_pair)

            #print("ntime", new_time)
            #print("after", max_released)
            '''if (min(jail_times) + new_time) < max_time: # don't know if this should be min_time + new_new_time
                priority = 1
                heappush(queue,
                         (priority,
                         (new_time, action_pair, current_flow, new_released,
                          open_valves, jail_times, new_valve_set)))'''
            if new_time < max_time:
                queue = heapq_action(queue, new_time, action_pair, current_flow, current_released,
                          open_valves, new_jail_times, new_valve_set, path1, path2)
            else:
                print(path1+[action_pair[0]])
                print(path2+[action_pair[1]])
                all_paths.append((path1+[action_pair[0]],path2+[action_pair[1]]))
            return queue, max_released

        #print(state)
        print(len(queue))
        #print(actions)

        if jail_times[0] != jail_times[1]:
            index_min = min(range(len(jail_times)), key=jail_times.__getitem__)
            print("single_c,", index_min, actions[index_min], valve_set)
            new_action = move_single_cursor(index_min, current_time, actions[index_min], valve_set, max_time)
            actions_list = list(actions)
            #print("zz", new_action)
            actions_list[index_min] = new_action
            other_index= 1-index_min
            print(actions_list[other_index])
            actions_list[other_index] = [actions_list[other_index]]
            #print("aaaa",actions_list)
            new_actions = tuple(actions_list)
            #print(new_actions)
        else:
            new_actions = (move_single_cursor(0, current_time, actions[0], valve_set, max_time),
                      move_single_cursor(1, current_time, actions[1], valve_set, max_time))
            #print(actions)
        action_pairs = (tuple(combo)
                        for combo in product(new_actions[0], new_actions[1]))
        action_pairs = tuple(action_pairs)
        print(actions, action_pairs)
        #print(tuple(action_pairs))
        if len(tuple(action_pairs)) == 1:
            decision = False
        for action_pair in action_pairs:
            if ((action_pair[0] != action_pair[1] or
                (action_pair[0] == "%%" and action_pair[1] == "%%"))
                    and current_time < max_time):
                #print("max_released")
                #print(max_released)
                #print(action_pair)


                queue, max_released = action_queuer(queue, current_time, action_pair,
                                                    current_flow, current_released, open_valves,
                                                    jail_times, max_time, max_released, valve_set)
        return queue, max_released

    max_released = 0
    queue = []
    heappush(queue,
             (0,
              (0, (start_node, start_node), 0, 0, frozenset(), [1, 1], valve_set, [start_node], [start_node])))
    while queue:
        priority, state = heappop(queue)
        #print("huh")
        #print(queue, state, max_time, max_released)
        #print(len(queue))
        queue, max_released = move_cursors(queue, state, max_time, max_released)
    return max_released

print(bfs_with_flow("AA", simple_graph, 3))
print(all_paths)
print(best_states[-1])
