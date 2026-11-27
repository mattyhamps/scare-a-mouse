# Getting Mouse in Hole into the App Store

The castle is finished (levels 1–1100). This file is the plan for shipping it as an iPhone app, as soon as
possible. Work through the steps in order, one pull request each (step 1 may need two). Each step says what
to build and how to check it. Ask Matt before any choice that changes how the game looks or plays, and
show screenshots of visual changes first, as usual.

## Decisions (Matt, November 2026)

- **Name:** the game is called **Mouse in Hole** everywhere players see it (store listing, app name, title
  bar, cards). The repo and the code keep the name Scare-a-Mouse. Keep "CastleMouse" and "Castle Mouse"
  out of everything.
- **Who it's for:** puzzle fans aged about 15–45. Game text stays plain and friendly. It isn't made for
  young children, so it doesn't go in Apple's Kids category.
- **Publisher:** Matt publishes as an individual, so his legal name shows as the seller. If the game takes
  off, he can form an LLC later and convert the account; nothing here should depend on the seller name.
- **Builds:** Matt has only occasional time on a Mac. iOS builds run on a cloud Mac (GitHub Actions macOS
  runners or Codemagic) and upload to TestFlight. Matt tests on his iPhone.
- **How the game earns:**
  - **Hints cost cheese:** 3 for the shaded area, 3 more for the exact square (one animal fully shown = 6).
  - **New players start with 0 cheese.** The first levels are easy, so everyone has about 20 by level 20.
  - **Earning:** 1 per first solve with no hints, 3 on a boss, and 2 for clearing a room. Flame levels
    still show that they're extra hard (the flame on the map, by the level number and in the tip) but pay
    the same 1 cheese as any other level (Matt). Using any hint on a level means that level earns nothing.
  - **A hint by ad is always there.** When a player can't afford a hint, the hint button offers "Watch an ad
    for this hint". The ad gives that one hint, never cheese. If no ad can load (offline, or no ad to show),
    give the hint anyway.
  - **Rewarded ads only:** never a forced ad between levels.
  - **Cheese packs** (consumable in-app purchases) are how players skip the ads: Wedge (30 cheese, $0.99),
    Wheel (110, $2.99), Cheese cellar (250, $4.99).
  - **A one-time starter offer** the first time a player runs short: 60 cheese for $0.99, shown once.
  - **No "remove ads" purchase and no unlimited hints:** either would make cheese worthless.
  - **Version 1.0 ships with cheese packs.** Rewarded ads come in 1.1, soon after.
- **Ads:** non-personalized at launch, so there's no tracking pop-up. Google's consent screen is shown to
  EU and UK players.
- **Difficulty:** the castle is made harder and more varied before launch (`docs/HARDER_CASTLE.md`). After
  launch, use player stats to find and fix any level that's too hard.

## Step 1: feel like a phone app (no Capacitor yet)

1. **Rename to Mouse in Hole.** Do it in every place players see: the top bar, the page title, the
   how-to-play cards, the win and finale text, the README's description, the tester link's thank-you
   screen.
