const fs=require('fs'),path=require('path');const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const {pipeTables,withHurmetWidths}=require('./hurmet_pipe_tables.cjs');
const file=path.join(__dirname,'Open-air Brayton cooler - Hurmet.md');
function val(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(withHurmetWidths(s)),html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet error');return out;}
(async()=>{const src=fs.readFileSync(file,'utf8'),out=await calc(await calc(src));const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'open-air-brayton-results.json'),'utf8')).hurmet_checks;
for(const[n,v]of Object.entries(expected))if(Math.abs(val(out,n)-v)>2e-6*Math.max(Math.abs(v),.01))throw Error(n+': '+val(out,n)+' != '+v);
const altered=await calc(src.replace('GeneratorEfficiency = 0.95','GeneratorEfficiency = 0.9'));
if(Math.abs(val(altered,'AvailableElectricity')/val(out,'AvailableElectricity')-.9/.95)>1e-6)throw Error('Alternator sensitivity');
const saved=pipeTables(out);const html=await h.hurmet2html(withHurmetWidths(saved));if((html.match(/<table/g)||[]).length!==3)throw Error('Expected three tables');fs.writeFileSync(file,saved);fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});fs.writeFileSync(path.join(__dirname,'preview/open-air-brayton.html'),html);console.log('Passed 10 numerical comparisons, save/reopen, alternator sensitivity and three tables.');
})().catch(e=>{console.error(e);process.exit(1)});
