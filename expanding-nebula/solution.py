import numpy as np

# debug = True
debug = False

def solution(x):
    H = len(x)
    W = len(x[0])
    if debug:
        print 'table of dimensions (', H, ",", W, ")"

    outcomes = np.array(x) # easier for indexing than list of lists
    col = dict()

    # Iterate over columns (as they are limited in size compared to the rows)
    for idW in range(W):
        col[idW] = dict() # dictionary with key 2 tuples and value multiplicity
        col_new = dict() # dictionary of list of 2-tuples (idW, idW+1)
        for idH in range(H):
            outcome = outcomes[idH, idW]
            col_new[idH] = []

            if debug:
                print "V: "+str(idW)+"/"+str(W-1)+" - H: "+str(idH)+"/"+str(H-1)+" with outcome "+str(outcome)

            # extend the column by going down one element and calculating the possibilities to get outcome
            if idH == 0:
                for prec in precursors(outcome):
                    col_new[idH].append(tuple((prec[0][0]+(prec[1][0]<<1), prec[0][1]+(prec[1][1]<<1))))
            else:
                for prec in precursors(outcome):
                    if debug:
                        print "    going to try matrix", prec, ": Look at bit", idH
                    for c in col_new[idH-1]:
                        # trim to compatible precursors of element above
                        # print "c", c
                        # print bit_n(c[0],idH) == prec[0][0], "bit_n(c[0],idH+1)", bit_n(c[0],idH), "prec[0][0]", prec[0][0]
                        # print bit_n(c[1],idH) == prec[0][1], "bit_n(c[1],idH+1)", bit_n(c[1],idH), "prec[0][1]", prec[0][1]
                        if (bit_n(c[0],idH) == prec[0][0] and bit_n(c[1],idH) == prec[0][1]): # compatible with above
                            if debug:
                                print "      compatible with column ", format(c[0], '09b'), format(c[1], '09b')
                            col_new[idH].append(tuple((c[0] + (prec[1][0]<<idH+1), c[1] + (prec[1][1]<<idH+1))))
                            if debug:
                                print "      results in", format(c[0] + (prec[1][0]<<idH+1), '09b'), format(c[1] + (prec[1][1]<<idH+1), '09b')
            if debug:
                print "for row", idH, "in column", idW, ":"
                for c in col_new[idH]:
                    print "", c, format(c[0], '09b'), format(c[1], '09b')
            
                    # val = map(int, '{:09b}'.format(c))
                    # print val
            
        # end of current column, now trim to compatible with previous
        if idW == 0:
            for c in col_new[idH]:
                if c[1] in col[0].keys():
                    col[0][c[1]] += 1
                else:
                    col[0][c[1]] = 1
        else:
            for c in col_new[idH]:
                # check if exists in previous col
                if c[0] in col[idW-1].keys(): # compatible with previous column
                    if c[1] in col[idW].keys(): # already in new column
                        col[idW][c[1]] += col[idW-1][c[0]]
                    else:
                        col[idW][c[1]] = col[idW-1][c[0]]

        if debug:
            print 'for entire column', idW, ":"
            for key, value in col[idW].items():
                print "added", key, "(", format(key, '09b'), ") with multiplicity", value

        # ri = raw_input('paused')
    
    return sum(col[idW].values())

def bit_n(val, n):
    # returns bool, can be compared to 1 or 0
    return val & 1<<n != 0

def precursors(outcome):
    if outcome: # True
        # [10]  [01]  [00]  [00]
        # [00], [00], [10], [01]
        return [((1,0),(0,0)),\
            ((0,1),(0,0)),\
            ((0,0),(1,0)),\
            ((0,0),(0,1)),\
            ]
    else: # False
        # [00]  [11]  [01]  [00]  [10]  [01]  [10]  [11]  [01]  [10]  [11]  [11]
        # [00], [00], [01], [11], [10], [10], [01], [01], [11], [11], [10], [11]
        return [((0,0),(0,0)),\
            ((1,1),(0,0)),\
            ((0,1),(0,1)),\
            ((0,0),(1,1)),\
            ((1,0),(1,0)),\
            ((0,1),(1,0)),\
            ((1,0),(0,1)),\
            ((1,1),(0,1)),\
            ((0,1),(1,1)),\
            ((1,0),(1,1)),\
            ((1,1),(1,0)),\
            ((1,1),(1,1)),\
            ]

if __name__ == "__main__":
    # x = [[True]]
    # print(x)
    # print(solution(x))
    # print('')

    # x = [[True, False], [False, False]]
    # print(x)
    # print(solution(x))
    # print('')

    # x = [[True, False, True], [False, True, False], [True, False, True]]
    # print(x)
    # print(solution(x))
    # print('')

    # x = [[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]
    # print(x)
    # print(solution(x))
    # print('')

    x = [[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]
    print(x)
    print(solution(x))
    print('')

    # x = [[True, True], [False, True], [False, False]]
    # print(x)
    # print(solution(x))
    # print('')