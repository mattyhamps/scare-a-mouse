package io.github.mattyhamps.scareamouse.engine;

/**
 * The animals, in food-chain order. Each animal fears only the next one up,
 * and the chain wraps around: elephants fear mice.
 */
public enum Animal {
    MOUSE("mouse", 'M'),
    CAT("cat", 'C'),
    DOG("dog", 'D'),
    BEAR("bear", 'B'),
    LION("lion", 'L'),
    ELEPHANT("elephant", 'E');

    private static final Animal[] ALL = values();

    private final String id;
    private final char letter;

    Animal(String id, char letter) {
        this.id = id;
        this.letter = letter;
    }

    /** The one animal this animal is afraid of. */
    public Animal predator() {
        return ALL[(ordinal() + 1) % ALL.length];
    }

    /** Lower-case name used in levels.json, for example "cat". */
    public String id() {
        return id;
    }

    /** Single letter used in test board pictures, for example 'C'. */
    public char letter() {
        return letter;
    }

    public static Animal fromId(String id) {
        for (Animal a : ALL) {
            if (a.id.equals(id)) {
                return a;
            }
        }
        throw new IllegalArgumentException("Unknown animal: " + id);
    }

    /** Returns the animal for a board-picture letter, or null if the letter isn't an animal. */
    public static Animal fromLetter(char c) {
        for (Animal a : ALL) {
            if (a.letter == c) {
                return a;
            }
        }
        return null;
    }
}
