
import numpy as np

def find_path_west_to_east(matrix):
    """
    Finds a path from west edge to east edge in a boolean matrix.

    Args:
        matrix: numpy array of booleans where True represents traversable cells

    Returns:
        List of (row, col) tuples representing the path, or None if no path exists
    """
    rows, cols = matrix.shape

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


    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols and matrix[r, c]


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
                    #look throuh paht and append them in order

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
        # Check if we've reached the east edge
        if (r,c) == target_cell:
            print("target reached with backwards edges: ", backwards_visited)
            return path + [(r, c)]

        current_path = path + [(r, c)]
        if (r, c) not in visited:
            visited.add((r, c))
        elif (r, c) not in backwards_visited:
            print("backtracking from ", path[-1], "to ", (r,c))
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

        # Try starting from each True cell on the west edge (leftmost column)

    origin_cell, target_cell = None, None
    for r in range(rows):
        print(r)
        print(origin_cell, target_cell)
        if matrix[r, 0]:
            origin_cell = (r, 0)
        if matrix[r, 6]:
            target_cell = (r, 6)
        if origin_cell is not None and target_cell is not None:
            print(origin_cell, target_cell)
            break

    path = dfs(origin_cell[0], origin_cell[1], set(), set(), [], target_cell)
    if path:
        return path

    return None

def get_max_y(path):
    max_y = -1
    for coordset in path:
        #print(coordset)
        if coordset[0] > max_y:
            max_y = coordset[0]
    return max_y


def add_piece_to_path(piece_coords, path, matrix):
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

    for coords in piece_coords:
        matrix[coords] = True


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
                    #look throuh paht and append them in order

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
        # Check if we've reached the east edge
        if (r,c) == target_cell:
            print("target reached with backwards edges: ", backwards_visited)
            return path + [(r, c)]

        current_path = path + [(r, c)]
        if (r, c) not in visited:
            visited.add((r, c))
        elif (r, c) not in backwards_visited:
            print("backtracking from ", path[-1], "to ", (r,c))
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


    ## new


    earliest_insertion = len(path)
    latest_insertion = 0
    for index in range(len(path)):
        (r, c) = path[index]
        for (rp, cp) in piece_coords:
            if np.abs(rp - r) <= 1 and np.abs(cp - c) <= 1:
                if index < earliest_insertion:
                    earliest_insertion = index
                if index > latest_insertion:
                    latest_insertion = index
    origin_cell = path[earliest_insertion]
    target_cell = path[latest_insertion]
    subpath = dfs(origin_cell[0], origin_cell[1], set(), set(), [], target_cell)
    print(earliest_insertion, latest_insertion)
    return path[:earliest_insertion] + subpath + path[latest_insertion:]

#do a bfs with these indices as origin and target
#return new_path


# Test with your example
test_c = np.array([
    [False, False, False, False, True, False, False],
    [False, False, False, False, True, False, False],
    [False, True, False, False, True, False, False],
    [True, False, False, False, True, True, True],
    [True, True, False, True, False, False, False],
    [True, False, True, True, False, False, False],
    [True, False, False, False, False, False, False],
    [True, True, True, True, True, True, True]
])

path = find_path_west_to_east(test_c)
if path:
    print("Path found:")
    for i, (r, c) in enumerate(path):
        print(f"Step {i + 1}: ({r}, {c})")
else:
    print("No path found")


test_b = np.array([[ True,  False,  True,  True,  True,  True,  True],
       [ True,  False,  False,  True,  True,  True,  True],
       [ True,  True,  False,  True,  True,  True,  True],
       [ True,  True,  True,  False,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True,  True]]) # should yield an offset of 4

path = find_path_west_to_east(test_b)
if path:
    print("Path found:")
    for i, (r, c) in enumerate(path):
        print(f"Step {i + 1}: ({r}, {c})")
else:
    print("No path found")


test_d = np.array([[ True,  False,  True,  False,  True,  True,  True],
       [ True,  True,  True,  False,  True,  True,  True],
       [ True,  True,  True,  False,  True,  True,  True],
       [ True,  False,  False,  False,  False,  True,  True],
       [ True,  True,  False,  True,  False,  True,  True],
       [ True,  True,  False,  True,  False,  False,  True],
       [ True,  True,  False,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True,  True]])

path = find_path_west_to_east(test_d)

if path:
    print("Path found:")
    for i, (r, c) in enumerate(path):
        print(f"Step {i + 1}: ({r}, {c})")
else:
    print("No path found")


test_e = np.array([[ False,  False,  False,  False,  False,  False,  False],
       [ False,  False,  False,  False,  False,  False,  False],
       [ False,  False,  False,  False,  False,  False,  False],
       [ False,  False,  False,  False,  False,  False,  False],
       [ False,  False,  False,  True,  False,  False,  False],
       [ False,  False,  True,  True,  True,  False,  False],
       [ False,  False,  False,  True,  False,  False,  False],
       [ True,  True,  True,  True,  True,  True,  True]]) # should yield an offset of 4

path = find_path_west_to_east(test_e)

if path:
    print("Path found:")
    for i, (r, c) in enumerate(path):
        print(f"Step {i + 1}: ({r}, {c})")
else:
    print("No path found")

test_f = np.array([[ False,  False,  False,  False,  False,  False,  False],
       [ True,  True,  True,  True,  True,  True,  True]])
path = find_path_west_to_east(test_f)

if path:
    print("Path found:")
    for i, (r, c) in enumerate(path):
        print(f"Step {i + 1}: ({r}, {c})")
else:
    print("No path found")


piece = [(0,1),(0,2)]
result = add_piece_to_path(piece, path, test_f)