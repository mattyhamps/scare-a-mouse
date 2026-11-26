// Shared bits for the screenshot scripts: serve the built game and open a phone-sized browser page.
// The game is served from web/target/site (build it first: mvn -q package -DskipTests -pl web -am),
// or from the folder in the SITE environment variable.
const fs = require('fs'), http = require('http'), path = require('path');
const { chromium } = require('playwright');
const root = process.env.SITE || path.resolve(__dirname, '../../web/target/site');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.woff2': 'font/woff2' };

function serve(port) {
  return http.createServer((q, r) => {
    // Work on the URL path, not the file path: on Windows path.join turns '/' into '\\', so checking the
    // file path for a trailing '/' never matched and the page itself came back as "not found".
    let u = decodeURIComponent(q.url.split('?')[0].split('#')[0]);
    if (u.endsWith('/')) u += 'index.html';
    const f = path.join(root, ...u.split('/'));
    if (path.relative(root, f).startsWith('..')) { r.writeHead(403); r.end(); return; }   // stay inside the site folder
    fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; }
      r.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); r.end(d); });
  }).listen(port);
}
async function browser() { return chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {}); }
// The same layout key the game uses for progress (index.html, levelKey).
const levelKey = l => { const parts = [l.hole, l.walls, l.fixed, l.inv]; if (l.turns && l.turns.length) parts.push(l.turns);
  if (l.traps && l.traps.length) parts.push(['traps', ...l.traps]); const s = JSON.stringify(parts);
  let h = 5381; for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0; return (h >>> 0).toString(36); };
// Pretend every level before n is solved and open level n (1-based). Cards already seen unless showCards.
async function openLevel(p, base, n, { showCards = false } = {}) {
  await p.goto(base); await p.waitForTimeout(300);
  await p.evaluate(async ({ n, showCards, src }) => { const levelKey = eval(src); const L = await (await fetch('levels.json')).json(); const solved = {};
    for (let i = 0; i < n - 1; i++) solved[levelKey(L[i])] = L[i].solution;
    localStorage.clear(); localStorage.setItem('cm_solved', JSON.stringify(solved)); localStorage.setItem('cm_intro', 'true');
    localStorage.setItem('cm_cards', JSON.stringify(showCards ? [] : [...Array(2000).keys()])); localStorage.setItem('cm_level', String(n - 1)); },
    { n, showCards, src: levelKey.toString() });
  await p.goto(base); await p.waitForTimeout(1200);
}
module.exports = { serve, browser, openLevel, root };
