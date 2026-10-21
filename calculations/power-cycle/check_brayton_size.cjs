const fs=require('fs'),path=require('path');const h=require('../hurmet_display.cjs').checkingEngine(require(process.env.HURMET_ENGINE));globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Brayton cooler size comparison - Hurmet.md');
function val(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s),html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet error');return out;}
(async()=>{const src=fs.readFileSync(file,'utf8'),out=await calc(await calc(src));const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'brayton-size-results.json'),'utf8')).hurmet_checks;
for(const[n,v]of Object.entries(expected))if(Math.abs(val(out,n)-v)>2e-6*Math.max(Math.abs(v),.01))throw Error(n+': '+val(out,n)+' != '+v);
const fast=await calc(src.replace('OpenVelocity = 15','OpenVelocity = 30'));
if(Math.abs(val(fast,'AirHotDiameter')/val(out,'AirHotDiameter')-Math.sqrt(.5))>1e-6)throw Error('Velocity sensitivity');
const html=await h.hurmet2html(out);if((html.match(/<table/g)||[]).length!==2)throw Error('Expected two tables');fs.writeFileSync(file,await h.forDisplay(out));fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});fs.writeFileSync(path.join(__dirname,'preview/brayton-size-comparison.html'),html);console.log('Passed 12 numerical comparisons, save/reopen, velocity sensitivity and two tables.');
})().catch(e=>{console.error(e);process.exit(1)});
