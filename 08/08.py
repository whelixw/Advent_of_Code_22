#IDEAS:
#Scan from both sides along an axis
#Keep heigth threshold on each side during scan
#Mark any positions that are lower than threshold on one axis.
#Scan those on second axis.
## Above has n^4 complexity
#Alternatively, use array slicing.
#Slicing is O(k) where k is the slice size.


#Use two lists for each axis, advance by removing first index and appending to other list.

import numpy as np

input_doc=open("08/input.txt").readlines()
#y=[xi[:-1] for xi in input_doc]
#aa=[[*xi[:-1]] for xi in input_doc]
#a2=[int(x) for x in aa]
matrix_of_trees=np.array([np.array([*xi[:-1]]) for xi in input_doc]).astype(int)
tree_count = 0
for current_x in range(1,len(matrix_of_trees)-1):
    for current_y in range(1,len(matrix_of_trees)-1):
        #direction_lists = [matrix_of_trees[:current_y, current_x], matrix_of_trees[current_y+1:, current_x],matrix_of_trees[current_y, :current_x], matrix_of_trees[current_y, current_x+1:]]
        direction_lists = [matrix_of_trees[:current_x, current_y], matrix_of_trees[current_x + 1:, current_y],
                           matrix_of_trees[current_x, :current_y], matrix_of_trees[current_x, current_y + 1:]]
        for direction in direction_lists:
            if np.all(direction < matrix_of_trees[current_x, current_y]):
                print(str(current_x)+" "+str(current_y))
                print(matrix_of_trees[current_x, current_y])
                tree_count += 1
                break

print(tree_count+len(matrix_of_trees)*4-4)
#print(tree_count)
#current_x = 1
#current_y = 1
#y_lists = [matrix_of_trees[:current_y,current_x], matrix_of_trees[current_y:,current_x]]
#x_lists = [matrix_of_trees[:current_x,current_y], matrix_of_trees[current_x:,current_y]]
#np.any(x_lists[0] <= int(matrix_of_trees[current_x,current_y]))


'''current_x, current_y = 1,3
direction_lists = [matrix_of_trees[:current_y, current_x], matrix_of_trees[current_y+1:, current_x],matrix_of_trees[current_y, :current_x], matrix_of_trees[current_y, current_x+1:]]
direction_lists[1] < matrix_of_trees[current_x, current_y]'''


#2
import numpy as np

input_doc=open("08/input.txt").readlines()
#y=[xi[:-1] for xi in input_doc]
#aa=[[*xi[:-1]] for xi in input_doc]
#a2=[int(x) for x in aa]
matrix_of_trees=np.array([np.array([*xi[:-1]]) for xi in input_doc]).astype(int)
max_scenic_score = 0

for current_x in range(1,len(matrix_of_trees)-1):
    for current_y in range(1,len(matrix_of_trees)-1):
        #direction_lists = [matrix_of_trees[:current_y, current_x], matrix_of_trees[current_y+1:, current_x],matrix_of_trees[current_y, :current_x], matrix_of_trees[current_y, current_x+1:]]
        current_scenic_score = []
        direction_lists = [matrix_of_trees[:current_x, current_y][::-1], matrix_of_trees[current_x + 1:, current_y], #up, down, left, right
                           matrix_of_trees[current_x, :current_y][::-1], matrix_of_trees[current_x, current_y + 1:]]
        #ordered by distance from current position
        #direction_lists = [direction_lists[0][::-1], direction_lists[1][::-1], direction_lists[2][::-1], direction_lists[3][::-1]]
        for direction in direction_lists:
            dir_count = 0
            for tree in direction:
                if tree < matrix_of_trees[current_x, current_y]:
                    dir_count += 1
                else:
                    dir_count += 1
                    break
            current_scenic_score.append(dir_count)

        if np.prod(current_scenic_score) > max_scenic_score:
            max_scenic_score = np.prod(current_scenic_score)
            print(str(current_x)+" "+str(current_y))
            print(matrix_of_trees[current_x, current_y])
            print(current_scenic_score)
            print(max_scenic_score)


