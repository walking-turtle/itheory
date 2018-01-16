import rps
import players

class RPSGame():
    def __init__(self,p1,p2,memory=0,steps=0):
        assert((isinstance(p1,players.RPSPlayer) and isinstance(p2,players.RPSPlayer)))
        self.used = 0
        self.c = 0
        self.climit = steps-1 if steps > 0 else 20
        self.p1 = p1
        self.b1 = list()
        self.s1 = 0
        self.p2 = p2
        self.b2 = list()
        self.s2 = 0
        memory = int(memory)
        self.mem = - memory if memory > 0 else 0

    def run(self):
        for _ in self:
            pass

    def __iter__(self):
        assert(self.used)
        return self

    def __next__(self):
        if self.c > self.climit:
            raise StopIteration
        c1 = self.p1.play(self.b2)
        c2 = self.p2.play(self.b1)
        if c1 is None or c2 is None:
            if c1 is None:
                rps.say("({:}) forfeit".format(self.p1))
                self.s1 = 0
            if c2 is None:
                rps.say("({:}) forfeit".format(self.p2))
                self.s2 = 0
            self.c = self.climit + 1
            return self.c
        rps.say("({:}) {:} vs {:} ({:})".format(
            self.p1,rps._names[c1],
            rps._names[c2],self.p2))
        match = rps.match(c1,c2)
        if match == 1:
            self.s2 += 1
            rps.say("{:} wins!".format(self.p2))
        elif match == 0:
            self.s1 += 1
            rps.say("{:} wins!".format(self.p1))
        else:
            rps.say("Null!")
        rps.say("({:}) {:} -- {:} ({:})".format(
            self.p1,self.s1,
            self.s2,self.p2))
        self.b1.append(c1)
        self.b2.append(c2)
        self.b1 = self.b1[self.mem:]
        self.b2 = self.b2[self.mem:]
        self.c += 1
        return self.c

    def __enter__(self):
        assert(not self.used)
        self.used += 1
        return self

    def __exit__(self,type,value,traceback):
        if self.c > self.climit:
            if self.s1 > self.s2:
                self.__winner = self.p1
            elif self.s2 > self.s1:
                self.__winner = self.p2
            else:
                self.__winner = None
        self.b1 = list()
        self.b2 = list()
        self.s1 = 0
        self.s2 = 0
        self.c = 0
        self.used -= 1

    def winner(self):
        try:
            w = self.__winner
            if w is not None:
                rps.say("{:} vs {:}: {:} wins!".format(self.p1,self.p2,w))
            else:
                rps.say("{:} vs {:}: null".format(self.p1,self.p2))
            return w
        except:
            raise KeyError("Game did not run.")
