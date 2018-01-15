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
        print("What's your move, {:}? {:}".format(self.name,_moves))
        rps.say("Given backlog: {:}".format([rps._names[k] for k in backlog]))
        while 1:
            try:
                choice = input("> ")
            except EOFError:
                print("")
                return None
            if choice:
                c = choice[0].upper()
                if c in _keys:
                    return _keys[c]
