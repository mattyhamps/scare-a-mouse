package io.github.mattyhamps.scareamouse.levels;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.mattyhamps.scareamouse.engine.Level;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.IntStream;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

/** Every level in data/levels.json must pass its rules. This is what keeps rule changes honest. */
class LevelsTest {
    static List<Level> levels;

    @BeforeAll
    static void load() throws IOException {
        levels = read();
    }

    static List<Level> read() throws IOException {
        Path file = Paths.get(System.getProperty("levels.file", "../data/levels.json"));
        return Level.listFromJson(new String(Files.readAllBytes(file), StandardCharsets.UTF_8));
    }

    /** Levels are added in batches of ten, or a whole room at a time (the Towers and roof's rooms have 25 levels). */
    @Test
    void levelsComeInBatchesOfTen() {
        int n = levels.size();
        boolean endsTowerRoom = n > 950 && n <= 1075 && (n - 950) % 25 == 0;
        assertTrue(n % 10 == 0 || endsTowerRoom, "level count " + n);
    }

    @ParameterizedTest(name = "tutorial level {0}")
    @MethodSource("tutorials")
    void tutorial(int n) {
        assertTrue(LevelsCli.tutorialOk(levels.get(n - 1)), "level " + n);
    }

    @ParameterizedTest(name = "level {0}")
    @MethodSource("generated")
    void passesRules(int n) {
        Level l = levels.get(n - 1);
        LevelChecker.Verdict v = LevelChecker.check(l, LevelRules.forLevel(n));
        assertNotNull(v, "level " + n + " \"" + l.name + "\" fails its rules");
    }

    /**
     * Every room with levels is drawn: it has a layout in the game's ROOM_SCENES (its floor, road and
     * furniture), its back wall in room-art.json, and a board look in BOARDS. New rooms get their drawing
     * with their levels.
     */
    @Test
    void everyRoomWithLevelsIsDrawn() throws IOException {
        String page = read("../web/src/main/webapp/index.html");
        String art = read("../web/src/main/webapp/room-art.json");
        String rooms = block(page, "const ROOMS = [", "];");
        String scenes = block(page, "const ROOM_SCENES = {", "};");
        String boards = block(page, "const BOARDS = {", "};");
        java.util.regex.Matcher m = java.util.regex.Pattern.compile("\\{end:\\s*(\\d+),\\s*area:\\d+,\\s*name:'([^']+)'").matcher(rooms);
        int start = 0, checked = 0;
        while (m.find()) {
            int end = Integer.parseInt(m.group(1));
            String name = m.group(2);
            if (start < levels.size()) {
                assertTrue(scenes.contains("'" + name + "':"), "the " + name + " has levels but no layout in ROOM_SCENES (index.html)");
                assertTrue(art.contains("\"" + name + "\":\"<"), "the " + name + " has levels but no back wall drawn in room-art.json");
                assertTrue(boards.contains("'" + name + "':"), "the " + name + " has levels but no board look in BOARDS (index.html)");
                checked++;
            }
            start = end;
        }
        assertTrue(checked > 0, "found no rooms in index.html");
    }

    /** No two levels are the same puzzle, counting mirror images and turned boards. */
    @Test
    void noTwoLevelsAreTheSamePuzzle() {
        StringBuilder msg = new StringBuilder();
        for (int[] p : Duplicates.pairs(levels)) {
            msg.append(" level ").append(p[0]).append(" repeats level ").append(p[1]).append(';');
        }
        assertTrue(msg.length() == 0, "Repeated puzzles:" + msg);
    }

    /**
     * A level's name must fit on one line in the header above the board on a small phone (360px wide), next to
     * the cheese count, with a crown or flame before it and the solved tick after it: 20 characters at most.
     * tools/screens/names.js measures the real header; this keeps CI from letting a longer name in.
     */
    @Test
    void levelNamesAreShortEnoughForAPhone() {
        for (int n = 1; n <= levels.size(); n++) {
            String name = levels.get(n - 1).name;
            assertTrue(name.length() <= 20, "level " + n + "'s name is too long for a phone's header (20 characters at most): " + name);
        }
    }

