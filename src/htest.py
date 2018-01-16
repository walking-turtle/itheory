#!/usr/bin/env python
import rps
# from players.human import Player as HP
from players.copycat import Player as CP
from players.random import Player as RP
# from game import RPSGame as G
from tournament import RPSTournament as T

if __name__=='__main__':
    rps.VERB=1
    ps = [(RP,1),(CP,2)]
    _t = T(steps=3)
    for p in ps:
        _t.add_players(*p)
    with _t as t:
        t.run()
