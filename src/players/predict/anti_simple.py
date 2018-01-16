import players
from players.predict import predict
import rps
from random import randrange


class Player(players.RPSPlayer):
    class_name = "AntiSimplePredictorPlayer"
    counter = 0
    
    def __init__(self,*args,**kwargs):
        players.RPSPlayer.__init__(self,*args,**kwargs)
        self.backlog = list()

    def play(self,backlog):
        if len(backlog):
            self.backlog = self.backlog[-len(backlog):]
            prediction = predict(self.backlog)

            if prediction is None:
                ret = players.moves[randrange(0,len(players.moves))]
            else:
                ret =  rps._beats[prediction]
        else:
            ret = players.moves[randrange(0,len(players.moves))]
        self.backlog.append(ret)
        return ret
        
    @classmethod
    def get_name(cls):
        cls.counter += 1
        return '{:}{:d}'.format(cls.class_name,cls.counter)

