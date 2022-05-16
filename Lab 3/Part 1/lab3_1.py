"""
"""
import random
import time
from collections import defaultdict, Counter, deque
from copy import deepcopy

class Clause: 
    def __init__(self, p, n):
        if isinstance(p, str) and n is None:
            conditions = p.split("V")
            p = set()
            n = set()
            for condition in conditions:
                if "-" in condition:
                    n.add(condition.strip("-- "))
                else:
                    p.add(condition.strip())
            self.p = p
            self.n = n
        else:
            self.p = p
            self.n = n

    def __str__(self):
        return str(self.p) + " " + str(self.n)

    def __repr__(self):
        return str(self.p) + " " + str(self.n)

def equalSetsOfClauses(A, B):
    assert isinstance(A, set)
    assert isinstance(B, set)

    if len(A) != len(B):
        return False

    for C1 in A:
        found = False
        for C2 in B:
            if C1.p == C2.p and C1.n == C2.n:
                found = True
                break
        if not found:
            return False
                
    return True

def clauseUnionSet(A, B):
    """
    Takes two sets of Clauses and returns the union of the two sets
    """
    assert isinstance(A, set)
    assert isinstance(B, set)

    C = set()
    
    for c1 in A:
        dup = False
        for c2 in C:
            if c1.p == c2.p and c1.n == c2.n:
                # already in set (union should not have duplicates)
                dup = True
                break
        if not dup:
            C.add(c1)
    
    for c1 in B:
        dup = False
        for c2 in C:
            if c1.p == c2.p and c1.n == c2.n:
                # already in set (union should not have duplicates)
                dup = True
                break
        if not dup:
            C.add(c1)
    
    return C

def resolutionClause(A, B):
    A_copy = deepcopy(A)
    B_copy = deepcopy(B)

    if not (A_copy.p & B_copy.n) and not (A_copy.n & B_copy.p):
        return False

    if (A_copy.p & B_copy.n):
        a = random.choice(list(A_copy.p & B_copy.n))
        A_copy.p.remove(a)
        B_copy.n.remove(a)
    else:
        a = random.choice(list(A_copy.n & B_copy.p))
        A_copy.n.remove(a)
        B_copy.p.remove(a)

    C = Clause(A_copy.p | B_copy.p, A_copy.n | B_copy.n)

    if (C.p & C.n):
        return False

    return C

def solver(KB):
    assert isinstance(KB, set)
    while True:
        S = set()
        assert len(S) == 0
        KB_copy = deepcopy(KB)
        for A in KB:
            for B in KB:
                C = resolutionClause(A, B)
                if C is not False:
                    S = S | set({C})

        if not S:
            return KB
        KB = incorperate(S, KB)

        print("KB: ")
        for C in KB: 
            print(C)
        print("S: ")
        for C in S:
            print(C)
        print()

        if equalSetsOfClauses(KB, KB_copy):
            break
    return KB

def incorperate(S, KB):
    assert isinstance(S, set)
    assert isinstance(KB, set)
    for A in S:
        KB = incorperate_clause(A, KB)
    return KB

def incorperate_clause(A, KB):
    assert isinstance(A, Clause)
    assert isinstance(KB, set)
    for B in KB:
        if subset(B, A):
            return KB
    for B in deepcopy(KB):
        if proper_subset(A, B):
            KB.discard(B)

    KB = KB | set({A})
    return KB

def subset(A, B):
    if len(A.p) > len(B.p) or len(A.n) > len(B.n):
        return False
    if A.p <= B.p and A.n <= B.n:
        return True
    return False

def proper_subset(A, B):
    """Check if A is a proper subset of B"""
    if not subset(A,B): 
        return False
    if A.p < B.p or A.n < B.n:
        return True
    return False

