import numpy as np

debug = True

class Node:
    def __init__(self, data, level_index=None):
        self.data = data
        self.level_index = level_index
        self.prev = None
    
    def __repr__(self):
        repr_str = "Node with value "+str(self.data)
        if self.level_index is None:
            repr_str += " and no level index"
        else:
            repr_str += " and level index "+str(self.level_index)
        return repr_str

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
    #  [875]
    #  [642]
    #  [310]
    # This will lead to the concept of levels I, as such:
    #  [432]
    #  [321]
    #  [210]
    # This way only the previous level's multiple possibilities are required to calculate the next
    # 
    # The level indicator I goes from 0 to H+W-2 where H is the height of the table and W the width
    # For each level we start lower left and and we iterate towards top right
    # If the grid is not squre, we will remove the points that fall outside of it by skipping

    vals = [] # will contain an entry for every level
    outcomes = np.array(x) # easier for indexing than list of lists

    # helper dict to convert position (2D) to element index (1D)
    pos2el = np.zeros((H+1, W+1), dtype=np.int8)
    for h in range(H+1): # extra column with wildcard
        pos2el[h,W] = -1
    for w in range(W): # extra row with wildcard
        pos2el[H,w] = -1

    el_idx = -1 # will ad 1 at beginning of loop
    for I in range(H+W-1):
        if debug:
            print ">> reached level", I
        
        for idx in range(I+1):
            pos = [H-1-I+idx, W-1-idx]
            if (pos[0] >= 0 and pos[0] < H and pos[1] >= 0 and pos[1] < W):
                el_idx  += 1
            else:
                continue # skip this one as it's outside the grid

            if debug:
                print "> within level", I, "at element", el_idx

            # update helper functions
            pos2el[pos[0],pos[1]] = el_idx
            if debug:
                print "pos2el:", pos2el

            # current outcome value
            outcome = outcomes[pos[0],pos[1]]
            
            # find B, D, R of current point
            # If we subtract the current element index, this shows how far back we have to go
            ind_B  = pos2el[pos[0]+1,pos[1]]
            ind_D = pos2el[pos[0]+1,pos[1]+1]
            ind_R  = pos2el[pos[0],  pos[1]+1]
            if debug:
                print "element index of B: ", ind_B
                print "element index of D: ", ind_D
                print "element index of R: ", ind_R
            
            # Iterate over all possitilibites of this level i
            vals.append([]) # a list of possible values of this level, linking back to the previous level

            if el_idx == 0: # Special case: first level, no previous thing to build on
                Node_B = Node(-1, None) # wildcard
                Node_D = Node(-1, None) # wildcard
                Node_R = Node(-1, None) # wildcard
                vals_for_0 = valid_vals(outcome, Node_B, Node_D, Node_R)
                print "vals for level 0", vals_for_0
                vals[-1].append(vals_for_0)
                print "!!!!!!!!! NEED TO PASS THE ENTIRE BLOCK AS IT AFFECTS THE NEXT VALUES"
            else:
                for prev_val in vals[el_idx-1]: # not first case, we do have previous things to build on
                    # get the neighbor Nodes
                    # As we haven't yet calculated vals for this level, we pass the previous level
                    # A Node contains its own element index, so the comparison will work fine like this
                    Node_B = get_neighbor(vals[-1], ind_B)
                    Node_D = get_neighbor(vals[-1], ind_D)
                    Node_R = get_neighbor(vals[-1], ind_R)

                    print "got here with Node_B", Node_B
                    print "got here with Node_D", Node_D
                    print "got here with Node_R", Node_R

                    if debug:
                        print "vals for level", I, "element index", el_idx, " position", pos, \
                            "outcome value", outcome, "boundary_args", boundary_args
                        for val in vals_for_level_I:
                            print "going to print", val
                            print_2D(val)
                            print("")

            print "ARTIFICIAL QUIT!!!!!!!!"
            quit()
        
    return

def get_neighbor(vals_list, ind_neighbor):
    if debug:
        print "index of neighbor:", ind_neighbor
    if ind_neighbor < 0:
        return Node(-1, None) # -1 means wildcard
    else:
        print "NOT YET IMPLEMENTED!!!!!!!"
        pass

def valid_vals(res, B,D,R):
    # valid values for result res, taking into account
    #   B: value below
    #   D: Value below right ("diagonal")
    #   R: Value right
    # B, D and R are nodes, res is a boolean, and the output is a list of Nodes
    # containing the values TL from
    #   [TL TR]
    #   [BL BR]
    # debug = False
    out = []

    for bits in range(0,16):
        if debug:
            print('trying: ', format(bits, '04b'))

        # Satisfy all the side constraints
        if D.data >= 0:
            if bit_is_set(bits, 0) != D.data:
                continue
        if B.data >= 0:
            if bit_is_set(bits, 1) != B.data:
                continue
        if R.data >= 0:
            if bit_is_set(bits, 3) != R.data:
                continue

        # Look at whether the number matches requirements for res
        bits_bools = [bool(int(bit)) for bit in format(bits, '04b')]
        n_ones = bits_bools.count(True)
        if res: # res = 1
            if n_ones != 1:
                out.append(Node(bits_bools[2]))
                if debug:
                    print ">>", res, "Added:"
                    print_2D(bits_bools)
        else: # res == 0
            if n_ones == 1:
                out.append(Node(bits_bools[2]))
                if debug:
                    print ">>", res, "Added:"
                    print_2D(bits_bools)

    return out

def bit_is_set(bit, idx):
    if bit & (1<<idx):
        return True
    else:
        return False

def print_2D(bits):
    bitstring = [str(bit).replace('False', ' ').replace('True', '*') for bit in bits]
    print("  ["+bitstring[2]+bitstring[3]+"]")
    print("  ["+bitstring[1]+bitstring[0]+"]")

if __name__ == "__main__":
    x = [[True, False, True], [False, True, False], [True, False, True]]
    print(x)
    print(solution(x))
    print('')