const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [file, out, theme, ...nums] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const k of nums) {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.addInitScript(t => { try { localStorage.setItem('ff-share-theme', t); } catch (e) {} }, theme);
    await p.goto('file://' + require('path').resolve(file) + '#' + k);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(600);
    // overflow check
    const ov = await p.evaluate(() => { const s = document.querySelector('.slide.active'); const r=[]; s.querySelectorAll('.pass-body *').forEach(e=>{ if (e.scrollHeight>e.clientHeight+2 && getComputedStyle(e).overflow!=='visible') r.push(e.className+' '+e.scrollHeight+'>'+e.clientHeight);}); const pb=s.querySelector('.pass-body'); r.push('pb '+pb.scrollHeight+'/'+pb.clientHeight); return r; });
    console.log(k, ov.join(' | '));
    await p.screenshot({ path: `${out}/${theme}-${String(k).padStart(2, '0')}.png` });
    await p.close();
  }
  await b.close();
})();
