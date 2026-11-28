# The harder castle: what the levels use now, and what can be built

Steps 1 and 2 of `docs/HARDER_CASTLE.md`, done before rebuilding anything. Nothing in `data/` changed.
Made with `LevelsCli techniques` (the tags) and `LevelsCli trial` (the dry run); both can be run again.

## Step 1: the techniques each room uses

Each level's intended solution is played in the engine and tagged by what actually happens in it (not by its
recipe, so hand-made and older levels count too). The tags agree with the recipes: every level whose recipe asks
for a stop, swerve, freeze-release, waiting runner, lane blocker or wrap-around gets that tag. Some solutions use
a technique without the recipe asking for it, and those count too.

What the tags mean:
- **stop**: your animal stands in a runner's way and halts it for good. **swerve**: a runner passes your animal
  (which it fears) and turns. **catch**: your animal is a link in the chain (a missing link put back), so it runs,
  but only once the chain reaches it.
- **clear path**: your animal holds a runner up for a while, then moves out of its way (timing).
- **freeze-release**, **waiting runner**, **wrap-around** as in the recipes. **lane cleared**: an animal
  standing on the mouse's way gets scared off it first. **standoff**: two animals head for the same square.
- **freeze on purpose**: your animal pins a board animal between two it fears, and it never moves.
- **two starters**: two of your animals each start a chain at once (every lane-blocker level does this).
- **mouse turns 2+**: the mouse changes direction at least twice.

### Levels 201-1100, all together

| Technique | Levels | Share |
|---|---|---|
| lane cleared | 671 | 75% (3 in 4) |
| freeze-release | 504 | 56% |
| catch | 491 | 55% |
| an animal placed touching nothing | 429 | 48% |
| moving start | 369 | 41% |
| stop | 254 | 28% (1 in 3.5) |
| swerve | 253 | 28% |
| walls | 187 | 21% |
| waiting runner | 178 | 20% |
| wrap-around | 109 | 12% |
| turn tile | 67 | 7% |
| trap sprung | 56 | 6% |
| standoff | 34 | 4% |
| trapdoor | 28 | 3% |
| mouse turns 2+ | 19 | 2% |
| steer round a trap | 10 | 1% |
| clear path | 9 | 1% |
| freeze on purpose | 0 | none |

What stands out:
- **The score is flat.** The room average goes up and down between about 10 and 14 from level 200 to 1100, and
  the Tower top (12.7) is no harder than the Ballroom (13.1). The rooms that bring in a new piece (Guard room,
  Royal chambers, Battlements) drop to 8-10.
- **Nobody places more than 3 animals,** anywhere in the castle.
- **Stop is in about 1 level in 3-4,** not just the 1 in 5 its recipes ask for: some solutions stop a runner on
  the way without the recipe asking (the "in play" column below). In the Trophy room 3 recipes ask for a stop
  but 16 solutions use one.
- **Three techniques are in over half the levels:** lane cleared (3 in 4), freeze-release and catch. These
  repeat far more than stop does, and probably feel just as samey.
- **The new ideas are nearly unused:** standoff (4%), the mouse turning twice (2%), clear path (1%), freeze on
  purpose (none).

### Each room

