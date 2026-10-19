// Render the overview and existing steam worksheet; no thermodynamic models are run.
const fs = require('fs');
const path = require('path');
const h = require(process.env.HURMET_ENGINE);
globalThis.temml = require(process.env.TEMML_ENGINE);
const {withHurmetWidths} = require('./hurmet_pipe_tables.cjs');
const prepareOverview = markdown => '---------------\ndecimalFormat: 1,000,000.\nsaveDate: 2026-10-19\n---------------\n\n' + withHurmetWidths(markdown);
const previews = new Map([
  ['brayton-overview.md', 'brayton-overview.html'],
  ['Brayton fan and salt pump balance - Hurmet.md', 'brayton-fan-pump.html'],
  ['Steam Brayton cooler - Hurmet.md', 'brayton-cooler.html'],
  ['Brayton-driven salt pump - Hurmet.md', 'brayton-salt-pump.html'],
  ['Nitrogen versus steam Brayton - Hurmet.md', 'nitrogen-brayton.html'],
  ['Open-air Brayton cooler - Hurmet.md', 'open-air-brayton.html'],
  ['Simple CO2 Brayton cooler - Hurmet.md', 'co2-brayton.html'],
  ['Brayton cooler size comparison - Hurmet.md', 'brayton-size-comparison.html'],
]);
function localLinks(html) {
  return html.replace(/href=(['"])(.*?)\1/g, (whole, quote, target) => {
    if (/^(?:[a-z]+:|#|\/)/i.test(target)) return whole;
    const decoded = decodeURIComponent(target);
    const preview = previews.get(decoded);
    const output = preview && fs.existsSync(path.join(__dirname, 'preview', preview)) ? preview : '../' + target;
    return 'href=' + quote + output + quote;
  });
}
const style = `body{font:17px/1.55 system-ui,sans-serif;color:#20313c;background:#f5f7fa;margin:0}main{max-width:1160px;margin:28px auto;padding:32px;background:white}h1{line-height:1.2}h2{margin-top:2em}a{color:#12618b}table{border-collapse:collapse;width:100%;table-layout:auto!important;font-size:15px}td,th{padding:9px 12px;border:1px solid #ccd6de;text-align:left;vertical-align:top}th{background:#e9f0f5}tr:nth-child(even){background:#f7f9fa}.table-scroll{overflow-x:auto}li{margin:.7em 0}@media print{body{background:white}main{margin:0;padding:0}table{font-size:11px}}`;
(async () => {
  const out = path.join(__dirname, 'preview');
  fs.mkdirSync(out, {recursive:true});
  // Create the target first so references to it resolve during this build.
  const overview = await h.hurmet2html(prepareOverview(fs.readFileSync(path.join(__dirname, 'brayton-overview.md'), 'utf8')));
  if ((overview.match(/<table/g) || []).length !== 2) throw Error('Expected comparison and sources tables');
  fs.writeFileSync(path.join(out, 'brayton-overview.html'), overview);
  for (const [source, target] of [...previews].slice(0, 2)) {
    const markdown = fs.readFileSync(path.join(__dirname, source), 'utf8');
    const body = localLinks(await h.hurmet2html(source === 'brayton-overview.md' ? prepareOverview(markdown) : markdown))
      .replace(/<table/g, '<div class="table-scroll"><table').replace(/<\/table>/g, '</table></div>');
    fs.writeFileSync(path.join(out, target), `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${source.replace(/\.md$/, '')}</title><style>${style}</style></head><body><main>${body}</main></body></html>`);
  }
  console.log('Published four-case overview and refreshed steam preview; source worksheets unchanged.');
})().catch(e => {console.error(e);process.exit(1);});
