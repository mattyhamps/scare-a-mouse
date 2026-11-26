package io.github.mattyhamps.scareamouse.engine;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * A puzzle layout: board size, the hole (on the border ring, just outside the board),
 * walls, the animals already on the board, the animals the player gets to place,
 * and the intended solution. Immutable.
 */
public final class Level {
    public final String name;
    public final String tip;
    public final int w;
    public final int h;
    public final int holeX;
    public final int holeY;
    /** Wall squares as {x, y}. */
    public final List<int[]> walls;
    /** Animals already on the board. By convention the mouse is first. */
    public final List<Piece> fixed;
    /** Animals the player places. */
    public final List<Animal> inventory;
    /** The intended solution (where the inventory animals go). */
    public final List<Piece> solution;
    /**
     * Turn tiles as {x, y, dir} (dir: 0 up, 1 right, 2 down, 3 left). An animal that runs onto one
     * heads the way its arrow points. Nothing can be placed on them.
     */
    public final List<int[]> turns;
    /**
     * Mousetraps as {x, y}. The mouse is caught if it runs onto a set trap (the run fails); any other
     * animal that runs onto one springs it and keeps going, and then it's harmless. Nothing can be
     * placed on them.
     */
    public final List<int[]> traps;

    public Level(String name, String tip, int w, int h, int holeX, int holeY,
                 List<int[]> walls, List<Piece> fixed, List<Animal> inventory, List<Piece> solution) {
        this(name, tip, w, h, holeX, holeY, walls, fixed, inventory, solution, Collections.<int[]>emptyList());
    }

    public Level(String name, String tip, int w, int h, int holeX, int holeY,
                 List<int[]> walls, List<Piece> fixed, List<Animal> inventory, List<Piece> solution, List<int[]> turns) {
        this(name, tip, w, h, holeX, holeY, walls, fixed, inventory, solution, turns, Collections.<int[]>emptyList());
    }

    public Level(String name, String tip, int w, int h, int holeX, int holeY, List<int[]> walls, List<Piece> fixed,
                 List<Animal> inventory, List<Piece> solution, List<int[]> turns, List<int[]> traps) {
        this.name = name;
        this.tip = tip;
        this.w = w;
        this.h = h;
        this.holeX = holeX;
        this.holeY = holeY;
        this.walls = Collections.unmodifiableList(new ArrayList<>(walls));
        this.fixed = Collections.unmodifiableList(new ArrayList<>(fixed));
        this.inventory = Collections.unmodifiableList(new ArrayList<>(inventory));
        this.solution = Collections.unmodifiableList(new ArrayList<>(solution));
        this.turns = Collections.unmodifiableList(new ArrayList<>(turns));
        this.traps = Collections.unmodifiableList(new ArrayList<>(traps));
    }

    /** True if (x, y) holds a mousetrap. */
    public boolean isTrap(int x, int y) {
        for (int[] t : traps) {
            if (t[0] == x && t[1] == y) {
                return true;
            }
        }
        return false;
    }

    /** The arrow's direction (0 up, 1 right, 2 down, 3 left) if (x, y) is a turn tile, otherwise -1. */
    public int turnAt(int x, int y) {
        for (int[] t : turns) {
            if (t[0] == x && t[1] == y) {
                return t[2];
            }
        }
        return -1;
    }

    public boolean isWall(int x, int y) {
        for (int[] p : walls) {
            if (p[0] == x && p[1] == y) {
                return true;
            }
        }
        return false;
    }

    /** True if (x, y) is on the board and holds no wall, no hole, no turn tile, no trap and no fixed animal. */
    public boolean isOpen(int x, int y) {
        if (x < 0 || y < 0 || x >= w || y >= h || isWall(x, y) || (x == holeX && y == holeY) || turnAt(x, y) >= 0 || isTrap(x, y)) {
            return false;
        }
        for (Piece p : fixed) {
            if (p.x == x && p.y == y) {
                return false;
            }
        }
        return true;
    }

