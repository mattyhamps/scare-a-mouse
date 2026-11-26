// Checks that every level's name fits on one line in the header above the board on a phone: never cut off, nothing spilling past the screen (the name with its crown or flame and solved tick, the cheese
// count, the top bar with the Level button).
// Usage: node tools/screens/names.js [width ...]      (default 360 and 390; exits with 1 if any name does not fit)
// It opens the game once per width and puts each level's name, badges, Level button and a 4-digit cheese count into the
// real header, the same way the game does, then measures it.
const fs = require('fs'), path = require('path'), { serve, browser, openLevel, root } = require('./common');
(async () => {
  const widths = process.argv.slice(2).map(Number).filter(Boolean);
  const PORT = 8794, base = `http://localhost:${PORT}/`, srv = serve(PORT), b = await browser();
  const levels = JSON.parse(fs.readFileSync(path.join(root, 'levels.json'), 'utf8'));
  const hard = new Set(JSON.parse(fs.readFileSync(path.join(root, 'hard-levels.json'), 'utf8')));
  const BOSSES = [100, 200, 350, 500, 650, 800, 950, 1075, 1100];
  let bad = 0;
  for (const W of widths.length ? widths : [360, 390]) {
    const p = await b.newPage({ viewport: { width: W, height: 800 } });
    // the crown and the flame icons, taken from the game itself (a boss and a flame level)
    await openLevel(p, base, 950); const crown = await p.$eval('#lvlName svg', e => e.outerHTML);
    await openLevel(p, base, 937); const flame = await p.$eval('#lvlName svg', e => e.outerHTML);
    const res = await p.evaluate(({ levels, hard, bosses, crown, flame }) => {
      const name = document.getElementById('lvlName'), btn = document.getElementById('lvlBtn'), cheese = document.getElementById('cheese');
      const header = btn.closest('header'), vw = document.documentElement.clientWidth;
      cheese.innerHTML = cheese.innerHTML.replace(/\d+\s*$/, '8888');
      const out = [], twoLines = new Set();
      levels.forEach((L, i) => { const n = i + 1, boss = bosses.includes(n), flamed = !boss && hard.includes(n);
        for (const solved of [false, true]) {
          name.innerHTML = (boss ? crown : flamed ? flame : '') + '<span></span>' + (solved ? '<span class="tick">✓</span>' : '');
          name.querySelector('span').textContent = L.name; btn.textContent = `Level ${n} ▾`;
          const line = parseFloat(getComputedStyle(name).lineHeight) || 26, lines = Math.round(name.getBoundingClientRect().height / line);
          if (lines > 1) twoLines.add(n);
          const spill = [name.parentElement, header, cheese, btn].some(e => e.getBoundingClientRect().right > vw + 1);
          if (name.scrollWidth > name.clientWidth + 1 || lines > 1 || spill || header.scrollWidth > header.clientWidth + 1)
            out.push({ n, name: L.name, kind: boss ? 'boss' : flamed ? 'flame' : 'plain', solved });
        } });
      return { out, twoLines: [...twoLines] }; }, { levels, hard: [...hard], bosses: BOSSES, crown, flame });
    const cut = res.out;
    console.log(`${W}px: ${cut.length} do not fit`);
    for (const c of cut) console.log(`  ${c.n} ${c.kind}${c.solved ? ' (solved)' : ''}: ${c.name}`);
    bad += cut.length; await p.close();
  }
  await b.close(); srv.close();
  process.exit(bad ? 1 : 0);
})();
