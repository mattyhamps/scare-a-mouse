package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import java.util.ArrayList;
import java.util.List;

/**
 * How hard a level is to solve (not how much happens in it: that's {@link Interest}). What makes a
 * puzzle hard for a player: more animals to place, placements that don't touch anything already on the
 * board (stopping or steering a runner, putting a missing link back), tricks to see through, a long
 * chain, and walls in the way.
 */
public final class Difficulty {
    private static final int[][] DIRS = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};

    private Difficulty() {
    }

    public static double score(Level level) {
        Interest.Breakdown b = Interest.breakdown(level);
        return 4.0 * (level.inventory.size() - 1)
                + 3.0 * blindPlacements(level)
                + 2.0 * (b.freezeRelease + b.waitingRunner)
                + (b.wrapAround ? 3.0 : 0)
                + 0.5 * b.depth
                + 1.0 * level.walls.size()
                + 1.0 * level.turns.size()
                + 1.0 * level.traps.size();
    }

    /** Animals in the solution that start next to nothing on the board, so nothing points at their square. */
    static int blindPlacements(Level level) {
        int count = 0;
        for (Piece p : level.solution) {
            boolean touches = false;
            for (int[] d : DIRS) {
                for (Piece f : level.fixed) {
                    touches |= f.x == p.x + d[0] && f.y == p.y + d[1];
                }
            }
            if (!touches) {
                count++;
            }
        }
        return count;
    }

    /**
     * The extra-hard levels of one area (levels from..to, 1-based): the hardest few, about 1 in 15, not
     * counting the boss (it has its crown) or the first 10 levels of the game.
     */
    public static List<Integer> hardest(List<Level> levels, int from, int to, int boss) {
        List<double[]> scored = new ArrayList<>();
        for (int n = Math.max(from, 11); n <= to; n++) {
            if (n != boss) {
                scored.add(new double[] {n, score(levels.get(n - 1))});
            }
        }
        scored.sort((a, b) -> a[1] != b[1] ? Double.compare(b[1], a[1]) : Double.compare(a[0], b[0]));
        int want = Math.round((to - from + 1) / 15f);
        List<Integer> out = new ArrayList<>();
        for (int k = 0; k < want && k < scored.size(); k++) {
            out.add((int) scored.get(k)[0]);
        }
        out.sort(null);
        return out;
    }

    /**
     * The extra-hard levels of the whole game, area by area (each area ends with its boss, see
     * {@link Recipe#BOSSES}). The game marks them with a flame; data/hard-levels.json holds this list.
     */
    public static List<Integer> hardLevels(List<Level> levels) {
        List<Integer> out = new ArrayList<>();
        int from = 1;
        for (int boss : Recipe.BOSSES) {
            if (from > levels.size()) {
                break;
            }
            out.addAll(hardest(levels, from, Math.min(boss, levels.size()), boss));
            from = boss + 1;
        }
        return out;
    }
}
