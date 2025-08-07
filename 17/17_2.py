#there is only one way a pice stops, by being unable to drop further
# todo:make a way to outline a perimeter. 
# The cells that make up the perimiter are the only ones needed to be checked for collision and updated
# we need a way to determine if a cell is "live" or not.
# any cell that is fully contained is not live.
# we just need to draw a line along the perimeter of the pieces.
# ideally, we want a smart way to update the perimiter.
# a naive implementation would start at the highest leftmode cell and check up,
#  then up/right, then right, then down/right ... until the perimeter has been established

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

min_y_list = [0, 0, 0, 0, 0, 0, 0]
min_y_across_xs = 0
lines_deleted = 0

def update_min_y_after_piece():
    pass

def adjust_min_y_for_line_insertion(difference):
    global min_y_list
    global min_y_across_xs
    for i in range(len(min_y_list)):
        if min_y_list[i] != -1:
            min_y_list[i] += difference
    min_y_across_xs += difference

def isValid(np_shape: tuple, index: tuple):
    if min(index) < 0:
        return False
    for ind,sh in zip(index,np_shape):
        if ind >= sh:
            return False
    return True

def drop_new_piece(chamber, movement_list, tetris_shape, time):
    global min_y_across_xs
    
    def check_colliding_direction(chamber, tuple_of_coords, direction): 
        #returns True if piece would move out of bounds
        # or collision is imminent in the provided direction
        #print(chamber, tuple_of_coords, direction)
        plane, offset = direction
        #print(plane, offset)
        #print("a")
        if plane == "lateral":
            print(tuple_of_coords)
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
            if not isValid(chamber.shape, coordinates):
                return True
        if np.any(chamber[positions_to_check] == True):
            return True
        else:
            return False
        

    def insert_piece(tetris_shape, chamber): #incorrect number of lines when block piece is inserted
        global min_y_across_xs 
        #adds lines to the chamber corresponding to the depth of the selected shape, then gives the coords of the shape
        tuple_of_coords = tetris_shape.tuple_of_coordinates
        depth = tetris_shape.depth
        #chamber_height = chamber.shape[0]
        spaces_above = 3

        lines_to_add = depth+spaces_above - min_y_across_xs
        #print(lines_to_add)
        if lines_to_add > 0:
            chamber = np.concatenate((np.full((lines_to_add,7), False), chamber), axis=0)
            adjust_min_y_for_line_insertion(lines_to_add)
        elif lines_to_add < 0:
            #print("before", tuple_of_coords)
            tuple_of_coords = (tuple_of_coords[0]-lines_to_add, tuple_of_coords[1]) 
            #print("after", tuple_of_coords)
            #if there are to many lines, we move the piece down instead

        
        return chamber, tuple_of_coords

    def lateral_movement(chamber, movement_list, tuple_of_coords, time):
        #updates the piece coords for lateral movement
        plane = "horizontal"
        
        position = time%(len(movement_list)*2) # cycles movements
        #(time, int(position/2))
        offset = movement_list[int(position/2)] #every other timestep is downwards
        direction = (plane, offset)
        is_colliding = check_colliding_direction(chamber, tuple_of_coords, direction)
        if not is_colliding:
            tuple_of_coords = (tuple_of_coords[0], tuple_of_coords[1]+offset)
        return tuple_of_coords

        

    def downwards_movement(chamber, tuple_of_coords):
        #print(chamber, tuple_of_coords)
        #checks if piece is settled, if not it updates the piece coords for horizontal movement
        plane = "lateral"
        offset = 1
        direction = (plane, offset)
        is_colliding = check_colliding_direction(chamber, tuple_of_coords, direction)
        pass
        if not is_colliding:
            tuple_of_coords = (tuple_of_coords[0]+offset, tuple_of_coords[1])
        return tuple_of_coords, is_colliding


    def advance_time(chamber, time, piece_coords):
        #print("adv", chamber, time, piece_coords)
        if time % 2 == 0:
            #print("lat")
            piece_coords = lateral_movement(chamber, movement_list, piece_coords, time)
        else:
            #print("wha")
            piece_coords, is_settled = downwards_movement(chamber, piece_coords)
            #print("d", piece_coords, is_settled)
            if is_settled:
                return piece_coords, time
                
        time += 1
        piece_coords, time = advance_time(chamber, time, piece_coords)

        #print(piece_coords)
        return piece_coords, time
    
    def reduce_chamber(chamber, piece): #todo: we need a way to update the min ys after deleting
        global min_y_list
        global min_y_across_xs
        global lines_deleted

        tuple_of_pairs = zip(piece[0], piece[1])
        for pair in tuple_of_pairs:
            #print(pair)
            if min_y_list[pair[1]] < pair[0]:
                print("min_index", pair[1], min_y_list)
                min_y_list[pair[1]] = pair[0]
        min_y_across_xs = min(min_y_list)
        if min_y_across_xs > -1:
            delete_cutoff = max(min_y_list)
            lines_to_delete = chamber.shape[0]-delete_cutoff
            if lines_to_delete > 0:
                print("deleting lines:", lines_to_delete, delete_cutoff)
                print(chamber.shape)
                print(min_y_list)
                chamber = chamber[:delete_cutoff,:]
                lines_deleted += lines_to_delete
                for i in range(len(min_y_list)):
                    if min_y_list[i] == delete_cutoff:
                        min_y_list[i] = -1
                print("after:", chamber.shape, lines_deleted)
        return chamber


        
            



    chamber, piece_coords = insert_piece(tetris_shape, chamber)
    #collision_tuple = check_colliding_direction(chamber, piece_coords, time)
    time += 1
    settled_piece, time = advance_time(chamber, time, piece_coords)
    #print(chamber)
    #print(settled_piece)
    #min_y_across_xs = min(min_y_across_xs, np.min(settled_piece[0]))
    chamber[settled_piece] = True
    chamber = reduce_chamber(chamber, piece_coords)
    #print(min_y_across_xs)
    
    return chamber, time


#drop_new_piece(drop_new_piece(base_state, direction_list, i_tetris))

tetris_order = [line_tetris, plus_tetris, j_tetris, i_tetris, block_tetris]

i = -1
chamber = base_state

time = -1

while i < 10000000:
    i += 1
    chamber, time = drop_new_piece(chamber, direction_list, tetris_order[i%5], time)

print(chamber.shape[0]-min_y_across_xs-1) #bottom is not rock
#lines_deleted

#print(chamber.shape)

#print(chamber.shape)


#drop_new_piece(base_state, direction_list, j_tetris)
#drop_new_piece(base_state, direction_list, block_tetris)

'''test = np.array([[False, False, True],[False, True, False],[True,True,True]])
np.where(test == True)
i_tetris.tuple_of_coordinates'''