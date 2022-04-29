public class Puzzle {
    public static void main(String[] args) {
        // Open list
        List ol = new List();
        List cl = new List();

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

        ol.add(start);
        Node head = ol.poll();
        int counter = 0;

        long startTime = System.nanoTime();
        while (true) {
            if (counter > 0) {
                head = ol.poll();
            }

            if (counter % 100 == 0) {
                clearScreen();
                System.out.println("Iterations: " + counter);
                System.out.println("Open list size: " + ol.size());
                System.out.println("Closed list size: " + cl.size());
                System.out.println("Current node depth: " + head.depth);
            }

            if (head == null) {
                System.err.println("No solution found");
                System.exit(0);
                break;
            }

            if (head.equals(goal)) {
                System.out.println("Goal found!");
                break;
            }

            Node[] children = head.getChildren();
            for (Node child : children) {
                if (child == null) {
                    continue;
                }

                int fvalue = child.depth + child.heuristic(goal);
                child.fvalue = fvalue;

                if (!ol.contains(head) && !ol.contains(head)) {
                    ol.add(child);
                }
            }

            cl.add(head);

            counter++;
        }
        long endTime = System.nanoTime();
        long duration = (endTime - startTime);

        System.out.println("Depth: " + head.depth);
        if (duration / 1000000 > 1000) {
            System.out.println("Time: " + (duration / 1000000000) + "s");
        } else {
            System.out.println("Time: " + (duration / 1000000) + "ms");
        }
        goal.print();
    }

    public static void clearScreen() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
}
