from difflib import restore


debug = True

def solution(x):
    H = len(x)
    W = len(x[0])
    if debug:
        print 'table of dimensions (', H, ",", W, ")"
    # val[0] = []

    # define the intervals, e.g.
    #  [986]
    #  [753]
    #  [421]
    # will have multiple levels:
    #  [432]
    #  [321]
    #  [210]
    # and only the previous level's multiple possibilities are required
    # to calculate the next
    # The level indicator I goes from 0 to H+W-2 where H is the height of the table and W the width
    # For each level we start at point [max(0,H-1-I), W-1]
    # and we iterate for i going from 0 until min(I,W,H)-1
    for I in range(H+W-1):
        startPos = [max(0, H-1-I), W-1]
        if debug:
            print "for level", I, "starting position", startPos
        for i in range(min(I, W, H)):
            pos = [startPos[0]+i, startPos[1]-i]
            if debug:
                print 'Level', I, ", iteration", i, "position", pos
        
    # vals = valid_vals(0)
    # for val in vals:
    #     print_2D(val)
    #     print("")
    return

def valid_vals(res, B=None,BR=None,R=None):
    # valid values for result res, optionally taking into account
    #   B: value below
    #   BR: Value below right
    #   R: Value right
    # res is a list containing lists of 3 values: (BL, TL, TR) from
    #   [TL TR]
    #   [BL BR]
    # BR is not returned as it is unnecessary
    debug = False
    out = []

    for bit in range(0,16):
        # if debug:
            # print('trying: ', format(bit, '04b'))
        if not BR is None:
            if bit_is_set(bit, 0) != BR:
                continue
        if not B is None:
            if bit_is_set(bit, 1) != B:
                continue
        if not R is None:
            if bit_is_set(bit, 3) != B:
                continue
        
        # If we reached here, we've satisfied all the side constraints
        # Now we need to look at whether the number matches requirements for res
        n_ones = format(bit, '04b').count("1")
        if res == 0:
            if n_ones != 1:
                out.append(bit)
                if debug:
                    print ">>", res, "Added:"
                    print_2D(bit)
        else: # res == 1
            if n_ones == 1:
                out.append(bit)
                if debug:
                    print ">>", res, "Added:"
                    print_2D(bit)

    return out

def bit_is_set(bit, idx):
    if bit & (1<<idx):
        return True
    else:
        return False

def print_2D(bit):
    bitStr = str(format(bit, '04b')).replace('0', ' ').replace('1', '*')
    print("  ["+bitStr[-2:]+"]")
    print("  ["+bitStr[1::-1]+"]")


if __name__ == "__main__":
    x = [[True, False, True], [False, True, False], [True, False, True]]
    print(x)
    print(solution(x))
    print('')