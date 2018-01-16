import rps
from game import RPSGame as G

class RPSTournament():
    def __init__(self,name="Tournament",memory=0,steps=0):
        self.used = 0
        self.game_memory = memory
        self.game_steps = steps
        self.name = name
        self.players = dict()
        self.categories = dict()
        self.scores = dict()
        self.victories = dict()

    def add_players(self,C,n=1):
        n = max(1,n)
        if C not in self.categories:
            self.categories[C] = list()
        for _ in range(n):
            p = C()
            self.players[p] = C
            self.scores[p] = 0
            self.victories[p] = 0
            self.categories[C].append(p)
        return self

    def add_score(self,p,x):
        self.scores[p] = self.scores.get(p,0) + x
        return self

    def add_victory(self,p):
        if p is not None:
            self.victories[p] = self.victories.get(p,0) + 1
        return self

    def run(self):
        for _ in self:
            pass

    def __enter__(self):
        assert(not self.used)
        self.used += 1
        self.games = [ (x,y) for x in self.players for y in self.players if x is not y ]
        return self

    def __iter__(self):
        assert(self.used)
        self.game_counter = 0
        return self

    def __next__(self):
        self.game_counter+= 1
        if len(self.games) == 0:
            raise StopIteration
        (x,y) = self.games.pop()
        rps.say("Game {:03d}: {:} vs {:}".format(self.game_counter,x.name,y.name))
        _g = G(x,y,memory=self.game_memory,steps=self.game_steps)
        with _g as g:
            g.run()
            self.add_score(x,g.s1)\
                    .add_score(y,g.s2)
        self.add_victory(g.winner())

    def __exit__(self,type,value,traceback):
        assert(self.used)
        self.used -= 1
        self.games = None
        self.scores = { p: 0 for p in self.scores }
        self.victories = { p: 0 for p in self.victories }
