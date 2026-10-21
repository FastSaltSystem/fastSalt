const fs=require('fs'),path=require('path');
const h=require('../hurmet_display.cjs').checkingEngine(require(process.env.HURMET_ENGINE));globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Cooling-water cases - Hurmet.md');
function val(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
(async()=>{
 const a=await h.updateAndSave(fs.readFileSync(file,'utf8'));const b=await h.updateAndSave(a);
 const html=await h.hurmet2html(b);if(html.includes('Error.'))throw Error('Hurmet error');
 const r=JSON.parse(fs.readFileSync(path.join(__dirname,'cooling-cases.json'),'utf8'));
 for(let i=1;i<=3;i++){
  if(Math.abs(val(b,'AreaRatio'+i)-1)>1e-6)throw Error('Area mismatch '+i);
  if(Math.abs(val(b,'WaterOutlet'+i)-(r.cases[i-1].outlet_C+273.15))>1e-4)throw Error('Outlet mismatch '+i);
 }
 fs.writeFileSync(file,await h.forDisplay(b));fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});
 fs.writeFileSync(path.join(__dirname,'preview','cooling-cases.html'),html);
 console.log('Hurmet round trip, three LMTD area checks and three outlet-temperature checks passed.');
})().catch(e=>{console.error(e);process.exit(1)});
