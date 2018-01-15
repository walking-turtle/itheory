#!/usr/bin/env python
import rps
from players.human import Player as HP
from players.copycat import Player as CP
from game import RPSGame as G

if __name__=='__main__':
    rps.VERB=1
    p1 = CP("Cat1")
    p2 = CP("Cat2")
    with G(p1,p2,memory=3,steps=6) as g:
        g.run()
    g.winner()
