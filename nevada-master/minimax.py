
################################################
## Author: Braydon Hampton
## 
## The following contains the minimax algorithm
## using a basic tree with basic nodes
################################################
import random
import heatmapper
import game


## Node class for testing minimax - to be deleted later
class node:
    def __init__(self, value=None, parent=None):
        self.value = value
        self.parent = parent
        self.children = []

    def __str__(self):
        if self.parent == None:
            return "Root Node: %s" % str(id(self))
        elif self.value is not None:
            return "\tLeaf Node: %s from parent %s" % (str(self.value), str(id(self.parent)))
        else:
            return "Node: %s from parent %s" % (str(id(self)), str(id(self.parent)))

    def prints(self, level=0):
        print '\t' * level + str(self) + "  Term: %s" % self.isTerm()
        for child in self.children:
            child.prints(level+1)

    def isTerm(self):
        return len(self.children) is 0

    def populate(self, width, depth):
        if depth is not 1:
            for val in range(width):
                self.children.append(node(None, self))
                self.children[val].populate(width, depth-1)
        else:
            for val in range(width):
                x = input("Leaf node: ")
                self.children.append(node(x, self))

    def RandomPopulate(self, width, depth):
        if depth is not 1:
            for val in range(width):
                self.children.append(node(None, self))
                self.children[val].RandomPopulate(width, depth-1)
        else:
            for val in range(width):
                x = random.randint(1, 20) 
                self.children.append(node(x, self))
                
class searchNode():
    def __init__(self, board_state, board_size, turn,
                 OGmove = None, move = None, score = None):
        self.board_state = board_state
        self.board_size = board_size
        self.turn = turn
        self.OGmove = OGmove
        self.move = move
        self.score = score
        
    def __str__(self):
        if self.move == None:
            return "Root Node: %s" % str(id(self))
        elif self.score == None:
            return "Middle Node: %s " % str(id(self))
        else:
            return "\tTerminal Node: %s score: %s" % (str(id(self)), self.score)
'''        
    def get_needed_move(self):
        node = self
        while node.parent is not None and node.parent.parent is not None:
            node = node.parent
        return node.move
'''
## Tree class to test minimax - to be deleted later
class Tree:
    def __init__(self):
        self.root = node()

    def prints(self):
        self.root.prints()
    
    def populate(self, width, depth):
        choice = input("Random: [0] UserInput: [1] ")
        if choice is 1:
            self.root.populate(width, depth)
        else:
            self.root.RandomPopulate(width, depth)

    
INF = 10000000000

#need to make node only remember OGmove
def minimax(s, player, alpha, beta, maxDepth, currentDepth, heuristic, turn):
    valid_moves = game.get_possible_moves(s.board_size, s.board_state, s.turn)
    OGmove = s if currentDepth == 1 else s.OGmove
    if maxDepth == currentDepth or len(valid_moves) <= 0:
        #nextTurn = 'W' if s.turn == 'B' else 'B'
        s.score = heatmapper.eval_heur(s.board_state, heuristic, turn)
        s.OGmove = OGmove
            
        #print "Terminal, sending %s for player %s" % (s.score, nextTurn)
        return s
    else:
        nextTurn = 'W' if s.turn == 'B' else 'B'
        for child in valid_moves:
            newState = game.do_move(s.board_state, child[1], s.turn)
            newNode = searchNode(newState, s.board_size, nextTurn, OGmove, child[0])
            v = minimax(newNode, player, alpha, beta, maxDepth, currentDepth + 1, heuristic, turn)
            
            if player is "MAX":
                if v.score >= beta.score:   
                    return beta
                if v.score > alpha.score:
                    alpha = v
            else:
                if v.score <= alpha.score:
                    return alpha
                if v.score < beta.score:
                    beta = v
        return alpha if player is "MAX" else beta



if __name__ == '__main__':
    
    board_size = input("Board Size: ")
    while board_size % 2 is not 0:
        print "Invalid board size"
        board_size = input("Board Size: ")

    board_state = game.init_board(board_size)
    heur = heatmapper.generate_heatmap(board_size)
    initialNode = searchNode(board_state, board_size, 'B')
    
    alphaNode = searchNode(None, None, None, None, None, -INF)
    betaNode = searchNode(None, None, None, None, None, INF)
    bestMove = minimax(initialNode, "MAX", alphaNode, betaNode, 2, 0, heur)
    print "BESTEST MOVE:"
    print bestMove
