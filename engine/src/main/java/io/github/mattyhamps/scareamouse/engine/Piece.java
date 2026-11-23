package io.github.mattyhamps.scareamouse.engine;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** An animal standing on a square. Immutable. */
public final class Piece {
    public final Animal type;
    public final int x;
    public final int y;

    public Piece(Animal type, int x, int y) {
        this.type = type;
        this.x = x;
        this.y = y;
    }

    static Piece fromJson(Object json) {
        Map<?, ?> m = (Map<?, ?>) json;
        return new Piece(Animal.fromId((String) m.get("t")), Json.toInt(m.get("x")), Json.toInt(m.get("y")));
    }

    public static List<Piece> listFromJson(Object json) {
        List<Piece> out = new ArrayList<>();
        if (json != null) {
            for (Object o : (List<?>) json) {
                out.add(fromJson(o));
            }
        }
        return out;
    }

    Map<String, Object> toJson() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("t", type.id());
        m.put("x", x);
        m.put("y", y);
        return m;
    }

    public static List<Object> listToJson(List<Piece> pieces) {
        List<Object> out = new ArrayList<>();
        for (Piece p : pieces) {
            out.add(p.toJson());
        }
        return out;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Piece)) {
            return false;
        }
        Piece p = (Piece) o;
        return p.type == type && p.x == x && p.y == y;
    }

    @Override
    public int hashCode() {
        return (type.ordinal() * 31 + x) * 31 + y;
    }

    @Override
    public String toString() {
        return type.id() + "(" + x + "," + y + ")";
    }
}
