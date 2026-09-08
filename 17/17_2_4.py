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
    this will reduce the offset and memory for pieces. a legal path has to start at one boundary and end at the other

algorithms:
    search: not really e dfs, always picks highest piece until it can form a "bridge" that connects each side
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


#todo: implement heuristic search without cycles, test larger pieces
# a new piece has neighbours. we can define a number cases for how to augment the pieceset
# i think i intended the set to be a way to narrow the neighbour search to only relevant pieces,
#   not as a replacement for the path
# if the piece is one the perimiter its always at the start or end of the path.
# otherwise, if the placed piece only has one neighbour
#   substitute one occurence of neighbour with neighbour -> placed_piece -> neighbour
# if the placed piece has multiple neighbours:
#   we need to trace the new perimeter, until we reach a subpath in the previous path/pieceset
#   what is the first/last point in the previous path that the newly placed piece can be reached?
#   if first and last point is not identical (which it shouldn't be since multiple neighbours) it can form a "bridge"
#   any pieces not on the new path can then be pruned
import numpy as np

class Piece:
    def __init__(self, shape = [], neighbours = set()):
        self.shape = shape #list of tuples of the shape
        self.neighbours = neighbours #point to other pieces it is touching
        self.x = None #origin point
        self.y = None #origin point

class PieceGrid():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.empty((rows, cols), dtype=object)
        self.pieceset = set()
        self.piece_path = list()


    def validate_piece_path(self, input_piece_path):
        #checks that a path is correctly formed. the path needs to connect the right and left side through pieces
        index = 0
        found = False
        while index < len(input_piece_path):
            selected_tuple = input_piece_path[index]
            x,y = selected_tuple
            #print(index)
            if index == 0:
                if y != 0:
                    return False
                else:
                    index += 1
                    continue
            elif index == len(input_piece_path)-1:
                if y != 6:
                    return False
                else: return True
            elif found == True:
                #print("bb")
                found = False
                continue
            else:
                for neighbour in self.matrix[x][y].neighbours:
                    if neighbour == input_piece_path[index+1]:
                        index += 1
                        found = True
                        #print("aa")
                        break
            if not found:
                return False

    def restructure_piece_path(self, piece, path_cuts): #make a new path that excludes the cuts
        if path_cuts[0] == None:
            self.piece_path = [(piece.x, piece.y)] + self.piece_path[path_cuts[1]:]
        elif path_cuts[1] == None:
            self.piece_path = self.piece_path[:path_cuts[0]] + [(piece.x, piece.y)]
        else:
            self.piece_path = self.piece_path[:path_cuts[0]] + [(piece.x, piece.y)] + self.piece_path[path_cuts[1]:]
        self.pieceset -= set(self.piece_path[path_cuts[0]:path_cuts[1]]) #remove pieces from pieceset
        #print("new", self.piece_path)
        #return self.piece_path

    def check_bounds(self, r, c, error=True):
        if r >= self.rows or c >= self.cols:
            if error:
                raise ValueError("Out of bounds")
        else:
            return (r, c)

    def neighbours_to_path_point(self, piece): #figures out where the piece can be inserted in the path
        max_index = -1
        min_index = len(self.piece_path)
        for neighbour in piece.neighbours:
            index = self.piece_path.index(neighbour)
            if index > max_index:
                max_index = index
            if index < min_index:
                min_index = index
        if piece.x == 0:
            min_index = None
        if piece.x == 6:
            max_index = None
        path_cuts = min_index, max_index
        return path_cuts



    def place_piece(self, piece, origin_x, origin_y):


        buffer = set()
        print("place", piece.shape)
        print(chamber.matrix)
        for dr, dc in piece.shape: #check all cells are free to for the piece to be inserted
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
        #print("buffer", buffer)
        for pairs in buffer:
            #check for neighbours
            for d in directions:
                r, c = (pairs[0]+d[0], pairs[1]+d[1])
                #print(r,c)
                if (r,c) not in buffer and not(r < 0 or c < 0):
                    if self.check_bounds(r,c, False) != None:
                        if (r != None and c != None):
                            if self.matrix[r][c] is not None:
                                print("neighbour at: ", tuple([self.matrix[r][c].x, self.matrix[r][c].y]), r, c)
                                piece.neighbours.add((self.matrix[r][c].x, self.matrix[r][c].y)) # add neighbours coords to set
                                #piece.neighbours.add(tuple([self.matrix[r][c].x, self.matrix[r][c].y]))
                                print(piece.neighbours)
                                self.matrix[r][c].neighbours.add((piece.x, piece.y)) #add coords to neighbours set
                                print(self.matrix[r][c].neighbours)
            print("placing")
            print(piece)
            #self.x, self.y = pairs[0], pairs[1]
            self.matrix[pairs[0]][pairs[1]] = piece


        #update piece path

        self.pieceset.add((piece.x, piece.y))
        path_cuts = self.neighbours_to_path_point(piece)
        print("ok?")
        print(path_cuts)
        self.restructure_piece_path(piece, path_cuts)


        #TODO: clean path and pieceset
        #search through neighbours to see where in the path you can place it
        # the deeper in the path the better




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


def initiate_chamber_base(chamber):
    initial_coords = [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6)]
    for index, item in enumerate(initial_coords):
        neighbours = []
        print(index,item)
        if index != 0:
            neighbours.append(initial_coords[index-1])
        if index != len(initial_coords)-1:
            neighbours.append(initial_coords[index+1])
        chamber.matrix[item] = Piece([item], set(neighbours))
        chamber.matrix[item].x = item[0]
        chamber.matrix[item].y = item[1]
        chamber.pieceset.add(item)
        chamber.piece_path.append(item)
    return chamber

chamber = PieceGrid(2,7)

chamber = initiate_chamber_base(chamber)

piece1 = Piece([(0,0)], set())
chamber.place_piece(piece1,0,0)



