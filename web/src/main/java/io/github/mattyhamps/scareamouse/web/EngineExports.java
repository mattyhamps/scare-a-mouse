package io.github.mattyhamps.scareamouse.web;

import io.github.mattyhamps.scareamouse.engine.Json;
import io.github.mattyhamps.scareamouse.engine.Level;
import io.github.mattyhamps.scareamouse.engine.Piece;
import io.github.mattyhamps.scareamouse.engine.Simulator;
import org.teavm.jso.JSExport;

/**
 * What the game page can call. TeaVM compiles this (and the engine) to js/engine.js, where
 * {@code scareSimulate} becomes a plain JavaScript function.
 * Strings go in and out as JSON, so the page and the engine only share the levels.json format.
 */
public final class EngineExports {
    private EngineExports() {
    }

    /**
     * Runs one level.
     *
     * @param levelJson  a level in levels.json format
     * @param placedJson the player's animals: [{"t":"cat","x":4,"y":3}, ...]
     * @return {"win":..,"loop":..,"moved":..,"ticks":..,"frames":[[{"id","t","x","y","gone"}, ...], ...]}
     */
    @JSExport
    public static String scareSimulate(String levelJson, String placedJson) {
        Level level = Level.fromJson(Json.parse(levelJson));
        return Simulator.record(level, Piece.listFromJson(Json.parse(placedJson))).toJson();
    }
}
