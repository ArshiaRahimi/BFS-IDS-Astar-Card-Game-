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

# part 3: A*


def getMin(sequence):
    if not sequence:
        raise ValueError('empty sequence')

    minimum = sequence[0]

    for item in sequence:
        if item[1] < minimum[1]:
            minimum = item

    return minimum


def heuristic(node, n, k):
    diff_colors = 0
    not_in_position = 0
    arr = []
    for i in node.keys():
        if i == k+1:
            continue
        for j in node[i]:
            if j == '#':
                continue
            if j[1] not in arr:
                arr.append(j[1])
            real_place = abs(int(j[0]) - n)
            #print(j)
            if real_place != node[i].index(j):
                not_in_position += 1
        if '#' not in j:
            minusOne = len(arr) - 1
            diff_colors += minusOne
            arr.clear()
    #print("not in place score: " + str(not_in_position))
    #print("diff_colors: " + str(diff_colors))
    total_score = not_in_position + diff_colors
    return total_score


#  heuristic number 2
def heuristic2(node,n,k):
    placement = 0
    diff_colors = 0
    arr = []
    for i in node.keys():
        if i == k+1:
            continue
        for j in node[i]:
            if j == '#':
                continue
            if j[1] not in arr:
                arr.append(j[1])
            real_place = abs(int(j[0]) - n)
            #print(j)
            place = abs(real_place - node[i].index(j))
            #print(place)
            #print(" ")
            placement += place
        diff_colors += len(arr)
        arr.clear()
    #print("total score: " + str(placement))
    #print(diff_colors)
    total_score = placement + diff_colors
    return total_score

#print(heuristic(test,5))

def Astar(problem, n, k):
    frontier = []
    explored = []
    generated = 0
    T = True
    if checkTest(problem, n, k):
        print("DONE")
        return problem
    frontier.append([problem, heuristic(problem, n, k)])
    while T:
        # print("Searching...")
        #print(explored)
        if not frontier:
            print("Failed")
            T = False

        # pop the node with the least heuristic
        node = frontier.pop(frontier.index(getMin(frontier)))
        # node[0] = node without f value
        explored.append(node[0])
        # actions
        for action in actions2(node[0], k):
            action1 = dict(itertools.islice(action.items(), k))

            explored1 = []
            for i in explored:
                explored1.append(dict(itertools.islice(i.items(), k)))

            frontier1 = []
            for j in frontier:
                frontier1.append(dict(itertools.islice(j[0].items(), k)))
            if action1 not in frontier1 and action1 not in explored1:
                generated += 1
                if checkTest(action1, n, k):
                    print("Done")
                    for i in action.keys():
                        if i <= k:
                            print("row" + str(i) + ": " + str(action[i]))
                        else:
                            print("------------")
                            for i in action[i]:
                                print(i)

                    print("------------")
                    print("Generated: " + str(generated))
                    print("Expanded: " + str(len(explored)))
                    print("Depth: " + str(len(action[k+1])))
                    T = False
                # adding f = g + h to each actions
                f = heuristic(action, n, k) + len(action[k+1])
                frontier.append([action, f])


#Astar(test3, 5, 4)
#Astar(test, 5, 5)



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
        Astar(initial, n, k)

