from players.predict import predict as simple_predict
from sys import stdin,stderr,stdout

def read_file():
    c=0
    for l in stdin.readlines():
        c+=1
    stderr.write('{:d}\n'.format(c))
