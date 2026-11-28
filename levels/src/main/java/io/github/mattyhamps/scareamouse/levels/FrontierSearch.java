package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.SimResult;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Finds the winning placements for a hand of animals without trying every square for every animal, so
 * hands of 4 and 5 can be checked (docs/HARDER_CASTLE.md, "Making 4 and 5 animals possible").
 *
 * <p>Why it finds the same placements as trying everything: an animal you place changes nothing until some
 * animal comes next to its square (only touching animals scare, freeze or block each other, and an animal can
 * only step onto a square next to it). So in any run, the first of your animals to be touched is touched at a
 * moment when the board has played out exactly as it would without it, so its square is next to where some
 * animal stood in that shorter run. The same holds for the next one, given the ones before it. The search
 * adds your animals in the order they are first touched, each one on a square that the run so far reaches
 * at or after the previous one's step (animals touched at the same step go in square order, unless one is
 * only reached thanks to the other). The one exception: two of your animals placed side by side, where one
 * scares the other, start each other off with nothing else near; the search tries such pairs anywhere
 * before anything touched later. A placement found twice is kept once.
 *
 * <p>A run that already wins with animals still in your hand is finished by trying the rest everywhere, like
 * the full search, since an animal nothing touches doesn't change the win. Results are sorted in the full
 * search's order. While there are fewer winning placements than {@code cap}, it returns exactly the same list
 * as the full search; when there are at least {@code cap}, it returns {@code cap} of them (not always the same
 * ones), which is all the checker needs to know. {@code FrontierSearchTest} compares the two.
 */
final class FrontierSearch {
    private final Level level;
    private final List<Animal> hand;
    private final int cap;
    private final List<int[]> open;
    private final int[] openIndex;   // board square -> index in open, or -1
    private final Map<String, List<Piece>> found = new LinkedHashMap<>();
    static final boolean PAIRS = !Boolean.getBoolean("frontier.noPairs");   // testing only

    private FrontierSearch(Level level, List<Animal> hand, int cap) {
        this.level = level;
        this.hand = hand;
        this.cap = cap;
        this.open = level.openSquares();
        this.openIndex = new int[level.w * level.h];
        Arrays.fill(openIndex, -1);
        for (int i = 0; i < open.size(); i++) {
            openIndex[open.get(i)[1] * level.w + open.get(i)[0]] = i;
        }
    }

    static List<List<Piece>> solutions(Level level, List<Animal> hand, int cap) {
        FrontierSearch s = new FrontierSearch(level, hand, cap);
        Map<Animal, Integer> left = new LinkedHashMap<>();
        for (Animal a : hand) {
            left.merge(a, 1, Integer::sum);
        }
        s.search(new ArrayList<Piece>(), new boolean[s.open.size()], left, -1, -1, null, -1);
        return s.sorted();
    }

    private boolean full() {
        return found.size() >= cap;
    }

    /**
     * Adds the next animal. prevStep and prevSquare: when and where the animal placed last is first touched;
     * parentFirst: the touch steps before it was placed (to put animals touched at the same step in one order).
     * partnerOf: if not -1, the animal placed last sits where nothing touches it, so this one has to go next to
     * it and scare it or be scared by it (two of your animals that start each other off).
     */
    private void search(List<Piece> placed, boolean[] used, Map<Animal, Integer> left, int prevStep, int prevSquare,
                        int[] parentFirst, int partnerOf) {
        if (full()) {
            return;
        }
        boolean done = left.values().stream().allMatch(v -> v == 0);
        int[][] dirs = {{0, 0}, {0, -1}, {1, 0}, {0, 1}, {-1, 0}};
        if (partnerOf >= 0) {
            // only next to the lone animal, and only an animal it fears or that fears it (no need to run the
            // board first: the lone animal changes nothing on its own)
            Animal lone = placed.get(placed.size() - 1).type;
            int[] sq = open.get(partnerOf);
            for (int d = 1; d < 5 && !full() && !done; d++) {
                int x = sq[0] + dirs[d][0];
                int y = sq[1] + dirs[d][1];
                int i = x >= 0 && y >= 0 && x < level.w && y < level.h ? openIndex[y * level.w + x] : -1;
                if (i < 0 || used[i]) {
                    continue;
                }
                for (Map.Entry<Animal, Integer> e : left.entrySet()) {
                    if (e.getValue() == 0 || (e.getKey() != lone.predator() && e.getKey().predator() != lone)) {
                        continue;
                    }
                    place(placed, used, left, e, i, 0, -1, null, -1);
                }
            }
            return;
        }
        if (done) {
            if (Simulator.run(level, placed).win) {
                add(placed);
            }
            return;
        }
        SimResult r = Simulator.record(level, placed);
        if (r.win) {
            // Wins already: the rest of your hand can go anywhere nothing touches (and maybe elsewhere too).
            List<Animal> rest = new ArrayList<>();
            for (Animal x : hand) {
                rest.add(x);
            }
            for (Piece p : placed) {
                rest.remove(p.type);
            }
            complete(placed, used, rest, 0, -1);
            return;
        }
        // The step at which each open square is first next to (or under) an animal in this run.
        int[] first = new int[open.size()];
        Arrays.fill(first, Integer.MAX_VALUE);
        for (int t = 0; t < r.frames.size(); t++) {
            for (SimResult.Snapshot a : r.frames.get(t)) {
                if (a.gone) {
                    continue;
                }
                for (int[] d : dirs) {
                    int x = a.x + d[0];
                    int y = a.y + d[1];
                    if (x >= 0 && y >= 0 && x < level.w && y < level.h) {
                        int i = openIndex[y * level.w + x];
                        if (i >= 0 && first[i] > t) {
                            first[i] = t;
                        }
                    }
                }
            }
        }
        for (int i = 0; i < open.size() && !full(); i++) {
            if (used[i] || first[i] == Integer.MAX_VALUE) {
                continue;
            }
            if (first[i] < prevStep) {
                continue;   // it would be touched before the animal placed last: that order is tried elsewhere
            }
            if (first[i] == prevStep && i < prevSquare && parentFirst != null && parentFirst[i] == prevStep) {
                continue;   // touched at the same step without the last animal's help: tried in the other order
            }
            for (Map.Entry<Animal, Integer> e : left.entrySet()) {
                if (e.getValue() > 0) {
                    place(placed, used, left, e, i, first[i], i, first, -1);
                }
            }
        }
        // Two of your animals can start each other off where nothing else touches them: one here, and the
        // next one next to it. Such a pair is touched at the very start, so only before anything touched later.
        if (prevStep <= 0 && PAIRS) {
            for (int i = 0; i < open.size() && !full(); i++) {
                if (used[i] || first[i] != Integer.MAX_VALUE) {
                    continue;
                }
                for (Map.Entry<Animal, Integer> e : left.entrySet()) {
                    if (e.getValue() > 0) {
                        place(placed, used, left, e, i, 0, -1, null, i);
                    }
                }
            }
        }
    }

