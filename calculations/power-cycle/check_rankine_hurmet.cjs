// Recalculate, round-trip, compare the external model and check duty scaling.
const fs=require('fs'),path=require('path');
const engine=process.env.HURMET_ENGINE;
if(!engine)throw Error('Set HURMET_ENGINE');
const h=require(engine);globalThis.temml=require(process.env.TEMML_ENGINE||engine.replace(/hurmet\.cjs$/,'temml.cjs'));
const file=path.join(__dirname,'Rankine cycle - Hurmet.md');
function value(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function recalc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.'))throw Error('Hurmet calculation error: '+html);return {out,html};}
(async()=>{
 const {out,html}=await recalc(fs.readFileSync(file,'utf8'));const again=await recalc(out);
 const r=JSON.parse(fs.readFileSync(path.join(__dirname,'rankine-results.json'),'utf8'));
 for(const [name,expected] of Object.entries({TotalSteam:r.mass,GrossElectric:r.gross/1e6,CondenserDuty:r.qcond/1e6,BFPShaft:r.bfp/1e6,CEPElectric:r.cep/1e6,ReheatDuty:r.reheat_duty/1e6})){
   const actual=value(again.out,name);if(Math.abs(actual-expected)>Math.abs(expected)*1e-6)throw Error(name+' mismatch '+actual+' vs '+expected);
 }
 const half=await recalc(out.replace('ReactorDuty = 1500 MW','ReactorDuty = 750 MW'));
 if(Math.abs(value(half.out,'GrossElectric')/value(out,'GrossElectric')-.5)>1e-6)throw Error('Duty scaling failed');
 if(Math.abs(value(half.out,'GrossEfficiency')-value(out,'GrossEfficiency'))>1e-7)throw Error('Fixed-cycle efficiency scaling failed');
 fs.writeFileSync(file,again.out);fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});
 fs.writeFileSync(path.join(__dirname,'preview','rankine.html'),html);
 console.log('Hurmet round-trip, six external-model comparisons and duty scaling passed.');
 console.log(['GrossElectric','CondenserDuty','CoolingVolume','CondenserArea'].map(n=>n+' = '+value(out,n)).join('\n'));
})().catch(e=>{console.error(e);process.exit(1)});
