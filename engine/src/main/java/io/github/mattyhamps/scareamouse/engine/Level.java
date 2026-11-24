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

    public Level(String name, String tip, int w, int h, int holeX, int holeY,
                 List<int[]> walls, List<Piece> fixed, List<Animal> inventory, List<Piece> solution) {
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
    }

    public boolean isWall(int x, int y) {
        for (int[] p : walls) {
            if (p[0] == x && p[1] == y) {
                return true;
            }
        }
        return false;
    }

    /** True if (x, y) is on the board and holds no wall, no hole and no fixed animal. */
    public boolean isOpen(int x, int y) {
        if (x < 0 || y < 0 || x >= w || y >= h || isWall(x, y) || (x == holeX && y == holeY)) {
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
        return new Level(name, tip, w, h, holeX, holeY, walls, f, inventory, solution);
    }

    public Level withoutWall(int index) {
        List<int[]> ws = new ArrayList<>(walls);
        ws.remove(index);
        return new Level(name, tip, w, h, holeX, holeY, ws, fixed, inventory, solution);
    }

    public Level withNameAndTip(String newName, String newTip) {
        return new Level(newName, newTip, w, h, holeX, holeY, walls, fixed, inventory, solution);
    }

    public Level withSolution(List<Piece> newSolution) {
        return new Level(name, tip, w, h, holeX, holeY, walls, fixed, inventory, newSolution);
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
        return new Level(
                (String) m.get("name"), (String) m.get("tip"),
                Json.toInt(m.get("w")), Json.toInt(m.get("h")),
                Json.toInt(hole.get(0)), Json.toInt(hole.get(1)),
                walls, Piece.listFromJson(m.get("fixed")), inv, Piece.listFromJson(m.get("solution")));
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
