s = "abaa abbaaaa bba abbaabb aab abb"
c = {
        ' ': '{\\_}',
        'a': '{a}',
        'b': '{b}',
        '.': '{.}',
}
m = 3
tree = dict()

print("""
\\tikzstyle{level 1}=[sibling distance=25ex]
\\tikzstyle{level 2}=[sibling distance=9ex]
\\tikzstyle{level 3}=[sibling distance=3.5ex,level distance=5em]
\\begin{tikzpicture}[]
""")

def insert(t,ss):
    n = t
    for y in ss:
        x = c[y]
        if x not in n:
            n[x] = dict()
        n = n[x]
    n['.'] = n.get('.',0)+1

def color(t,u,clr='red',step='1-'):
    for y in u:
        x = c[y]
        if x in t:
            color(t[x],u[y],clr=clr,step=step)
            t[x]['-'] =  t[x].get('-','') + '\\only<{:}>{{\\color{{{:}}}}}'.format(step,clr)

green = { 'a': { 'b': { 'b': {} } } }
blue = { 'a': { 'b': { 'a': {}, 'b': {}, ' ': {} } } }
red = { 'a': { 'b': {} } }

for i in range(len(s)+1):
    for j in range(1,min(i,m)+1):
        insert(tree,s[i-j:i])
color(tree,blue,'bleu','2-')
color(tree,green,'vert','3-')
color(tree,red,'rouge','2-')

def __str__(x,t):
    children = [ x for x in t if x not in ['.','-'] ]
    ret = ""
    if '.' in t:
        label = '{{\\begin{{tabular}}{{c}}{:}\\\\({:d})\\end{{tabular}}}}'.format(x,t['.'])
    else:
        label = '{{{:}}}'.format(x)
    if '-' in t:
        label = '{{{:}{:}}}'.format(t['-'], label)
    ret += "node{:}\n".format(label)
    for y in children:
        ret += "child {\n"
        ret += __str__(y,t[y])
        ret += "}\n"
    return ret

print("\\", end='')
print(__str__('.',tree))
print(";")

print("""
\\end{tikzpicture}
""")
