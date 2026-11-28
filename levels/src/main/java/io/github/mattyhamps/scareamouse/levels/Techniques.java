package io.github.mattyhamps.scareamouse.levels;

import io.github.mattyhamps.scareamouse.engine.Animal;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.SimResult;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Tags a level's intended solution with the techniques it uses (docs/HARDER_CASTLE.md, step 1). The tags come
 * from playing the solution in the engine and watching what happens, not from the recipe, so they also work for
 * levels made by hand or by older recipes.
 */
public final class Techniques {
    /** The techniques, with the short name used in reports. */
    public enum Tag {
        STOP("stop"),               // your animal stands in a runner's way and halts it for good
        SWERVE("swerve"),           // a runner passes your animal (which it fears) and turns
        CATCH("catch"),             // your animal is scared by a runner passing its square and carries the chain on
        CLEAR_PATH("clear path"),   // your animal holds a runner up for a while, then moves out of its way
        FREEZE("freeze-release"),   // an animal starts frozen between two it fears and bolts later
        WAITING("waiting runner"),  // an animal starts scared but blocked and takes off later
        LANE("lane cleared"),       // an animal standing on the mouse's way is scared off it first
        WRAP("wrap-around"),        // the mouse runs, scares an elephant, and the chain comes back for it
        STANDOFF("standoff"),       // two animals head for the same square, so neither moves
        PIN("freeze on purpose"),   // your animal pins a board animal between two it fears, and it never moves
        TWO_STARTS("two starters"), // two of your animals each start a chain at the first step (every lane-blocker level does)
        BLIND("blind placement"),   // one of your animals goes on a square touching nothing on the board
        MOUSE_TURNS("mouse turns 2+"),   // the mouse changes direction at least twice
        SPRING("trap sprung"),      // another animal springs a mousetrap before the mouse gets there
        STEER("steer round trap"),  // a mousetrap the mouse must be kept away from
        TRAPDOOR("trapdoor"),
        TURN_TILE("turn tile"),
        WALLS("walls"),
        MOVING("moving start");     // the board starts moving on its own when you press Go

        public final String label;

        Tag(String label) {
            this.label = label;
        }
    }

    /** What one level uses. */
    public static final class Tags {
        public final Set<Tag> tags = EnumSet.noneOf(Tag.class);
        public int hand;
        public int depth;
        public int blind;
        public int mouseTurns;
        public double score;

        @Override
        public String toString() {
            StringBuilder s = new StringBuilder();
            for (Tag t : tags) {
                s.append(s.length() == 0 ? "" : ", ").append(t.label);
            }
            return String.format("hand %d, chain %d, score %.1f: %s", hand, depth, score, s.length() == 0 ? "plain" : s);
        }
    }

    private Techniques() {
    }

    public static Tags of(Level level) {
        Tags t = detect(level);
        t.score = Difficulty.score(level, t);
        return t;
    }

