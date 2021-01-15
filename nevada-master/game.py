## OG Author: Kevin Weston
## Edit for use: Braydon Hampton & Caleb Fischer

## This program will simulate a game of othello in the console
## In order to use it, you need to:
## 1. Import code for your AIs.
## 2. You also need to import a function which applies an action to the board state,
##	and replace my function call (main.get_action(...)) within the while loop.
## 3. Your AIs must have a get_move() function. Assign these functions to
##	white_get_move and black_get_move.
## 4. Create an initial board state to be played on

## Replace these imports with the file(s) that contain your ai(s)
#import main
#import Rando
#import MiniMaximus
import random
import copy
import heatmapper
import minimax

## randyMove, userMove, init_board added by BH

def is_in_bounds(board_size, (r, c)):
    return r < (board_size) and c < (board_size) and r >= 0 and c >= 0

def do_move2(board_state, flip_list, turn):
    #new_state = copy.deepcopy(board_state)
    for space in flip_list:
        board_state[space[0]][space[1]] = turn
    #return new_state

def do_move(board_state, flip_list, turn):
    new_state = copy.deepcopy(board_state)
    for space in flip_list:
        new_state[space[0]][space[1]] = turn
    return new_state

def get_possible_moves(board_size, board_state, turn):
    valid_moves = []
    for r in range(0, board_size, 1):
        for c in range(0, board_size, 1):
            moves = get_valid_move(board_size, board_state, turn, (r,c))
            if len(moves) > 0:
                for sublist in moves:
                    valid_moves.append(sublist) #flatten list
    
    
    valid_moves_remove_dupes = {}
    returned_moves = []
    if len(valid_moves) > 0:
        for move in valid_moves:
            if move[0] in valid_moves_remove_dupes:
                index = valid_moves_remove_dupes[move[0]]
                returned_moves[index] = (returned_moves[index][0], returned_moves[index][1] + move[1]) #concat to combine two sets of flipping
            else:
                returned_moves.append(move)
                valid_moves_remove_dupes[move[0]] =  (len(returned_moves) - 1)
    #print returned_moves
    return returned_moves

def get_valid_move(board_size, board_state, turn, (r,c)): #turn = 'B' or 'W'
    opponent_tile = 'W' if turn == 'B' else 'B'
    
    valid_moves = []
    if board_state[r][c] == turn: #only search around turn tiles
        for (row_direction, col_direction) in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            (row_search,col_search) = (r,c)
            flip_list = []
            row_search = row_search + row_direction
            col_search = col_search + col_direction

            while is_in_bounds(board_size, (row_search,col_search)) and board_state[row_search][col_search] == opponent_tile:
                flip_list.append((row_search, col_search))
                row_search += row_direction
                col_search += col_direction
            
            if (
                is_in_bounds(board_size, (row_search,col_search)) 
                and len(flip_list) > 0 
                and board_state[row_search][col_search] == ' '
            ):        
                flip_list.append((row_search,col_search))                                                    #some tiles can have multiple moves
                valid_moves.append(((row_search, col_search), flip_list)) #only append if end is a space

    return valid_moves

def randyMove(board_size, board_state, turn, time_left, opponent_time_left):
    valid_moves = get_possible_moves(board_size, board_state, turn)
    if len(valid_moves) > 0:
        selected_move = valid_moves[random.randrange(0, len(valid_moves))]
        do_move2(board_state, selected_move[1], turn)
        return selected_move[0]
    else:
        return None

def mmMove(board_size, board_state, turn, time_left, opponent_time_left):
    #for best move as black, maxDepth should be odd, white -> even
    
    maxDepth = 3 if turn == 'B' else 2
    possible_moves = get_possible_moves(board_size, board_state, turn)
    if len(possible_moves) <= 0:
        return None

    
    heur = heatmapper.generate_heatmap(board_size)
    INF = 100000000
    initialNode = minimax.searchNode(board_state, board_size, turn)
    
    alphaNode = minimax.searchNode(None, None, None, None, None, -INF)
    betaNode = minimax.searchNode(None, None, None, None, None, INF)
    bestMove = minimax.minimax(initialNode, "MAX", alphaNode, betaNode, maxDepth, 0, heur, turn)
    
    #print "Move leads to this: %s" % bestMove.score
    #print_board(bestMove.board_state, board_size)
    move = bestMove.OGmove.move
    print "MM Sending: %s" % str(move)
    
    for child in possible_moves:
        if child[0] == move:
            do_move2(board_state, child[1], turn)
            break   
    
    return move

