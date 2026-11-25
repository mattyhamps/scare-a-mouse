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
7. **Turn tiles:** an animal that runs onto a turn tile heads the way its chevrons point from then on
   (unless something scares it, as usual). Animals can't be placed on turn tiles.

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
mvn verify                                        # build, test, compile the engine to JS
mvn verify -Dbuilder.tests.excluded=none          # also check every kind of recipe can still be built (slow)
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
Kitchens the walls are drawn as counters, in the Library and Study as bookshelves, in the Great hall as banquet
tables, in the Ballroom as marble pillars and in the Gallery as statues, in the Chapel as pews, in the Secret passage as rock, in the Map room as map tables and in the Armory as weapon racks (from the Library on, only about 1 level
in 5 has walls). The Second floor (351–500, the first 10×10 boards) eases in with the Chapel, has rock walls in most Secret passage levels, then gets harder through the Map room and Armory to its boss at 500. The First floor gets harder room by room: the Great hall is about as hard as the Study, the
Ballroom and Gallery use more two-animal moves and more blockers, and level 350 is its boss. The Third floor (501–650: Guard room, Toy room, Hall of mirrors, Bathhouse, Trophy room) brings in turn tiles: 501–515 ramp up slowly (one animal and a short chain through one turn, then a second animal, then a trick), then each level reuses the recipe of the level 150 before it, so the floor is about as hard as the Second floor, with a turn tile in about 1 level in 6 or 7 (`Recipe.THIRD_FLOOR_TURNS`). Walls behave the same whatever they look like, so a room's new wall drawing (crates, toy blocks, potted palms, wash tubs, trophy stands) gets no tip or card. The Fourth floor (651–800: Treasury, Music room, Sewing room, Guest bedrooms, Clock tower) has nothing new to learn: each level reuses the Second floor's recipe from 300 levels before, so it's about as hard again, with a turn tile in about 1 level in 6 or 7 in other places than the Third floor's (`Recipe.FOURTH_FLOOR_TURNS`). Its walls are treasure chests, drums, thread spools, travelling trunks and gears. **No two levels may be the same puzzle**, counting mirror images and turned boards: the level maker refuses to save a repeat (`Duplicates`) and `LevelsTest` checks the whole set.

Recipes are mixed through each batch of ten rather than grouped.

