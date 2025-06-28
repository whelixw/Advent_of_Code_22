import numpy as np
import re



def get_dimensions(file):
    max_x = 0
    min_x = 0
    max_y = 0
    min_y=0
    points = []
    with(open(file)) as f:
        for line in f:
            #print(type(line))
            wordlist=re.split('[=:,]', line)
            #print(wordlist)
            sx, sy, bx, by = int(wordlist[1]), int(wordlist[3]), int(wordlist[5]), int(wordlist[7])
            points.append((sx, sy, bx, by))
            if sx > max_x:
                max_x = sx
            if bx > max_x:
                max_x = bx
            if by > max_y:
                max_y = by
            if sy > max_y:
                max_y = sy
            if sx < min_x:
                min_x = sx
            if bx < min_x:
                min_x = bx
            if by < min_y:
                min_y = by
            if sy < min_y:
                min_y = sy
    return max_x, max_y, min_x, min_y, points

def calc_manhatten_distance(sensor_coords, beacon_coords):
    return (np.abs(sensor_coords[0]-beacon_coords[0]) + np.abs(sensor_coords[1]-beacon_coords[1]))

max_x, max_y, min_x, min_y, points=get_dimensions("15/input.txt")

def count_for_y(points, y):
    no_beacon = set()
    is_beacon = set()
    for coords in points:
        dist = calc_manhatten_distance((coords[0],coords[1]),(coords[2],coords[3]))
        dist_to_target = calc_manhatten_distance((coords[0], coords[1]), (coords[0], y))
        if coords[3] == y:
            is_beacon.add(coords[2])
        if dist_to_target <= dist:
            for i in range(coords[0]-(dist-dist_to_target), coords[0]+(dist-dist_to_target)+1):#this feels inefficient
                no_beacon.add(i)#this feels inefficient
            #counter += 2*(dist-dist_to_target)+1
    no_beacon = no_beacon.difference(is_beacon)
    #print(no_beacon)
    counter = len(no_beacon)
    return counter
count_for_y(points, 2000000)