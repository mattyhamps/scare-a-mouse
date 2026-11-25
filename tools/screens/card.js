// Opens level n with its how-to card showing (if it has one) and screenshots the card and then the board.
// Usage: node tools/screens/card.js 501     (images go to tools/screens/out/card-<n>.png and board-<n>.png)
const fs = require('fs'), path = require('path'), { serve, browser, openLevel } = require('./common');
(async () => {
  const PORT = 8793, base = `http://localhost:${PORT}/`, out = path.join(__dirname, 'out'); fs.mkdirSync(out, { recursive: true });
  const srv = serve(PORT), b = await browser();
  for (const n of process.argv.slice(2).map(Number)) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await openLevel(p, base, n, { showCards: true });
    await p.screenshot({ path: path.join(out, `card-${n}.png`) });
    if (await p.$('#guide.show')) { await p.click('#guideNext'); await p.waitForTimeout(400); }
    await p.screenshot({ path: path.join(out, `board-${n}.png`) });
    console.log(n, (await p.textContent('#tip')).trim()); await p.close();
  }
  await b.close(); srv.close();
})();
