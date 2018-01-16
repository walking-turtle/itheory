import rps
from random import randrange

moves = list(rps._names)

def randomfirst(f):
    def g(s,bl):
        if len(bl):
            return f(s,bl)
        else:
            return moves[randrange(0,len(moves))]
    return g

class RPSPlayer():
    def __init__(self,name=None):
        if name is not None:
            self.name = str(name)
        else:
            self.name = type(self).get_name()
    def play(self,backlog):
        raise NotImplementedError('{:}.play'.format(str(type(self))))
    @classmethod
    def get_name(cls):
        raise NotImplementedError('{:}.get_name'.format(str(cls)))
