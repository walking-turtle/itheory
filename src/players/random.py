import players
from random import randrange

class Player(players.RPSPlayer):
    class_name = "RandomPlayer"
    counter = 0
    def play(self,backlog):
        return players.moves[randrange(0,len(players.moves))]
    @classmethod
    def get_name(cls):
        cls.counter += 1
        return '{:}{:d}'.format(cls.class_name,cls.counter)
