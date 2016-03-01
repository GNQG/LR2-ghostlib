#coding: utf-8
import re

import ghostinfo as ghi


PG,GR,GD,BD,PR,PR_EX = ghi.judge
GRPG = ghi.GRPG


def ghost_to_hist(ghost_str):
    '''
    convert LR2 ghost string (^([@A-Ya-z][0-9@A-Ya-z]*)?(ZZ?)$)
    to string with intermediate expression (^[ghostinfo.judge]^*(ZZ?)$)

    in intermediate expression, each character in lr2ghost.judge means
        E : PG = perfect great,
        D : GR = great,
        C : GD = good,
        B : BD = bad,
        A : PR = overlooked poor,
        @ : PR_EX = extra poor,
    and n-th character without '@' expresses the judge of n-th note
    '''

    re_gh = ghi.re_validghost.match(ghost_str)
    if re_gh is None:
        raise Exception('Invalid ghost string.')

    hist = ''
    num = 0
    loop = ''

    for c in ghost_str:
        if '0' <= c <= '9':
            num = num*10+int(c)
        else:
            if num:
                hist += loop*int(num)
            else:
                hist += loop

            if c == 'Z':break

            j = ghi.ghchar_to_judge[c]
            hist += j[0][:-1]
            loop  = j[0][-1]
            num = j[1]

    return hist + re_gh.group(2)


def hist_to_ghost(hist_str):
    '''
    convert note-judge map string (^[ghostinfo.judge]*ZZ?$)
    to LR2 ghost string (^([@A-Ya-z][0-9@A-Ya-z]*)?(ZZ?)$)
    '''

    re_expr = ghi.re_validexpr.match(hist_str)
    if re_expr is None:
        raise Exception('Invalid history string.')

    hist_split = ghi.re_PR_EX.split(re_expr.group(1))
    hist_split.append('')
    ghost = ''
    head = ''
    loop = 0

    for i in range(0,len(hist_split),2):
        hstr = hist_split[i] # [A-E]*

        while hstr:
            c0 = hstr[0]
            c1 = hstr[1:2]
            head = c0+c1
            if c0 == c1:
                match_loop = ghi.re_loop[c0].match(hstr)
                loop = len(match_loop.group())
                ghost += ghi.genc(c0,loop)
                hstr = hstr[loop:]
            elif (not c1) or c0 == BD or head == PG+GR:
                # '[A-E]$', '[B.].', 'ED' : not 'O'
                ghost += c0
                hstr = hstr[1:]
            else: # head = [ACDE][ABCDE], c0 != c1
                if head == GRPG: # q or r-z or X
                    c3 = hstr[2:4]
                    if c3 == GRPG: # 'DEDE...' : q
                        head += GRPG
                    elif c3[:1] != PG: # DE -> 'X'
                        ghost += 'X'
                        hstr = hstr[2:]
                        continue
                    #else: # DEE... : r-z
                    #    pass

                match_loop = ghi.re_loop[head[-1:]].match(hstr[len(head)-1:])
                loop = len(match_loop.group())
                ghost += ghi.genc(head,loop)
                hstr = hstr[len(head)-1+loop:]

        PREXnum = len(hist_split[i+1])

        if PREXnum <= 1:
            ghost += PR_EX*PREXnum
        else:
            ghost += PR_EX+str(PREXnum)


    return ghost + re_expr.group(2)


if __name__ == '__main__':
    teststr = 'HBHsS6Et9B2GT@TEs0THr1YEuSg2gBIqSEsUPSjQXYbYXlmhnjBTPPng2Xm2cBEq2cB4hEXiGcPQggcRjRgBShdBY4BdBdBicoF1sBUh2hEZ'
    testghost = ghost_to_hist(teststr)
    print 'ghost_to_hist(%s) = %s' % (teststr,testghost,)
    print "length:", len(testghost), "total:", len(testghost)-testghost.count(ghi.judge[5])
    for c in ghi.judge:
        print testghost.count(c),
    print
    print 'hist_to_ghost(%s) = %s' % (testghost,hist_to_ghost(testghost),)

    pass
