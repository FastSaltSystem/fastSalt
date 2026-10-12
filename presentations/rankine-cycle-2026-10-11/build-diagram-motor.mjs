import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
const root=path.resolve(process.argv[2] || '/Users/thomaswielenga/Documents/dev/fastSalt');
const workspaceDir=path.resolve(process.argv[3] || path.join(root,'outputs/rankine-motor-bfp'));
await fs.mkdir(path.join(workspaceDir,'build'),{recursive:true});
const sourcePath=path.join(root,'calculations/power-cycle/bfp-drive-comparison.json');
const source=await fs.readFile(sourcePath,'utf8');
const study=JSON.parse(source), e=study.proposed_pressure_comparison.electric;
const oldPath=path.join(root,'calculations/power-cycle/reheat-selection.json');
const oldSource=await fs.readFile(oldPath,'utf8'),old=JSON.parse(oldSource).selected_at_5kPa;
const coolingPath=path.join(root,'calculations/power-cycle/cooling-cases.json');
const coolingSource=await fs.readFile(coolingPath,'utf8'),cool=JSON.parse(coolingSource);
const states={...old.states,IPex:e.heater_bleed_states.DA,LP3:e.heater_bleed_states.LP3,LP2:e.heater_bleed_states.LP2,LP1:e.heater_bleed_states.LP1,boiler_feed_pump:e.hp_feed[0],condensate_pump:e.lp_feed[0]};
const d={states,gross:e.gross_MW*1e6,mass:e.mass_kg_s,fractions:Object.fromEntries(Object.entries(e.flows_kg_s).map(([k,v])=>[k,v/e.mass_kg_s])),reheat_flow:e.reheat_flow_kg_s,reheat_duty:e.reheat_MW*1e6,qcond:e.condenser_MW*1e6,moisture:e.moisture_percent/100};
const capacity=cool.water_mass_kg_s*cool.water_cp_J_kgK;
const effectiveness=1-Math.exp(-cool.U_W_m2K*cool.area_m2/capacity);
const coolingIn=states.condenser.t-273.15-d.qcond/(capacity*effectiveness),coolingOut=coolingIn+d.qcond/capacity;

