// Recalculate the actual Hurmet worksheet; compare to independent Python arithmetic.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const root=__dirname,file=path.join(root,'Coolant inventory and storage capacity - Hurmet.md');
const results=JSON.parse(fs.readFileSync(path.join(root,'coolant-inventory-results.json'),'utf8'));
function val(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN')){fs.writeFileSync(path.join(root,'hurmet-error.html'),html);throw Error('Hurmet evaluation error');}return out;}
function near(a,b,name){if(!Number.isFinite(a)||Math.abs(a-b)>3e-6*Math.max(Math.abs(b),.01))throw Error(`${name}: ${a} != ${b}`);}
(async()=>{
 const source=fs.readFileSync(file,'utf8'),first=await calc(source),saved=await calc(first);
 for(const [n,v] of Object.entries(results.hurmet_checks)){near(val(saved,n),v,n);near(val(first,n),val(saved,n),'reopen '+n);}
 const bigger=await calc(saved.replace('TankOD = 4 m','TankOD = 6 m'));
 near(val(bigger,'TankWorking')/val(saved,'TankWorking'),Math.pow((6-.05)/(4-.05),2),'Tank diameter sensitivity');
 const warmer=await calc(saved.replace('FillTemperature = 723.15 K','FillTemperature = 773.15 K'));
 const scenario=results.fill_temperature_sensitivity.find(x=>x.fill_temperature_K===773.15);
 near(val(warmer,'FullDrainHot'),scenario.hot_drain_m3,'Fill temperature mass conservation');
 near(val(warmer,'NormalExpansionVolume'),scenario.normal_expansion_m3,'Expansion temperature sensitivity');
 const cooler=await calc(saved.replace('StoreTemperature = 723.15 K','StoreTemperature = 773.15 K'));
 const density=2112.8-.56355*773.15;
 near(val(cooler,'FullDrainStore'),results.hurmet_checks.ChargeMass/density,'Storage temperature sensitivity');
 near(val(cooler,'FullDrainHot'),val(saved,'FullDrainHot'),'Hot drain independent of storage temperature');
 fs.writeFileSync(file,saved);const preview=path.join(root,'outputs','coolant-inventory');fs.mkdirSync(preview,{recursive:true});
 fs.writeFileSync(path.join(preview,'coolant-inventory.html'),await h.hurmet2html(saved));
 const report={passed:true,numerical_comparisons:Object.keys(results.hurmet_checks).length,checks:['Hurmet save/reopen','tank diameter sensitivity','fill temperature mass balance','storage temperature sensitivity'],engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(process.env.HURMET_ENGINE)).digest('hex')};
 fs.writeFileSync(path.join(root,'coolant-inventory-hurmet-checks.json'),JSON.stringify(report,null,2)+'\n');console.log(report);
})().catch(e=>{console.error(e);process.exit(1)});
