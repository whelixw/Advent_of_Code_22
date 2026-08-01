#I think I should refactor
#lets try to model the pieces as single nodes instead
#each node has a set of coordinates that it belongs to.
# a node whose set of coords are adjecent to another node's coords is adjecent to the node.
# the pathfinding algorithm needs to find the "highest" path. how can we handle this, when a node has multiple?
# when a piece is connected to a node, the coord it connects to could be notd. then the highest coord could be prioritized


"""
draft:

data structures:

    offset: an int that indicates the distance to the bottom of the chamber. This is uses to keep coords consistent.

    dict of "pointers" - key : coords for each piece, value : "pointer" to node object

    nodes: represnts pieces,  contains edges to neighbouring coords, which gives access to other nodes/pieces
        the chamber boundaries are special nodes that are infinitely tall

    path: the highest path outlines a perimeter that can be used to simplify the pointer dict.
    any pieces under the path can be removed and all rows under can be ignored as well
    this will reduce the offset. a legal path has to start at one boundary and end at the other

algorithms:
    search: not really e dfs, always picks highest piece until it can form a "bridge"
        by handling the pieces as nodes. the search state needs to contain the selected piece
        as well as all edges used earlier. we need a way of avoiding cycles.
        this can probably be accomplished by removing the set of used edges?
        can maybe be thought of as a priQ?

steps:
    initialize the 7 cells at the start as nodes - they are treated as a piece each
    this is the initial path
    iterate:
        read next piece make space for it and change the offset
        place the piece, see if it collides - this is done by checking dict
            advance time, move piece and repeat above step until collision happens
        a node is created, connected to any other node that is dist 1 away, incl diagonal
        the path should be updated: the new path HAS to include the new piece and HAS to have some subset of last path


"""


#todo
import numpy as np

class Piece:
    def __init__(self, shape = [], neighbours = set()):
        self.shape = shape #list of tuples of the shape
        self.neighbours = neighbours
        self.x = None #origin point
        self.y = None #origin point

class PieceGrid():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.empty((rows, cols), dtype=object)
        self.pieceset = set()

    def check_bounds(self, r, c, error=True):
        if r >= self.rows or c >= self.cols:
            if error:
                raise ValueError("Out of bounds")
        else:
            return (r, c)

    def place_piece(self, piece, origin_x, origin_y):


        buffer = set()
        print("place", piece.shape)
        for dr, dc in piece.shape:
            r = origin_x+dr
            c = origin_y+dc

            r,c = self.check_bounds(r,c)

            if self.matrix[r][c] is not None:
                raise ValueError(f"Collision at {r}, {c}")
            buffer.add((r,c))
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
        piece.x = origin_x
        piece.y = origin_y
        for pairs in buffer:
            #check for neighbours
            for d in directions:
                r, c = (pairs[0]+d[0], pairs[1]+d[1])
                print(r,c)
                if (r,c) not in buffer:
                    if self.check_bounds(r,c, False) != None:
                        if r and c:
                            if self.matrix[r][c] is not None:
                                print("neighbour at: ", tuple([self.matrix[r][c].x, self.matrix[r][c].y]))
                                piece.neighbours.add((self.matrix[r][c].x, self.matrix[r][c].y)) # add neighbours coords to set
                                #piece.neighbours.add(tuple([self.matrix[r][c].x, self.matrix[r][c].y]))
                                print(piece.neighbours)
                                self.matrix[r][c].neighbours.add((piece.x, piece.y)) #add coords to neighbours set
                                print(self.matrix[r][c].neighbours)
            print("placing")
            print(piece)
            self.matrix[pairs[0]][pairs[1]] = piece
        self.pieceset.add(piece)


    def remove_piece(self, piece):
        buffer = []
        for dr, dc in piece.shape:
            r = piece.x+dr
            c = piece.y+dc
            r,c = self.check_bounds(self, r, c)
            if self.matrix[r][c] is None:
                raise ValueError(f"Missing at {r}, {c}")
            buffer.append((r,c))
            for pairs in buffer:
                self.matrix[pairs[0]][pairs[1]] = None
            self.pieceset.remove(piece)


chamber = PieceGrid(2,7)

piece1 = Piece([(0,0)], set())
chamber.place_piece(piece1,1,1)
piece2 = Piece([(0,0)], set())
chamber.place_piece(piece2,1,2)