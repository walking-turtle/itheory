from . import read_file
import sys

index=1
try:
    a = float(sys.argv[index])
    index+=1
except (IndexError,ValueError,TypeError):
    a = 1.
try:
    f = sys.argv[index]
    index+=1
except IndexError:
    f = sys.stdin

print(read_file(f,alpha=a))
