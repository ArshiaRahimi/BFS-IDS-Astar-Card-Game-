import itertools
import math
import re
from itertools import groupby
from copy import deepcopy

test = {
    1: ['5g', '4g', '3g', '2g', '1g'],
    2: ['5r', '4r', '3r', '1r', '2y'],
    3: ['5y', '4y', '3y','2r','1y'],
    4: ['#'],
    5: ['#'],
    6: []
}

test2 = {
    1: ['5y', '4y', '3y', '2y', '1y'],
    2: ['#'],
    3: ['#'],
    4: ['5r', '4r', '3r', '2r', '1r'],
    5: ['5g', '4g', '3g', '2g', '1g'],
    6: []
}

test3 = {
    1: ['5g', '4g', '3g', '2r', '1g'],
    2: ['5r', '4r', '3r', '2g', '1r'],
    3: ['#'],
    4: ['#'],
    5: []
}
test4 = {
    1: ['2g', '1b', '2b'],
    2: ['2r', '1g', '1r'],
    3: ['#'],
    4: ['#']
}


def actions2(state, k):
    list = []
    index = 0
    for i in range(1, k + 1):
        if '#' in state[i]:
            first = math.inf
        else:
            first = int(re.search(r'\d+', state[i][-1]).group())
        for j in range(1, k + 1):
            if i == j:
                continue
            if '#' in state[j]:
                second = math.inf
            else:
                second = int(re.search(r'\d+', state[j][-1]).group())
            if first < second:
                list.append(deepcopy(state))
                #children[ch_ind][k+1] = []
                selected = list[index][i][-1]
                if '#' in list[index][j]:
                    list[index][j].pop()
                list[index][j].append(state[i][-1])
                ## adding new one
                list[index][i].pop()
                list[index][k+1].append("popped " + selected+" from " + str(i) + " append to " + str(j))
                if len(list[index][i]) == 0:
                    list[index][i].append('#')
                index += 1

    return list

"""for i in actions2(test3,4):
    print(i)"""


# iterable is one of the items of dict e.g [1,1,1,1,1]
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def all_sorted(numberOfCards, iterable):
    index = 0
    if len(iterable) == 0:
        return True

    if numberOfCards == len(iterable):
        while numberOfCards >= 0:
            if str(numberOfCards) in iterable[index]:
                numberOfCards -= 1
                index += 1
                if numberOfCards == 0:
                    return True
            else:
                return False
    else:
        return False


# k added to if i =="#" and to the function param
def checkTest(node, n, k):
    colors = []
    numbers = []
    final = True
    for key in node.keys():
        # colors.clear()
        # numbers.clear()

        for i in node[key]:
            if i == "#":
                continue
            if key == k+1:
                continue
            colors.append(i[1])
            numbers.append(i[0])
        # print(colors)
        # print(numbers)
        if all_equal(colors) == False:
            final = False
        if all_sorted(n, numbers) == False:
            final = False
        colors.clear()
        numbers.clear()
    return final

#print(checkTest(test2,5,5))
# print(checkTest(test2, 5))

# Part 2: IDS

expanded = 0
generated = 0


def RECURSIVE_DLS(problem, limit, n, k):
    global expanded
    global generated
    if checkTest(problem, n, k):
        print("DONE")
        return problem
    elif limit == 0:
        # cutoff
        cutoff = None
        return cutoff
    else:
        cutoff_occurred = False
        expanded += 1
        for action in actions2(problem, k):
            generated += 1
            result = RECURSIVE_DLS(action, limit - 1, n, k)
            if result is None:
                cutoff_occurred = True
            elif result:
                return result
        if cutoff_occurred:
            return None
        else:
            return False

#print(RECURSIVE_DLS(test3,8,5,4))

def IDS(problem,n,k):
    # we can change the depth
    depth = 0
    # depth = 7
    while True:
        result = RECURSIVE_DLS(problem, depth, n, k)
        if result is not None:
            for i in result.keys():
                if i <= k:
                    print("row" + str(i) + ": " + str(result[i]))
                else:
                    print("------------")
                    for i in result[i]:
                        print(i)
            print("------------")
            print("Limit="+str(depth))
            print("Expanded=" + str(expanded))
            print("Generated=" + str(generated))
            return result
        depth = depth + 1

#IDS(test,5,5)


if __name__ == '__main__':
    initial = dict()
    user_input = input("Please enter k m n ")
    spliter = user_input.split()
    if len(spliter) > 3:
        print("You entered more than 3 variables!")
    else:
        k = int(spliter[0])
        m = int(spliter[1])
        n = int(spliter[2])
        for i in range(int(user_input.split()[0])):
            lines = input()
            initial[i+1] = lines.split()
        initial[k+1] = []
        print(initial)
        """ our algorithms: remove comment to test"""
        IDS(initial, n, k)

