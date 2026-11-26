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
import java.util.List;

/**
 * Test levels for mousetraps, to try in the game with ?lab before the real levels are made.
 * Usage: TrapLab out.json firstSlot secondsPerLevel
 * The first five steer the mouse around traps and get harder; the next ones have a trap on the mouse's
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
        Recipe[] plan = {
            new Recipe(Animal.BEAR, 0, false, "New: mousetraps!", plain).withMoves(catchIt).withTraps(1, 1),
            new Recipe(Animal.LION, 0, false, "", plain).withMoves(stop).withTraps(1, 2),
            new Recipe(Animal.LION, 0, false, "", plain).withMoves(catchIt).withTraps(1, 2),
            new Recipe(Animal.BEAR, 1, false, "", plain).withTraps(1, 2),
            new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(stop).withTraps(1, 2),
            new Recipe(Animal.BEAR, 0, false, "New: other animals spring traps!", plain).withSpringTraps(1),
            new Recipe(Animal.ELEPHANT, 0, false, "", plain).withSpringTraps(1),
            new Recipe(Animal.LION, 0, false, "", Recipe.Trick.FREEZE_RELEASE).withSpringTraps(1),
            new Recipe(Animal.BEAR, 0, false, "", plain).withMoves(catchIt).withSpringTraps(1).withTraps(0, 1),
            new Recipe(Animal.ELEPHANT, 0, false, "", Recipe.Trick.WAITING_RUNNER).withSpringTraps(1).withTraps(0, 2),
        };
        List<Level> out = new ArrayList<>();
        for (int k = 0; k < plan.length; k++) {
            Recipe r = plan[k].withSize(10);
            String name = "Test " + (first + k);
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
        System.out.println(out.size() + " of " + plan.length);
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
