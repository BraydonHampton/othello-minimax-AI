import sys


## borrowed from game.py for testing
def init_board(board_size):
    board_state = [[' '] * board_size for i in range(board_size)] 

    board_state[board_size / 2][board_size / 2] = 'W'
    board_state[board_size / 2 - 1][board_size / 2 - 1] = 'W'
    board_state[board_size / 2 - 1][board_size / 2] = 'B'
    board_state[board_size / 2][board_size / 2 - 1] = 'B'

    #print_board(board_state, board_size)

    return board_state

def matrix(n, s):
    chunkContainer = []
    for i in range(0, (n * n), n):
        chunkContainer.append(s[i:i + n])
    return chunkContainer

def isCorner(n, i):
    return (i == n - 1 or i == n * n - 1 or i == (n * n) - n or i == 0)

def print_board(board_state, board_size):
    s = '\t '.join([str(x) for x in range(board_size)])
    print "   ", s
    print "--------" * board_size
    row_num = 0
    for row in board_state:
        q = '\t|'.join([str(x) for x in row])
        print row_num, '|', q
        row_num += 1

def generate_heatmap(n):
    DEFAULT = 50
    heuristic = [DEFAULT] * (n * n)
    seperator = ','
    MAX = n * 1000

    #CORNERS========================================
    heuristic[0] = MAX
    for i in range(1, (n * n), 1):
        if (isCorner(n, i)):
            heuristic[i] = MAX

    matrixBoard = matrix(n, heuristic)

    #SECONDTOLAST=======================================================================
    SECOND_ROW = 5
    for i in range(n):
        if (matrixBoard[1][i] != MAX):
            matrixBoard[1][i] = SECOND_ROW

    # last row
    for i in range(n):
        if (matrixBoard[n - 2][i] != MAX):
            matrixBoard[n - 2][i] = SECOND_ROW

    # col 0
    for i in range(n):
        if (matrixBoard[i][1] != MAX):
            matrixBoard[i][1] = SECOND_ROW

    # last col
    for i in range(n):
        if (matrixBoard[i][n - 2] != MAX):
            matrixBoard[i][n - 2] = SECOND_ROW

    #EDGES==============================================================================
    # row 0
    EDGE_VAL = 100
    for i in range(n):
        if (matrixBoard[0][i] != MAX):
            matrixBoard[0][i] = EDGE_VAL

    # last row
    for i in range(n):
        if (matrixBoard[n - 1][i] != MAX):
            matrixBoard[n - 1][i] = EDGE_VAL

    # col 0
    for i in range(n):
        if (matrixBoard[i][0] != MAX):
            matrixBoard[i][0] = EDGE_VAL

    # last col
    for i in range(n):
        if (matrixBoard[i][n - 1] != MAX):
            matrixBoard[i][n - 1] = EDGE_VAL
    #===============================================================================
    
    #BY_CORNERS========================================================================
    #top left
    matrixBoard[0][1] = 1
    matrixBoard[1][1] = 0
    matrixBoard[1][0] = 1

    #top right
    matrixBoard[0][n - 2] = 1
    matrixBoard[1][n - 2] = 0
    matrixBoard[1][n - 1] = 1

    #bottom left
    matrixBoard[n - 2][0] = 1
    matrixBoard[n - 2][1] = 0
    matrixBoard[n - 1][1] = 1
    
    #bottom right
    matrixBoard[n - 2][n - 1] = 1
    matrixBoard[n - 2][n - 2] = 0
    matrixBoard[n - 1][n - 2] = 1
    #==========================================================================

    print_board(matrixBoard, n)
    return matrixBoard
        
        
def eval_heur(board_state, heuristic, turn):
    w_count = 0
    b_count = 0
    empty_count = 0
    w_weight = 0
    b_weight = 0
    
    for i in range(len(board_state)):
        for j in range(len(board_state)):
            if board_state[i][j] == ' ':
                empty_count += 1
            elif board_state[i][j] == 'B':
                b_count += 1
                b_weight += heuristic[i][j]
            elif board_state[i][j] == 'W':
                w_count += 1
                w_weight += heuristic[i][j]
    
    if turn == 'B':
        return b_weight - w_weight
    else:
        return w_weight - b_weight
    #print "White weight:", w_weight
    #print "White count:", w_count
    
    #print "Black weight:", b_weight
    #print "Black count:", b_count    


if __name__ == "__main__":
    size = input("Input size: ")
    heur = generate_heatmap(size)
    board = init_board(size)

    eval_heur(board, heur, 'B')

