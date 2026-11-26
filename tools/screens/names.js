// Checks that every level's name fits on one line in the header above the board on a phone, with nothing cut off.
// Usage: node tools/screens/names.js [width ...]      (default 360 and 390; exits with 1 if any name does not fit)
// It opens the game once per width and puts each level's name, label ("Boss · Level N", the flame, "solved")
// and a 4-digit cheese count into the real header, the same way the game does, then measures it.
const fs = require('fs'), path = require('path'), { serve, browser, openLevel, root } = require('./common');
(async () => {
  const widths = process.argv.slice(2).map(Number).filter(Boolean);
  const PORT = 8794, base = `http://localhost:${PORT}/`, srv = serve(PORT), b = await browser();
  const levels = JSON.parse(fs.readFileSync(path.join(root, 'levels.json'), 'utf8'));
  const hard = new Set(JSON.parse(fs.readFileSync(path.join(root, 'hard-levels.json'), 'utf8')));
  const BOSSES = [100, 200, 350, 500, 650, 800, 950, 1070, 1100];
  let bad = 0;
  for (const W of widths.length ? widths : [360, 390]) {
    const p = await b.newPage({ viewport: { width: W, height: 800 } });
    // the crown and the flame icons, taken from the game itself (a boss and a flame level)
    await openLevel(p, base, 950); const crown = await p.$eval('#lvlSub svg', e => e.outerHTML);
    await openLevel(p, base, 937); const flame = await p.$eval('#lvlSub svg', e => e.outerHTML);
    const cut = await p.evaluate(({ levels, hard, bosses, crown, flame }) => {
      const name = document.getElementById('lvlName'), sub = document.getElementById('lvlSub'), cheese = document.getElementById('cheese');
      cheese.innerHTML = cheese.innerHTML.replace(/\d+\s*$/, '8888');
      const out = [];
      levels.forEach((L, i) => { const n = i + 1, boss = bosses.includes(n), flamed = !boss && hard.includes(n);
        for (const solved of [false, true]) {
          name.textContent = L.name;
          sub.innerHTML = (boss ? `${crown} Boss · ` : flamed ? `${flame} ` : '') + (solved ? `Level ${n} · solved ✓` : `Level ${n}`);
          // doesn't fit: the name is cut off or needs a second line, or the label row spills past the screen
          const row = name.parentElement.getBoundingClientRect(), line = parseFloat(getComputedStyle(name).lineHeight) || 26;
          const box = sub.parentElement;   // the label and the cheese
          if (name.scrollWidth > name.clientWidth + 1 || name.getBoundingClientRect().height > line * 1.5
              || box.scrollWidth > box.clientWidth + 1 || row.right > document.documentElement.clientWidth + 1)
            out.push({ n, name: L.name, kind: boss ? 'boss' : flamed ? 'flame' : 'plain', solved });
        } });
      return out; }, { levels, hard: [...hard], bosses: BOSSES, crown, flame });
    const unsolved = cut.filter(c => !c.solved), solvedOnly = cut.filter(c => c.solved && !unsolved.some(u => u.n === c.n));
    const kinds = k => unsolved.filter(c => c.kind === k).length;
    console.log(`${W}px: ${unsolved.length} names do not fit (boss ${kinds('boss')}, flame ${kinds('flame')}, plain ${kinds('plain')}), and ${solvedOnly.length} more once solved ("· solved ✓")`);
    for (const c of cut) if (!c.solved || solvedOnly.includes(c)) console.log(`  ${c.n} ${c.kind}${c.solved ? ' (solved)' : ''}: ${c.name}`);
    bad += cut.length; await p.close();
  }
  await b.close(); srv.close();
  process.exit(bad ? 1 : 0);
})();