| Room | Avg score | Hand (avg / most) | lane cleared | freeze-release | catch | stop | swerve | waiting runner | wrap-around | standoff | mouse turns 2+ | clear path |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Library (201-230) | 10.9 | 2.2 / 3 | 18 | 17 | 17 | 10 | 9 | 7 |  |  |  |  |
| Study (231-260) | 11.4 | 2.3 / 3 | 21 | 11 | 22 | 6 | 11 | 3 |  |  |  |  |
| Great hall (261-290) | 11.7 | 2.3 / 3 | 21 | 15 | 22 | 6 | 10 | 5 |  | 1 |  |  |
| Ballroom (291-320) | 13.1 | 2.5 / 3 | 24 | 18 | 19 | 8 | 15 | 9 | 4 |  | 2 |  |
| Gallery (321-350) | 13.2 | 2.6 / 3 | 27 | 20 | 18 | 12 | 12 | 5 | 4 | 2 | 2 |  |
| Chapel (351-390) | 11.3 | 2.3 / 3 | 27 | 28 | 23 | 11 | 11 | 4 | 6 | 4 | 1 |  |
| Secret passage (391-420) | 11.3 | 2.2 / 3 | 24 | 17 | 15 | 4 | 9 | 2 | 4 | 2 |  |  |
| Map room (421-460) | 13.1 | 2.5 / 3 | 33 | 29 | 20 | 12 | 13 | 11 | 7 | 2 |  |  |
| Armory (461-500) | 13.7 | 2.8 / 3 | 38 | 26 | 22 | 9 | 12 | 12 | 6 | 3 |  | 1 |
| Guard room (501-530) | 9.4 | 2.0 / 3 | 17 | 15 | 12 | 6 | 4 | 3 | 2 | 2 |  |  |
| Toy room (531-560) | 11.1 | 2.2 / 3 | 22 | 17 | 14 | 7 | 6 | 5 | 6 | 1 | 1 |  |
| Hall of mirrors (561-590) | 12.4 | 2.4 / 3 | 25 | 21 | 16 | 12 | 10 | 3 | 2 |  |  | 1 |
| Bathhouse (591-620) | 13.1 | 2.6 / 3 | 26 | 21 | 19 | 6 | 9 | 7 | 8 |  | 2 |  |
| Trophy room (621-650) | 14.3 | 2.8 / 3 | 28 | 19 | 17 | 16 | 13 | 13 | 3 | 1 | 1 | 1 |
| Treasury (651-680) | 12.3 | 2.3 / 3 | 21 | 22 | 18 | 10 | 9 | 3 | 3 |  |  |  |
| Music room (681-710) | 10.4 | 2.2 / 3 | 22 | 17 | 15 | 10 | 6 | 3 | 6 | 1 |  |  |
| Sewing room (711-740) | 12.1 | 2.4 / 3 | 25 | 21 | 18 | 9 | 8 | 3 | 2 |  | 1 | 1 |
| Guest bedrooms (741-770) | 13.3 | 2.6 / 3 | 27 | 21 | 16 | 5 | 11 | 8 | 8 |  | 1 | 1 |
| Clock tower (771-800) | 14.4 | 2.8 / 3 | 28 | 19 | 19 | 6 | 14 | 9 | 3 | 2 | 1 | 2 |
| Royal chambers (801-830) | 9.9 | 2.0 / 3 | 13 | 12 | 16 | 7 | 6 | 3 | 2 |  | 2 |  |
| Wardrobe (831-860) | 11.6 | 2.3 / 3 | 19 | 17 | 19 | 9 | 8 | 6 | 5 | 2 | 1 | 1 |
| Sitting room (861-890) | 11.4 | 2.2 / 3 | 20 | 14 | 13 | 10 | 9 | 7 | 4 | 1 | 1 |  |
| Tower stairs (891-920) | 11.2 | 2.3 / 3 | 20 | 10 | 14 | 8 | 6 | 6 | 3 | 1 | 2 | 1 |
| Throne room (921-950) | 11.6 | 2.4 / 3 | 22 | 12 | 15 | 12 | 5 | 5 | 4 | 2 |  |  |
| Battlements (951-975) | 8.4 | 1.8 / 3 | 10 | 7 | 10 | 5 | 2 | 5 | 2 | 1 | 1 |  |
| Aviary (976-1000) | 11.1 | 2.2 / 3 | 16 | 11 | 13 | 7 | 4 | 5 | 3 |  |  |  |
| Watchtower (1001-1025) | 12.1 | 2.3 / 3 | 18 | 13 | 12 | 9 | 5 | 6 | 3 | 1 |  |  |
| Belfry (1026-1050) | 12.1 | 2.2 / 3 | 19 | 12 | 12 | 9 | 6 | 8 | 3 | 1 |  |  |
| Crown vault (1051-1075) | 12.2 | 2.4 / 3 | 20 | 11 | 12 | 6 | 6 | 6 | 4 | 3 |  |  |
| Tower top (1076-1100) | 12.7 | 2.4 / 3 | 20 | 11 | 13 | 7 | 4 | 6 | 2 | 1 |  |  |

<details><summary>Every technique, every room (the full table from <code>LevelsCli techniques --from 201</code>)</summary>

