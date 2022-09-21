import copy
debug = True

# based on 2 observations:
# 1. divisibility by 3 means that the sum of digits is divisible by 3
#    -> implication: rearranging the numbers won't change disibility,
#       so best organize them with the highest numbers first
# 2. if not divisible, the remainder can be 1 or 2
#    -> imlpication: removing a single number that has a remainder equal to the overall remainder 
#       will make the entire number divisible
#    -> implication: if this is not satisfactory, removing two numbers the sum of which 
#       leads to a remainder equal to the overal remainder will make the entire number divisible
#       e.g. if overal remainder is 1, removing numbers that together give remainder of 2 will
#       both have remainder of 1 and vice versa
#    -> implicatino: if we cannot do taht, the number will never be divisible
def solution(x):
    # sort x from high to low
    x.sort(reverse=True)
    if debug:
        print("working with sorted array", x)
    
    # check special case if there are no digits
    if len(x)==0:
        return 0

    # overall remainder
    m = sum(x)%3

    # check if divisble by 3 by checking sum
    if m == 0:
        return digits2number(x)
    
    # check special case if there is only 1 digit
    if len(x)==1:
        return 0
    
    # there is a remainder of 1 or 2.
    # First check if we can make it dissapear by removing the least impactful digits
    if debug:
        print('need to get rid of remainder', m)
    xMod = copy.copy(x)
    for idx in range(len(x)):
        if debug:
            print('removing element', x[-1-idx])
        if (x[-1-idx]%3 == m):
            if debug:
                print("now it's divisible")
            del xMod[-1-idx]
            return digits2number(xMod)

    # if we have gotten here, there is still a remainder of 1 or 2.
    # We can try removing 2 numbers, both of which should have a 
    # remainder equal to 3-m (i.e. 1 if 2 and 2 if 1)
    
    # check special case if there is only 2 digits
    if len(x)==2:
        return 0
    
    m = 3-m
    if debug:
        print('trying removing 2 numbers, both should get rid of remainder...', m)
    nRemoved = 0
    xMod = copy.copy(x)
    for idx in range(len(x)):
        if debug:
            print('removing element', x[-1-idx])
        if (x[-1-idx]%3 == m):
            del xMod[-1-idx+nRemoved] # need extra offset because xMod can have alreay decreased in size
            nRemoved += 1
            if debug:
                print(nRemoved, 'removed so far')
            if nRemoved == 2:
                if debug:
                    print("now it's divisible II")
                return digits2number(xMod)

    # if we have gotten here, all hope is lost
    return 0

def digits2number(integers):
    strings = [str(integer) for integer in integers]
    a_string = "".join(strings)
    an_integer = int(a_string)
    return an_integer

if __name__ == "__main__":
    x = [3, 1, 4, 1]
    print(x)
    print(solution(x))
    print('')

    x = [3, 1, 4, 1, 5, 9]
    print(x)
    print(solution(x))
    print('')

    x = [1,2,4]
    print(x)
    print(solution(x))
    print('')

    x = [1,2,5]
    print(x)
    print(solution(x))
    print('')

    x = [0,1,1,1,1,4]
    print(x)
    print(solution(x))
    print('')

    x = [2]
    print(x)
    print(solution(x))
    print('')

    x = [1,1]
    print(x)
    print(solution(x))
    print('')

    x = [0,0,0]
    print(x)
    print(solution(x))
    print('')

    x = []
    print(x)
    print(solution(x))
    print('')

    x = [3, 9, 9, 6, 4, 3, 6, 4, 9, 6, 0]
    print(x)
    print(solution(x))
    print('')
    
    x = [2, 2, 5, 5, 8]
    print(x)
    print(solution(x))
    print('')