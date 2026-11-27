# Where things stand

Update this file in every pull request: what changed, what's next, and any decision Matt made.

_Last updated: 27 November 2026._

## Done

- Levels 1–800: the Outside (1–100), Cellars (101–200), First floor (201–350), Second floor (351–500),
  Third floor (501–650: Guard room, Toy room, Hall of mirrors, Bathhouse, Trophy room) and Fourth floor
  (651–800: Treasury, Music room, Sewing room, Guest bedrooms, Clock tower), all with drawn rooms, a
  castle map, bosses, flames on the hardest levels (2 cheese), hints bought per animal with cheese, and
  the mouse travelling between rooms when you clear one.
- Levels 801–950, the whole Royal floor (five rooms and its boss), with mousetraps (see below).
- Levels 951–1100, the whole Towers and roof (six rooms, the floor's boss at 1075 and the castle's last boss
  at 1100), with trapdoors (see below). The castle is finished: a finale card after 1100.
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
- A level with a pop-up card (a new animal or board piece) shows it every time you open that level, not
  just the first time, so a player who skipped it or comes back later can read it again. (Not when the
  map is about to open over the level, after "All levels" or "Open the door" on the win card.)
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
- The castle's upper floors were reordered (Matt): the Royal floor now comes before the Towers and roof,
  as in a real castle where the royal rooms sit under the roof. Royal floor 801–950: Royal chambers,
  Wardrobe, Sitting room (new, in place of the Crown vault), Tower stairs, Throne room; mousetraps at 801,
  boss at 950. Towers and roof 951–1075: Battlements, Aviary, Watchtower, Belfry and the Crown vault (moved
  up, last before the Tower top); trapdoors at 951.
- **Rooms of 25 on the Towers and roof** (Matt, #64): every room ends on a 5 or a 0. Battlements 951–975,
  Aviary 976–1000, Watchtower 1001–1025, Belfry 1026–1050, Crown vault 1051–1075 (the floor's boss moved
  from 1070 to 1075), Tower top 1076–1100 (the finale boss stays at 1100). They were 24 each before.
- The Royal chambers (801–830) and Wardrobe (831–860), drawn in `tools/art/gen25.py` (`export_royal.py`):
  Royal chambers is the king and queen's bedroom (rose wallpaper, curtained windows, coat of arms; a canopy
  bed, fireplace, cradle, crowned armchair, writing desk, orange trees, a royal pet bed), dusty-rose floor
  with a red velvet path that crosses the room in drooping swags. Board walls are velvet footstools.
  The Wardrobe is the royal dressing room (striped lilac wall with shelves of folded clothes, hats and
  capes; robes on a rail, a gown on a stand, an open wardrobe, a swinging mirror, a shoe shelf, a
  shoemaker's bench), basket-weave wood floor with a lilac carpet shaped like coat hangers on a rail. No
  walls on the Wardrobe's boards (Matt's call).
- Their levels have fresh recipes (`Recipe.royalFloor`): 801–802 only the mouse and cats (made by
  `TrapLab.catsOnly`, through `LevelsCli make`), 803–807 steer around traps in longer chains, the second
  card at 808 with easy spring levels (808–811), then a mix of easy and hard with traps in about 1 level
  in 5 and footstools in about 1 in 5 in the Royal chambers. `LevelsCli make` now refuses a trap level
  where a trap doesn't matter (`TrapLab.trapsDoTheirJob`).
- Wardrobe fix (Matt's review of #59): the two little red slippers on the floor and the parasol pot are
  gone; a stack of hat boxes and a domed travel trunk took their place, and the folded-clothes stool shows
  up less often. Levels 836 and 848 were renamed to match ("Steamer Trunk", "Hat Box Tower").
- The Sitting room (861–890) and Tower stairs (891–920), drawn in `gen25.py`:
  The Sitting room is the royal family's tea-and-games room (sage wallpaper, a window seat, a landscape
  painting, a shelf of plates and a tea set; a sofa, a tea table with a cake stand, a chess table with
  plain pieces, a card table, a rocking chair with a knitting basket, a fish tank, a curio cabinet, a fern and a lamp
  table), sage and cream checked tiles with a cream runner whose path climbs in L-shaped knight's moves.
  Board walls are tea chests.
  The Tower stairs is a stone stairwell (arrow slits, banners, a round window; a rope hoist with a basket,
  portraits of a mouse queen, a lion king and an elephant on easels, a banner stand, a high-backed bench,
  a knight statue in a niche, a lantern post, climbing ivy), grey stone floor with a red stair carpet with
  brass rods, running up the walls with a stone landing at each turn (`shape.landings`). Board walls are
  stone blocks. (Matt turned down a chess rook and an iron lantern for the board walls, and animal-headed
  chess pieces.)
