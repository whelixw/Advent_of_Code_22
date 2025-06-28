

import numpy as np
import re

def calc_manhatten_distance(sensor_coords, beacon_coords):
    return (np.abs(sensor_coords[0]-beacon_coords[0]) + np.abs(sensor_coords[1]-beacon_coords[1]))


def get_dimensions(file):
    points = []
    with(open(file)) as f:
        for line in f:
            #print(type(line))
            wordlist=re.split('[=:,]', line)
            #print(wordlist)
            sx, sy, bx, by = int(wordlist[1]), int(wordlist[3]), int(wordlist[5]), int(wordlist[7])
            dist = calc_manhatten_distance((sx, sy), (bx, by))
            points.append((sx, sy, dist))

    sorted_points = sorted(points, key=lambda tup: tup[0])
    return sorted_points



points=get_dimensions("15/input.txt")

def count_for_y(points, y, xrange): #O(4000000)
    #possible_positions = set([i for i in range (xrange+1)])
    no_beacon = set()
    cursor = 0
    for coords in points: #O(30)

        dist_to_target = calc_manhatten_distance((coords[0], coords[1]), (coords[0], y))
        dist = coords[2]
        if dist_to_target <= dist and cursor >= coords[0]-(dist-dist_to_target):
            cursor = max(coords[0]+(dist-dist_to_target)+1, cursor)
            #print("moving cursor to: ", cursor)
            #print(coords)
            if cursor > xrange:
                #print("AAAAA")
                return

    return cursor
dims = 4000000
for y in range (dims+1):
    if (y%100000 == 0):
        print(y)
    x = count_for_y(points, y, dims)
    #print(type(x))
    if x is not None:
        print(np.int64(x),np.int64(y))
        print((np.multiply(x,4000000, dtype=object)+y))
        break
        #pass