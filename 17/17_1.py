#there is only one way a pice stops, by being unable to drop further
# todo:
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

def drop_new_piece(chamber, movement_list, tetris_shape, time):
    global global_min_y
    
    def check_colliding_direction(chamber, tuple_of_coords, direction): 
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
            if not isValid(chamber.shape, coordinates):
                return True
        if np.any(chamber[positions_to_check] == True):
            return True
        else:
            return False
        

    def insert_piece(tetris_shape, chamber): #incorrect number of lines when block piece is inserted
        global global_min_y 
        #adds lines to the chamber corresponding to the depth of the selected shape, then gives the coords of the shape
        tuple_of_coords = tetris_shape.tuple_of_coordinates
        depth = tetris_shape.depth
        #chamber_height = chamber.shape[0]
        spaces_above = 3

        lines_to_add = depth+spaces_above - global_min_y
        #print(lines_to_add)
        if lines_to_add > 0:
            chamber = np.concatenate((np.full((lines_to_add,7), False), chamber), axis=0)
            global_min_y = global_min_y + lines_to_add
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
    
    def reduce_chamber(chamber, piece):
        global min_y_list
        pass



    chamber, piece_coords = insert_piece(tetris_shape, chamber)
    #collision_tuple = check_colliding_direction(chamber, piece_coords, time)
    time += 1
    settled_piece, time = advance_time(chamber, time, piece_coords)
    #print(chamber)
    #print(settled_piece)
    global_min_y = min(global_min_y, np.min(settled_piece[0]))

    #print(global_min_y)
    chamber[settled_piece] = True
    return chamber, time


#drop_new_piece(drop_new_piece(base_state, direction_list, i_tetris))

tetris_order = [line_tetris, plus_tetris, j_tetris, i_tetris, block_tetris]

i = -1
chamber = base_state

time = -1

while i < 2021:
    i += 1
    chamber, time = drop_new_piece(chamber, direction_list, tetris_order[i%5], time)

print(chamber.shape[0]-global_min_y-1) #bottom is not rock

#print(chamber.shape)

#print(chamber.shape)


#drop_new_piece(base_state, direction_list, j_tetris)
#drop_new_piece(base_state, direction_list, block_tetris)

test = np.array([[False, False, True],[False, True, False],[True,True,True]])
np.where(test == True)