    /** The tags without the score (the score counts some of them, see {@link Difficulty#score}). */
    static Tags detect(Level level) {
        Tags t = new Tags();
        t.hand = level.inventory.size();
        t.depth = LevelChecker.depth(level, level.solution);
        Interest.Breakdown b = Interest.breakdown(level);
        if (b.freezeRelease > 0) {
            t.tags.add(Tag.FREEZE);
        }
        if (b.waitingRunner > 0) {
            t.tags.add(Tag.WAITING);
        }
        if (b.wrapAround) {
            t.tags.add(Tag.WRAP);
        }
        if (b.moving) {
            t.tags.add(Tag.MOVING);
        }
        t.blind = Difficulty.blindPlacements(level);
        if (t.blind > 0) {
            t.tags.add(Tag.BLIND);
        }
        if (!level.walls.isEmpty()) {
            t.tags.add(Tag.WALLS);
        }
        if (!level.turns.isEmpty()) {
            t.tags.add(Tag.TURN_TILE);
        }

        SimResult r = Simulator.record(level, level.solution);
        List<List<SimResult.Snapshot>> f = r.frames;
        int fixed = level.fixed.size();
        int n = f.get(0).size();
        int mouse = -1;
        for (int i = 0; i < fixed; i++) {
            if (level.fixed.get(i).type == Animal.MOUSE) {
                mouse = i;
                break;
            }
        }
        for (List<Integer> bump : r.bumps) {
            if (!bump.isEmpty()) {
                t.tags.add(Tag.STANDOFF);
            }
        }
        for (List<Integer> s : r.snaps) {
            if (!s.isEmpty()) {
                t.tags.add(Tag.SPRING);
            }
        }
        for (List<Integer> d : r.drops) {
            if (!d.isEmpty()) {
                t.tags.add(Tag.TRAPDOOR);
            }
        }
        // a trap nothing ever springs is there to keep the mouse (in a wrong solution) away
        int sprung = 0;
        for (List<Integer> s : r.snaps) {
            sprung += s.size();
        }
        if (level.traps.size() > sprung) {
            t.tags.add(Tag.STEER);
        }

        // Each animal's step direction (0,0 when it didn't move) for each step k (from frame k-1 to k).
        int steps = f.size() - 1;
        int[][] dx = new int[n][steps + 1];
        int[][] dy = new int[n][steps + 1];
        for (int k = 1; k <= steps; k++) {
            for (int i = 0; i < n; i++) {
                SimResult.Snapshot a = f.get(k).get(i);
                SimResult.Snapshot p = f.get(k - 1).get(i);
                if (!a.gone && !p.gone && Math.abs(a.x - p.x) + Math.abs(a.y - p.y) == 1) {
                    dx[i][k] = a.x - p.x;
                    dy[i][k] = a.y - p.y;
                }
            }
        }
        // The mouse's turns, and the board animals standing on squares the mouse later runs over.
        if (mouse >= 0) {
            int pdx = 0;
            int pdy = 0;
            for (int k = 1; k <= steps; k++) {
                if (dx[mouse][k] == 0 && dy[mouse][k] == 0) {
                    continue;
                }
                if ((pdx != 0 || pdy != 0) && (dx[mouse][k] != pdx || dy[mouse][k] != pdy)) {
                    t.mouseTurns++;
                }
                pdx = dx[mouse][k];
                pdy = dy[mouse][k];
                SimResult.Snapshot m = f.get(k).get(mouse);
                for (int i = 0; i < fixed; i++) {
                    SimResult.Snapshot o = f.get(0).get(i);
                    if (i != mouse && o.x == m.x && o.y == m.y) {
                        t.tags.add(Tag.LANE);
                    }
                }
            }
            if (t.mouseTurns >= 2) {
                t.tags.add(Tag.MOUSE_TURNS);
            }
        }

        // Freezing on purpose, and two chains started at once.
        int starters = 0;
        for (int p = fixed; p < n; p++) {
            SimResult.Snapshot at = f.get(0).get(p);
            boolean starts = false;
            for (int i = 0; i < fixed; i++) {
                SimResult.Snapshot o = f.get(0).get(i);
                if (o.type.predator() != at.type || Math.abs(o.x - at.x) + Math.abs(o.y - at.y) != 1) {
                    continue;
                }
                boolean ever = false;
                for (int k = 1; k <= steps; k++) {
                    ever |= dx[i][k] != 0 || dy[i][k] != 0;
                }
                starts |= steps >= 1 && (dx[i][1] != 0 || dy[i][1] != 0);
                // frozen at some moment (touched by two or more it fears, one of them yours) and never moves
                int fears = 0;
                for (List<SimResult.Snapshot> frame : f) {
                    int here = 0;
                    for (SimResult.Snapshot q : frame) {
                        here += !q.gone && q.type == o.type.predator() && Math.abs(q.x - o.x) + Math.abs(q.y - o.y) == 1 ? 1 : 0;
                    }
                    fears = Math.max(fears, here);
                }
                if (fears >= 2 && !ever) {
                    t.tags.add(Tag.PIN);
                }
            }
            starters += starts ? 1 : 0;
        }
        if (starters >= 2) {
            t.tags.add(Tag.TWO_STARTS);
        }
        // What each of your animals does.
        for (int p = fixed; p < n; p++) {
            Animal mine = f.get(0).get(p).type;
            int firstMove = -1;
            for (int k = 1; k <= steps && firstMove < 0; k++) {
                if (dx[p][k] != 0 || dy[p][k] != 0) {
                    firstMove = k;
                }
            }
            // CATCH: your animal is a link in the chain (a missing link put back): it runs, but only later, once
            // the chain reaches it (it may start frozen or blocked, too).
            if (firstMove > 1) {
                t.tags.add(Tag.CATCH);
            }
            for (int i = 0; i < n; i++) {
                if (i == p) {
                    continue;
                }
                Animal other = f.get(0).get(i).type;
                for (int k = 2; k <= steps; k++) {
                    boolean wasRunning = dx[i][k - 1] != 0 || dy[i][k - 1] != 0;
                    if (!wasRunning) {
                        continue;
                    }
                    SimResult.Snapshot me = f.get(k - 1).get(p);
                    SimResult.Snapshot it = f.get(k - 1).get(i);
                    boolean moved = dx[i][k] != 0 || dy[i][k] != 0;
                    boolean turned = moved && (dx[i][k] != dx[i][k - 1] || dy[i][k] != dy[i][k - 1]);
                    // SWERVE: a runner that fears my animal turns while beside it
                    if (turned && other.predator() == mine && Math.abs(me.x - it.x) + Math.abs(me.y - it.y) == 1
                            && !(me.x - it.x == dx[i][k - 1] && me.y - it.y == dy[i][k - 1])) {
                        t.tags.add(Tag.SWERVE);
                    }
                    // A runner halts with my animal on the next square of its way: a stop if it never moves on,
                    // otherwise my animal cleared the path later (timing).
                    if (!moved && me.x == it.x + dx[i][k - 1] && me.y == it.y + dy[i][k - 1] && other.predator() != mine) {
                        // its next move, if any: carrying on the same way means my animal got out of its way
                        boolean carriesOn = false;
                        for (int j = k + 1; j <= steps; j++) {
                            if (dx[i][j] != 0 || dy[i][j] != 0) {
                                carriesOn = dx[i][j] == dx[i][k - 1] && dy[i][j] == dy[i][k - 1];
                                break;
                            }
                        }
                        t.tags.add(carriesOn ? Tag.CLEAR_PATH : Tag.STOP);
                    }
                }
            }
        }
        return t;
    }

