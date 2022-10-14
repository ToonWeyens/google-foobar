debug = True

class Node:
   def __init__(self, data=None):
      self.data = data
      self.prev = None

class NodeList:
   def __init__(self):
      self.head = None


def solution(x):
    H = len(x)
    W = len(x[0])
    if debug:
        print 'table of dimensions (', H, ",", W, ")"

    # We will use a linked list to describe the different ways in which each next element
    # can be different, going in the following direction:
    #  [986]
    #  [753]
    #  [421]
    # This will lead to the concept of levels I, as such:
    #  [432]
    #  [321]
    #  [210]
    # This way only the previous level's multiple possibilities are required to calculate the next
    # The level indicator I goes from 0 to H+W-2 where H is the height of the table and W the width
    # For each level we start lower left and and we iterate towards top right
    # If the grid is not squre, we will remove the points that fall outside of it by skipping
    vals = []
    vals.append([])
    vals[0].append(NodeList())
    

    vals = []
    vals.append([None]*3)

    for I in range(H+W-1):
        vals_for_level_I = []
        i = 0
        for idx in range(I+1):
            pos = [H-1-I+idx, W-1-idx]
            if not (pos[0] >= 0 and pos[0] < H and pos[1] >= 0 and pos[1] < W):
                continue
            
            # find valid options for current point
            # the entries in vals store
            # - for each option (first index)
            # - the series of values at the boundary points,
            # where boundary points are defined as in this example for level 4:
            #  [    ]
            #  [   5]
            #  [  34]
            #  [ 12x]
            # For point [3, 0], we need [False,  False,  val(1)]
            # For point [2, 1], we need [val(1), val(2), val(3)]
            # For point [1, 2], we need [val(3), val(4), val(5)]
            # For point [0, 3], we need [val(5), False,  False]
            # as the indices for the valid_res routine are (B, BR, R)
            # Note that False is the absense of a condition
            boundary_args = vals[-1][i:i+4]
            outcome = x[pos[0]][pos[1]]
            vals_for_level_I.append(valid_vals(outcome, *boundary_args))
            if debug:
                print "vals for level", I, "iteration", i, " position", pos, \
                    "outcome value", outcome, "boundary_args", boundary_args
                for val in vals_for_level_I:
                    print "going to print", val
                    print_2D(val)
                    print("")

            quit()
            i += 1
        
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

    for bits in range(0,16):
        if debug:
            print('trying: ', format(bits, '04b'))
        if not BR is None:
            if bit_is_set(bits, 0) != BR:
                continue
        if not B is None:
            if bits_is_set(bits, 1) != B:
                continue
        if not R is None:
            if bit_is_set(bits, 3) != R:
                continue

        # If we reached here, we've satisfied all the side constraints
        # Now we need to look at whether the number matches requirements for res
        bits_bools = [bool(int(bit)) for bit in format(bits, '04b')]
        n_ones = bits_bools.count(True)
        if res: # res = 1
            if n_ones != 1:
                out.append(bits_bools)
                if debug:
                    print ">>", res, "Added:"
                    print_2D(bits_bools)
        else: # res == 0
            if n_ones == 1:
                out.append(bits_bools)
                if debug:
                    print ">>", res, "Added:"
                    print_2D(bits_bools)

    print "going to return", out
    return out

def bit_is_set(bit, idx):
    if bit & (1<<idx):
        return True
    else:
        return False

def print_2D(bit):
    bitStr = str(bit).replace('False', ' ').replace('True', '*')
    print 'bit', bit
    print 'bitstring', bitStr
    print("  ["+bitStr[-2:]+"]")
    print("  ["+bitStr[1::-1]+"]")


if __name__ == "__main__":
    x = [[True, False, True], [False, True, False], [True, False, True]]
    print(x)
    print(solution(x))
    print('')