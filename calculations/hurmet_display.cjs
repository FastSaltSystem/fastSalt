// Check with full precision, then publish the same calculation with h3 display.
// Rounding is a display choice; it must not loosen numerical test tolerances.
const {execFileSync}=require('child_process');
const path=require('path');
function style(text) {
  return execFileSync(process.env.PYTHON || 'python3',
    [path.join(__dirname,'hurmet_style.py')],
    {input:text,encoding:'utf8',maxBuffer:32*1024*1024});
}
function highPrecision(text) { return style(text).replace('format = "h3"','format = "h15"'); }
// Hurmet's serializer can emit NaN widths for otherwise valid Markdown tables.
// Remove invalid layout metadata only; calculation errors remain visible.
function cleanTables(text) { return text.replace(/ colWidths="[^"]*NaN[^"]*"/g,'').trimEnd()+'\n'; }
function checkingEngine(engine) {
  const display=async text=>cleanTables(await engine.updateAndSave(style(text)));
  return {...engine,
    updateAndSave:async text=>cleanTables(await engine.updateAndSave(highPrecision(text))),
    forDisplay:display,
    hurmet2html:async(text,...args)=>engine.hurmet2html(await display(text),...args)
  };
}
module.exports={style,highPrecision,checkingEngine};
