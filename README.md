# Scare-a-Mouse 🐭

A chain-reaction puzzle game. Place animals so each one scares the next, and get the mouse
into the mouse hole.

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
6. **The hole:** a square on the board. Only the mouse can go into it, and the mouse getting in
   wins. Every other animal treats it like a wall.

A run ends when the mouse gets into the hole, when nothing moves for a step, or when the board repeats
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
- **Board size grows as you go:** 1–100 are 7×7, 101–200 are 8×8, 201–350 are 9×9, and from 351
  on they are 10×10, the original game's size (`Recipe.sizeForLevel`). Boards bigger than
  7×7 get a thinner castle wall on screen so the squares stay easy to tap.

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

**Already-moving levels** (from level 101, about half of each batch) put the first animal of the
chain on the board, so the board starts moving by itself when you press Go. Your animals steer it
instead of starting it:

| Move | What you do |
| --- | --- |
| Swerve | Place an animal a runner fears beside its path, so it turns the right way. |
| Catch | A chain link is missing from the board; place it where a runner passes so it carries the chain on. |
| Stop | Place an animal in a runner's path to halt it before it scares a "spoiler" that would ruin the run. |

**Walls** (from the Kitchens, level 171): recipes can ask for 2–4 walls. Some stop a runner on the
right square before it reaches a spoiler; the rest close off squares that would give a second,
easier solution. Like every board piece, each wall has to matter to the puzzle.

Each castle room also tints the board (floor, stone and wall look) so it fits the room; in the
Kitchens the walls are drawn as counters.

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

Work on a branch and open a pull request into `main`. On every pull request CI builds, runs every
test, checks the compiled engine and publishes a **preview** at
`https://mattyhamps.github.io/scare-a-mouse/pr-preview/pr-<number>/` (a bot comments the link).
Play the preview before merging; its progress is stored separately from the live game. Merging to
`main` publishes the live site, and closing a pull request removes its preview.

Both the live site and the previews are folders on the `gh-pages` branch
(Settings → Pages → Deploy from a branch: `gh-pages`, `/ (root)`).
