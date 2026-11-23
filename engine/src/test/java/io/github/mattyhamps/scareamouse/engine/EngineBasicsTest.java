package io.github.mattyhamps.scareamouse.engine;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import java.util.Collections;
import org.junit.jupiter.api.Test;

class EngineBasicsTest {

    @Test
    void foodChainWrapsAround() {
        assertEquals(Animal.CAT, Animal.MOUSE.predator());
        assertEquals(Animal.DOG, Animal.CAT.predator());
        assertEquals(Animal.BEAR, Animal.DOG.predator());
        assertEquals(Animal.LION, Animal.BEAR.predator());
        assertEquals(Animal.ELEPHANT, Animal.LION.predator());
        assertEquals(Animal.MOUSE, Animal.ELEPHANT.predator());
    }

    @Test
    void placedAnimalsCount() {
        Level level = BoardPicture.level(Arrays.asList(".M....."), new int[] {-1, 0});
        assertFalse(Simulator.run(level, Collections.<Piece>emptyList()).win);
        assertTrue(Simulator.run(level, Arrays.asList(new Piece(Animal.CAT, 2, 0))).win);
    }

    @Test
    void standoffIsReported() {
        // Both cats flee their dogs toward the middle square at the same time: neither moves.
        Level level = BoardPicture.level(Arrays.asList("DC.CD"), null);
        SimResult r = Simulator.record(level, Collections.<Piece>emptyList());
        assertEquals(Arrays.asList(1, 2), r.bumps.get(1)); // the two cats (ids follow reading order: D=0, C=1, C=2, D=3)
        assertTrue(r.bumps.get(0).isEmpty());
    }

    @Test
    void jsonRoundTrip() {
        String text = "{\"name\":\"T\",\"tip\":\"a \\\"tip\\\"\",\"w\":7,\"h\":7,\"hole\":[-1,3],\"walls\":[[2,2]],"
                + "\"fixed\":[{\"t\":\"mouse\",\"x\":3,\"y\":3}],\"inv\":[\"cat\"],\"solution\":[{\"t\":\"cat\",\"x\":4,\"y\":3}]}";
        assertEquals(text, Json.write(Level.fromJson(Json.parse(text)).toJson()));
    }
}
