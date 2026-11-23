package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.SimResult;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Designs a level on purpose instead of hoping a random board is good.
 *
 * <p>It builds the chain forward from the first animal you place, one link at a time. After every
 * placement it runs the simulator to confirm the new link really gets scared, at the right moment,
 * and that nothing on the board moves before you place anything. Tricks from the {@link Recipe}
 * are built in as special links. The chain ends with the mouse beside the last runner's path and
 * the hole straight ahead of it. Recipes can also put animals in the mouse's path to the hole, each
 * cleared by its own short chain that you start ("clear the path"), which is how you get more
 * animals in hand. {@link LevelChecker} still has the final say on every level.
 */
public final class ChainBuilder {
    static final int N = 7;
    private static final int[][] DIRS = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};
    private static final int TRIES_PER_STEP = 40;

    private ChainBuilder() {
    }

    /** One planned step of the chain. */
    private static final class Step {
        final Recipe.Trick trick;
        final Animal runner;   // the chain animal placed by this step (the blocker for WAITING_RUNNER)
        final Animal next;     // FREEZE_RELEASE / WAITING_RUNNER: the animal that bolts afterwards
        final Animal guard;    // FREEZE_RELEASE / WAITING_RUNNER: the static predator that holds it

        Step(Recipe.Trick trick, Animal runner, Animal next, Animal guard) {
            this.trick = trick;
            this.runner = runner;
            this.next = next;
            this.guard = guard;
        }
    }

    /** A level under construction. */
    private static final class Draft {
        final List<Piece> fixed = new ArrayList<>();
        final List<Piece> placed = new ArrayList<>();
        final List<Integer> chain = new ArrayList<>();   // fixed indices, in chain order
        final List<Integer> guards = new ArrayList<>();  // fixed indices
        int holeX = -1;                                  // (-1,-1) is a corner, so no hole yet
        int holeY = -1;

        Level level() {
            return new Level("", "", N, N, holeX, holeY, Collections.<int[]>emptyList(), fixed,
                    Collections.<Animal>emptyList(), Collections.<Piece>emptyList());
        }

        boolean free(int x, int y) {
            if (x < 0 || y < 0 || x >= N || y >= N) {
                return false;
            }
            for (Piece p : fixed) {
                if (p.x == x && p.y == y) {
                    return false;
                }
            }
            for (Piece p : placed) {
                if (p.x == x && p.y == y) {
                    return false;
                }
            }
            return true;
        }

        int add(Animal type, int x, int y) {
            fixed.add(new Piece(type, x, y));
            return fixed.size() - 1;
        }

        void removeLast(int count) {
            for (int k = 0; k < count; k++) {
                int idx = fixed.size() - 1;
                fixed.remove(idx);
                chain.remove(Integer.valueOf(idx));
                guards.remove(Integer.valueOf(idx));
            }
        }
    }

    /** Builds one candidate level for the recipe, or returns null if this attempt got stuck. */
    static Level build(Recipe recipe, LevelGenerator.Rng rng, String name) {
        List<Step> plan = plan(recipe, rng);
        if (plan == null) {
            return null;
        }
        Draft d = new Draft();
        boolean wrap = recipe.wrapAround;

        // First link: your first animal right behind the first chain animal.
        boolean placedFirst = false;
        for (int t = 0; t < TRIES_PER_STEP && !placedFirst; t++) {
            int x = 1 + (int) (rng.next() * (N - 2));
            int y = 1 + (int) (rng.next() * (N - 2));
            int[] dir = DIRS[(int) (rng.next() * 4)];
            int tx = x - dir[0];
            int ty = y - dir[1];
            if (!d.free(x, y) || !d.free(tx, ty) || !d.free(x + dir[0], y + dir[1])) {
                continue;
            }
            d.placed.add(new Piece(recipe.trigger, tx, ty));
            d.chain.add(d.add(plan.get(0).runner, x, y));
            placedFirst = true;
        }
        if (!placedFirst) {
            return null;
        }
        if (!applyTrickAtFirst(d, plan.get(0), rng)) {
            return null;
        }

        for (int s = 1; s < plan.size(); s++) {
            if (!applyStep(d, plan.get(s), rng, wrap && s == plan.size() - 1)) {
                return null;
            }
        }
        if (!wrap && !placeMouseAndHole(d, rng)) {
            return null;
        }
        if (wrap && d.holeX == -1) {
            return null;
        }
        if (!Simulator.run(d.level(), d.placed).win) {
            return null;
        }
        for (int k = 0; k < recipe.laneBlockers; k++) {
            if (!addLaneBlocker(d, rng, wrap)) {
                return null;
            }
        }
        return assemble(d, recipe, name);
    }

    /** Turns the recipe into steps: which chain animals appear and where the tricks go. */
    private static List<Step> plan(Recipe recipe, LevelGenerator.Rng rng) {
        List<Animal> types = new ArrayList<>();
        Animal t = prey(recipe.trigger);
        if (recipe.wrapAround) {
            if (recipe.trigger != Animal.CAT) {
                return null;
            }
            // mouse, elephant, lion, bear, dog, cat ... and the cat brings the chain back to the mouse
            for (int k = 0; k < 6; k++) {
                types.add(t);
                t = prey(t);
            }
        } else {
            while (t != Animal.MOUSE) {
                types.add(t);
                t = prey(t);
            }
        }
        // Choose where each trick goes; a trick uses two (freeze) or three (waiting) chain types.
        int[] at = new int[types.size()];
        java.util.Arrays.fill(at, -1);
        // Never on the first link (your animal could send it any way, which gives extra solutions),
        // and never on the wrap-around mouse.
        int firstUsable = 1;
        for (int k = 0; k < recipe.tricks.length; k++) {
            Recipe.Trick trick = recipe.tricks[k];
            if (trick == Recipe.Trick.PLAIN) {
                continue;
            }
            int width = trick == Recipe.Trick.FREEZE_RELEASE ? 2 : 3;
            List<Integer> options = new ArrayList<>();
            for (int i = firstUsable; i + width <= types.size(); i++) {
                boolean clear = true;
                for (int j = i; j < i + width; j++) {
                    clear &= at[j] == -1;
                }
                if (clear) {
                    options.add(i);
                }
            }
            if (options.isEmpty()) {
                return null;
            }
            int i = rng.pick(options);
            for (int j = i; j < i + width; j++) {
                at[j] = k;
            }
            at[i] = 100 + k; // marks where the trick starts
        }
        List<Step> plan = new ArrayList<>();
        for (int i = 0; i < types.size(); i++) {
            if (at[i] >= 100) {
                Recipe.Trick trick = recipe.tricks[at[i] - 100];
                if (trick == Recipe.Trick.FREEZE_RELEASE) {
                    plan.add(new Step(trick, types.get(i), types.get(i + 1), types.get(i)));
                    i += 1;
                } else {
                    plan.add(new Step(trick, types.get(i), types.get(i + 2), types.get(i + 1)));
                    i += 2;
                }
            } else {
                plan.add(new Step(Recipe.Trick.PLAIN, types.get(i), null, null));
            }
        }
        return plan;
    }

    private static boolean applyTrickAtFirst(Draft d, Step step, LevelGenerator.Rng rng) {
        if (step.trick == Recipe.Trick.PLAIN) {
            return valid(d);
        }
        int y = d.chain.get(d.chain.size() - 1);
        Piece trigger = d.placed.get(0);
        Piece yp = d.fixed.get(y);
        int[] q = {yp.x - trigger.x, yp.y - trigger.y};
        return addTrickAnimals(d, step, yp, q, rng);
    }

    /** Places one step's animals beside the newest runner's path, retrying until the simulator agrees. */
    private static boolean applyStep(Draft d, Step step, LevelGenerator.Rng rng, boolean wrapFinal) {
        int runner = d.chain.get(d.chain.size() - 1);
        List<int[]> path = path(d, runner);
        if (path == null) {
            return false;
        }
        List<int[]> options = new ArrayList<>(); // {x, y, dx, dy}: new animal square and the way it will run
        for (int[] p : path) {
            for (int[] s : DIRS) {
                int cx = p[0] + s[0];
                int cy = p[1] + s[1];
                if (d.free(cx, cy) && d.free(cx + s[0], cy + s[1])) {
                    options.add(new int[] {cx, cy, s[0], s[1]});
                }
            }
        }
        if (wrapFinal) {
            options = aimedAtMouse(d, options);
        }
        Collections.shuffle(options, new java.util.Random((long) (rng.next() * Long.MAX_VALUE)));
        int tries = 0;
        for (int[] o : options) {
            if (tries++ >= TRIES_PER_STEP) {
                break;
            }
            int before = d.fixed.size();
            d.chain.add(d.add(step.runner, o[0], o[1]));
            boolean ok = valid(d);
            if (ok && step.trick != Recipe.Trick.PLAIN) {
                ok = addTrickAnimals(d, step, d.fixed.get(d.fixed.size() - 1), new int[] {o[2], o[3]}, rng);
            }
            if (ok && wrapFinal) {
                ok = closeWrapAround(d);
            }
            if (ok) {
                return true;
            }
            d.removeLast(d.fixed.size() - before);
            d.holeX = -1;
            d.holeY = -1;
        }
        return false;
    }

    /**
     * Adds the extra animals of a trick around chain animal {@code y}, which runs in direction q.
     * FREEZE_RELEASE: "next" sits beside y and a guard pins it from another side; when y runs off, next bolts.
     * WAITING_RUNNER: "next" is already scared by a guard behind it but y blocks its way; when y moves, next goes.
     */
    private static boolean addTrickAnimals(Draft d, Step step, Piece y, int[] q, LevelGenerator.Rng rng) {
        List<int[][]> options = new ArrayList<>(); // {{zx, zy}, {gx, gy}}
        for (int[] r : DIRS) {
            if (r[0] * q[0] + r[1] * q[1] != 0) {
                continue; // must be to the side of y's run
            }
            if (step.trick == Recipe.Trick.FREEZE_RELEASE) {
                int zx = y.x + r[0];
                int zy = y.y + r[1];
                for (int[] r2 : DIRS) {
                    if (r2[0] == -r[0] && r2[1] == -r[1]) {
                        continue; // that side is y itself
                    }
                    int gx = zx + r2[0];
                    int gy = zy + r2[1];
                    // when released, next runs away from the guard: that square must be open (or be y's, which empties)
                    int ex = zx - r2[0];
                    int ey = zy - r2[1];
                    boolean exitOpen = (ex == y.x && ey == y.y) || d.free(ex, ey);
                    if (d.free(zx, zy) && d.free(gx, gy) && exitOpen) {
                        options.add(new int[][] {{zx, zy}, {gx, gy}});
                    }
                }
            } else {
                int zx = y.x - r[0];
                int zy = y.y - r[1];
                int gx = zx - r[0];
                int gy = zy - r[1];
                if (d.free(zx, zy) && d.free(gx, gy)) {
                    options.add(new int[][] {{zx, zy}, {gx, gy}});
                }
            }
        }
        Collections.shuffle(options, new java.util.Random((long) (rng.next() * Long.MAX_VALUE)));
        for (int[][] o : options) {
            int z = d.add(step.next, o[0][0], o[0][1]);
            int g = d.add(step.guard, o[1][0], o[1][1]);
            d.chain.add(z);
            d.guards.add(g);
            if (valid(d)) {
                return true;
            }
            d.removeLast(2);
        }
        return false;
    }

    /**
     * Checks the draft so far: nothing moves before you place anything, every chain animal runs,
     * each one starts after the one before it, and guards never move.
     */
    private static boolean valid(Draft d) {
        Level level = d.level();
        if (!still(level)) {
            return false;
        }
        SimResult r = Simulator.record(level, d.placed);
        int last = 0;
        for (int idx : d.chain) {
            int f = firstMove(r.frames, idx);
            if (f < 0 || f < last) { // a released animal can start on the same step its blocker leaves
                return false;
            }
            last = f;
        }
        for (int g : d.guards) {
            if (firstMove(r.frames, g) >= 0) {
                return false;
            }
        }
        return true;
    }

    /** True if nothing on the board moves when you press Go with nothing placed. */
    private static boolean still(Level level) {
        return Simulator.run(level, Collections.<Piece>emptyList()).moved == 0;
    }

    /** Ends a normal chain: the mouse goes beside the last runner's path, the hole straight ahead of it. */
    private static boolean placeMouseAndHole(Draft d, LevelGenerator.Rng rng) {
        int runner = d.chain.get(d.chain.size() - 1);
        List<int[]> path = path(d, runner);
        if (path == null) {
            return false;
        }
        List<int[]> options = new ArrayList<>();
        for (int[] p : path) {
            for (int[] s : DIRS) {
                int mx = p[0] + s[0];
                int my = p[1] + s[1];
                if (!d.free(mx, my)) {
                    continue;
                }
                int[] hole = laneToHole(d, mx, my, s);
                if (hole != null) {
                    options.add(new int[] {mx, my, hole[0], hole[1]});
                }
            }
        }
        Collections.shuffle(options, new java.util.Random((long) (rng.next() * Long.MAX_VALUE)));
        int tries = 0;
        for (int[] o : options) {
            if (tries++ >= TRIES_PER_STEP) {
                break;
            }
            d.fixed.add(0, new Piece(Animal.MOUSE, o[0], o[1]));
            shift(d, 1);
            d.holeX = o[2];
            d.holeY = o[3];
            if (still(d.level()) && Simulator.run(d.level(), d.placed).win && allChainMoved(d)) {
                return true;
            }
            d.fixed.remove(0);
            shift(d, -1);
            d.holeX = -1;
            d.holeY = -1;
        }
        return false;
    }

    /** Wrap-around: keep only cat squares whose run passes right beside where the mouse rests. */
    private static List<int[]> aimedAtMouse(Draft d, List<int[]> options) {
        List<SimResult.Snapshot> end = Simulator.record(d.level(), d.placed).lastFrame();
        int mx = end.get(0).x;
        int my = end.get(0).y;
        List<int[]> out = new ArrayList<>();
        for (int[] o : options) {
            int cx = o[0];
            int cy = o[1];
            while (cx >= 0 && cy >= 0 && cx < N && cy < N) {
                if (Math.abs(cx - mx) + Math.abs(cy - my) == 1) {
                    out.add(o);
                    break;
                }
                cx += o[2];
                cy += o[3];
                if (!d.free(cx, cy)) {
                    break;
                }
            }
        }
        return out;
    }

    /** Ends a wrap-around chain: after the last cat runs, the mouse must escape through a hole we can add. */
    private static boolean closeWrapAround(Draft d) {
        // The mouse (fixed index 0) ran once already. Find where it rests, then try each direction for the hole.
        SimResult r = Simulator.record(d.level(), d.placed);
        List<SimResult.Snapshot> end = r.lastFrame();
        int mx = end.get(0).x;
        int my = end.get(0).y;
        for (int[] h : DIRS) {
            int[] hole = laneToHole(d, mx, my, h);
            if (hole == null) {
                continue;
            }
            d.holeX = hole[0];
            d.holeY = hole[1];
            SimResult w = Simulator.record(d.level(), d.placed);
            if (w.win && allChainMoved(d) && mouseRanTwice(w.frames)) {
                return true;
            }
        }
        d.holeX = -1;
        d.holeY = -1;
        return false;
    }

    /** From (x, y) heading in dir: if the way to the castle edge is clear, the hole square on the border. */
    private static int[] laneToHole(Draft d, int x, int y, int[] dir) {
        int cx = x + dir[0];
        int cy = y + dir[1];
        while (cx >= 0 && cy >= 0 && cx < N && cy < N) {
            if (!d.free(cx, cy)) {
                return null;
            }
            cx += dir[0];
            cy += dir[1];
        }
        return new int[] {cx, cy};
    }

    private static boolean allChainMoved(Draft d) {
        SimResult r = Simulator.record(d.level(), d.placed);
        for (int idx : d.chain) {
            if (firstMove(r.frames, idx) < 0) {
                return false;
            }
        }
        return true;
    }

    private static boolean mouseRanTwice(List<List<SimResult.Snapshot>> frames) {
        int runs = 0;
        boolean moving = false;
        for (int f = 1; f < frames.size(); f++) {
            SimResult.Snapshot a = frames.get(f).get(0);
            SimResult.Snapshot b = frames.get(f - 1).get(0);
            boolean moved = a.x != b.x || a.y != b.y;
            if (moved && !moving) {
                runs++;
            }
            moving = moved;
        }
        return runs >= 2;
    }

    /** Squares the animal occupies from its first move to the end (where the next link can be placed beside). */
    private static List<int[]> path(Draft d, int idx) {
        SimResult r = Simulator.record(d.level(), d.placed);
        int f = firstMove(r.frames, idx);
        if (f < 0) {
            return null;
        }
        List<int[]> out = new ArrayList<>();
        for (int k = f; k < r.frames.size(); k++) {
            SimResult.Snapshot s = r.frames.get(k).get(idx);
            if (!s.gone) {
                int[] p = {s.x, s.y};
                if (out.isEmpty() || out.get(out.size() - 1)[0] != p[0] || out.get(out.size() - 1)[1] != p[1]) {
                    out.add(p);
                }
            }
        }
        return out;
    }

    private static int firstMove(List<List<SimResult.Snapshot>> frames, int idx) {
        for (int f = 1; f < frames.size(); f++) {
            SimResult.Snapshot a = frames.get(f).get(idx);
            SimResult.Snapshot b = frames.get(f - 1).get(idx);
            if (a.x != b.x || a.y != b.y) {
                return f;
            }
        }
        return -1;
    }

    private static void shift(Draft d, int by) {
        for (int k = 0; k < d.chain.size(); k++) {
            d.chain.set(k, d.chain.get(k) + by);
        }
        for (int k = 0; k < d.guards.size(); k++) {
            d.guards.set(k, d.guards.get(k) + by);
        }
    }

    /**
     * Clear the path: puts an animal between the mouse and the hole, plus a board animal that will run
     * right past it, and adds the animal you place to start that runner. The blocker is moved by a board
     * runner (not by your animal directly), so there's only one right square for your new animal.
     */
    private static boolean addLaneBlocker(Draft d, LevelGenerator.Rng rng, boolean wrap) {
        // Where the mouse starts its run to the hole, and which way the hole is.
        int px;
        int py;
        if (wrap) {
            SimResult first = Simulator.record(d.level(), Collections.singletonList(d.placed.get(0)));
            px = mouseRestBeforeLastRun(first.frames)[0];
            py = mouseRestBeforeLastRun(first.frames)[1];
        } else {
            px = d.fixed.get(0).x;
            py = d.fixed.get(0).y;
        }
        int hx = Integer.signum(d.holeX - px);
        int hy = Integer.signum(d.holeY - py);
        if (hx != 0 && hy != 0 || hx == 0 && hy == 0) {
            return false;
        }
        List<int[]> lane = new ArrayList<>();
        for (int x = px + hx, y = py + hy; x >= 0 && y >= 0 && x < N && y < N; x += hx, y += hy) {
            lane.add(new int[] {x, y});
        }
        // Not lions: a lion is moved by an elephant, and an elephant is started by a mouse, which you never place.
        Animal[] blockerTypes = {Animal.DOG, Animal.BEAR};
        List<int[]> options = new ArrayList<>(); // {bx, by, type, sx, sy, runDir sign, distance}
        for (int[] b : lane) {
            for (int t = 0; t < blockerTypes.length; t++) {
                for (int[] s : DIRS) {
                    if (s[0] * hx + s[1] * hy != 0) {
                        continue; // the runner passes to the side of the blocker
                    }
                    for (int sign = -1; sign <= 1; sign += 2) {
                        for (int m = 1; m <= 4; m++) {
                            options.add(new int[] {b[0], b[1], t, s[0], s[1], sign, m});
                        }
                    }
                }
            }
        }
        Collections.shuffle(options, new java.util.Random((long) (rng.next() * Long.MAX_VALUE)));
        int tries = 0;
        for (int[] o : options) {
            int bx = o[0];
            int by = o[1];
            Animal blocker = blockerTypes[o[2]];
            Animal runner = blocker.predator();
            Animal starter = runner.predator();
            int ux = o[5] * hx; // the runner moves along the lane's direction (either way), offset to the side
            int uy = o[5] * hy;
            int rx = bx + o[3] - ux * o[6];
            int ry = by + o[4] - uy * o[6];
            int tx = rx - ux;
            int ty = ry - uy;
            if (!d.free(bx, by) || !d.free(rx, ry) || !d.free(tx, ty) || !d.free(bx - o[3], by - o[4])) {
                continue;
            }
            if (tries++ >= 3 * TRIES_PER_STEP) {
                break;
            }
            int bIdx = d.add(blocker, bx, by);
            int rIdx = d.add(runner, rx, ry);
            d.placed.add(new Piece(starter, tx, ty));
            if (still(d.level()) && Simulator.run(d.level(), d.placed).win && allChainMoved(d)
                    && movesIn(d, rIdx) && movesIn(d, bIdx)) {
                return true;
            }
            d.placed.remove(d.placed.size() - 1);
            d.removeLast(2);
        }
        return false;
    }

    private static boolean movesIn(Draft d, int idx) {
        return firstMove(Simulator.record(d.level(), d.placed).frames, idx) >= 0;
    }

    /** Where the mouse is standing when it starts its last run. */
    private static int[] mouseRestBeforeLastRun(List<List<SimResult.Snapshot>> frames) {
        int[] rest = {frames.get(0).get(0).x, frames.get(0).get(0).y};
        for (int f = 1; f < frames.size(); f++) {
            SimResult.Snapshot a = frames.get(f).get(0);
            SimResult.Snapshot b = frames.get(f - 1).get(0);
            if (a.x == b.x && a.y == b.y) {
                rest = new int[] {a.x, a.y};
            }
        }
        return rest;
    }

    /** The finished level. Your animals are listed in chain order, which is the order hints reveal them. */
    private static Level assemble(Draft d, Recipe recipe, String name) {
        List<Animal> hand = new ArrayList<>();
        for (Piece p : d.placed) {
            if (p.type == Animal.MOUSE) {
                return null; // there is only ever one mouse
            }
            hand.add(p.type);
        }
        hand.sort((a, b) -> a.id().compareTo(b.id()));
        return new Level(name, recipe.tip, N, N, d.holeX, d.holeY, Collections.<int[]>emptyList(), d.fixed, hand,
                new ArrayList<>(d.placed));
    }

    /** A finished, checked level and how interesting it scored. */
    public static final class Built {
        public final Level level;
        public final LevelChecker.Verdict verdict;
        public final double score;
        public final long seed;

        Built(Level level, LevelChecker.Verdict verdict, double score, long seed) {
            this.level = level;
            this.verdict = verdict;
            this.score = score;
            this.seed = seed;
        }
    }

    /**
     * Builds candidates on several threads, keeps those that pass {@link LevelChecker}, and returns the
     * most interesting once {@code want} have passed (or when time runs out with at least one).
     */
    public static Built find(Recipe recipe, String name, long baseSeed, int threads, int want, long timeoutSeconds)
            throws InterruptedException {
        LevelRules rules = recipe.rules();
        List<Built> found = Collections.synchronizedList(new ArrayList<>());
        java.util.concurrent.ExecutorService pool = java.util.concurrent.Executors.newFixedThreadPool(threads);
        for (int t = 0; t < threads; t++) {
            final long seed = baseSeed + t;
            pool.submit(() -> {
                LevelGenerator.Rng rng = new LevelGenerator.Rng(seed);
                while (found.size() < want && !Thread.currentThread().isInterrupted()) {
                    Level candidate = build(recipe, rng, name);
                    if (candidate == null) {
                        continue;
                    }
                    LevelChecker.Verdict v = LevelChecker.check(candidate, rules);
                    if (v != null) {
                        // keep the builder's chain-ordered solution (hints reveal it in this order)
                        found.add(new Built(candidate, v, Interest.score(candidate), seed));
                    }
                }
            });
        }
        pool.shutdown();
        long deadline = System.currentTimeMillis() + timeoutSeconds * 1000;
        while (found.size() < want && System.currentTimeMillis() < deadline && !pool.isTerminated()) {
            pool.awaitTermination(200, java.util.concurrent.TimeUnit.MILLISECONDS);
        }
        pool.shutdownNow();
        pool.awaitTermination(10, java.util.concurrent.TimeUnit.SECONDS);
        Built best = null;
        synchronized (found) {
            for (Built b : found) {
                if (best == null || b.score > best.score) {
                    best = b;
                }
            }
        }
        return best;
    }

    static Animal prey(Animal a) {
        Animal[] all = Animal.values();
        return all[(a.ordinal() + all.length - 1) % all.length];
    }
}
