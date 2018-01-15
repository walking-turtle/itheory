#!/usr/bin/env python
import rps
from players.human import Player as HP
from game import RPSGame as G

if __name__=='__main__':
    rps.VERB=1
    p1 = HP("Player1")
    p2 = HP("Player2")
    with G(p1,p2,memory=3,steps=6) as g:
        g.run()
    g.winner()
