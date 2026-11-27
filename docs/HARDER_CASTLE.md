# A harder, less repetitive castle (before launch)

Matt's playtest, November 2026: 801–830 took under 10 minutes and 1001–1025 about 15, with few hints. The
upper castle is too easy for puzzle fans. It also felt repetitive: once he learned to stop a runner (a dog
halting a lion before it passes a spoiler), he kept seeing it.

The numbers back this up:
- Average `Difficulty.score` sits at about 12 from level 200 all the way to 1100, so the castle stops getting
  harder.
- No level asks for more than 3 animals.
- In 801–1100, `Move.STOP` is in about 1 level in 5, often several close together (1011, 1016, 1018, 1023,
  1025).
- CATCH or `withCatches` is in a third to a half of each room.

There are no real players yet, so changing levels now costs nobody their progress. This work runs
alongside the App Store steps, in its own pull requests.

## What Matt picked

1. **Placements with no clue:** more animals that go on squares touching nothing on the board.
2. **Longer chains:** more animals in the chain before the mouse moves.
3. **Two tricks in one puzzle:** for example a frozen animal plus a waiting runner, or a stop plus a swerve.
4. **New techniques:**
   - a freeze on purpose (your animal pins a spoiler between two animals it fears);
   - a standoff on purpose (two animals heading for the same square, so neither moves);
   - two chains that must meet in time;
   - the mouse turned two or three times on its way;
   - the elephant-fears-mouse loop as a puzzle;
   - a placed animal that clears a path for another.
5. **Timing puzzles:** the right square isn't enough; the animal has to arrive at the right moment.
6. **Red herrings:** a board animal that looks important but plays no part in the solution. This relaxes
   the checker's clutter rule, so only allow it on purpose, in recipes that ask for it, and keep the
   solution unique.
7. **More than one way the chain could start:** only one of them works, so the obvious first move is wrong.
8. **A rising curve:** each floor harder than the last, instead of flat at about 12 from level 200.
9. **Fewer breather levels** on the upper floors, but keep the easy warm-up levels after each new piece
   (turn tiles at 501, mousetraps at 801, trapdoors at 951).
10. **Real flame levels and bosses:** the hardest recipes the level maker can build, not just the hardest
    of an ordinary batch.
11. **Limits on repeats:** no single technique in more than about 1 level in 8–10, and never the same
    technique within 3 levels of itself. When choosing among candidates, mark down solutions that repeat
    the techniques of the last few levels, like the existing hand-animal penalty.

Not picked for now: 4 or more animals to place (build time unknown), a spare animal in your hand (it
changes a core rule), and expert extras like stars or a daily puzzle.

## How to do it

1. **Tag the techniques.** Tag every level's intended solution by the techniques it uses: swerve,
   freeze-release, waiting runner, catch, stop, lane blocker cleared, wrap-around, standoff, an animal
   placed touching nothing, trap sprung first, steer round a trap, trapdoor, turn tile, and the new ones as
   they're added. Report how often each appears per room, with the STOP and CATCH counts called out.
2. **Dry run the new techniques and combinations** (points 1–7). Use `LevelsCli probe`, and report build
   time and `Difficulty.score` for each. Drop anything that can't build in about a minute.
3. **Propose the curve to Matt** as a table by room, and wait for his OK:
   - Levels 1–200 and the warm-ups stay as they are.
   - From about 200 up, the average climbs steadily from about 12 to about 16–18 by the Tower top.
   - Show the share of each technique per room.
4. **Rebuild floor by floor,** one pull request per floor or two:
   - Keep each room's look, its names (rename where a puzzle changes, 20 characters at most and none
     repeated), its walls, traps and trapdoors at about the same rates, and its boss.
   - Flames come from `LevelsCli hard --write`.
   - Run all the usual checks.
   - Include the technique counts before and after.
