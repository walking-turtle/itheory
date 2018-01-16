import players
from random import randrange

class Player(players.RPSPlayer):
    def play(self,backlog):
        return players.moves[randrange(0,len(players.moves))]
