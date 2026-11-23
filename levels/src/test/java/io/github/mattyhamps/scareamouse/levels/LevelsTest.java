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

    @Test
    void levelsComeInBatchesOfTen() {
        assertEquals(0, levels.size() % 10, "level count " + levels.size());
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

    /** After the first ten levels, tips never describe the solution; they can only announce a new animal. */
    @ParameterizedTest(name = "level {0} tip")
    @MethodSource("afterTenth")
    void tipDoesNotGiveAwayTheSolution(int n) {
        String tip = levels.get(n - 1).tip;
        assertTrue(tip == null || tip.isEmpty() || tip.startsWith("New animal:"),
                "level " + n + " tip describes the solution: \"" + tip + "\"");
    }

    static IntStream afterTenth() throws IOException {
        return IntStream.rangeClosed(11, read().size());
    }

    static IntStream tutorials() {
        return IntStream.rangeClosed(1, 3);
    }

    static IntStream generated() throws IOException {
        return IntStream.rangeClosed(4, read().size());
    }
}
