from random import random, shuffle
from re import search
from collections import deque
import numpy as np
from numpy.array_api import floor
from numpy.core.multiarray import result_type
from numpy.lib.function_base import insert

with(open("13/input.txt")) as f:
    line_number = 0
    list_full = []
    #lines are mod 3
    #first line contains a list. The list can be nested or empty and contains integers.
    #it should be read into a list
    #second contains the same data, but is read to a seperate list
    #third is skipped
    #repeat
    for line in f.readlines():
        if line_number%3 == 0 or line_number%3 == 1:
            list_full.append(eval(line))
            print(eval(line))
        line_number += 1
    list_full.append([[2]]) # dont need to evaluate this
    list_full.append([[6]])

def evalute_lists(left, right):
    i = 0
    while i < len(left) and i < len(right):
        if type(left[i]) == int and type(right[i]) == int:
            #if left is smaller then return
            if left[i] < right[i]:
                #print(left[i], right[i])
                return 0
            #if right is smaller then return 1
            elif left[i] > right[i]:
                #print(left[i], right[i])
                return 1
        elif type(left[i]) == list and type(right[i]) == list:
            #recursively call the function
            nested_return = evalute_lists(left[i], right[i])
            #if nested return is 1 then return 1
            if nested_return == 1:
                return 1
            #if nested return is 0 then return 0
            elif nested_return == 0:
                return 0
        #if one is a list and the other is an int, convert the int to a list
        elif type(left[i]) == int and type(right[i]) == list:
            #left[i] = [left[i]]
            nested_return = evalute_lists([left[i]], right[i])
            if nested_return == 1:
                return 1
            elif nested_return == 0:
                return 0
        elif type(left[i]) == list and type(right[i]) == int:
            #right[i] = [right[i]]
            nested_return = evalute_lists(left[i], [right[i]])
            if nested_return == 1:
                return 1
            elif nested_return == 0:
                return 0
        i += 1
        #if right is longer then return 0
    if len(left) < len(right):
        return 0
    #if left is longer then return 1
    elif len(left) > len(right):
        return 1

i = 0

sorted_list = []

#shuffle(list_full)
#list_full = backup_list.copy()
#backup_list = list_full.copy()
#list_full = backup_list

sorted_list.append(list_full.pop(0))

def binary_search (item, sorted_list):
    high = len(sorted_list)
    low = 0
    while high > low:
        search_point = (high+low)//2
        print(low, high)
        result = evalute_lists(item, sorted_list[search_point])
        if result == 1:
            low = search_point+1
        else:
            high = search_point
    return low

while list_full:
    item = list_full.pop(0)
    point = binary_search(item, sorted_list)
    sorted_list.insert(point, item)

print(sorted_list)

score = 1
for i in range(len(sorted_list)):
    if sorted_list[i] == [[2]] or sorted_list[i] == [[6]]:
        #print(i)
        score *= i+1
print(score)
