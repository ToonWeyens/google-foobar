debug = True

def solution(num_buns, num_required):
    # We will look at just-incomplete bunny groups: Those that have size num_required-1
    # For these groups we know all of the remaining num_buns-num_required+1 bunnies must have the key that
    # this incomplete group did not have.
    # Therefore when we iterate over the combinations we can assign the keys that were missing for the 
    # particular incomplete group, simply giving them a one-to-one correspondence to the combination index.
    # We can always do a fixed permutation to reduce any other rule to this.
    # This also means that the number of combinations is also identical to the number of keys required.
    # In this case it should always be < 10 as it's a single digit problem
    from itertools import combinations

    buns = [[] for i in range(num_buns)]

    if num_required == 0:
        return buns

    idx = 0
    if debug:
        print "combinations of", num_buns - num_required + 1, "elements in total of", buns
    for c in combinations(buns, num_buns - num_required + 1): # Nr. of combinations is also number of keys
        # let's distribute the keys for this round idx
        for item in c:
            item.append(idx)
        if debug:
            print 'after adding', idx, c
        idx += 1
    if debug:
        print 'at the end:', buns
    return buns

if __name__ == "__main__":
    assert all([all([x == y for x, y in zip(a, b)])
                for a, b in zip([[0, 1, 2, 3, 4, 5], [0, 1, 2, 6, 7, 8], [0, 3, 4, 6, 7, 9], [1, 3, 5, 6, 8, 9], [2, 4, 5, 7, 8, 9]], solution(5, 3))])
    # assert all([all([x == y for x, y in zip(a, b)])
    #             for a, b in zip([[0], [1], [2], [3]], solution(4, 4))])