    /** A room of the castle: its name and its last level (from ROOMS in index.html). */
    public static final class Room {
        public final String name;
        public final int start;
        public final int end;

        Room(String name, int start, int end) {
            this.name = name;
            this.start = start;
            this.end = end;
        }
    }

    /** The rooms, read from index.html's ROOMS list, so the report always matches the game. */
    public static List<Room> rooms(Path indexHtml, int levels) throws IOException {
        String html = new String(Files.readAllBytes(indexHtml), StandardCharsets.UTF_8);
        Matcher m = Pattern.compile("\\{end:(\\d+),\\s*area:\\d+,\\s*name:'([^']+)'").matcher(html);
        List<Room> out = new ArrayList<>();
        int start = 1;
        while (m.find()) {
            int end = Integer.parseInt(m.group(1));
            if (start > levels) {
                break;
            }
            out.add(new Room(m.group(2), start, Math.min(end, levels)));
            start = end + 1;
        }
        return out;
    }

    /**
     * The report: for each room, how many levels use each technique, the average score and hand, and the
     * repeats (the same technique within 3 levels of itself). Markdown, so it can go in a pull request.
     */
    public static String report(List<Level> levels, List<Room> rooms, int fromLevel) {
        List<Tags> all = new ArrayList<>();
        for (Level l : levels) {
            all.add(of(l));
        }
        Tag[] shown = Tag.values();
        StringBuilder s = new StringBuilder();
        s.append("| Room | Levels | Avg score | Avg hand | Max hand |");
        for (Tag t : shown) {
            s.append(' ').append(t.label).append(" |");
        }
        s.append(" Repeats within 3 |\n|---|---|---|---|---|");
        for (int k = 0; k < shown.length; k++) {
            s.append("---|");
        }
        s.append("---|\n");
        for (Room room : rooms) {
            if (room.end < fromLevel) {
                continue;
            }
            int count = room.end - room.start + 1;
            double score = 0;
            int hand = 0;
            int maxHand = 0;
            Map<Tag, Integer> c = new LinkedHashMap<>();
            for (int n = room.start; n <= room.end; n++) {
                Tags t = all.get(n - 1);
                score += t.score;
                hand += t.hand;
                maxHand = Math.max(maxHand, t.hand);
                for (Tag g : t.tags) {
                    c.merge(g, 1, Integer::sum);
                }
            }
            s.append(String.format("| %s (%d-%d) | %d | %.1f | %.1f | %d |", room.name, room.start, room.end, count,
                    score / count, (double) hand / count, maxHand));
            for (Tag g : shown) {
                int v = c.getOrDefault(g, 0);
                s.append(' ').append(v == 0 ? "" : v).append(" |");
            }
            s.append(' ').append(repeats(all, room.start, room.end)).append(" |\n");
        }
        return s.toString();
    }

