package colorlines;

/**
 * Classe représentant un point sur le plateau de jeu
 * @author Jordan Oshoffa
 */
public class Point {
    public int x;
    public int y;
    
    /**
     * Constructeur
     * @param x Coordonnée x
     * @param y Coordonnée y
     */
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Point point = (Point) obj;
        return x == point.x && y == point.y;
    }
    
    @Override
    public int hashCode() {
        return 31 * x + y;
    }
}
