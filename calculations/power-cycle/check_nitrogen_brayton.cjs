const fs=require('fs'),path=require('path');const h=require('../hurmet_display.cjs').checkingEngine(require(process.env.HURMET_ENGINE));globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Nitrogen versus steam Brayton - Hurmet.md');
function val(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s),html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet error');return out;}
(async()=>{const src=fs.readFileSync(file,'utf8'),out=await calc(await calc(src));const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'nitrogen-hurmet-checks.json'),'utf8'));
for(const[n,v]of Object.entries(expected))if(Math.abs(val(out,n)-v)>2e-6*Math.max(Math.abs(v),.01))throw Error(n+': '+val(out,n)+' != '+v);
const fan=await calc(src.replace('AirPressureDrop = 500 Pa','AirPressureDrop = 1000 Pa'));if(Math.abs(val(fan,'FanPower')/val(out,'FanPower')-2)>1e-6)throw Error('Fan sensitivity');
const html=await h.hurmet2html(out);if((html.match(/<table/g)||[]).length!==2)throw Error('Expected two tables');fs.writeFileSync(file,await h.forDisplay(out));fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});fs.writeFileSync(path.join(__dirname,'preview/nitrogen-brayton.html'),html);console.log('Passed 11 numerical comparisons, save/reopen, fan sensitivity and two tables.');
})().catch(e=>{console.error(e);process.exit(1)});
