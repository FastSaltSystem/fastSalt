const fs=require('fs'),path=require('path');
const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Brayton-driven salt pump - Hurmet.md');
function value(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN')){fs.writeFileSync('/private/tmp/salt-pump-hurmet-error.html',html);throw Error('Hurmet calculation error');}return out;}
(async()=>{
 const src=fs.readFileSync(file,'utf8');const out=await calc(await calc(src));
 const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'brayton-salt-pump-results.json'),'utf8')).hurmet_checks;
 for(const[n,v]of Object.entries(expected))if(Math.abs(value(out,n)-v)>2e-6*Math.max(Math.abs(v),.01))throw Error(n+': '+value(out,n)+' != '+v);
 const alteredLoss=await calc(src.replace('LoopFactor = 1.5','LoopFactor = 2'));
 const alteredPump=await calc(src.replace('PumpEfficiency = 0.8','PumpEfficiency = 0.6'));
 for(const n of ['TwoPowerClosure','EightPowerClosure'])for(const test of [alteredLoss,alteredPump])if(Math.abs(value(test,n)-4/3)>1e-6)throw Error('Input sensitivity: '+n);
 const html=await h.hurmet2html(out);
 if((html.match(/<table/g)||[]).length!==3)throw Error('Expected three tables');
 fs.writeFileSync(file,out);fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});fs.writeFileSync(path.join(__dirname,'preview/brayton-salt-pump.html'),html);
 console.log('Passed '+Object.keys(expected).length+' numerical comparisons, save/reopen, loop-loss and efficiency sensitivity, and three tables.');
})().catch(e=>{console.error(e);process.exit(1)});
