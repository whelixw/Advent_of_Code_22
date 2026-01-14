# there is only one way a pice stops, by being unable to drop further
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
        self.depth = max(tuple_of_coordinates[0] + 1)
        self.width = max(tuple_of_coordinates[1] + 1)
        self.tuple_of_coordinates = (tuple_of_coordinates[0], tuple_of_coordinates[1] + 2)


line_tetris = Shape(np.where(np.array([True, True, True, True], ndmin=2) == True))
plus_tetris = Shape(np.where(np.array([[False, True, False],
                                       [True, True, True],
                                       [False, True, False]]) == True))
j_tetris = Shape(np.where(np.array([[False, False, True],
                                    [False, False, True],
                                    [True, True, True]]) == True))
i_tetris = Shape(np.where(np.full((4, 1), True) == True))
block_tetris = Shape(np.where(np.full((2, 2), True) == True))

x_instert_level = 3

# base_state = np.array([np.full((7), False), np.full((7), False), np.full((7), False), np.full((7), True)])
base_state = np.full((1, 7), True)
base_path = [(0, x) for x in range(7)]

# base_state = np.concatenate((np.full((1,7), False),base_state), axis=0)
global_min_y = 0
min_y_list = [0, 0, 0, 0, 0, 0, 0]


def isValid(np_shape: tuple, index: tuple):
    if min(index) < 0:
        return False
    for ind, sh in zip(index, np_shape):
        if ind >= sh:
            return False
    return True


