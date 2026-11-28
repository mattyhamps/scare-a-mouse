package io.github.mattyhamps.scareamouse.levels;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

/**
 * The quicker search for 4 and 5 animals ({@link FrontierSearch}) must find the same winning placements as
 * trying every square. Checked on real levels, on those levels with one board piece taken away (the checker's
 * clutter rule asks about those), and with one animal fewer in the hand.
 */
class FrontierSearchTest {
    @Test
    void findsTheSamePlacementsAsTryingEverySquare() throws Exception {
        List<Level> levels = Level.listFromJson(new String(Files.readAllBytes(Paths.get("../data/levels.json")), StandardCharsets.UTF_8));
        int compared = 0;
        for (int n = 1; n <= levels.size(); n += 9) {
            Level level = levels.get(n - 1);
            List<Level> variants = new ArrayList<>();
            variants.add(level);
            for (int i = 1; i < level.fixed.size(); i += 2) {
                variants.add(level.withoutFixed(i));
            }
            for (int i = 0; i < level.walls.size(); i++) {
                variants.add(level.withoutWall(i));
            }
            for (int i = 0; i < level.traps.size(); i++) {
                variants.add(level.withoutTrap(i));
            }
            for (Level v : variants) {
                for (List<Animal> hand : hands(level.inventory)) {
                    for (int cap : new int[] {1, 2, 12}) {
                        compare(n, v, hand, cap);
                        compared++;
                    }
                }
            }
        }
        System.out.println("FrontierSearchTest: " + compared + " searches agree");
    }

    /** The level's hand, and the hand with each animal left out. */
    private static List<List<Animal>> hands(List<Animal> inventory) {
        List<List<Animal>> out = new ArrayList<>();
        out.add(inventory);
        for (int i = 0; i < inventory.size() && inventory.size() > 1; i++) {
            List<Animal> fewer = new ArrayList<>(inventory);
            fewer.remove(i);
            out.add(fewer);
        }
        return out;
    }

    static void compare(int n, Level level, List<Animal> hand, int cap) {
        List<List<Piece>> all = LevelChecker.allPlacements(level, hand, cap);
        List<List<Piece>> quick = FrontierSearch.solutions(level, hand, cap);
        if (all.size() < cap) {
            assertEquals(str(all), str(quick), "level " + n + " hand " + hand + " cap " + cap);
        } else {
            assertEquals(cap, quick.size(), "level " + n + " hand " + hand + " cap " + cap + ": both should reach the cap");
        }
    }

    private static String str(List<List<Piece>> sols) {
        StringBuilder s = new StringBuilder();
        for (List<Piece> p : sols) {
            for (Piece q : p) {
                s.append(q.type).append(q.x).append(',').append(q.y).append(' ');
            }
            s.append('|');
        }
        return s.toString();
    }
}
