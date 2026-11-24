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
 * animals in hand.
 *
 * <p>Already-moving levels ({@link Recipe#moves}) put the starter on the board, so the chain runs on its
 * own when you press Go, and your animals steer it instead: a SWERVE animal turns a runner the right
 * way, a CATCH animal is a chain link taken off the board for you to put back, and a STOP animal
 * halts a runner before it scares a "spoiler" that would ruin the run. {@link LevelChecker} still has
 * the final say on every level.
 */
public final class ChainBuilder {
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
        final int n;                                     // board size
        final List<Piece> fixed = new ArrayList<>();
        final List<Piece> placed = new ArrayList<>();
        final List<Integer> chain = new ArrayList<>();   // fixed indices, in chain order
        final List<Integer> guards = new ArrayList<>();  // fixed indices
        int holeX = -1;                                  // (-1,-1) is a corner, so no hole yet
        int holeY = -1;
        final List<int[]> walls = new ArrayList<>();
        boolean moving;                                  // the starter is on the board: no "still" check
        int tx;                                          // where the starter is
        int ty;

        Draft(int n) {
            this.n = n;
        }

        Level level() {
            return new Level("", "", n, n, holeX, holeY, walls, fixed,
                    Collections.<Animal>emptyList(), Collections.<Piece>emptyList());
        }

        boolean free(int x, int y) {
            if (x < 0 || y < 0 || x >= n || y >= n || (x == holeX && y == holeY)) {
                return false;
            }
            for (int[] w : walls) {
                if (w[0] == x && w[1] == y) {
                    return false;
                }
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
        Draft d = new Draft(recipe.size);
        boolean wrap = recipe.wrapAround;
        d.moving = recipe.moving();
        if (d.moving && wrap) {
            return null;
        }
        // Which links get a SWERVE: your animal turns the runner before that link's animal is placed.
        boolean[] swerveAt = new boolean[plan.size()];
        for (Recipe.Move m : recipe.moves) {
            if (m == Recipe.Move.SWERVE) {
                List<Integer> free = new ArrayList<>();
                for (int k = 1; k < plan.size(); k++) {
                    if (!swerveAt[k]) {
                        free.add(k);
                    }
                }
                if (free.isEmpty()) {
                    return null;
                }
                swerveAt[rng.pick(free)] = true;
            }
        }

        // First link: your first animal right behind the first chain animal.
        boolean placedFirst = false;
        for (int t = 0; t < TRIES_PER_STEP && !placedFirst; t++) {
            int x = 1 + (int) (rng.next() * (d.n - 2));
            int y = 1 + (int) (rng.next() * (d.n - 2));
            int[] dir = DIRS[(int) (rng.next() * 4)];
            int tx = x - dir[0];
            int ty = y - dir[1];
            if (!d.free(x, y) || !d.free(tx, ty) || !d.free(x + dir[0], y + dir[1])) {
                continue;
            }
            if (d.moving) {
                d.add(recipe.trigger, tx, ty); // on the board: the chain starts by itself
            } else {
                d.placed.add(new Piece(recipe.trigger, tx, ty));
            }
            d.tx = tx;
            d.ty = ty;
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
            if (!applyStep(d, plan.get(s), rng, wrap && s == plan.size() - 1, swerveAt[s])) {
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
            if (!addLaneBlocker(d, rng, wrap, recipe.blockers)) {
                return null;
            }
        }
        for (Recipe.Move m : recipe.moves) {
            if (m == Recipe.Move.STOP && !addStop(d, rng, false)) {
                return null;
            }
        }
        for (Recipe.Move m : recipe.moves) {
            if (m == Recipe.Move.CATCH && !takeOffBoard(d, rng)) {
                return null;
            }
        }
        // Walls that stop a runner before a spoiler: up to half the walls, the rest come from closing off
        // other solutions (see candidate()).
        int stopWalls = recipe.wallsMax == 0 ? 0 : (int) (rng.next() * (recipe.wallsMax / 2 + 1));
        for (int k = 0; k < stopWalls; k++) {
            addStop(d, rng, true);
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
        Piece yp = d.fixed.get(y);
        int[] q = {yp.x - d.tx, yp.y - d.ty};
        return addTrickAnimals(d, step, yp, q, rng);
    }

    /** Places one step's animals beside the newest runner's path, retrying until the simulator agrees. */
    private static boolean applyStep(Draft d, Step step, LevelGenerator.Rng rng, boolean wrapFinal, boolean swerve) {
        if (swerve) {
            return swerveThenStep(d, step, rng, wrapFinal);
        }
        return placeStep(d, step, rng, wrapFinal, 0);
    }

    /**
     * SWERVE: you place an animal the runner fears beside its path, so it turns when it gets there. The
     * next link then goes beside the new stretch of path, which the runner only takes because of you.
     */
    private static boolean swerveThenStep(Draft d, Step step, LevelGenerator.Rng rng, boolean wrapFinal) {
        int runner = d.chain.get(d.chain.size() - 1);
        Animal type = d.fixed.get(runner).type;
        List<int[]> path = path(d, runner);
        if (path == null || type.predator() == Animal.MOUSE) {
            return false;
        }
        List<int[]> options = new ArrayList<>(); // {k, sx, sy}: turn at path[k], your animal on side s
        for (int k = 1; k < path.size(); k++) {
            int mx = path.get(k)[0] - path.get(k - 1)[0];
            int my = path.get(k)[1] - path.get(k - 1)[1];
            for (int[] side : DIRS) {
                if (side[0] * mx + side[1] * my != 0) {
                    continue;
                }
                int[] p = path.get(k);
                if (d.free(p[0] + side[0], p[1] + side[1]) && d.free(p[0] - side[0], p[1] - side[1])) {
                    options.add(new int[] {k, side[0], side[1]});
                }
            }
        }
        Collections.shuffle(options, new java.util.Random((long) (rng.next() * Long.MAX_VALUE)));
        int tries = 0;
        for (int[] o : options) {
            if (tries++ >= TRIES_PER_STEP / 2) {
                break;
            }
            int[] p = path.get(o[0]);
            d.placed.add(new Piece(type.predator(), p[0] + o[1], p[1] + o[2]));
            List<int[]> turned = path(d, runner);
            int from = turned == null ? -1 : indexOf(turned, p[0] - o[1], p[1] - o[2]);
            if (from > 0 && placeStep(d, step, rng, wrapFinal, from)) {
                return true;
            }
            d.placed.remove(d.placed.size() - 1);
        }
        return false;
    }

    private static int indexOf(List<int[]> path, int x, int y) {
        for (int i = 0; i < path.size(); i++) {
            if (path.get(i)[0] == x && path.get(i)[1] == y) {
                return i;
            }
        }
        return -1;
    }

    /** Places the step's animal beside the runner's path, from path index {@code from} on. */
    private static boolean placeStep(Draft d, Step step, LevelGenerator.Rng rng, boolean wrapFinal, int from) {
        int runner = d.chain.get(d.chain.size() - 1);
        List<int[]> path = path(d, runner);
        if (path == null) {
            return false;
        }
        path = path.subList(Math.min(from, path.size()), path.size());
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
        if (!d.moving && !still(level)) {
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
                for (int[] hole : laneToHole(d, mx, my, s)) {
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
            if ((d.moving || still(d.level())) && Simulator.run(d.level(), d.placed).win && allChainMoved(d)) {
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
            while (cx >= 0 && cy >= 0 && cx < d.n && cy < d.n) {
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

    /**
     * Ends a wrap-around chain: after the last cat runs, the mouse must get into a hole we can add. The
     * hole goes on the mouse's second run, so the mouse falls in on the way instead of stopping.
     */
    private static boolean closeWrapAround(Draft d) {
        SimResult r = Simulator.record(d.level(), d.placed);
        int[] start = mouseRestBeforeLastRun(r.frames);
        List<SimResult.Snapshot> end = r.lastFrame();
        int ex = end.get(0).x;
        int ey = end.get(0).y;
        int sx = Integer.signum(ex - start[0]);
        int sy = Integer.signum(ey - start[1]);
        if (sx != 0 && sy != 0 || sx == 0 && sy == 0) {
            return false;
        }
        // Farthest first: where the mouse used to stop, then back along its run (at least two squares in).
        for (int x = ex, y = ey; Math.abs(x - start[0]) + Math.abs(y - start[1]) >= 2; x -= sx, y -= sy) {
            if (!d.free(x, y)) {
                continue;
            }
            d.holeX = x;
            d.holeY = y;
            SimResult w = Simulator.record(d.level(), d.placed);
            if (w.win && allChainMoved(d) && mouseRanTwice(w.frames)) {
                return true;
            }
        }
        d.holeX = -1;
        d.holeY = -1;
        return false;
    }

    /**
     * From (x, y) heading in dir: the squares where the hole could go, each with a clear run to it.
     * The hole is never right next to the mouse, so the mouse always runs at least two squares.
     * Farthest squares come first.
     */
    private static List<int[]> laneToHole(Draft d, int x, int y, int[] dir) {
        List<int[]> out = new ArrayList<>();
        int cx = x + dir[0];
        int cy = y + dir[1];
        int steps = 1;
        while (d.free(cx, cy)) {
            if (steps >= 2) {
                out.add(0, new int[] {cx, cy});
            }
            cx += dir[0];
            cy += dir[1];
            steps++;
        }
        return out;
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
    private static boolean addLaneBlocker(Draft d, LevelGenerator.Rng rng, boolean wrap, Animal[] blockerTypes) {
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
        for (int x = px + hx, y = py + hy; x != d.holeX || y != d.holeY; x += hx, y += hy) {
            lane.add(new int[] {x, y});
        }
        // Never lions: a lion is moved by an elephant, and an elephant is started by a mouse, which you never place.
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
            if ((d.moving || still(d.level())) && Simulator.run(d.level(), d.placed).win && allChainMoved(d)
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

    /**
     * STOP: a chain runner gets a "spoiler" beside the rest of its path (an animal it scares, which would
     * run off and ruin the level), and you place an animal in the runner's path to halt it before that.
     */
    private static boolean addStop(Draft d, LevelGenerator.Rng rng, boolean wall) {
        List<int[]> options = new ArrayList<>(); // {chain idx, k, side x, side y, j}
        java.util.Map<Integer, List<int[]>> paths = new java.util.HashMap<>();
        for (int idx : d.chain) {
            Animal type = d.fixed.get(idx).type;
            if (prey(type) == Animal.MOUSE) {
                continue; // the mouse can't be a spoiler: there is only one
            }
            List<int[]> path = path(d, idx);
            paths.put(idx, path);
            if (path == null) {
                continue;
            }
            for (int k = 0; k + 2 < path.size(); k++) {
                for (int j = k + 2; j < path.size(); j++) {
                    int mx = path.get(j)[0] - path.get(j - 1)[0];
                    int my = path.get(j)[1] - path.get(j - 1)[1];
                    for (int[] side : DIRS) {
                        if (side[0] * mx + side[1] * my == 0) {
                            options.add(new int[] {idx, k, side[0], side[1], j});
                        }
                    }
                }
            }
        }
        Collections.shuffle(options, new java.util.Random((long) (rng.next() * Long.MAX_VALUE)));
        int tries = 0;
        for (int[] o : options) {
            Animal type = d.fixed.get(o[0]).type;
            List<int[]> path = paths.get(o[0]);
            int[] stopAt = path.get(o[1] + 1);
            int[] p = path.get(o[4]);
            int sx = p[0] + o[2];
            int sy = p[1] + o[3];
            if (!d.free(stopAt[0], stopAt[1]) || !d.free(sx, sy) || !d.free(sx + o[2], sy + o[3])) {
                continue;
            }
            if (tries++ >= 3 * TRIES_PER_STEP) {
                break;
            }
            // Your stopping animal: one the runner neither scares nor fears (never a mouse).
            List<Animal> neutral = new ArrayList<>();
            for (Animal a : Animal.values()) {
                if (a != Animal.MOUSE && a != prey(type) && a != type.predator()) {
                    neutral.add(a);
                }
            }
            Animal stopper = rng.pick(neutral);
            int spoiler = d.add(prey(type), sx, sy);
            boolean spoils = !Simulator.run(d.level(), d.placed).win;
            if (wall) {
                d.walls.add(new int[] {stopAt[0], stopAt[1]});
            } else {
                d.placed.add(new Piece(stopper, stopAt[0], stopAt[1]));
            }
            SimResult with = Simulator.record(d.level(), d.placed);
            int stopperId = d.fixed.size() + d.placed.size() - 1;
            if (spoils && with.win && firstMove(with.frames, spoiler) < 0
                    && (wall || firstMove(with.frames, stopperId) < 0) && allChainMoved(d)) {
                d.guards.add(spoiler);
                return true;
            }
            if (wall) {
                d.walls.remove(d.walls.size() - 1);
            } else {
                d.placed.remove(d.placed.size() - 1);
            }
            d.removeLast(1);
        }
        return false;
    }

    /** CATCH: takes one chain animal (not the first) off the board; you put it back where the chain needs it. */
    private static boolean takeOffBoard(Draft d, LevelGenerator.Rng rng) {
        List<Integer> options = new ArrayList<>(d.chain.subList(1, d.chain.size()));
        Collections.shuffle(options, new java.util.Random((long) (rng.next() * Long.MAX_VALUE)));
        for (int idx : options) {
            Piece c = d.fixed.get(idx);
            if (c.type == Animal.MOUSE) {
                continue;
            }
            List<Piece> fixed = new ArrayList<>(d.fixed);
            fixed.remove(idx);
            Level without = new Level("", "", d.n, d.n, d.holeX, d.holeY, d.walls, fixed,
                    Collections.<Animal>emptyList(), Collections.<Piece>emptyList());
            List<Piece> placed = new ArrayList<>(d.placed);
            if (Simulator.run(without, placed).win) {
                continue; // the chain doesn't need it
            }
            if (!d.moving && Simulator.run(without, Collections.<Piece>emptyList()).moved > 0) {
                continue; // taking it away would set something off before you place anything
            }
            placed.add(c);
            if (!Simulator.run(without, placed).win) {
                continue;
            }
            d.fixed.remove(idx);
            d.chain.remove(Integer.valueOf(idx));
            for (int k = 0; k < d.chain.size(); k++) {
                if (d.chain.get(k) > idx) {
                    d.chain.set(k, d.chain.get(k) - 1);
                }
            }
            for (int k = 0; k < d.guards.size(); k++) {
                if (d.guards.get(k) > idx) {
                    d.guards.set(k, d.guards.get(k) - 1);
                }
            }
            d.placed.add(c);
            return true;
        }
        return false;
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
        return new Level(name, recipe.tip, d.n, d.n, d.holeX, d.holeY, d.walls, d.fixed, hand,
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
        return find(recipe, name, baseSeed, threads, want, timeoutSeconds, java.util.Collections.emptyMap());
    }

    /**
     * Like {@link #find(Recipe, String, long, int, int, long)}, but keeps the animals you place in a level
     * varied: {@code recent} counts the animals placed in the levels just before this one, and candidates
     * whose hand repeats the most common of those lose points, so rarer animals win.
     */
    public static Built find(Recipe recipe, String name, long baseSeed, int threads, int want, long timeoutSeconds,
                             java.util.Map<Animal, Integer> recent) throws InterruptedException {
        LevelRules rules = recipe.rules();
        List<Built> found = Collections.synchronizedList(new ArrayList<>());
        java.util.concurrent.ExecutorService pool = java.util.concurrent.Executors.newFixedThreadPool(threads);
        for (int t = 0; t < threads; t++) {
            final long seed = baseSeed + t;
            pool.submit(() -> {
                LevelGenerator.Rng rng = new LevelGenerator.Rng(seed);
                while (found.size() < want && !Thread.currentThread().isInterrupted()) {
                    Level candidate = candidate(recipe, rng, name);
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
        double bestValue = 0;
        synchronized (found) {
            for (Built b : found) {
                double value = b.score - handPenalty(b.level.inventory, recent);
                if (best == null || value > bestValue) {
                    best = b;
                    bestValue = value;
                }
            }
        }
        return best;
    }

    /**
     * One candidate level: built by {@link #build}, then, for recipes with walls, other solutions are
     * closed off with walls on the squares they use. Returns null if the wall count is out of range.
     * The caller still runs {@link LevelChecker}.
     */
    static Level candidate(Recipe recipe, LevelGenerator.Rng rng, String name) {
        Level level = build(recipe, rng, name);
        if (level == null || recipe.wallsMax == 0) {
            return level;
        }
        level = closeOffOtherSolutions(level, recipe.wallsMax);
        if (level == null || level.walls.size() < recipe.wallsMin || level.walls.size() > recipe.wallsMax) {
            return null;
        }
        return level;
    }

    /**
     * While the level has other solutions besides the intended one, puts a wall on the square that rules
     * out the most of them (never one the intended run needs). Each such wall matters: take it away and
     * an easier solution comes back.
     */
    private static Level closeOffOtherSolutions(Level level, int maxWalls) {
        for (int guard = 0; guard < 8; guard++) {
            List<List<Piece>> all = LevelChecker.solutions(level, level.inventory, 12);
            List<List<Piece>> others = new ArrayList<>();
            for (List<Piece> s : all) {
                if (!sameSet(s, level.solution)) {
                    others.add(s);
                }
            }
            if (others.isEmpty()) {
                return level;
            }
            if (all.size() >= 12 || level.walls.size() >= maxWalls) {
                return null; // too many to close off
            }
            java.util.Set<String> used = usedSquares(level);
            java.util.Map<String, Integer> votes = new java.util.HashMap<>();
            for (List<Piece> s : others) {
                for (Piece p : s) {
                    if (!used.contains(p.x + "," + p.y)) {
                        votes.merge(p.x + "," + p.y, 1, Integer::sum);
                    }
                }
            }
            List<String> squares = new ArrayList<>(votes.keySet());
            squares.sort((a, b) -> votes.get(b) - votes.get(a));
            Level next = null;
            for (String sq : squares) {
                String[] xy = sq.split(",");
                List<int[]> walls = new ArrayList<>(level.walls);
                walls.add(new int[] {Integer.parseInt(xy[0]), Integer.parseInt(xy[1])});
                Level tryLevel = new Level(level.name, level.tip, level.w, level.h, level.holeX, level.holeY, walls,
                        level.fixed, level.inventory, level.solution);
                if (Simulator.run(tryLevel, tryLevel.solution).win) {
                    next = tryLevel;
                    break;
                }
            }
            if (next == null) {
                return null;
            }
            level = next;
        }
        return null;
    }

    /** Squares the intended run uses: where your animals go and every square an animal passes through. */
    private static java.util.Set<String> usedSquares(Level level) {
        java.util.Set<String> used = new java.util.HashSet<>();
        for (List<SimResult.Snapshot> frame : Simulator.record(level, level.solution).frames) {
            for (SimResult.Snapshot s : frame) {
                used.add(s.x + "," + s.y);
            }
        }
        return used;
    }

    private static boolean sameSet(List<Piece> a, List<Piece> b) {
        if (a.size() != b.size()) {
            return false;
        }
        java.util.Set<String> s = new java.util.HashSet<>();
        for (Piece p : a) {
            s.add(p.type + "," + p.x + "," + p.y);
        }
        for (Piece p : b) {
            if (!s.contains(p.type + "," + p.x + "," + p.y)) {
                return false;
            }
        }
        return true;
    }

    /** Points off for placing animals that were already common in the levels just before (0 when no history). */
    static double handPenalty(List<Animal> hand, java.util.Map<Animal, Integer> recent) {
        int total = 0;
        for (int c : recent.values()) {
            total += c;
        }
        if (total == 0) {
            return 0;
        }
        double penalty = 0;
        for (Animal a : hand) {
            penalty += 100.0 * recent.getOrDefault(a, 0) / total;
        }
        return penalty;
    }

    static Animal prey(Animal a) {
        Animal[] all = Animal.values();
        return all[(a.ordinal() + all.length - 1) % all.length];
    }
}
