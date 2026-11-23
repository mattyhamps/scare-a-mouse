package io.github.mattyhamps.scareamouse.engine;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Text pictures of a board, used by the physics tests.
 * Legend: M mouse, C cat, D dog, B bear, L lion, E elephant, # wall, . floor.
 * <pre>
 *   ".MC...."   a mouse with a cat to its right
 * </pre>
 */
public final class BoardPicture {
    private BoardPicture() {
    }

    /** Builds a level from rows of text. Hole may be null (no hole). The mouse is listed first, like real levels. */
    public static Level level(List<String> rows, int[] hole) {
        List<int[]> walls = new ArrayList<>();
        List<Piece> mice = new ArrayList<>();
        List<Piece> others = new ArrayList<>();
        for (int y = 0; y < rows.size(); y++) {
            String row = rows.get(y);
            for (int x = 0; x < row.length(); x++) {
                char c = row.charAt(x);
                if (c == '#') {
                    walls.add(new int[] {x, y});
                    continue;
                }
                Animal a = Animal.fromLetter(c);
                if (a != null) {
                    (a == Animal.MOUSE ? mice : others).add(new Piece(a, x, y));
                }
            }
        }
        List<Piece> fixed = new ArrayList<>(mice);
        fixed.addAll(others);
        int hx = hole == null ? -1 : hole[0];
        int hy = hole == null ? -1 : hole[1];
        return new Level("test", "", rows.get(0).length(), rows.size(), hx, hy,
                walls, fixed, Collections.<Animal>emptyList(), Collections.<Piece>emptyList());
    }

    /** Draws where everything ended up (escaped animals are left off). */
    public static List<String> render(Level level, List<SimResult.Snapshot> frame) {
        char[][] g = new char[level.h][level.w];
        for (char[] row : g) {
            java.util.Arrays.fill(row, '.');
        }
        for (int[] p : level.walls) {
            g[p[1]][p[0]] = '#';
        }
        for (SimResult.Snapshot s : frame) {
            if (!s.gone) {
                g[s.y][s.x] = s.type.letter();
            }
        }
        List<String> out = new ArrayList<>();
        for (char[] row : g) {
            out.add(new String(row));
        }
        return out;
    }
}
