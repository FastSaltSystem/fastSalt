const fs=require('fs'),path=require('path');
const h=require('../hurmet_display.cjs').checkingEngine(require(process.env.HURMET_ENGINE));globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Steam Brayton cooler - Hurmet.md');
function val(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet error');return out;}
(async()=>{const src=fs.readFileSync(file,'utf8');const out=await calc(await calc(src));
const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'brayton-hurmet-checks.json'),'utf8'));
for(const[n,v]of Object.entries(expected))if(Math.abs(val(out,n)-v)>2e-6*Math.max(Math.abs(v),.01))throw Error(n+': '+val(out,n)+' != '+v);
const twice=await calc(src.replace('HeatInput = 10 MW','HeatInput = 20 MW'));
for(const n of ['SteamFlow','AvailablePower','FanPower','RemainingPower','EightFlow','EightAvailable','EightFanPower','EightRemaining'])if(Math.abs(val(twice,n)/val(out,n)-2)>1e-5)throw Error('Duty scaling '+n);
const fan=await calc(src.replace('AirPressureDrop = 500 Pa','AirPressureDrop = 1000 Pa'));
if(Math.abs(val(fan,'FanPower')/val(out,'FanPower')-2)>1e-5)throw Error('Fan pressure sensitivity');
if(((await h.hurmet2html(out)).match(/<table/g)||[]).length!==4)throw Error('Expected four result tables');
fs.writeFileSync(file,await h.forDisplay(out));fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});fs.writeFileSync(path.join(__dirname,'preview/brayton-cooler.html'),await h.hurmet2html(out));
console.log('Hurmet save/reopen, '+Object.keys(expected).length+' numerical checks, duty scaling and fan-loss sensitivity passed.');
})().catch(e=>{console.error(e);process.exit(1)});