| Room | Levels | Avg score | Avg hand | Max hand | stop | swerve | catch | clear path | freeze-release | waiting runner | lane cleared | wrap-around | standoff | freeze on purpose | two starters | blind placement | mouse turns 2+ | trap sprung | steer round trap | trapdoor | turn tile | walls | moving start | Repeats within 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Library (201-230) | 30 | 10.9 | 2.2 | 3 | 10 | 9 | 17 |  | 17 | 7 | 18 |  |  |  | 7 | 15 |  |  |  |  |  | 6 | 15 | freeze-release 14, stop 6, swerve 4, catch 16, lane cleared 16, two starters 2, waiting runner 3 |
| Study (231-260) | 30 | 11.4 | 2.3 | 3 | 6 | 11 | 22 |  | 11 | 3 | 21 |  |  |  | 12 | 22 |  |  |  |  |  | 6 | 16 | freeze-release 7, lane cleared 20, catch 21, swerve 8, two starters 11, stop 2 |
| Great hall (261-290) | 30 | 11.7 | 2.3 | 3 | 6 | 10 | 22 |  | 15 | 5 | 21 |  | 1 |  | 10 | 21 |  |  |  |  |  | 6 | 15 | catch 21, freeze-release 13, lane cleared 20, two starters 6, waiting runner 2, swerve 5 |
| Ballroom (291-320) | 30 | 13.1 | 2.5 | 3 | 8 | 15 | 19 |  | 18 | 9 | 24 | 4 |  |  | 9 | 17 | 2 |  |  |  |  | 5 | 17 | catch 16, freeze-release 16, lane cleared 23, swerve 12, two starters 7, waiting runner 4, stop 3 |
| Gallery (321-350) | 30 | 13.3 | 2.6 | 3 | 12 | 12 | 18 |  | 20 | 5 | 27 | 4 | 2 |  | 13 | 14 | 2 |  |  |  |  | 6 | 16 | freeze-release 18, lane cleared 26, swerve 10, two starters 11, catch 17, stop 10 |
| Chapel (351-390) | 40 | 11.3 | 2.3 | 3 | 11 | 11 | 23 |  | 28 | 4 | 27 | 6 | 4 |  | 15 | 21 | 1 |  |  |  |  | 9 | 18 | catch 20, freeze-release 26, swerve 7, lane cleared 25, two starters 12, standoff 1, waiting runner 1, stop 6, wrap-around 2 |
| Secret passage (391-420) | 30 | 11.3 | 2.2 | 3 | 4 | 9 | 15 |  | 17 | 2 | 24 | 4 | 2 |  | 15 | 11 |  |  |  |  |  | 25 | 10 | freeze-release 16, lane cleared 23, catch 13, two starters 14, waiting runner 1, swerve 5 |
| Map room (421-460) | 40 | 13.1 | 2.6 | 3 | 12 | 13 | 20 |  | 29 | 11 | 33 | 7 | 2 |  | 19 | 17 |  |  |  |  |  | 8 | 16 | freeze-release 28, lane cleared 32, catch 16, stop 7, two starters 15, swerve 8, wrap-around 3, waiting runner 5 |
| Armory (461-500) | 40 | 13.7 | 2.8 | 3 | 9 | 12 | 22 | 1 | 26 | 12 | 38 | 6 | 3 |  | 25 | 13 |  |  |  |  |  | 9 | 13 | freeze-release 24, lane cleared 37, catch 20, two starters 22, waiting runner 9, wrap-around 3, swerve 8, stop 3 |
| Guard room (501-530) | 30 | 9.4 | 2.0 | 3 | 6 | 4 | 12 |  | 15 | 3 | 17 | 2 | 2 |  | 12 | 9 |  |  |  |  | 15 | 4 | 7 | turn tile 12, catch 11, freeze-release 14, lane cleared 16, two starters 11, waiting runner 1, swerve 2, stop 4 |
| Toy room (531-560) | 30 | 11.1 | 2.2 | 3 | 7 | 6 | 14 |  | 17 | 5 | 22 | 6 | 1 |  | 15 | 12 | 1 |  |  |  | 4 | 19 | 10 | stop 3, lane cleared 21, two starters 13, catch 12, freeze-release 16, wrap-around 3, swerve 2, waiting runner 2 |
| Hall of mirrors (561-590) | 30 | 12.5 | 2.4 | 3 | 12 | 10 | 16 | 1 | 21 | 3 | 25 | 2 |  |  | 13 | 11 |  |  |  |  | 5 | 15 | 11 | lane cleared 24, swerve 7, catch 14, freeze-release 20, two starters 10, stop 8, waiting runner 1 |
| Bathhouse (591-620) | 30 | 13.1 | 2.6 | 3 | 6 | 9 | 19 |  | 21 | 7 | 26 | 8 |  |  | 18 | 12 | 2 |  |  |  | 5 | 3 | 9 | catch 18, lane cleared 25, swerve 4, waiting runner 2, freeze-release 20, wrap-around 4, stop 2, two starters 16 |
| Trophy room (621-650) | 30 | 14.3 | 2.8 | 3 | 16 | 13 | 17 | 1 | 19 | 13 | 28 | 3 | 1 |  | 17 | 11 | 1 |  |  |  | 5 | 7 | 12 | waiting runner 9, lane cleared 27, two starters 14, swerve 11, freeze-release 18, stop 15, catch 16, wrap-around 2, turn tile 1 |
| Treasury (651-680) | 30 | 12.4 | 2.3 | 3 | 10 | 9 | 18 |  | 22 | 3 | 21 | 3 |  |  | 12 | 19 |  |  |  |  | 5 | 6 | 16 | catch 17, freeze-release 21, swerve 5, lane cleared 19, stop 8, two starters 9 |
| Music room (681-710) | 30 | 10.4 | 2.2 | 3 | 10 | 6 | 15 |  | 17 | 3 | 22 | 6 | 1 |  | 15 | 11 |  |  |  |  | 4 | 6 | 11 | stop 6, lane cleared 21, catch 12, freeze-release 16, wrap-around 3, two starters 13, waiting runner 1, swerve 1 |
| Sewing room (711-740) | 30 | 12.1 | 2.4 | 3 | 9 | 8 | 18 | 1 | 21 | 3 | 25 | 2 |  |  | 13 | 11 | 1 |  |  |  | 5 | 6 | 13 | catch 17, lane cleared 24, swerve 5, freeze-release 20, two starters 10, stop 6, waiting runner 2 |
| Guest bedrooms (741-770) | 30 | 13.3 | 2.6 | 3 | 5 | 11 | 16 | 1 | 21 | 8 | 27 | 8 |  |  | 18 | 12 | 1 |  |  |  | 5 | 6 | 10 | lane cleared 26, swerve 6, catch 15, waiting runner 5, freeze-release 20, wrap-around 4, stop 1, two starters 16 |
| Clock tower (771-800) | 30 | 14.4 | 2.8 | 3 | 6 | 14 | 19 | 2 | 19 | 9 | 28 | 3 | 2 |  | 17 | 12 | 1 |  |  |  | 4 | 6 | 12 | waiting runner 6, lane cleared 27, two starters 14, stop 3, swerve 12, freeze-release 18, catch 18, wrap-around 2 |
| Royal chambers (801-830) | 30 | 9.9 | 2.0 | 3 | 7 | 6 | 16 |  | 12 | 3 | 13 | 2 |  |  | 8 | 18 | 2 | 12 | 2 |  |  | 5 | 14 | mouse turns 2+ 1, steer round trap 1, trap sprung 8, catch 14, stop 4, swerve 2, freeze-release 10, lane cleared 12, two starters 6, waiting runner 1 |
| Wardrobe (831-860) | 30 | 11.6 | 2.3 | 3 | 9 | 8 | 19 | 1 | 17 | 6 | 19 | 5 | 2 |  | 9 | 17 | 1 | 6 |  |  |  |  | 16 | catch 18, lane cleared 18, stop 6, two starters 5, freeze-release 15, swerve 2 |
| Sitting room (861-890) | 30 | 11.4 | 2.2 | 3 | 10 | 9 | 13 |  | 14 | 7 | 20 | 4 | 1 |  | 11 | 16 | 1 | 5 | 1 |  | 2 | 6 | 13 | freeze-release 11, lane cleared 19, two starters 8, swerve 5, catch 10, trap sprung 2, stop 6, waiting runner 2, wrap-around 1 |
| Tower stairs (891-920) | 30 | 11.2 | 2.3 | 3 | 8 | 6 | 14 | 1 | 10 | 6 | 20 | 3 | 1 |  | 12 | 16 | 2 | 5 | 1 |  | 2 | 6 | 13 | stop 5, lane cleared 19, two starters 10, mouse turns 2+ 1, freeze-release 6, catch 12, waiting runner 2, swerve 1 |
| Throne room (921-950) | 30 | 11.6 | 2.4 | 3 | 12 | 5 | 15 |  | 12 | 5 | 22 | 4 | 2 |  | 15 | 14 |  | 5 | 1 |  |  | 6 | 11 | lane cleared 21, two starters 12, catch 13, stop 10, freeze-release 9, wrap-around 1, swerve 1, trap sprung 1 |
| Battlements (951-975) | 25 | 8.4 | 1.8 | 3 | 5 | 2 | 10 |  | 7 | 5 | 10 | 2 | 1 |  | 7 | 9 | 1 | 2 | 2 | 9 | 1 |  | 6 | trapdoor 5, catch 8, lane cleared 8, two starters 5, freeze-release 5, swerve 1, waiting runner 2, stop 2 |
| Aviary (976-1000) | 25 | 11.1 | 2.2 | 3 | 7 | 4 | 13 |  | 11 | 5 | 16 | 3 |  |  | 10 | 13 |  | 5 |  | 3 | 1 |  | 9 | catch 10, lane cleared 14, freeze-release 8, wrap-around 1, two starters 7, waiting runner 3, stop 4, swerve 1, trap sprung 1 |
| Watchtower (1001-1025) | 25 | 12.1 | 2.3 | 3 | 9 | 5 | 12 |  | 13 | 6 | 18 | 3 | 1 |  | 10 | 15 |  | 3 | 1 | 4 | 1 |  | 10 | freeze-release 11, lane cleared 17, catch 10, two starters 8, stop 7, swerve 2, wrap-around 1, waiting runner 4, trap sprung 1 |
| Belfry (1026-1050) | 25 | 12.1 | 2.2 | 3 | 9 | 6 | 12 |  | 12 | 8 | 19 | 3 | 1 |  | 10 | 14 |  | 4 |  | 4 | 1 |  | 12 | stop 5, freeze-release 9, lane cleared 18, catch 10, two starters 8, waiting runner 3, swerve 2 |
| Crown vault (1051-1075) | 25 | 12.2 | 2.4 | 3 | 6 | 6 | 12 |  | 11 | 6 | 20 | 4 | 3 |  | 14 | 13 |  | 4 | 1 | 4 | 1 |  | 9 | catch 9, lane cleared 19, two starters 11, wrap-around 2, swerve 2, freeze-release 10, waiting runner 2, standoff 1, stop 3 |
| Tower top (1076-1100) | 25 | 12.7 | 2.4 | 3 | 7 | 4 | 13 |  | 11 | 6 | 20 | 2 | 1 |  | 13 | 13 |  | 5 | 1 | 4 | 1 | 6 | 9 | stop 2, lane cleared 19, two starters 10, catch 11, freeze-release 10, waiting runner 2, swerve 1, trap sprung 2 |

