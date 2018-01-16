import players

class Player(players.RPSPlayer):
    class_name = "CopycatPlayer"
    counter = 0
    @players.randomfirst
    def play(self,backlog):
        return backlog[-1]
    @classmethod
    def get_name(cls):
        cls.counter += 1
        return '{:}{:d}'.format(cls.class_name,cls.counter)
