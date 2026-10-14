const fs=require('fs'),path=require('path'),crypto=require('crypto');
const h=require(process.env.HURMET_ENGINE);globalThis.temml=require(process.env.TEMML_ENGINE);
const root=__dirname,file=path.join(root,'Normal coolant pressure profile - Hurmet.md');
const results=JSON.parse(fs.readFileSync(path.join(root,'coolant-pressure-results.json'),'utf8'));
function val(s,n){const m=s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet evaluation error');return out;}
function near(a,b,n){if(!Number.isFinite(a)||Math.abs(a-b)>Math.max(1e-7,3e-6*Math.abs(b)))throw Error(`${n}: ${a} != ${b}`);}
function input(s,n,x){const pattern=new RegExp('¢` '+n+' = [^`]+`');if(!pattern.test(s))throw Error('Missing input '+n);return s.replace(pattern,'¢` '+n+' = '+x+' `');}
(async()=>{
 const source=fs.readFileSync(file,'utf8'),first=await calc(source),saved=await calc(first);
 for(const [n,v] of Object.entries(results.hurmet_checks)){near(val(saved,n),v,n);near(val(saved,n),val(first,n),'reopen '+n);}
 const names=['SGIn','SGOut','Suction','Discharge','ReactorIn','Bottom','ReactorOut'];
 const lower=await calc(input(saved,'TopPressure','50000 Pa'));
 for(const c of ['Base','Low','High'])for(const n of names)near(val(lower,c+n),val(saved,c+n)-.5,'reference shift '+c+n);
 const raised=await calc(input(saved,'TopZ','18 m'));
 for(const n of names)near(val(raised,'Base'+n),val(saved,'Base'+n)+val(saved,'Gradient'),'reference elevation '+n);
 const i=results.inputs;
 const z={SGIn:'SGInZ',SGOut:'SGOutZ',Suction:'SuctionZ',Discharge:'DischargeZ',ReactorIn:'ReactorInZ',Bottom:'BottomZ',ReactorOut:'ReactorOutZ'};
 for(const rho of [1611.2405,1656.3245]){
  const changed=await calc(input(saved,'Density',rho+' kg/m3'));
  for(const n of names)near(val(changed,'Base'+n),val(saved,'Base'+n)+(rho-i.Density.value)*i.Gravity.value*(i.TopZ.value-i[z[n]].value)/1e5,'hydrostatic density '+n);
  near(val(changed,'BasePumpRise'),val(saved,'BasePumpRise'),'density screen leaves imported losses fixed');
 }
 for(const c of ['Base','Low','High'])near(val(saved,c+'ClosureError'),0,'loop closure '+c);
 fs.writeFileSync(file,saved);const preview=path.join(root,'outputs','coolant-pressure');fs.mkdirSync(preview,{recursive:true});fs.writeFileSync(path.join(preview,'coolant-pressure.html'),await h.hurmet2html(saved));
 const report={passed:true,revision:'itemized',numerical_comparisons:Object.keys(results.hurmet_checks).length,checks:['independent pressure balances','save/reopen','three case loop closures','reference pressure shift','reference elevation shift','uniform-density hydrostatic sensitivities'],engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(process.env.HURMET_ENGINE)).digest('hex')};
 fs.writeFileSync(path.join(root,'coolant-pressure-hurmet-checks.json'),JSON.stringify(report,null,2)+'\n');console.log(report);
})().catch(e=>{console.error(e);process.exit(1)});
