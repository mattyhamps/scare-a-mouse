package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Command-line level tools.
 * <pre>
 *   audit                          check every level; exit code 1 if any fail
 *   check N                        explain level N
 *   hard [--write]   (lists the extra-hard levels; --write saves data/hard-levels.json)
 *   trial [--timeout SEC] [--only TEXT]   dry run of new kinds of puzzle (4 and 5 animals, new techniques)
 *   techniques [N] [--from N] [--csv PATH]   which techniques each room's levels use (or one level's)
 *   make N [--seed S] [--threads T] [--timeout SEC] [--name NAME] [--tip TIP] [--balance K] [--write]
 *                                  generate a replacement for level N (or a new level at the end);
 *                                  --write saves it into levels.json
 *   probe FROM TO [--timeout SEC]  dry run: try each recipe in FROM..TO once (default 30s each), save
 *                                  nothing, and list the ones that are slow; run it before a big build
 *   --file PATH                    levels file (default data/levels.json)
 * </pre>
 */
public final class LevelsCli {
    private LevelsCli() {
    }

    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            usage();
            return;
        }
        Path file = Paths.get(option(args, "--file", "data/levels.json"));
        List<Level> levels = Level.listFromJson(new String(Files.readAllBytes(file), StandardCharsets.UTF_8));
        switch (args[0]) {
            case "audit":
                System.exit(audit(levels) ? 0 : 1);
                break;
            case "check":
                explain(levels, Integer.parseInt(args[1]));
                break;
            case "make":
                make(levels, file, args);
                break;
            case "techniques": {   // docs/HARDER_CASTLE.md step 1: which techniques each room uses
                List<Techniques.Room> rooms = Techniques.rooms(Paths.get("web/src/main/webapp/index.html"), levels.size());
                if (args.length > 1 && args[1].matches("[0-9]+")) {   // one level
                    System.out.println(args[1] + ": " + Techniques.of(levels.get(Integer.parseInt(args[1]) - 1)));
                    break;
                }
                int from = Integer.parseInt(option(args, "--from", "1"));
                System.out.print(Techniques.report(levels, rooms, from));
                System.out.println();
                System.out.print(Techniques.stopsAndCatches(levels, rooms, from));
                if (contains(args, "--limits")) {   // where each room breaks the repeat limits
                    for (Techniques.Room room : rooms) {
                        if (room.end >= from) {
                            List<String> problems = Techniques.limitProblems(levels, room.start, room.end);
                            System.out.println(room.name + ": " + (problems.isEmpty() ? "keeps the limits" : problems.size() + " problems: " + problems));
                        }
                    }
                }
                String csv = option(args, "--csv", null);
                if (csv != null) {
                    Files.write(Paths.get(csv), Techniques.perLevel(levels, rooms).getBytes(StandardCharsets.UTF_8));
                    System.out.println("Saved every level's tags to " + csv);
                }
                break;
            }
            case "trial":   // docs/HARDER_CASTLE.md step 2: try new kinds of puzzle, save nothing
                DryRun.run(Long.parseLong(option(args, "--timeout", "60")), option(args, "--only", null));
                System.exit(0);   // don't wait for checks still running past the time limit
                break;
            case "probe":
                probe(Integer.parseInt(args[1]), Integer.parseInt(args[2]),
                        Long.parseLong(option(args, "--timeout", "30")));
                break;
            case "hard": {   // the extra-hard levels (marked with a flame in the game); --write saves them
                List<Integer> hard = Difficulty.hardLevels(levels);
                System.out.println(hard.size() + " extra-hard levels: " + hard);
                if (java.util.Arrays.asList(args).contains("--write")) {
                    Path out = Paths.get(option(args, "--hard-file", "data/hard-levels.json"));
                    Files.write(out, (hard + "\n").replace(" ", "").getBytes(StandardCharsets.UTF_8));
                    System.out.println("Saved to " + out);
                }
                break;
            }
            default:
                usage();
        }
    }

    static boolean audit(List<Level> levels) {
        List<Integer> failed = new ArrayList<>();
        for (int n = 1; n <= levels.size(); n++) {
            boolean ok = n <= 3 ? tutorialOk(levels.get(n - 1)) : LevelChecker.check(levels.get(n - 1), LevelRules.forLevel(n)) != null;
            if (!ok) {
                failed.add(n);
            }
        }
        if (failed.isEmpty()) {
            System.out.println("All " + levels.size() + " levels pass.");
            return true;
        }
        System.out.println("Failing levels: " + failed);
        return false;
    }

    /** Tutorials 1-3: the intended solution wins, nothing placed doesn't, and there's exactly one solution. */
    public static boolean tutorialOk(Level l) {
        return Simulator.run(l, l.solution).win
                && !Simulator.run(l, Collections.<Piece>emptyList()).win
                && LevelChecker.solutions(l, l.inventory, 2).size() == 1;
    }

    private static void explain(List<Level> levels, int n) {
        Level l = levels.get(n - 1);
        System.out.println("Level " + n + " \"" + l.name + "\": hand " + l.inventory + ", " + l.fixed.size()
                + " board animals, " + l.walls.size() + " walls");
        if (n <= 3) {
            System.out.println(tutorialOk(l) ? "Tutorial OK" : "Tutorial FAILS");
            return;
        }
        LevelChecker.Verdict v = LevelChecker.check(l, LevelRules.forLevel(n));
        System.out.println(v == null ? "FAILS the rules"
                : "PASSES: " + v.solutions + " solution(s), chain depth " + v.depth + ", solution " + v.solution);
    }

    private static void make(List<Level> levels, Path file, String[] args) throws IOException, InterruptedException {
        int n = Integer.parseInt(args[1]);
        long seed = Long.parseLong(option(args, "--seed", String.valueOf(n * 1000L)));
        int threads = Integer.parseInt(option(args, "--threads", String.valueOf(Runtime.getRuntime().availableProcessors())));
        long timeout = Long.parseLong(option(args, "--timeout", "900"));
        if (n > levels.size() + 1) {
            System.out.println("Make level " + (levels.size() + 1) + " first.");
            System.exit(2);
        }
        boolean adding = n == levels.size() + 1;
        Level old = adding ? null : levels.get(n - 1);
        String name = option(args, "--name", adding ? "Level " + n : old.name);
        String tip = option(args, "--tip", adding ? "" : old.tip);
        long start = System.currentTimeMillis();
        if (n == Recipe.TRAPDOOR_INTRO) {   // made by hand, like level 1: the trapdoors take the mouse under a mousetrap
            save(levels, file, args, n, TrapdoorLab.intro(name, option(args, "--tip", adding ? "New: trapdoors!" : old.tip)), start);
            return;
        }
        Recipe recipe = Recipe.forLevel(n);
        if (Recipe.TRAP_INTRO.containsKey(n)) {   // the mouse-and-cats levels that bring in mousetraps
            String introTip = option(args, "--tip", adding ? recipe.tip : old.tip);
            Level level = TrapLab.catsOnly(new java.util.Random(seed), Recipe.TRAP_INTRO.get(n)[0], Recipe.TRAP_INTRO.get(n)[1],
                    Recipe.TRAP_INTRO.get(n)[2], (int) Math.min(timeout, 60), name, introTip);
            if (level == null) {
                System.out.println("No level built. Try another --seed.");
                System.exit(2);
            }
            save(levels, file, args, n, level, start);
            return;
        }
        if (recipe != null) {
            buildDesigned(levels, file, args, n, recipe, name, option(args, "--tip", null), seed, threads, timeout, start);
            return;
        }
        LevelGenerator.Found found = LevelGenerator.searchParallel(LevelRules.forLevel(n), seed, threads, timeout, name, tip);
        if (found == null) {
            System.out.println("No level found in " + timeout + "s. Try another --seed or a longer --timeout.");
            System.exit(2);
        }
        System.out.printf("Found level %d in %.1fs (seed %d, %d tries on the winning thread): %d solution(s), depth %d%n",
                n, (System.currentTimeMillis() - start) / 1000.0, found.seed, found.tries,
                found.verdict.solutions, found.verdict.depth);
        if (args.length > 2 && contains(args, "--write")) {
            if (adding) {
                levels.add(found.level);
            } else {
                levels.set(n - 1, found.level);
            }
            Files.write(file, Level.listToJson(levels).getBytes(StandardCharsets.UTF_8));
            System.out.println("Saved to " + file);
        } else {
            System.out.println(io.github.mattyhamps.scareamouse.engine.Json.write(found.level.toJson()));
        }
    }

    /**
     * A quick dry run before building a batch: tries to build one level from each recipe in FROM..TO with a
     * short time limit, saves nothing, and lists the recipes that are slow or can't be built, so they can be
     * changed before a long build gets stuck on them. Exit code 1 if any are slow.
     */
    private static void probe(int from, int to, long timeout) throws InterruptedException {
        int threads = Runtime.getRuntime().availableProcessors();
        List<String> slow = new ArrayList<>();
        for (int n = from; n <= to; n++) {
            Recipe recipe = Recipe.forLevel(n);
            if (recipe == null || Recipe.TRAP_INTRO.containsKey(n)) {   // the mouse-and-cats levels are quick to make
                continue;
            }
            long start = System.currentTimeMillis();
            ChainBuilder.Built built = ChainBuilder.find(recipe, "probe", n * 1000L, threads, 1, timeout);
            double secs = (System.currentTimeMillis() - start) / 1000.0;
            System.out.printf("%d %s in %.1fs  (%s)%s%n", n, built == null ? "SLOW, nothing" : "ok", secs, recipe.key(),
                    built == null ? "" : "  -> " + Techniques.of(built.level));
            if (built == null) {
                slow.add(n + " (" + recipe.key() + ")");
            }
        }
        System.out.println(slow.isEmpty() ? "Every recipe in " + from + "-" + to + " builds within " + timeout + "s."
                : slow.size() + " slow recipe(s), change them before building: " + slow);
        System.exit(slow.isEmpty() ? 0 : 1);
    }

    /** Designed levels: the chain builder makes several candidates and keeps the most interesting. */
    private static void buildDesigned(List<Level> levels, Path file, String[] args, int n, Recipe recipe, String name,
                                      String tipOverride, long seed, int threads, long timeout, long start)
            throws IOException, InterruptedException {
        int want = Integer.parseInt(option(args, "--candidates", "6"));
        // --balance K: keep the animals you place varied, compared with the K levels before this one.
        int window = Integer.parseInt(option(args, "--balance", "0"));
        java.util.Map<io.github.mattyhamps.scareamouse.engine.Animal, Integer> recent = new java.util.HashMap<>();
        for (int k = Math.max(0, n - 1 - window); k < Math.min(n - 1, levels.size()); k++) {
            for (io.github.mattyhamps.scareamouse.engine.Animal a : levels.get(k).inventory) {
                recent.merge(a, 1, Integer::sum);
            }
        }
        // keep puzzle styles from repeating: candidates that repeat the 8 levels before lose points (Matt's limits)
        List<Level> before = new ArrayList<>(levels.subList(Math.max(0, n - 1 - Techniques.STYLE_GAP), Math.min(n - 1, levels.size())));
        java.util.function.Predicate<Level> keep = l -> true;
        if (contains(args, "--strict")) {   // only candidates that keep the room's repeat limits (and use the recipe's new technique)
            keep = strictFilter(levels, n, recipe);
        }
        ChainBuilder.Built built = ChainBuilder.find(recipe, name, seed, threads, want, timeout, recent, keep,
                l -> Techniques.repeatPenalty(l, before));
        // a trap level where a trap doesn't matter to the puzzle: try a few more seeds before giving up
        for (int k = 1; k <= 6 && built != null && !built.level.traps.isEmpty()
                && !TrapLab.trapsDoTheirJob(built.level, recipe.springTraps); k++) {
            built = ChainBuilder.find(recipe, name, seed + k * 104729L, threads, want, timeout, recent);
        }
        if (built == null) {
            System.out.println("No level built in " + timeout + "s. Try another --seed or a longer --timeout.");
            System.exit(2);
        }
        Level level = tipOverride == null ? built.level : built.level.withNameAndTip(name, tipOverride);
        if (!level.traps.isEmpty() && !TrapLab.trapsDoTheirJob(level, recipe.springTraps)) {   // every trap has to matter
            System.out.println("Built level " + n + " but a trap doesn't matter to the puzzle. Try another --seed.");
            System.exit(3);
        }
        int twin = Duplicates.twin(levels, level, n);
        if (twin > 0) {   // the same puzzle (or its mirror image) as another level: try another seed
            System.out.println("Built level " + n + " but it is the same puzzle as level " + twin + ". Try another --seed.");
            System.exit(3);
        }
        System.out.printf("Built level %d in %.1fs (seed %d): %s%n", n, (System.currentTimeMillis() - start) / 1000.0,
                built.seed, Interest.breakdown(level));
        if (contains(args, "--write")) {
            if (n == levels.size() + 1) {
                levels.add(level);
            } else {
                levels.set(n - 1, level);
            }
            Files.write(file, Level.listToJson(levels).getBytes(StandardCharsets.UTF_8));
            System.out.println("Saved to " + file);
        } else {
            System.out.println(io.github.mattyhamps.scareamouse.engine.Json.write(level.toJson()));
        }
    }

    /**
     * The --strict filter for level n: the candidate keeps the repeat limits of its room, counting the room's levels
     * before n (a room is built in order, so those are the new ones) and the tricks the room's later recipes ask for,
     * so a level never spends an allowance a later level needs. It must use the technique its recipe asks for (a
     * freeze on purpose, a standoff, the mouse turning). A trick it uses by chance is fine (it makes the level harder)
     * as long as the rest of the room still fits: not in the 3 levels after it if they ask for it, and within the room's
     * allowance counting every later recipe that asks for it.
     */
    private static java.util.function.Predicate<Level> strictFilter(List<Level> levels, int n, Recipe recipe) throws IOException {
        Techniques.Room room = null;
        for (Techniques.Room r : Techniques.rooms(Paths.get("web/src/main/webapp/index.html"), Integer.MAX_VALUE)) {
            if (r.start <= n && n <= r.end) {
                room = r;
            }
        }
        if (room == null) {
            return l -> true;
        }
        List<Techniques.Tags> before = new ArrayList<>();
        for (int k = room.start; k < n && k <= levels.size(); k++) {
            before.add(Techniques.of(levels.get(k - 1)));
        }
        int size = room.end - room.start + 1;
        java.util.Set<Techniques.Tag> must = java.util.EnumSet.noneOf(Techniques.Tag.class);
        for (Recipe.Move m : recipe.moves) {
            if (m == Recipe.Move.PIN) {
                must.add(Techniques.Tag.PIN);
            } else if (m == Recipe.Move.STANDOFF) {
                must.add(Techniques.Tag.STANDOFF);
            }
        }
        if (recipe.mouseTurns >= 2) {
            must.add(Techniques.Tag.MOUSE_TURNS);
        }
        java.util.Map<Techniques.Tag, Integer> later = new java.util.EnumMap<>(Techniques.Tag.class);
        java.util.Set<Techniques.Tag> next3 = java.util.EnumSet.noneOf(Techniques.Tag.class);
        for (int k = n + 1; k <= room.end; k++) {
            Recipe r = Recipe.forLevel(k);
            if (r == null) {
                continue;
            }
            for (Techniques.Tag g : asked(r)) {
                later.merge(g, 1, Integer::sum);
                if (k - n <= Techniques.HEADLINE_GAP) {
                    next3.add(g);
                }
            }
        }
        java.util.Set<Techniques.Tag> mine = asked(recipe);
        final int roomSize = size;
        return l -> {
            Techniques.Tags t = Techniques.of(l);
            if (!t.tags.containsAll(must) || Techniques.breaks(t, before, roomSize) != null) {
                return false;
            }
            for (Techniques.Tag g : t.tags) {
                int most = Techniques.most(g, roomSize);
                if (most == Integer.MAX_VALUE) {
                    continue;
                }
                int used = 0;
                for (Techniques.Tags b : before) {
                    used += b.tags.contains(g) ? 1 : 0;
                }
                if (used + 1 + later.getOrDefault(g, 0) > most) {
                    return false;   // the room's later levels need this allowance
                }
                if (!mine.contains(g) && Techniques.HEADLINE.contains(g) && next3.contains(g)) {
                    return false;   // a trick by chance that one of the next 3 levels asks for
                }
            }
            return true;
        };
    }

    /** The techniques a recipe asks for (what the level is built to use). */
    static java.util.Set<Techniques.Tag> asked(Recipe recipe) {
        java.util.Set<Techniques.Tag> asked = java.util.EnumSet.noneOf(Techniques.Tag.class);
        for (Recipe.Move m : recipe.moves) {
            asked.add(m == Recipe.Move.STOP ? Techniques.Tag.STOP : m == Recipe.Move.SWERVE ? Techniques.Tag.SWERVE
                    : m == Recipe.Move.CATCH ? Techniques.Tag.CATCH : m == Recipe.Move.PIN ? Techniques.Tag.PIN : Techniques.Tag.STANDOFF);
        }
        if (recipe.has(Recipe.Trick.FREEZE_RELEASE)) {
            asked.add(Techniques.Tag.FREEZE);
        }
        if (recipe.has(Recipe.Trick.WAITING_RUNNER)) {
            asked.add(Techniques.Tag.WAITING);
        }
        if (recipe.laneBlockers > 0 || recipe.wrapAround) {
            asked.add(Techniques.Tag.LANE);
        }
        if (recipe.wrapAround) {
            asked.add(Techniques.Tag.WRAP);
        }
        if (recipe.mouseTurns >= 2) {
            asked.add(Techniques.Tag.MOUSE_TURNS);
        }
        if (recipe.springTraps > 0) {
            asked.add(Techniques.Tag.SPRING);
        }
        return asked;
    }

    /** Saves a level built some other way (the mouse-and-cats trap levels), after the repeat check. */
    private static void save(List<Level> levels, Path file, String[] args, int n, Level level, long start) throws IOException {
        int twin = Duplicates.twin(levels, level, n);
        if (twin > 0) {
            System.out.println("Built level " + n + " but it is the same puzzle as level " + twin + ". Try another --seed.");
            System.exit(3);
        }
        System.out.printf("Built level %d in %.1fs: %s%n", n, (System.currentTimeMillis() - start) / 1000.0, Interest.breakdown(level));
        if (contains(args, "--write")) {
            if (n == levels.size() + 1) {
                levels.add(level);
            } else {
                levels.set(n - 1, level);
            }
            Files.write(file, Level.listToJson(levels).getBytes(StandardCharsets.UTF_8));
            System.out.println("Saved to " + file);
        } else {
            System.out.println(io.github.mattyhamps.scareamouse.engine.Json.write(level.toJson()));
        }
    }

    private static String option(String[] args, String name, String fallback) {
        for (int i = 0; i + 1 < args.length; i++) {
            if (args[i].equals(name)) {
                return args[i + 1];
            }
        }
        return fallback;
    }

    private static boolean contains(String[] args, String flag) {
        for (String a : args) {
            if (a.equals(flag)) {
                return true;
            }
        }
        return false;
    }

    private static void usage() {
        System.out.println("Usage: audit | check N | hard [--write] | techniques [N] [--from N] [--csv PATH] | probe FROM TO [--timeout SEC] | make N [--seed S] [--threads T] [--timeout SEC] [--name NAME] [--tip TIP] [--write]  [--file PATH]");
    }
}
