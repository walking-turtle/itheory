#!/usr/bin/env python
import rps,sys
from players.copycat import Player as CP
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
    for _ in range(1000):
        with _g as g:
            g.run()
        assert(g.winner() is None)
    _g = G(p1,p2,steps=21)
    for _ in range(1000):
        with _g as g:
            next(g)
            w = g.p1 if (g.s1 > g.s2) else g.p2 if (g.s2 > g.s1) else None
            g.run()
        assert(g.winner() is w)
    return 0

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

    if __test_counter == __ok_counter:
        sys.exit(0)
    message = """
TESTS: {:03d}
OK   : {:03d}
KO   : {:03d}
"""
    print(message.format(__test_counter,__ok_counter,__ko_counter))
    sys.exit(1)
