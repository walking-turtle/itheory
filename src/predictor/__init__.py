import json
import progressbar

class SafeDict(dict):
    def __getitem__(self,key):
        return dict.__getitem__(self,''.join(key))
    def __setitem__(self,key,val):
        return dict.__setitem__(self,''.join(key),val)
    # def __missing__(self,key):
        # return 0

class Counters(object):
    def __init__(self):
        pass
    def __getattribute__(self,x):
        try:
            return object.__getattribute__(self,x)
        except AttributeError:
            return 0
    def __str__(self):
        return json.dumps(self.__dict__)

    def reduce(self):
        dup = type(self)()
        t = sum(map(lambda x: x[1], self.__dict__.items()))
        for x,y in self.__dict__.items():
            setattr(dup,x,y/t)
        return dup

class Predictor:
    def __init__(self):
        self.string=list()
        self.substrings=SafeDict()
        self.stats=Counters()
        pass
    def append(self,x):
        self._process_last_char()
        self.string.append(x)
        return self
    def _process_last_char(self):
        l = len(self.string)
        for i in range(l):
            self.substrings[self.string[i:l]]=l
        return self
    def predict(self):
        l = len(self.string)
        for i in range(1,l):
            ss = self.string[i:l]
            if ''.join(ss) in self.substrings:
                return self.string[self.substrings[ss]]
        return None
    def stat_append(self,x):
        p = self.predict()
        if p is None:
            self.stats.unable += 1
        elif p == x:
            self.stats.correct += 1
        else:
            self.stats.wrong += 1
        return self.append(x)

def read_file(f):
    pred = Predictor()
    with open(f,'r') if isinstance(f,str) else f as the_input:
        chars = list(the_input.read())
    bar = progressbar.ProgressBar()
    for i in bar(range(len(chars))):
        pred.stat_append(chars[i])
    return pred.stats.reduce()

def test_predictor():
    l = "aabaabcaabaabc"
    p = "xxaxbbaxbbcabc"
    pred = Predictor()
    for x,y in zip(l,p):
        assert(y == 'x' or pred.predict() == y)
        pred.append(x)
