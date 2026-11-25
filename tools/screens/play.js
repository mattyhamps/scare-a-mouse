// Plays levels with their intended solution and reports whether the mouse escapes.
// Usage: node tools/screens/play.js 501 526 650     (screenshots go to tools/screens/out/play-<n>.png)
const fs = require('fs'), path = require('path'), { serve, browser, openLevel } = require('./common');
(async () => {
  const PORT = 8791, base = `http://localhost:${PORT}/`, out = path.join(__dirname, 'out'); fs.mkdirSync(out, { recursive: true });
  const srv = serve(PORT), b = await browser();
  for (const n of process.argv.slice(2).map(Number)) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); p.on('pageerror', e => console.log('page error', e.message));
    await openLevel(p, base, n);
    await p.screenshot({ path: path.join(out, `play-${n}.png`) });
    const L = await p.evaluate(async i => (await (await fetch('levels.json')).json())[i], n - 1), rem = [...L.inv];
    for (const s of L.solution) { const i = rem.indexOf(s.t); await p.click(`.piece[data-i="${i}"]`); rem.splice(i, 1);
      await p.evaluate(s => [...document.querySelectorAll('.floor')].find(e => +e.dataset.x === s.x && +e.dataset.y === s.y && !e.classList.contains('turn')).click(), s); }
    await p.click('#goBtn'); let won = false;
    for (let k = 0; k < 150 && !won; k++) { await p.waitForTimeout(100); won = !!(await p.$('#win.show')); }
    console.log(`${n} ${(await p.textContent('#lvlName')).trim()}: ${won ? 'solved' : 'NOT solved'}`);
    await p.close();
  }
  await b.close(); srv.close();
})();