- Their levels (`Recipe.royalFloor`, 861–920) mix the new puzzle types below in with the familiar ones,
  with traps in 6 levels and walls in 6 levels per room, and a few easy dog chains as breathers. They
  score about as hard as 801–860. 882 and 890 were changed after the dry run (a walled STOP+CATCH moving
  level and a frozen SWERVE+CATCH one were slow).
- Flames from 801 on are spread out (Matt's review of #60): `Difficulty.hardest` skips a level within 4 of a
  flame already picked and takes the next hardest, so a room doesn't get several in a row. Earlier floors
  keep their flames. The Royal floor's flames are now 816, 830, 840, 850, 872, 886, 909 and 920 (832, 870
  and 871 lost theirs); they are counted across 801–950 and will shift again when the Throne room is
  built. A test checks the spacing.
- The Sitting room's second chess table became a card table with two chairs (`games_table`; the Guard
  room already has a `card_table`). Matt kept the Wardrobe's two folded-clothes stools.
- The Throne room (921–950), drawn in `gen25.py`: a court day (deep red damask wall with two stained-glass
  windows, a red canopy with a crown over the door, the king's and queen's thrones on a dais; a lion statue on
  a plinth, a gold candelabra, the heralds' trumpets, a court bench, the sceptre and orb in a glass case, a
  palm in a gold tub, a chest of gifts), cream and gold diamond marble floor, and a red carpet with a double
  gold border that sweeps between two rows of marble pillars, then runs straight up to the thrones
  (`processional`). Board walls are marble columns. Each piece of furniture appears once (Matt: no repeats,
  `maxProps` keeps the list from starting over).
- Its levels (`Recipe.royalFloor`, 921–950): the same mix, traps in 6 levels and walls in 6 (counting the
  boss). 942 was changed after the dry run (a waiting runner with SWERVE+CATCH was slow). The boss, 950
  "Crowning Glory", has 3 animals to place, 4 walls and a trap to spring (scores 19, against 14.5 for 800).
  The Royal floor's flames: 816, 830, 840, 850, 872, 886, 909, 920, 937, 948.
