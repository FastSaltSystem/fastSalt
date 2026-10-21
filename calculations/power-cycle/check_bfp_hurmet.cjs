const fs=require('fs'),path=require('path');
const h=require('../hurmet_display.cjs').checkingEngine(require(process.env.HURMET_ENGINE));globalThis.temml=require(process.env.TEMML_ENGINE);
const dir=process.argv[2]||__dirname,file=path.join(dir,'BFP drive comparison - Hurmet.md');
function val(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.'))throw Error('Hurmet calculation error');return out;}
(async()=>{let src=fs.readFileSync(file,'utf8');let out=await calc(await calc(src));const expected=JSON.parse(fs.readFileSync(path.join(dir,'bfp-hurmet-checks.json'),'utf8'));
for(const[n,v]of Object.entries(expected))if(Math.abs(val(out,n)-v)>2e-6*Math.max(Math.abs(v),.01))throw Error(n+' differs: '+val(out,n)+' vs '+v);
const changed=await calc(src.replace('DriveEfficiency = 0.95','DriveEfficiency = 0.97'));
const model=JSON.parse(fs.readFileSync(path.join(dir,'bfp-drive-comparison.json'),'utf8'));
const reference=model.efficiency_sensitivity.find(x=>x.aux_turbine_eff===.8&&x.electric_eff===.97);
if(Math.abs(val(changed,'OutputPenalty')+reference.delta_MW)>1e-5)throw Error('Drive-efficiency sensitivity failed');
const html=await h.hurmet2html(out);if((html.match(/<table/g)||[]).length!==4||out.includes('NaN'))throw Error('Table serialization failed');
fs.writeFileSync(file,await h.forDisplay(out));fs.mkdirSync(path.join(dir,'preview'),{recursive:true});fs.writeFileSync(path.join(dir,'preview/bfp-drive-comparison.html'),await h.hurmet2html(out));console.log('Hurmet save/reopen, '+Object.keys(expected).length+' numerical comparisons, and efficiency sensitivity passed.');})().catch(e=>{console.error(e);process.exit(1)});
