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
    /**
     * Animals that can be blockers. A cat is cleared by a dog (started by a bear), a dog by a bear (started by
     * a lion), a bear by a lion (started by an elephant). All three by default, so your hand gets a mix.
     */
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
    /** One animal you place per move. */
    public final Move[] moves;
    /** The chain's starter is on the board, so it moves when you press Go (set by withMoves, not withCatches). */
    public final boolean starterOnBoard;
    /** How many walls the level must have (0 and 0 for none). Each wall has to matter to the puzzle. */
    public final int wallsMin;
    public final int wallsMax;
    /** Turn tiles the chain must use: each bends a runner onto the stretch where the next link waits. */
    public final int turnTiles;

    public Recipe(Animal trigger, int laneBlockers, boolean wrapAround, String tip, Trick... tricks) {
        this(7, new Move[0], false, 0, 0, trigger, laneBlockers, wrapAround, tip,
                new Animal[] {Animal.CAT, Animal.DOG, Animal.BEAR}, 0, tricks);
    }

    private Recipe(int size, Move[] moves, boolean starterOnBoard, int wallsMin, int wallsMax, Animal trigger,
                   int laneBlockers, boolean wrapAround, String tip, Animal[] blockers, int turnTiles, Trick... tricks) {
        this.size = size;
        this.turnTiles = turnTiles;
        this.moves = moves;
        this.starterOnBoard = starterOnBoard;
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
        return (starterOnBoard ? 0 : 1) + moves.length + laneBlockers;
    }

    /**
     * The same recipe with walls: some stop a runner before it reaches a spoiler, the rest close off
     * squares that would give a second, easier solution.
     */
    public Recipe withWalls(int min, int max) {
        return new Recipe(size, moves, starterOnBoard, min, max, trigger, laneBlockers, wrapAround, tip, blockers, turnTiles, tricks);
    }

    /** Everything that shapes the puzzle (not the tip), so two levels made the same way have the same key. */
    public String key() {
        return size + " " + trigger + " " + laneBlockers + " " + wrapAround + " " + java.util.Arrays.toString(tricks)
                + " " + java.util.Arrays.toString(moves) + (starterOnBoard ? " moving" : "") + " "
                + java.util.Arrays.toString(blockers)
                + " " + wallsMin + "-" + wallsMax + (turnTiles > 0 ? " turns " + turnTiles : "");
    }

    /** True if the board starts moving on its own when you press Go. */
    public boolean moving() {
        return starterOnBoard;
    }

    /**
     * The same recipe with chain links missing from the board: you start the chain as usual, and also put
     * these animals back where the chain needs them. This is how cats and dogs end up in your hand.
     */
    public Recipe withCatches(int count) {
        Move[] more = java.util.Arrays.copyOf(moves, moves.length + count);
        java.util.Arrays.fill(more, moves.length, more.length, Move.CATCH);
        return new Recipe(size, more, starterOnBoard, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip,
                blockers, turnTiles, tricks);
    }

    /** The same recipe as an already-moving level: the starter is on the board, and you make these moves. */
    public Recipe withMoves(Move... newMoves) {
        return new Recipe(size, newMoves, true, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip, blockers, turnTiles, tricks);
    }

    /** The same recipe with turn tiles that the chain has to use. */
    public Recipe withTurnTiles(int count) {
        return new Recipe(size, moves, starterOnBoard, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip, blockers, count, tricks);
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
        return new Recipe(size, moves, starterOnBoard, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip, types, turnTiles, tricks);
    }

    /**
     * The last level of each castle area (the Outside and each floor): a "boss" puzzle, marked with a
     * crown on the map. 25, 70, 170 and 260 were bosses when every room had one; they keep their
     * tougher recipes.
     */
    public static final int[] BOSSES = {100, 200, 350, 500, 600, 750, 850, 980, 1000};
    // Third floor (501+): introduce something new to learn there, such as a new board piece (planned).

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
        return new Recipe(newSize, moves, starterOnBoard, wallsMin, wallsMax, trigger, laneBlockers, wrapAround, tip, blockers, turnTiles, tricks);
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
            // Boss levels: the last level of each castle area is the hardest there (see BOSSES).
            case 25: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1); // tougher (no elephants yet: they arrive at level 33)
            case 61: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 62: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 63: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 64: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withCatches(1);
            case 65: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 66: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 67: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 68: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 69: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 70: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1); // tougher
            // 71-80: same difficulty as 61-70, new combinations
            case 71: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 72: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withCatches(1);
            case 73: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 74: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 75: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 76: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 77: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withCatches(1);
            case 78: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 79: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE);
            case 80: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            // 81-90: same difficulty, more variety in your hand (mostly dog blockers, cleared by lions)
            case 81: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 82: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 83: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 84: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withCatches(1);
            case 85: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 86: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 87: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withCatches(1);
            case 88: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 89: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 90: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            // 91-100: same difficulty and hand variety as 81-90; 100 gets the richest recipe
            case 91: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 92: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 93: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 94: return new Recipe(Animal.CAT, 0, true, "", Trick.PLAIN);
            case 95: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 96: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 97: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 98: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN);
            case 99: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withCatches(1);
            case 100: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withCatches(1); // boss
            // 101-110: the first 8x8 boards, in the cellars (Storeroom). Same difficulty as 91-100; about half start
            // moving on their own when you press Go, and your animals swerve, catch or stop the runners.
            case 101: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 102: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 103: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 104: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 105: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 106: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withCatches(1);
            case 107: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 108: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 109: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 110: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            // 111-170: the rest of the Storeroom, the Wine cellar and the Dungeon (8x8). Same difficulty as 101-110, about half already moving.
            case 111: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 112: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 113: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 114: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH);
            case 115: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 116: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 117: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 118: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 119: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 120: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 121: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withCatches(1);
            case 122: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 123: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 124: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 125: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 126: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 127: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 128: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 129: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 130: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH);
            case 131: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 132: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 133: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 134: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 135: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 136: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 137: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 138: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withCatches(1);
            case 139: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 140: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 141: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 142: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 143: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 144: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 145: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 146: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 147: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 148: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 149: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 150: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH);
            case 151: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 152: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 153: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 154: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 155: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 156: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 157: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 158: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 159: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 160: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 161: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 162: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 163: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 164: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 165: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 166: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH);
            case 167: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 168: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 169: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 170: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH); // tougher
            // 171-200: the Kitchens (8x8). Same difficulty as 101-170, about half already moving, and
            // 2-4 walls in every level (drawn as kitchen counters). Walls do the stopping here, so no STOP moves.
            // Most are already moving: with walls, a missing link is what puts cats and dogs in your hand.
            case 171: return new Recipe(Animal.ELEPHANT, 1, false, "New: kitchen counters! Animals can't run through them, so watch out for the counters.", Trick.WAITING_RUNNER).withWalls(2, 4);
            case 172: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 173: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 174: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH).withWalls(2, 4);
            case 175: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(2, 4);
            case 176: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH).withWalls(2, 4);
            case 177: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE).withWalls(2, 4);
            case 178: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withWalls(2, 4);
            case 179: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(2, 4);
            case 180: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 181: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withWalls(2, 4);
            case 182: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(2, 4);
            case 183: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 184: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 185: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 186: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(2, 4);
            case 187: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(2, 4);
            case 188: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(2, 4);
            case 189: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 190: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(2, 4);
            case 191: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH).withWalls(2, 4);
            case 192: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withWalls(2, 4);
            case 193: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(2, 4);
            case 194: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(2, 4);
            case 195: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH).withWalls(2, 4);
            case 196: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(2, 4);
            case 197: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withWalls(2, 4);
            case 198: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(2, 4);
            case 199: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 200: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4); // boss
            // 201-260: the Library, the first 9x9 boards. A smidge harder than the Kitchens (more levels with
            // 3 animals in your hand), about half already moving, and about 1 in 5 levels with 1-3 bookshelves.
            case 201: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 202: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 203: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 204: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 205: return new Recipe(Animal.ELEPHANT, 1, false, "New: bookshelves! Like the counters, animals can't run through them.", Trick.WAITING_RUNNER).withWalls(1, 3);
            case 206: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 207: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 208: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 209: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 210: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 211: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 212: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 213: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 214: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 215: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 216: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 217: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 218: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH);
            case 219: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 220: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withCatches(1);
            case 221: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 222: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 223: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 224: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 225: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 226: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 227: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 228: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 229: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 230: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(1, 3);
            case 231: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 232: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 233: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 234: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 235: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 236: return new Recipe(Animal.BEAR, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 237: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH).withWalls(1, 3);
            case 238: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 239: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 240: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 241: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 242: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 243: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 244: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 245: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 246: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 247: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 248: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 249: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(1, 3);
            case 250: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 251: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 252: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 253: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 254: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 255: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH).withWalls(1, 3);
            case 256: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 257: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 258: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 259: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 260: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH); // tougher
            // 261-290: the Great hall (9x9). About as hard as the Study; about half already moving, and about
            // 1 in 5 levels with walls (drawn as banquet tables).
            case 261: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 262: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 263: return new Recipe(Animal.ELEPHANT, 1, false, "New: banquet tables! Animals can't run through them.", Trick.WAITING_RUNNER).withWalls(1, 3);
            case 264: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 265: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 266: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 267: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH);
            case 268: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 269: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 270: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 271: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 272: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 273: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 274: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(1, 3);
            case 275: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withCatches(1);
            case 276: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 277: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 278: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 279: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 280: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 281: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withCatches(1);
            case 282: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 283: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withCatches(1);
            case 284: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 285: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 286: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE);
            case 287: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 288: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH);
            case 289: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.CATCH).withWalls(1, 3);
            case 290: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH); // tougher
            // 291-320: the Ballroom. A bit harder: more levels steered with two animals, more blockers in the
            // mouse's way (cats and dogs, so the animals you place stay varied). About half already moving;
            // about 1 in 5 with walls (marble pillars). Hands vary from 1 to 3 animals.
            case 291: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 292: return new Recipe(Animal.CAT, 2, true, "", Trick.PLAIN); // starts with a cat: the chain wraps round through the elephant
            case 293: return new Recipe(Animal.LION, 1, false, "New: marble pillars! Animals can't run through them.", Trick.PLAIN).withWalls(1, 3);
            case 294: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 295: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withCatches(1);
            case 296: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 297: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 298: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 299: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE).withCatches(1); // starts with a cat: the chain wraps round through the elephant
            case 300: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.STOP);
            case 301: return new Recipe(Animal.LION, 2, false, "", Trick.PLAIN).withBlockers(Animal.CAT, Animal.DOG);
            case 302: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.STOP);
            case 303: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.CATCH);
            case 304: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(1, 3);
            case 305: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withCatches(1); // starts with a cat: the chain wraps round through the elephant
            case 306: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.STOP);
            case 307: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE);
            case 308: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 309: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 310: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 311: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withCatches(1);
            case 312: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP);
            case 313: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.CATCH);
            case 314: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE); // starts with a cat: the chain wraps round through the elephant
            case 315: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(1, 3);
            case 316: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.STOP);
            case 317: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 318: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE);
            case 319: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 320: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH); // tougher
            // 321-350: the Gallery. Harder again: more blockers and two-animal moves. Still boards start with an
            // elephant or a lion (the only starts the builder manages on 9x9), and more levels are steered
            // with a catch or a stop, which is how cats and dogs get into your hand. About 1 in 5
            // with walls (statues). 350 is the First floor's boss.
            case 321: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 322: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 323: return new Recipe(Animal.LION, 2, false, "New: statues! Animals can't run through them.", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 324: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.CATCH);
            case 325: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE);
            case 326: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 327: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 328: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP).withWalls(1, 3);
            case 329: return new Recipe(Animal.CAT, 2, true, "", Trick.PLAIN); // starts with a cat: the chain wraps round through the elephant
            case 330: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 331: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.CATCH);
            case 332: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE);
            case 333: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.STOP);
            case 334: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 335: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 336: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 337: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 338: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withCatches(1); // starts with a cat: the chain wraps round through the elephant
            case 339: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE, Move.CATCH).withWalls(1, 3);
            case 340: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 341: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE);
            case 342: return new Recipe(Animal.LION, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 343: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 344: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 345: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withWalls(1, 3); // starts with a cat: the chain wraps round through the elephant
            case 346: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.CATCH);
            case 347: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN);
            case 348: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withBlockers(Animal.CAT, Animal.DOG).withMoves(Move.SWERVE, Move.CATCH);
            case 349: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE); // starts with a cat: the chain wraps round through the elephant
            case 350: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4); // boss
            // 351-390: the Chapel, the first 10x10 boards. Eases in (about like the Great hall), about half already
            // moving, about 1 in 5 with walls (pews). Starts mix elephants, lions and cats (wrap-around chains).
            case 351: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 352: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 353: return new Recipe(Animal.ELEPHANT, 0, false, "New: chapel pews! Animals can't run through them.", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 354: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 355: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 356: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 357: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(1, 3);
            case 358: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 359: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 360: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 361: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 362: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 363: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 364: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH);
            case 365: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 366: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 367: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 368: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 369: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 370: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 371: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 372: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 373: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 374: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP).withWalls(1, 3);
            case 375: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 376: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 377: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 378: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 379: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 380: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 381: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 382: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 383: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 384: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 385: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 386: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withWalls(1, 3);
            case 387: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 388: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 389: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 390: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            // 391-420: the Secret passage, a twisty tunnel: most levels have walls (rock). About as hard as the Chapel.
            case 391: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 392: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP).withWalls(1, 3);
            case 393: return new Recipe(Animal.LION, 2, false, "New: rock walls! Animals can't run through them.", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 394: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 395: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 396: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withWalls(2, 4);
            case 397: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(1, 3);
            case 398: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withWalls(2, 4);
            case 399: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 400: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 401: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 402: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withWalls(1, 3);
            case 403: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP).withWalls(1, 3);
            case 404: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 405: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(1, 3);
            case 406: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withWalls(1, 3);
            case 407: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 408: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 409: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(2, 4);
            case 410: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 411: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withMoves(Move.SWERVE).withWalls(2, 4);
            case 412: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 413: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 414: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH).withWalls(2, 4);
            case 415: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 416: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(1, 3);
            case 417: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 418: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP).withWalls(1, 3);
            case 419: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 420: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withWalls(1, 3);
            // 421-460: the Map room. A bit harder: more two-animal moves and blockers. About 1 in 5 with walls (map tables).
            case 421: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 422: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 423: return new Recipe(Animal.ELEPHANT, 1, false, "New: map tables! Animals can't run through them.", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(1, 3);
            case 424: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 425: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 426: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 427: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 428: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 429: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP).withWalls(1, 3);
            case 430: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 431: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 432: return new Recipe(Animal.LION, 0, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 433: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 434: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 435: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 436: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 437: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 438: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 439: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 440: return new Recipe(Animal.LION, 1, false, "", Trick.PLAIN).withWalls(1, 3);
            case 441: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 442: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 443: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 444: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 445: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 446: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 447: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 448: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 449: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 450: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 451: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 452: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 453: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 454: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withWalls(1, 3);
            case 455: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 456: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 457: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 458: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 459: return new Recipe(Animal.CAT, 0, true, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 460: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            // 461-500: the Armory. Harder again, then the Second floor's boss at 500. About 1 in 5 with walls (weapon racks).
            case 461: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 462: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 463: return new Recipe(Animal.LION, 2, false, "New: weapon racks! Animals can't run through them.", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 464: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 465: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 466: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 467: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 468: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 469: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withWalls(2, 4);
            case 470: return new Recipe(Animal.CAT, 2, true, "", Trick.PLAIN);
            case 471: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 472: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 473: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 474: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 475: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.STOP);
            case 476: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 477: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 478: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 479: return new Recipe(Animal.CAT, 1, true, "", Trick.PLAIN).withWalls(1, 3);
            case 480: return new Recipe(Animal.CAT, 1, true, "", Trick.FREEZE_RELEASE);
            case 481: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 482: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 483: return new Recipe(Animal.CAT, 2, true, "", Trick.PLAIN);
            case 484: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 485: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withCatches(1);
            case 486: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 487: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 488: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 489: return new Recipe(Animal.ELEPHANT, 0, false, "", Trick.PLAIN).withMoves(Move.STOP, Move.CATCH);
            case 490: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(1, 3);
            case 491: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 492: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 493: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 494: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 495: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.SWERVE, Move.CATCH);
            case 496: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.WAITING_RUNNER).withMoves(Move.SWERVE, Move.CATCH);
            case 497: return new Recipe(Animal.ELEPHANT, 1, false, "", Trick.FREEZE_RELEASE).withMoves(Move.CATCH).withWalls(1, 3);
            case 498: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withBlockers(Animal.CAT, Animal.DOG);
            case 499: return new Recipe(Animal.LION, 2, false, "", Trick.FREEZE_RELEASE).withWalls(1, 3);
            case 500: return new Recipe(Animal.ELEPHANT, 2, false, "", Trick.PLAIN).withWalls(2, 4); // boss
            default: return null;
        }
    }
}
