# TNM096
> If this helped you in any way, consider giving this repo a star 😄 ⭐️

Labs in the course TNM096 at Linköping University

## Lab 1 - 8 Puzzle

In this lab we solve the 8-puzzle using A* search with two different heuristics, missplaced tiles and manhattan distans.

### Solve times (Java)

| Heuristic                | No Moves   | Time        |
| ------------------------ |:----------:| -----------:|
| missplaces tiles         | 159        | 10ms        |
| manhattan distans        | 47         | 2ms         |
| depth                    | 31         | 538ms       |
| missplaces + depth       | 31         | 394ms       |
| manhattan + depth        | 31         | 55ms        |
| missplaces + manhattan   | 45         | 2ms         |
| **all three**            | **31**     | **38ms**    |

The shortest solve time with the least amount of moves was obtained by using all three heuristics.

## Lab 2 - Sudoku

## Lab 3 - CNF Solver
