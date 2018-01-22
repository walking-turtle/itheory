from . import read_file
import sys

try:
    f = sys.argv[1]
except IndexError:
    f = sys.stdin

print(read_file(f))
