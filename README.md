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
| `levels/` | Level checker, chain builder and random generator (command line). `LevelsTest` checks that every level passes its rules; `ChainBuilderTest` checks every recipe can still be built. |
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
- **No clutter:** every animal and wall affects the puzzle. Remove any one and either the solution
  breaks or the puzzle gets easier (so blockers and pinning animals count, decorations don't).
- Every animal in your hand is needed, and you never place a mouse.

## How levels are made

- **Levels 4–60:** random layouts, kept only if they pass the checker (`LevelGenerator`).
- **Levels 61+:** designed by `ChainBuilder` from a `Recipe`. It builds the chain forward from your
  first animal, one link at a time, running the simulator after every placement to confirm the new
  link gets scared at the right moment and that nothing moves before you place anything. It makes
  several candidates, keeps those that pass the checker, and picks the most interesting by
  `Interest` (chain length, tricks used, turns, how far your animals are from the mouse).

Tricks a recipe can ask for:

| Trick | What happens |
| --- | --- |
| Long chain | Elephant → lion → bear → dog → cat → mouse. |
| Freeze and release | An animal starts pinned between two predators; the chain pulls one away and it bolts. |
| Waiting runner | An animal is already scared but stuck behind another; it takes off when the blocker moves. |
| Clear the path | Animals sit between the mouse and the hole; each needs its own chain (one more animal in your hand). |
| Wrap-around | The mouse runs first, scares an elephant, and the chain comes all the way back for it. |

Recipes are mixed through each batch of ten rather than grouped.

Level tools:

```sh
./scripts/levels.sh audit             # check all levels
./scripts/levels.sh check 30          # explain one level
./scripts/levels.sh make 30 --write   # make a new level 30 (designed if it has a recipe) and save it
./scripts/levels.sh make 71 --name "Some Name" --write   # add a new level at the end
```

If you change the rules in `Simulator`, run `mvn verify`: the physics tests show what changed and
`LevelsTest` lists any level that no longer passes. Regenerate those with `make N --write`.

## Contributing

Work on a branch and open a pull request into `main`. CI builds, runs every test and checks the
compiled engine on each pull request; merging to `main` publishes the site.