- Long level names no longer get cut off on phones. Before, the name shared its row with the label ("Boss ·
  Level N · solved ✓") and the cheese count: 6 names were cut off at 390px and 24 at 360px, and 115 / 370 more
  once a level was solved. Now the header is one line: the crown (boss) or flame sits just before the name,
  the solved tick just after it, and the cheese count on the right. The "Level N" label is gone from there
  (the Level button at the top already shows it). Matt first picked a two-line header, then this one-line
  version to save height. Names are kept to 20 characters (the most that fit at 360px with a crown and a
  tick); six were renamed: 514 "Guard Change", 650 "Floor Champion", 830 "Goodnight, Majesty", 898 "The Mouse
  Queen", 926 "Coloured Windows", 944 "Kneel to the Crown" (only names changed, so progress is kept).
  `tools/screens/names.js` checks every name in the real header at 360px and 390px, and `LevelsTest` fails on
  a name over 20 characters.
- The top bar's title is a little smaller on screens 380px wide and narrower, so the Level button ("Level 950")
  no longer pokes into the page's right margin on small phones (it did from level 20 on). The old 420px rule
  for it never took effect (a later rule overrode it).
- The art scripts need Python 3.12 or newer (`python` on Matt's PC is 3.10; use the Python 3.13 install).
- Trapdoors, the piece (no real levels yet), with Matt's choices: one linked pair per board; every animal,
  the mouse too, drops in one and comes out of the other still heading the same way; if either trapdoor is
  covered the animal waits (engine rule 9; the engine reports `drops`). The look: an open wooden hatch with
  stone steps going down, flat on the floor (Matt picked it over a purple swirl, a plain or round wooden
  hatch, a stone slab, and open hatches with a ladder or a lid). In the game the animal shrinks into the
  first trapdoor, both flash with a soft "whoop", and it grows out of the other. Card at 951: "New:
  trapdoors!". The level maker can make trapdoor levels (`Recipe.withTrapdoors(1)`) and throws away any
  where the trapdoors don't matter. 951 is made by hand like level 1 (Matt): one cat, and the trapdoors take
  the mouse under a mousetrap (`TrapdoorLab.intro`, `LevelsCli make 951`); the checker skips its clutter
  rule there only, since the trap is there to show the idea (Matt). Eleven test levels at
  `?lab=trapdoor-lab` (951–961, `TrapdoorLab`): 951, then chains through a trapdoor started by a dog, bear,
  lion and elephant, a second animal to place, then trapdoors with tricks and with a mousetrap.
- Dragging an animal onto the board no longer drops it on a turn tile, mousetrap or trapdoor (tapping
  already didn't).
- The Battlements (951–975) and Aviary (976–1000), drawn in `tools/art/gen26.py` (`export_towers.py`):
  the Battlements is the defenders' wall, outdoors (sky, hills far below, far-off towers, a parapet to the
  door's tower; a cannon, a pyramid of cannonballs, a catapult, a striped sentry box, a signal fire, a rack
  of bows and arrows, a brass telescope), a grey stone wall-walk with merlons down both sides and a plank
  path that swings round round turret platforms at the corners (`turrets`). The Aviary is a garden bird
  house (glass and iron arches with ivy; tall cages, a cage on a shepherd's hook, a parrot perch, a bird
  bath, nest boxes, a seed table, a little tree with birds, two birds flying in open grass, clear of the
  path and the level spots: `flyClear` in `ROOM_SCENES`), clover grass with a pale gravel
  path gliding side to side (`flight`). Matt turned down a loop-the-loop path (too twirly, levels
  overlapped) and asked for bird colours that stand out (deep blue, purple, orange, red).
- **No walls on the Towers and roof** (Matt): the boards have no wall drawing (the cannon and birdcage board
  walls he picked earlier were dropped).
- Their levels (`Recipe.towersFloor`): 951 is made by hand ("Under the Trap": one cat, the trapdoors take
  the mouse under a mousetrap), 952–956 learn trapdoors (chains through one started by a dog, bear and
  lion, a second animal to place, an elephant chain), then trapdoors about 1 level in 7 (Matt: sparse after
  onboarding), mousetraps about as often, turn tiles twice. 974, 998 and 999 were changed after the dry run.
  975 ("Turret Trapdoor", once "Bird House") moved into the Battlements with its puzzle kept; 999 and 1000
  are new. Flames so far: 965, 981, 986 (counted across 951–1075, so they'll shift as the floor fills up).
  `LevelsTest` now also accepts a level count that ends a 25-level Towers and roof room.
- The Watchtower (1001–1025), Belfry (1026–1050) and Crown vault (1051–1075), also in `gen26.py` (Matt picked
  each idea, then asked for more contrast):
  - Watchtower: the lookout room, a round sandstone room with windows over the fields and a map of the lands
    over the door; a map table, a stand of spyglasses, a signal horn, a beacon lamp, a desk with a logbook and
    hourglass, a cockerel weathervane, a bench with a blanket. Dark flagstones; a pale rope-edged path that winds
    round sandstone pillars down the middle (`slalom`, the pillars come from the shape: `pillar` in `ROOM_SCENES`).
  - Belfry: the bell loft, oak beams, three bronze bells (the big one on a wheel), louvred windows, sleepy bats;
    a cracked old bell, a bell on a frame, a ladder, a coil of rope, a bat post, handbells, a crate with a spare
    clapper. Dark planks; a cream bell-rope path that swings across in big arches (`bellswing`).
  - Crown vault: the crown jewels behind a round steel vault door (its way out), crowns in lit alcoves; a crown
    on a plinth, an orb and sceptre, a jewelled sword in a case, a tiara cabinet, a ring tray, an ermine robe, a
    crowned bust (none of them repeat the Treasury's). Near-black floor; a red velvet queue with brass posts down
    both edges (`queue`, `posts` in `ROOM_SCENES`).
  - Boards: sandy, oak and gold, no walls. Map icons: a tower, a bell, a crown.
- Their levels (`Recipe.towersFloor`): the same mix as 951–1000, no walls, trapdoors in 12 of the 75 (about
  1 in 6 or 7), mousetraps in 13, turn tiles in 3. 1005 was changed after the dry run. 1075 is the floor's boss:
  three to place, a trap to spring and a trapdoor.
- Made harder after Matt's review of #65 (the castle was getting easier as it climbed): 18 of the easiest
  recipes swapped for harder ones (the three one-dog levels are gone, most trapdoor levels now have two to
  place, more three-animal levels: 1001, 1003, 1004, 1009, 1013, 1017, 1020, 1026, 1031, 1036, 1037, 1044, 1046, 1052,
  1056, 1057, 1063, 1066). Average `Difficulty.score` now about 12 in each room (Watchtower 12.1, Belfry
  12.1, Crown vault 12.2; before 10.0, 10.6, 10.7), above the Royal floor (11.1), below the Fourth (12.5).
  Flames across the floor: 965, 981, 986, 1029, 1034, 1040, 1054, 1066.
- The Tower top (1076–1100), the finale, also in `gen26.py` (Matt picked the starry roof, then swapped
  most of the first pieces and the board walls):
  - The open roof at night: moon, stars and fireworks, the castle's other towers far below, and far-off
    hills with a road and a village's lights (the world beyond the castle, in place of a first idea of a
    new wing being built). The climb ends at a little stair turret with the castle's flag on its roof.
  - Pieces: a brass telescope, a star chart on an easel, a globe of the night sky, a desk with a book of
    stars, a rug with cushions for stargazing, a rain barrel with the moon in it. Lanterns on posts at
    every third turn of the path (`pillar` in `ROOM_SCENES`, placed by the shape).
  - Dark blue-grey roof stones; a pale moonlit path with gold dots that runs straight from point to point
    like a constellation (`constellation`). The board: pale night-blue checks, the plain walls (Matt).
  - Its door says "Beyond the castle" (Matt), not the next room's name; the rooms after 1100 are still
    called East wing 1, 2 and so on in `index.html` until they are designed.
  - The finale card (`FINALE_CARD`): after clearing the Tower top it pops up over the win screen, says you
    reached the top of the castle, and that the door leads beyond the castle with more on the way. Like the
    other cards it can be read again: it shows whenever level 1100 is opened after the room is cleared
    (Matt's review of #66).
- Its levels (`Recipe.towersFloor`): the hardest room so far, average `Difficulty.score` 12.6. Walls are back
  in 6 of the 25 (about 1 in 5, Matt; a room's wall drawing never gets a card), mousetraps in 6, trapdoors
  in 4, one turn tile. 1084 was changed after the dry run. 1100 is the castle's last boss (score 19, the
  hardest in the room): walls, two traps to spring and a trapdoor; its first build scored only 15.5, so the
  recipe was made harder. Flames: 1083 and 1099.

## Next

1. **The App Store:** ship the finished castle as an iPhone app called **Mouse in Hole**, as soon as
   possible. The plan, Matt's decisions (name, audience, cheese and hints, ads, cheese packs) and the steps
   are in `docs/APP_STORE.md`. Work through its steps in order, one pull request each. Step 1 (feel like a
   phone app) includes Matt's height check: the level screen, the floor map and the cards must fit a phone
   without scrolling.
2. **Beyond the castle (past 1100):** on hold while the app ships (Matt). What comes next is still open
   (Matt: leave the door open for more levels and a bigger world). Name and design it first, then
   drawings (show Matt). Levels there should get gradually harder (see the decisions below).
   `trap-lab.json` is still kept (Matt, #60).

## New puzzle types for 861 on

Matt wants the rest of the castle to switch it up instead of reusing the same 15 or so recipe types
(levels 351–860 mostly used those). A dry run (one build each, 30 s) found these new types build quickly:

- `Recipe(ELEPHANT, 2, WAITING_RUNNER)`: two blockers and a waiting runner (hard, 3 to place)
- `Recipe(LION, 2, PLAIN).withMoves(CATCH)`: already moving with two blockers and one catch (hard)
- `Recipe(ELEPHANT, 1, FREEZE_RELEASE).withMoves(SWERVE)`: already moving with a blocker
- `Recipe(ELEPHANT, 0, FREEZE_RELEASE).withMoves(SWERVE, STOP)`
- `Recipe(ELEPHANT, 1, WAITING_RUNNER).withMoves(STOP).withTraps(1, 2)`
- `Recipe(CAT, 1, wrap, PLAIN).withTraps(1, 2)` and `Recipe(CAT, 0, wrap, PLAIN).withSpringTraps(1)`: wrap-around chains with traps
- `Recipe(LION, 0, PLAIN).withSpringTraps(2)`: two traps to spring (3 to place)
- `Recipe(ELEPHANT, 0, FREEZE_RELEASE).withWalls(1, 3).withSpringTraps(1)`: walls and a trap
- `Recipe(LION, 0, PLAIN).withTurnTiles(1).withSpringTraps(1)` and
  `Recipe(ELEPHANT, 0, PLAIN).withMoves(CATCH).withTurnTiles(1).withTraps(1, 2)`: turn tiles and traps together
- `Recipe(DOG, 1, PLAIN)` (fairly easy) and `Recipe(DOG, 0, PLAIN)` (very easy, a breather)

These found nothing in 30 s, so don't rely on them: a frozen animal and a waiting runner in one chain; three
moves, or two catches, in a moving level; a lion chain with two missing links; bear-started chains with a
frozen animal; a wrap-around chain that's already moving; walls plus steering round traps. Lane-blocker
levels with steer-around traps (`Recipe(BEAR, 1).withTraps`) kept leaving a trap that didn't matter.

## Before release

Notes from Matt's legal and App Store checklist (a separate document):
- Keep "CastleMouse" and "Castle Mouse" out of the game's name, store listing, keywords and icon.
- Nothing important may be drawn with emoji (already true, and a test enforces it).
- The repo is public with no license. Plan to make it private before launch.
- The rest of the release checklist (listing, privacy policy, privacy labels, the EU contact details) is
  step 5 of `docs/APP_STORE.md`.

## Decisions to remember

- The game's name is **Mouse in Hole** (store, app and everything players see). It's for puzzle fans aged
  about 15–45, with plain, friendly text. Matt publishes as an individual. (November 2026)
- Hints cost 3 cheese for the shaded area and 3 more for the exact square, and new players start with 0
  cheese. A hint by ad is always available, rewarded ads only. Cheese packs are how players skip ads. There's
  no "remove ads" purchase and no unlimited hints, so cheese keeps its value. Details in `docs/APP_STORE.md`.
- Difficulty: the castle (1–1100) stays at its current difficulty for launch; it levels off at about 12
  from level 200 on. Levels after 1100 should get gradually harder: a higher average, and flame and boss
  levels that properly test puzzle fans (for example 4 animals to place, or two new pieces together). After
  launch, use player stats (where people stop or use hints) to fix any castle level that's too hard.

- A level's pop-up card shows every time the level is opened (Matt: so it can be read again).
- Boards stay 10×10 from the Second floor on.
- Each floor is about as hard as the one before, with a mix of easier and harder levels; the toughest
  get a flame. Rooms of about 30 levels.
- Walls: about 1 level in 5 has walls in each room (about 6 of 30), spread through the room.
- A new piece starts at the beginning of a room with a pop-up card and easy levels, and is used
  sparingly afterwards.
- New pieces ramp up slowly. The first turn-tile test levels jumped from very easy to very hard ("0 to
  100"). The real ramp goes: one animal and a short chain through the new piece, then longer chains, then
  a second animal to place, then the piece combined with tricks, and only then sparingly mixed in.
  Mousetraps (801) and trapdoors (951) follow the same pattern.
- Pieces you step on stay flat on the floor. The turn tile is a flat blue painted space with a plain
  outline and three chevrons. Raised or blocky versions (tokens, slabs, a bevelled edge) looked like walls
  that would block the animal instead of something it runs onto. Keep this in mind for how mousetraps
  and trapdoors look, and show Matt a few options before choosing. (Trapdoors: an open hatch with stone steps,
  flat in the floor, so it reads as a hole to go down rather than a block.)
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
- From level 861 on, mix the new puzzle types above in with the familiar ones (Matt).
- From the Royal floor on, work a couple of rooms at a time (drawings, then levels, one pull
  request), not a whole floor at once.
- Big jobs like building hundreds of levels are much faster in Claude Code on Matt's own computer than in
  a cloud session.
