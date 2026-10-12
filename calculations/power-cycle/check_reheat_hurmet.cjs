const fs=require('fs'),path=require('path');
const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Selected reheat and wetness - Hurmet.md');
function val(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
(async()=>{
 const once=await h.updateAndSave(fs.readFileSync(file,'utf8'));const out=await h.updateAndSave(once);
 const html=await h.hurmet2html(out);if(html.includes('Error.'))throw Error('Hurmet error');
 const r=JSON.parse(fs.readFileSync(path.join(__dirname,'reheat-selection.json'),'utf8'));const s=r.selected_at_5kPa;
 for(const [n,v] of Object.entries({MainFlow:s.mass,GrossElectric:s.gross/1e6,ReheatColdDuty:s.reheat_duty/1e6,ReheatHotDuty:s.reheat_duty/1e6,ExhaustMoisture:s.moisture,ReheaterArea1:r.reheater_UA_W_K/500,ReheaterArea2:r.reheater_UA_W_K/1000,ReheaterArea3:r.reheater_UA_W_K/1500})){
  if(Math.abs(val(out,n)-v)>1e-6*Math.max(Math.abs(v),.01))throw Error(n+' differs');
 }
 if(Math.abs(val(out,'ReheatBalance'))>1e-6)throw Error('Reheater energy mismatch');
 if(val(out,'ExhaustMoisture')>.10)throw Error('Moisture target failed');
 fs.writeFileSync(file,out);fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});
 fs.writeFileSync(path.join(__dirname,'preview','selected-reheat.html'),html);
 console.log('Hurmet round-trip, eight model comparisons and hot/cold reheater energy check passed.');
})().catch(e=>{console.error(e);process.exit(1)});