def drop_new_piece(chamber, path, movement_list, tetris_shape, time, offset):
    global global_min_y
    def check_colliding_direction(chamber, tuple_of_coords, direction):
        # returns True if piece would move out of bounds
        # or collision is imminent in the provided direction
        # print(chamber, tuple_of_coords, direction)
        plane, offset = direction
        # print(plane, offset)
        # print("a")
        if plane == "lateral":
            # print(tuple_of_coords)
            # print("AAA")
            # print(offset)
            positions_to_check = (tuple_of_coords[0] + offset, tuple_of_coords[1])
        else:
            positions_to_check = (tuple_of_coords[0], tuple_of_coords[1] + offset)
        # rint(positions_to_check)
        # coordnate_pairs = np.argwhere(positions_to_check).tolist()
        coordinate_pairs = zip(positions_to_check[0], positions_to_check[1])
        # print(coordinate_pairs)
        for coordinates in coordinate_pairs:
            # print(coordinates)
            if not isValid(chamber.shape, coordinates):
                return True
        if np.any(chamber[positions_to_check] == True):
            return True
        else:
            return False

    def insert_piece(tetris_shape, path, chamber):  # incorrect number of lines when block piece is inserted
        global global_min_y
        # adds lines to the chamber corresponding to the depth of the selected shape, then gives the coords of the shape
        tuple_of_coords = tetris_shape.tuple_of_coordinates
        depth = tetris_shape.depth
        # chamber_height = chamber.shape[0]
        spaces_above = 3

        lines_to_add = depth + spaces_above - global_min_y
        path = [(r+lines_to_add,c) for (r,c) in path]
        # print(lines_to_add)
        if lines_to_add > 0:
            chamber = np.concatenate((np.full((lines_to_add, 7), False), chamber), axis=0)
            global_min_y = global_min_y + lines_to_add
        elif lines_to_add < 0:
            # print("before", tuple_of_coords)
            tuple_of_coords = (tuple_of_coords[0] - lines_to_add, tuple_of_coords[1])
            # print("after", tuple_of_coords)
            # if there are to many lines, we move the piece down instead

        return path, chamber, tuple_of_coords

    def lateral_movement(chamber, movement_list, tuple_of_coords, time):
        # updates the piece coords for lateral movement
        plane = "horizontal"

        position = time % (len(movement_list) * 2)  # cycles movements
        # (time, int(position/2))
        offset = movement_list[int(position / 2)]  # every other timestep is downwards
        direction = (plane, offset)
        is_colliding = check_colliding_direction(chamber, tuple_of_coords, direction)
        if not is_colliding:
            tuple_of_coords = (tuple_of_coords[0], tuple_of_coords[1] + offset)
        return tuple_of_coords

    def downwards_movement(chamber, tuple_of_coords):
        # print(chamber, tuple_of_coords)
        # checks if piece is settled, if not it updates the piece coords for horizontal movement
        plane = "lateral"
        offset = 1
        direction = (plane, offset)
        is_colliding = check_colliding_direction(chamber, tuple_of_coords, direction)
        pass
        if not is_colliding:
            tuple_of_coords = (tuple_of_coords[0] + offset, tuple_of_coords[1])
        return tuple_of_coords, is_colliding

    def advance_time(chamber, time, piece_coords):
        # print("adv", chamber, time, piece_coords)
        if time % 2 == 0:
            # print("lat")
            piece_coords = lateral_movement(chamber, movement_list, piece_coords, time)
        else:
            # print("wha")
            piece_coords, is_settled = downwards_movement(chamber, piece_coords)
            # print("d", piece_coords, is_settled)
            if is_settled:
                print("no downwards movement from ", piece_coords)
                print(chamber)
                return piece_coords, time

        time += 1
        piece_coords, time = advance_time(chamber, time, piece_coords)

        # print(piece_coords)
        return piece_coords, time

    def reduce_chamber(chamber, piece):
        global min_y_list
        pass

    def add_piece_to_path(piece_coords, path, matrix):
        #TODO: needs how to determine if piece can reach the walls or just reach first/last pos in path

        # Direction vectors in order of preference
        # North, Northwest, West, Southwest, South, Southeast, East, Northeast
        directions = [
            (-1, -1),  # Northwest (highest preference)
            (-1, 0),  # North
            (-1, 1),  # Northeast
            (0, 1),  # East
            (1, 1),  # Southeast
            (1, 0),  # South
            (1, -1),  # Southwest
            (0, -1)  # West (lowest preference)
        ]

        rows, cols = matrix.shape

        def is_valid(r, c):
            return 0 <= r < rows and 0 <= c < cols and matrix[r, c]

        '''for coords in piece_coords:
            matrix[coords] = True'''

        def get_neighbors(r, c, visited, backwards_visited, path):
            """Get neighbors in order of preference, prioritizing unvisited ones"""
            unvisited = []
            visited_neighbors = []

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc):
                    if (nr, nc) not in visited:
                        unvisited.append((nr, nc))
                    elif (nr, nc) not in backwards_visited:
                        # look throuh paht and append them in order

                        visited_neighbors.append((nr, nc))

            # Return unvisited first, then visited if no unvisited available
            if unvisited:
                return unvisited
            else:
                visited_order = []
                for node in path:
                    if node in visited_neighbors:
                        visited_order.append(node)
                return visited_order

        def dfs(r, c, visited, backwards_visited, path, target_cell):
            print("r", r, "c", c, "target_cell", target_cell)
            # Check if we've reached the east edge
            if (r, c) == target_cell:
                print("target reached with backwards edges: ", backwards_visited)
                return path

            current_path = path + [(r, c)]
            if (r, c) not in visited:
                visited.add((r, c))
            elif (r, c) not in backwards_visited:
                print("backtracking from ", path[-1], "to ", (r, c))
                backwards_visited.add((r, c))
            else:
                return None

            # Get neighbors in preference order
            neighbors = get_neighbors(r, c, visited, backwards_visited, path)
            for nr, nc in neighbors:

                result = dfs(nr, nc, visited.copy(), backwards_visited.copy(), current_path, target_cell)
                if result:
                    return result

            return None

        def first_coords(piece_coords, order):
            print(piece_coords, order)
            if order == "left":
                indices = np.lexsort((-piece_coords[:,0],piece_coords[:,1]))
            if order == "right":
                indices = np.lexsort((piece_coords[:,0], piece_coords[:,1]))
            sorted_coords = piece_coords[indices]
            first_row = sorted_coords[0]
            return (first_row[0],first_row[1])

        earliest_insertion = len(path)
        print(path)
        latest_insertion = 0
        piece_coords = np.transpose(piece_coords)
        for index in range(len(path)):
            (r, c) = path[index]

            #print(piece_coords)
            for (rp, cp) in piece_coords:
                if cp == 0:
                    print("leftrow")
                    earliest_insertion = 0
                if cp == 7:
                    print("rightrow")
                    latest_insertion = len(path)
                if np.abs(rp - r) <= 1 and np.abs(cp - c) <= 1 and (rp != r or cp != c):
                    if index < earliest_insertion:
                        earliest_insertion = index
                    if index > latest_insertion:
                        latest_insertion = index
        print("something odd with the path")
        print(earliest_insertion, latest_insertion, len(path))
        print(piece_coords, path)
        if earliest_insertion > 0:
            origin_cell = path[earliest_insertion]
        else:
            origin_cell = first_coords(piece_coords, "left")
            #highest pchord in left col
        if latest_insertion < len(path): #there is a difference of being able to reach last cell and being after last cell?
            target_cell = path[latest_insertion]
        else:
            target_cell = first_coords(piece_coords, "right")
            #highest pchord in right col
        subpath = dfs(origin_cell[0], origin_cell[1], set(), set(), [], target_cell)
        #issue with subpath
        print(earliest_insertion, latest_insertion, subpath)
        print("prev. path: ", path)
        print("resulting path : ", path[:earliest_insertion] + subpath + path[latest_insertion:])
        return path[:earliest_insertion] + subpath + path[latest_insertion:] #this is clearly wrong

    def reduce_matrix(path, matrix, offset=0):
        # print(path,matrix)
        for item in path:
            matrix[item] = True
        nrows = matrix.shape[0]
        # min_r = (min(x[0]) for x in path)
        # print(path)
        max_r = max((x[0]) for x in path)
        # print(max_r, nrows)
        offset = offset + ((nrows - 1) - max_r)
        reduced_matrix = matrix[:max_r + 1]
        return reduced_matrix, offset

    path, chamber, piece_coords = insert_piece(tetris_shape, path, chamber)
    # collision_tuple = check_colliding_direction(chamber, piece_coords, time)
    time += 1
    settled_piece, time = advance_time(chamber, time, piece_coords)
    # print(chamber)
    # print(settled_piece)
    global_min_y = min(global_min_y, np.min(settled_piece[0]))

    # print(global_min_y)
    chamber[settled_piece] = True

    path = add_piece_to_path(settled_piece, path, chamber)
    chamber, offset = reduce_matrix(path, chamber, offset)
    path = [(r-offset, c) for (r,c) in path]
    for i in range(len(settled_piece[0])):
        settled_piece[0][i] = settled_piece[0][i] - offset



    return path, chamber, time, offset


# drop_new_piece(drop_new_piece(base_state, direction_list, i_tetris))

tetris_order = [line_tetris, plus_tetris, j_tetris, i_tetris, block_tetris]

i = -1
chamber = base_state

offset = 0
time = -1
path = base_path
while i < 2021:
    i += 1
    path, chamber, time, offset = drop_new_piece(chamber, path, direction_list, tetris_order[i % 5], time, offset)

print(chamber.shape[0] - global_min_y - 1)  # bottom is not rock

# print(chamber.shape)

# print(chamber.shape)


# drop_new_piece(base_state, direction_list, j_tetris)
# drop_new_piece(base_state, direction_list, block_tetris)

test = np.array([[False, False, True], [False, True, False], [True, True, True]])
np.where(test == True)

# test
