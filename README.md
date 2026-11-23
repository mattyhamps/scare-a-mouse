# Scare-a-Mouse 🐭

A chain-reaction puzzle game. Place animals so each one scares the next, and get the mouse
out through the hole.

**Play:** https://mattyhamps.github.io/scare-a-mouse/ (works on iPhone and Android; use
"Add to Home Screen" to keep it like an app).

## Rulebook

The physics live in one place, [`Simulator.java`](engine/src/main/java/io/github/mattyhamps/scareamouse/engine/Simulator.java),
and every part of the project uses that code.

0. **Food chain:** mouse < cat < dog < bear < lion < elephant < mouse. Each animal fears only the
   next one up (and elephants fear mice).
1. **Steps:** every animal moves at most one square per step, all at the same time.
2. **Scared:** if exactly one animal it fears is touching it (side by side, not diagonal), it runs
   straight away from that animal.
3. **Frozen:** if two or more animals it fears are touching it, it doesn't move. It starts running
   again once only one is touching it.
4. **Blocked:** when a running animal's next square holds another animal, it waits and keeps its
   direction, and keeps going if the square clears. It only stops for good at a wall, the castle
   edge, or (for every animal but the mouse) the hole. If two animals would step into the same
   square at the same time, neither moves.
5. **Passing by:** a running animal that ends up beside an animal it fears turns and runs away from it.
6. **The hole:** only the mouse can go through it. The mouse escaping wins.

A run ends when the mouse escapes, when nothing moves for a step, or when the board repeats
(an endless loop).

## Project layout

| Folder | What it is |
| --- | --- |
| `engine/` | The rulebook in plain Java, no dependencies. `PhysicsTest` runs every scenario in `physics-fixtures.json`. |
| `levels/` | Level checker and generator (command line). `LevelsTest` checks that every level passes its rules. |
| `web/` | The game page. TeaVM compiles the engine to `js/engine.js`; the page only draws and animates. |
| `data/levels.json` | All 50 levels, one per line. |
| `.github/workflows/ci.yml` | On every push: build, run all tests, check the compiled JavaScript, publish to GitHub Pages. |

## Building

Java 21 and Maven:

```sh
mvn verify                                        # build, test everything, compile the engine to JS
node web/test/check-engine.js                     # check the compiled engine (Node 18+)
cd web/target/site && python3 -m http.server      # play locally at http://localhost:8000
```

## Level rules

Every level must pass these checks (`LevelChecker`, numbers per level in `LevelRules`):

- Pressing Go with nothing placed doesn't win.
- At most 2–3 solutions (most levels have exactly one).
- **No shortcuts:** in every solution, other animals start running before the mouse does.
- **No clutter:** every animal and wall on the board is needed in every solution.
- With two animals to place, both are needed.

Level tools:

```sh
./scripts/levels.sh audit             # check all levels
./scripts/levels.sh check 30          # explain one level
./scripts/levels.sh make 30 --write   # generate a new level 30 (uses all CPU cores) and save it
```

If you change the rules in `Simulator`, run `mvn verify`: the physics tests show what changed and
`LevelsTest` lists any level that no longer passes. Regenerate those with `make N --write`.
