"""
Fringe is the base class if fringe subclasses.
    - put, get
    - membership (i.e., __contains__)
    - find and update (later for search such as UCS and heuristic)
    - size
    - __len__ (similar to size)
    - __iter__ (for iteration in a for-loop. This is already done for you.)

A complete Stack and Queue class is provided. However membership check (i.e.
__contains__) is very slow. Therefore we have the following classes:

FSStack and FSQueue

A FSStack object contains a stack and a set. They contain the same values.
The set is used for find membership fast (with O(1) runtime). This is also
the same for FSQueue.
"""
import collections

def to_tuple(b):
    return tuple(tuple(r) for r in b)
class Fringe(object):
    def __init__(self, problem):
        object.__init__(self)
        self.problem = problem
    def put(self, x):
        raise NotImplementedError
    def get(self, x):
        raise NotImplementedError
    def __contains__(self):
        raise NotImplementedError
    def size(self):
        raise NotImplementedError
    def __len__(self):
        return 0 # Must be overwritten
    def __contains__(self, x):
        raise NotImplementedError
    def __iter__(self):
        raise NotImplementedError
 
    
class Stack(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.deque = collections.deque()
    def put(self, node):
        if node.state not in [n.state for n in self.deque]:
            self.deque.append(node)
    def get(self):
        return self.deque.pop()
    def __len__(self):
        return len(self.deque)
    def size(self):
        return len(self.deque)
    def __contains__(self, node):
        for n in self.deque:
            if node.state == n.state:
                return True
        return False
    def __str__(self):
        s = str(self.deque)[7:-2]
        return '<Stack [%s]>' % s
    def __iter__(self):
        return iter(self.deque)

class FSStack(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.set = set()
    def add(self, x):
        self.set.add(x)
    def put(self, x):
        self.deque.append(x)
        self.add(x.board)
    def get(self):
        node =  self.deque.pop()
        self.set.remove(node.board)
        return node
    def __contains__(self, state):
        return to_tuple(state) in self.set
    def remove(self, x):
        self.set.remove(x)

class IDDFS(FSStack):
    def __init__(self, max_depth = 0, initial_node = None, closed_list = None):
        FSStack.__init__(self)
        self.depth_limit = 0
        self.max_depth = -1
        self.initial_node = initial_node

    def put(self, node):
        if node.parent != None:
            parent_depth = node.parent.depth
            node.depth = parent_depth + 1
            #Add cumulative score here
            if (node.depth_limit <= self.depth_limit):
                self.deque.append(node)
                self.set.add(to_tuple(node.board_obj.state))
        else:
            self.deque.append(node)
            self.set.add(node.state)

    def reset(self):
        self.closed_list.clear()
        self.depth_limit += 1
        self.deque.append(self.initial_node)
        self.set.add(self.initial_node.board)
        

    def get(self):
        node =  self.deque.pop()
        self.set.remove(node.board)
        if len(self) == 0:
            self.reset()
        return node

    def remove(self, x):
        self.set.remove(x)

    def __str__(self):
        s = ''
        for n in self.deque:
            s += '<' + str(n.board_obj.state) + ' ' + str(n.board_obj) + '>'
        s = s[:-1]
        return '<IDDFS [%s]>' % s