    /**
     * STOP and CATCH called out per room: how many levels' recipes ask for one (the trick a player learns), and
     * how many solutions use one at all (sometimes along the way, without the recipe asking), with the levels
     * where the recipe asks for a stop.
     */
    public static String stopsAndCatches(List<Level> levels, List<Room> rooms, int fromLevel) {
        StringBuilder s = new StringBuilder("| Room | STOP asked | STOP in play | CATCH asked | CATCH in play | Levels asking for a stop |\n|---|---|---|---|---|---|\n");
        for (Room room : rooms) {
            if (room.end < fromLevel) {
                continue;
            }
            int stopAsked = 0;
            int stopSeen = 0;
            int catchAsked = 0;
            int catchSeen = 0;
            List<String> where = new ArrayList<>();
            for (int n = room.start; n <= room.end; n++) {
                Tags t = of(levels.get(n - 1));
                stopSeen += t.tags.contains(Tag.STOP) ? 1 : 0;
                catchSeen += t.tags.contains(Tag.CATCH) ? 1 : 0;
                Recipe r = Recipe.forLevel(n);
                boolean stop = false;
                boolean caught = false;
                if (r != null) {
                    for (Recipe.Move m : r.moves) {
                        stop |= m == Recipe.Move.STOP;
                        caught |= m == Recipe.Move.CATCH;
                    }
                }
                if (stop) {
                    stopAsked++;
                    where.add(String.valueOf(n));
                }
                catchAsked += caught ? 1 : 0;
            }
            s.append(String.format("| %s | %d | %d | %d | %d | %s |%n", room.name, stopAsked, stopSeen, catchAsked, catchSeen,
                    String.join(", ", where)));
        }
        return s.toString();
    }

    /** The techniques that come back within 3 levels of themselves in a room (not counting walls and moving starts). */
    static String repeats(List<Tags> all, int from, int to) {
        Map<Tag, Integer> c = new LinkedHashMap<>();
        for (int n = from; n <= to; n++) {
            for (Tag g : all.get(n - 1).tags) {
                if (g == Tag.WALLS || g == Tag.MOVING || g == Tag.BLIND) {
                    continue;
                }
                for (int back = 1; back <= 3 && n - back >= from; back++) {
                    if (all.get(n - 1 - back).tags.contains(g)) {
                        c.merge(g, 1, Integer::sum);
                        break;
                    }
                }
            }
        }
        List<String> out = new ArrayList<>();
        for (Map.Entry<Tag, Integer> e : c.entrySet()) {
            out.add(e.getKey().label + " " + e.getValue());
        }
        return out.isEmpty() ? "" : String.join(", ", out);
    }

