import numpy as np
queue = []
visited = set()
def get_altitude(x, y):
    #convert the character to an integer
    character = matrix[x][y]
    if character == "S":
        return 0
    elif character == "E":
        return ord("z") - ord("a")
        print("end")
    altitude = ord(character) - ord("a")
    return altitude
with open("12/input.txt") as f:
    #read lines into matrix of characters
    matrix = np.array([list(line.strip()) for line in f.readlines()])
    #get matrix size
    width, height = matrix.shape
    # get the position of the S character
    start = np.argwhere(matrix == "S")[0]
    queue.append((start, 0))

# while the queue is not empty
while queue:
    # get the current cell and its altitude
    current, distance = queue.pop(0)
    #print(current, distance)
    #print(matrix[current[1]][current[0]])
    # if the current cell is the end cell, print the altitude and break
    if matrix[current[0]][current[1]] == "E":
        print(distance)
    else:
        current_altitude = get_altitude(current[0], current[1])
        #print(current_altitude)
    #for each adjacent cell, if it is not more than 1 altitude higher, add it to the queue
    #as long as cells are within the bounds of the matrix (higher than 0 and less than the width/height)
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if 0 <= current[0] + dx < width and 0 <= current[1] + dy < height:
            #print(current[0] + dx, current[1] + dy)
            x, y = current[0] + dx, current[1] + dy
            next_altitude = get_altitude(x, y)
            if next_altitude <= current_altitude+1 and tuple((x,y)) not in visited:
                #print(current_altitude, next_altitude)
                queue.append(((x, y), distance + 1))
                visited.add(tuple((x, y)))
