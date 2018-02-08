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

print("\\only<{:d}->{{\\colorlet{{fboxcolor}}{{noir}}}}".format(5))

header=["\\def\\matchingset{none}"]

tabular=["\\begin{tabular}{"+'c'*len(s)+"}"]
tabular.append(' & '.join(map(lambda x: '{{\\footnotesize{{}}{:d}}}'.format(x),range(len(s)))) + '\\\\')

def mapping(x):
    i,a = x[:]
    a = c[a]
    fmt = '{:}'
    if i in epe:
        fmt = fmt.format('\\textbf{{\\color{{rouge}}{:}}}')
    elif i in { x-j for x in epe for j in range(1,pl) }:
        fmt = fmt.format('\\textcolor{{bleu}}{{{:}}}')
    if len(tepe) == 0 and i in { x+1 for x in epe }:
        fmt = fmt.format('\\cfbox{{{:}}}')
    if len(s) - i <= pl:
        a = a.upper()
        fmt = fmt.format('\\textcolor{{vert}}{{{:}}}')
    return fmt.format(a)

while len(tepe):
    epe = tepe
    ce = s[-pl-1]
    tepe = { i+pl for i in range(len(s)-pl-1) if s[i] is ce } & epe
    header.append('\\only<{pl:d}->{{\\def\\matchingset{{\\{{{epe}\\}}}}}}'.format(pl=pl,epe=','.join(map(str,sorted(list(epe))))))
    tabular.append('\\uncover<{pl:d}->{{{line}}}'.format(pl=pl,line='&'.join(map(mapping,enumerate(s))) + '\\\\',epe=str(epe)))
    pl+=1

tabular.append("\\end{tabular}")

print('\n'.join(header))
print('\n'.join(tabular))

print("\\bigskip\n\nSet~=~{\\matchingset}")

print("\\bigskip\n\n\\uncover<{pl:d}->{{Prediction given by most recent pattern: \\textbf{{{pred}}}.}}".format(pl=pl,pred=s[max(epe)+1]))

print("\\colorlet{fboxcolor}{white}")
