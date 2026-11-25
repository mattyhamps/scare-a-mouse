// Measures the level spots on every room's map and lists any two that are closer than a spot's width.
// Usage: node tools/screens/spots.js [MIN]     (MIN in room units, default 50; the room is 390 wide)
const { serve, browser, openLevel } = require('./common');
(async () => {
  const PORT = 8793, base = `http://localhost:${PORT}/`, MIN = +(process.argv[2] || 50);
  const srv = serve(PORT), b = await browser();
  const p = await b.newPage({ viewport: { width: 430, height: 900 } }); p.on('pageerror', e => console.log('page error', e.message));
  await p.goto(base); await p.waitForTimeout(400);
  const L = await p.evaluate(async () => (await (await fetch('levels.json')).json()).length);
  let firsts = [1], bad = 0;
  for (let rooms = 0; firsts[firsts.length - 1] <= L && rooms < 60; rooms++) {
    const n = firsts[firsts.length - 1];
    await openLevel(p, base, n);
    await p.click('#lvlBtn'); await p.waitForTimeout(700);
    const r = await p.evaluate(() => {
      const room = document.querySelector('.room.drawn-room'), vb = room.querySelector('.room-body > svg').viewBox.baseVal;
      const nodes = [...room.querySelectorAll('.node')].map(e => ({ i: +e.dataset.i + 1, x: parseFloat(e.style.left) / 100 * vb.width, y: parseFloat(e.style.top) / 100 * vb.height }));
      return { name: room.querySelector('.room-head b').textContent, nodes };
    });
    const close = [];
    r.nodes.forEach((a, i) => r.nodes.forEach((c, j) => { const d = Math.hypot(a.x - c.x, a.y - c.y); if (j > i && d < MIN) close.push(`${a.i}/${c.i} (${d.toFixed(0)})`); }));
    const last = Math.max(...r.nodes.map(q => q.i));
    console.log(`${r.name} ${n}-${last}: ${close.length ? close.length + ' too close: ' + close.join(', ') : 'ok'}`);
    bad += close.length;
    firsts.push(last + 1);
  }
  console.log(bad ? `${bad} pairs too close` : `No spots closer than ${MIN}.`);
  await b.close(); srv.close(); process.exit(bad ? 1 : 0);
})();
