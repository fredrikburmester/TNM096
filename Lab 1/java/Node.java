import java.util.Arrays;

public class Node {
    int fvalue;
    int depth;
    int[][] state;

    public Node(int[][] state, int depth, int fvalue) {
        this.state = state;
        this.depth = depth;
        this.fvalue = fvalue;
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
                System.out.print(state[i][j] + " ");
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
                        children[i] = new Node(newState, this.depth + 1, this.fvalue);
                        i++;
                    }

                    // Move down
                    if (j < 2) {
                        // Deep clone state

                        int[][] newState = this.deepcopystate();
                        newState[j][k] = newState[j + 1][k];
                        newState[j + 1][k] = 0;
                        children[i] = new Node(newState, this.depth + 1, this.fvalue);
                        i++;
                    }

                    // Move left
                    if (k > 0) {
                        int[][] newState = this.deepcopystate();
                        newState[j][k] = newState[j][k - 1];
                        newState[j][k - 1] = 0;
                        children[i] = new Node(newState, this.depth + 1, this.fvalue);
                        i++;
                    }

                    // Move right
                    if (k < 2) {
                        int[][] newState = this.deepcopystate();
                        newState[j][k] = newState[j][k + 1];
                        newState[j][k + 1] = 0;
                        children[i] = new Node(newState, this.depth + 1, this.fvalue);
                        i++;
                    }
                }
            }
        }
        return children;
    }

    public int heuristic(Node goal) {
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

    public int[][] deepcopystate() {
        int[][] newState = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                newState[i][j] = this.state[i][j];
            }
        }
        return newState;
    }
}
