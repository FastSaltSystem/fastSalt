const fs=require('fs'),path=require('path'),crypto=require('crypto');
const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const root=__dirname,file=path.join(root,'Normal coolant pressure profile - Hurmet.md');
const result=JSON.parse(fs.readFileSync(path.join(root,'coolant-pressure-results.json'),'utf8'));
function val(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet evaluation error');return out;}
function near(a,b,name){if(!Number.isFinite(a)||Math.abs(a-b)>3e-6*Math.max(Math.abs(b),.01))throw Error(`${name}: ${a} != ${b}`);}
(async()=>{
 const source=fs.readFileSync(file,'utf8'),first=await calc(source),saved=await calc(first);
 for(const [n,v] of Object.entries(result.hurmet_checks)){near(val(saved,n),v,n);near(val(first,n),val(saved,n),'reopen '+n);}
 const lower=await calc(saved.replace('TopPressure = 1 bar','TopPressure = 0.5 bar'));
 for(const n of ['SGInPressure','SGOutPressure','SuctionLow','SuctionHigh','DischargeLow','DischargeHigh','BottomLow','BottomHigh'])near(val(lower,n),val(saved,n)-.5,'bias shift '+n);
 for(const density of [2112.68-.5635*875,2112.68-.5635*810]){
  const changed=await calc(saved.replace('Density = 1637.93125 kg/m3',`Density = ${density} kg/m3`));
  const i=result.inputs,g=i.Gravity.value,zt=i.TopZ.value,loss=i.SGLoss.value*1000;
  near(val(changed,'SuctionLow'),(1e5+density*g*(zt-i.SuctionZ.value)-1.5*loss)/1e5,'density suction');
  near(val(changed,'BottomHigh'),(1e5+density*g*(zt-i.BottomZ.value)+.5*loss)/1e5,'density bottom');
 }
 fs.writeFileSync(file,saved);const preview=path.join(root,'outputs','coolant-pressure');fs.mkdirSync(preview,{recursive:true});
 fs.writeFileSync(path.join(preview,'coolant-pressure.html'),await h.hurmet2html(saved));
 const report={passed:true,numerical_comparisons:Object.keys(result.hurmet_checks).length,checks:['Hurmet recalculation and save/reopen','0.5 bar reference-pressure shift','hot and cold uniform-density sensitivities'],engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(process.env.HURMET_ENGINE)).digest('hex')};
 fs.writeFileSync(path.join(root,'coolant-pressure-hurmet-checks.json'),JSON.stringify(report,null,2)+'\n');console.log(report);
})().catch(e=>{console.error(e);process.exit(1)});