    private void place(List<Piece> placed, boolean[] used, Map<Animal, Integer> left, Map.Entry<Animal, Integer> e, int i,
                       int step, int square, int[] first, int partnerOf) {
        if (full()) {
            return;
        }
        used[i] = true;
        e.setValue(e.getValue() - 1);
        placed.add(new Piece(e.getKey(), open.get(i)[0], open.get(i)[1]));
        search(placed, used, left, step, square, first, partnerOf);
        placed.remove(placed.size() - 1);
        e.setValue(e.getValue() + 1);
        used[i] = false;
    }

    /** Tries the rest of the hand on every free square (the same way as the full search). */
    private void complete(List<Piece> placed, boolean[] used, List<Animal> rest, int k, int prevIndex) {
        if (full()) {
            return;
        }
        if (k == rest.size()) {
            if (Simulator.run(level, placed).win) {
                add(placed);
            }
            return;
        }
        int start = k > 0 && rest.get(k) == rest.get(k - 1) ? prevIndex + 1 : 0;
        for (int i = start; i < open.size() && !full(); i++) {
            if (used[i]) {
                continue;
            }
            used[i] = true;
            placed.add(new Piece(rest.get(k), open.get(i)[0], open.get(i)[1]));
            complete(placed, used, rest, k + 1, i);
            placed.remove(placed.size() - 1);
            used[i] = false;
        }
    }

    /** Stores a placement once, in the full search's form: pieces in hand order, the same animals by square. */
    private void add(List<Piece> placed) {
        int[] key = key(placed);
        StringBuilder s = new StringBuilder();
        for (int v : key) {
            s.append(v).append(',');
        }
        if (!found.containsKey(s.toString())) {
            List<Piece> p = new ArrayList<>();
            for (int i = 0; i < hand.size(); i++) {
                int[] sq = open.get(key[i]);
                p.add(new Piece(hand.get(i), sq[0], sq[1]));
            }
            found.put(s.toString(), p);
        }
    }

    /** For each animal in the hand, in order, the open-square index of its piece (the same animals take squares in order). */
    private int[] key(List<Piece> placed) {
        boolean[] taken = new boolean[placed.size()];
        int[] key = new int[hand.size()];
        for (int i = 0; i < hand.size(); i++) {
            int best = -1;
            for (int j = 0; j < placed.size(); j++) {
                Piece p = placed.get(j);
                if (!taken[j] && p.type == hand.get(i)) {
                    int idx = openIndex[p.y * level.w + p.x];
                    if (best < 0 || idx < openIndex[placed.get(best).y * level.w + placed.get(best).x]) {
                        best = j;
                    }
                }
            }
            taken[best] = true;
            key[i] = openIndex[placed.get(best).y * level.w + placed.get(best).x];
        }
        return key;
    }

    private List<List<Piece>> sorted() {
        List<int[]> keys = new ArrayList<>();
        Map<String, List<Piece>> byKey = new LinkedHashMap<>();
        for (Map.Entry<String, List<Piece>> e : found.entrySet()) {
            keys.add(key(e.getValue()));
            byKey.put(Arrays.toString(keys.get(keys.size() - 1)), e.getValue());
        }
        keys.sort(Arrays::compare);
        List<List<Piece>> out = new ArrayList<>();
        for (int[] k : keys) {
            out.add(byKey.get(Arrays.toString(k)));
        }
        return out;
    }
}
