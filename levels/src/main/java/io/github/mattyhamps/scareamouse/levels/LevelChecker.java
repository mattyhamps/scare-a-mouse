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
 *   <li>every animal in your hand is needed;</li>
 *   <li>every solution moves at least {@code minMoved} animals (for chains where the mouse moves early);</li>
 *   <li>no clutter (except on hand-made teaching levels): every board animal, wall, turn tile, mousetrap and trapdoor pair affects the puzzle (remove any one and either the solution
 *       breaks or the puzzle gets easier);</li>
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
        if (hand.contains(Animal.MOUSE)) {
            return null; // there is only ever one mouse, and it's never in your hand
        }
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
        for (List<Piece> s : sols) {
            if (Simulator.run(level, s).moved < rules.minMoved) {
                return null; // a solution with too short a chain
            }
        }
        if (hand.size() >= 2) {
            for (int i = 0; i < hand.size(); i++) {
                if (i > 0 && hand.get(i) == hand.get(i - 1)) {
                    continue; // same smaller hand as the previous one
                }
                List<Animal> fewer = new ArrayList<>(hand);
                fewer.remove(i);
                if (!solutions(level, fewer, 1).isEmpty()) {
                    return null; // the level can be won without one of your animals
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
        for (int i = 0; i < level.turns.size(); i++) {
            parts.add(level.withoutTurn(i));
        }
        for (int i = 0; i < level.traps.size(); i++) {
            parts.add(level.withoutTrap(i));
        }
        if (!level.trapdoors.isEmpty()) {   // the trapdoor pair goes as one piece
            parts.add(level.withTrapdoors(java.util.Collections.<int[]>emptyList()));
        }
        for (Level part : rules.clutterCheck ? parts : java.util.Collections.<Level>emptyList()) {
            boolean stillWins = false;
            for (List<Piece> s : sols) {
                stillWins |= Simulator.run(part, s).win;
            }
            // A piece is clutter if taking it away changes nothing: the solutions still work and no new
            // ones open up. (Blockers and pinning animals pass, because removing them makes the puzzle easier.)
            if (stillWins && !puzzleChanges(part, hand, sols.size())) {
                return null;
            }
        }
        if (rules.mustMove != null && !boardAnimalMoves(level, sols.get(best), rules.mustMove)) {
            return null;
        }
        return new Verdict(sols.get(best), maxDepth, sols.size());
    }

    /** True if, without some piece, pressing Go with nothing placed wins, or more solutions exist than before. */
    private static boolean puzzleChanges(Level without, List<Animal> hand, int solutionsBefore) {
        if (Simulator.run(without, Collections.<Piece>emptyList()).win) {
            return true;
        }
        return solutions(without, hand, solutionsBefore + 1).size() > solutionsBefore;
    }

    /**
     * Every winning placement, up to {@code cap}, for any number of animals in hand.
     * Identical animals are never tried in swapped order, so each placement is counted once.
     */
    public static List<List<Piece>> solutions(Level level, List<Animal> hand, int cap) {
        List<int[]> open = level.openSquares();
        List<List<Piece>> out = new ArrayList<>();
        search(level, hand, open, 0, new int[hand.size()], new boolean[open.size()], cap, out);
        return out;
    }

    private static boolean search(Level level, List<Animal> hand, List<int[]> open, int k, int[] pick,
                                  boolean[] used, int cap, List<List<Piece>> out) {
        if (k == hand.size()) {
            List<Piece> p = new ArrayList<>(hand.size());
            for (int i = 0; i < hand.size(); i++) {
                p.add(new Piece(hand.get(i), open.get(pick[i])[0], open.get(pick[i])[1]));
            }
            if (Simulator.run(level, p).win) {
                out.add(p);
                return out.size() >= cap;
            }
            return false;
        }
        int start = k > 0 && hand.get(k) == hand.get(k - 1) ? pick[k - 1] + 1 : 0;
        for (int c = start; c < open.size(); c++) {
            if (used[c]) {
                continue;
            }
            used[c] = true;
            pick[k] = c;
            boolean full = search(level, hand, open, k + 1, pick, used, cap, out);
            used[c] = false;
            if (full) {
                return true;
            }
        }
        return false;
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
