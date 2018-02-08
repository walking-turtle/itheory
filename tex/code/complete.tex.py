s = "abaa abbaaaa bba abbaabb aab abb"
c = {
        ' ': '\\_',
        'a': 'a',
        'b': 'b'
}

pl = 1
ce = s[-pl]
epe = set()
tepe = { i+pl-1 for i in range(len(s)-pl) if s[i] is ce }

print("\\only<{:d}->{{\\colorlet{{fboxcolor}}{{noir}}}}".format(4))

print("\\uncover<2->{$\\alpha = 0.75$}\\bigskip\n\n")

header=["\\def\\matchingset{none}"]
tabular=list()
tabular.append("\\begin{tabular}{"+'c'*len(s)+"}")
tabular.append(' & '.join(map(lambda x: '{{\\footnotesize{{}}{:d}}}'.format(x),range(len(s)))) + '\\\\')

def mapping(x):
    i,a = x[:]
    a = c[a]
    fmt = '{:}'
    if i in epe:
        fmt = fmt.format('\\textbf{{\\color{{rouge}}{:}}}')
    elif i in { x-j for x in epe for j in range(1,pl) }:
        fmt = fmt.format('\\textcolor{{bleu}}{{{:}}}')
    if pl == 3 and i in { x+1 for x in epe }:
        fmt = fmt.format('\\cfbox{{{:}}}')
    if len(s) - i <= pl:
        a = a.upper()
        fmt = fmt.format('\\textcolor{{vert}}{{{:}}}')
    return fmt.format(a)

while len(tepe):
    epe = tepe
    ce = s[-pl-1]
    tepe = { i+pl for i in range(len(s)-pl-1) if s[i] is ce } & epe
    if pl >= 3:
        header.append('\\only<{w}>{{\\def\\matchingset{{\\{{{epe}\\}}}}}}'.format(w="1-2" if pl > 3 else "3-",epe=','.join(map(str,sorted(list(epe))))))
    tabular.append('{line}'.format(line='&'.join(map(mapping,enumerate(s))) + '\\\\',epe=str(epe)))
    pl+=1

tabular.append("\\end{tabular}")

print('\n'.join(header))
print('\n'.join(tabular))

print("\\uncover<2->{\\bigskip\n\nMaximum length: $4$. Used length: $4\cdot\\alpha = 3$.}")

print("\\uncover<3->{\\bigskip\n\nSet~=~{\\matchingset}}")

print("\\uncover<4->{{\\bigskip\n\nPrediction given by most frequent pattern: \\textbf{{{:}}}.}}".format('a'))
