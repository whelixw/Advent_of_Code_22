#there is only one way a pice stops, by being unable to drop further
# todo: update main function to work with a perimiter instead of a matrix
# test perimeter function. check_node work

import numpy as np 

file = "17/test.txt"

direction_dict = {"<": -1,
                  ">": 1}
direction_list = []

with(open(file)) as f:
    for line in f:
        for char in line:
            offset = direction_dict.get(char)
            if offset is not None:
                direction_list.append(offset)




class Shape:
    def __init__(self, tuple_of_coordinates):
        self.depth = max(tuple_of_coordinates[0]+1)
        self.width = max(tuple_of_coordinates[1]+1)
        self.tuple_of_coordinates = (tuple_of_coordinates[0], tuple_of_coordinates[1]+2)

line_tetris = Shape(np.where(np.array([True,True,True,True], ndmin=2) == True))
plus_tetris = Shape(np.where(np.array([[False, True, False],
                 [True, True, True],
                 [False, True, False]]) == True ))
j_tetris =  Shape(np.where(np.array([[False, False, True],
                     [False, False, True],
                     [True, True, True]]) == True))
i_tetris =  Shape(np.where(np.full((4,1), True) == True))
block_tetris =  Shape(np.where(np.full((2,2), True) == True))

x_instert_level = 3

#base_state = np.array([np.full((7), False), np.full((7), False), np.full((7), False), np.full((7), True)])
base_state = np.full((1,7), True)

#base_state = np.concatenate((np.full((1,7), False),base_state), axis=0)
global_min_y = 0
min_y_list = [0, 0, 0, 0, 0, 0, 0]




def isValid(np_shape: tuple, index: tuple):
    if min(index) < 0:
        return False
    for ind,sh in zip(index,np_shape):
        if ind >= sh:
            return False
    return True


def trace_perimeter(last_perimiter, placed_coords):
    #update the traced perimiter from the ealiest node in path that can reach the new piece
    # when the new path converges to the old one, the perimiter can be updated.
    start_index = False
    end_index = 0
    def check_node(node, coordinate_pairs):
        #checks if node can path to new piece
        x,y = node
        print(node, list(coordinate_pairs))
        for pair in coordinate_pairs:
            ydiff = np.abs((y-pair[0]))
            xdiff = np.abs((x-pair[1]))

            if xdiff <= 1 and ydiff <= 1:
                #print("safe")
                return True


            '''if (x-1 <= pair[0] >= x+1 and
            y-1 <= pair[1] >= y+1):'''
    def path_search(pos, dir_priority, search_positions, path):
        #terminates when last position that can reach piece is selected
        for direction in dir_priority: #goes through the direction in order
            pos = list(pos)
            #print(new_pos)
            for pair_index in range(len(direction)):
                print("modifying", pos, direction[pair_index])
                pos[pair_index] += direction[pair_index] 
                #moves cursor from selected pos in direction
                print(pos)
            if tuple(pos) in search_positions:
                #if piece is contained in that position, add to path and select position
                path.append(tuple(pos))
                print("appending")
                return(pos, path)
    
    def build_path(dir_priority, last_perimiter, coordinate_pairs, start_index, end_index ):
        #selects the first position that can reach the new piece
        #needs to check for not only placed piece but also end cell
        #potentially even more
        # the while works for the smallest test case now
        end_cell = last_perimiter[end_index]
        path = []
        search_positions = set(coordinate_pairs).union(set(tuple([end_cell])))
        # too many paths are added
        selected_pos = last_perimiter[start_index]
        while tuple(selected_pos) != end_cell: 
            #should i use while?
            print("outer")
            selected_pos, path = path_search(selected_pos, dir_priority, search_positions, path)

            '''#terminates when last position that can reach piece is selected
            for direction in dir_priority: #goes through the direction in order
                new_pos = list(selected_pos)
                print(new_pos)
                for pair_index in range(len(direction)):
                    print("modifying", new_pos, direction[pair_index])
                    new_pos[pair_index] += direction[pair_index] 
                    #moves cursor from selected pos in direction
                    print(new_pos)
                if tuple(new_pos) in search_positions:
                    #if piece is contained in that position, add to path and select position
                    path.append(new_pos)
                    print("appending")
                    selected_pos = new_pos'''
                    #
        print(last_perimiter[:start_index]+path+last_perimiter[end_index+1:])
        return last_perimiter[:start_index]+path+last_perimiter[end_index+1:]
    


        
    
    dir_priority = ((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1))
    #up, up/right, right, down/right, down, down/left, left, up/left
    # down is (+1,0)
    int_coords = ((int(c) for c in placed_coords[0]), (int(c) for c in placed_coords[1] ))
    coordinate_pairs = tuple(zip(int_coords[0],int_coords[1]))
    
    for index in range(len(last_perimiter)):
        if check_node(last_perimiter[index], coordinate_pairs):
            if start_index is False:
                start_index = index
            if index > end_index and index < 7:
                end_index = index
    new_perimeter = build_path(dir_priority, last_perimiter, 
               coordinate_pairs, start_index, end_index)
    
    return new_perimeter
    
last_perimeter = [(1,0),(1,1)]
trace_perimeter(last_perimeter, (np.array([0]), np.array([0])))   
pass


