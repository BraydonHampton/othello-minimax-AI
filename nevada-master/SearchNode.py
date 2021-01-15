class SearchNode:
    def __init__(self,
                 board_obj,
                 board_size,
                 parent_turn,
                 move=None,
                 parent=None,
                 depth=None,
                 score=None
                 ):
        self.move = move
        self.board_obj = board_obj
        self.board_size = board_size
        self.parent = parent
        self.parent_turn = parent_turn
        self.depth = depth
        self.score = score

    def __str__(self):
        return '<SearchNode %s %s %s %s %s>' % (id(self),
                                                self.board_obj,
                                                id(self.parent),
                                                id(self.parent_turn),
                                                self.score)
    def get_score(self):
        return self.score
    