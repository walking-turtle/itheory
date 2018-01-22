from players.predict import predict as simple_predict
from sys import stdin,stderr,stdout

def read_file(f):
    with open(f,'rb') if isinstance(f,str) else f as the_input:
        b = the_input.read()
    return b
