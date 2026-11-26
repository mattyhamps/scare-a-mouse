package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.SimResult;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Test levels for mousetraps, to try in the game with ?lab before the real levels are made.
 * Usage: TrapLab out.json firstSlot secondsPerLevel [intro]
 * The first two have only the mouse and cats, with a trap between the mouse and the hole; the next ones have a trap on the mouse's
 * way and one more animal for you to send over it first; the last mix both.
 */
public final class TrapLab {
    private TrapLab() {
    }

    public static void main(String[] args) throws Exception {
        String outPath = args[0];
        int first = Integer.parseInt(args[1]);
        int secs = Integer.parseInt(args[2]);
        Recipe.Trick plain = Recipe.Trick.PLAIN;
        Recipe.Move catchIt = Recipe.Move.CATCH;
        Recipe.Move stop = Recipe.Move.STOP;
        List<Level> out = new ArrayList<>();
        // 801-802: only the mouse and cats. The mouse could run straight at the hole, but a trap is in the way.
        int[][] intro = {   // {cats on the board, traps, cats in your hand}
            {2, 1, 1}, {1, 1, 2},
        };
        for (int k = 0; k < intro.length; k++) {
            Level l = catsOnly(new java.util.Random(4242L * (k + 1)), intro[k][0], intro[k][1], intro[k][2], secs,
                    "Test " + (first + k), k == 0 ? "New: mousetraps!" : "");
            System.out.println("Test " + (first + k) + ": " + (l == null ? "none" : "traps " + str(l.traps) + " hand " + l.inventory
                    + " fixed " + l.fixed.size()));
            if (l != null) {
                out.add(l);
                Files.write(Paths.get(outPath), Level.listToJson(out).getBytes(StandardCharsets.UTF_8));
            }
        }
        // then: steer around traps in bigger chains, getting harder; then a trap on the mouse's way with one more
        // animal to send over it first (the second card); then both
        Recipe[] plan = {
            new Recipe(Animal.BEAR, 0, false, "", plain).withMoves(catchIt).withTraps(1, 1),
            new Recipe(Animal.LION, 0, false, "", plain).withMoves(stop).withTraps(1, 2),
            new Recipe(Animal.LION, 0, false, "", plain).withMoves(catchIt).withTraps(1, 2),
            new Recipe(Animal.BEAR, 1, false, "", plain).withTraps(1, 2),
            new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(stop).withTraps(1, 2),
            new Recipe(Animal.BEAR, 0, false, "New: springing traps!", plain).withSpringTraps(1),
            new Recipe(Animal.ELEPHANT, 0, false, "", plain).withSpringTraps(1),
            new Recipe(Animal.LION, 0, false, "", Recipe.Trick.FREEZE_RELEASE).withSpringTraps(1),
            new Recipe(Animal.BEAR, 0, false, "", plain).withMoves(catchIt).withSpringTraps(1).withTraps(0, 1),
            new Recipe(Animal.ELEPHANT, 0, false, "", Recipe.Trick.WAITING_RUNNER).withSpringTraps(1).withTraps(0, 2),
        };
        boolean introOnly = args.length > 3 && args[3].equals("intro");   // TrapLab out.json 801 30 intro: just the first two
        for (int k = 0; k < (introOnly ? 0 : plan.length); k++) {
            Recipe r = plan[k].withSize(10);
            String name = "Test " + (first + intro.length + k);
            ChainBuilder.Built best = null;
            for (int seed = 1; seed <= 4 && best == null; seed++) {
                ChainBuilder.Built b = ChainBuilder.find(r, name, 911L * (k + 1) * seed, 2, 3, secs);
                if (b != null && trapsDoTheirJob(b.level, r.springTraps)) {
                    best = b;
                }
            }
            if (best == null) {
                System.out.println(name + ": none (" + r.key() + ")");
                continue;
            }
            System.out.println(name + ": traps " + str(best.level.traps) + " hand " + best.level.inventory
                    + " depth " + best.verdict.depth + " " + Interest.breakdown(best.level));
            out.add(best.level);
            Files.write(Paths.get(outPath), Level.listToJson(out).getBytes(StandardCharsets.UTF_8));
        }
        System.out.println(out.size() + " of " + (intro.length + plan.length));
    }

