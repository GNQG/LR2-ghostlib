#coding: utf-8
import re


# for enc/dec

judge = [
    'E', # PG = perfect great
    'D', # GR = great
    'C', # GD = good
    'B', # BD = bad
    'A', # PR = overlooked poor
    '@'  # PR = extra poor
]

PG,GR,GD,BD,PR,PR_EX = judge
GRPG = GR+PG


# for dec

re_validghost = re.compile(r'^([@A-Ya-z][0-9@A-Ya-z]*)?(ZZ?)$')

ghchar_to_judge = {}

for c in '@ABCDE':
    ghchar_to_judge[c] = (judge[69-ord(c)], 0 )
for c in 'FGHIJKLMN':
    ghchar_to_judge[c] = (PG, ord(c)-69)
for c in 'OPQR':
    ghchar_to_judge[c] = (PG+judge[ord(c)-78], 0)
for c in 'STUVW':
    ghchar_to_judge[c] = (GR, ord(c)-81)

ghchar_to_judge['X'] = (GR+PG, 0)
ghchar_to_judge['Y'] = (GR+GD, 0)
ghchar_to_judge['a'] = (GR+BD, 0)
ghchar_to_judge['b'] = (GR+PR, 0)

# 'Z' is not defined because it means end of ghost string

for c in 'cdef':
    ghchar_to_judge[c] = (GD, ord(c)-97)

ghchar_to_judge['g'] = (GD+PG, 0)
ghchar_to_judge['h'] = (GD+GR, 0)
ghchar_to_judge['i'] = (GD+BD, 0)
ghchar_to_judge['j'] = (GD+PR, 0)

for c in 'klmn':
    ghchar_to_judge[c] = (PR+judge[110-ord(c)], 0 )
for c in 'op':
    ghchar_to_judge[c] = (PR, ord(c)-109)

ghchar_to_judge['q'] = (GRPG+GRPG, 0)

for c in 'rstuvwxyz':
    ghchar_to_judge[c] = (GRPG, ord(c)-113)


# for enc

re_validexpr  = re.compile(r'^([%s]*)(ZZ?)$' % ''.join(judge))
re_PR_EX = re.compile(r'(@+)')

re_loop = {} # re_loop[X] : /^X+/
for c in judge:
    re_loop[c] = re.compile(r'^%s+' % c)

PRdict   = { str(i) : chr(109+i) for i in range(2,4) } # o-p
GDdict   = { str(i) : chr(97+i)  for i in range(2,6) } # c-f
GRdict   = { str(i) : chr(81+i)  for i in range(2,7) } # S-W
PGdict   = { str(i) : chr(69+i)  for i in range(1,10)} # F-N
GRPGdict = { str(i) : chr(113+i) for i in range(1,10)} # r-z

judge_to_numdict = {
    PR : PRdict,
    GD : GDdict,
    GR : GRdict,
    PG : PGdict,
    GRPG : GRPGdict
}

judge_to_ghchar = {
    PR+BD : 'k', PR+GD : 'l', PR+GR : 'm', PR+PG : 'n',
    GD+PR : 'j', GD+BD : 'i', GD+GR : 'h', GD+PG : 'g',
    GR+PR : 'b', GR+BD : 'a', GR+GD : 'Y',
    PG+PR : 'R', PG+BD : 'Q', PG+GD : 'P', 
    GRPG+GRPG : 'q',
}

def genc(head, loop):
    Ndict = judge_to_numdict.get(head)
    strlp = str(loop)
    numhead = strlp[0]
    if Ndict and Ndict.get(numhead) :
        return Ndict[numhead] + strlp[1:]
    elif loop == 1:
        return judge_to_ghchar.get(head,head)
    else:
        return judge_to_ghchar.get(head,head) + strlp