    /** One line per level (for a CSV file): level, room, hand, chain, score, then the tags. */
    public static String perLevel(List<Level> levels, List<Room> rooms) {
        StringBuilder s = new StringBuilder("level,room,name,hand,chain,score,blind,mouse turns,tags\n");
        for (Room room : rooms) {
            for (int n = room.start; n <= room.end; n++) {
                Level l = levels.get(n - 1);
                Tags t = of(l);
                List<String> names = new ArrayList<>();
                for (Tag g : t.tags) {
                    names.add(g.label);
                }
                s.append(String.format("%d,%s,\"%s\",%d,%d,%.1f,%d,%d,\"%s\"%n", n, room.name, l.name.replace("\"", "'"),
                        t.hand, t.depth, t.score, t.blind, t.mouseTurns, String.join("; ", names)));
            }
        }
        return s.toString();
    }

    // ---- Repeat limits (Matt, 27 November 2026; docs/HARDER_CASTLE_REPORT.md "Limits on repeats") ----

    /** Tricks a player notices and remembers: each in at most about 1 level in 8, never within 3 levels of itself. */
    static final Set<Tag> HEADLINE = EnumSet.of(Tag.STOP, Tag.SWERVE, Tag.WAITING, Tag.WRAP, Tag.STANDOFF, Tag.PIN,
            Tag.CLEAR_PATH, Tag.MOUSE_TURNS, Tag.SPRING);
    /** Everyday building blocks and the most of a room's levels each may use. */
    static final Map<Tag, Double> EVERYDAY = Map.of(Tag.LANE, 0.40, Tag.CATCH, 0.40, Tag.FREEZE, 0.25);
    static final double HEADLINE_SHARE = 1 / 8.0;
    static final int HEADLINE_GAP = 3;
    /** The same puzzle style never comes back within this many levels. */
    static final int STYLE_GAP = 8;
    /** Tags that make up a puzzle's style (with the number of animals you place). */
    private static final Set<Tag> STYLE_TAGS = EnumSet.of(Tag.STOP, Tag.SWERVE, Tag.CATCH, Tag.FREEZE, Tag.WAITING,
            Tag.LANE, Tag.WRAP, Tag.STANDOFF, Tag.PIN, Tag.CLEAR_PATH, Tag.MOUSE_TURNS, Tag.SPRING, Tag.STEER,
            Tag.TRAPDOOR, Tag.TURN_TILE, Tag.MOVING);

    /**
     * Rooms rebuilt for the harder castle. Add each room's name here as it's rebuilt: {@code TechniquesTest} then
     * holds it to the repeat limits. Rooms not rebuilt yet are left alone (most of them break the limits today).
     */
    static final List<String> REBUILT_ROOMS = List.of("Library");

    /** A puzzle's style: how many animals you place and which techniques it uses, for example "3: catch, stop". */
    public static String style(Tags t) {
        List<String> parts = new ArrayList<>();
        for (Tag g : t.tags) {
            if (STYLE_TAGS.contains(g)) {
                parts.add(g.label);
            }
        }
        return t.hand + ": " + String.join(", ", parts);
    }

    /** Where a room breaks the repeat limits (empty if it keeps them). Levels from..to, 1-based. */
    public static List<String> limitProblems(List<Level> levels, int from, int to) {
        List<Tags> tags = new ArrayList<>();
        for (int n = from; n <= to; n++) {
            tags.add(of(levels.get(n - 1)));
        }
        List<String> out = new ArrayList<>();
        int count = tags.size();
        Map<Tag, Integer> uses = new LinkedHashMap<>();
        for (Tags t : tags) {
            for (Tag g : t.tags) {
                uses.merge(g, 1, Integer::sum);
            }
        }
        for (Tag g : HEADLINE) {
            int most = (int) Math.ceil(count * HEADLINE_SHARE);
            if (uses.getOrDefault(g, 0) > most) {
                out.add(g.label + " in " + uses.get(g) + " levels (at most " + most + ")");
            }
        }
        for (Map.Entry<Tag, Double> e : EVERYDAY.entrySet()) {
            int most = (int) Math.floor(count * e.getValue());
            if (uses.getOrDefault(e.getKey(), 0) > most) {
                out.add(e.getKey().label + " in " + uses.get(e.getKey()) + " levels (at most " + most + ")");
            }
        }
        for (int i = 0; i < count; i++) {
            for (int back = 1; back <= Math.max(HEADLINE_GAP, STYLE_GAP) && i - back >= 0; back++) {
                Tags now = tags.get(i);
                Tags then = tags.get(i - back);
                if (back <= HEADLINE_GAP) {
                    for (Tag g : now.tags) {
                        if (HEADLINE.contains(g) && then.tags.contains(g)) {
                            out.add((from + i) + " repeats " + g.label + " from " + (from + i - back));
                        }
                    }
                }
                if (style(now).equals(style(then))) {
                    out.add((from + i) + " repeats the style of " + (from + i - back) + " (" + style(now) + ")");
                }
            }
        }
        return out;
    }

