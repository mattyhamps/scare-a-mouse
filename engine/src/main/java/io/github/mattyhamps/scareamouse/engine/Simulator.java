package io.github.mattyhamps.scareamouse.engine;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The game's physics. This class is the single source of truth: the game (compiled to
 * JavaScript with TeaVM), the level generator, the level checker and the tests all use it.
 *
 * <h2>Rulebook</h2>
 * <ol start="0">
 *   <li><b>Food chain:</b> mouse &lt; cat &lt; dog &lt; bear &lt; lion &lt; elephant &lt; mouse.
 *       Each animal fears only the next one up (and elephants fear mice).</li>
 *   <li><b>Steps:</b> every animal moves at most one square per step, all at the same time.</li>
 *   <li><b>Scared:</b> if exactly one animal it fears is touching it (side by side, not diagonal),
 *       it runs straight away from that animal.</li>
 *   <li><b>Frozen:</b> if two or more animals it fears are touching it, it doesn't move. It starts
 *       running again (rule 2) once only one is touching it.</li>
 *   <li><b>Blocked:</b> when a running animal's next square holds another animal, it waits and keeps
 *       its direction; if the square clears, it keeps going. It only stops for good at a wall, the
 *       castle edge, or (for every animal but the mouse) the hole. If two animals would step into
 *       the same square at the same time, neither moves that step.</li>
 *   <li><b>Passing by:</b> a running animal that ends up beside an animal it fears turns and runs away
 *       from it (rules 2 and 3 are checked at the start of every step).</li>
 *   <li><b>The hole:</b> a square on the board. Only the mouse can go into it, and the mouse getting
 *       in wins the level. Every other animal treats it like a wall.</li>
 *   <li><b>Turn tiles:</b> an animal that runs onto a turn tile heads the way its arrow points from
 *       then on (unless something scares it, as usual). Animals can't be placed on them.</li>
 * </ol>
 * The run ends when the mouse gets into the hole, when a step passes with nothing moving, or when the
 * board repeats an earlier state (an endless loop).
 */
