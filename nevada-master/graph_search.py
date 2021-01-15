import random
from SearchNode import SearchNode
from game import get_possible_moves
from game import do_move
#==============================================================================
# GRAPH_SEARCH
#
# The fringe and closed list must be drawn while the thinking takes place.
# - Draw the closed list blue (255, 0, 0).
# - Draw the fringe in green (0, 255, 0).
#
# There must be NO console printing in this python file. Make sure you remove
# them or comment them out when you are done.
#==============================================================================
class Board():
    def __init__(self,
                 size=None,
                 state=None,
                 turn=None
                 ):
        self.size = size
        self.state = state
        self.turn = turn

    def next_turn(self):
        return ('W' if self.turn == 'B' else 'B')


def graph_search(
                 fringe,
                 ):
    #==========================================================================
    # TODO: The code here creates a *random* solution starting at state (0,0).
    # Replace with the correct late version of graph search algorithm.
    #CONVERT BOARD TO TUPLE TO STORE IN CLOSED LIST
    #==========================================================================
    solution = []
    def toList(b):
        return list(list(r) for r in b)

    i = 0
    while 1:
        while len(fringe) > 0:
            board_obj = fringe.get() #let's store the whole board obj
            
            # if problem.goal_test(toList(board_obj.state)): #yeah idk what we're going to do for the return
            #     return move
            #move = ((r,c), flip_list)
            possible_moves = get_possible_moves(board_obj.size, board_obj.state, board_obj.turn)
            if possible_moves != []:
                for move in possible_moves:
                    (r, c) = move[0]
                    new_board_obj = Board(board_obj.size, do_move(board_obj.state, move[1], move[0]), board_obj.next_turn()) 
                    
                    if not(new_board_obj.state in fringe.set):
                        fringe.put(SearchNode((r, c), new_board_obj, board_obj, turn, new_board_obj.score))
        return None            