def ai_move(board_size, board_state, turn, time_left, opponent_time_left):
    possible_moves = get_possible_moves(board_obj.size, board_obj.state, board_obj.turn)
    fringe = IDDFS()
    for moves in possible_moves:
        fringe.put(Board(board_size, board_state, turn))
        
    initial_node = SearchNode((r, c), new_board_obj, board_obj, turn, new_board_obj.score)
    fringe.put()
    selected_move = graph_search()
    do_move(board_state, selected_move[1], turn) #((r,c), flip_list)
    return selected_move[0]

def userMove(board_size, board_state, turn, time_left, opponent_time_left):
    valid_moves = get_possible_moves(board_size, board_state, turn)
    print valid_moves
    if len(valid_moves) > 0:
        row = input("Row: ")
        col = input("Col: ")
        while 1:
            for x in range(len(valid_moves)):
                if valid_moves[x][0] == (row, col):
                    do_move2(board_state, valid_moves[x][1], turn)
                    return (row, col)
            print "Invalid move! Try again!"
            row = input("Row: ")
            col = input("Col: ")
    else:
        return None

def init_board(board_size):
    board_state = [[' '] * board_size for i in range(board_size)] 

    board_state[board_size / 2][board_size / 2] = 'W'
    board_state[board_size / 2 - 1][board_size / 2 - 1] = 'W'
    board_state[board_size / 2 - 1][board_size / 2] = 'B'
    board_state[board_size / 2][board_size / 2 - 1] = 'B'

    print_board(board_state, board_size)

    return board_state


def get_winner(board_state):
    black_score = 0
    white_score = 0
    for row in board_state: 
        for col in row: 
            if col == 'W':
                white_score += 1
            elif col == 'B':
                black_score += 1
    
    if black_score > white_score:
        winner = 'B'
    elif white_score > black_score:
        winner = 'W'
    else:
        winner = None
    return (winner, white_score, black_score)


def prepare_next_turn(turn, white_get_move, black_get_move):
	next_turn = 'W' if turn == 'B' else 'B'
	next_move_function = white_get_move if next_turn == 'W' else black_get_move
	return next_turn, next_move_function


# needs state and size atm - BH
def print_board(board_state, board_size, tabover = 0):
    tabover = '\t' * tabover
    s = '    '.join([str(x) for x in range(board_size)])
    print tabover, "   ", s
    row_num = 0
    for row in board_state:
        print tabover, row_num, row
        row_num += 1
   	 

def apply_action(board_state, action, turn):
    board_state[action[0]][action[1]] = turn
    return board_state

def simulate_game(board_state,
              	board_size,
              	white_get_move,
              	black_get_move):
    player_blocked = False
    turn = 'B'
    get_move = black_get_move
    print_board(board_state, board_size)
    see_moves = input("See moves? Yes = 0  No = 1")
    while True:
        	## GET ACTION ##
        next_action = get_move(board_size=board_size,
                                board_state=board_state,
                                turn=turn, 
                                time_left=0, 
                                opponent_time_left=0)
        
        print "turn: ", turn, "next action: ", next_action
        if see_moves == 0: _ = raw_input()
        ## CHECK FOR BLOCKED PLAYER ##
        # The gameover check - BH
        if next_action is None:
            if player_blocked:
                print "Both players blocked!"
                break
            else:
                player_blocked = True
                print "Player %s had to skip!" % str(turn)
                time_left = 0
                opponent_time_left = 0
                turn, get_move = prepare_next_turn(turn,
                                white_get_move, 
                                black_get_move)
                continue
        else:
            player_blocked = False

    	## APPLY ACTION ##
    	## Replace this function with your own apply function
        # AKA place the piece on the board - BH
    	#board_state = apply_action(board_state=board_state,action=next_action,turn=turn)

    	print_board(board_state, board_size)
    	turn, get_move = prepare_next_turn(turn, white_get_move, black_get_move)
 
	winner, white_score, black_score = get_winner(board_state)

	print "Winner: ", winner
	print "White score: ", white_score
	print "Black score: ", black_score
    

if __name__ == "__main__":
	
    board_size = board_size = input("Board Size: ")
    while board_size % 2 is not 0:
        print "Invalid board size"
        board_size = input("Board Size: ")

    board_state = init_board(board_size)

	## Give these the get_move functions from whatever ais you want to test
    white_get_move = mmMove
    black_get_move = mmMove
    simulate_game(board_state, board_size, white_get_move, black_get_move)
