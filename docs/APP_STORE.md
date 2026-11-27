# Getting Mouse in Hole into the App Store

The castle is finished (levels 1–1100), and it's being made harder before launch (`docs/HARDER_CASTLE.md`,
in its own pull requests). This file is the plan for shipping it as a phone app on **iPhone and Android**,
as soon as possible. Both come from the same Capacitor project; the iPhone launches first and Android follows
(see "Android" below). Work through the steps in order, one pull request each (step 1 may need two). Each step says what
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
- **Platforms:** iPhone and Android, from one Capacitor project around the same web game. The iPhone
  launches first; Android follows once Google's closed test is done (it takes at least two weeks, so start
  it early).
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
  - **Maybe later, not at launch:** "Big appetite", a one-time purchase (about $2.99) where clean solves
    pay 2 cheese instead of 1. Also cosmetics bought with cheese (hats for the mouse, a golden hole), to
    give strong players' cheese piles a use.
  - **Version 1.0 ships with cheese packs.** Rewarded ads come in 1.1, soon after.
- **Ads:** non-personalized at launch, so there's no tracking pop-up. Google's consent screen is shown to
  EU and UK players.
- **Difficulty:** the castle is made harder and more varied before launch (`docs/HARDER_CASTLE.md`). After
  launch, use player stats to find and fix any level that's too hard.

### Why these numbers

A simulation of three kinds of player through all 1,100 levels (the hint rates were guesses):
- **Old prices (hints 1 + 2, start with 5):** puzzle fans and average players finished with hundreds of
  cheese and never needed help. Only casual players ran short.
- **New prices (3 + 3, start with 0):** puzzle fans still never run short. Average players start feeling
  it around the Second floor, about 85 times over the castle. Casual players run short often, from about
  level 25–50.
- **Ad hints and packs** are the way through, so nobody is ever truly stuck.

Rewarded video pays very roughly 0.5–1.5 cents per ad watched. Matt doesn't expect real money from this,
so the aim is a fair, friendly economy, not squeezing players. Check the balance with TestFlight players
and the level stats.

## Matt's to-dos (outside the code)

1. **Enroll in the Apple Developer Program as an individual** ($99/year): legal name, two-factor sign-in
   on the Apple Account, and a real street address (P.O. boxes aren't accepted at enrollment).
2. **Reserve the name "Mouse in Hole"** in App Store Connect once approved (create the app record).
3. **Decide about the EU** before step 5. Selling there (purchases or ads) means Apple shows a contact
   address, phone and email on the EU store. A PO box is fine for the address. Otherwise, leave the EU
   out at launch.
4. **At step 4:** a RevenueCat account (free at this size) and the Paid Apps agreement, tax (W-9) and bank
   details in App Store Connect.
5. **At step 6:** a Google AdMob account (one account covers both phones).
6. **An LLC isn't needed now.** If the game takes off, Matt can form one (Pennsylvania: $125, then $7 a
   year) and convert the Apple account to an organization, keeping the app.
7. **For Android:** a Google Play developer account ($25 once) and 12 testers for the closed test (see
   "Android" below). Start both well before the Android launch.

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

## Android (after the iPhone)

The same game ships on Google Play from the same Capacitor project (`npx cap add android` next to `ios`).
Almost everything in steps 1–6 carries over; this section is what's different. Check Google's current rules
in Play Console when each part starts, since they change from time to time.

### Matt's to-dos for Android

