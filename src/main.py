#!/usr/bin/env python
import rps

if __name__=='__main__':
    print("Rock: {:}, Paper: {:}, Scissors: {:}".format(rps.R,rps.P,rps.S))

    rps.VERB = 1
    rps.match(rps.R,rps.P)
    rps.match(rps.P,rps.R)
    rps.match(rps.P,rps.S)
    rps.match(rps.S,rps.P)
    rps.match(rps.S,rps.R)
    rps.match(rps.R,rps.S)
