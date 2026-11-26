package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Test levels for trapdoors, to try in the game with ?lab=trapdoor-lab before the real levels are made.
 * Usage: TrapdoorLab out.json firstSlot secondsPerLevel
 * The first is built by hand, like level 1: one cat to place, the hole straight ahead of the mouse and a mousetrap
 * in the way, with a trapdoor just before the trap and its partner just after it, so the mouse goes under the trap.
 * Then chains through a trapdoor, slowly longer; then a second animal to place; then trapdoors with tricks.
 */
public final class TrapdoorLab {
    private TrapdoorLab() {
    }

    /**
     * The first trapdoor level (Matt): like level 1, with a mousetrap between the mouse and the hole and a trapdoor
     * on each side of it. Placing the cat behind the mouse sends it under the trap and into the hole.
     */
    public static Level intro(String name, String tip) {
        int y = 5;
        List<Piece> fixed = Collections.singletonList(new Piece(Animal.MOUSE, 6, y));
        List<Piece> solution = Collections.singletonList(new Piece(Animal.CAT, 7, y));
        return new Level(name, tip, 10, 10, 0, y, Collections.<int[]>emptyList(), fixed,
                Collections.singletonList(Animal.CAT), solution, Collections.<int[]>emptyList(),
                Collections.singletonList(new int[] {3, y}), Arrays.asList(new int[] {4, y}, new int[] {2, y}));
    }

    public static void main(String[] args) throws Exception {
        String outPath = args[0];
        int first = Integer.parseInt(args[1]);
        int secs = Integer.parseInt(args[2]);
        Recipe.Trick plain = Recipe.Trick.PLAIN;
        List<Level> out = new ArrayList<>();
        Level intro = intro("Test " + first, "New: trapdoors!");
        boolean wins = Simulator.run(intro, intro.solution).win;
        boolean caughtWithout = !Simulator.run(intro.withTrapdoors(Collections.<int[]>emptyList()), intro.solution).win;
        LevelChecker.Verdict v = LevelChecker.check(intro, LevelRules.forBuilt(1, 0, 0).teaching());
        System.out.println("Test " + first + ": by hand, wins " + wins + ", fails without the trapdoors " + caughtWithout
                + ", " + (v == null ? "FAILS the checker" : v.solutions + " solution(s)"));
        out.add(intro);
        Files.write(Paths.get(outPath), Level.listToJson(out).getBytes(StandardCharsets.UTF_8));
        Recipe[] plan = {
            // chains through a trapdoor, getting longer
            new Recipe(Animal.DOG, 0, false, "", plain).withTrapdoors(1),
            new Recipe(Animal.BEAR, 0, false, "", plain).withTrapdoors(1),
            new Recipe(Animal.LION, 0, false, "", plain).withTrapdoors(1),
            new Recipe(Animal.ELEPHANT, 0, false, "", plain).withTrapdoors(1),
            // a second animal to place
            new Recipe(Animal.BEAR, 0, false, "", plain).withCatches(1).withTrapdoors(1),
            // trapdoors with tricks
            new Recipe(Animal.LION, 0, false, "", Recipe.Trick.FREEZE_RELEASE).withTrapdoors(1),
            new Recipe(Animal.ELEPHANT, 0, false, "", Recipe.Trick.WAITING_RUNNER).withTrapdoors(1),
            new Recipe(Animal.LION, 1, false, "", plain).withTrapdoors(1),
            new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(Recipe.Move.CATCH).withTrapdoors(1),
            new Recipe(Animal.LION, 0, false, "", plain).withSpringTraps(1).withTrapdoors(1),
        };
        for (int k = 0; k < plan.length; k++) {
            Recipe r = plan[k].withSize(10);
            String name = "Test " + (first + 1 + k);
            ChainBuilder.Built best = null;
            for (int seed = 1; seed <= 4 && best == null; seed++) {
                ChainBuilder.Built b = ChainBuilder.find(r, name, 733L * (k + 1) * seed, 2, 3, secs);
                if (b != null && (b.level.traps.isEmpty() || TrapLab.trapsDoTheirJob(b.level, r.springTraps))) {
                    best = b;
                }
            }
            if (best == null) {
                System.out.println(name + ": none (" + r.key() + ")");
                continue;
            }
            System.out.println(name + ": trapdoors " + TrapLab.str(best.level.trapdoors) + " hand " + best.level.inventory
                    + " depth " + best.verdict.depth + " " + Interest.breakdown(best.level));
            out.add(best.level);
            Files.write(Paths.get(outPath), Level.listToJson(out).getBytes(StandardCharsets.UTF_8));
        }
        System.out.println("wrote " + out.size() + " levels to " + outPath);
    }
}
