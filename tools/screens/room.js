// Screenshots the whole map of the room that level n is in (a tall image), with the levels before n solved.
// Usage: node tools/screens/room.js 501 531     (images go to tools/screens/out/room-<n>.png)
const fs = require('fs'), path = require('path'), { serve, browser, openLevel } = require('./common');
(async () => {
  const PORT = 8792, base = `http://localhost:${PORT}/`, out = path.join(__dirname, 'out'); fs.mkdirSync(out, { recursive: true });
  const srv = serve(PORT), b = await browser();
  for (const n of process.argv.slice(2).map(Number)) {
    const p = await b.newPage({ viewport: { width: 430, height: 3200 } }); p.on('pageerror', e => console.log('page error', e.message));
    await openLevel(p, base, n);
    await p.click('#lvlBtn'); await p.waitForTimeout(900);
    await p.evaluate(() => { const c = document.querySelector('.card.pick'); c.style.height = 'auto'; c.style.maxHeight = 'none';
      const m = document.getElementById('dots'); m.style.maxHeight = 'none'; m.style.flex = 'none'; m.style.overflow = 'visible'; });
    await p.waitForTimeout(400);
    await (await p.$('.room')).screenshot({ path: path.join(out, `room-${n}.png`) });
    console.log('saved', `room-${n}.png`); await p.close();
  }
  await b.close(); srv.close();
})();