</details>

### STOP and CATCH

"Asked" is how many levels' recipes ask for one; "in play" is how many solutions use one at all.

| Room | STOP asked | STOP in play | CATCH asked | CATCH in play | Levels asking for a stop |
|---|---|---|---|---|---|
| Library | 7 | 10 | 17 | 17 | 202, 203, 211, 212, 223, 225, 226 |
| Study | 5 | 6 | 20 | 22 | 231, 238, 247, 257, 259 |
| Great hall | 5 | 6 | 19 | 22 | 265, 269, 273, 278, 282 |
| Ballroom | 7 | 8 | 14 | 19 | 291, 296, 300, 302, 306, 312, 316 |
| Gallery | 4 | 12 | 16 | 18 | 326, 328, 333, 335 |
| Chapel | 8 | 11 | 23 | 23 | 356, 361, 367, 371, 374, 381, 382, 387 |
| Secret passage | 3 | 4 | 10 | 15 | 392, 403, 418 |
| Map room | 7 | 12 | 20 | 20 | 425, 427, 429, 437, 445, 452, 457 |
| Armory | 3 | 9 | 17 | 22 | 475, 487, 489 |
| Guard room | 3 | 6 | 12 | 12 | 517, 521, 524 |
| Toy room | 5 | 7 | 11 | 14 | 531, 532, 537, 542, 553 |
| Hall of mirrors | 5 | 12 | 13 | 16 | 568, 575, 577, 579, 587 |
| Bathhouse | 3 | 6 | 14 | 19 | 595, 602, 607 |
| Trophy room | 3 | 16 | 14 | 17 | 625, 637, 639 |
| Treasury | 5 | 10 | 18 | 18 | 656, 661, 667, 671, 674 |
| Music room | 5 | 10 | 11 | 15 | 681, 682, 687, 692, 703 |
| Sewing room | 5 | 9 | 13 | 18 | 718, 725, 727, 729, 737 |
| Guest bedrooms | 3 | 5 | 14 | 16 | 745, 752, 757 |
| Clock tower | 3 | 6 | 14 | 19 | 775, 787, 789 |
| Royal chambers | 5 | 7 | 15 | 16 | 804, 807, 815, 817, 823 |
| Wardrobe | 5 | 9 | 18 | 19 | 835, 837, 848, 849, 857 |
| Sitting room | 5 | 10 | 9 | 13 | 862, 873, 875, 878, 890 |
| Tower stairs | 6 | 8 | 10 | 14 | 891, 893, 903, 905, 911, 914 |
| Throne room | 6 | 12 | 8 | 15 | 928, 929, 931, 938, 944, 948 |
| Battlements | 3 | 5 | 7 | 10 | 960, 968, 974 |
| Aviary | 5 | 7 | 8 | 13 | 980, 983, 987, 998, 999 |
| Watchtower | 5 | 9 | 9 | 12 | 1011, 1016, 1018, 1023, 1025 |
| Belfry | 6 | 9 | 8 | 12 | 1026, 1027, 1035, 1038, 1042, 1049 |
| Crown vault | 4 | 6 | 9 | 12 | 1059, 1067, 1072, 1073 |
| Tower top | 5 | 7 | 6 | 13 | 1076, 1082, 1090, 1094, 1098 |

