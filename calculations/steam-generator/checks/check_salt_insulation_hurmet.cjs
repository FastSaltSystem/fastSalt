const fs=require('fs');
const hp=process.env.HURMET_ENGINE;
if(!hp)throw Error('Set HURMET_ENGINE to the official Hurmet bundle');
const h=require('../../hurmet_display.cjs').checkingEngine(require(hp));globalThis.temml=require(hp.replace(/hurmet\.cjs$/,'temml.cjs'));
const p=process.argv[2] || require('path').join(__dirname,'..','Molten-salt coolant insulation - Hurmet.md');
function result(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function check(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.'))throw Error('Hurmet calculation error');return out;}
(async()=>{
 const source=fs.readFileSync(p,'utf8');const normal=await check(source);const roundtrip=await check(normal);
 const names=[...source.matchAll(/¢(?:\?\?|%%)` (\w+) =/g)].map(m=>m[1]);
 for(const n of names)if(result(normal,n)!==result(roundtrip,n))throw Error('Roundtrip changed '+n);
 for(const [oldval,newval] of [ ['Ambient = 313.15','Ambient = 323.15'], ['Conductivity = 0.09','Conductivity = 0.11'], ['Emissivity = 0.2','Emissivity = 0.1'] ]){
  if(!source.includes(oldval))throw Error('Missing input '+oldval);
  const changed=await check(source.replace(oldval,newval));
  if(result(changed,'HotThickness')<=result(normal,'HotThickness'))throw Error('Sensitivity failed '+oldval);
  console.log(newval+': hot-leg thickness '+result(changed,'HotThickness')+' mm');
 }
 const bad=await h.hurmet2html(source.replace('Ambient = 313.15','Ambient = 340'));
 if(!bad.includes('Error.'))throw Error('Invalid target/ambient not rejected');
 console.log(names.length+' results round-trip unchanged; three sensitivities and invalid-input guard passed.');
})();
