import rps
from random import randrange

moves = list(rps._names)

def randomfirst(f):
    def g(s,bl):
        if len(bl):
            return f(s,bl)
        else:
            return moves[randrange(0,len(moves))]

class RPSPlayer():
    def __init__(self,name):
        self.name = str(name)
    def play(self,backlog):
        raise NotImplemented
