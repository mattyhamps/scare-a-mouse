package io.github.mattyhamps.scareamouse.engine;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;
import org.junit.jupiter.api.Named;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

/**
 * One test per scenario in physics-fixtures.json: a board picture, optional placed animals,
 * and what the rulebook says should happen. The same file is used to check the
 * JavaScript build of the engine in CI.
 */
class PhysicsTest {

    static Stream<Arguments> fixtures() throws IOException {
        List<Arguments> out = new ArrayList<>();
        for (Object o : (List<?>) Json.parse(resource("/physics-fixtures.json"))) {
            Map<?, ?> f = (Map<?, ?>) o;
            out.add(Arguments.of(Named.of((String) f.get("name"), f)));
        }
        return out.stream();
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("fixtures")
    void scenario(Map<?, ?> fixture) {
        List<String> board = strings(fixture.get("board"));
        List<?> holeJson = (List<?>) fixture.get("hole");
        int[] hole = holeJson == null ? null : new int[] {Json.toInt(holeJson.get(0)), Json.toInt(holeJson.get(1))};
        Level level = BoardPicture.level(board, hole);
        SimResult r = Simulator.record(level, Piece.listFromJson(fixture.get("placed")));
        Map<?, ?> expect = (Map<?, ?>) fixture.get("expect");

        if (expect.containsKey("pic")) {
            assertEquals(String.join("/", strings(expect.get("pic"))),
                    String.join("/", BoardPicture.render(level, r.lastFrame())), "final board");
        }
        if (expect.containsKey("win")) {
            assertEquals(expect.get("win"), r.win, "win");
        }
        if (expect.containsKey("loop")) {
            assertEquals(expect.get("loop"), r.loop, "loop");
        }
        if (expect.containsKey("steps")) {
            assertEquals(Json.toInt(expect.get("steps")), r.frames.size() - 1, "steps");
        }
    }

    private static List<String> strings(Object json) {
        List<String> out = new ArrayList<>();
        for (Object o : (List<?>) json) {
            out.add((String) o);
        }
        return out;
    }

    private static String resource(String path) throws IOException {
        try (InputStream in = PhysicsTest.class.getResourceAsStream(path)) {
            assertNotNull(in, path);
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }
    }
}
