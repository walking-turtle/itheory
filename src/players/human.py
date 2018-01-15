import rps
import players

_moves = list()
_keys = dict()

for k in rps._names:
    _moves.append("{:} ({:})".format(rps._names[k],rps._keys[k]))
    _keys[rps._keys[k]] = k

_moves = ','.join(_moves)

class Player(players.RPSPlayer):
    def play(self,backlog):
        print("Whats your move? {:}".format(_moves))
        while 1:
            try:
                choice = input("> ")
            except EOFError:
                return None
            if choice:
                c = choice[0]
                if c in _keys:
                    return _keys[c]
