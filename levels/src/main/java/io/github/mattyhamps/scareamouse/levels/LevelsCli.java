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
 *   make N [--seed S] [--threads T] [--timeout SEC] [--name NAME] [--tip TIP] [--write]
 *                                  generate a replacement for level N (or a new level at the end);
 *                                  --write saves it into levels.json
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
        System.out.println("Usage: audit | check N | make N [--seed S] [--threads T] [--timeout SEC] [--name NAME] [--tip TIP] [--write]  [--file PATH]");
    }
}
