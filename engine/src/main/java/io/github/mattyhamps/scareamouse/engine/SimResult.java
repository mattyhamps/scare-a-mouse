package io.github.mattyhamps.scareamouse.engine;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Outcome of one run. Frames are recorded only when asked for (the game needs them to animate). */
public final class SimResult {
    /** One animal's state in one frame. */
    public static final class Snapshot {
        public final int id;
        public final Animal type;
        public final int x;
        public final int y;
        public final boolean gone;

        Snapshot(int id, Animal type, int x, int y, boolean gone) {
            this.id = id;
            this.type = type;
            this.x = x;
            this.y = y;
            this.gone = gone;
        }
    }

    /** The mouse escaped through the hole. */
    public final boolean win;
    /** The run was stopped because the board repeated an earlier state. */
    public final boolean loop;
    /** The mouse ran onto a set mousetrap (the run fails). */
    public final boolean caught;
    /** How many different animals moved at least once. */
    public final int moved;
    /** Steps taken until the mouse escaped (0 if it didn't). */
    public final int ticks;
    /** Frame 0 is the starting board; one more frame per step. Null unless recorded. */
    public final List<List<Snapshot>> frames;
    /**
     * For each frame, the animals that couldn't move that step because another animal was heading for
     * the same square (a standoff, rule 4). Lined up with {@link #frames}. Null unless recorded.
     */
    public final List<List<Integer>> bumps;
    /**
     * For each frame, the mousetraps (indexes into the level's traps) sprung that step. Lined up with
     * {@link #frames}. Null unless recorded.
     */
    public final List<List<Integer>> snaps;
    /**
     * For each frame, the animals that dropped through a trapdoor that step (they come out of the other one).
     * Lined up with {@link #frames}. Null unless recorded.
     */
    public final List<List<Integer>> drops;

    SimResult(boolean win, boolean loop, boolean caught, int moved, int ticks, List<List<Snapshot>> frames,
              List<List<Integer>> bumps, List<List<Integer>> snaps, List<List<Integer>> drops) {
        this.drops = drops;
        this.win = win;
        this.loop = loop;
        this.caught = caught;
        this.snaps = snaps;
        this.moved = moved;
        this.ticks = ticks;
        this.frames = frames;
        this.bumps = bumps;
    }

    public List<Snapshot> lastFrame() {
        return frames == null ? null : frames.get(frames.size() - 1);
    }

    /** JSON for the browser: {win, loop, caught, moved, ticks, frames:[[{id,t,x,y,gone}...]...], bumps:[[ids]...], snaps:[[traps]...], drops:[[ids]...]}. */
    public String toJson() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("win", win);
        m.put("loop", loop);
        m.put("caught", caught);
        m.put("moved", moved);
        m.put("ticks", ticks);
        List<Object> fs = new ArrayList<>();
        if (frames != null) {
            for (List<Snapshot> frame : frames) {
                List<Object> f = new ArrayList<>();
                for (Snapshot s : frame) {
                    Map<String, Object> a = new LinkedHashMap<>();
                    a.put("id", s.id);
                    a.put("t", s.type.id());
                    a.put("x", s.x);
                    a.put("y", s.y);
                    a.put("gone", s.gone);
                    f.add(a);
                }
                fs.add(f);
            }
        }
        m.put("frames", fs);
        List<Object> bs = new ArrayList<>();
        if (bumps != null) {
            for (List<Integer> b : bumps) {
                bs.add(new ArrayList<Object>(b));
            }
        }
        m.put("bumps", bs);
        List<Object> ss = new ArrayList<>();
        if (snaps != null) {
            for (List<Integer> k : snaps) {
                ss.add(new ArrayList<Object>(k));
            }
        }
        m.put("snaps", ss);
        List<Object> ds = new ArrayList<>();
        if (drops != null) {
            for (List<Integer> d : drops) {
                ds.add(new ArrayList<Object>(d));
            }
        }
        m.put("drops", ds);
        return Json.write(m);
    }
}