    /** From the Royal floor on, no two flames sit within a few levels of each other. */
    @Test
    void flamesAreSpreadOutFromTheRoyalFloor() {
        List<Integer> hard = Difficulty.hardLevels(levels);
        for (int i = 1; i < hard.size(); i++) {
            if (hard.get(i - 1) >= Difficulty.SPREAD_FROM) {
                assertTrue(hard.get(i) - hard.get(i - 1) > Difficulty.SPREAD,
                        "flames " + hard.get(i - 1) + " and " + hard.get(i) + " are too close");
            }
        }
    }

    /** The flame marks in the game come from data/hard-levels.json; it must match the levels (LevelsCli hard --write). */
    @Test
    void hardLevelsListIsUpToDate() throws IOException {
        String file = new String(Files.readAllBytes(Paths.get("../data/hard-levels.json")), StandardCharsets.UTF_8).trim();
        assertEquals(Difficulty.hardLevels(levels).toString().replace(" ", ""), file,
                "data/hard-levels.json is out of date: run LevelsCli hard --write");
    }

    /** The game is drawn: no emoji anywhere in the page, the room drawings or the levels. */
    @Test
    void theGameHasNoEmoji() throws IOException {
        java.util.regex.Pattern emoji = java.util.regex.Pattern.compile("[\\p{IsExtended_Pictographic}\\x{FE0F}]");
        for (String file : new String[] {"../web/src/main/webapp/index.html", "../web/src/main/webapp/room-art.json", "../data/levels.json"}) {
            String[] lines = read(file).split("\n", -1);
            for (int i = 0; i < lines.length; i++) {
                java.util.regex.Matcher m = emoji.matcher(lines[i]);
                if (m.find()) assertTrue(false, file + " line " + (i + 1) + " has an emoji (" + lines[i].substring(m.start(), Math.min(lines[i].length(), m.start() + 2)) + "); draw it instead");
            }
        }
    }

    private static String read(String path) throws IOException {
        return new String(Files.readAllBytes(Paths.get(path)), StandardCharsets.UTF_8);
    }

    private static String block(String page, String from, String to) {
        int i = page.indexOf(from);
        assertTrue(i >= 0, "index.html has no " + from);
        return page.substring(i, page.indexOf(to, i));
    }

    /** Boards grow as you go: 7x7, then 8x8, 9x9 and 10x10 (see Recipe.sizeForLevel). */
    @ParameterizedTest(name = "level {0} board size")
    @MethodSource("all")
    void boardSizeFollowsTheLevelNumber(int n) {
        Level l = levels.get(n - 1);
        int want = Recipe.sizeForLevel(n);
        assertTrue(l.w == want && l.h == want,
                "level " + n + " is " + l.w + "x" + l.h + ", should be " + want + "x" + want);
    }

    /**
     * After the first ten levels, tips never describe the solution; they can only announce something new
     * (a new animal, or a new kind of board piece such as the Kitchens' counters).
     */
    @ParameterizedTest(name = "level {0} tip")
    @MethodSource("afterTenth")
    void tipDoesNotGiveAwayTheSolution(int n) {
        String tip = levels.get(n - 1).tip;
        assertTrue(tip == null || tip.isEmpty() || tip.startsWith("New animal:") || tip.startsWith("New:"),
                "level " + n + " tip describes the solution: \"" + tip + "\"");
    }

    static IntStream afterTenth() throws IOException {
        return IntStream.rangeClosed(11, read().size());
    }

    static IntStream all() throws IOException {
        return IntStream.rangeClosed(1, read().size());
    }

    static IntStream tutorials() {
        return IntStream.rangeClosed(1, 3);
    }

    static IntStream generated() throws IOException {
        return IntStream.rangeClosed(4, read().size());
    }
}
