"""
"""
import json
import sys
import time
import math
from collections import defaultdict, Counter, deque
from copy import deepcopy
from typing import Union
from sortedcontainers import SortedKeyList
import cProfile

class Node:
    def __init__(self, state, depth):
        self.state = state
        self.depth = depth
        self.fvalue = None

    def getEmptySlot(self):
        for i in range(3):
            for j in range(3):
                if self.state[(i,j)] == 0:
                    return (i,j)

    def generate_children(self):
        state = self.state
        empty_space = self.getEmptySlot()
        x,y = empty_space

        children = []
        for n in neighbours_4(state, x, y):
            child_state = move_empty_square_to_neighbour(state, empty_space, n)
            child_node = Node(child_state, self.depth + 1)
            children.append(child_node)
        return children

    def __repr__(self):
        for i in range(3):
            for j in range(3):
                print(self.state[(i,j)], end=" ")
            print()
        return ""

    def hash(self):
        return hash(frozenset(self.state.items()))


def neighbours_4(m: Union[list, defaultdict], x, y) -> list:
    def in_range(x, y):
        return min(m)[0] <= x <= max(m)[0] and min(m)[1] <= y <= max(m)[1]
    return [p for p in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] if in_range(*p)]

def move_empty_square_to_neighbour(mapp, empty_space, neighbour):
        """
        Returns a new state with the empty square moved to a neighbour
        """
        new_mapp = mapp.copy()
        if new_mapp[empty_space] == 0:
            new_mapp[empty_space] = new_mapp[neighbour]
            new_mapp[neighbour] = 0
            return new_mapp

def fvalue(current_node, goal_state, h1, h2):
    """ Cost function: Sum of accrued costs from the start to the current node """
    if h1 and h2:
        return hvalue(current_node, goal_state) + mvalue(current_node, goal_state) + current_node.depth
    if h1 and not h2:
        return hvalue(current_node, goal_state) + current_node.depth
    if not h1 and h2:
        return mvalue(current_node, goal_state) + current_node.depth

def hvalue(current_node, goal):
    """ 
    Calculates the different between the given puzzles 
    High value = bad
    """
    value = 0
    for i in range(3):
        for j in range(3):
            state = current_node.state[(i,j)]
            if state == 0:
                continue
            if state != goal[(i,j)]:
                value += 1
    return value

def mvalue(current_node, goal_state):
    # calculate the manhattan distance from each square to its goal square and add them up
    distance = 0
    for i in range(3):
        for j in range(3):
            value = current_node.state[(i,j)]
            # find value in goal_stat
            if value != 0:
                for k in range(3):
                    for l in range(3):
                        if goal_state[(k,l)] == value:
                            distance += abs(i - k) + abs(j - l)
                            break
    
    return distance


def solve(start, goal, h1=True, h2=True):
    start = Node(start, 0)
    
    start.fvalue = fvalue(start, goal, h1, h2)

    open_list = SortedKeyList([start], key=lambda x: x.fvalue)
    closed_list = set()
    moves = []

    tests = 0

    while True:
        tests += 1

        if tests % 10000 == 0:
            print("\033[H\033[J", end="")
            print("Tests:", tests)
            print("Open list:", len(open_list))
            print(f"Depth: {open_list[0].depth} - {open_list[len(open_list) - 1].depth}")

            print("Open list values:", end=" ")
            for i in range(len(open_list)): 
                if i < 10:
                    print(open_list[i].fvalue, end=" ")
                    continue

                if i == 10: 
                    print("..." , end=" ")
                    continue

                if i > (len(open_list) - 10):
                    print(open_list[i].fvalue, end=" ")
                    continue

                if i > 10:
                    continue
            print()
            print()

        current_node = open_list.pop(0)

        if current_node.state == goal:
            print(f"\nGoal found in {current_node.depth} moves")

            break
        for child in current_node.generate_children():
            child.fvalue = fvalue(child, goal, h1, h2)

            if child.depth > 31:
                continue

            # if child.state in [n.state for n in open_list]:
            #     continue

            if child.hash() in closed_list:
                continue

            open_list.add(child)

        closed_list.add(current_node.hash())
        moves.append(current_node)  

    return moves, current_node

def read_input():
    start = defaultdict(int)
    goal = defaultdict(int)
    h1 = False
    h2 = False

    while True:
        print("Input starting position:")
        user_input = input()
        if user_input == "" or None:
            user_input = "2 5 0 1 4 8 7 3 6"
        user_input = [int(i) for i in user_input.strip().split(" ")]
        for i in range(3):
            for j in range(3):
                start[(i,j)] = user_input[i*3 + j]
        
        print("\nStarting position:")
        print(Node(start, 0))
        
        print("Input goal position:")
        user_input = input()
        if user_input == "" or None:
            user_input = "1 2 3 4 5 6 7 8 0"
        user_input = [int(i) for i in user_input.strip().split(" ")]
        for i in range(3):
            for j in range(3):
                goal[(i,j)] = user_input[i*3 + j]

        print("\nGoal position:")
        print(Node(goal, 0))

        h1 = input("Use misplaced tiles? (y/n)")
        if h1 == "y":
            h1 = True
        else:
            h1 = False

        h2 = input("Use manhattan distance? (y/n)")
        if h2 == "y":
            h2 = True
        else:
            h2 = False

        print("\nOk? (y/n)")
        user_input = input()
        if user_input == "y":
            break

        

    return start, goal, h1, h2

def lab1(start, goal, h1, h2):
    """ Part 1"""
    cost = 1

    with cProfile.Profile() as pr:
        closed_list, node = solve(start, goal, h1, h2)

    pr.print_stats()

    print()
    print(node)

    return 0

def main():
    # Example inputs:
    """ 
    Easy: 
        Start: 1 2 3 0 4 6 7 5 8
        Goal:  1 2 3 4 5 6 7 8 0

    Hard: 
        Start: 2 5 0 1 4 8 7 3 6
        Goal:  1 2 3 4 5 6 7 8 0
    
    Hardest
        Start: 6 4 7 8 5 0 3 2 1
        Goal:  1 2 3 4 5 6 7 8 0
    """
    start, goal, h1, h2 = read_input()
    t0 = time.time()
    result = lab1(start, goal, h1, h2)
    t1 = time.time()
    print(f"\n{result} is the result of lab 1.\n{round(t1-t0, 4)} seconds\n")

    """
    # Results:
        ## Only h1:
            ### Easy:   
                - Goal found in 3 moves
                - Time: 0.0015 seconds
            ### Hard: 
                - Goal found in 20 moves
                - Time: 3.0065 seconds
        ## Only h2: 
            ### Easy:
                - Goal found in 3 moves
                - Time: 0.0012 seconds
            ### Hard: 
                - Goal found in 20 moves
                - Time: 0.2351 seconds
        ## Both h1 and h2:
            ### Easy:
                - Goal found in 3 moves
                - Time: 0.0018 seconds
            ### Hard:
                - Goal found in 20 moves
                - Time: 0.1177 seconds

    # Conclusion:
        Both h1 and h2 is faster than either h1 or h2 separatly.
    """

# Run main function
if __name__ == "__main__":
    main()