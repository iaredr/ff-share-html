// usage: node shot.js <html file> <out dir> <light|dark> [slide numbers...]
const { chromium } = require('playwright');
(async () => {
  const [file, out, theme = 'light', ...nums] = process.argv.slice(2);
  require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.addInitScript(t => { try { localStorage.setItem('ff-share-theme', t); } catch (e) {} }, theme);
  await p.goto('file://' + require('path').resolve(file));
  const n = await p.$$eval('.slide', s => s.length);
  const list = nums.length ? nums.map(Number) : Array.from({ length: n }, (_, k) => k + 1);
  for (const k of list) {
    await p.evaluate(k => { location.hash = '#' + k; location.reload(); }, k);
    await p.waitForLoadState('load');
    await p.evaluate(() => Promise.all(Array.from(document.querySelectorAll('.slide.active img')).map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))));
    await p.waitForTimeout(500);
    await p.screenshot({ path: `${out}/${theme}-${String(k).padStart(2, '0')}.png` });
  }
  await b.close();
})();