const f=(v,n=0)=>v.toLocaleString('en-US',{minimumFractionDigits:n,maximumFractionDigits:n});
const T=k=>f(d.states[k].t-273.15,0);
const P=(k,n=2)=>f(d.states[k].p/1e6,n);
const p=Presentation.create({slideSize:{width:1920,height:1080}});
const s=p.slides.add(); s.background.fill='#FFFFFF';
const c={ink:'#183044',muted:'#5A6874',steam:'#B44722',water:'#166C9A',bleed:'#967228',salt:'#846038',pale:'#F2F6F8',light:'#CED8DE',cw:'#3E877E'};
let seq=0; const tracks=[];
function shape(g,x,y,w,h,fill='white',stroke=c.ink,sw=2,name='') {return s.shapes.add({geometry:g,name:name||`${g}-${++seq}`,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw,style:'solid'}});}
function text(txt,x,y,w,h,size=27,color=c.ink,bold=false,align='left',bg='none') {const q=shape('textbox',x,y,w,h,bg,'none',0,txt.replace(/\n/g,' / '));q.text=txt;q.text.style={typeface:'Arial',fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',wrap:'none',autoFit:'none',insets:0};return q;}
function poly(pts,col=c.ink,sw=3,fill='none',closed=false,name='path') {const xs=pts.map(v=>v[0]),ys=pts.map(v=>v[1]),x=Math.min(...xs),y=Math.min(...ys),w=Math.max(1,Math.max(...xs)-x),h=Math.max(1,Math.max(...ys)-y);const cmd=pts.map((v,i)=>({[i?'lineTo':'moveTo']:{x:v[0]-x,y:v[1]-y}}));if(closed)cmd.push({close:{}});return s.shapes.add({geometry:'custom',name:`${name}-${++seq}`,position:{left:x,top:y,width:w,height:h},fill,line:{fill:col,width:sw,style:'solid'},customPaths:[{width:w,height:h,commands:cmd}]});}
function line(pts,col=c.steam,sw=4,arrow=true){tracks.push(pts);poly(pts,col,sw);if(arrow){const b=pts.at(-1),a=pts.at(-2),dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy),ux=dx/l,uy=dy/l;poly([b,[b[0]-12*ux+5*uy,b[1]-12*uy-5*ux],[b[0]-12*ux-5*uy,b[1]-12*uy+5*ux]],col,1,col,true,'flow arrow');}}
function dot(x,y,col=c.steam){shape('ellipse',x-5,y-5,10,10,col,col,0);}
function box(txt,x,y,w,h){shape('rect',x,y,w,h,c.pale,c.ink,2);text(txt,x+5,y+5,w-10,h-10,27,c.ink,true,'center');}
function turbine(txt,x,y,w=145,h=130){poly([[x,y+30],[x+w,y],[x+w,y+h],[x,y+h-30]],c.ink,3,c.pale,true);text(txt,x+9,y+30,w-16,78,26,c.ink,true,'center');}
function pump(x,y,label){shape('ellipse',x-25,y-25,50,50,'white',c.water,3);poly([[x+12,y-13],[x-12,y],[x+12,y+13]],c.water,2,c.water,true);text(label,x-75,y+32,150,32,24,c.ink,false,'center');}
function hx(txt,x,y,w=115,h=50){box(txt,x,y,w,h);}

// Orthogonal extraction routes with explicit bridges at non-junction crossings.
function route(pts,col=c.bleed){
 const pad=10, x=Math.min(...pts.map(a=>a[0]))-pad,y=Math.min(...pts.map(a=>a[1]))-pad;
 const w=Math.max(...pts.map(a=>a[0]))-x+pad,h=Math.max(...pts.map(a=>a[1]))-y+pad;
 const cmd=[{moveTo:{x:pts[0][0]-x,y:pts[0][1]-y}}];
 for(let i=1;i<pts.length;i++){
  const a=pts[i-1],b=pts[i],vert=a[0]===b[0],axis=vert?1:0,other=1-axis,dir=Math.sign(b[axis]-a[axis]);
  const cuts=[];
  for(const tr of tracks)for(let j=1;j<tr.length;j++){
   const q=tr[j-1],r=tr[j];if((q[0]===r[0])===vert)continue;
   const z=q[axis];
   if(z>Math.min(a[axis],b[axis])+10&&z<Math.max(a[axis],b[axis])-10&&a[other]>Math.min(q[other],r[other])+1&&a[other]<Math.max(q[other],r[other])-1)cuts.push(z);
  }
  for(const z of [...new Set(cuts)].sort((a,b)=>dir*(a-b))){
   if(vert){cmd.push({lineTo:{x:a[0]-x,y:z-dir*7-y}});cmd.push({cubicBezTo:{x1:a[0]+11-x,y1:z-dir*7-y,x2:a[0]+11-x,y2:z+dir*7-y,x:a[0]-x,y:z+dir*7-y}});}
   else{cmd.push({lineTo:{x:z-dir*7-x,y:a[1]-y}});cmd.push({cubicBezTo:{x1:z-dir*7-x,y1:a[1]-11-y,x2:z+dir*7-x,y2:a[1]-11-y,x:z+dir*7-x,y:a[1]-y}});}
  }
  cmd.push({lineTo:{x:b[0]-x,y:b[1]-y}});
 }
 s.shapes.add({geometry:'custom',name:`Extraction route ${++seq}`,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'white',width:8,style:'solid'},customPaths:[{width:w,height:h,commands:cmd}]});
 s.shapes.add({geometry:'custom',name:`Extraction route ${seq}`,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:col,width:3,style:'solid'},customPaths:[{width:w,height:h,commands:cmd}]});
 const b=pts.at(-1),a=pts.at(-2),l=Math.hypot(b[0]-a[0],b[1]-a[1]),ux=(b[0]-a[0])/l,uy=(b[1]-a[1])/l;
 poly([b,[b[0]-12*ux+5*uy,b[1]-12*uy-5*ux],[b[0]-12*ux-5*uy,b[1]-12*uy+5*ux]],col,1,col,true,'flow arrow');tracks.push(pts);
}

