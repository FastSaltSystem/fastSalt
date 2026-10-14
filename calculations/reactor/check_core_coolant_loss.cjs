const fs=require('fs'),path=require('path'),crypto=require('crypto');
const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const root=__dirname,file=path.join(root,'Core coolant pressure loss - Hurmet.md');
const results=JSON.parse(fs.readFileSync(path.join(root,'core-coolant-loss-results.json'),'utf8'));
function val(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet evaluation error');return out;}
function near(a,b,n){if(!Number.isFinite(a)||Math.abs(a-b)>3e-6*Math.max(Math.abs(b),.01))throw Error(`${n}: ${a} != ${b}`);}
(async()=>{
 const source=fs.readFileSync(file,'utf8'),first=await calc(source),saved=await calc(first);
 for(const [n,v] of Object.entries(results.hurmet_checks)){near(val(saved,n),v,n);near(val(saved,n),val(first,n),'reopen '+n);}
 const long=await calc(saved.replace('CoreLength = 3.4 m','CoreLength = 6.8 m'));
 near(val(long,'CoreFriction'),2*val(saved,'CoreFriction'),'length scaling');near(val(long,'EndLoss'),val(saved,'EndLoss'),'end loss independent of length');
 const half=await calc(saved.replace('MassFlow = 18500 kg/s','MassFlow = 9250 kg/s').replace('MassFlow = 18,500 kg/s','MassFlow = 9250 kg/s'));
 near(val(half,'Velocity'),val(saved,'Velocity')/2,'flow velocity scaling');near(val(half,'EndLoss'),val(saved,'EndLoss')/4,'local loss flow scaling');
 const rough=await calc(saved.replace(/¢` Roughness = [^`]+`/, '¢` Roughness = 0.00001 m `'));
 near(val(rough,'TotalLoss'),val(saved,'RougherTotalLoss'),'roughness sensitivity');
 fs.writeFileSync(file,saved);const preview=path.join(root,'outputs','core-coolant-loss');fs.mkdirSync(preview,{recursive:true});fs.writeFileSync(path.join(preview,'core-coolant-loss.html'),await h.hurmet2html(saved));
 const r={passed:true,numerical_comparisons:Object.keys(results.hurmet_checks).length,checks:['independent Colebrook solve','Hurmet save/reopen','length scaling','flow sensitivity','roughness sensitivity'],engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(process.env.HURMET_ENGINE)).digest('hex')};
 fs.writeFileSync(path.join(root,'core-coolant-loss-hurmet-checks.json'),JSON.stringify(r,null,2)+'\n');console.log(r);
})().catch(e=>{console.error(e);process.exit(1)});
