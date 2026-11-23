package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;

/**
 * What kind of puzzle a built level should be. The {@link ChainBuilder} designs a chain to match.
 */
public final class Recipe {
    /** A trick the chain should include. */
    public enum Trick {
        /** Nothing special: each link is scared by the one before it as it runs past. */
        PLAIN,
        /** An animal starts frozen between two predators and bolts when the chain pulls one away. */
        FREEZE_RELEASE,
        /** An animal is already scared but blocked; it takes off when the chain moves the blocker. */
        WAITING_RUNNER,
    }

    /** The first animal you place; the chain runs down the food chain from it. */
    public final Animal trigger;
    /**
     * Animals sitting between the mouse and the hole. Each one needs its own little chain to scare it out
     * of the way, started by one more animal in your hand.
     */
    public final int laneBlockers;
    /** Tricks the chain must contain, in addition to plain links. */
    public final Trick[] tricks;
    /** The chain goes all the way round: the mouse runs, scares an elephant, and the chain comes back for it. */
    public final boolean wrapAround;
    /** Shown in the game as the level's tip. */
    public final String tip;

    public Recipe(Animal trigger, int laneBlockers, boolean wrapAround, String tip, Trick... tricks) {
        this.trigger = trigger;
        this.laneBlockers = laneBlockers;
        this.wrapAround = wrapAround;
        this.tip = tip;
        this.tricks = tricks;
    }

    public int handSize() {
        return 1 + laneBlockers;
    }

    /** Checker rules that go with this recipe. */
    public LevelRules rules() {
        if (wrapAround) {
            // The mouse moves early on purpose, so judge the chain by how many animals move instead.
            return LevelRules.forBuilt(handSize(), 0, 6);
        }
        int chain = trigger.ordinal() - 1; // animals between your first animal and the mouse
        return LevelRules.forBuilt(handSize(), Math.min(chain, 3), 0);
    }

    public boolean has(Trick t) {
        for (Trick x : tricks) {
            if (x == t) {
                return true;
            }
        }
        return false;
    }

    /**
     * Recipes for built levels. Puzzle types are deliberately mixed through each batch,
     * with difficulty rising slowly. Returns null for levels that aren't built this way.
     */
    public static Recipe forLevel(int n) {
        switch (n) {
            case 61: return new Recipe(Animal.LION, 2, false, "Three animals: one chases the mouse, two clear the path.", Trick.PLAIN);
            case 62: return new Recipe(Animal.LION, 0, false, "Two predators freeze an animal. Take one away and it bolts.", Trick.FREEZE_RELEASE);
            case 63: return new Recipe(Animal.BEAR, 1, false, "Something's in the way. Clear the path to the hole.", Trick.PLAIN);
            case 64: return new Recipe(Animal.ELEPHANT, 0, false, "An elephant in your hand: the longest chain yet.", Trick.PLAIN);
            case 65: return new Recipe(Animal.ELEPHANT, 0, false, "Someone's already scared but stuck. Clear the way.", Trick.WAITING_RUNNER);
            case 66: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE);
            case 67: return new Recipe(Animal.CAT, 0, true, "All the way round: the mouse scares the elephant.", Trick.PLAIN);
            case 68: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER);
            case 69: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE);
            case 70: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN);
            default: return null;
        }
    }
}
