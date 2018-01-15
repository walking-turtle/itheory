import players

class Player(players.RPSPlayer):
    @players.randomfirst
    def play(self,backlog):
        return backlog[-1]
