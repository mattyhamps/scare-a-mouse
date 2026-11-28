package io.github.mattyhamps.scareamouse.levels;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.levels.Techniques.Tag;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The technique tags (docs/HARDER_CASTLE.md step 1) match what some levels' recipes ask for. */
class TechniquesTest {
    private static List<Level> levels() throws Exception {
        return Level.listFromJson(new String(Files.readAllBytes(Paths.get("../data/levels.json")), StandardCharsets.UTF_8));
    }

    @Test
    void tagsMatchTheRecipes() throws Exception {
        List<Level> levels = levels();
        // 1011: an already-moving level where you swerve one runner and stop another
        Techniques.Tags t = Techniques.of(levels.get(1010));
        assertTrue(t.tags.containsAll(List.of(Tag.STOP, Tag.SWERVE, Tag.MOVING)), t.toString());
        // 1016: moving, a stop and a missing link put back
        t = Techniques.of(levels.get(1015));
        assertTrue(t.tags.containsAll(List.of(Tag.STOP, Tag.CATCH)), t.toString());
        // 33: one elephant next to the lion, nothing else going on
        assertEquals("[]", Techniques.of(levels.get(32)).tags.toString());
    }

    @Test
    void reportCoversEveryRoom() throws Exception {
        List<Level> levels = levels();
        List<Techniques.Room> rooms = Techniques.rooms(Paths.get("../web/src/main/webapp/index.html"), levels.size());
        assertEquals(1, rooms.get(0).start);
        assertEquals(levels.size(), rooms.get(rooms.size() - 1).end);
        String report = Techniques.report(levels, rooms, 1);
        assertEquals(rooms.size() + 2, report.split("\n").length);   // a header, a divider and a row per room
    }

    @Test
    void rebuiltRoomsKeepTheRepeatLimits() throws Exception {
        List<Level> levels = levels();
        List<Techniques.Room> rooms = Techniques.rooms(Paths.get("../web/src/main/webapp/index.html"), levels.size());
        StringBuilder problems = new StringBuilder();
        for (Techniques.Room room : rooms) {
            if (Techniques.REBUILT_ROOMS.contains(room.name)) {
                List<String> p = Techniques.limitProblems(levels, room.start, room.end);
                if (!p.isEmpty()) {
                    problems.append(room.name).append(": ").append(p).append('\n');
                }
            }
        }
        assertEquals("", problems.toString(), "rooms that break the repeat limits (docs/HARDER_CASTLE_REPORT.md)");
    }

    @Test
    void limitsSpotRepeatsInTodaysLevels() throws Exception {
        // The Watchtower (1001-1025) has stops in 1011, 1016, 1018: the limits must notice
        List<String> p = Techniques.limitProblems(levels(), 1001, 1025);
        assertTrue(p.stream().anyMatch(s -> s.contains("repeats stop")), p.toString());
        assertEquals("2: stop, swerve, freeze-release, moving start", Techniques.style(Techniques.of(levels().get(1010))));
    }
}
