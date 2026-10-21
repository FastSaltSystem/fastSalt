const fs=require('fs');
const hp=process.env.HURMET_ENGINE;
if(!hp)throw Error('Set HURMET_ENGINE to the official Hurmet bundle');
const h=require('../../hurmet_display.cjs').checkingEngine(require(hp));globalThis.temml=require(hp.replace(/hurmet\.cjs$/,'temml.cjs'));
const p=process.argv[2] || require('path').join(__dirname,'..','Steam and feedwater pipe sizing - Hurmet.md');
function result(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function check(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.'))throw Error('Hurmet calculation error');return out;}
(async()=>{const source=fs.readFileSync(p,'utf8');const normal=await check(source);await check(normal);
for(const [oldval,newval,variable,relation] of [
 ['SteamDesignPressure = 30','SteamDesignPressure = 36','SHWall','greater'],
 ['SteamStress = 80','SteamStress = 60','SHWall','greater'],
 ['SteamVelocityLimit = 25','SteamVelocityLimit = 15','SHBore','greater'],
 ['GeneratorCount = 3','GeneratorCount = 4','SBBore','less']]){
 const changed=await check(source.replace(oldval,newval));let a=result(normal,variable),b=result(changed,variable);
 if(!(relation==='greater'?b>a:b<a))throw Error('Sensitivity failed '+variable);
 if(oldval.startsWith('GeneratorCount') && result(normal,'HeaderMass')!==result(changed,'HeaderMass'))throw Error('Total flow changed');
 console.log(oldval+' -> '+newval+': '+variable+' '+a+' -> '+b);
}
let bad=await h.hurmet2html(source.replace('SteamStress = 80','SteamStress = 1'));
if(!bad.includes('Invalid') || !bad.includes('combination'))throw Error('Invalid pressure/stress not rejected');
console.log('Round-trip, four sensitivity cases, and invalid-input guard passed.');
})();