// Title and consistent reference-case summary.
text('Fast Salt System | Rankine power cycle',52,32,1480,64,48,c.ink,true);
text('Motor-driven boiler feed pump • Preliminary cycle at 5 kPa condenser pressure',55,99,1610,38,28,c.muted);
shape('rect',52,147,1816,61,c.pale,'none',0);
text(`1,500 MW thermal   →   ${f(d.gross/1e6,1)} MW gross   |   ${f(e.partial_net_MW,1)} MW after BFP + condensate pumps*`,78,157,1760,40,30,c.ink,true);
// Main steam circuit; all main flow paths use arrowheads.
line([[355,375],[355,246],[580,246],[580,393],[600,393]]);
line([[580,246],[975,246],[975,335]]);dot(580,246);
line([[745,393],[900,393]]);
line([[1050,393],[1210,393]]);
line([[1355,393],[1510,393]]);
line([[1655,393],[1880,393],[1880,635],[1850,635]]);
// Main equipment.
shape('roundRect',305,375,100,225,c.pale,c.ink,3);
text('Steam\ngenerators\n(3 × 500 MWt)',414,394,170,102,27,c.ink,true,'center');
poly([[330,410],[380,440],[330,470],[380,500],[330,530],[380,560]],c.ink,2);
turbine('HP\nturbine',600,328);box('Steam\nreheater',900,335,150,115);turbine('Reheat\n(IP)',1210,328);turbine('LP\nturbine',1510,328);



text(`Main steam\n${P('main',0)} MPa • ${T('main')}°C\n${f(d.mass,1)} kg/s`,366,256,250,100,26,c.steam,true);
text(`Heating branch\n${f(d.mass*d.fractions.reheat,1)} kg/s`,708,259,263,66,26,c.steam);
text(`${P('HPex',1)} MPa\n${T('HPex')}°C`,761,329,137,58,25,c.steam,false,'center');
text(`${P('reheat_hot')} MPa\n${T('reheat_hot')}°C\n${f(d.reheat_flow,1)} kg/s`,1060,275,148,98,25,c.steam,true,'center');
text(`${P('IPex',2)} MPa\n${T('IPex')}°C`,1367,313,131,67,25,c.steam,true,'center');
text(`${f(d.reheat_duty/1e6)} MW reheat`,1000,442,215,34,26,c.steam,true,'center');
text(`LP exhaust\n5 kPa • ${T('LPex')}°C\n${f(d.moisture*100,1)}% moisture`,1659,474,226,100,26,c.steam,true,'center');
// Reactor and molten-salt circuit.
box('WISTR',55,438,130,125);
line([[120,438],[120,375],[305,375]],c.salt,4);
line([[305,565],[255,565],[255,590],[120,590],[120,563]],c.salt,4);
shape('ellipse',227,540,55,55,'white',c.salt,3);text('P',231,544,47,46,27,c.salt,true,'center');
text('Salt\n602°C',174,312,100,65,25,c.salt);
text('537°C',167,599,100,34,25,c.salt);
text('Coolant pump',50,641,190,34,24,c.salt);
// Shaft lines remain separate from the steam extraction paths.
line([[670,444],[670,490],[1320,490]],c.muted,2,false);
line([[1280,444],[1280,490]],c.muted,2,false);
shape('ellipse',1320,465,50,50,'white',c.ink,2);text('G',1326,470,38,40,25,c.ink,true,'center');
line([[1580,444],[1580,490],[1515,490]],c.muted,2,false);
shape('ellipse',1465,465,50,50,'white',c.ink,2);text('G',1471,470,38,40,25,c.ink,true,'center');
// Condenser and cooling-water connections.
shape('rect',1600,590,250,90,c.pale,c.ink,2);text('Condenser',1605,600,240,36,27,c.ink,true,'center');
text(`${f(d.qcond/1e6)} MW rejected`,1608,643,230,30,25,c.cw,false,'center');
line([[1560,610],[1600,610]],c.cw,3);line([[1600,660],[1560,660]],c.cw,3);
text(`Cooling water\n${f(coolingIn,1)} → ${f(coolingOut,1)}°C\n${f(cool.water_volume_m3_s,1)} m³/s`,1340,594,207,88,25,c.cw,false,'center');
// Electric BFP drive, shown in aggregate for the two operating pump trains.
text('24 MPa / 380°C¹',442,498,182,29,23,c.bleed);
text(`${f(e.bfp_electric_MW,1)} MW electric`,850,695,264,32,25,c.water,true,'center');
shape('ellipse',912,737,56,56,'white',c.water,3);
text('M',918,741,44,47,28,c.water,true,'center');
line([[940,793],[940,815]],c.muted,4,false);
text('BFP motor',977,746,150,32,24,c.ink);
text(`${f(e.bfp_shaft_MW,1)} MW shaft`,977,779,175,28,22,c.muted);

