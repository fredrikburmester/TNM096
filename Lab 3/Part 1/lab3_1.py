"""
"""
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


def resolutionClause(A, B):
    res = None
    return res

def part1(input_list):
    """ Part 1"""

    mapp = defaultdict(int)
    s = set()

    matrix = [[int(x) for x in line] for line in input_list]
    for line in matrix:
        print(line)

    return 0

def main():
    with open("./2021/Day 24/input.txt", "r", encoding='UTF-8') as file:
        input_list = [str(line.strip()) for line in file]

    t0 = time.time()
    result = part1(input_list)
    t1 = time.time()
    print(f"\n{bcolors.OKGREEN}{result}{bcolors.ENDC} is the result of part 1.\n{bcolors.OKBLUE}{round(t1-t0, 4)}{bcolors.ENDC} seconds\n")

# Run main function
if __name__ == "__main__":
    main()