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
@org.junit.jupiter.api.Tag("builder")
class ChainBuilderTest {
    private static final long TIME_PER_RECIPE_MS = 180_000;
    private static final int ATTEMPTS_PER_SEED = 2_000;
    /**
     * Rare recipes and a seed that is known to build them (found by searching offline), tried first so the
     * test stays quick. If a change to the rules or the builder stops it working, the normal search runs.
     */
    private static final java.util.Map<Integer, Long> KNOWN_SEEDS = java.util.Map.of(291, 349_538L, 305, 2_266_370L,
            306, 120_352L, 350, 18_769L);

    /**
     * The first level made with each distinct recipe. Many levels share a recipe (with different layouts),
     * and building each kind once is enough to show it can still be built.
     */
    static IntStream recipes() {
        java.util.Set<String> seen = new java.util.HashSet<>();
        return IntStream.rangeClosed(61, 500).filter(n -> seen.add(Recipe.forLevel(n).key()));
    }

    @ParameterizedTest(name = "recipe for level {0}")
    @MethodSource("recipes")
    void recipeProducesAValidLevel(int n) {
        Recipe recipe = Recipe.forLevel(n);
        Level found = null;
        // Like the level maker, search from several seeds: a fresh seed every few thousand attempts, until a
        // level turns up or the time runs out. (One fixed seed and a fixed number of attempts was too strict
        // for the rarer recipes, such as an already-moving chain with a swerve and a stop.)
        long deadline = System.currentTimeMillis() + TIME_PER_RECIPE_MS;
        for (int k = KNOWN_SEEDS.containsKey(n) ? -1 : 0; found == null && System.currentTimeMillis() < deadline; k++) {
            LevelGenerator.Rng rng = new LevelGenerator.Rng(k < 0 ? KNOWN_SEEDS.get(n) : n * 31L + k * 7919L);
            for (int attempt = 0; attempt < ATTEMPTS_PER_SEED && found == null; attempt++) {
                Level candidate = ChainBuilder.candidate(recipe, rng, "test");
                if (candidate != null && LevelChecker.check(candidate, recipe.rules()) != null) {
                    found = candidate;
                }
            }
        }
        assertNotNull(found, "no valid level built for recipe " + n);
        assertTrue(Simulator.run(found, found.solution).win, "intended solution wins");
        assertFalse(found.inventory.contains(Animal.MOUSE), "never a mouse in your hand");
        assertTrue(found.inventory.size() == recipe.handSize(), "hand size matches the recipe");
    }
}
