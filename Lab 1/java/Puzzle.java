import java.util.HashSet;

public class Puzzle {
    public static void main(String[] args) {
        // Open list
        List open_list = new List();

        HashSet<String> open_set = new HashSet<>();
        HashSet<String> closed_set = new HashSet<>();

        boolean useManhattan = false;
        boolean useMisplaced = true;

        // EASY
        // Node start = new Node(new int[][] {
        // { 2, 5, 0 },
        // { 1, 4, 8 },
        // { 7, 3, 6 }
        // }, 0, 0);

        // HARD
        Node start = new Node(new int[][] {
                { 6, 4, 7 },
                { 8, 5, 0 },
                { 3, 2, 1 }
        }, 0, 0, null);

        Node goal = new Node(new int[][] {
                { 1, 2, 3 },
                { 4, 5, 6 },
                { 7, 8, 0 }
        }, 0, 0, null);

        open_list.add(start);

        Node head = open_list.poll();
        int counter = 0;
        long startTime = System.nanoTime();
        Node[] children = new Node[4];

        while (true) {
            if (counter > 0) {
                head = open_list.poll();
            }

            if (head == null) {
                System.err.println("No solution found");
                System.exit(0);
            }

            // if (counter % 1000 == 0) {
            // printStats(counter, head.depth, open_set, closed_set);
            // }

            if (head.equals(goal)) {
                System.out.println("\nGoal found!");
                break;
            }

            children = head.getChildren();
            for (Node child : children) {
                if (child == null) {
                    continue;
                }

                child.fvalue = child.depth + child.heuristic(goal, useManhattan, useMisplaced);

                if (!open_set.contains(child.hash()) && !closed_set.contains(child.hash())) {
                    open_list.add(child);
                    open_set.add(child.hash());
                }
            }

            // Add to closed set so we don't revisit
            closed_set.add(head.hash());

            // Keep track of how many nodes we've expanded
            counter++;
        }

        // Print number of moves to goal

        // Print execution time
        printExecutionTime(startTime, System.nanoTime());
        System.out.println();

        // Print path to goal
        System.out.println("Moves: \u001B[32m" + head.depth + "\u001B[0m");
        printPath(head);
    }

    public static void printPath(Node head) {
        Node[] path = new Node[head.depth + 1];
        Node current = head;
        Node previous = head;
        String stringPath = "";

        while (current != null) {
            previous = current;
            path[current.depth] = current;
            current = current.parent;

            if (current != null) {
                stringPath += getMoveLetter(current, previous);
            }
        }

        System.out.println("Path to goal:");
        // print string in reverse
        for (int i = stringPath.length() - 1; i >= 0; i--) {
            System.out.print("\u001B[33m" + stringPath.charAt(i) + "\u001B[0m");
        }
        System.out.println();
        for (int i = 0; i < path.length; i++) {
            if (path[i] != null) {
                path[i].print();
                System.out.println();
                System.out.println("  |");
                System.out.println("  v");
                System.out.println();
            }
        }
    }

    public static String getMoveLetter(Node n1, Node n2) {
        String move = "";

        int[][] state1 = n1.state;
        int[][] state2 = n2.state;

        int x1 = 0;
        int y1 = 0;
        int x2 = 0;
        int y2 = 0;

        // get location of 0
        for (int i = 0; i < state1.length; i++) {
            for (int j = 0; j < state1[i].length; j++) {
                if (state1[i][j] == 0) {
                    x1 = i;
                    y1 = j;
                }
            }
        }

        for (int i = 0; i < state2.length; i++) {
            for (int j = 0; j < state2[i].length; j++) {
                if (state2[i][j] == 0) {
                    x2 = i;
                    y2 = j;
                }
            }
        }

        if (x1 == x2) {
            if (y1 < y2) {
                move = "R";
            } else {
                move = "L";
            }
        } else if (y1 == y2) {
            if (x1 < x2) {
                move = "D";
            } else {
                move = "U";
            }
        }

        return move;
    }

    public static void printStats(int counter, int depth, HashSet<String> open_set, HashSet<String> closed_set) {
        System.out.print("\033[H\033[2J");
        System.out.flush();

        System.out.println("Iterations: " + counter);
        System.out.println("Open list size: " + open_set.size());
        System.out.println("Closed list size: " + closed_set.size());
        System.out.println("Current node depth: " + depth);
    }

    public static void printExecutionTime(long startTime, long endTime) {
        long duration = endTime - startTime;
        if (duration / 1000000 > 1000) {
            System.out.println("Execution time: \u001B[32m" + (duration / 1000000000) + "s\u001B[0m");
        } else {
            System.out.println("Execution time: \u001B[32m" + (duration / 1000000) + "ms\u001B[0m");
        }
    }
}