// Regenerative feed train: flow runs right to left.
line([[1740,680],[1740,810]],c.water,4);
pump(1740,840,'Cond. pump');
line([[1715,840],[1645,840]],c.water,4);
const hp=[{x:305,n:'HP4',t:f(e.hp_feed[4].t-273.15),p:'7.64'}, {x:455,n:'HP3',t:f(e.hp_feed[3].t-273.15),p:'2.80'}, {x:605,n:'HP2',t:f(e.hp_feed[2].t-273.15),p:'1.60'}, {x:755,n:'HP1',t:f(e.hp_feed[1].t-273.15),p:'1.00'}];
const lp=[{x:1205,n:'LP3',t:f(e.lp_feed[3].t-273.15),p:f(e.inputs.plp3/1e6,3)}, {x:1365,n:'LP2',t:f(e.lp_feed[2].t-273.15),p:'0.100'}, {x:1525,n:'LP1',t:f(e.lp_feed[1].t-273.15),p:'0.030'}];
line([[915,840],[870,840]],c.water,4);
line([[1035,840],[965,840]],c.water,4);
pump(940,840,'Feed pump');
box('Deaerator',1035,808,145,64);
text('0.60 MPa\n159°C',1038,880,142,64,25,c.water,true,'center');
line([[1205,840],[1180,840]],c.water,4);
for(let i=0;i<hp.length;i++){
 const q=hp[i];hx(q.n,q.x,815);text(`${q.t}°C`,q.x,877,115,32,25,c.water,true,'center');
 text(`${q.p}\nMPa`,q.x-23,750,72,55,23,c.bleed,false,'center');
 if(i<hp.length-1)line([[hp[i+1].x,840],[q.x+115,840]],c.water,4);
}
for(let i=0;i<lp.length;i++){
 const q=lp[i];hx(q.n,q.x,815);text(`${q.t}°C`,q.x,877,115,32,25,c.water,true,'center');
 text(`${q.p}\nMPa`,q.x-23,750,72,55,23,c.bleed,false,'center');
 if(i<lp.length-1)line([[lp[i+1].x,840],[q.x+115,840]],c.water,4);
}
line([[305,840],[260,840],[260,718],[355,718],[355,600]],c.water,4);
text('Feedwater → SG\n24 MPa • 287°C',65,748,210,67,25,c.water,true);
text(`26.5 MPa\n${T('boiler_feed_pump')}°C`,872,921,143,62,25,c.water,false,'center');
text(`1.0 MPa\n${T('condensate_pump')}°C`,1707,909,150,62,25,c.water,false,'center');
text('HP feedwater heaters',321,924,486,38,29,c.ink,true,'center');
text('LP feedwater heaters',1230,924,440,38,28,c.ink,true,'center');


// Full heating and extraction connections. Dots mark real tees; bridges do not join.
route([[630,434],[630,570],[465,570],[465,730],[363,730],[363,815]]); // HP4

route([[810,393],[810,600],[513,600],[513,815]]);dot(810,393,c.steam); // HP3
route([[975,450],[975,530],[435,530],[435,710],[363,710],[363,730]]);dot(363,730,c.bleed); // RH -> HP4
// Throttle on reheater heating return, upstream of the HP4 junction.
poly([[426,645],[444,665],[426,665],[444,645]],c.bleed,2,'white',true,'Throttle valve');
route([[1240,435],[1240,650],[663,650],[663,815]]); // HP2, main IP extraction
route([[1290,445],[1290,680],[813,680],[813,815]]); // HP1, main IP extraction
route([[1400,393],[1400,530],[1160,530],[1160,808]]);dot(1400,393,c.steam); // DA, main IP outlet
route([[1530,432],[1530,548],[1263,548],[1263,815]]); // LP3
route([[1590,445],[1590,578],[1320,578],[1320,695],[1423,695],[1423,815]]); // LP2
route([[1640,455],[1640,560],[1550,560],[1550,690],[1583,690],[1583,815]]); // LP1 (moved around condenser below)

