import json,time,zlib
import progressbar

class TreeData:
    def __init__(self):
        self.tree = dict()

    def run(self,*args,**kwargs):
        raise NotImplementedError

    def add(self,*args,**kwargs):
        raise NotImplementedError

    def get(self,sequence):
        raise NotImplementedError

    def parseiter(self,data):
        raise NotImplementedError

    def parse(self,data):
        for _ in self.parseiter(data):
            pass

    def fparse(self,filename):
        with open(filename,'r') as stream:
            self.parse(stream.read())

    def dump(self,stream):
        json.dump(self.tree,stream,separators=(',',':'))

    def sdump(self):
        return json.dumps(self.tree,separators=(',',':'))

    def fdump(self,filename):
        with open(filename,'w') as stream:
            self.dump(stream)

    def zdump(self,filename):
        data = self.sdump().encode()
        with open(filename,'wb') as stream:
            stream.write(zlib.compress(data,9))

    def post_load_hook(self):
        raise NotImplementedError

    def load(self,stream):
        new = json.load(stream)
        del self.tree
        self.tree = new
        self.post_load_hook()

    def sload(self,string):
        new = json.loads(string)
        del self.tree
        self.tree = new
        self.post_load_hook()

    def fload(self,filename):
        with open(filename,'r') as stream:
            self.load(stream)

    def zload(self,filename):
        with open(filename,'rb') as stream:
            data = stream.read()
        self.sload(zlib.decompress(data).decode())

    @classmethod
    def merge(cls,src=dict(),dst=dict()):
        raise NotImplementedError

    def update(self,other):
        type(self).merge(src=other.tree,dst=self.tree)

    def iteritems(self,value=None,depth=None):
        if value is None or depth is None:
            value = self.tree
            depth = 0
        for c in filter(lambda x: x!='__',value):
            yield c,value[c],depth
            for k,v,d in self.iteritems(value=value[c],depth=depth+1):
                yield k,v,d

    def depth(self):
        return max(d for k,v,d in self.iteritems())

    def __len__(self):
        return sum(1 for _ in self.iteritems())

    def __walk(self,key='.',value=None,depth=None,last=1,label=None):
        if value is None or depth is None:
            value = self.tree
            depth = -1
        yield key,label,depth,last
        children = list(filter(lambda x: x!='__', value))
        for c in children[:-1]:
            for k,lb,d,l in self.__walk(key=c,value=value[c],\
                    depth=depth+1,last=0,label=value[c].get('__',None)):
                yield k,lb,d,l
        for c in children[-1:]:
            for k,lb,d,l in self.__walk(key=c,value=value[c],\
                    depth=depth+1,last=1,label=value[c].get('__',None)):
                yield k,lb,d,l

    def show(self):
        res = ''
        prefixes = list()
        for key,label,depth,last in self.__walk():
            if depth >= 0:
                while depth >= len(prefixes):
                    prefixes.append('|  ')
                if last:
                    prefixes[depth] = '   '
                else:
                    prefixes[depth] = '|  '
                res += ''.join(prefixes[:depth])
                res += '└─ ' if last else '├─ '
                res += '{:}'.format(key)
                if label is not None:
                    res += ' ({:})'.format(label)
            else:
                res += key
            res += '\n'
        print(res)

class SubStrings(TreeData):
    def __init__(self,cache = 5):
        super(SubStrings,self).__init__()
        self.cache = cache

    def add(self,sequence):
        node = self.tree
        for x in sequence:
            if x not in node:
                node[x] = dict()
            node = node[x]
        node['__'] = node.get('__',0)+1

    def parseiter(self,data):
        last = len(data)
        step = last//100
        for i in range(last):
            for j in range(min(self.cache,i)):
                self.add(data[i-j-1:i])
            if i%step == 1:
                yield i

    @classmethod
    def merge(cls,src=dict(),dst=dict()):
        for k,v in src.items():
            if k == '__':
                dst['__'] = dst.get('__',0) + v
                continue
            if k not in dst:
                dst[k] = dict()
            cls.merge(src=v,dst=dst[k])

    def post_load_hook(self):
        self.cache = max(self.cache,self.depth()+1)

class Predictions(TreeData):
    def __init__(self,cache = 5):
        super(Predictions,self).__init__()
        self.cache = cache

    @classmethod
    def from_substrings(cls,substrings):
        self = cls(cache = substrings.cache)
        path = list()
        for key,value,depth in substrings.iteritems():
            while depth >= len(path):
                path.append('xxx')
            path[depth] = key
            children = list(filter(lambda x: x!='__' and '__' in value[x], value))
            children.sort()
            if children:
                maximum, best_child = 0, 'xxx'
                for child in children:
                    if value[child]['__'] > maximum:
                        best_child = child
                        maximum = value[child]['__']
                self.add(path[:depth+1], best_child)
        return self

    def add(self,sequence,prediction):
        node = self.tree
        for x in reversed(sequence):
            if x not in node:
                node[x] = dict()
            node = node[x]
        node['__'] = prediction

    def get(self,sequence):
        node = self.tree
        for x in sequence[::-1]:
            if x not in node:
                break
            node = node[x]
        return node.get('__',None)

    def run(self,text,verb=0):
        correct = 0
        total = len(text)
        if verb:
            bar = progressbar.ProgressBar(maxval=total).start()
            step = total//100
        for i in range(total):
            if text[i] == self.get(text[max(0,i-self.cache):i]):
                correct += 1
            if verb and (i%step == 1):
                bar.update(i)
        if verb:
            bar.finish()
        return correct/total,total

    def post_load_hook(self):
        self.cache = max(self.cache,self.depth()+2)

