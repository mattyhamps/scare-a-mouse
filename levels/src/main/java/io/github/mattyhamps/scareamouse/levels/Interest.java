package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.SimResult;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.util.List;

/**
 * Scores how interesting a (valid) level is, so the builder can pick its best candidate and a
 * batch can be ordered from easiest to hardest. Higher is more interesting.
 */
public final class Interest {
    private static final int[][] DIRS = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};

    private Interest() {
    }

    /** Counts of what happens in the intended solution. */
    public static final class Breakdown {
        public int moved;
        public int depth;
        public int freezeRelease;
        public int waitingRunner;
        public boolean wrapAround;
        public int turns;
        public int distance;
        public int steps;
        public int hand;

        public double score() {
            return 3 * moved + 2 * depth + 4 * freezeRelease + 4 * waitingRunner + (wrapAround ? 6 : 0)
                    + turns + 0.5 * distance + 0.1 * steps + 2 * (hand - 1);
        }

        @Override
        public String toString() {
            return String.format("score %.1f: %d animals move, depth %d, %d freeze-release, %d waiting-runner%s, "
                            + "%d turns, %d steps, %d in hand",
                    score(), moved, depth, freezeRelease, waitingRunner, wrapAround ? ", wrap-around" : "",
                    turns, steps, hand);
        }
    }

    public static double score(Level level) {
        return breakdown(level).score();
    }

    public static Breakdown breakdown(Level level) {
        Breakdown b = new Breakdown();
        SimResult r = Simulator.record(level, level.solution);
        List<List<SimResult.Snapshot>> f = r.frames;
        b.moved = r.moved;
        b.steps = f.size() - 1;
        b.hand = level.inventory.size();
        b.depth = LevelChecker.depth(level, level.solution);
        List<SimResult.Snapshot> start = f.get(0);
        for (SimResult.Snapshot a : start) {
            int touching = 0;
            for (int[] d : DIRS) {
                for (SimResult.Snapshot o : start) {
                    if (o.x == a.x + d[0] && o.y == a.y + d[1] && o.type == a.type.predator()) {
                        touching++;
                    }
                }
            }
            int first = firstMove(f, a.id);
            if (touching >= 2 && first > 0) {
                b.freezeRelease++;
            } else if (touching == 1 && first > 1) {
                b.waitingRunner++;
            }
            b.turns += turns(f, a.id);
        }
        b.wrapAround = mouseRuns(f) >= 2;
        int mx = start.get(0).x;
        int my = start.get(0).y;
        int best = Integer.MAX_VALUE;
        for (Piece p : level.solution) {
            best = Math.min(best, Math.abs(p.x - mx) + Math.abs(p.y - my));
        }
        b.distance = best == Integer.MAX_VALUE ? 0 : best;
        return b;
    }

    private static int firstMove(List<List<SimResult.Snapshot>> f, int id) {
        for (int k = 1; k < f.size(); k++) {
            if (f.get(k).get(id).x != f.get(k - 1).get(id).x || f.get(k).get(id).y != f.get(k - 1).get(id).y) {
                return k;
            }
        }
        return -1;
    }

    private static int turns(List<List<SimResult.Snapshot>> f, int id) {
        int turns = 0;
        int pdx = 0;
        int pdy = 0;
        for (int k = 1; k < f.size(); k++) {
            int dx = f.get(k).get(id).x - f.get(k - 1).get(id).x;
            int dy = f.get(k).get(id).y - f.get(k - 1).get(id).y;
            if (dx == 0 && dy == 0 || f.get(k).get(id).gone) {
                continue;
            }
            if ((pdx != 0 || pdy != 0) && (dx != pdx || dy != pdy)) {
                turns++;
            }
            pdx = dx;
            pdy = dy;
        }
        return turns;
    }

    private static int mouseRuns(List<List<SimResult.Snapshot>> f) {
        int runs = 0;
        boolean moving = false;
        for (int k = 1; k < f.size(); k++) {
            SimResult.Snapshot a = f.get(k).get(0);
            SimResult.Snapshot b = f.get(k - 1).get(0);
            boolean moved = (a.x != b.x || a.y != b.y) && a.type == Animal.MOUSE;
            if (moved && !moving) {
                runs++;
            }
            moving = moved;
        }
        return runs;
    }
}
