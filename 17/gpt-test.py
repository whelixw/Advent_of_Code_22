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
        (-1, 0),  # North (highest preference)
        (-1, 1),  # Northeast
        (0, 1),  # East
        (1, 1),  # Southeast
        (1, 0),  # South
        (1, -1),  # Southwest
        (0, -1),  # West
        (-1, -1)  # Northwest (lowest preference)






    ]


    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols and matrix[r, c]


    def get_neighbors(r, c, visited):
        """Get neighbors in order of preference, prioritizing unvisited ones"""
        unvisited = []
        visited_neighbors = []

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc):
                if (nr, nc) not in visited:
                    unvisited.append((nr, nc))
                else:
                    visited_neighbors.append((nr, nc))

        # Return unvisited first, then visited if no unvisited available
        return unvisited if unvisited else visited_neighbors


    def dfs(r, c, visited, path):
        # Check if we've reached the east edge
        if c == cols - 1:
            return path + [(r, c)]

        current_path = path + [(r, c)]
        visited.add((r, c))

        # Get neighbors in preference order
        neighbors = get_neighbors(r, c, visited)

        for nr, nc in neighbors:
            # Avoid immediate backtracking
            if len(current_path) >= 2 and (nr, nc) == current_path[-2]:
                continue

            result = dfs(nr, nc, visited.copy(), current_path)
            if result:
                return result

        return None

        # Try starting from each True cell on the west edge (leftmost column)


    for r in range(rows):
        if matrix[r, 0]:
            path = dfs(r, 0, set(), [])
            if path:
                return path

    return None



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