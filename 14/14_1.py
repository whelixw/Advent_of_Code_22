import numpy as np
from numpy.matrixlib.defmatrix import matrix


def draw_line (x1, y1, x2, y2):
    global matrix
    # Draw a line between two points (x1, y1) and (x2, y2)
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            #print(x1, y)
            matrix[x1][y] = True
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            #print(x,y1)
            matrix[x][y1] = True
    else:
        # Diagonal lines are not handled in this example
        pass

def get_dimensions(file):
    max_x = 500
    max_y = 0
    with(open(file)) as f:
        for line in f:
            words = line.split(sep=" -> ")
            for i in range(len(words)):
                words[i] = words[i].split(sep=",")
                if int(words[i][0]) > max_x:
                    max_x = int(words[i][0])
                if int(words[i][1]) > max_y:
                    max_y = int(words[i][0])
        return max_x,max_y

def falling_sand(dimensions):
    new_matrix = np.copy(matrix)
    pos = 500,0
    moving = True
    #print(pos)
    #single iteration
    def check_directions(dimensions):
        dir_map = {
            "down": (pos[0],pos[1]+1),
            "down_left": (pos[0]-1,pos[1]+1),
            "down_right": (pos[0]+1,pos[1]+1)}
        #print(dimensions)
        #print(dir_map)
        for key in dir_map:
            if dir_map[key][0] > dimensions[0] or dir_map[key][1] > dimensions[1]:
                return True
            else:
                #print (dir_map[key])
                if not matrix[dir_map[key]]:
                    return dir_map[key]
        print("no")
        return False

    while moving:
        new_pos = check_directions(dimensions)
        if type(new_pos) == tuple:
            pos = new_pos
        else:
            moving = False
            if new_pos == True:
                break
            else:
                new_matrix[pos[0],pos[1]] = True
                print("inserted sand in pos: " +str(pos))


    return new_matrix



file = "14/input.txt"
dimensions = get_dimensions(file)
matrix=np.full((dimensions[0]+1, dimensions[1]+1), False)


with open(file) as f:
    for line in f:
        words = line.split(sep=" -> ")
        for i in range(len(words)):
            if i == 0:
                pass
            else:
                pos1 = words[i-1].split(sep=",")
                pos2 = words[i].split(sep=",")
                draw_line(int(pos1[0]),int(pos1[1]),int(pos2[0]),int(pos2[1]))

itertation = 0
testmatrix = matrix[494:505,:10]
testmatrix.shape

new_matrix = falling_sand(dimensions)
itertation += 1
print(itertation)
matrix = new_matrix

testmatrix = matrix[494:505,:10].transpose()
print(testmatrix)
matrix_backup =testmatrix

new_matrix = falling_sand(dimensions)
itertation = 1
while not np.array_equal(new_matrix, matrix):
    matrix = new_matrix
    new_matrix = falling_sand(dimensions)
    itertation += 1
    if itertation%100 == 0:
        print(itertation)

print(itertation)