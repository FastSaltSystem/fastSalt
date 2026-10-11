const fs=require('fs'),path=require('path');
const hp=process.env.HURMET_ENGINE;if(!hp)throw Error('Set HURMET_ENGINE to the official Hurmet bundle');
const h=require(hp);globalThis.temml=require(hp.replace(/hurmet\.cjs$/,'temml.cjs'));
const p=process.argv[2]||path.join(__dirname,'..','Molten-salt coolant pipe wall - Hurmet.md');
function result(s,n){let m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);let v=m[1].replaceAll(',','');return v==='true'||v==='false'?v:Number(v);}
async function check(s){const out=await h.updateAndSave(s);if((await h.hurmet2html(out)).includes('Error.'))throw Error('Hurmet error');return out;}
(async()=>{
 const s=fs.readFileSync(p,'utf8'),base=await check(s),again=await check(base);
 const names=[...s.matchAll(/¢\?\?` (\w+) =/g)].map(m=>m[1]);
 for(const n of names)if(result(base,n)!==result(again,n))throw Error('Roundtrip '+n);
 for(const [oldval,newval,target] of [['DesignPressure = 1','DesignPressure = 2',40],['EffectiveStress = 50','EffectiveStress = 30',35]]){
  if(!s.includes(oldval))throw Error('Missing input');
  const changed=await check(s.replace(oldval,newval));
  if(result(changed,'NominalWall')!==target || result(changed,'PressureCheck')!=='true')throw Error('Sensitivity failed '+newval);
  console.log(newval+': nominal wall '+target+' mm; rounded wall recheck passes');
 }
 const bad=await h.hurmet2html(s.replace('EffectiveStress = 50','EffectiveStress = 0'));
 if(!bad.includes('Error.'))throw Error('Invalid effective stress not rejected');
 console.log(names.length+' results round-trip unchanged; two sensitivity cases and invalid-input guard passed.');
})();
