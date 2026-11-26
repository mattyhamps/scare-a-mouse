# Tools

## `art/`: the room drawings

Every room's back wall and piece of furniture in `web/src/main/webapp/room-art.json` comes from these
Python scripts. Each `genNN.py` builds on the one before it (it runs the earlier file's helpers), so the
drawing style stays the same: flat shapes, the light half of each object on the left and a darker half on
the right, one soft shadow under anything that stands on the floor.

- `gen22.py`, `gen23.py`: the Third floor (Guard room, Toy room, Hall of mirrors, Bathhouse, Trophy room).
  `python3 gen22.py && python3 gen23.py && python3 export_third.py` rebuilds those rooms in room-art.json.
- `gen25.py`: the Royal floor (Royal chambers, Wardrobe, Sitting room, Tower stairs, Throne room).
  `python3 gen25.py && python3 export_royal.py` rebuilds them; it also writes `royal_tiles.json`, the board
  walls used in index.html's CSS (footstool, tea chest, stone block, marble column).
- `export_outside.py`, `export_cellars.py`, `export_upper.py`: the earlier floors.
- Run them from this folder (`cd tools/art`). Python 3.12 or newer (the scripts use f-strings that older
  versions can't read; on Matt's PC plain `python` is 3.10, so use the Python 3.13 install), no extra packages.
- For a new floor, start a `gen24.py` that runs `gen23.py`'s helpers the same way, add the new rooms'
  walls and pieces, and write an `export_*.py` for it.

Some older scripts also write design mockups to a folder outside the repo when run on their own; the
export scripts don't need those.

## `screens/`: look at the game and play it

Node scripts using Playwright (`npm install -g playwright` and `npx playwright install chromium` once).
They serve the built game from `web/target/site` (build it with `mvn -q package -DskipTests -pl web -am`).

- `node tools/screens/play.js 501 650`: plays each level with its intended solution and says whether the
  mouse escapes; saves a screenshot.
- `node tools/screens/room.js 501`: a tall screenshot of the room map that level 501 is in.
- `node tools/screens/spots.js`: measures the level spots on every room map and lists any two closer than 48 room units.
- `node tools/screens/card.js 501`: the level with its how-to card, then the board.

Screenshots go to `tools/screens/out/` (not committed). Set `SITE` to serve another folder, and `CHROME`
to use a particular Chrome.
