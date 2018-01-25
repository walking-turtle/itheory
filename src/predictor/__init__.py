import json,time
# import progressbar

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

class PredictableText:
    def __init__(self,text,lower=0,upper=None):
        if isinstance(text,str):
            self.string=text
        else:
            raise TypeError
        self.lower = lower
        self.upper = upper

    def __iter__(self):
        return Predictor(self)

class Predictor:
    def __init__(self,text):
        self.text = text
        self.string=text.string
        self.stats = Counters()
        self.c = text.lower
        self.l = len(self.string) if text.upper is None else text.upper
        """
        self.bar = progressbar.ProgressBar(max_value=self.l,redirect_stdout=True,\
                widgets=['[',Widget(self),'] ',\
                progressbar.Percentage(),' (',progressbar.Counter(),' of {:d}) '.format(self.l),\
                progressbar.Bar(),' ',progressbar.Timer()])
        """
        self.n = None
        self.δcount = 0
        self.δ = 0.1

    def predict(self,l=None):
        if l is None:
            return None
        """
        Initialize loop:
          * we are looking for the indices of the end of
            patterns of length 1
          * the only element to look at is the last one
            of the pattern (controlled_element)
        """
        pattern_length = 1
        controlled_element = self.string[l-pattern_length]
        end_pattern_indices = set()
        tmp_end_pattern_indices = {\
                i + pattern_length - 1\
                for i in range(l-pattern_length)\
                if self.string[i] is controlled_element\
                }
        while len(tmp_end_pattern_indices):
            del end_pattern_indices
            end_pattern_indices = tmp_end_pattern_indices
            pattern_length += 1
            controlled_element = self.string[l-pattern_length]
            tmp_end_pattern_indices = {\
                    i + pattern_length - 1\
                    for i in range(l-pattern_length)\
                    if self.string[i] is controlled_element\
                    } & end_pattern_indices
        if len(end_pattern_indices):
            return self.string[max(end_pattern_indices)+1]
        return None

    def update_delta(self):
        if self.δcount > 10 and self.δ < 100:
            self.δcount = 0
            self.δ *= 10.
        else:
            self.δcount += 1

    def update_bar(self):
        t = time.time()
        if self.n is None or ((t-self.n) > self.δ):
            self.bar.update(min(self.c,self.l))
            self.n = t
            self.update_delta()

    def __next__(self):
        if self.c > self.l:
            self.text.stats = self.stats.reduce()
            self.text.fullstats = str(self.stats)
            # self.bar.update(self.l)
            raise StopIteration
        p = self.predict(self.c)
        if self.c < self.l:
            x = self.string[self.c]
            if p is None:
                self.stats.unable += 1
            elif p is x:
                self.stats.correct += 1
            else:
                self.stats.wrong += 1
        # self.update_bar()
        self.c += 1
        return p

"""
class Widget:
    def __init__(self,p):
        self.predictor = p

    def __call__(self,*args):
        return '{:08.04f}% correct'.format(100*self.predictor.stats.reduce().correct)
"""

def read_file(f):
    with open(f,'r') if isinstance(f,str) else f as the_input:
        t = PredictableText(the_input.read())
    for _ in t:
        pass
    return t.stats

def test_predictor():
    l = "aabaabcaabaabc"
    p = "xxaxbbaxbbcabc"
    pred = Predictor()
    for x,y in zip(l,p):
        assert(y == 'x' or pred.predict() == y)
        pred.append(x)