    /** All open squares, row by row. */
    public List<int[]> openSquares() {
        List<int[]> out = new ArrayList<>();
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                if (isOpen(x, y)) {
                    out.add(new int[] {x, y});
                }
            }
        }
        return out;
    }

    public Level withoutFixed(int index) {
        List<Piece> f = new ArrayList<>(fixed);
        f.remove(index);
        return new Level(name, tip, w, h, holeX, holeY, walls, f, inventory, solution, turns, traps);
    }

    public Level withoutWall(int index) {
        List<int[]> ws = new ArrayList<>(walls);
        ws.remove(index);
        return new Level(name, tip, w, h, holeX, holeY, ws, fixed, inventory, solution, turns, traps);
    }

    public Level withoutTurn(int index) {
        List<int[]> ts = new ArrayList<>(turns);
        ts.remove(index);
        return new Level(name, tip, w, h, holeX, holeY, walls, fixed, inventory, solution, ts, traps);
    }

    public Level withTurns(List<int[]> newTurns) {
        return new Level(name, tip, w, h, holeX, holeY, walls, fixed, inventory, solution, newTurns, traps);
    }

    public Level withTraps(List<int[]> newTraps) {
        return new Level(name, tip, w, h, holeX, holeY, walls, fixed, inventory, solution, turns, newTraps);
    }

    public Level withoutTrap(int index) {
        List<int[]> ts = new ArrayList<>(traps);
        ts.remove(index);
        return withTraps(ts);
    }

    public Level withNameAndTip(String newName, String newTip) {
        return new Level(newName, newTip, w, h, holeX, holeY, walls, fixed, inventory, solution, turns, traps);
    }

    public Level withSolution(List<Piece> newSolution) {
        return new Level(name, tip, w, h, holeX, holeY, walls, fixed, inventory, newSolution, turns, traps);
    }

    // ---- JSON (same shape the game page reads) ----

    public static Level fromJson(Object json) {
        Map<?, ?> m = (Map<?, ?>) json;
        List<?> hole = (List<?>) m.get("hole");
        List<int[]> walls = new ArrayList<>();
        Object wallsJson = m.get("walls");
        if (wallsJson != null) {
            for (Object o : (List<?>) wallsJson) {
                List<?> p = (List<?>) o;
                walls.add(new int[] {Json.toInt(p.get(0)), Json.toInt(p.get(1))});
            }
        }
        List<Animal> inv = new ArrayList<>();
        Object invJson = m.get("inv");
        if (invJson != null) {
            for (Object o : (List<?>) invJson) {
                inv.add(Animal.fromId((String) o));
            }
        }
        List<int[]> turns = new ArrayList<>();
        Object turnsJson = m.get("turns");
        if (turnsJson != null) {
            for (Object o : (List<?>) turnsJson) {
                List<?> p = (List<?>) o;
                turns.add(new int[] {Json.toInt(p.get(0)), Json.toInt(p.get(1)), Json.toInt(p.get(2))});
            }
        }
        List<int[]> traps = new ArrayList<>();
        Object trapsJson = m.get("traps");
        if (trapsJson != null) {
            for (Object o : (List<?>) trapsJson) {
                List<?> p = (List<?>) o;
                traps.add(new int[] {Json.toInt(p.get(0)), Json.toInt(p.get(1))});
            }
        }
        return new Level(
                (String) m.get("name"), (String) m.get("tip"),
                Json.toInt(m.get("w")), Json.toInt(m.get("h")),
                Json.toInt(hole.get(0)), Json.toInt(hole.get(1)),
                walls, Piece.listFromJson(m.get("fixed")), inv, Piece.listFromJson(m.get("solution")), turns, traps);
    }

    public Map<String, Object> toJson() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("name", name);
        m.put("tip", tip == null ? "" : tip);
        m.put("w", w);
        m.put("h", h);
        m.put("hole", new int[] {holeX, holeY});
        List<Object> ws = new ArrayList<>();
        for (int[] p : walls) {
            ws.add(new int[] {p[0], p[1]});
        }
        m.put("walls", ws);
        m.put("fixed", Piece.listToJson(fixed));
        List<Object> inv = new ArrayList<>();
        for (Animal a : inventory) {
            inv.add(a.id());
        }
        m.put("inv", inv);
        m.put("solution", Piece.listToJson(solution));
        if (!turns.isEmpty()) {   // only levels with turn tiles have the key, so older levels stay as they were
            List<Object> ts = new ArrayList<>();
            for (int[] t : turns) {
                ts.add(new int[] {t[0], t[1], t[2]});
            }
            m.put("turns", ts);
        }
        if (!traps.isEmpty()) {   // the same for mousetraps
            List<Object> ts = new ArrayList<>();
            for (int[] t : traps) {
                ts.add(new int[] {t[0], t[1]});
            }
            m.put("traps", ts);
        }
        return m;
    }

    public static List<Level> listFromJson(String text) {
        List<Level> out = new ArrayList<>();
        for (Object o : (List<?>) Json.parse(text)) {
            out.add(fromJson(o));
        }
        return out;
    }

    /** One level per line, so diffs of levels.json stay readable. */
    public static String listToJson(List<Level> levels) {
        StringBuilder b = new StringBuilder("[\n");
        for (int k = 0; k < levels.size(); k++) {
            b.append(Json.write(levels.get(k).toJson()));
            b.append(k + 1 < levels.size() ? ",\n" : "\n");
        }
        return b.append("]\n").toString();
    }
}
