"""
"""
import random
import sys
import time
import math
from collections import defaultdict, Counter, deque
from copy import deepcopy

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Clause: 
    def __init__(self, p, n):
        self.p = p
        self.n = n

    def __str__(self):
        return "p: " + str(self.p) + " n: " + str(self.n)

    def __repr__(self):
        return "p: " + str(self.p) + " n: " + str(self.n)


def resolutionClause(A, B):
    if not (A.p & B.n) and not (A.n & B.p):
        return False

    if (A.p & B.n):
        a = random.choice(list(A.p & B.n))
        A.p.remove(a)
        B.n.remove(a)
    else:
        a = random.choice(list(A.n & B.p))
        A.n.remove(a)
        B.p.remove(a)

    C = Clause(A.p | B.p, A.n | B.n)

    if (C.p & C.n):
        return False

    return C


def solver(KB):
    while True:
        S = set()
        KB_copy = deepcopy(KB)
        for A in KB_copy:
            for B in KB_copy:
                C = resolutionClause(A, B)
                if C:
                    S.add(C)

        print("S", S)

        if not S:
            return KB
        KB = incorperate(KB, S)
        if KB == KB_copy:
            break
    return KB

def incorperate(KB, S):
    for A in S:
        KB = incorperate_clause(KB, A)
    return KB

def incorperate_clause(KB, A):
    for B in KB:
        if subset(B, A):
            return KB
    for B in KB:
        if proper_subset(A, B):
            KB.remove(B)
    KB.append(A)
    return KB


def subset(A, B):
    if not (A.p <= B.p) and not (A.n <= B.n):
        return False
    return True

def proper_subset(A, B):
    if not (A.p < B.p) and not (A.n < B.n):
        return False
    return True


def part1():
    # Test 1
    A = Clause(set({1,2}), set({3}))
    B = Clause(set({2,3}), set({}))

    C = resolutionClause(A, B)
    assert C.p == set({1,2}) and C.n == set()


    A = Clause(set({1,2}), set({3}))
    B = Clause(set({4,2}), set({7}))

    C = resolutionClause(A, B)
    assert not C

    # Test 3
    A = Clause(set({'c','t'}), set({'b'}))
    B = Clause(set({'z','b'}), set({'c'}))

    C = resolutionClause(A, B)
    assert not C

    print("Part 1 complete.")

    return 0


def part2():
    # Test 1
    A = Clause(set({'ice'}), set({'sun','money'}))
    B = Clause(set({'ice','movie'}), set({'money'}))
    C = Clause(set({'money'}), set({'movie'}))
    D = Clause(set({}), set({'movie','ice'}))

    KB = set({A, B, C, D})

    S = solver(KB)
    for C in S:
        print(C)

def main():
    t0 = time.time()
    result = part1()
    t1 = time.time()
    print(f"\n{bcolors.OKGREEN}{result}{bcolors.ENDC} is the result of part 1.\n{bcolors.OKBLUE}{round(t1-t0, 4)}{bcolors.ENDC} seconds\n")

    t0 = time.time()
    result = part2()
    t1 = time.time()
    print(f"\n{bcolors.OKGREEN}{result}{bcolors.ENDC} is the result of part 1.\n{bcolors.OKBLUE}{round(t1-t0, 4)}{bcolors.ENDC} seconds\n")

# Run main function
if __name__ == "__main__":
    main()