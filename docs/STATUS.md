# Where things stand

Update this file in every pull request: what changed, what's next, and any decision Matt made.

_Last updated: 25 November 2026._

## Done

- Levels 1–800: the Outside (1–100), Cellars (101–200), First floor (201–350), Second floor (351–500),
  Third floor (501–650: Guard room, Toy room, Hall of mirrors, Bathhouse, Trophy room) and Fourth floor
  (651–800: Treasury, Music room, Sewing room, Guest bedrooms, Clock tower), all with drawn rooms, a
  castle map, bosses, flames on the hardest levels (2 cheese), hints bought per animal with cheese, and
  the mouse travelling between rooms when you clear one.
- Turn tiles (blue painted space with chevrons that flashes when it turns an animal) come in at 501 with a
  card and a slow ramp, then appear in about 1 level in 6 or 7. Adding `?lab` to the address loads test
  puzzles from turn-lab.json.
- No repeated puzzles: the level maker refuses a repeat (mirror images and turned boards count) and a test
  checks the whole game. 13 older repeats were rebuilt.
- The Fourth floor: five rooms drawn (`tools/art/gen24.py`, `export_fourth.py`), each with its own floor,
  path and path shape: Treasury (green vault, cream runner, key pattern), Music room (plum, piano keys, a
  bobbing tune), Sewing room (gingham, tape measure, zigzag stitching), Guest bedrooms (blue carpet,
  striped runner, bays to each side), Clock tower (planks, iron catwalk, pendulum swings). Board walls
  are chests, drums, thread spools, trunks and gears. The levels reuse the Second floor's recipes, with
  turn tiles in about 1 in 6 or 7 and walls in 6 levels per room (`Recipe.FOURTH_FLOOR_WALLS`).
- Level spots on the room maps never overlap: `roomLayout` re-spaces a room's spots when two would sit
  closer than 48 room units (a spot is about 42 wide), and leaves other rooms' layouts as they were.
  `node tools/screens/spots.js` measures every room.
- Building levels: `LevelsCli probe` is a quick dry run of a batch's recipes, and `tools/levels/build.sh`
  runs it first, then builds in order and stops after two failed tries on a level.
- Claude Code is set up on Matt's Windows PC (JDK 21, Maven, Node 22, Playwright, Python 3.13 for the
  art scripts, and the GitHub CLI signed in as mattyhamps).
- Tester link: https://mattyhamps.github.io/scare-a-mouse/?demo plays only the Meadow (levels 1–20) with
  its own saved progress, no developer mode and no feedback button. The rest of the castle says "Coming
  soon", and clearing level 20 opens the door and then shows a thank-you screen with "Play again".
- Mousetraps, the piece (no real levels yet): engine rule 8, the drawing (classic snap trap with a big
  wedge of cheese; sprung = faded, no cheese), the snap with stars and a "Snap!" sound, a caught mouse with
  the bar on its tail and "The mouse got caught!", and two cards (801: mousetraps catch the mouse but
  other animals run over them safely; 808: a trap another animal sprung is safe for the mouse).
  The level maker can make trap levels: `Recipe.withTraps(min, max)` (steer around) and
  `withSpringTraps(n)` (a trap on the mouse's way plus one more animal to send over it first). Steer-around
  traps need a recipe with a few other solutions to close off: moving levels with one CATCH or STOP, or a
  lane blocker, work; plain one-animal levels don't (they only ever have one solution). Twelve test levels:
  `?lab=trap-lab` (801–812, made by `TrapLab`). 801–802 have only the mouse and cats: the hole is straight
  ahead of the mouse with a trap in between, so cats have to turn it the long way round (sending it
  straight gets it caught, so you can try that and see). Matt wants one or two of these, not more.

## Next

1. **Towers and roof (801–920):** Battlements, Aviary, Watchtower, Belfry. New piece: **mousetraps**
   (the piece is done; see above). Next: Matt tries the test levels, then the Battlements and Aviary
   drawings (show Matt first), then their levels with fresh recipes: 801–805 steer around traps and get
   harder (start with one or two mouse-and-cats levels like the test ones), the second card with easy spring
   levels, both mixed after that, then traps in about
   1 level in 5. Work two rooms at a time.
2. **Royal floor (921–1070):** Royal chambers, Wardrobe, Crown vault, Tower stairs, Throne room. New
   piece: **trapdoors**, two linked squares: an animal that runs into one comes out of the other, still
   going the same way.
3. **Tower top (1071–1100):** everything together, the finale. Past 1100 an east wing: a mix of everything.

## Before release

Notes from Matt's legal and App Store checklist (a separate document):
- Keep "CastleMouse" and "Castle Mouse" out of the game's name, store listing, keywords and icon.
- Nothing important may be drawn with emoji (already true, and a test enforces it).
- The repo is public with no license. Plan to make it private before launch.

## Decisions to remember

- Boards stay 10×10 from the Second floor on.
- Each floor is about as hard as the one before, with a mix of easier and harder levels; the toughest
  get a flame. Rooms of about 30 levels.
- Walls: about 1 level in 5 has walls in each room (about 6 of 30), spread through the room.
- A new piece starts at the beginning of a room with a pop-up card and easy levels, and is used
  sparingly afterwards.
- New pieces ramp up slowly. The first turn-tile test levels jumped from very easy to very hard ("0 to
  100"). The real ramp goes: one animal and a short chain through the new piece, then longer chains, then
  a second animal to place, then the piece combined with tricks, and only then sparingly mixed in.
  Mousetraps (801) and trapdoors (921) follow the same pattern.
- Pieces you step on stay flat on the floor. The turn tile is a flat blue painted space with a plain
  outline and three chevrons. Raised or blocky versions (tokens, slabs, a bevelled edge) looked like walls
  that would block the animal instead of something it runs onto. Keep this in mind for how mousetraps
  and trapdoors look, and show Matt a few options before choosing.
- Never show the total number of levels (no "Level 47 of 500" or "out of 500"). Show just the level
  number.
- Ideas considered but not chosen: sticky squares (an animal stops on it), hiding spots (an animal on it
  can't scare or be scared), and corner bumpers (a turn tile that bounces like a mirror, depending on
  which side the animal comes from). Turn tiles use fixed arrows instead. Don't propose these as new;
  they're on record if Matt wants more twists later.
- Room details that worked: playful touches tied to the game, like toy blocks spelling animal names,
  went over well. Display rooms, like the Trophy room, should look organized, not scattered with small
  items.
- Room drawings: varied furniture (no repeating the same small item over and over), nothing that looks
  like it floats, nothing so small you can't tell what it is. Nothing lying on the floor that wouldn't
  be there (loose gems, sheet music); use the space for bigger, striking pieces. Keep a room's path calm
  and make it stand out from the floor (Matt turned down a busy coin path and gold-on-brown).
- Picking a level on the map shows a "Level N" button; the next room's first level is picked after the
  mouse travels there.
- New wall drawings normally get no tip, but round ones that could be mistaken for animals get a
  "New: ..." tip the first time they appear (drums at 683, gears at 771). No card for them.
- From the Towers and roof on, work a couple of rooms at a time (drawings, then levels, one pull
  request), not a whole floor at once.
- Big jobs like building hundreds of levels are much faster in Claude Code on Matt's own computer than in
  a cloud session.
