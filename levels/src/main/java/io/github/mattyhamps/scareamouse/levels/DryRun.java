package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.levels.Recipe.Move;
import io.github.mattyhamps.scareamouse.levels.Recipe.Trick;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Predicate;

/**
 * The dry run for a harder castle (docs/HARDER_CASTLE.md, step 2): tries to build one 10x10 level for each
 * new kind of puzzle, with a time limit, and reports how long it took, its {@link Difficulty} score and the
 * techniques its solution uses. Nothing is saved. {@code LevelsCli trial [--timeout SEC] [--only TEXT]}.
 */
final class DryRun {
    private DryRun() {
    }

    /** One kind of puzzle to try: a recipe, and (for the new techniques) which technique the level must use. */
    static final class Trial {
        final String name;
        final Recipe recipe;
        final Techniques.Tag must;

        Trial(String name, Recipe recipe, Techniques.Tag must) {
            this.name = name;
            this.recipe = recipe.withSize(10);
            this.must = must;
        }
    }

    static List<Trial> trials() {
        Trick plain = Trick.PLAIN;
        Trick free = Trick.FREEZE_RELEASE;
        Trick wait = Trick.WAITING_RUNNER;
        List<Trial> t = new ArrayList<>();
        // 2 and 3: longer chains and two tricks in one puzzle (several found nothing in 30s before)
        t.add(new Trial("freeze-release + waiting runner", new Recipe(Animal.ELEPHANT, 0, false, "", free, wait), null));
        t.add(new Trial("freeze-release + waiting runner, 1 blocker", new Recipe(Animal.ELEPHANT, 1, false, "", free, wait), null));
        t.add(new Trial("moving: swerve + stop + catch", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(Move.SWERVE, Move.STOP, Move.CATCH), null));
        t.add(new Trial("moving: swerve + catch + catch", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(Move.SWERVE, Move.CATCH, Move.CATCH), null));
        t.add(new Trial("moving: two swerves, freeze-release", new Recipe(Animal.ELEPHANT, 0, false, "", free).withMoves(Move.SWERVE, Move.SWERVE), null));
        t.add(new Trial("lion chain, 2 missing links", new Recipe(Animal.LION, 0, false, "", plain).withCatches(2), null));
        t.add(new Trial("elephant chain, 2 missing links", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withCatches(2), null));
        t.add(new Trial("wrap-around + freeze-release", new Recipe(Animal.CAT, 0, true, "", free), null));
        t.add(new Trial("wrap-around, 1 blocker, 1 catch", new Recipe(Animal.CAT, 1, true, "", plain).withCatches(1), null));
        t.add(new Trial("walls + steer round traps", new Recipe(Animal.ELEPHANT, 0, false, "", free).withWalls(1, 3).withTraps(1, 2), null));
        t.add(new Trial("trapdoor + freeze-release + catch", new Recipe(Animal.ELEPHANT, 0, false, "", free).withCatches(1).withTrapdoors(1), null));
        // 12: four and five animals to place
        t.add(new Trial("4: lion, 3 lane blockers", new Recipe(Animal.LION, 3, false, "", plain), null));
        t.add(new Trial("4: elephant, 3 lane blockers", new Recipe(Animal.ELEPHANT, 3, false, "", plain), null));
        t.add(new Trial("4: elephant, 2 blockers, waiting runner, 1 catch", new Recipe(Animal.ELEPHANT, 2, false, "", wait).withCatches(1), null));
        t.add(new Trial("4: elephant freeze-release, 1 blocker, 2 catches", new Recipe(Animal.ELEPHANT, 1, false, "", free).withCatches(2), null));
        t.add(new Trial("4: elephant freeze-release, 2 blockers, 1 trap to spring", new Recipe(Animal.ELEPHANT, 2, false, "", free).withSpringTraps(1), null));
        t.add(new Trial("4: moving, 2 blockers, swerve + stop", new Recipe(Animal.ELEPHANT, 2, false, "", plain).withMoves(Move.SWERVE, Move.STOP), null));
        t.add(new Trial("5: elephant, 3 blockers, 1 catch", new Recipe(Animal.ELEPHANT, 3, false, "", plain).withCatches(1), null));
        t.add(new Trial("5: elephant freeze-release, 2 blockers, 2 catches", new Recipe(Animal.ELEPHANT, 2, false, "", free).withCatches(2), null));
        t.add(new Trial("5: elephant, 2 blockers, 2 traps to spring", new Recipe(Animal.ELEPHANT, 2, false, "", plain).withSpringTraps(2), null));
        t.add(new Trial("5: elephant, 3 blockers, 1 catch, walls", new Recipe(Animal.ELEPHANT, 3, false, "", plain).withCatches(1).withWalls(1, 4), null));
        t.add(new Trial("5: lion, 4 lane blockers, walls", new Recipe(Animal.LION, 4, false, "", plain).withWalls(1, 4), null));
        t.add(new Trial("4: elephant freeze-release, 1 blocker, 2 catches, walls", new Recipe(Animal.ELEPHANT, 1, false, "", free).withCatches(2).withWalls(1, 4), null));
        // closing off shortcuts (a win with one animal fewer) with walls or mousetraps
        t.add(new Trial("closed: lion chain, 2 missing links, walls", new Recipe(Animal.LION, 0, false, "", plain).withCatches(2).withWalls(1, 4), null));
        t.add(new Trial("closed: lion chain, 2 missing links, traps", new Recipe(Animal.LION, 0, false, "", plain).withCatches(2).withTraps(1, 3), null));
        t.add(new Trial("closed: 4: moving, 2 blockers, swerve + stop, walls", new Recipe(Animal.ELEPHANT, 2, false, "", plain).withMoves(Move.SWERVE, Move.STOP).withWalls(1, 4), null));
        t.add(new Trial("closed: 5: elephant, 3 blockers, 1 catch, walls", new Recipe(Animal.ELEPHANT, 3, false, "", plain).withCatches(1).withWalls(1, 4), null));
        t.add(new Trial("closed: 5: elephant, 3 blockers, 1 catch, traps", new Recipe(Animal.ELEPHANT, 3, false, "", plain).withCatches(1).withTraps(1, 3), null));
        t.add(new Trial("closed: 5: lion, 4 lane blockers, walls", new Recipe(Animal.LION, 4, false, "", plain).withWalls(1, 4), null));
        // taught to the builder (step 2 of teaching it): each technique on its own, then mixed with others
        t.add(new Trial("taught: freeze-release + waiting runner", new Recipe(Animal.ELEPHANT, 0, false, "", free, wait), null));
        t.add(new Trial("taught: freeze-release + waiting runner, 1 blocker", new Recipe(Animal.ELEPHANT, 1, false, "", free, wait), null));
        t.add(new Trial("taught: freeze on purpose", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withPlaced(Move.PIN), Techniques.Tag.PIN));
        t.add(new Trial("taught: freeze on purpose, freeze-release", new Recipe(Animal.ELEPHANT, 0, false, "", free).withPlaced(Move.PIN), Techniques.Tag.PIN));
        t.add(new Trial("taught: freeze on purpose, moving", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(Move.PIN), Techniques.Tag.PIN));
        t.add(new Trial("taught: standoff", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withPlaced(Move.STANDOFF), Techniques.Tag.STANDOFF));
        t.add(new Trial("taught: standoff, waiting runner", new Recipe(Animal.ELEPHANT, 0, false, "", wait).withPlaced(Move.STANDOFF), Techniques.Tag.STANDOFF));
        t.add(new Trial("taught: standoff, moving", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(Move.STANDOFF), Techniques.Tag.STANDOFF));
        t.add(new Trial("taught: freeze on purpose, walls", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withPlaced(Move.PIN).withWalls(1, 3), Techniques.Tag.PIN));
        t.add(new Trial("taught: freeze on purpose, traps", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withPlaced(Move.PIN).withTraps(1, 2), Techniques.Tag.PIN));
        t.add(new Trial("taught: freeze on purpose, moving, walls", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(Move.PIN).withWalls(1, 3), Techniques.Tag.PIN));
        t.add(new Trial("taught: standoff, walls", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withPlaced(Move.STANDOFF).withWalls(1, 3), Techniques.Tag.STANDOFF));
        t.add(new Trial("taught: standoff, traps", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withPlaced(Move.STANDOFF).withTraps(1, 2), Techniques.Tag.STANDOFF));
        t.add(new Trial("taught: standoff, moving, walls", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMoves(Move.STANDOFF).withWalls(1, 3), Techniques.Tag.STANDOFF));
        t.add(new Trial("taught: mouse turns twice", new Recipe(Animal.ELEPHANT, 0, false, "", plain).withMouseTurns(2), Techniques.Tag.MOUSE_TURNS));
        t.add(new Trial("taught: mouse turns twice, freeze-release", new Recipe(Animal.ELEPHANT, 0, false, "", free).withMouseTurns(2), Techniques.Tag.MOUSE_TURNS));
        t.add(new Trial("taught: mouse turns three times", new Recipe(Animal.LION, 0, false, "", plain).withMouseTurns(3), Techniques.Tag.MOUSE_TURNS));
        t.add(new Trial("taught: red herring", new Recipe(Animal.ELEPHANT, 0, false, "", free).withHerrings(1, 0), null));
        t.add(new Trial("taught: decoy start", new Recipe(Animal.ELEPHANT, 0, false, "", free).withHerrings(0, 1), null));
        t.add(new Trial("taught: decoy start + red herring, 1 blocker", new Recipe(Animal.ELEPHANT, 1, false, "", plain).withHerrings(1, 1), null));
        t.add(new Trial("taught: 4: pin + standoff, 1 blocker", new Recipe(Animal.ELEPHANT, 1, false, "", plain).withPlaced(Move.PIN, Move.STANDOFF), null));
        t.add(new Trial("taught: 4: freeze + wait, 1 blocker, pin", new Recipe(Animal.ELEPHANT, 1, false, "", free, wait).withPlaced(Move.PIN), null));
        t.add(new Trial("taught: 4: 2 blockers, standoff, mouse turns", new Recipe(Animal.ELEPHANT, 2, false, "", plain).withPlaced(Move.STANDOFF).withMouseTurns(2), null));
        // timing and the loop (built before, from familiar recipes)
        t.add(new Trial("new: your animal clears a path (timing)", new Recipe(Animal.ELEPHANT, 1, false, "", wait).withCatches(1), Techniques.Tag.CLEAR_PATH));
        t.add(new Trial("new: elephant-mouse loop, 3 to place", new Recipe(Animal.CAT, 1, true, "", free).withCatches(1), Techniques.Tag.WRAP));
        return t;
    }