    /** The most levels of a room of this size that may use a technique (no limit for the rest). */
    static int most(Tag g, int roomSize) {
        return HEADLINE.contains(g) ? (int) Math.ceil(roomSize * HEADLINE_SHARE)
                : EVERYDAY.containsKey(g) ? (int) Math.floor(roomSize * EVERYDAY.get(g)) : Integer.MAX_VALUE;
    }

    /**
     * Why a candidate would break the repeat limits, given the levels of its room built before it (in order), or null
     * if it keeps them: a headline trick from the 3 levels before, a style from the 8 before, or one more use of a
     * technique than the room may have. {@code LevelsCli make --strict} only keeps candidates that keep the limits, so
     * a room built in order passes {@link #limitProblems} (as long as its recipes leave room for every technique).
     */
    static String breaks(Tags t, List<Tags> before, int roomSize) {
        int n = before.size();
        for (int back = 1; back <= Math.max(HEADLINE_GAP, STYLE_GAP) && back <= n; back++) {
            Tags then = before.get(n - back);
            if (back <= HEADLINE_GAP) {
                for (Tag g : t.tags) {
                    if (HEADLINE.contains(g) && then.tags.contains(g)) {
                        return g.label + " was " + back + " level(s) back";
                    }
                }
            }
            if (back <= STYLE_GAP && style(then).equals(style(t))) {
                return "style " + style(t) + " was " + back + " level(s) back";
            }
        }
        for (Tag g : t.tags) {
            int most = most(g, roomSize);
            int used = 0;
            for (Tags b : before) {
                used += b.tags.contains(g) ? 1 : 0;
            }
            if (used + 1 > most) {
                return g.label + " would be in " + (used + 1) + " levels of the room (at most " + most + ")";
            }
        }
        return null;
    }

    /**
     * How much a candidate level would repeat the levels just before it, for the builder to mark it down: a lot for
     * the same style within 8 levels or a headline trick within 3, a little for each everyday block the recent
     * levels already use often. 0 if it repeats nothing.
     */
    public static double repeatPenalty(Level candidate, List<Level> before) {
        Tags t = of(candidate);
        double penalty = 0;
        int n = before.size();
        Map<Tag, Integer> recent = new LinkedHashMap<>();
        for (int back = 1; back <= n; back++) {
            Tags then = of(before.get(n - back));
            if (back <= STYLE_GAP && style(then).equals(style(t))) {
                penalty += 100;
            }
            for (Tag g : t.tags) {
                if (back <= HEADLINE_GAP && HEADLINE.contains(g) && then.tags.contains(g)) {
                    penalty += 50;
                }
            }
            for (Tag g : then.tags) {
                recent.merge(g, 1, Integer::sum);
            }
        }
        for (Tag g : t.tags) {
            Double share = EVERYDAY.get(g);
            if (share != null && n > 0 && recent.getOrDefault(g, 0) >= share * n) {
                penalty += 20;
            }
            if (HEADLINE.contains(g) && n > 0 && recent.getOrDefault(g, 0) >= HEADLINE_SHARE * n) {
                penalty += 20;
            }
        }
        return penalty;
    }
}