// Footer legend and important engineering qualifiers.
shape('rect',52,995,1816,2,c.light,'none',0);
line([[58,1025],[110,1025]],c.steam,4,false);text('Steam',121,1008,100,33,24,c.steam);
line([[234,1025],[286,1025]],c.water,4,false);text('Water',297,1008,100,33,24,c.water);
line([[410,1025],[462,1025]],c.bleed,3,false);text('Heating / extraction',473,1008,276,33,24,c.bleed);
text('Pressures absolute • *Other station loads excluded',864,1006,1000,34,24,c.muted,false,'right');
text('Dots = junctions; bridges = crossings. ¹ Return throttles into HP4. Drains cascade to deaerator (HP) / condenser (LP), not drawn.',55,1045,1810,25,21,c.muted);
s.speakerNotes.text=`Fast Salt System — motor-driven boiler feed pump alternative, 11 October 2026. Layout adapted from the prior editable cycle diagram, originating with Thomas J. Wielenga's supplied Diagram.pdf (23 April 2025). Source: ${sourcePath}, proposed_pressure_comparison.electric, SHA-256 ${createHash('sha256').update(source).digest('hex')}. Original common state source: ${oldPath}, SHA-256 ${createHash('sha256').update(oldSource).digest('hex')}. Cooling envelope: ${coolingPath}, SHA-256 ${createHash('sha256').update(coolingSource).digest('hex')}. Official calculation: calculations/power-cycle/BFP drive comparison - Hurmet.md. All pressures absolute. Main flow ${e.mass_kg_s} kg/s; gross ${e.gross_MW} MW; BFP ${e.bfp_shaft_MW} MW shaft and ${e.bfp_electric_MW} MW electrical, assumed combined drive efficiency 95%; condensate pump ${e.cep_electric_MW} MW electrical; remainder ${e.partial_net_MW} MW excludes all other station loads. This is not final net export. BFP discharge 26.5 MPa; modeled pressure budget is dissipated after the HP heaters before the SG inlet at 24 MPa / 286.85°C. Condensate discharge 1.0 MPa. The aggregate BFP symbol represents the two duty units in a 3 x 50% arrangement, with a provisional 15 MW motor shaft allowance for each. It is no longer driven by a steam turbine. HP2/HP1 receive 1.6/1.0 MPa bleeds from the main IP expansion, at ${e.heater_bleed_states.HP2.t-273.15}/${e.heater_bleed_states.HP1.t-273.15}°C, ${e.flows_kg_s.HP2}/${e.flows_kg_s.HP1} kg/s; DA receives ${e.flows_kg_s.DA} kg/s from the 0.6 MPa IP outlet. LP3 pressure ${e.inputs.plp3/1e6} MPa closes the matched steam-drive reference at the larger pump duty and is retained here. Reheater duty ${e.reheat_MW} MW, heating branch ${e.flows_kg_s.reheat} kg/s, reheated flow ${e.reheat_flow_kg_s} kg/s. Reheater minimum approach ${e.reheater_min_approach_K} K. Condenser heat ${e.condenser_MW} MW at exactly 5 kPa, LP moisture ${e.moisture_percent}%. The shown cooling water ${coolingIn}/${coolingOut}°C with ${cool.water_volume_m3_s} m3/s is consistent with that exact pressure and the retained condenser UA, not the separate coupled 20°C case. HP drains cascade 4→3→2→1→DA; LP drains 3→2→1→condenser; drains not drawn. Reheater heating return stays at 24 MPa / 380°C until throttled into HP4. Shaft/generator grouping preserves the earlier conceptual schematic; it is not a selected mechanical arrangement. Native editable objects; no flattened diagram. This presentation of the alternative does not select equipment or establish startup/transient capability.`;
await (await PresentationFile.exportPptx(p)).save(path.join(workspaceDir,'build/candidate.pptx'));
const img=await p.export({slide:s,format:'png',scale:2});await fs.writeFile(path.join(workspaceDir,'build/preview.png'),new Uint8Array(await img.arrayBuffer()));
console.log('Built editable diagram and preview.');
