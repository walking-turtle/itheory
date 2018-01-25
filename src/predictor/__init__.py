import json,time

class SubStrings:
    def __init__(self):
        self.t = dict()

    def add_string(self,s):
        c = self.t
        for x in s:
            if x not in c:
                c[x] = dict()
            c = c[x]
        c['__'] = c.get('__',0)+1

    def iteritems(self,value=None,depth=None):
        if value is None or depth is None:
            value = self.t
            depth = 0
        for c in filter(lambda x: x!='__',value):
            yield c,value[c],depth
            for k,v,d in self.iteritems(value=value[c],depth=depth+1):
                yield k,v,d

    def walk(self,node,value='.',depth=-1,last=1,count=None):
        yield value,count,depth,last
        children = [ k for k in node if k != '__' ]
        for c in children[:-1]:
            for v,c,d,l in self.walk(node[c],value=c,depth=depth+1,last=0,count=node[c].get('__',None)):
                yield v,c,d,l
        for c in children[-1:]:
            for v,c,d,l in self.walk(node[c],value=c,depth=depth+1,last=1,count=node[c].get('__',None)):
                yield v,c,d,l

    def show(self):
        res = ''
        prefixes = list()
        for value,count,depth,last in self.walk(self.t):
            if depth >= 0:
                while depth >= len(prefixes):
                    prefixes.append('|  ')
                if last:
                    prefixes[depth] = '   '
                else:
                    prefixes[depth] = '|  '
                res += ''.join(prefixes[:depth]) + ('└' if last else '├') + '─ ' + '{:}'.format(value) + (' ({:d})'.format(count) if count is not None else '') + '\n'
            else:
                res += value + '\n'
        print(res)

    def dump(self,s):
        json.dump(self.t,s,separators=(',',':'))

    def load(self,s):
        self.t = json.load(s)

    def update(self,SS):
        type(self).merge(src=SS.ss,dst=self.ss)

    @classmethod
    def merge(cls,src=dict(),dst=dict()):
        for k,v in src.items():
            if k == '__':
                dst['__'] = dst.get('__',0) + v
                continue
            if k not in dst:
                dst[k] = dict()
            cls.merge(src=v,dst=dst[k])

class Learner:
    default_buffer_size = 5
    def __init__(self,buffer_size=None):
        if buffer_size is None:
            buffer_size = type(self).default_buffer_size
        self.ss = SubStrings()
        self.bs = buffer_size

    @classmethod
    def from_backup(cls,filename,*args,**kwargs):
        self = cls(*args,**kwargs)
        with open(filename,'r') as f:
            return self.load(f)

    def save_backup(self,filename):
        with open(filename,'w') as f:
            return self.dump(f)

    def read_text(self,data):
        for i in range(len(data)):
            for j in range(min(self.bs,i)):
                self.ss.add_string(data[i-j-1:i])
        # for i in range(len(data)-self.bs):
            # self.ss.add_string(data[i:i+self.bs])
        return self

    def read_file(self, filename):
        if not isinstance(filename,str):
            raise TypeError("<filename> should be a string")
        with open(filename,'r') as f:
            return self.read_text(f.read())

    def dump(self,s):
        self.ss.dump(s)
        return self
    def load(self,s):
        self.ss.load(s)
        return self

class Predictions:
    def __init__(self):
        self.t = dict()

    def add_prediction(self,s,p):
        c = self.t
        for x in reversed(s):
            if x not in c:
                c[x] = dict()
            c = c[x]
        c['__'] = p

    def get_prediction(self,s):
        c = self.t
        for x in s[::-1]:
            if x not in c:
                break
            c = c[x]
        return c.get('__',None)

    def walk(self,node,value='.',depth=-1,last=1,count=None):
        yield value,count,depth,last
        children = [ k for k in node if k != '__' ]
        for c in children[:-1]:
            for v,c,d,l in self.walk(node[c],value=c,depth=depth+1,last=0,count=node[c].get('__',None)):
                yield v,c,d,l
        for c in children[-1:]:
            for v,c,d,l in self.walk(node[c],value=c,depth=depth+1,last=1,count=node[c].get('__',None)):
                yield v,c,d,l

    def dump(self,s):
        json.dump(self.t,s,separators=(',',':'))

    def load(self,s):
        self.t = json.load(s)

    def show(self):
        res = ''
        prefixes = list()
        for value,count,depth,last in self.walk(self.t):
            if depth >= 0:
                while depth >= len(prefixes):
                    prefixes.append('|  ')
                if last:
                    prefixes[depth] = '   '
                else:
                    prefixes[depth] = '|  '
                res += ''.join(prefixes[:depth]) + ('└' if last else '├') + '─ ' + '{:}'.format(value) + (' ({:})'.format(count) if count is not None else '') + '\n'
            else:
                res += value + '\n'
        print(res)

class Predictor:
    def __init__(self):
        self.ps = Predictions()

    @classmethod
    def from_substrings(cls,ss,*args,**kwargs):
        self = cls(*args,**kwargs)
        path = list()
        for k,v,d in ss.iteritems():
            while d >= len(path):
                path.append('xxx')
            path[d] = k
            children = list(filter(lambda x: x!='__' and '__' in v[x], v))
            children.sort()
            if len(children):
                # print(''.join(path[:d+1]) + ' has leafs')
                # print({ c:v[c]['__'] for c in children })
                m,c = 0,'xxxxx'
                for i in children:
                    if v[i]['__'] > m:
                        c = i
                        m = v[i]['__']
                # print('best leaf is {:}'.format(c))
                self.ps.add_prediction(path[:d+1],c)
        return self

    def predict(self,s):
        return self.ps.get_prediction(s)

    def read_text(self,text):
        c = 0
        d = 0
        for i in range(len(text)):
            d += 1
            if text[i] == self.ps.get_prediction(text[max(0,i-10):i]):
                c += 1
            if i % 5000 == 1:
                print('{:.4g}%'.format(100*(c/d)))

    @classmethod
    def from_backup(cls,filename,*args,**kwargs):
        self = cls(*args,**kwargs)
        with open(filename,'r') as f:
            return self.load(f)

    def save_backup(self,filename):
        with open(filename,'w') as f:
            return self.dump(f)

    def dump(self,s):
        self.ps.dump(s)
        return self

    def load(self,s):
        self.ps.load(s)
        return self
