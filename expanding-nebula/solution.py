import numpy as np

debug = True
# debug = False
if debug:
    glob_node_idx = 0

class Node:
    def __init__(self, data):
        if debug:
            global glob_node_idx
        self.data = data
        self.prev = None
        if debug:
            self.idx = glob_node_idx
            glob_node_idx += 1
    
    def __repr__(self):
        repr_str = "Node "+str(self.data).replace('False', '.').replace('True', '*')
        if debug:
            repr_str += " ["+str(self.idx)+"]"
        return repr_str

class NodeList:
    def __init__(self, head=None):
        # Optionally pass a node
        self.head = head
    
    def __repr__(self):
        printVal = self.head
        if printVal is None:
            repr_str = "empty Node list"
        else:
            repr_str = "Node list ("
        while printVal is not None:
            repr_str += str(printVal.data).replace('False', '.').replace('True', '*')
            if debug:
                repr_str += "["+str(printVal.idx)+"]"
            printVal = printVal.prev
            if printVal is not None:
                repr_str += "<-"
            else:
                repr_str += ")"
        return repr_str
    
    def add(self, data):
        prevHead = self.head
        self.head = Node(data)
        self.head.prev = prevHead
        return self



def solution(x):
    H = len(x)
    W = len(x[0])
    if debug:
        print 'table of dimensions (', H, ",", W, ")"

    # We will use a linked list to describe the different ways in which each next element
    # can be different, going in the following direction:
    #  [11 10 8]
    #  [9  7  5]
    #  [6  4  2]
    #  [4  1  0]
    # This will lead tohe concept of levels I, as such:
    #  [543]
    #  [432]
    #  [321]
    #  [210]
    # This way only the previous level's multiple possibilities are required to calculate the next
    # 
    # The level indicator I goes in principle from 0 to H+W where H is the height of the table and W the width
    # Note that this means we've added one row and one column, and level 2 contains the bottom right
    # corner of the original (outcomes) table
    # For each level we start lower left and and we iterate towards top right
    # If the grid is not square, as in the example, we will remove the points that fall outside of it by skipping

    outcomes = np.array(x) # easier for indexing than list of lists
    vals = [] # will contain an entry for every level
    vals.append([NodeList(Node(True)), NodeList(Node(False))])

    # helper dict to convert position (2D) to element index (1D)
    pos2el = np.zeros((H+1, W+1), dtype=np.int8)

    el_idx = 0 # already set level 0 above, will ad 1 at beginning of loop
    for I in range(H+W+1):
        if debug:
            print ">> reached level", I
        
        # iterate over non-boundary elements in this level
        for idx in range(I+1):
            pos = [H-idx, W-I+idx]
            if (pos[0] >= 0 and pos[0] <= H and pos[1] >= 0 and pos[1] <= W):
                el_idx  += 1

                if debug:
                    print "> within level", I, "at element", el_idx, "with position", pos

                # update helper functions
                pos2el[pos[0],pos[1]] = el_idx
                if debug:
                    print "pos2el:", pos2el

                # new level
                vals.append([])
                
                # boundary
                if ( (pos[0] == H and pos[1]>= 0) or # bottom row
                    (pos[1] == W and pos[0]>= 0) ): # rightern column

                    for val in vals[el_idx-1]:
                        vals[el_idx].append(NodeList(val.head).add(True))
                        vals[el_idx].append(NodeList(val.head).add(False))
                    
                    if debug:
                        print "appended boundary points at pos", pos

                # internal
                else:
                    # current outcome value
                    outcome = outcomes[pos[0],pos[1]]
                    
                    # find B, D, R of current point
                    # If we subtract the current element index, this shows how far back we have to go
                    ind_B  = pos2el[pos[0]+1,pos[1]]
                    ind_D = pos2el[pos[0]+1,pos[1]+1]
                    ind_R  = pos2el[pos[0],  pos[1]+1]
                    
                    for val in vals[el_idx-1]: # previous values
                        Node_B = get_neighbor(val, el_idx-1, ind_B)
                        Node_D = get_neighbor(val, el_idx-1, ind_D)
                        Node_R = get_neighbor(val, el_idx-1, ind_R)

                        # if debug:
                            # print "for outcome", outcome, "neighbor - B: ( ", ind_B, ")", Node_B, "; D: ( ", ind_D, ")", Node_D, "; R: ( ", ind_R, ")", Node_R

                        for val_next in valid_vals(outcome, Node_B,Node_D,Node_R):
                            vals[el_idx].append(NodeList(val.head).add(val_next))
                            # if debug:
                            #     print "added", vals[el_idx][-1]

                        # raw_input('paused inside node '+str(el_idx))

            else:
                continue # skip this one as it's outside the grid

            if debug:
                print "node", el_idx, ":"
                for val in vals[-1]:
                    print val
                # res = raw_input('paused at end of node '+str(el_idx))

    if debug:
        print "at final element", el_idx, "found", len(vals[-1]), "paths"
    return

def get_neighbor(val, el_idx, nb_idx):
    debug = False
    nbVal = val.head
    while nb_idx < el_idx:
        nbVal = nbVal.prev
        nb_idx += 1
        if debug:
            print "getting neighbor", nbVal

    return nbVal


def valid_vals(outcome, B,D,R):
    # valid values for resulting outcome, taking into account
    #   B: value below
    #   D: Value below right ("diagonal")
    #   R: Value right
    # B, D and R are nodes, outcome is a boolean, and the output is a list of booleans
    # containing the values TL from
    #   [TL TR]
    #   [BL BR]
    debug = False
    res = []

    for bits in range(0,16):
        # if debug:
            # print 'trying:', format(bits, '04b') 

        # Satisfy all the side constraints
        # indexing: TR TL BL BR
        if bit_is_set(bits, 3) != D.data:
            continue
        if bit_is_set(bits, 2) != B.data:
            continue
        if bit_is_set(bits, 0) != R.data:
            continue

        # Look at whether the number matches requirements for outcome
        #   - n_ones = 0 or 1 -> xor(outcome)
        #   - n_ones > 1      -> 0 or 1
        bits_bools = [bool(int(bit)) for bit in format(bits, '04b')]
        n_ones = bits_bools.count(True)
        # if debug:
            # print "n_ones", n_ones, "for outcome", outcome

        if n_ones <= 1:
            res.append(True^outcome) # 1 of outcome is 0 and vice versa
        else:
            if not outcome: # only outcome 0 can still be reached, with whatever val
                res.append(False)
                res.append(True)
        if debug:
            if n_ones <= 1 or (not outcome):
                print ">> for ", outcome, ", added TL value:"
                print_2D(bits_bools)
            else:
                print ">> no compatible TL values for", outcome
    
    if debug:
        print "returning", len(res), "values"

    return res

def bit_is_set(bit, idx):
    # print "is bit set?", bit, "idx", idx, bool(bit & (1<<idx))
    if bit & (1<<idx):
        return True
    else:
        return False

def print_2D(bits):
    bitstring = [str(bit).replace('False', '.').replace('True', '*') for bit in bits]
    print("  ["+bitstring[2]+bitstring[3]+"]")
    print("  ["+bitstring[1]+bitstring[0]+"]")

if __name__ == "__main__":
    x = [[True, False, True], [False, True, False], [True, False, True]]
    print(x)
    print(solution(x))
    print('')