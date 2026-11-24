// Renders the concept screens to PNG: node _concept/shot.cjs  (run from the repo root)
const path = require('path');
const puppeteer = require('C:/Users/chedo/Dropbox/claude/skills/site-status/node_modules/puppeteer-core');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const file = 'file:///' + path.resolve(__dirname, 'screens.html').replace(/\\/g, '/');
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  for (const mode of ['solo', 'coop']) {
    const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
    await p.goto(file + '#' + mode, { waitUntil: 'networkidle0' });
    await p.screenshot({ path: path.join(__dirname, `concept-${mode}.png`) });
    console.log(mode, errs.length ? 'ERRORS: ' + errs.join('; ') : 'ok');
    await p.close();
  }
  await b.close();
})();
