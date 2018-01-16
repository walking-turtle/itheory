#!/usr/bin/env python
import rps
from players.human import Player as HP
from players.copycat import Player as CP
from players.random import Player as RP
from players.predict.simple import Player as SPP
from game import RPSGame as G
from tournament import RPSTournament as T

if __name__=='__main__':
    rps.VERB=1
    human_player = HP()
    simple_predict_player = SPP()
    my_game = G(human_player,simple_predict_player,steps=10)
    with my_game as game:
        game.run()
    print(my_game.winner())