**The castle map.** Levels are grouped into rooms, and rooms into areas: the Outside (Meadow,
Orchard, Stables, Moat bridge, Gate: 1–100), then in through the Cellars (Storeroom, Wine cellar,
Dungeon, Kitchens: 101–200), then up the castle's floors (First floor: Library, Study, Great hall,
Ballroom, Gallery: 201–350; and so on up to the Tower top at level 1000). The level picker opens at your room; from there you can go back to
the floor plan or to the whole castle. The last level of each area is its boss (`Recipe.BOSSES`).
Rooms and areas are listed in `ROOMS` and `AREAS` in `index.html`. Each room's map is one flat
drawing: the back wall with the door out at the top, then the floor, with the road winding up from the
bottom. The drawings (each room's back wall and every piece of furniture) are in `room-art.json`; each
room's floor, road shape, road material and furniture list are in `ROOM_SCENES`, and furniture is
placed wherever it fits clear of the road. Levels sit an even step apart along the road; when a tight bend
would bring two closer than a spot's width, `roomLayout` re-spaces that room's levels (or lengthens the
room), and `node tools/screens/spots.js` checks every room. **Every room's drawing ships with its levels:** when you add
levels to a new room, add its back wall to `room-art.json`, its layout to `ROOM_SCENES` and its board
look to `BOARDS` in the same change. `LevelsTest` fails if a room has levels but is missing any of them.
When you clear a room, its door opens and the mouse travels to the next room: along the corridor on
the floor plan, or, when the next room is on a new floor, first up the castle map and then in from the
stairs. Then the new room opens with the mouse walking in to its first level. A tap skips ahead.
On a room's map, tapping a level picks it (a gold ring) and shows a "Level N" button next to Close;
that button opens the level.

**Turn tiles** (planned for the Third floor, then used sparingly): a recipe can ask for turn tiles with
`withTurnTiles(n)`. The builder puts the tile on a runner's path and builds the next link beside the new
stretch, so the tile is always needed (`LevelChecker` also treats an unneeded tile as clutter). On the
board they are drawn as a blue painted space with chevrons, which flashes when it turns an animal.
Levels only carry a `turns` list (`[x, y, dir]`, dir 0 up, 1 right, 2 down, 3 left) when they have
tiles, so older levels are unchanged. For trying them out before they're in real levels, `TurnLab` builds
test levels into `web/src/main/webapp/turn-lab.json`; adding `?lab` to the game's address swaps those in
over the levels with the same numbers (each is named "Test <number>").

**The plan for the rest of the castle** (all 10×10, each floor about as hard as the one before, with a mix
of easier and harder levels, flames on the toughest and a boss at the end):

| Floor | Levels | Rooms | New board piece |
|---|---|---|---|
| Third floor | 501–650 | Guard room, Toy room, Hall of mirrors, Bathhouse, Trophy room | Turn tiles (501), then about 1 level in 6 or 7 |
| Fourth floor | 651–800 | Treasury, Music room, Sewing room, Guest bedrooms, Clock tower | None; turn tiles in about 1 level in 6 or 7 |
| Towers and roof | 801–920 | Battlements, Aviary, Watchtower, Belfry | Mousetraps (801): the mouse is caught if it runs onto one; any other animal springs it safely |
| Royal floor | 921–1070 | Royal chambers, Wardrobe, Crown vault, Tower stairs, Throne room | Trapdoors (921): run into one, come out of its partner |
| Tower top | 1071–1100 | Tower top | Everything together, the finale |

Past 1100 the castle grows an east wing: a mix of everything, moving the story along. Each new piece
comes in at the start of a room, with a card and a few easy levels, then shows up more rarely.

**No emoji.** Everything in the game is drawn: animals (`ART`), icons (`ICONS`) and rooms
(`room-art.json`). `LevelsTest` fails if an emoji appears in `index.html`, `room-art.json` or the levels.

**Extra-hard levels.** About 1 level in 15 on each floor is marked with a flame (on the map, by the level
number and in its tip) and pays 2 cheese. `Difficulty` scores how hard a level is to solve: more animals
to place, placements that touch nothing on the board, tricks, a long chain, walls and turn tiles. The
hardest of each floor, not counting the boss, get the flame. `LevelsCli hard --write` saves the list to
`data/hard-levels.json`, and `LevelsTest` fails if the list is out of date, so run it after changing levels.

**Hints and cheese.** Tap one of your animals (in the tray or on the board), then press Hint. Its first
hint costs 1 cheese and shades the 3×3 patch it goes in; its second costs 2 and lights up its exact
square. If the animal is already on its right square, the hint confirms that instead, for the same
price, and that animal needs no more hints. Tapping a placed animal picks it; tapping it again sends
it back to the tray. Cheese is scarce: you earn 1 the first time you solve a level with no hints (2 on
an extra-hard level, 3 on a boss level, nothing if you used a hint) and 2 for clearing a room. New players start with 5. Hints
you've bought stay bought for that level.

Level tools:

```sh
./scripts/levels.sh audit             # check all levels
./scripts/levels.sh check 30          # explain one level
./scripts/levels.sh make 30 --write   # make a new level 30 (designed if it has a recipe) and save it
./scripts/levels.sh make 71 --name "Some Name" --write   # add a new level at the end
```

If you change the rules in `Simulator` or the builder, run `mvn verify -Dbuilder.tests.excluded=none`
(the build does this automatically when those files change): the physics tests show what changed and
`LevelsTest` lists any level that no longer passes. Regenerate those with `make N --write`.

## Look and feel

The game is drawn in a flat medieval style: flat two-tone colours, no outlines and no gradients,
with each thing's darker tone below or to its right as if lit from the top-left. The palette and the
two fonts are CSS variables at the top of the "Flat medieval style" block in `index.html`:
`--font-title` (Almendra, for titles) and `--font-body` (Fredoka, for everything else). Change a
font or a colour there and the whole game follows.

## Contributing

Work on a branch and open a pull request into `main`. On every pull request CI builds, runs every
test, checks the compiled engine and publishes a **preview** at
`https://mattyhamps.github.io/scare-a-mouse/pr-preview/pr-<number>/` (a bot comments the link).
Play the preview before merging; its progress is stored separately from the live game. Merging to
`main` publishes the live site, and closing a pull request removes its preview.

Both the live site and the previews are folders on the `gh-pages` branch
(Settings → Pages → Deploy from a branch: `gh-pages`, `/ (root)`).
