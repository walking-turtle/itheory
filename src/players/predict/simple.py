import players
from players.predict import predict
import rps
from random import randrange


class Player(players.RPSPlayer):
    class_name = "SimplePredictorPlayer"
    counter = 0
    
    @players.randomfirst
    def play(self,backlog):
        prediction = predict(backlog)
        if prediction is None:
            return players.moves[randrange(0,len(players.moves))]
        return rps._is_beaten_by[prediction]
        
    @classmethod
    def get_name(cls):
        cls.counter += 1
        return '{:}{:d}'.format(cls.class_name,cls.counter)
