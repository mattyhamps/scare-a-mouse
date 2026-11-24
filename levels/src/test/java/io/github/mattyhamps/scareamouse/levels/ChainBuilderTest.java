package io.github.mattyhamps.scareamouse.levels;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.util.stream.IntStream;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

/**
 * Every recipe must still be buildable. If a rule change makes a recipe impossible, this fails
 * instead of the generator silently searching forever.
 */
class ChainBuilderTest {

    static IntStream recipes() {
        return IntStream.rangeClosed(61, 260);
    }

    @ParameterizedTest(name = "recipe for level {0}")
    @MethodSource("recipes")
    void recipeProducesAValidLevel(int n) {
        Recipe recipe = Recipe.forLevel(n);
        LevelGenerator.Rng rng = new LevelGenerator.Rng(n * 31L);
        Level found = null;
        // Already-moving recipes with a STOP succeed less often per attempt, but each attempt is quick.
        int attempts = recipe.moving() ? 100000 : 20000;
        for (int attempt = 0; attempt < attempts && found == null; attempt++) {
            Level candidate = ChainBuilder.candidate(recipe, rng, "test");
            if (candidate != null && LevelChecker.check(candidate, recipe.rules()) != null) {
                found = candidate;
            }
        }
        assertNotNull(found, "no valid level built for recipe " + n);
        assertTrue(Simulator.run(found, found.solution).win, "intended solution wins");
        assertFalse(found.inventory.contains(Animal.MOUSE), "never a mouse in your hand");
        assertTrue(found.inventory.size() == recipe.handSize(), "hand size matches the recipe");
    }
}
