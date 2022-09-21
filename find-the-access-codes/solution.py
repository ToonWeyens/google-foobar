debug = True

# x should be sorted low to high
def solution(x):
    # initialize array that holds number of previous digits that divides each entry of x
    c = [0] * len(x)
    
    # total count
    count = 0

    # go over all digits in sorted x
    for idx in range(len(x)):
        # count all previous digits that divided current xi
        for jdx in range(0, idx):
            if x[idx] % x[jdx] == 0:
                c[idx] = c[idx] + 1
                count += c[jdx]
    
    return count



if __name__ == "__main__":
    x = [1, 2, 3, 4, 5, 6]
    print(x)
    print(solution(x))
    print('')