class ClosedList(object):
    def __init__(self):
        object.__init__(self)
    def put(self, x):
        """ Put x into closed list """
        raise NotImplementedError
    def __contains__(self, x):
        """ Implements "in" operator to check is x is in the closed list """
        raise NotImplementedError
    def size(self):
        """ Returns the number of values in the closed list """
        raise NotImplementedError
    def __len__(self):
        """ Returns the number of values in the closed list """
        return 0 # Must be overwritten
    def values(self):
        raise NotImplementedError
    def __iter__(self):
        raise NotImplementedError
    def clear(self):
        raise NotImplementedError

class SetClosedListWithCompression(ClosedList):
    """ Implementation of ClosedList using python sets and with state compression"""
    def __init__(self, compress=lambda x:x, decompress=lambda x:x):
        """
        compress -- a function to compress state
        decompress -- inverse function of compress
        """
        ClosedList.__init__(self)
        self.set = set()
        self.compress = compress
        self.decompress = decompress
    def add(self, x):
        x = self.compress(x)
        self.set.add(x)
    def __contains__(self, x):
        x = self.compress(x)
        return x in self.set
    def size(self):
        return len(self.set)
    def __len__(self):
        return len(self.set)
    def __str__(self):
        s = str(self.set)[5:-2]
        return "<SetClosedListWithCompression {%s}>" % s
    def values(self):
        f = self.decompress
        return [f(x) for x in self.set]    
    def __iter__(self):
        for x in self.set:
            yield f(x)
        raise StopIteration
    def clear(self):
        self.set.clear()

        #test
