package colorlines;

import java.util.*;

/**
 * Classe implémentant l'algorithme A* pour trouver le chemin entre deux points
 * @author Jordan Oshoffa
 */
public class PathFinder {
    private GameBoard board;
    
    /**
     * Constructeur
     * @param board Plateau de jeu
     */
    public PathFinder(GameBoard board) {
        this.board = board;
    }
    
    /**
     * Trouve le chemin entre deux points
     * @param start Point de départ
     * @param end Point d'arrivée
     * @return Liste des points formant le chemin, ou null si aucun chemin n'est trouvé
     */
    public List<Point> findPath(Point start, Point end) {
        // Si la destination est occupée, pas de chemin possible
        if (board.getBall(end.x, end.y) != null) {
            return null;
        }
        
        // Initialisation des structures pour A*
        PriorityQueue<Node> openSet = new PriorityQueue<>();
        Set<Point> closedSet = new HashSet<>();
        Map<Point, Node> allNodes = new HashMap<>();
        
        // Nœud de départ
        Node startNode = new Node(start, null, 0, heuristic(start, end));
        openSet.add(startNode);
        allNodes.put(start, startNode);
        
        while (!openSet.isEmpty()) {
            Node current = openSet.poll();
            
            // Si on a atteint la destination
            if (current.position.equals(end)) {
                return reconstructPath(current);
            }
            
            closedSet.add(current.position);
            
            // Explorer les voisins
            for (Point neighbor : getNeighbors(current.position)) {
                if (closedSet.contains(neighbor)) {
                    continue;
                }
                
                double tentativeGScore = current.gScore + 1;
                
                Node neighborNode = allNodes.getOrDefault(neighbor, 
                                    new Node(neighbor, null, Double.MAX_VALUE, 0));
                
                if (!openSet.contains(neighborNode)) {
                    openSet.add(neighborNode);
                } else if (tentativeGScore >= neighborNode.gScore) {
                    continue;
                }
                
                // Mettre à jour le nœud voisin
                neighborNode.parent = current;
                neighborNode.gScore = tentativeGScore;
                neighborNode.fScore = tentativeGScore + heuristic(neighbor, end);
                allNodes.put(neighbor, neighborNode);
            }
        }
        
        // Aucun chemin trouvé
        return null;
    }
    
    /**
     * Retourne les voisins valides d'un point
     */
    private List<Point> getNeighbors(Point point) {
        List<Point> neighbors = new ArrayList<>();
        int[][] directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}}; // Bas, Droite, Haut, Gauche
        
        for (int[] dir : directions) {
            int newX = point.x + dir[0];
            int newY = point.y + dir[1];
            
            if (board.isValidPosition(newX, newY) && board.getBall(newX, newY) == null) {
                neighbors.add(new Point(newX, newY));
            }
        }
        
        return neighbors;
    }
    
    /**
     * Calcule l'heuristique (distance de Manhattan) entre deux points
     */
    private double heuristic(Point a, Point b) {
        return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
    }
    
    /**
     * Reconstruit le chemin à partir du nœud final
     */
    private List<Point> reconstructPath(Node endNode) {
        List<Point> path = new ArrayList<>();
        Node current = endNode;
        
        while (current != null) {
            path.add(current.position);
            current = current.parent;
        }
        
        Collections.reverse(path);
        return path;
    }
    
    /**
     * Classe interne représentant un nœud dans l'algorithme A*
     */
    private class Node implements Comparable<Node> {
        Point position;
        Node parent;
        double gScore; // Coût du chemin depuis le départ
        double fScore; // gScore + heuristique
        
        Node(Point position, Node parent, double gScore, double hScore) {
            this.position = position;
            this.parent = parent;
            this.gScore = gScore;
            this.fScore = gScore + hScore;
        }
        
        @Override
        public int compareTo(Node other) {
            return Double.compare(this.fScore, other.fScore);
        }
    }
}
