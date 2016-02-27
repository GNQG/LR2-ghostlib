#coding: utf-8

judge = ['E','D','C','B','A','@']
'''
    E : PG = perfect great
    D : GR = great
    C : GD = good
    B : BD = bad
    A : PR = overlooked poor
    @ : PR = extra poor
'''

cndict = {}

for c in '@ABCDE':
    cndict[c] = ('', 69-ord(c), 0 )
for c in 'FGHIJKLMN':
    cndict[c] = ('', 0, ord(c)-69 )
for c in 'OPQR':
    cndict[c] = (judge[0], ord(c)-78, 0)
for c in 'STUVW':
    cndict[c] = ('', 1, ord(c)-81 )

cndict['X'] = (judge[1], 0, 0)
cndict['Y'] = (judge[1], 2, 0)
cndict['a'] = (judge[1], 3, 0)
cndict['b'] = (judge[1], 4, 0)

# 'Z' is not defined because it means end of ghost string

for c in 'cdef':
    cndict[c] = ('', 2, ord(c)-97 )

cndict['g'] = (judge[2], 0, 0)
cndict['h'] = (judge[2], 1, 0)
cndict['i'] = (judge[2], 3, 0)
cndict['j'] = (judge[2], 4, 0)

for c in 'klmn':
    cndict[c] = (judge[4], 110-ord(c), 0 )
for c in 'op':
    cndict[c] = ('', 4, ord(c)-109)

cndict['q'] = (judge[1]+judge[0]+judge[1], 0, 0)

for c in 'rstuvwxyz':
    cndict[c] = (judge[1], 0, ord(c)-113 )