## Step 2: the dry run

`LevelsCli trial` tries to build one 10x10 level of each kind, using all 12 cores, and saves nothing. The new
techniques were tried by building from familiar recipes and keeping only levels whose solution really uses
the technique. "Score" is `Difficulty.score`: today's room averages are 10-14 and the bosses about 19.

| Puzzle | Hand | Built in | Score | Blind | Chain | Techniques |
|---|---|---|---|---|---|---|
| freeze-release + waiting runner | 1 | nothing in 90s | | | | |
| freeze-release + waiting runner, 1 blocker | 2 | nothing in 90s | | | | |
| moving: swerve + stop + catch | 3 | nothing in 94s | | | | |
| moving: swerve + catch + catch | 3 | nothing in 94s | | | | |
| moving: two swerves, freeze-release | 2 | 0.6s | 14.5 | 2 | 5 | swerve, freeze-release, blind placement, moving start |
| lion chain, 2 missing links | 3 | nothing in 91s | | | | |
| elephant chain, 2 missing links | 3 | nothing in 91s | | | | |
| wrap-around + freeze-release | 1 | 0.1s | 5.0 | 0 | 0 | freeze-release, wrap-around |
| wrap-around, 1 blocker, 1 catch | 3 | 6.2s | 11.0 | 0 | 0 | catch, lane cleared, wrap-around, two starters |
| walls + steer round traps | 1 | nothing in 15 min | | | | |
| trapdoor + freeze-release + catch | 2 | 0.7s | 12.5 | 1 | 4 | catch, freeze-release, blind placement, trapdoor |
| 4: lion, 3 lane blockers | 4 | 24.6s | 18.5 | 0 | 9 | waiting runner, lane cleared, two starters |
| 4: elephant, 3 lane blockers | 4 | 19.7s | 17.5 | 0 | 11 | stop, lane cleared, two starters |
| 4: elephant, 2 blockers, waiting runner, 1 catch | 4 | 42.0s | 19.0 | 0 | 6 | catch, clear path, waiting runner, lane cleared, two starters |
| 4: elephant freeze-release, 1 blocker, 2 catches | 4 | nothing in 92s | | | | |
| 4: the same, walls allowed | 4 | 892s | 21.0 | 1 | 6 | swerve, catch, freeze-release, lane cleared, two starters, blind placement, walls |
| 4: elephant freeze-release, 2 blockers, 1 trap to spring | 4 | 14.4s | 22.5 | 1 | 9 | stop, catch, freeze-release, lane cleared, two starters, blind placement, trap sprung |
| 4: moving, 2 blockers, swerve + stop | 4 | nothing in 100s | | | | |
| 5: elephant, 3 blockers, 1 catch | 5 | nothing in 20 min | | | | |
| 5: the same, walls allowed | 5 | nothing in 15 min | | | | |
| 5: lion, 4 lane blockers, walls allowed | 5 | nothing in 15 min | | | | |
| 5: elephant freeze-release, 2 blockers, 2 catches | 5 | nothing in 100s | | | | |
| 5: elephant, 2 blockers, 2 traps to spring | 5 | nothing in 15 min | | | | |
| new: freeze on purpose | 3 | nothing in 92s | | | | |
| new: standoff | 3 | nothing in 92s | | | | |
| two starters at once | 3 | 5.9s | 12.0 | 0 | 8 | stop, lane cleared, two starters |
| new: mouse turned twice | 3 | nothing in 92s | | | | |
| new: mouse turned twice (turn tile) | 2 | nothing in 90s | | | | |
| new: your animal clears a path (timing) | 3 | 7.9s | 12.0 | 0 | 4 | catch, clear path, waiting runner, lane cleared, two starters |
| new: elephant-mouse loop, 3 to place | 3 | 9.8s | 16.0 | 1 | 0 | catch, freeze-release, lane cleared, wrap-around, two starters, blind placement |

