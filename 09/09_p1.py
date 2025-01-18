import numpy as np

grid = np.zeros((6, 6)).astype(int)
headpos = np.array([0, 0])
tailpos = np.array([0, 0])
visited_count = 0
log = []
uniqute_tail_positions = set()

def movetail(headpos, tailpos, visited_count):
    diff = headpos - tailpos
    if np.sum(np.abs(diff)) == 3:
        tailpos[0] += np.sign(diff[0])
        tailpos[1] += np.sign(diff[1])
    elif np.abs(diff[0]) == 2:
        tailpos[0] += np.sign(diff[0])
    elif np.abs(diff[1]) == 2:
        tailpos[1] += np.sign(diff[1])

    return tailpos
def movehead(headpos, direction):
    direction_dict = {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}
    headpos[0] += direction_dict[direction][0]
    headpos[1] += direction_dict[direction][1]
    return headpos

def move(direction, steps):
    global headpos, tailpos, visited_count
    for i in range(steps):
        headpos = movehead(headpos, direction)
        tailpos = movetail(headpos, tailpos, visited_count)
        print(tailpos)
        uniqute_tail_positions.add(tuple(tailpos))
    log.append(tailpos.copy())

input_doc = open("09/input.txt").readlines()
for line in input_doc:
    line = line.split(" ")
    move(line[0], int(line[1]))

print(log)
print(len(uniqute_tail_positions))