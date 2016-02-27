#coding: utf-8
from lr2ghost import judge, cndict

def ghost_to_hist(ghost_str):
    '''
    convert LR2 ghost string ([0-9@A-Za-z]*)
    to string with intermediate expression ([@A-E]^*)

    in intermediate expression, each character means
        E : PG = perfect great
        D : GR = great
        C : GD = good
        B : BD = bad
        A : PR = overlooked poor
        @ : PR = extra poor
    and n-th character without '@' expresses the judge of n-th note
    '''

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

            j = cndict[c]
            hist += j[0]
            loop = judge[j[1]]
            num = j[2]

    return hist

if __name__ == '__main__':
    test = ghost_to_hist('Iam@GNQGonGithubZ')
    print test
    print "length:", len(test), "total:", len(test)-test.count('@')
    for c in 'EDCBA@':
        print test.count(c),
    pass
