// Run: node checks/check_reactor_top.cjs /path/to/hurmet.cjs /path/to/temml.cjs
const fs=require('fs'),path=require('path'),assert=require('assert');
const h=require(process.argv[2]);globalThis.temml=require(process.argv[3]);
const source=fs.readFileSync(process.argv[4]||path.join(__dirname,'../Reactor top insulation - Hurmet.md'),'utf8');
const value=(s,n)=>Number(s.match(new RegExp('¢\\?\\?` '+n+' = (?:(?!`).)*?〔([^〕]+)〕','s'))[1].replaceAll(',',''));
(async()=>{
 const saved=await h.updateAndSave(source);
 assert(!(await h.hurmet2html(saved,'Check')).includes('Error.'));
 for(const m of source.matchAll(/¢\?\?` (\w+) =/g)) assert.equal(value(source,m[1]),value(saved,m[1]));
 const warmer=await h.updateAndSave(source.replace('Ambient = 313.15 K','Ambient = 323.15 K'));
 assert(value(warmer,'MinimumThickness')>800);
 assert.equal(value(warmer,'SelectedThickness'),900);
 assert(value(warmer,'SelectedSurface')<60);
 const bad=await h.updateAndSave(source.replace('SurfaceLimit = 333.15 K','SurfaceLimit = 303.15 K'));
 assert((await h.hurmet2html(bad,'Invalid target')).includes('Error.'));
 console.log('Hurmet round trip, edited ambient, and invalid-target guard passed.');
})();
