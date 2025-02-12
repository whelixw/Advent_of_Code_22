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
#there is a hack way of solving this
#swap S and E, then replace all a's with E and inverse all the letters.
#the search still starts at S(E) and ends at any E (a or S)
with open("12/input.txt") as f:
    #read lines into matrix
    matrix = np.array([list(line.strip()) for line in f.readlines()])
    #get matrix size
    width, height = matrix.shape
    #get the position of the S character
    start = np.argwhere(matrix == "S")[0]
    #get the position of the E character
    end = np.argwhere(matrix == "E")[0]



    #invert the characters
    matrix = np.vectorize(lambda x: chr(ord("z") - ord(x) + ord("a")))(matrix)
    #swap the S and E characters
    matrix[start[0], start[1]] = "E"
    matrix[end[0], end[1]] = "S"
    #get the position of the S character

    #replace all z's with E
    matrix[matrix == "z"] = "E"
    queue.append((end, 0))

#while the queue is not empty
while queue:
    # get the current cell and its altitude
    current, distance = queue.pop(0)
    #print(current, distance)
    #print(matrix[current[0]][current[1]])
    # if the current cell is the end cell, print the altitude and break
    if matrix[current[0]][current[1]] == "E":
        print(distance)
        break
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