const fs=require('fs'),path=require('path'),crypto=require('crypto');
const h=require('../hurmet_display.cjs').checkingEngine(require(process.env.HURMET_ENGINE));globalThis.temml=require(process.env.TEMML_ENGINE);
const root=__dirname,file=path.join(root,'Itemized coolant pump estimate - Hurmet.md');
const results=JSON.parse(fs.readFileSync(path.join(root,'coolant-pump-itemized-results.json'),'utf8'));
function val(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet evaluation error');return out;}
function near(a,b,n){if(!Number.isFinite(a)||Math.abs(a-b)>3e-6*Math.max(Math.abs(b),.01))throw Error(`${n}: ${a} != ${b}`);}
function input(s,n,x){const pattern=new RegExp('¢` '+n+' = [^`]+`');if(!pattern.test(s))throw Error('Missing input '+n);return s.replace(pattern,'¢` '+n+' = '+x+' `');}
(async()=>{
 const source=fs.readFileSync(file,'utf8'),first=await calc(source),saved=await calc(first);
 for(const [n,v] of Object.entries(results.hurmet_checks)){near(val(saved,n),v,n);near(val(first,n),val(saved,n),'reopen '+n);}
 const eta=await calc(input(saved,'PumpEfficiency','0.75'));
 near(val(eta,'TotalElectrical'),val(saved,'TotalElectrical')*.8/.75,'efficiency sensitivity');near(val(eta,'PumpRise'),val(saved,'PumpRise'),'loss independent of efficiency');
 const length=await calc(input(saved,'SGTubeLength',(results.inputs.SGTubeLength.value*1.1)+' m'));
 near(val(length,'SGFriction'),1.1*val(saved,'SGFriction'),'SG length scaling');near(val(length,'SGEnds'),val(saved,'SGEnds'),'SG ends independent of length');
 const bends=await calc(input(saved,'BendK','0.6'));near(val(bends,'BendLoss'),2*val(saved,'BendLoss'),'bend coefficient sensitivity');
 near(val(bends,'PumpRise'),val(saved,'PumpRise')+val(saved,'BendLoss'),'itemized addition');
 fs.writeFileSync(file,await h.forDisplay(saved));const preview=path.join(root,'outputs','coolant-pump-itemized');fs.mkdirSync(preview,{recursive:true});fs.writeFileSync(path.join(preview,'coolant-pump-itemized.html'),await h.hurmet2html(saved));
 const report={passed:true,numerical_comparisons:Object.keys(results.hurmet_checks).length,checks:['independent SI/Colebrook calculation','save/reopen','efficiency sensitivity','SG length scaling','bend K and itemized sum'],engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(process.env.HURMET_ENGINE)).digest('hex')};
 fs.writeFileSync(path.join(root,'coolant-pump-itemized-hurmet-checks.json'),JSON.stringify(report,null,2)+'\n');console.log(report);
})().catch(e=>{console.error(e);process.exit(1)});
