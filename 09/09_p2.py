import numpy as np

allpos = [np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0]),
          np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0])]
log = []
unique_tail_positions = set()

def movetail(headpos, tailpos):
    diff = headpos - tailpos
    if np.sum(np.abs(diff)) > 2:
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
    global allpos
    for i in range(steps):
        allpos[0] = movehead(allpos[0], direction)
        for i in range(1, len(allpos)):
            allpos[i] = movetail(allpos[i-1], allpos[i])
        unique_tail_positions.add(tuple(allpos[9]))
    log.append(allpos[9].copy())

input_doc = open("09/input.txt").readlines()
for line in input_doc:
    line = line.split(" ")
    move(line[0], int(line[1]))

#print(log)
print(len(unique_tail_positions))

def draw_unique_tail_positions():
    #draw grid based allpos
    # get highest and lowest x and y
    highest_x = 0
    highest_y = 0
    lowest_x = 0
    lowest_y = 0
    for pos in unique_tail_positions:
        if pos[0] > highest_x:
            highest_x = pos[0]
        if pos[0] < lowest_x:
            lowest_x = pos[0]
        if pos[1] > highest_y:
            highest_y = pos[1]
        if pos[1] < lowest_y:
            lowest_y = pos[1]
    difference_x = np.abs(lowest_x - highest_x)
    difference_y = np.abs(lowest_y - highest_y)
    print(difference_x, difference_y)
    print(lowest_x, highest_x)
    print(lowest_y, highest_y)
    grid = np.zeros((difference_x + 2, difference_y + 2)).astype(int)
    # 0,0 is a position as well, so add 1 to difference
    #calculate offset for 0,0
    center_x = int(np.ceil(difference_x/2))
    center_y = int(np.ceil(difference_y/2))
    for pos in unique_tail_positions:
        #insert adjusted position
        print(pos[0], pos[1])
        print(pos[0]+center_x, pos[1]+center_y)
        grid[pos[0]+center_x][pos[1]+center_y] = 1
    print(np.rot90(grid, 1))

draw_unique_tail_positions()


#306 is too low

#340 is too high