public final class Simulator {
    /** Up, right, down, left. */
    private static final int[][] DIRS = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};
    public static final int MAX_STEPS = 300;

    private Simulator() {
    }

    public static SimResult run(Level level, List<Piece> placed) {
        return simulate(level, placed, false);
    }

    public static SimResult record(Level level, List<Piece> placed) {
        return simulate(level, placed, true);
    }

    public static SimResult simulate(Level level, List<Piece> placed, boolean record) {
        final int w = level.w;
        final int h = level.h;
        final boolean[] wall = new boolean[w * h];
        for (int[] p : level.walls) {
            wall[p[1] * w + p[0]] = true;
        }
        final int[] turn = new int[w * h];   // arrow direction, or -1
        java.util.Arrays.fill(turn, -1);
        for (int[] t : level.turns) {
            turn[t[1] * w + t[0]] = t[2];
        }

        List<Piece> all = new ArrayList<>(level.fixed);
        all.addAll(placed);
        final int n = all.size();
        final Animal[] type = new Animal[n];
        final int[] x = new int[n];
        final int[] y = new int[n];
        final int[] dx = new int[n];
        final int[] dy = new int[n];
        final boolean[] gone = new boolean[n];
        final int[] grid = new int[w * h];
        java.util.Arrays.fill(grid, -1);
        for (int i = 0; i < n; i++) {
            Piece p = all.get(i);
            type[i] = p.type;
            x[i] = p.x;
            y[i] = p.y;
            grid[p.y * w + p.x] = i;
        }

        List<List<SimResult.Snapshot>> frames = record ? new ArrayList<>() : null;
        List<List<Integer>> bumps = record ? new ArrayList<>() : null;
        if (record) {
            frames.add(snap(type, x, y, gone));
            bumps.add(new ArrayList<Integer>());
        }
        boolean[] everMoved = new boolean[n];
        Set<String> seen = new HashSet<>();

        for (int tick = 0; tick < MAX_STEPS; tick++) {
            // Rules 2, 3, 5: scare check from positions at the start of the step.
            for (int i = 0; i < n; i++) {
                if (gone[i]) {
                    continue;
                }
                Animal fear = type[i].predator();
                int count = 0;
                int fx = 0;
                int fy = 0;
                for (int[] d : DIRS) {
                    int j = at(grid, w, h, x[i] + d[0], y[i] + d[1]);
                    if (j >= 0 && type[j] == fear) {
                        count++;
                        if (count == 1) {
                            fx = -d[0];
                            fy = -d[1];
                        }
                    }
                }
                if (count == 1) {
                    dx[i] = fx;
                    dy[i] = fy;
                } else if (count > 1) { // frozen
                    dx[i] = 0;
                    dy[i] = 0;
                }
            }
            // Rule 4: a runner facing a wall, the edge, or (for non-mice) the hole stops for good.
            for (int i = 0; i < n; i++) {
                if (!gone[i] && (dx[i] != 0 || dy[i] != 0)
                        && solid(level, wall, type[i], x[i] + dx[i], y[i] + dy[i])) {
                    dx[i] = 0;
                    dy[i] = 0;
                }
            }

            // Loop detection: the same positions and directions as before means it would repeat forever.
            StringBuilder key = new StringBuilder();
            for (int i = 0; i < n; i++) {
                if (i > 0) {
                    key.append(';');
                }
                if (!gone[i]) {
                    key.append(x[i]).append(',').append(y[i]).append(',').append(dx[i]).append(',').append(dy[i]);
                }
            }
            if (!seen.add(key.toString())) {
                return new SimResult(false, true, count(everMoved), 0, frames, bumps);
            }

            List<Integer> runners = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                if (!gone[i] && (dx[i] != 0 || dy[i] != 0)) {
                    runners.add(i);
                }
            }
            if (runners.isEmpty()) {
                break;
            }

            // Rule 4: two animals stepping into the same square => neither moves.
            Map<Integer, Integer> claims = new HashMap<>();
            for (int i : runners) {
                claims.merge(cellKey(x[i] + dx[i], y[i] + dy[i]), 1, Integer::sum);
            }
            List<Integer> pending = new ArrayList<>();
            List<Integer> standoff = new ArrayList<>(); // blocked this step by another animal heading for the same square
            for (int i : runners) {
                if (claims.get(cellKey(x[i] + dx[i], y[i] + dy[i])) == 1) {
                    pending.add(i);
                } else {
                    standoff.add(i);
                }
            }

            // Move everything whose square is free, repeating so a line of animals can follow each other.
            boolean[] done = new boolean[n];
            boolean anyDone = false;
            boolean won = false;
            boolean progress = true;
            while (progress) {
                progress = false;
                for (int i : pending) {
                    if (done[i]) {
                        continue;
                    }
                    int nx = x[i] + dx[i];
                    int ny = y[i] + dy[i];
                    if (type[i] == Animal.MOUSE && nx == level.holeX && ny == level.holeY) {
                        grid[y[i] * w + x[i]] = -1;
                        x[i] = nx;
                        y[i] = ny;
                        gone[i] = true;
                        dx[i] = 0;
                        dy[i] = 0;
                        done[i] = true;
                        anyDone = true;
                        progress = true;
                        won = true;
                        continue;
                    }
                    if (at(grid, w, h, nx, ny) < 0) {
                        grid[y[i] * w + x[i]] = -1;
                        x[i] = nx;
                        y[i] = ny;
                        grid[ny * w + nx] = i;
                        if (turn[ny * w + nx] >= 0) {   // rule 7: the arrow sets the new heading
                            dx[i] = DIRS[turn[ny * w + nx]][0];
                            dy[i] = DIRS[turn[ny * w + nx]][1];
                        }
                        done[i] = true;
                        anyDone = true;
                        progress = true;
                    }
                }
            }
            // Anything that didn't move is waiting behind an animal: it keeps its direction (rule 4).
            for (int i = 0; i < n; i++) {
                if (done[i]) {
                    everMoved[i] = true;
                }
            }
            if (record) {
                frames.add(snap(type, x, y, gone));
                bumps.add(standoff);
            }
            if (won) {
                return new SimResult(true, false, count(everMoved), tick + 1, frames, bumps);
            }
            if (!anyDone) {
                break; // nothing moved: the board is settled
            }
        }
        return new SimResult(false, false, count(everMoved), 0, frames, bumps);
    }

    /** Walls, the castle edge, and the hole for anything but the mouse. */
    private static boolean solid(Level level, boolean[] wall, Animal type, int nx, int ny) {
        if (type == Animal.MOUSE && nx == level.holeX && ny == level.holeY) {
            return false;
        }
        if (nx == level.holeX && ny == level.holeY) {
            return true;
        }
        return nx < 0 || ny < 0 || nx >= level.w || ny >= level.h || wall[ny * level.w + nx];
    }

    private static int at(int[] grid, int w, int h, int x, int y) {
        return x < 0 || y < 0 || x >= w || y >= h ? -1 : grid[y * w + x];
    }

    private static int cellKey(int x, int y) {
        return (x + 2) * 1000 + (y + 2);
    }

    private static int count(boolean[] flags) {
        int c = 0;
        for (boolean f : flags) {
            if (f) {
                c++;
            }
        }
        return c;
    }

    private static List<SimResult.Snapshot> snap(Animal[] type, int[] x, int[] y, boolean[] gone) {
        List<SimResult.Snapshot> f = new ArrayList<>(type.length);
        for (int i = 0; i < type.length; i++) {
            f.add(new SimResult.Snapshot(i, type[i], x[i], y[i], gone[i]));
        }
        return f;
    }
}
