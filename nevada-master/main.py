import sys
from Problem import *
from Fringe import *
from ClosedList import *
from graph_search import graph_search
from SearchNode import SearchNode


#TO DO
def create_heat_map():
    print "caleb sucks"

def calculate_score():
    pass

def get_max_move(): 
    pass

def get_min_move():
    pass

class Game:
     def __init__(self, board, size, turn, time_left):
         self.board = board
         self.size = size
         self.turn = turn
         self.time_left = time_left

    #Get list of possible moves
    def get_moves(self):
        pass

fringe = IDDFS()

#Get game state from website
#instead of swapping from fringe, put into closed list?

def toTuple(b):
    return tuple(tuple(r) for r in b) 
                    

closed_list = SetClosedListWithCompression()
initial_node = SearchNode(get_initial(size, initial_state), None, None, 0, initial_state)
