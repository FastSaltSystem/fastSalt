const fs=require('fs'),path=require('path');
const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Brayton fan and salt pump balance - Hurmet.md');
function value(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet error');return out;}
function near(a,b,n){if(Math.abs(a-b)>2e-6*Math.max(Math.abs(b),.01))throw Error(n+': '+a+' != '+b);}
(async()=>{
 const src=fs.readFileSync(file,'utf8'),out=await calc(await calc(src));
 const r=JSON.parse(fs.readFileSync(path.join(__dirname,'brayton-fan-pump-results.json'),'utf8'));
 for(const[n,v]of Object.entries(r.hurmet_checks))near(value(out,n),v,n);
 const fifty=await calc(src.replace('HeatDuty = 30 MW','HeatDuty = 50 MW'));
 near(value(fifty,'RemainingElectricity'),r.cases[1].remaining_electric_W/1000,'50 MW margin');
 const pressure=await calc(src.replace('AirPressureDrop = 500 Pa','AirPressureDrop = 1000 Pa'));
 near(value(pressure,'FanElectricity'),value(out,'FanElectricity')*2,'Fan pressure sensitivity');
 const deficit=await calc(src.replace('AirPressureDrop = 500 Pa','AirPressureDrop = 1000 Pa').replace('AirRise = 100 K','AirRise = 50 K'));
 near(value(deficit,'RemainingElectricity'),r.sensitivity[2].remaining_electric_W/1000,'Deficit case');
 if(value(deficit,'RemainingElectricity')>=0)throw Error('Expected power deficit');
 const html=await h.hurmet2html(out);if((html.match(/<table/g)||[]).length!==2)throw Error('Expected two tables');
 fs.writeFileSync(file,out);fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});fs.writeFileSync(path.join(__dirname,'preview/brayton-fan-pump.html'),html.replaceAll('brayton-overview.md','brayton-overview.html'));
 console.log('Passed 17 numerical checks, save/reopen, 50 MW duty, fan pressure sensitivity and deficit case; two tables.');
})().catch(e=>{console.error(e);process.exit(1)});
