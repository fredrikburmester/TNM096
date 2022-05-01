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
        }, 0, 0);

        Node goal = new Node(new int[][] {
                { 1, 2, 3 },
                { 4, 5, 6 },
                { 7, 8, 0 }
        }, 0, 0);

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

            if (counter % 1000 == 0) {
                printStats(counter, head.depth, open_set, closed_set);
            }

            if (head.equals(goal)) {
                System.out.println("Goal found!");
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
        System.out.println("Moves: " + head.depth);

        // Print execution time
        printExecutionTime(startTime, System.nanoTime());

        // Print goal state
        goal.print();
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
            System.out.println("Execution time: " + (duration / 1000000000) + "s");
        } else {
            System.out.println("Execution time: " + (duration / 1000000) + "ms");
        }
    }
}
