package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Finds levels that are the same puzzle: the same board, animals, walls, hole and turn tiles, or the
 * same after turning or flipping the board (a mirror image of a puzzle is still the same puzzle).
 */
public final class Duplicates {
    private static final int[][] DIRS = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};

    private Duplicates() {
    }

    /** One text key per puzzle: the smallest of its eight turned and flipped versions (four if not square). */
    public static String key(Level l) {
        String best = null;
        for (int t = 0; t < 8; t++) {
            if (t >= 4 && l.w != l.h) {
                break;
            }
            String k = version(l, t);
            if (best == null || k.compareTo(best) < 0) {
                best = k;
            }
        }
        return best;
    }

    /** Level numbers (1-based) of each later copy and the earlier level it repeats: {copy, original}. */
    public static List<int[]> pairs(List<Level> levels) {
        Map<String, Integer> seen = new HashMap<>();
        List<int[]> out = new ArrayList<>();
        for (int i = 0; i < levels.size(); i++) {
            Integer first = seen.putIfAbsent(key(levels.get(i)), i + 1);
            if (first != null) {
                out.add(new int[] {i + 1, first});
            }
        }
        return out;
    }

    /** The number (1-based) of another level that is the same puzzle as {@code level}, or -1. */
    public static int twin(List<Level> levels, Level level, int n) {
        String k = key(level);
        for (int i = 0; i < levels.size(); i++) {
            if (i != n - 1 && key(levels.get(i)).equals(k)) {
                return i + 1;
            }
        }
        return -1;
    }

    private static int[] move(int t, int x, int y, int w, int h) {
        switch (t) {
            case 0: return new int[] {x, y};
            case 1: return new int[] {w - 1 - x, y};
            case 2: return new int[] {x, h - 1 - y};
            case 3: return new int[] {w - 1 - x, h - 1 - y};
            case 4: return new int[] {y, x};
            case 5: return new int[] {h - 1 - y, x};
            case 6: return new int[] {y, w - 1 - x};
            default: return new int[] {h - 1 - y, w - 1 - x};
        }
    }

    private static String version(Level l, int t) {
        int w = l.w, h = l.h;
        List<String> walls = new ArrayList<>();
        for (int[] p : l.walls) {
            int[] q = move(t, p[0], p[1], w, h);
            walls.add(q[0] + "," + q[1]);
        }
        List<String> fixed = new ArrayList<>();
        for (Piece p : l.fixed) {
            int[] q = move(t, p.x, p.y, w, h);
            fixed.add(p.type.id() + "@" + q[0] + "," + q[1]);
        }
        List<String> turns = new ArrayList<>();
        for (int[] p : l.turns) {
            int[] q = move(t, p[0], p[1], w, h), r = move(t, p[0] + DIRS[p[2]][0], p[1] + DIRS[p[2]][1], w, h);
            turns.add(q[0] + "," + q[1] + ">" + (r[0] - q[0]) + "," + (r[1] - q[1]));
        }
        List<String> traps = new ArrayList<>();
        for (int[] p : l.traps) {
            int[] q = move(t, p[0], p[1], w, h);
            traps.add(q[0] + "," + q[1]);
        }
        Collections.sort(traps);
        List<String> hand = new ArrayList<>();
        for (Animal a : l.inventory) {
            hand.add(a.id());
        }
        Collections.sort(walls);
        Collections.sort(fixed);
        Collections.sort(turns);
        Collections.sort(hand);
        int[] hole = move(t, l.holeX, l.holeY, w, h);
        boolean flip = t >= 4;
        return (flip ? h + "x" + w : w + "x" + h) + " hole " + hole[0] + "," + hole[1] + " walls " + walls + " animals " + fixed
                + " hand " + hand + " turns " + turns + (traps.isEmpty() ? "" : " traps " + traps);
    }
}
