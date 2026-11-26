package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * What each level number is supposed to be: how many animals you place, which animals appear,
 * how crowded the board is, and how hard it must be. The checker and generator both read this.
 */
public final class LevelRules {
    private static final List<Animal> C = Arrays.asList(Animal.CAT, Animal.DOG, Animal.BEAR);
    private static final List<Animal> CL = Arrays.asList(Animal.CAT, Animal.DOG, Animal.BEAR, Animal.LION);
    private static final List<Animal> CLE = Arrays.asList(Animal.CAT, Animal.DOG, Animal.BEAR, Animal.LION, Animal.ELEPHANT);

    /** Number of animals the player places (1 or 2). */
    public final int pieces;
    public final int fixedMin;
    public final int fixedMax;
    public final int wallsMin;
    public final int wallsMax;
    /** Animals that can appear on the board. */
    public final List<Animal> types;
    /** Animals that can be in the player's hand. */
    public final List<Animal> handTypes;
    /** Animals forced onto the board (in order, after the mouse), for levels that introduce something. */
    public final List<Animal> ensure;
    /** Animal forced into the player's hand, or null. */
    public final Animal mustPlace;
    /** Board animal that must move in the solution, or null. */
    public final Animal mustMove;
    /** At most this many solutions. */
    public final int maxSolutions;
    /** In every solution, at least this many other animals start running before the mouse does. */
    public final int minDepth;
    /** In every solution, at least this many animals move (0 = no rule). */
    public final int minMoved;
    /** Every piece on the board must change the puzzle (false only for hand-made teaching levels, see {@link #teaching}). */
    public final boolean clutterCheck;

    private LevelRules(int pieces, int fixedMin, int fixedMax, int wallsMin, int wallsMax, List<Animal> types,
                       List<Animal> handTypes, List<Animal> ensure, Animal mustPlace, Animal mustMove,
                       int maxSolutions, int minDepth) {
        this(pieces, fixedMin, fixedMax, wallsMin, wallsMax, types, handTypes, ensure, mustPlace, mustMove,
                maxSolutions, minDepth, 0);
    }

    /** Rules for a built level: how many animals you place and how long the chain must be. */
    public static LevelRules forBuilt(int pieces, int minDepth, int minMoved) {
        return new LevelRules(pieces, 0, 0, 0, 0, CLE, CLE, Collections.<Animal>emptyList(), null, null,
                1, minDepth, minMoved);
    }

    private LevelRules(int pieces, int fixedMin, int fixedMax, int wallsMin, int wallsMax, List<Animal> types,
                       List<Animal> handTypes, List<Animal> ensure, Animal mustPlace, Animal mustMove,
                       int maxSolutions, int minDepth, int minMoved) {
        this.pieces = pieces;
        this.fixedMin = fixedMin;
        this.fixedMax = fixedMax;
        this.wallsMin = wallsMin;
        this.wallsMax = wallsMax;
        this.types = types;
        this.handTypes = handTypes;
        this.ensure = ensure;
        this.mustPlace = mustPlace;
        this.mustMove = mustMove;
        this.maxSolutions = maxSolutions;
        this.minDepth = minDepth;
        this.minMoved = minMoved;
        this.clutterCheck = true;
    }

    private LevelRules(LevelRules r, boolean clutterCheck) {
        this.pieces = r.pieces;
        this.fixedMin = r.fixedMin;
        this.fixedMax = r.fixedMax;
        this.wallsMin = r.wallsMin;
        this.wallsMax = r.wallsMax;
        this.types = r.types;
        this.handTypes = r.handTypes;
        this.ensure = r.ensure;
        this.mustPlace = r.mustPlace;
        this.mustMove = r.mustMove;
        this.maxSolutions = r.maxSolutions;
        this.minDepth = r.minDepth;
        this.minMoved = r.minMoved;
        this.clutterCheck = clutterCheck;
    }

    /**
     * The same rules for a hand-made teaching level, whose pieces are there to show something rather than to close
     * off other solutions (951: the trapdoors carry the mouse past a mousetrap, so the trap never changes the puzzle).
     */
    public LevelRules teaching() {
        return new LevelRules(this, false);
    }

    private static LevelRules of(int pieces, int fMin, int fMax, int wMin, int wMax, List<Animal> types,
                                 int maxSol, int minDepth) {
        return new LevelRules(pieces, fMin, fMax, wMin, wMax, types, types, Collections.<Animal>emptyList(),
                null, null, maxSol, minDepth);
    }

    /** Rules for level number n (1-based). Levels 1-3 are hand-made tutorials and have no rules here. */
    public static LevelRules forLevel(int n) {
        if (n <= 3) {
            throw new IllegalArgumentException("Levels 1-3 are hand-made tutorials");
        }
        if (n == Recipe.TRAPDOOR_INTRO) {   // hand-made: one cat, and the trapdoors take the mouse under a mousetrap
            return forBuilt(1, 0, 0).teaching();
        }
        Recipe recipe = Recipe.forLevel(n);
        if (recipe != null) {
            return recipe.rules(); // a designed level (see ChainBuilder)
        }
        if (n <= 12) {
            return of(1, 2, 3, 0, 2, C, 2, 1);
        }
        if (n == 13) { // introduces lions
            return new LevelRules(1, 3, 4, 0, 2, CL, CL, C, Animal.LION, null, 2, 3);
        }
        if (n <= 22) {
            return of(1, 3, 4, 0, 2, CL, 2, 2);
        }
        if (n == 23) { // first two-animal level
            return of(2, 2, 3, 0, 2, C, 3, 1);
        }
        if (n <= 32) {
            return of(2, 2, 4, 0, 2, CL, 3, 2);
        }
        if (n == 33) { // introduces elephants
            return new LevelRules(1, 4, 5, 0, 2, CLE, CLE, CL, Animal.ELEPHANT, null, 2, 2);
        }
        if (n == 34) { // elephants fear mice (this one is hand-designed; the rules still check it)
            return new LevelRules(1, 2, 5, 0, 3, CLE, CLE, Arrays.asList(Animal.ELEPHANT), null, Animal.ELEPHANT, 2, 1);
        }
        if (n <= 42) {
            return of(1, 3, 5, 0, 2, CLE, 2, 2);
        }
        if (n <= 50) {
            return new LevelRules(2, 2, 4, 0, 2, CLE, CL, Collections.<Animal>emptyList(), null, null, 3, 2);
        }
        if (n <= 60) { // second batch: any animal can be in your hand, exactly one solution, longer chains
            return new LevelRules(2, 3, 5, 0, 3, CLE, CLE, Collections.<Animal>emptyList(), null, null, 1, 2);
        }
        throw new IllegalArgumentException("No rules for level " + n + " yet: add them here first");
    }
}
