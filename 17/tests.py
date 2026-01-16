import numpy as np

matrix = [
    [False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False],
    [False, False, True, False, False, False, False],
    [False, False, True, False, False, False, False],
    [True, True, True, True, False, False, False],
    [False, False, True, True, True, False, False],
    [False, False, False, True, False, False, False],
    [False, False, True, True, True, True, False],
    [True, True, True, True, True, True, True],
]

prev_path = [
    (9, 0),
    (9, 1),
    (8, 2),
    (7, 2),
    (8, 2),
    (9, 3),
    (10, 4),
    (11, 3),
    (10, 2),
    (9, 2),
    (10, 3),
    (11, 3),
    (12, 4),
    (12, 5),
    (13, 6),
]

piece_chords = [[6, 4], [7, 4], [8, 4], [9, 4]]


def add_piece_to_path(piece_coords, path, matrix):
    # TODO: needs how to determine if piece can reach the walls or just reach first/last pos in path
    # Also, the new piece coords should always be in path before reducing. This should not happen:
    """prev. path:  [(9, 0), (9, 1), (8, 2), (7, 2), (8, 2), (9, 3), (10, 4), (11, 3), (10, 2), (9, 2), (10, 3), (11, 3), (12, 4), (12, 5), (13, 6)]
    resulting path :  [(9, 0), (9, 1), (8, 2), (7, 2), (8, 2), (9, 3), (8, 2), (7, 2), (8, 2), (9, 2), (10, 3), (11, 3), (12, 4), (12, 5), (13, 6)]"""

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
            indices = np.lexsort((-piece_coords[:, 0], piece_coords[:, 1]))
        if order == "right":
            indices = np.lexsort((piece_coords[:, 0], piece_coords[:, 1]))
        sorted_coords = piece_coords[indices]
        first_row = sorted_coords[0]
        return (first_row[0], first_row[1])

    earliest_insertion = len(path)
    print(path)
    latest_insertion = 0
    piece_coords = np.transpose(piece_coords)
    for index in range(len(path)):
        (r, c) = path[index]

        # print(piece_coords)
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
        # highest pchord in left col
    if latest_insertion < len(
            path):  # there is a difference of being able to reach last cell and being after last cell?
        target_cell = path[latest_insertion]
    else:
        target_cell = first_coords(piece_coords, "right")
        # highest pchord in right col
    subpath = dfs(origin_cell[0], origin_cell[1], set(), set(), [], target_cell)
    # issue with subpath
    print(earliest_insertion, latest_insertion, subpath)
    print("prev. path: ", path)
    print("resulting path : ", path[:earliest_insertion] + subpath + path[latest_insertion:])
    return path[:earliest_insertion] + subpath + path[latest_insertion:]  # this is clearly wrong

piece_chords = np.transpose(np.array(piece_chords))
matrix = np.array(matrix)
print(piece_chords, matrix)

result = add_piece_to_path(piece_chords, prev_path, matrix)