1. **A Google Play developer account as an individual: $25, paid once** (Apple's is $99 a year). Google
   checks his ID and a phone number, and he needs an Android phone for the account's device check. His legal
   name shows as the developer. If the game sells cheese, Google may also show a contact address on the
   listing; as with the EU on Apple, check what Play Console asks for before launch.
2. **The closed test (new personal accounts):** before Google lets a new personal account publish to
   everyone, the app has to run a **closed test with at least 12 testers who stay opted in for at least 14
   days in a row**. Then Matt applies for production access in Play Console (it asks a few questions about
   the test), and Google takes a few days to answer. So:
   - Line up 12+ testers early (friends and family with Android phones, a Google Group or an email list).
   - Start the closed test as soon as the first Android build runs, ideally while the iPhone version is in
     TestFlight, so the 14 days are over by the time the iPhone launches.
   - Ask testers to actually play and leave feedback; Google looks at whether the test was real.
3. **An Android phone to test on** (borrowed is fine), or the Android emulator for a first look. Matt tests
   on his iPhone; a few real Android checks before launch are still worth it.
4. **Payments profile** in Play Console (tax and bank details) before cheese packs can be sold.

### What changes in each step

- **Step 1 (this one):** nothing extra. The fit check already covers a small Android phone (360×640).
- **Step 2 (Capacitor):**
  - The same bundled site, Capacitor Preferences for saved progress (it uses Android's own storage), and the
    same first-launch copy from browser storage.
  - **The back button:** Android phones have a back gesture or button, and Google expects it to work. With
    Capacitor's App plugin (`backButton`): close the open pop-up first (a card, the map, the win card), then
    on the level screen open the map, and from the map leave the app (never lose progress). Show Matt how it
    behaves before building more on it.
  - **Screen sizes:** Android phones come in many shapes, from small (360×640) to tall (about 360×800 and
    412×915) and foldables and tablets. Add the tall sizes to `tools/screens/fit.js`. On tablets the game
    keeps its 520px-wide column in the middle (it already does in a browser).
  - **Edge to edge:** new Android versions draw the app under the status bar and the gesture bar, like the
    iPhone notch. Check that `env(safe-area-inset-*)` works in Android's WebView on a real phone; if it
    comes back as 0, use a safe-area plugin so the header and the Go button stay clear.
  - **Icon:** Android needs an adaptive icon (a foreground drawing on a plain background) on top of the
    iPhone icon; make both from the icon Matt picks.
  - **Cloud builds:** Android doesn't need a Mac. A GitHub Actions workflow on a Linux runner builds a signed
    App Bundle (`.aab`) and uploads it to the closed-test track with a Play service account. The upload key
    and the service account key live in GitHub secrets, never in the repo. Play App Signing keeps the real
    signing key at Google, so a lost upload key can be replaced.
  - **Target API level:** Google requires new apps to target a recent Android version (it moves up every
    August). Use the level Play Console asks for.
- **Step 3 (native touches):** Google Play Games achievements are optional; skip them at first unless Matt
  wants them. Capacitor's Haptics plugin works on Android too. The same privacy-friendly level stats.
- **Step 4 (cheese packs):** **Google Play Billing, through RevenueCat**, the same as StoreKit on the
  iPhone: the same three packs and the starter offer as consumable products in Play Console, with the same
  names and prices. RevenueCat keeps one list of products for both stores, so the cheese shop code is the
  same. Test with Play's license testers (purchases that aren't charged). Google takes 15% of the first $1M
  a year (Apple's Small Business Program is also 15%, but Matt has to sign up for it).
- **Step 5 (launch):** the Play listing (short and long description, feature graphic, phone screenshots from
  `tools/screens`), the **content rating questionnaire** (IARC), the **target audience** (pick the 13+ age
  groups, so the game isn't in Google's Families programme, the same as staying out of Apple's Kids
  category), the **Data safety form** (Google's privacy label, matching the privacy policy), and the same
  privacy policy page. Then the closed test, production access, and release.
- **Step 6 (ads):** **AdMob** rewarded ads on Android too, from the same AdMob account (a separate Android
  app and ad unit in AdMob), wired into the same "Watch an ad for this hint" place. The same UMP consent
  screen for the EU and UK, non-personalized ads, and the same `app-ads.txt`. Android has no tracking
  pop-up like Apple's, but the Data safety form must say the app uses ads.