def drop_new_piece(perimeter, movement_list, tetris_shape, time):
    #should take perimeter, and return new perimeter
    global global_min_y
    
    def check_colliding_direction(perimeter, tuple_of_coords, direction):
        # should work 
        #ex. tuple of coords  = (np.array([236, 236, 236, 236]), np.array([2, 3, 4, 5]))
        #returns True if piece would move out of bounds
        # or collision is imminent in the provided direction
        #print(chamber, tuple_of_coords, direction)
        plane, offset = direction
        #print(plane, offset)
        #print("a")
        if plane == "lateral":
            #print(tuple_of_coords)
            #print("AAA")
            #print(offset)
            positions_to_check = (tuple_of_coords[0]+offset, tuple_of_coords[1])
        else:
            positions_to_check = (tuple_of_coords[0], tuple_of_coords[1]+offset)
        #rint(positions_to_check)
        #coordnate_pairs = np.argwhere(positions_to_check).tolist()
        coordinate_pairs = zip(positions_to_check[0],positions_to_check[1])
        #print(coordinate_pairs)
        for coordinates in coordinate_pairs:
            #print(coordinates)
            '''if not isValid(shape, coordinates): #there will be no chamber matrix
                return True'''
            if not 0 > coordinates[1] > 8:
                return True
            if (int(coordinates[0]), int(coordinates[1])) in set(perimeter):
                #there is probably a more efficient way, maybe just store as in64?
                return True
            return False
    
    

    def insert_piece(tetris_shape): #incorrect number of lines when block piece is inserted
        #wip
        global global_min_y 
        #adds lines to the chamber corresponding to the depth of the selected shape, then gives the coords of the shape
        tuple_of_coords = tetris_shape.tuple_of_coordinates
        depth = tetris_shape.depth
        #chamber_height = shape[0]
        spaces_above = 3

        lines_to_add = depth+spaces_above - global_min_y
        #print(lines_to_add)
        if lines_to_add > 0:
            #instead of adding lines insertion index should be updated.
            # alternatively, all y indices in the perimiter could be updated
            # but it is more costly
            #chamber = np.concatenate((np.full((lines_to_add,7), False), chamber), axis=0)
            global_min_y = global_min_y + lines_to_add
        

        #elif lines_to_add < 0:
            #print("before", tuple_of_coords)
        
        tuple_of_coords = (tuple_of_coords[0]-lines_to_add, tuple_of_coords[1]) 
        #print("after", tuple_of_coords)
        #if there are to many lines, we move the piece down instead


        return tuple_of_coords

    def lateral_movement(perimeter, movement_list, tuple_of_coords, time):
        #updates the piece coords for lateral movement
        plane = "horizontal"
        
        position = time%(len(movement_list)*2) # cycles movements
        #(time, int(position/2))
        offset = movement_list[int(position/2)] #every other timestep is downwards
        direction = (plane, offset)
        is_colliding = check_colliding_direction(perimeter, tuple_of_coords, direction)
        if not is_colliding:
            tuple_of_coords = (tuple_of_coords[0], tuple_of_coords[1]+offset)
        return tuple_of_coords

        

    def downwards_movement(perimeter, tuple_of_coords):
        #print(chamber, tuple_of_coords)
        #checks if piece is settled, if not it updates the piece coords for horizontal movement
        plane = "lateral"
        offset = 1
        direction = (plane, offset)
        is_colliding = check_colliding_direction(perimeter, tuple_of_coords, direction)
        pass
        if not is_colliding:
            tuple_of_coords = (tuple_of_coords[0]+offset, tuple_of_coords[1])
        return tuple_of_coords, is_colliding


    def advance_time(perimeter, time, piece_coords):
        #print("adv", chamber, time, piece_coords)
        if time % 2 == 0:
            #print("lat")
            piece_coords = lateral_movement(perimeter, movement_list, piece_coords, time)
        else:
            #print("wha")
            piece_coords, is_settled = downwards_movement(perimeter, piece_coords)
            #print("d", piece_coords, is_settled)
            if is_settled: # update perimeter, min_y could be updated?
                return piece_coords, time
                
        time += 1
        piece_coords, time = advance_time(perimeter, time, piece_coords)

        #print(piece_coords)
        return piece_coords, time
    
    def reduce_chamber(chamber, piece):
        global min_y_list
        pass



    piece_coords = insert_piece(tetris_shape)
    #collision_tuple = check_colliding_direction(chamber, piece_coords, time)
    time += 1
    settled_piece, time = advance_time(perimeter, time, piece_coords)
    #print(chamber)
    #print(settled_piece)
    global_min_y = min(global_min_y, np.min(settled_piece[0]))

    #print(global_min_y)
    #chamber[settled_piece] = True
    perimeter = trace_perimeter(perimeter, settled_piece)
    return perimeter, time 


#drop_new_piece(drop_new_piece(base_state, direction_list, i_tetris))

tetris_order = [line_tetris, plus_tetris, j_tetris, i_tetris, block_tetris]

perimeter = [(0,i) for i in range(7)]

i = -1
chamber = base_state

time = -1

while i < 2021:
    i += 1
    chamber, time = drop_new_piece(perimeter, direction_list, tetris_order[i%5], time)

print(shape[0]-global_min_y-1) #bottom is not rock

#print(shape)

#print(shape)


#drop_new_piece(base_state, direction_list, j_tetris)
#drop_new_piece(base_state, direction_list, block_tetris)

test = np.array([[False, False, True],[False, True, False],[True,True,True]])
np.where(test == True)
