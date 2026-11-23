package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.SimResult;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Decides whether a level is a good puzzle:
 * <ul>
 *   <li>pressing Go with nothing placed doesn't win;</li>
 *   <li>it has at least one and at most {@code maxSolutions} solutions;</li>
 *   <li>no shortcuts: in every solution, at least {@code minDepth} other animals start running before the mouse;</li>
 *   <li>with two animals to place, both are needed;</li>
 *   <li>no clutter: every board animal and wall matters in every solution (remove any one and that solution fails);</li>
 *   <li>for intro levels, the animal being introduced actually moves.</li>
 * </ul>
 */
public final class LevelChecker {
    private LevelChecker() {
    }

    /** Result of a successful check. */
    public static final class Verdict {
        public final List<Piece> solution;
        public final int depth;
        public final int solutions;

        Verdict(List<Piece> solution, int depth, int solutions) {
            this.solution = solution;
            this.depth = depth;
            this.solutions = solutions;
        }
    }

    /** Returns null if the level fails any rule. */
    public static Verdict check(Level level, LevelRules rules) {
        List<Animal> hand = level.inventory;
        if (Simulator.run(level, Collections.<Piece>emptyList()).win) {
            return null;
        }
        List<List<Piece>> sols = solutions(level, hand, rules.maxSolutions + 1);
        if (sols.isEmpty() || sols.size() > rules.maxSolutions) {
            return null;
        }
        int[] depths = new int[sols.size()];
        int minDepth = Integer.MAX_VALUE;
        int maxDepth = -1;
        int best = 0;
        for (int k = 0; k < sols.size(); k++) {
            depths[k] = depth(level, sols.get(k));
            minDepth = Math.min(minDepth, depths[k]);
            if (depths[k] > maxDepth) {
                maxDepth = depths[k];
                best = k;
            }
        }
        if (minDepth < rules.minDepth) {
            return null; // a shortcut exists
        }
        if (hand.size() == 2) {
            for (Animal a : hand) {
                if (!solutions(level, Arrays.asList(a), 1).isEmpty()) {
                    return null; // one animal alone is enough
                }
            }
        }
        List<Level> parts = new ArrayList<>();
        for (int i = 1; i < level.fixed.size(); i++) {
            parts.add(level.withoutFixed(i));
        }
        for (int i = 0; i < level.walls.size(); i++) {
            parts.add(level.withoutWall(i));
        }
        for (List<Piece> s : sols) {
            for (Level part : parts) {
                if (Simulator.run(part, s).win) {
                    return null; // something on the board doesn't matter for this solution
                }
            }
        }
        if (rules.mustMove != null && !boardAnimalMoves(level, sols.get(best), rules.mustMove)) {
            return null;
        }
        return new Verdict(sols.get(best), maxDepth, sols.size());
    }

    /** Every winning placement, up to {@code cap}. Supports one or two animals in hand. */
    public static List<List<Piece>> solutions(Level level, List<Animal> hand, int cap) {
        List<int[]> open = level.openSquares();
        List<List<Piece>> out = new ArrayList<>();
        if (hand.size() == 1) {
            for (int[] c : open) {
                List<Piece> p = Arrays.asList(new Piece(hand.get(0), c[0], c[1]));
                if (Simulator.run(level, p).win) {
                    out.add(p);
                    if (out.size() >= cap) {
                        return out;
                    }
                }
            }
        } else if (hand.size() == 2) {
            boolean same = hand.get(0) == hand.get(1);
            for (int i = 0; i < open.size(); i++) {
                for (int j = same ? i + 1 : 0; j < open.size(); j++) {
                    if (i == j) {
                        continue;
                    }
                    List<Piece> p = Arrays.asList(
                            new Piece(hand.get(0), open.get(i)[0], open.get(i)[1]),
                            new Piece(hand.get(1), open.get(j)[0], open.get(j)[1]));
                    if (Simulator.run(level, p).win) {
                        out.add(p);
                        if (out.size() >= cap) {
                            return out;
                        }
                    }
                }
            }
        } else {
            throw new IllegalArgumentException("Only 1 or 2 animals in hand are supported");
        }
        return out;
    }

    /** How many animals (other than the mouse) start running before the mouse does. */
    public static int depth(Level level, List<Piece> placed) {
        List<List<SimResult.Snapshot>> frames = Simulator.record(level, placed).frames;
        int n = frames.get(0).size();
        int[] start = new int[n];
        Arrays.fill(start, -1);
        for (int f = 1; f < frames.size(); f++) {
            for (int id = 0; id < n; id++) {
                SimResult.Snapshot a = frames.get(f).get(id);
                SimResult.Snapshot b = frames.get(f - 1).get(id);
                if (start[id] < 0 && (a.x != b.x || a.y != b.y)) {
                    start[id] = f;
                }
            }
        }
        int mouse = start[0]; // the mouse is always listed first
        int count = 0;
        for (int id = 1; id < n; id++) {
            if (start[id] >= 0 && start[id] < mouse) {
                count++;
            }
        }
        return count;
    }

    private static boolean boardAnimalMoves(Level level, List<Piece> solution, Animal type) {
        List<List<SimResult.Snapshot>> frames = Simulator.record(level, solution).frames;
        List<SimResult.Snapshot> first = frames.get(0);
        for (SimResult.Snapshot s : first) {
            if (s.type != type || s.id >= level.fixed.size()) {
                continue;
            }
            for (List<SimResult.Snapshot> f : frames) {
                if (f.get(s.id).x != s.x || f.get(s.id).y != s.y) {
                    return true;
                }
            }
        }
        return false;
    }
}
