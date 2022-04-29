import java.util.Comparator;
import java.util.PriorityQueue;

public class List {
    public PriorityQueue<Node> ol = new PriorityQueue<Node>(1000, new Comparator<Node>() {
        @Override
        public int compare(Node n1, Node n2) {
            return n1.fvalue - n2.fvalue;
        }
    });

    public boolean contains(Node n1) {
        for (Node n2 : this.ol) {
            if (n2.equals(n1)) {
                return true;
            }
        }
        return false;
    }

    public void add(Node n) {
        this.ol.add(n);
    }

    public Node poll() {
        return this.ol.poll();
    }

    public int size() {
        return this.ol.size();
    }
}
