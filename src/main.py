#!/usr/bin/env python
import rps,sys
from players.copycat import Player as CP
from players.random import Player as RP
from game import RPSGame as G

__test_counter=0
__ok_counter=0
__ko_counter=0

def test_printing(title):
    if len(title)>20:
        title=title[:17]+'...'
    def wrapper(f):
        def g(*args,**kwargs):
            global __test_counter,__ok_counter,__ko_counter
            __test_counter+=1
            print("**** TEST {:03d}: {:20} ****".format(
                __test_counter,
                title[:20]))
            try:
                r = f(*args,**kwargs)
            except Exception:
                r = 1
            print("**** TEST {:03d}: {:20} ****".format(
                __test_counter,
                "FAILED" if r else "SUCCESS"))
            if r:
                __ko_counter+=1
            else:
                __ok_counter+=1
        return g
    return wrapper

@test_printing("Copycat vs Copycat")
def test_copycat(ntests=1000):
    p1 = CP("Cat1")
    p2 = CP("Cat2")
    _g = G(p1,p2,steps=20)
    for _ in range(ntests):
        with _g as g:
            g.run()
        assert(g.winner() is None)
    _g = G(p1,p2,steps=21)
    for _ in range(ntests):
        with _g as g:
            next(g)
            w = g.p1 if (g.s1 > g.s2) else g.p2 if (g.s2 > g.s1) else None
            g.run()
        assert(g.winner() is w)
    return 0

def run_match(p1,p2,ntests=1000,steps=20):
    score = { p1: 0, p2: 0 }
    _g = G(p1,p2,steps=20)
    for _ in range(ntests):
        with _g as g:
            g.run()
        w = g.winner()
        if w is not None:
            score[w]+=1
    s1 = score[p1]
    s2 = score[p2]
    r = abs(s1 - s2)/(s1+s2)
    return r,s1,s2

@test_printing("Random vs Random")
def test_random(ntests=1000):
    p1 = RP("Random1")
    p2 = RP("Random2")
    r,s1,s2 = run_match(p1,p2,ntests=ntests,steps=20)
    return 0 if (s1+s2 == 0 or r < 0.1) else 1

@test_printing("Random vs Copycat")
def test_copyrand(ntests=1000):
    p1 = RP("Random")
    p2 = CP("Copycat")
    r,s1,s2 = run_match(p1,p2,ntests=ntests,steps=20)
    return 0 if (s1+s2 == 0 or r < 0.1) else 1

if __name__=='__main__':
    print("Rock: {:}, Paper: {:}, Scissors: {:}".format(rps.R,rps.P,rps.S))

    rps.VERB = 1
    rps.match(rps.R,rps.P)
    rps.match(rps.P,rps.R)
    rps.match(rps.P,rps.S)
    rps.match(rps.S,rps.P)
    rps.match(rps.S,rps.R)
    rps.match(rps.R,rps.S)

    rps.VERB = 0
    test_copycat()
    test_random()
    test_copyrand()

    if __test_counter == __ok_counter:
        sys.exit(0)
    message = """
TESTS: {:03d}
OK   : {:03d}
KO   : {:03d}
"""
    print(message.format(__test_counter,__ok_counter,__ko_counter))
    sys.exit(1)
