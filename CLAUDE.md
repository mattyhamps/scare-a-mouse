# Scare-a-Mouse: notes for Claude

A chain-reaction puzzle game: each animal scares the next one up the food chain (mouse, cat, dog, bear,
lion, elephant, and elephants fear mice), and you place animals so the chain ends with the mouse running
into its hole. The levels climb a castle, floor by floor. Owner: Matt (GitHub `mattyhamps`).

- Live: https://mattyhamps.github.io/scare-a-mouse/
- Each pull request gets a preview: https://mattyhamps.github.io/scare-a-mouse/pr-preview/pr-<number>/
- The README explains the rules, the code layout, how levels are made and the plan for the rest of the castle.
- **Read `docs/STATUS.md` first**: where the project is right now and what's next. Update it in every PR.

## How we work

- Every change goes on a new branch made from `main`, then a pull request. Matt tests the preview and
  merges (squash). Never merge, never push to `main`, and don't build one branch on top of another
  unmerged one. Before pushing more commits to a PR's branch, check the PR hasn't been merged; if it
  has, start a new branch from `main`.
- Commit as Matt: `git -c user.name=mattyhamps -c user.email=32683412+mattyhamps@users.noreply.github.com commit ...`.
  No `Co-Authored-By` or session lines in commits, and no "Generated with Claude" lines in PR descriptions.
- Who does what: Claude Code writes all the code. The Claude app reviews pull requests and leaves its
  feedback as PR comments; it doesn't open PRs or push without asking Matt first.
- Reviews before merging: when a PR is ready, Matt asks for a review. Act on the review comments in the
  same PR (push to the same branch, after checking it isn't merged), then update the PR description.
- Ask before building when there are real choices to make. Show anything visual (room drawings, new
  board pieces, cards, map changes) as screenshots and get Matt's OK before building big changes on it.
- Plain, friendly game text for all ages. After level 10, a level's tip only announces something new
  ("New: ..."), never how to solve it.
- No emoji anywhere in the game: everything is drawn (`ART`, `ICONS`, room-art.json). A test enforces it.
- Walls work the same whatever they look like, so a room's new wall drawing gets no tip and no card.
  A new board piece or rule (turn tiles, mousetraps, trapdoors) comes in at the start of a room, with a
  pop-up card (`NEW_CARDS` in index.html) and a few easy levels, then shows up more rarely.
- No two levels may be the same puzzle, counting mirror images and turned boards. The level maker refuses
  to save a repeat and a test checks the whole game.
- Developer mode (every level open) needs a passphrase in the address (`#dev=...`). It is not in the
  repo; Matt has it. Never write it in a commit, PR, issue or file here.

## Build and test

Java 21 and Maven, Node 22 for the JavaScript check.

```
mvn -B verify                                      # everything except the slow builder test
mvn -B verify -Dbuilder.tests.excluded=none        # also checks every recipe can still be built (slow)
node web/test/check-engine.js web/target/site/js/engine.js   # the compiled JavaScript engine
```

`mvn verify` puts the playable site in `web/target/site` (serve it over http, for example
`python -m http.server -d web/target/site`, since the page loads its levels with fetch).

CI runs the builder test only when the physics or the level builder change (see `.github/workflows/ci.yml`).

## Making levels

1. Write the recipes in `levels/.../Recipe.java` (`designed(n)`; the Third and Fourth floors are in `thirdFloor(n)` and `fourthFloor(n)`).
2. Build the levels with `tools/levels/build.sh FROM TO` (from the repo root, in Git Bash on Windows)
   after `mvn -q -pl levels -am package -DskipTests`. It first does a quick dry run (`LevelsCli probe`)
   and stops if any recipe is slow, so change that recipe first (a turn tile on a recipe that is already
   hard, like a moving board with a waiting runner, can take forever). Then it builds each level in
   order and stops after two failed tries on one level instead of grinding on. By hand, one level is:
   `java -cp engine/target/classes:levels/target/classes io.github.mattyhamps.scareamouse.levels.LevelsCli make 651 --candidates 3 --balance 10 --write`
   (on Windows use `;` between the two classpath folders). If it finds nothing, try `--seed` with another
   number. `make` refuses a level that repeats another one.
3. Give each new level a name that fits its room (every name in the game is different, 20 characters at most so it
   fits on a phone; `node tools/screens/names.js` checks the real header at 360px and 390px).
4. `LevelsCli hard --write` updates `data/hard-levels.json` (the flame marks), then run the tests.
5. A new room also needs its drawings (room-art.json, see `tools/README.md`), a layout in `ROOM_SCENES`
   and a board look in `BOARDS` (index.html). The tests check all three.

## Looking at the game

`tools/screens/` has scripts that play levels and take screenshots (see `tools/README.md`). Use them to
check work and to show Matt pictures before asking for approval.
