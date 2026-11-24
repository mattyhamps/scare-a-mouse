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

    /**
     * Already-moving levels: the board starts moving on its own when you press Go, and each of these is
     * one animal you place to steer the chain.
     */
    public enum Move {
        /** Your animal stands beside a runner's path and makes it turn the right way (it fears your animal). */
        SWERVE,
        /** A runner passes the empty spot where your animal goes; it gets scared and carries the chain on. */
        CATCH,
        /** Your animal stands in a runner's path and halts it, before it reaches an animal that would spoil things. */
        STOP,
    }

    /** The first animal in the chain's start; you place it, unless the level is already moving. */
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
     * trick: leave it empty, or announce something new without saying how to use it ("New animal: ..."
     * or "New: ..."). LevelsTest enforces this.
     */
    public final String tip;
    /** Width and height of the board, in squares. */
    public final int size;
    /** Empty for normal levels. Otherwise the starter is on the board and you place one animal per move. */
    public final Move[] moves;
    /** How many walls the level must have (0 and 0 for none). Each wall has to matter to the puzzle. */
    public final int wallsMin;
    public final int wallsMax;

    public Recipe(Animal trigger, int laneBlockers, boolean wrapAround, String tip, Trick... tricks) {
        this(7, new Move[0], 0, 0, trigger, laneBlockers, wrapAround, tip, new Animal[] {Animal.DOG, Animal.BEAR}, tricks);
    }

    private Recipe(int size, Move[] moves, int wallsMin, int wallsMax, Animal trigger, int laneBlockers,
                   boolean wrapAround, String tip, Animal[] blockers, Trick... tricks) {
        this.size = size;
        this.moves = moves;
        this.wallsMin = wallsMin;
        this.wallsMax = wallsMax;
        this.blockers = blockers;
        this.trigger = trigger;
        this.laneBlockers = laneBlockers;
        this.wrapAround = wrapAround;
        this.tip = tip;
        this.tricks = tricks;
    }

    public int handSize() {
        return (moves.length > 0 ? moves.length : 1) + laneBlockers;
    }

    /**
     * The same recipe with walls: some stop a runner before it reaches a spoiler, the rest close off
     * squares that would give a second, easier solution.
     */
    public Recipe withWalls(int min, int max) {
        return new Recipe(size, moves, min, max, trigger, laneBlockers, wrapAround, tip, blockers, tricks);
    }

    /** True if the board starts moving on its own when you press Go. */
    public boolean moving() {
        return moves.length > 0;
    }

    /** The same recipe as an already-moving level: the starter is on the board, and you make these moves. */
    public Recipe withMoves(Move... newMoves) {
        return new Recipe(size, newMoves, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip, blockers, tricks);
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
        return new Recipe(size, moves, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip, types, tricks);
    }

    /**
     * Board size for level n: the boards grow as you go. Levels 1-100 are 7x7, 101-200 are 8x8,
     * 201-350 are 9x9, and from 351 on they are 10x10 (the original game's size). Each size change
     * starts a new room of the castle map.
     */
    public static int sizeForLevel(int n) {
        return n <= 100 ? 7 : n <= 200 ? 8 : n <= 350 ? 9 : 10;
    }

    /** The same recipe on a bigger (or smaller) square board. */
    public Recipe withSize(int newSize) {
        return new Recipe(newSize, moves, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip, blockers, tricks);
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
        Recipe r = designed(n);
        return r == null ? null : r.withSize(sizeForLevel(n));
    }

    private static Recipe designed(int n) {
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
            // 101-110: the first 8x8 boards, in the Great hall. Same difficulty as 91-100; about half start
            // moving on their own when you press Go, and your animals swerve, catch or stop the runners.
            case 101: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 102: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 103: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 104: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 105: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 106: return new Recipe(Animal.BEAR, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 107: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 108: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 109: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 110: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            // 111-170: the rest of the Great hall (8x8). Same difficulty as 101-110, about half already moving.
            case 111: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 112: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 113: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 114: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 115: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 116: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 117: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 118: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 119: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 120: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 121: return new Recipe(Animal.BEAR, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 122: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 123: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 124: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 125: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 126: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 127: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 128: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 129: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 130: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 131: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 132: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 133: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 134: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 135: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 136: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 137: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 138: return new Recipe(Animal.BEAR, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 139: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 140: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 141: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 142: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 143: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 144: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 145: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 146: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 147: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 148: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 149: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 150: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 151: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 152: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 153: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 154: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 155: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 156: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 157: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 158: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 159: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 160: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 161: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 162: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 163: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 164: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 165: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 166: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 167: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 168: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 169: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 170: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            // 171-200: the Kitchens (8x8). Same difficulty as the Great hall, about half already moving, and
            // 2-4 walls in every level (drawn as kitchen counters). Walls do the stopping here, so no STOP moves.
            case 171: return new Recipe(Animal.ELEPHANT, 1, false, "New: kitchen counters! Animals can't run through them, so watch out for the counters.", Trick.WAITING_RUNNER).withBlockers(Animal.DOG).withWalls(2, 4);
            case 172: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 173: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(2, 4);
            case 174: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH).withWalls(2, 4);
            case 175: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH).withWalls(2, 4);
            case 176: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(2, 4);
            case 177: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.SWERVE).withWalls(2, 4);
            case 178: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withWalls(2, 4);
            case 179: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(2, 4);
            case 180: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 181: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(2, 4);
            case 182: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE).withWalls(2, 4);
            case 183: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 184: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG).withWalls(2, 4);
            case 185: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 186: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE).withWalls(2, 4);
            case 187: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(2, 4);
            case 188: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH).withWalls(2, 4);
            case 189: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withWalls(2, 4);
            case 190: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(2, 4);
            case 191: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG).withWalls(2, 4);
            case 192: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withWalls(2, 4);
            case 193: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE).withWalls(2, 4);
            case 194: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(2, 4);
            case 195: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH).withWalls(2, 4);
            case 196: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH).withWalls(2, 4);
            case 197: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withWalls(2, 4);
            case 198: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE).withWalls(2, 4);
            case 199: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 200: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(2, 4);
            // 201-260: the Library, the first 9x9 boards. A smidge harder than the Kitchens (more levels with
            // 3 animals in your hand), about half already moving, and about 1 in 5 levels with 1-3 bookshelves.
            case 201: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 202: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 203: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 204: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 205: return new Recipe(Animal.ELEPHANT, 1, false, "New: bookshelves! Like the counters, animals can't run through them.", Trick.WAITING_RUNNER).withBlockers(Animal.DOG).withWalls(1, 3);
            case 206: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 207: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 208: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 209: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(1, 3);
            case 210: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 211: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 212: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 213: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 214: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withWalls(1, 3);
            case 215: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 216: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 217: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 218: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 219: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 220: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 221: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 222: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 223: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 224: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 225: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 226: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 227: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 228: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.CATCH);
            case 229: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 230: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE).withWalls(1, 3);
            case 231: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 232: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 233: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 234: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 235: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 236: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(1, 3);
            case 237: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH).withWalls(1, 3);
            case 238: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 239: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 240: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 241: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.DOG);
            case 242: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 243: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 244: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 245: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 246: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 247: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 248: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG).withWalls(1, 3);
            case 249: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE).withWalls(1, 3);
            case 250: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 251: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 252: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 253: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            case 254: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.SWERVE);
            case 255: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.CATCH).withWalls(1, 3);
            case 256: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withWalls(1, 3);
            case 257: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 258: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.DOG);
            case 259: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.DOG).withMoves(Move.STOP);
            case 260: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.DOG);
            default: return null;
        }
    }
}
