const fs=require('fs'),path=require('path'),crypto=require('crypto');
const h=require('../hurmet_display.cjs').checkingEngine(require(process.env.HURMET_ENGINE));globalThis.temml=require(process.env.TEMML_ENGINE);
const file=path.join(__dirname,'Absorber capacity and gas modules - Hurmet.md');
const r=JSON.parse(fs.readFileSync(path.join(__dirname,'absorber-capacity-results.json')));
function val(s,n){const m=s.match(new RegExp('¢(?:\\?\\?|%%)` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'));if(!m)throw Error('Missing '+n);return Number(m[1].replaceAll(',',''));}
function near(a,b,n){if(!Number.isFinite(a)||Math.abs(a-b)>Math.max(1e-7,4e-6*Math.abs(b)))throw Error(`${n}: ${a} != ${b}`);}
async function calc(s){const out=await h.updateAndSave(s);const html=await h.hurmet2html(out);if(html.includes('Error.')||out.includes('NaN'))throw Error('Hurmet evaluation error');return out;}
(async()=>{
 const original=fs.readFileSync(file,'utf8'),first=await calc(original),saved=await calc(first);
 for(const [n,x] of Object.entries(r.hurmet_checks)){near(val(saved,n),n==='Gradient'||n.endsWith('P0')||n.endsWith('Final')?x/1000:x,n);near(val(saved,n),val(first,n),'reopen '+n);}
 const changed=await calc(saved.replace(/¢` WallTrial = [^`]+`/,'¢` WallTrial = 0.004 m `'));
 near(val(changed,'TrialNetL'),1000*(2.1-.012)*(.08-.008)*3.4,'wall sensitivity');
 const moved=await calc(saved.replace(/¢` ReservoirBottom = [^`]+`/,'¢` ReservoirBottom = 0.95 m `'));
 for(const p of ['ActivePrimary','ActiveSecondary','UpperPrimary','UpperSecondary'])near(val(moved,p+'P0')-val(saved,p+'P0'),r.head_gradient_Pa_m/1000,'elevation '+p);
 fs.writeFileSync(file,await h.forDisplay(saved));const out=path.join(__dirname,'outputs','absorber-capacity');fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'absorber-capacity.html'),(await h.hurmet2html(saved)).replaceAll('src="assets/', 'src="../../assets/'));
 const checks={passed:true,equations:Object.keys(r.hurmet_checks).length,checks:['Python numerical comparison','save and reopen','absorber tank-wall sensitivity','reservoir elevation sensitivity'],engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(process.env.HURMET_ENGINE)).digest('hex')};
 fs.writeFileSync(path.join(__dirname,'absorber-capacity-hurmet-checks.json'),JSON.stringify(checks,null,2)+'\n');console.log(checks);
})().catch(e=>{console.error(e);process.exit(1)});