2. **The level screen fits a phone without scrolling.** That's the header, tip, board, animal tray and the
   Hint, Reset and Go buttons. Check at 390×664 (Matt's iPhone browser) and 360×640. Shrink the board
   rather than the text, as with the page limits elsewhere.
3. **The floor-map pop-up shows its bottom buttons** ("Royal floor", "Upstairs") without clipping, and the
   "coming soon" label shows both words.
4. **App feel:**
   - no pinch or double-tap zoom;
   - no page bounce or text selection while playing;
   - the notch and home bar respected (safe areas);
   - "Reset progress (testing)" shown only in developer mode.
5. **Hints and cheese** (from the decisions above):
   - `HINT_PRICE` becomes 3 and 3, and new players start with 0 cheese.
   - Flame levels pay 1 cheese like any other level: drop the extra cheese, and the "Solve it without hints
     for 2 cheese" part of the flame tip. The flame still marks the level as extra hard.
   - Add a line to the how-to-play cards: "Stuck? Spend cheese on a hint. You earn cheese by solving
     levels without hints."
   - Keep any price wording in cards and tips correct.
   - In the hint code, leave one clear place where "Watch an ad for this hint" will go when the player
     can't afford a hint. For now it shows the "not enough cheese" message.
6. **A screenshot check** in `tools/screens` that fails if the level screen needs scrolling at 360×640.

Check: before and after screenshots at both sizes (level screen, floor map, a card); `mvn -B verify`;
`node tools/screens/names.js`.

## Step 2: wrap it with Capacitor

1. **An iOS app with Capacitor** around the built site (`web/target/site`). All levels, art and sounds are
   bundled inside the app, and nothing is loaded from the website, so it works offline. Apple rejects
   apps that feel like a repackaged website (guideline 4.2).
2. **Saved progress moves to native storage** (Capacitor Preferences): solved levels, hints and cheese.
   Browser storage can be wiped by iOS, and players will pay for cheese. On first launch, copy anything
   already in browser storage across.
3. **App icon and launch screen:** show Matt a few icon ideas first.
4. **Cloud builds:**
   - A GitHub Actions workflow on a macOS runner (or Codemagic) builds and signs the app, then uploads it
     to TestFlight.
   - Signing uses an App Store Connect API key kept in GitHub secrets. Never put keys in the repo.
   - Write down the one-time setup Matt has to do (Apple Developer account, App Store Connect app record,
     API key) in `docs/APP_STORE.md`, step by step.
5. **The website version keeps working as it is.**

Check: the app runs offline on Matt's iPhone through TestFlight, progress survives closing the app and
restarting the phone, and the web version is unchanged.

## Step 3: native touches

1. **Game Center achievements:** for example clearing each floor, the first flame level, the first boss,
   and reaching the top. Show Matt the list first. A leaderboard is optional.
2. **Haptics:** a light tap when placing an animal, a snap when a trap springs, a happy buzz when the mouse
   escapes. Respect the phone's settings.
3. **Simple, privacy-friendly level stats** (for example TelemetryDeck): which level players stop on and
   where they use hints, with no personal data. This is how too-hard levels get found after launch.

## Step 4: cheese packs (in-app purchases)

1. **RevenueCat** (or StoreKit directly) for the three cheese packs and the starter offer. The packs are
   consumables.
2. **A small cheese shop:** opened from the cheese count and from the "not enough cheese" message. Show
   Matt a mockup first.
3. **Bought cheese goes straight into native storage,** and a purchase is never lost if the app closes
   mid-way.
4. **Store details:** the products in App Store Connect, with names and descriptions.

Check: buy each pack in the sandbox (TestFlight), with the cheese added once and only once.

## Step 5: launch 1.0

1. **App Store listing:**
   - screenshots at the required iPhone sizes, taken with `tools/screens`;
   - a short description, keywords and an age rating;
   - a support URL and a privacy policy page (GitHub Pages is fine). The policy says what's collected:
     purchases, level stats and, from 1.1, ads.
2. **App privacy labels** in App Store Connect to match.
3. **The EU:** decide with Matt whether to sell there at launch. If so, Apple shows a contact address
   (a PO box is fine), phone and email on the EU store.
4. **Submit for review.**
5. **Before launch, from the checklist:** make the repo private and add a license.

## Step 6 (update 1.1): rewarded ads

1. **AdMob rewarded ads,** non-personalized, wired into the place left in step 1: "Watch an ad for this
   hint". The ad gives that one hint. If no ad loads, give the hint anyway.
2. **Google's consent screen** for EU and UK players (AdMob's UMP SDK).
3. **An `app-ads.txt` file** on Matt's website.
4. **Update the privacy policy and Apple's privacy labels** for the ads.
