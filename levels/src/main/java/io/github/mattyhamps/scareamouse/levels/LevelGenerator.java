package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Builds random 7x7 layouts and keeps the first one that passes {@link LevelChecker}.
 * Runs one search per CPU core in parallel, each with its own seed; the seed of the winner is
 * reported so a result can be reproduced with a single thread.
 */
public final class LevelGenerator {
    public static final int SIZE = 7;

    private LevelGenerator() {
    }

    /** Same simple generator the original JavaScript tools used (a 32-bit linear congruential RNG). */
    static final class Rng {
        private long state;

        Rng(long seed) {
            state = seed & 0xFFFFFFFFL;
        }

        double next() {
            state = (state * 1664525L + 1013904223L) & 0xFFFFFFFFL;
            return state / 4294967296.0;
        }

        int between(int lo, int hi) {
            return lo + (int) Math.floor(next() * (hi - lo + 1));
        }

        <T> T pick(List<T> list) {
            return list.get((int) Math.floor(next() * list.size()));
        }
    }

    /** Result of a search. */
    public static final class Found {
        public final Level level;
        public final LevelChecker.Verdict verdict;
        public final long seed;
        public final long tries;

        Found(Level level, LevelChecker.Verdict verdict, long seed, long tries) {
            this.level = level;
            this.verdict = verdict;
            this.seed = seed;
            this.tries = tries;
        }
    }

    /** One random layout following the rules (not checked). */
    static Level randomLayout(Rng r, LevelRules rules, String name, String tip) {
        List<int[]> cells = new ArrayList<>();
        for (int y = 0; y < SIZE; y++) {
            for (int x = 0; x < SIZE; x++) {
                cells.add(new int[] {x, y});
            }
        }
        for (int i = cells.size() - 1; i > 0; i--) {
            int j = (int) Math.floor(r.next() * (i + 1));
            Collections.swap(cells, i, j);
        }
        int k = 0;
        List<int[]> walls = new ArrayList<>();
        for (int i = r.between(rules.wallsMin, rules.wallsMax); i > 0; i--) {
            walls.add(cells.get(k++));
        }
        List<Piece> fixed = new ArrayList<>();
        int[] m = cells.get(k++);
        fixed.add(new Piece(Animal.MOUSE, m[0], m[1]));
        for (int i = r.between(rules.fixedMin, rules.fixedMax); i > 0; i--) {
            int[] c = cells.get(k++);
            fixed.add(new Piece(r.pick(rules.types), c[0], c[1]));
        }
        for (int i = 0; i < rules.ensure.size() && i + 1 < fixed.size(); i++) {
            Piece p = fixed.get(i + 1);
            fixed.set(i + 1, new Piece(rules.ensure.get(i), p.x, p.y));
        }
        List<Animal> hand = new ArrayList<>();
        for (int i = 0; i < rules.pieces; i++) {
            hand.add(r.pick(rules.handTypes));
        }
        if (rules.mustPlace != null) {
            hand.set(0, rules.mustPlace);
        }
        hand.sort((a, b) -> a.id().compareTo(b.id()));
        int[] hole = r.pick(borderCells());
        return new Level(name, tip, SIZE, SIZE, hole[0], hole[1], walls, fixed, hand, Collections.<Piece>emptyList());
    }

    private static List<int[]> borderCells() {
        List<int[]> out = new ArrayList<>();
        for (int i = 0; i < SIZE; i++) {
            out.add(new int[] {i, -1});
            out.add(new int[] {i, SIZE});
            out.add(new int[] {-1, i});
            out.add(new int[] {SIZE, i});
        }
        return out;
    }

    /** Single-threaded search from one seed. Gives up after maxTries (returns null). */
    public static Found search(LevelRules rules, long seed, long maxTries, String name, String tip) {
        Rng r = new Rng(seed);
        for (long t = 1; t <= maxTries; t++) {
            Level candidate = randomLayout(r, rules, name, tip);
            LevelChecker.Verdict v = LevelChecker.check(candidate, rules);
            if (v != null) {
                return new Found(candidate.withSolution(v.solution), v, seed, t);
            }
        }
        return null;
    }

    /**
     * Parallel search: one worker per thread, seeds baseSeed, baseSeed+1, ... Stops as soon as one
     * worker finds a level, or after timeoutSeconds (returns null).
     */
    public static Found searchParallel(LevelRules rules, long baseSeed, int threads, long timeoutSeconds,
                                       String name, String tip) throws InterruptedException {
        AtomicReference<Found> winner = new AtomicReference<>();
        AtomicLong totalTries = new AtomicLong();
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        for (int t = 0; t < threads; t++) {
            final long seed = baseSeed + t;
            pool.submit(() -> {
                Rng r = new Rng(seed);
                long tries = 0;
                while (winner.get() == null && !Thread.currentThread().isInterrupted()) {
                    Level candidate = randomLayout(r, rules, name, tip);
                    tries++;
                    LevelChecker.Verdict v = LevelChecker.check(candidate, rules);
                    if (v != null) {
                        winner.compareAndSet(null, new Found(candidate.withSolution(v.solution), v, seed, tries));
                    }
                }
                totalTries.addAndGet(tries);
            });
        }
        pool.shutdown();
        long deadline = System.currentTimeMillis() + timeoutSeconds * 1000;
        while (winner.get() == null && System.currentTimeMillis() < deadline && !pool.isTerminated()) {
            pool.awaitTermination(200, TimeUnit.MILLISECONDS);
        }
        pool.shutdownNow();
        pool.awaitTermination(10, TimeUnit.SECONDS);
        return winner.get();
    }
}
