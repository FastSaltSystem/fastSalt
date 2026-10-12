import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
const root=path.resolve(process.argv[2] || '/Users/thomaswielenga/Documents/dev/fastSalt');
const workspaceDir=path.resolve(process.argv[3] || path.join(root,'outputs/rankine-diagram'));
await fs.mkdir(path.join(workspaceDir,'build'),{recursive:true});
const sourcePath=path.join(root,'calculations/power-cycle/reheat-selection.json');
const source=await fs.readFile(sourcePath,'utf8');
const d=JSON.parse(source).selected_at_5kPa;
const f=(v,n=0)=>v.toLocaleString('en-US',{minimumFractionDigits:n,maximumFractionDigits:n});
const T=k=>f(d.states[k].t-273.15,0);
const P=(k,n=2)=>f(d.states[k].p/1e6,n);
const p=Presentation.create({slideSize:{width:1920,height:1080}});
const s=p.slides.add(); s.background.fill='#FFFFFF';
const c={ink:'#183044',muted:'#5A6874',steam:'#B44722',water:'#166C9A',bleed:'#967228',salt:'#846038',pale:'#F2F6F8',light:'#CED8DE',cw:'#3E877E'};
let seq=0;
function shape(g,x,y,w,h,fill='white',stroke=c.ink,sw=2,name='') {return s.shapes.add({geometry:g,name:name||`${g}-${++seq}`,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw,style:'solid'}});}
function text(txt,x,y,w,h,size=27,color=c.ink,bold=false,align='left',bg='none') {const q=shape('textbox',x,y,w,h,bg,'none',0,txt.replace(/\n/g,' / '));q.text=txt;q.text.style={typeface:'Arial',fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',wrap:'none',autoFit:'none',insets:0};return q;}
function poly(pts,col=c.ink,sw=3,fill='none',closed=false,name='path') {const xs=pts.map(v=>v[0]),ys=pts.map(v=>v[1]),x=Math.min(...xs),y=Math.min(...ys),w=Math.max(1,Math.max(...xs)-x),h=Math.max(1,Math.max(...ys)-y);const cmd=pts.map((v,i)=>({[i?'lineTo':'moveTo']:{x:v[0]-x,y:v[1]-y}}));if(closed)cmd.push({close:{}});return s.shapes.add({geometry:'custom',name:`${name}-${++seq}`,position:{left:x,top:y,width:w,height:h},fill,line:{fill:col,width:sw,style:'solid'},customPaths:[{width:w,height:h,commands:cmd}]});}
function line(pts,col=c.steam,sw=4,arrow=true){poly(pts,col,sw);if(arrow){const b=pts.at(-1),a=pts.at(-2),dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy),ux=dx/l,uy=dy/l;poly([b,[b[0]-12*ux+5*uy,b[1]-12*uy-5*ux],[b[0]-12*ux-5*uy,b[1]-12*uy+5*ux]],col,1,col,true,'flow arrow');}}
function dot(x,y,col=c.steam){shape('ellipse',x-5,y-5,10,10,col,col,0);}
function box(txt,x,y,w,h){shape('rect',x,y,w,h,c.pale,c.ink,2);text(txt,x+5,y+5,w-10,h-10,27,c.ink,true,'center');}
function turbine(txt,x,y,w=145,h=130){poly([[x,y+30],[x+w,y],[x+w,y+h],[x,y+h-30]],c.ink,3,c.pale,true);text(txt,x+14,y+40,w-20,50,28,c.ink,true,'center');}
function pump(x,y,label){shape('ellipse',x-25,y-25,50,50,'white',c.water,3);poly([[x+12,y-13],[x-12,y],[x+12,y+13]],c.water,2,c.water,true);text(label,x-75,y+32,150,32,24,c.ink,false,'center');}
function hx(txt,x,y,w=115,h=50){box(txt,x,y,w,h);}
// Title and consistent reference-case summary.
text('Fast Salt System | Rankine power cycle',52,32,1480,64,48,c.ink,true);
text('Selected preliminary design • 5 kPa condenser reference case',55,99,1610,38,28,c.muted);
shape('rect',52,147,1816,61,c.pale,'none',0);
text(`1,500 MW thermal     →     ${f(d.gross/1e6)} MW gross electric     |     ${f(d.gross/15e6,1)}% gross efficiency`,78,157,1760,40,31,c.ink,true);
// Main steam circuit; all main flow paths use arrowheads.
line([[355,375],[355,246],[580,246],[580,393],[600,393]]);
line([[580,246],[975,246],[975,335]]);dot(580,246);
line([[745,393],[900,393]]);
line([[1050,393],[1210,393]]);
line([[1355,393],[1510,393]]);
line([[1655,393],[1880,393],[1880,635],[1850,635]]);
// Main equipment.
shape('roundRect',305,375,100,225,c.pale,c.ink,3);
text('Steam\ngenerators\n(3 × 500 MWt)',411,577,270,96,27,c.ink,true,'center');
poly([[330,410],[380,440],[330,470],[380,500],[330,530],[380,560]],c.ink,2);
turbine('HP',600,328);box('Steam\nreheater',900,335,150,115);turbine('IP',1210,328);turbine('LP',1510,328);
text('HP turbine',575,466,195,34,26,c.ink,true,'center');
text('Reheat turbine',1170,466,235,34,26,c.ink,true,'center');
text('LP turbine',1485,466,195,34,26,c.ink,true,'center');
text(`Main steam\n${P('main',0)} MPa • ${T('main')}°C\n${f(d.mass,1)} kg/s`,366,256,250,100,26,c.steam,true);
text(`Heating branch\n${f(d.mass*d.fractions.reheat,1)} kg/s`,708,259,263,66,26,c.steam);
text(`${P('HPex',1)} MPa\n${T('HPex')}°C`,761,329,137,58,25,c.steam,false,'center');
text(`${P('reheat_hot')} MPa\n${T('reheat_hot')}°C\n${f(d.reheat_flow,1)} kg/s`,1060,275,148,98,25,c.steam,true,'center');
text(`${P('IPex',2)} MPa\n${T('IPex')}°C`,1367,313,131,67,25,c.steam,true,'center');
text(`${f(d.reheat_duty/1e6)} MW reheat`,925,469,228,34,26,c.steam,true,'center');
text(`LP exhaust\n5 kPa • ${T('LPex')}°C\n${f(d.moisture*100,1)}% moisture`,1659,474,226,100,26,c.steam,true,'center');
// Reactor and molten-salt circuit.
box('WISTR',55,438,130,125);
line([[120,438],[120,375],[305,375]],c.salt,4);
line([[305,565],[255,565],[255,590],[120,590],[120,563]],c.salt,4);
shape('ellipse',227,540,55,55,'white',c.salt,3);text('P',231,544,47,46,27,c.salt,true,'center');
text('Salt\n602°C',174,312,100,65,25,c.salt);
text('537°C',167,599,100,34,25,c.salt);
text('Coolant pump',50,641,190,34,24,c.salt);
// Turbine output symbols and shaft links (schematic grouping).
line([[670,501],[670,539],[1320,539]],c.muted,2,false);
line([[1280,501],[1280,539]],c.muted,2,false);
shape('ellipse',1320,514,50,50,'white',c.ink,2);text('G',1326,519,38,40,25,c.ink,true,'center');
line([[1580,501],[1580,539],[1515,539]],c.muted,2,false);
shape('ellipse',1465,514,50,50,'white',c.ink,2);text('G',1471,519,38,40,25,c.ink,true,'center');
// Condenser and cooling-water connections.
shape('rect',1600,590,250,90,c.pale,c.ink,2);text('Condenser',1605,600,240,36,27,c.ink,true,'center');
text(`${f(d.qcond/1e6)} MW rejected`,1608,643,230,30,25,c.cw,false,'center');
line([[1560,610],[1600,610]],c.cw,3);line([[1600,660],[1560,660]],c.cw,3);
text('Cooling water\n19.8 → 27.9°C\n23.8 m³/s',1340,588,207,98,25,c.cw,false,'center');
// Heating-stream outlet shown with a destination tag to avoid spaghetti.
line([[910,450],[910,525],[885,525]],c.bleed,3);
text('Heating return → HP4\n24 MPa • 380°C¹',685,552,306,66,25,c.bleed);
// Boiler-feed-pump steam turbine, with explicitly summarized source/destination.
box('Feed-pump\nturbine',1035,590,190,75);
text('From HP: 7.64 MPa / 378°C',1018,553,332,32,23,c.bleed);
line([[1115,580],[1115,590]],c.bleed,3);
text('21.4 MW shaft',993,669,176,32,23,c.muted,false,'center');
line([[1170,665],[1170,725],[1120,725],[1120,808]],c.bleed,3);
text('Exhaust\n0.60 MPa',1190,706,144,58,23,c.bleed);
// Regenerative feed train: flow runs right to left.
line([[1740,680],[1740,810]],c.water,4);
pump(1740,840,'Cond. pump');
line([[1715,840],[1645,840]],c.water,4);
const hp=[{x:305,n:'HP4',t:287,p:'7.64',src:'HP + RH¹'}, {x:455,n:'HP3',t:225,p:'2.80',src:'HP exhaust'}, {x:605,n:'HP2',t:196,p:'1.60',src:'Pump turbine'}, {x:755,n:'HP1',t:175,p:'1.00',src:'Pump turbine'}];
const lp=[{x:1205,n:'LP3',t:107,p:'0.155'}, {x:1365,n:'LP2',t:95,p:'0.100'}, {x:1525,n:'LP1',t:64,p:'0.030'}];
line([[915,840],[870,840]],c.water,4);
line([[1035,840],[965,840]],c.water,4);
pump(940,840,'Feed pump');
box('Deaerator',1035,808,145,64);
text('0.60 MPa\n159°C',1038,880,142,64,25,c.water,true,'center');
line([[1205,840],[1180,840]],c.water,4);
for(let i=0;i<hp.length;i++){
 const q=hp[i];hx(q.n,q.x,815);text(`${q.t}°C`,q.x,877,115,32,25,c.water,true,'center');
 text(q.src,q.x-17,726,150,30,21,c.bleed,false,'center');text(`${q.p} MPa`,q.x-15,760,145,30,23,c.bleed,false,'center');line([[q.x+58,792],[q.x+58,815]],c.bleed,2);
 if(i<hp.length-1)line([[hp[i+1].x,840],[q.x+115,840]],c.water,4);
}
for(let i=0;i<lp.length;i++){
 const q=lp[i];hx(q.n,q.x,815);text(`${q.t}°C`,q.x,877,115,32,25,c.water,true,'center');
 text(`${q.p} MPa`,q.x-14,763,143,30,23,c.bleed,false,'center');line([[q.x+58,796],[q.x+58,815]],c.bleed,2);
 if(i<lp.length-1)line([[lp[i+1].x,840],[q.x+115,840]],c.water,4);
}
line([[305,840],[260,840],[260,718],[355,718],[355,600]],c.water,4);
text('Feedwater → SG\n24 MPa • 287°C',65,748,210,67,25,c.water,true);
text('24 MPa\n163°C',872,921,143,62,25,c.water,false,'center');
text('0.72 MPa\n33°C',1707,909,150,62,25,c.water,false,'center');
text('HP feedwater heaters',369,680,486,38,29,c.ink,true,'center');
text('LP feedwater heaters',1307,709,336,38,29,c.ink,true,'center');
text('LP turbine bleeds',1360,746,250,26,21,c.bleed,false,'center');
text('Water outlet temperatures shown below heaters',339,924,526,32,23,c.water);
// Footer legend and important engineering qualifiers.
shape('rect',52,995,1816,2,c.light,'none',0);
line([[58,1025],[110,1025]],c.steam,4,false);text('Steam',121,1008,100,33,24,c.steam);
line([[234,1025],[286,1025]],c.water,4,false);text('Water',297,1008,100,33,24,c.water);
line([[410,1025],[462,1025]],c.bleed,3,false);text('Heating / extraction',473,1008,276,33,24,c.bleed);
text('Pressures absolute • Gross output; net auxiliaries pending',864,1006,1000,34,24,c.muted,false,'right');
text('¹ Heating return throttles into HP4. Heater drains cascade to deaerator (HP) / condenser (LP); small lines summarized.',55,1045,1810,25,21,c.muted);
s.speakerNotes.text=`Fast Salt System — preliminary Rankine cycle, 11 October 2026. Layout redrawn from Thomas J. Wielenga's supplied Diagram.pdf (23 April 2025), ${'/Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Steam Generator/graphics/Diagram.pdf'}. Calculated states: ${sourcePath}, selected_at_5kPa. SHA-256: ${createHash('sha256').update(source).digest('hex')}. Official calculation commentary: calculations/power-cycle/Selected reheat and wetness - Hurmet.md. All pressures absolute. The 5 kPa reference, not the coupled 20°C cooling case, is used consistently. Main steam 711.670 kg/s, heating branch 187.006 kg/s, hot reheat 415.329 kg/s, LP exhaust 361.044 kg/s. Gross 678.723 MW (45.248%); no net power claim. Feed-pump turbine shaft 21.435 MW is already allowed in the cycle flow calculation. Reheater minimum approach 20.276 K. HP exhaust 2.8 MPa/253°C becomes 2.66 MPa/250.7°C after the reheater inlet loss. Heating fluid remains at 24 MPa until throttled into HP4; it is not an isothermal condensing stream. LP moisture is equilibrium exhaust moisture, not a supplier wetness guarantee. Condenser reference cooling water 19.820/27.932°C and 23.763 m³/s. SG salt 875/810 K from the inherited generator design. Three SG represented in aggregate. HP/IP and LP generator symbols preserve the source schematic, not a selected shaft-line design. Bleed and drain lines are summarized: HP4 at7.644 MPa also takes heating return; HP3 at2.8 MPa; HP2/HP1 at1.6/1.0 MPa from feed pump turbine; its0.6 MPa exhaust supplies deaerator. LP3/2/1 at0.155246/0.1/0.03 MPa. HP drains cascade4→3→2→1→DA; LP drains3→2→1→condenser. Feedwater pressure losses other than modeled pumps are not yet resolved. Preliminary performance and equipment arrangement; supplier verification pending.`;
await (await PresentationFile.exportPptx(p)).save(path.join(workspaceDir,'build/candidate.pptx'));
const img=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(workspaceDir,'build/preview.png'),new Uint8Array(await img.arrayBuffer()));
console.log('Built editable diagram and preview.');