    static void run(long timeout, String only) throws InterruptedException {
        int threads = Runtime.getRuntime().availableProcessors();
        System.out.println("| Puzzle | Hand | Built in | Score | Blind | Chain | Techniques |");
        System.out.println("|---|---|---|---|---|---|---|");
        long seed = 7_000_000L;
        for (Trial t : trials()) {
            if (only != null && !t.name.contains(only)) {
                continue;
            }
            Predicate<Level> keep = t.must == null ? l -> true : l -> Techniques.of(l).tags.contains(t.must);
            long start = System.currentTimeMillis();
            ChainBuilder.Built b = ChainBuilder.find(t.recipe, "dry run", seed, threads, 1, timeout, Collections.emptyMap(), keep);
            double secs = (System.currentTimeMillis() - start) / 1000.0;
            seed += 1000;
            if (b == null) {
                System.out.printf("| %s | %d | nothing in %.0fs | | | | |%n", t.name, t.recipe.handSize(), secs);
            } else {
                Techniques.Tags tags = Techniques.of(b.level);
                String list = tags.toString().replaceFirst("^[^:]*: ", "");
                System.out.printf("| %s | %d | %.1fs | %.1f | %d | %d | %s |%n", t.name, tags.hand, secs, tags.score, tags.blind, tags.depth, list);
            }
            System.out.flush();
        }
    }
}