### Checking 4 and 5 animals: before and after

Checking a level means finding every winning placement (to make sure there's only one), several times over:
for the whole hand, for the hand with each animal left out, and for the board with each piece taken away.
Trying every square for every animal is about 14 million placements for a hand of 4 (two pairs) and 1.2
billion for 5, and more when the animals all differ. Measured on Matt's PC, one search of every placement:

| Hand | One full search, before | One search, after (`FrontierSearch`) | A whole check of a candidate, after |
|---|---|---|---|
| 3 | 0.5-3 s | 0.15-0.8 s | about 1 s (3-animal levels keep the old search) |
| 4 | about 50 s (4 different animals: about 4 times that) | about 1 s | 0.3-3 s on average, 12 s at worst |
| 5 | about 1 hour | 3-23 s (80 s at worst) | 6-80 s |

`FrontierSearch` only tries squares the run actually reaches, adding your animals in the order they're first
touched, and gives the same answers as trying everything: `FrontierSearchTest` compares the two on 5,502
searches (real levels, the same levels with a piece taken away, and smaller hands), and they also matched on
4-animal hands. It's only used for hands of 4 or more, so today's levels are checked exactly as before.

**4 animals are now practical:** 4 of 6 kinds built in 14-42 s, and a fifth once walls were allowed (15
minutes), scoring 17.5-22.5 (today's bosses score about 19). **5 animals aren't yet:** nothing built in 15-20 minutes for any 5-animal kind. The searches finish; the
trouble is that the builder's 5-animal candidates almost always have a second solution, and it has no way yet
to close those off except walls, which didn't help either. Making 5 work needs builder changes (designing the
chain so fewer squares give another way to win), not just a faster checker.

### What the builder can't make yet

- **Freeze-release with a waiting runner** (two tricks in one chain): the builder never produces one at all (0 of
  40 million tries). It needs to learn to put both in one chain.
- **Two missing links** (lion or elephant chain), **three moves in a moving level**: plenty of candidates (tens of
  thousands in 15 s), but every one has more than one solution. Same fix as 5 animals: the builder has to close
  off the other ways.
- **Freeze on purpose, a standoff, the mouse turning twice:** never turned up in levels built from familiar
  recipes. Each needs the builder to design for it on purpose.
- **Walls plus steering round traps:** a handful of candidates, none passed in 15 minutes.

Points 6 and 7 of the plan (red herrings and more than one way to start) weren't tried: both need new checker
rules first (a red herring breaks today's clutter rule on purpose).

## Step 3: a proposed curve

**Matt's decision (27 November 2026): option B, the steeper curve, with 4-animal levels anywhere they fit,
not only flames and bosses.** He wants more difficulty across the board. 4-animal levels start turning up in
ordinary levels as the curve rises and are common on the upper floors; breathers and the warm-ups after a
new piece stay easy. Flame levels and bosses sit above the line (4 animals, and 5 once the builder can make
them).

Levels 1-200 and the warm-ups after each new piece stay as they are. From 201 the room average climbs steadily
from about 12. About 1 level in 9 is a breather that stays easy (score about 7) wherever it is, so the other
levels climb a little faster than the average. The number in brackets is what the other levels average.

Two heights for the top:
- **Option A, up to 16:** the upper floors are mostly 3-animal levels with two tricks, with 4 animals for flame
  levels and bosses. Today's 3-animal levels score up to about 19, and 4-animal ones 17.5-22.5, so this can be
  built with what works now plus the techniques the builder learns.
- **Option B, up to 17.5:** the Towers and roof average about 18.5 outside the breathers, as hard as today's
  bosses. That means 4 animals in most upper levels, so building takes longer (a few minutes per level).

The rooms that bring in a new piece (Guard room 501, Royal chambers 801, Battlements 951) keep their easy
warm-up levels at the start, so their averages will sit a little under these numbers.

| Room | Now | Option A: top at 16 (others) | Option B: top at 17.5 (others) |
|---|---|---|---|
| Library (201-230) | 10.9 | 12.1 (12.6) | 12.1 (12.7) |
| Study (231-260) | 11.4 | 12.2 (12.8) | 12.3 (12.9) |
| Great hall (261-290) | 11.7 | 12.3 (12.9) | 12.5 (13.1) |
| Ballroom (291-320) | 13.1 | 12.5 (13.1) | 12.6 (13.3) |
| Gallery (321-350) | 13.2 | 12.6 (13.2) | 12.8 (13.5) |
| Chapel (351-390) | 11.3 | 12.8 (13.4) | 13.0 (13.7) |
| Secret passage (391-420) | 11.3 | 12.9 (13.6) | 13.3 (13.9) |
| Map room (421-460) | 13.1 | 13.1 (13.7) | 13.5 (14.2) |
| Armory (461-500) | 13.7 | 13.2 (13.9) | 13.7 (14.5) |
| Guard room (501-530) | 9.4 | 13.4 (14.1) | 13.9 (14.7) |
| Toy room (531-560) | 11.1 | 13.5 (14.3) | 14.1 (14.9) |
| Hall of mirrors (561-590) | 12.4 | 13.7 (14.4) | 14.3 (15.1) |
| Bathhouse (591-620) | 13.1 | 13.8 (14.6) | 14.5 (15.3) |
| Trophy room (621-650) | 14.3 | 13.9 (14.7) | 14.7 (15.5) |
| Treasury (651-680) | 12.3 | 14.1 (14.9) | 14.8 (15.7) |
| Music room (681-710) | 10.4 | 14.2 (15.0) | 15.0 (15.9) |
| Sewing room (711-740) | 12.1 | 14.3 (15.1) | 15.2 (16.1) |
| Guest bedrooms (741-770) | 13.3 | 14.5 (15.3) | 15.4 (16.3) |
| Clock tower (771-800) | 14.4 | 14.6 (15.4) | 15.6 (16.5) |
| Royal chambers (801-830) | 9.9 | 14.7 (15.6) | 15.8 (16.7) |
| Wardrobe (831-860) | 11.6 | 14.9 (15.7) | 15.9 (16.9) |
| Sitting room (861-890) | 11.4 | 15.0 (15.9) | 16.1 (17.1) |
| Tower stairs (891-920) | 11.2 | 15.1 (16.0) | 16.3 (17.3) |
| Throne room (921-950) | 11.6 | 15.3 (16.2) | 16.5 (17.5) |
| Battlements (951-975) | 8.4 | 15.4 (16.5) | 16.7 (18.0) |
| Aviary (976-1000) | 11.1 | 15.5 (16.7) | 16.8 (18.2) |
| Watchtower (1001-1025) | 12.1 | 15.6 (16.8) | 17.0 (18.3) |
| Belfry (1026-1050) | 12.1 | 15.7 (16.9) | 17.1 (18.5) |
| Crown vault (1051-1075) | 12.2 | 15.8 (17.0) | 17.3 (18.7) |
| Tower top (1076-1100) | 12.7 | 15.9 (17.2) | 17.4 (18.8) |

### Limits on repeats

**Decided (Matt, 27 November 2026):** Matt doesn't want to notice puzzle styles repeating, and wants
techniques less common wherever that's possible. The plan, as starting numbers to tighten once the new
techniques exist:
- **Repeats are judged by puzzle style,** not single techniques: the main trick plus the set-up (for example "4
  animals, stop + catch, moving start"). The same style never comes back within about 8 levels.
- **Headline tricks** (stop, swerve, waiting runner, wrap-around, standoff, freeze on purpose, timing, the mouse
  turning, sprung traps): each in at most about 1 level in 8-10, never within 3 levels of itself.
- **Everyday building blocks, cut well down:** lane cleared from 75% to about 40%, catch from 55% to about 40%,
  freeze-release from 56% to about 25%.
- **The builder enforces it:** when choosing among candidates it marks down ones that repeat the styles and
  techniques of the last few levels, and a test fails if a room breaks the limits.

Why not 1 in 8-10 for everything: today lane cleared (75%), freeze-release (56%) and catch (55%) are how most
chains are built, and a hard level uses two or three at once. Holding them to 1 in 10 would leave too few kinds
of puzzle to fill a room, so they're cut as far as the new techniques allow instead.

## Questions for Matt before rebuilding (all decided)

1. ~~How high should the curve go?~~ Decided: option B, 4 animals anywhere they fit (see step 3).
2. ~~Limits on repeats?~~ Decided: see "Limits on repeats" above.
3. ~~Teach the builder first?~~ Decided: yes, the builder first (Matt agreed it's more efficient: the castle is
   rebuilt once instead of twice, the limits need the new techniques to swap in, and the steeper curve needs
   4-5 animals with two tricks, which the builder can't make yet). The question was: Freeze on purpose, standoffs, the mouse turning twice, freeze-release with a
   waiting runner, and 5 animals all need builder work before they can go in levels. Either do that next (one
   pull request, with a new dry run), then rebuild; or start rebuilding the lower floors now with what builds
   today (4 animals, timing, the elephant-mouse loop, trapdoors with tricks) and add the new techniques to the
   upper floors once the builder can make them.

## Teaching the level maker (28 November 2026)

The level maker can now build each new technique Matt picked. Nothing in `data/` changed yet: this is the
builder, a new dry run, and the repeat limits, ready for the rebuild.

**What it learned:**
- **Freeze-release with a waiting runner** in one chain. In a short chain they share a link: the animal the freeze
  releases is the blocker the waiting runner is stuck behind. (Before, the builder never made one: the two need
  5 links one after the other and an elephant chain has 4.)
- **Freeze on purpose** (`withPlaced(PIN)`): a spoiler beside a runner's path with its way out blocked; your animal
  beside it means it's touched by two when the runner passes, so it freezes instead of bolting.
- **Standoff on purpose** (`withPlaced(STANDOFF)`): your animal is scared off by one on the board and reaches a square
  on a runner's way on the same step as the runner, so neither moves. Any kind of animal works for it (the two
  sit diagonally at the standoff), and one the runner scares or fears can't just be used as a plain stop instead.
- **The mouse turning** (`withMouseTurns(n)`): the mouse swerves away from cats beside its run, two or three times.
- **Red herrings and decoy starts** (`withHerrings(h, d)`): the checker allows exactly that many board animals to
  play no part, and nothing else changes (one solution, every animal needed).
- **Closing off shortcuts.** Most failed candidates weren't failing because of a second solution: one of your
  animals wasn't needed (a smaller hand won, often by starting the chain partway along). Walls or mousetraps now
  close those off too, smallest shortcut first. Mousetraps work best: they can sit on a square a runner passes
  over, where a wall would stop it. For pins and standoffs the builder also picks an animal that can't start the
  chain on its own.
- **The "Standoff!" card** (shown to Matt as a screenshot): shown on the first level that needs a standoff, set when the
  castle is rebuilt.
- **Repeat limits** as decided: `LevelsCli make` marks down candidates that repeat a style from the 8 levels before
  or a headline trick from the 3 before; `techniques --limits` lists where each room breaks the limits; rooms are
  added to `Techniques.REBUILT_ROOMS` as they're rebuilt and a test holds them to the limits.

**The dry run** (`LevelsCli trial`, 12 threads; 2 minutes each for the first rows, 5 for the rest):

| Puzzle | Hand | Built in | Score | Blind | Chain | Techniques |
|---|---|---|---|---|---|---|
| freeze-release + waiting runner | 1 | 0.0s | 5.5 | 0 | 3 | freeze-release, waiting runner |
| freeze-release + waiting runner, 1 blocker | 2 | 0.5s | 11.0 | 0 | 6 | freeze-release, waiting runner, lane cleared, two starters |
| freeze on purpose | 2 | nothing in 120s | | | | |
| freeze on purpose, freeze-release | 2 | 1.3s | 8.0 | 0 | 4 | freeze-release, freeze on purpose |
| freeze on purpose, moving | 1 | nothing in 120s | | | | |
| standoff | 2 | nothing in 120s | | | | |
| standoff, waiting runner | 2 | 0.0s | 8.0 | 0 | 4 | waiting runner, standoff |
| standoff, moving | 1 | nothing in 120s | | | | |
| freeze on purpose, walls | 2 | nothing in 120s | | | | |
| freeze on purpose, traps | 2 | nothing in 120s | | | | |
| freeze on purpose, moving, walls | 1 | nothing in 120s | | | | |
| standoff, walls | 2 | nothing in 120s | | | | |
| standoff, traps | 2 | 1.7s | 7.5 | 0 | 5 | standoff, trap sprung |
| standoff, moving, walls | 1 | nothing in 120s | | | | |
| mouse turns twice | 1 | 0.0s | 2.0 | 0 | 4 | mouse turns 2+ |
| mouse turns twice, freeze-release | 1 | 0.0s | 4.5 | 0 | 5 | freeze-release, mouse turns 2+ |
| mouse turns three times | 1 | 0.0s | 1.5 | 0 | 3 | mouse turns 2+ |
| red herring | 1 | 0.0s | 4.0 | 0 | 4 | freeze-release |
| decoy start | 1 | 0.0s | 4.0 | 0 | 4 | freeze-release |
| decoy start + red herring, 1 blocker | 2 | 0.1s | 7.5 | 0 | 7 | stop, lane cleared, two starters |
| 4: pin + standoff, 1 blocker | 4 | nothing in 123s | | | | |
| 4: freeze + wait, 1 blocker, pin | 3 | nothing in 121s | | | | |
| 4: 2 blockers, standoff, mouse turns | 4 | nothing in 123s | | | | |
| lion chain, 2 missing links, walls | 3 | nothing in 300s | | | | |
| lion chain, 2 missing links, traps | 3 | nothing in 303s | | | | |
| 4: moving, 2 blockers, swerve + stop, walls | 4 | nothing in 310s | | | | |
| 5: elephant, 3 blockers, 1 catch, walls | 5 | nothing in 310s | | | | |
| 5: elephant, 3 blockers, 1 catch, traps | 5 | nothing in 310s | | | | |
| 5: lion, 4 lane blockers, walls | 5 | nothing in 310s | | | | |
| 4: pin + standoff, 1 blocker | 4 | nothing in 300s | | | | |
| 4: freeze + wait, 1 blocker, pin | 3 | nothing in 301s | | | | |
| 4: 2 blockers, standoff, mouse turns | 4 | nothing in 301s | | | | |

What it shows:
- **Every new technique builds,** most in seconds: freeze-release with a waiting runner, standoffs (with a waiting
  runner, or closed off with mousetraps), freeze on purpose (with a freeze-release), the mouse turning two or three
  times, red herrings and decoy starts.
- **Their scores look low** (2-11) because `Difficulty.score` doesn't count the new techniques yet: a mouse that
  turns twice scores the same as a plain one-animal level. The score needs updating before the rebuild; it moves
  today's flames, so it goes with the rebuild.
- **Not yet:** 5 animals, two missing links and the hardest 4-animal mixes (pin + standoff, standoff + the mouse
  turning) found nothing in 5 minutes. One 4-animal moving kind that built in 150 s before (swerve + stop, two
  blockers, walls) didn't in this run: closing off now checks every smaller hand, which is slower. These need
  more work: most likely designing the chain so fewer shortcuts exist in the first place, rather than closing them
  off afterwards.
