VERB = 0

ROCK = 0
PAPER = 1
SCISSORS = 2

R = ROCK
P = PAPER
S = SCISSORS

_names = {
        R: "Rock",
        P: "Paper",
        S: "Scissors",
        }

_keys = {
        R: "R",
        P: "P",
        S: "S",
        }

_beats = {
        R: S,
        P: R,
        S: P,
        }

_is_beaten_by = {
        y:x for x,y in _beats.items()
        }

def say(*args,**kwargs):
    if VERB:
        print(*args,**kwargs)

def match(a,b):
    assert((a in _names) and (b in _names))
    res = 0 if _beats[a] == b else 1 if _beats[b] == a else 2
    say("{:} {:} {:}".format(
        _names[a],
        "beats" if res == 0 else "is beaten by" if res == 1 else "is equal to",
        _names[b]))
    return res
