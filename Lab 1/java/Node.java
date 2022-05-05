import java.util.Arrays;

public class Node {
    int fvalue;
    int depth;
    int[][] state;
    Node parent;

    public Node(int[][] state, int depth, int fvalue, Node parent) {
        this.state = state;
        this.depth = depth;
        this.fvalue = fvalue;
        this.parent = parent;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Node other = (Node) obj;
        if (!Arrays.deepEquals(this.state, other.state)) {
            return false;
        }
        return true;
    }

    // Print function
    public void print() {
        for (int i = 0; i < state.length; i++) {
            for (int j = 0; j < state[i].length; j++) {
                if (state[i][j] == 0) {
                    System.out.print("\u001B[31m" + state[i][j] + "\u001B[0m ");
                } else {
                    System.out.print(state[i][j] + " ");
                }
            }
            System.out.println();
        }
    }

    public Node[] getChildren() {
        Node[] children = new Node[4];
        int[][] state = this.state.clone();
        int i = 0;
        for (int j = 0; j < 3; j++) {
            for (int k = 0; k < 3; k++) {
                if (state[j][k] == 0) {
                    // Move up
                    if (j > 0) {
                        int[][] newState = this.deepcopystate();
                        newState[j][k] = newState[j - 1][k];
                        newState[j - 1][k] = 0;
                        children[i] = new Node(newState, this.depth + 1, this.fvalue, this);
                        i++;
                    }

                    // Move down
                    if (j < 2) {
                        // Deep clone state

                        int[][] newState = this.deepcopystate();
                        newState[j][k] = newState[j + 1][k];
                        newState[j + 1][k] = 0;
                        children[i] = new Node(newState, this.depth + 1, this.fvalue, this);
                        i++;
                    }

                    // Move left
                    if (k > 0) {
                        int[][] newState = this.deepcopystate();
                        newState[j][k] = newState[j][k - 1];
                        newState[j][k - 1] = 0;
                        children[i] = new Node(newState, this.depth + 1, this.fvalue, this);
                        i++;
                    }

                    // Move right
                    if (k < 2) {
                        int[][] newState = this.deepcopystate();
                        newState[j][k] = newState[j][k + 1];
                        newState[j][k + 1] = 0;
                        children[i] = new Node(newState, this.depth + 1, this.fvalue, this);
                        i++;
                    }
                }
            }
        }
        return children;
    }

    public int heuristic(Node goal, boolean useManhattan, boolean useMisplaced) {
        if (useManhattan && useMisplaced) {
            return manhattan_distance_value(goal) + missplaces_tiles_value(goal);
        } else if (useMisplaced && !useManhattan) {
            return missplaces_tiles_value(goal);
        } else if (!useMisplaced && useManhattan) {
            return manhattan_distance_value(goal);
        }
        return 0;
    }

    public int missplaces_tiles_value(Node goal) {
        int h = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (this.state[i][j] != goal.state[i][j] && this.state[i][j] != 0) {
                    h++;
                }
            }
        }
        return h;
    }

    public int manhattan_distance_value(Node goal) {
        int m = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (this.state[i][j] != goal.state[i][j] && this.state[i][j] != 0) {
                    int x = (this.state[i][j] - 1) / 3;
                    int y = (this.state[i][j] - 1) % 3;
                    m += Math.abs(i - x) + Math.abs(j - y);
                }
            }
        }
        return m;
    }

    public int[][] deepcopystate() {
        int[][] newState = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                newState[i][j] = this.state[i][j];
            }
        }
        return newState;
    }

    public String hash() {
        String hash = "";
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                hash += this.state[i][j];
            }
        }
        return hash;
    }
}