    /**
     * A small level with only the mouse and cats: the mouse sits in line with the hole, but a trap is in the
     * way, so the cats on the board have to turn it onto another way in (that takes two cats: one turns it
     * off its line, the other back onto the hole's). Sending the mouse straight at the
     * hole always gets it caught, so you can try it and see. Keeps the one with the longest winning run.
     */
    static Level catsOnly(java.util.Random rnd, int boardCats, int traps, int handCats, int secs, String name, String tip) {
        final int n = 10;
        int[][] dirs = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};
        LevelRules rules = LevelRules.forBuilt(handCats, 0, 0);
        Level best = null;
        int bestSteps = -1;
        long end = System.currentTimeMillis() + secs * 1000L;
        while (System.currentTimeMillis() < end) {
            int mx = 1 + rnd.nextInt(n - 2), my = 1 + rnd.nextInt(n - 2);
            int[] d = dirs[rnd.nextInt(4)];
            int room = 0;   // squares between the mouse and the board's edge, straight ahead
            while (mx + d[0] * (room + 1) >= 0 && mx + d[0] * (room + 1) < n && my + d[1] * (room + 1) >= 0 && my + d[1] * (room + 1) < n) {
                room++;
            }
            if (room < 3) {
                continue;
            }
            int dist = 3 + rnd.nextInt(room - 2);   // the hole: straight ahead of the mouse
            int hx = mx + d[0] * dist, hy = my + d[1] * dist;
            int t = 1 + rnd.nextInt(dist - 1);   // the trap: on the straight way to the hole
            List<int[]> trapList = new ArrayList<>();
            trapList.add(new int[] {mx + d[0] * t, my + d[1] * t});
            List<Piece> fixed = new ArrayList<>();
            fixed.add(new Piece(Animal.MOUSE, mx, my));
            java.util.Set<String> taken = new java.util.HashSet<>();
            taken.add(mx + "," + my);
            taken.add(hx + "," + hy);
            taken.add(trapList.get(0)[0] + "," + trapList.get(0)[1]);
            boolean ok = true;
            for (int c = 0; c < boardCats && ok; c++) {
                int cx = rnd.nextInt(n), cy = rnd.nextInt(n);
                ok = !taken.contains(cx + "," + cy) && Math.abs(cx - mx) + Math.abs(cy - my) > 1;   // not touching the mouse at the start
                taken.add(cx + "," + cy);
                fixed.add(new Piece(Animal.CAT, cx, cy));
            }
            for (int c = 1; c < traps && ok; c++) {
                int tx = rnd.nextInt(n), ty = rnd.nextInt(n);
                ok = !taken.contains(tx + "," + ty);
                taken.add(tx + "," + ty);
                trapList.add(new int[] {tx, ty});
            }
            if (!ok) {
                continue;
            }
            List<Animal> hand = new ArrayList<>();
            for (int c = 0; c < handCats; c++) {
                hand.add(Animal.CAT);
            }
            Level level = new Level(name, tip, n, n, hx, hy, Collections.<int[]>emptyList(), fixed, hand,
                    Collections.<Piece>emptyList(), Collections.<int[]>emptyList(), trapList);
            LevelChecker.Verdict v = LevelChecker.check(level, rules);
            if (v == null) {
                continue;
            }
            level = level.withSolution(v.solution);
            // a cat right behind the mouse sends it straight at the hole: that has to get it caught
            List<Piece> straight = new ArrayList<>();
            straight.add(new Piece(Animal.CAT, mx - d[0], my - d[1]));
            for (int c = 1; c < handCats; c++) {
                straight.add(v.solution.get(c < v.solution.size() ? c : 0));
            }
            if (!level.isOpen(mx - d[0], my - d[1]) || !Simulator.run(level, straight.subList(0, 1)).caught) {
                continue;
            }
            int steps = Simulator.record(level, v.solution).frames.size();
            if (steps > bestSteps) {
                best = level;
                bestSteps = steps;
            }
        }
        return best;
    }

    /**
     * Spring traps are sprung by another animal in the intended run, and every other trap would catch the
     * mouse in some wrong try (a placement that wins once that trap is gone).
     */
    static boolean trapsDoTheirJob(Level level, int springCount) {
        SimResult run = Simulator.record(level, level.solution);
        int sprung = 0;
        for (List<Integer> s : run.snaps) {
            sprung += s.size();
        }
        if (sprung < springCount) {
            return false;
        }
        for (int i = 0; i < level.traps.size(); i++) {
            int[] t = level.traps.get(i);
            boolean sprungInRun = false;
            for (List<Integer> s : run.snaps) {
                sprungInRun |= s.contains(i);
            }
            if (sprungInRun) {
                continue;
            }
            Level without = level.withoutTrap(i);
            boolean catches = false;
            for (List<Piece> s : LevelChecker.solutions(without, level.inventory, 12)) {
                for (List<SimResult.Snapshot> f : Simulator.record(without, s).frames) {
                    catches |= f.get(0).x == t[0] && f.get(0).y == t[1];
                }
            }
            if (!catches) {
                return false;
            }
        }
        return true;
    }

    private static String str(List<int[]> traps) {
        List<String> s = new ArrayList<>();
        for (int[] t : traps) {
            s.add(Arrays.toString(t));
        }
        return s.toString();
    }
}
