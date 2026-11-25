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
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.IntStream;

/**
 * Prototype: tries adding one turn tile to existing levels and keeps the boards where the tile is
 * needed and actually turns an animal. Usage: TurnLab levels.json out.json from to triesPerLevel
 */
public final class TurnLab {
    private static final int[][] DIRS = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};

    public static void main(String[] args) throws Exception {
        // Usage: TurnLab out.json from to secondsPerLevel  (builds levels from those levels' recipes, plus one turn tile)
        if (args[1].equals("easy")) {   // TurnLab out.json easy firstSlot count: easy intro levels (one animal to place)
            easy(args[0], Integer.parseInt(args[2]), Integer.parseInt(args[3]));
            return;
        }
        int from = Integer.parseInt(args[1]), to = Integer.parseInt(args[2]), secs = Integer.parseInt(args[3]);
        List<Level> out = new ArrayList<>();
        long t0 = System.currentTimeMillis();
        for (int n = from; n <= to; n++) {
            Recipe r = Recipe.forLevel(n);
            if (r == null) {
                continue;
            }
            r = r.withSize(Recipe.sizeForLevel(n)).withTurnTiles(1);
            ChainBuilder.Built b = ChainBuilder.find(r, "Test " + n, 1000L * n, 2, 2, secs);
            if (b == null) {
                System.out.println("level " + n + ": none (" + r.key() + ")");
                continue;
            }
            boolean turns = turnsSomething(b.level, b.level.solution);
            System.out.println("level " + n + ": turn " + Arrays.toString(b.level.turns.get(0)) + " turns=" + turns
                    + " depth " + b.verdict.depth + " hand " + b.level.inventory + " score " + String.format("%.1f", b.score));
            if (turns) {
                out.add(b.level);
            }
            Files.write(Paths.get(args[0]), Level.listToJson(out).getBytes(StandardCharsets.UTF_8));
        }
        System.out.println(out.size() + " of " + (to - from + 1) + " in " + (System.currentTimeMillis() - t0) / 1000 + "s");
    }

    /** Easy levels: you place one bear; it scares a dog, which turns on the tile, and so on to the mouse. */
    static void easy(String outPath, int firstSlot, int count) throws Exception {
        List<Level> out = new ArrayList<>();
        Animal[] triggers = {Animal.BEAR, Animal.BEAR, Animal.LION, Animal.BEAR, Animal.LION};
        for (int k = 0; k < count; k++) {
            Recipe r = new Recipe(triggers[k % triggers.length], 0, false, "New: turn tiles!", Recipe.Trick.PLAIN)
                    .withSize(10).withTurnTiles(1);
            ChainBuilder.Built b = ChainBuilder.find(r, "Test " + (firstSlot + k), 77L * (k + 1), 2, 4, 60);
            if (b == null || !turnsSomething(b.level, b.level.solution)) {
                System.out.println("easy " + k + ": none");
                continue;
            }
            System.out.println("easy " + (firstSlot + k) + ": turn " + Arrays.toString(b.level.turns.get(0)) + " hand " + b.level.inventory
                    + " depth " + b.verdict.depth);
            out.add(b.level);
            Files.write(Paths.get(outPath), Level.listToJson(out).getBytes(StandardCharsets.UTF_8));
        }
    }

    /** True if, in the solution, some animal runs onto the tile going another way than its arrow. */
    static boolean turnsSomething(Level l, List<Piece> sol) {
        int[] t = l.turns.get(0);
        List<List<SimResult.Snapshot>> f = Simulator.record(l, sol).frames;
        for (int i = 1; i < f.size(); i++) {
            for (SimResult.Snapshot a : f.get(i)) {
                SimResult.Snapshot b = f.get(i - 1).get(a.id);
                if (a.x == t[0] && a.y == t[1] && (b.x != a.x || b.y != a.y)) {
                    int dx = a.x - b.x, dy = a.y - b.y;
                    if (dx != DIRS[t[2]][0] || dy != DIRS[t[2]][1]) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    static boolean sameAs(List<Piece> a, List<Piece> b) {
        if (a.size() != b.size()) {
            return false;
        }
        for (Piece p : a) {
            boolean hit = false;
            for (Piece q : b) {
                hit |= p.type == q.type && p.x == q.x && p.y == q.y;
            }
            if (!hit) {
                return false;
            }
        }
        return true;
    }
}
