# Lab 1

## Tree Search

### Breadth first

`A -> B -> C -> D -> E -> F -> G -> H -> I -> J`

### Depth first

`A -> B -> E -> F -> G -> C -> H -> D -> I -> J`

### Iterative Deepening Search

**1st iteration:**

`A`

**2nd iteration:**

`A -> B -> C -> D`

**3rd iteration:**

`A -> B -> C -> D -> E -> F -> G -> H -> I -> J`

### Best-first search

`A -> C -> D -> J -> B -> F -> G -> I -> E -> H`

### A* search

`A -> B -> F -> G -> E -> D -> J -> I -> C -> H`

## Search Algorithms

- A.
Iterative deepening search is a good choice when the depth is unknown. Its a good combination of DFS and BFS. It might be a bit slow though due to all the iterations.
- B.
A best-first search is the best approach if we have a cost associated with the arcs. We can choose a search algorithm that elliminates cycles.
- C.
A* search is optimal if we have a heuristic and are looking for a leaf node.
- D.
I would again choose to use A* in this example since we have a heuristic and arc costs but limit cycles.

## Search Problem Formulation

We have a small and a big pitcher containing a max of 3 and 4 litres of liquid respectivly with no indicators for volume. The goal is reached when the big pithcer has 2 litres of liquid in it. In total there are 6 actions:

- Fill big completely
- Fill small completely
- Empty big completely
- Empty small completely
- Pour from big -> small until small is full or big is empty
- Pour from small -> big until big is full or small is empty

All actions are not valid at each step, since we can not fill an already full pitcher and not empty an already empty pithcer nor pour from a full pitcher into another full pitcher.

The state will hold two values, the amount of liquid in the big and the small pitcher. At the start node the values are (0, 0). Each branch from each node is one of the valid six actions. The space can be very cyclic which demands disallowing cycles over a certain length, for example 2. We could probably disallow cycles completely since the same state always has the same actions.

Since the space is very small and we don't have a clear heuristic or cost (except the depth) BFS would probably be both fast and optimal in this case.

If we would like to improve our search we could think logically and add a heuristic. For example: we know that to get 2 litres of liquid into the large pitcher we would need to have exacly 2 litres of liquid in the small pitcher that we could pour into the large one. Thus a value of 2 for the smaller pithcer state would be optimal and we could strive for that. This is halfway to solving the problem manually though so I don't think we want to add a heuristic to this simple problem.

## The 8-puzzle

### C

1. H1 and H2 individually are admissible since none of them **over**estimates the cost.
2. H2 performs better because it looks at the difference between the current state and goal state in a way that weighs the distance from wrong placement to correct placement. H1 only consideres inclorrectly placed blocks and not how close they are to actually being correctly placed.
3.
   1. H3 would not be admissible since the two heuristics are different in order of magnitude (h1 is one dimentional and h2 is two dimentional), and only dividing by 2 would not be acurate and an overestimate could be made.
   2. H4 is still admissable since its only a scaled h1 value.
   3. H5 is admissible if we assume 1. is admissible.
