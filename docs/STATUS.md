# Where things stand

Update this file in every pull request: what changed, what's next, and any decision Matt made.

_Last updated: 25 November 2026._

## Done

- Levels 1–650 are live: the Outside (1–100), Cellars (101–200), First floor (201–350), Second floor
  (351–500) and Third floor (501–650: Guard room, Toy room, Hall of mirrors, Bathhouse, Trophy room), all with drawn rooms, a castle map, bosses, flames on the hardest levels (2 cheese), hints
  bought per animal with cheese, and the mouse travelling between rooms when you clear one.
- Turn tiles (blue painted space with chevrons that flashes when it turns an animal) come in at 501 with a
  card and a slow ramp, then appear in about 1 level in 6 or 7. Adding `?lab` to the address loads test
  puzzles from turn-lab.json.
- No repeated puzzles: the level maker refuses a repeat (mirror images and turned boards count) and a test
  checks the whole game. 13 older repeats were rebuilt.

## Next

1. **Fourth floor (651–800):** Treasury, Music room, Sewing room, Guest bedrooms, Clock tower. Turn tiles
   now and then. Draw the five rooms first and get Matt's OK (show all five at once), then the levels.
2. **Towers and roof (801–920):** Battlements, Aviary, Watchtower, Belfry. New piece: **mousetraps**. The
   mouse is caught if it runs onto one (the run fails, cartoon "Snap!"); any other animal that runs over
   it springs it safely, and then it's harmless. Only running onto it counts, not standing next to it.
3. **Royal floor (921–1070):** Royal chambers, Wardrobe, Crown vault, Tower stairs, Throne room. New
   piece: **trapdoors**, two linked squares: an animal that runs into one comes out of the other, still
   going the same way.
4. **Tower top (1071–1100):** everything together, the finale. Past 1100 an east wing: a mix of everything.

## Decisions to remember

- Boards stay 10×10 from the Second floor on.
- Each floor is about as hard as the one before, with a mix of easier and harder levels; the toughest
  get a flame. Rooms of about 30 levels.
- A new piece starts at the beginning of a room with a pop-up card and easy levels, and is used
  sparingly afterwards.
- Room drawings: varied furniture (no repeating the same small item over and over), nothing that looks
  like it floats, nothing so small you can't tell what it is.
- Picking a level on the map shows a "Level N" button; the next room's first level is picked after the
  mouse travels there.
- Big jobs like building hundreds of levels are much faster in Claude Code on Matt's own computer than in
  a cloud session.