def part1():
    # Test 1
    A = Clause(set({1,2}), set({3}))
    B = Clause(set({2,3}), set({}))

    C = resolutionClause(A, B)
    assert C.p == set({1,2}) and C.n == set()

    A = Clause(set({'a','b'}), set({'c'}))
    B = Clause(set({'c','b'}), set({}))

    C = resolutionClause(A, B)
    assert C.p == set({'a','b'}) and C.n == set()

    A = Clause(set({1,2}), set({3}))
    B = Clause(set({4,2}), set({7}))

    C = resolutionClause(A, B)
    assert not C

    A = Clause(set({'a','b'}), set({'c'}))
    B = Clause(set({'d','b'}), set({'g'}))

    C = resolutionClause(A, B)
    assert not C

    # Test 3
    A = Clause(set({'c','t'}), set({'b'}))
    B = Clause(set({'z','b'}), set({'c'}))

    C = resolutionClause(A, B)
    assert not C

    print("Part 1 complete.")

    # Test 4
    A = Clause("c V a", None)
    B = Clause("a V b V c", None)

    assert proper_subset(A, B)

    # Test 5
    A = Clause("b V -c", None)
    B = Clause("a V b V -c", None)

    assert proper_subset(A, B)

    # Test 6
    A = Clause("b V -f V -c", None)
    B = Clause("a V b V -c", None)

    assert not proper_subset(A, B)
    
    # Test 7
    A = Clause("b", None)
    B = Clause("a V b V -c", None)

    assert proper_subset(A, B)

    # Test 8
    A = Clause("b V -c V a", None)
    B = Clause("a V b V -c", None)

    assert not  proper_subset(A, B)

    # Test 9
    A = set({1,2})
    B = set({3,4,5})

    assert not (A & B)
    
    # Test 9
    A = set({1,2})
    B = set({1})

    assert A & B

    # Test 9
    A = set({1,2})
    B = set({1})

    assert A & B == set({1})

    # Test 9
    A = set({1,2})
    B = set({1})

    assert A | B == set({1, 2})

    # Test 9
    C1 = Clause(set({1,2}), set({3,4,5}))
    C2 = Clause(set({1,2}), set({3,4,5}))

    S1 = set({C1})
    S2 = set({C2})

    assert equalSetsOfClauses(S1, S2)


    C1 = Clause(set({}), set({3,4,5}))
    C2 = Clause(set(), set({3,4,5}))

    S1 = set({C1})
    S2 = set({C2})

    assert equalSetsOfClauses(S1, S2)

    C1 = Clause(set({1}), set({3,4,5}))
    C2 = Clause(set(), set({3,4,5}))

    S1 = set({C1})
    S2 = set({C2})

    assert not equalSetsOfClauses(S1, S2)

    # Test 10
    C1 = Clause(set({1,2}), set({3,4,}))
    C2 = Clause(set({1,2}), set({3,4,5}))

    S1 = set({C1})
    S2 = set({C2})

    assert not equalSetsOfClauses(S1, S2)

    # Test 11
    C1 = Clause(set({1,2}), set({3}))
    C2 = Clause(set({1,2}), set({3,4,5}))
    C3 = Clause(set({1}), set({3,4,5}))

    S1 = set({C1,C2})
    S2 = set({C3})
    S3 = set({C3,C1})

    assert not equalSetsOfClauses(S1, S2)
    assert not equalSetsOfClauses(S2, S3)
    assert not equalSetsOfClauses(S1, S3)

    S1.discard(C2)
    S3.discard(C3)
    
    assert equalSetsOfClauses(S1, S3)

    return 0

def part2():
    A = Clause("-sun V -money V ice", None)
    B = Clause("-money V ice V movie", None)
    C = Clause("-movie V money", None)
    D = Clause("-movie V -ice", None)
    E = Clause("sun V money V cry", None)
    F = Clause("movie", None)

    KB = set({A, B, C, D, E, F})

    S = solver(KB)

    print("\nFinal clause S: ")
    for C in S:
        print(C)

def main():
    t0 = time.time()
    result = part1()
    t1 = time.time()
    print(f"\n{round(t1-t0, 4)} seconds\n")

    t0 = time.time()
    result = part2()
    t1 = time.time()
    print(f"\n{round(t1-t0, 4)} seconds\n")

# Run main function
if __name__ == "__main__":
    main()