// Checks that the game fits a phone without scrolling: the level screen (header, tip, board, tray and the
// Hint, Reset and Go buttons), the floor-map pop-up (its bottom buttons) and a card, at 390×664 (an iPhone
// browser) and 360×640. Takes a screenshot of each and fails if anything needs scrolling.
// Usage: node tools/screens/fit.js [level ...]    (images go to tools/screens/out/fit-<w>x<h>-*.png)
// Build the site first: mvn -q package -DskipTests -pl web -am
const fs = require('fs'), path = require('path'), { serve, browser, openLevel } = require('./common');
const SIZES = [[390, 664], [360, 640]];
// A spread of boards: small early ones, 10×10 with a long name and tip, a boss, a moving level, a card.
const LEVELS = process.argv.slice(2).map(Number).filter(Boolean);
const levels = LEVELS.length ? LEVELS : [1, 33, 200, 501, 800, 950, 1075, 1100];
(async () => {
  const PORT = 8794, base = `http://localhost:${PORT}/`, out = process.env.OUT || path.join(__dirname, 'out'); fs.mkdirSync(out, { recursive: true });
  const srv = serve(PORT), b = await browser(); const bad = [];
  // How far the page, or a pop-up card, runs past the screen (0 = fits).
  const overflow = p => p.evaluate(() => {
    const d = document.scrollingElement, page = Math.max(0, d.scrollHeight - innerHeight), wide = Math.max(0, d.scrollWidth - innerWidth);
    let card = 0; document.querySelectorAll('.overlay.show .card').forEach(c => { card = Math.max(card, c.scrollHeight - c.clientHeight, c.getBoundingClientRect().bottom - innerHeight); });
    // the level screen's last row (the buttons) must be on screen
    const ctl = document.querySelector('.controls:not(.replay-controls)'), btn = ctl ? Math.max(0, ctl.getBoundingClientRect().bottom - innerHeight) : 0;
    return { page, wide, card: Math.max(0, Math.round(card)), btn: Math.round(btn) };
  });
  const check = async (p, what, w, h) => {
    const o = await overflow(p), name = `fit-${w}x${h}-${what}.png`;
    await p.screenshot({ path: path.join(out, name) });
    // behind a pop-up only the pop-up itself counts
    const worst = what.startsWith('level') ? Math.max(o.page, o.wide, o.btn) : Math.max(o.wide, o.card);
    console.log(`${w}x${h} ${what.padEnd(14)} ${worst ? 'NEEDS SCROLLING ' + JSON.stringify(o) : 'fits'}`);
    if (worst) bad.push(`${w}x${h} ${what}`);
  };
  for (const [w, h] of SIZES) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    // How to play: the cards a new player sees before level 1.
    await p.goto(base); await p.evaluate(() => localStorage.clear()); await p.goto(base); await p.waitForTimeout(1200);
    for (let k = 1; await p.$('#guide.show') && k < 10; k++) { await check(p, `intro-${k}`, w, h); await p.click('#guideNext'); await p.waitForTimeout(350); }
    for (const n of levels) {
      await openLevel(p, base, n, { showCards: true });
      if (await p.$('#guide.show')) { await check(p, `card-${n}`, w, h); await p.click('#guideNext'); await p.waitForTimeout(400); }
      await check(p, `level-${n}`, w, h);
    }
    // The floor map, opened from the Level button, then the castle view (Castle button).
    // From level 900: the room's map, the floor's map (Back) with its stairs buttons, then the whole castle.
    await openLevel(p, base, 900);
    await p.click('#lvlBtn'); await p.waitForTimeout(800); await check(p, 'map-room', w, h);
    await p.click('#pickBack'); await p.waitForTimeout(600); await check(p, 'map-floor', w, h);
    await p.click('#pickCastle'); await p.waitForTimeout(600); await check(p, 'map-castle', w, h);
    // The tester link: the rest of the castle says "Coming soon".
    await p.evaluate(() => localStorage.clear()); await p.goto(base + '?demo'); await p.waitForTimeout(1200);
    if (await p.$('#guide.show')) { await p.click('#guideSkip'); await p.waitForTimeout(400); }
    await p.click('#lvlBtn'); await p.waitForTimeout(800);
    if (await p.$('#pickCastle:not([hidden])')) { await p.click('#pickCastle'); await p.waitForTimeout(600); }
    await check(p, 'map-demo', w, h);
    await p.click('.band-floor[data-a="0"], .castle-cut [data-a="0"]').catch(() => {}); await p.waitForTimeout(600); await check(p, 'map-demo-outside', w, h);
    await p.close();
  }
  await b.close(); srv.close();
  if (bad.length) { console.log(`\n${bad.length} screen(s) need scrolling: ${bad.join(', ')}`); process.exit(1); }
  console.log('\nEverything fits.');
})();
