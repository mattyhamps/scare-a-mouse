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
    /** Animals that can be blockers. A dog is cleared by a bear (started by a lion), a bear by a lion (started by an elephant). */
    public final Animal[] blockers;
    /** Tricks the chain must contain, in addition to plain links. */
    public final Trick[] tricks;
    /** The chain goes all the way round: the mouse runs, scares an elephant, and the chain comes back for it. */
    public final boolean wrapAround;
    /**
     * Shown in the game as the level's tip. After level 10, tips never describe the solution or the
     * trick: leave it empty, or announce a new animal ("New animal: ..."). LevelsTest enforces this.
     */
    public final String tip;

    public Recipe(Animal trigger, int laneBlockers, boolean wrapAround, String tip, Trick... tricks) {
        this(trigger, laneBlockers, wrapAround, tip, new Animal[] {Animal.DOG, Animal.BEAR}, tricks);
    }

    private Recipe(Animal trigger, int laneBlockers, boolean wrapAround, String tip, Animal[] blockers, Trick... tricks) {
        this.blockers = blockers;
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

    /** The same recipe, with only these blocker animals (for example only dogs, so you place lions not elephants). */
    public Recipe withBlockers(Animal... types) {
        return new Recipe(trigger, laneBlockers, wrapAround, tip, types, tricks);
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
            case 61: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN);
            case 62: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE);
            case 63: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN);
            case 64: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN);
            case 65: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER);
            case 66: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE);
            case 67: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 68: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER);
            case 69: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE);
            case 70: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN);
            // 71-80: same difficulty as 61-70, new combinations
            case 71: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE);
            case 72: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN);
            case 73: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 74: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE);
            case 75: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 76: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE);
            case 77: return new Recipe(Animal.BEAR, 2, false, "", Trick.PLAIN);
            case 78: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER);
            case 79: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE);
            case 80: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            // 81-90: same difficulty, more variety in your hand (mostly dog blockers, cleared by lions)
            case 81: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 82: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE);
            case 83: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 84: return new Recipe(Animal.BEAR, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 85: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER);
            case 86: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 87: return new Recipe(Animal.BEAR, 2, false, "", Trick.PLAIN);
            case 88: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 89: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE);
            case 90: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            // 91-100: same difficulty and hand variety as 81-90; 100 gets the richest recipe
            case 91: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 92: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE);
            case 93: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 94: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 95: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 96: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 97: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE);
            case 98: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN);
            case 99: return new Recipe(Animal.BEAR, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 100: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            default: return null;
        }
    }
}
