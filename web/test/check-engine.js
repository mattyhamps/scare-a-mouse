// Checks the JavaScript build of the Java engine (TeaVM output) against the same physics
// fixtures the JUnit tests use, plus every level in data/levels.json.
// Usage: node web/test/check-engine.js [path/to/engine.js]
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '..', '..');
const enginePath = path.resolve(process.argv[2] || path.join(root, 'web/target/site/js/engine.js'));
const { scareSimulate } = require(enginePath);
if (typeof scareSimulate !== 'function') {
  console.error('scareSimulate was not exported by ' + enginePath);
  process.exit(1);
}
const run = (level, placed) => JSON.parse(scareSimulate(JSON.stringify(level), JSON.stringify(placed || [])));

const LETTERS = { M: 'mouse', C: 'cat', D: 'dog', B: 'bear', L: 'lion', E: 'elephant' };
function levelFromBoard(rows, hole) {
  const walls = [], mice = [], others = [], turns = [], traps = [];
  rows.forEach((row, y) => [...row].forEach((ch, x) => {
    if (ch === '#') walls.push([x, y]);
    else if ('^>v<'.includes(ch)) turns.push([x, y, '^>v<'.indexOf(ch)]);
    else if (ch === 'T') traps.push([x, y]);
    else if (LETTERS[ch]) (ch === 'M' ? mice : others).push({ t: LETTERS[ch], x, y });
  }));
  return { name: 'test', tip: '', w: rows[0].length, h: rows.length, hole: hole || [-1, -1],
    walls, fixed: [...mice, ...others], inv: [], solution: [], turns, traps };
}
function render(level, frame, snaps) {
  const sprung = new Set((snaps || []).flat());
  const g = Array.from({ length: level.h }, () => Array(level.w).fill('.'));
  level.walls.forEach(([x, y]) => { g[y][x] = '#'; });
  (level.turns || []).forEach(([x, y, d]) => { g[y][x] = '^>v<'[d]; });
  (level.traps || []).forEach(([x, y], k) => { g[y][x] = sprung.has(k) ? 't' : 'T'; });
  frame.forEach(a => { if (!a.gone) g[a.y][a.x] = Object.keys(LETTERS).find(k => LETTERS[k] === a.t); });
  return g.map(r => r.join('')).join('/');
}

let pass = 0, fail = 0;
const check = (ok, what) => { if (ok) pass++; else { fail++; console.log('FAIL ' + what); } };

const fixtures = JSON.parse(fs.readFileSync(path.join(root, 'engine/src/test/resources/physics-fixtures.json'), 'utf8'));
for (const f of fixtures) {
  const level = levelFromBoard(f.board, f.hole);
  const r = run(level, f.placed);
  const e = f.expect;
  let ok = true;
  if (e.pic) ok = ok && render(level, r.frames[r.frames.length - 1], r.snaps) === e.pic.join('/');
  if ('caught' in e) ok = ok && r.caught === e.caught;
  if ('win' in e) ok = ok && r.win === e.win;
  if ('loop' in e) ok = ok && r.loop === e.loop;
  if ('steps' in e) ok = ok && r.frames.length - 1 === e.steps;
  check(ok, 'physics: ' + f.name);
}

const levels = JSON.parse(fs.readFileSync(path.join(root, 'data/levels.json'), 'utf8'));
levels.forEach((l, i) => {
  check(run(l, l.solution).win === true, `level ${i + 1} "${l.name}": intended solution should win`);
  check(run(l, []).win === false, `level ${i + 1} "${l.name}": pressing Go with nothing placed should not win`);
});

console.log(`compiled engine: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
