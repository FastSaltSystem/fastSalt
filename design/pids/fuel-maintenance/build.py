"""Render the fuel-maintenance P&ID from its TOML basis and independent layout."""
from pathlib import Path
import csv, hashlib, html, json, math, textwrap, tomllib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import toColor as HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
ROOT=Path(__file__).resolve().parent
M=tomllib.loads((ROOT/'pid.toml').read_text()); UNIT=next(u for u in M['pressure_units'] if u['unit']==M['sharing']['representative_unit']); B=tomllib.loads((ROOT/M['basis']).read_text())
L=tomllib.loads((ROOT/'layout.toml').read_text()); W=L['width']; H=L['height']
OUT=ROOT/'outputs/current'; OUT.mkdir(parents=True,exist_ok=True)
INK='#15232b'; MUTED='#4b5b64'; GAS='#335a70'; FUEL='#20282c'; OFF='#6b4e72'
PDF=canvas.Canvas(str(OUT/'WISTR-fuel-maintenance-PID.pdf'),pagesize=(W,H),invariant=1)
PDF.setTitle('WISTR fuel maintenance - preliminary P&ID'); PDF.setAuthor('Fast Salt System')
registers={'equipment':[],'instruments':[],'valves':[],'lines':[],'signals':[]}; seen={}; checks=[]
def add(group,tag,description,location='',sheet=1):
 assert tag not in seen, f'Duplicate tag {tag}'
 seen[tag]=group; registers[group].append(dict(tag=tag,description=description,location=location,sheet=sheet))
def ident(key,index=1,sector=1): return M['identification'][key].format(index=index,sector=sector)
class Drawing:
 def __init__(self,n,title,subtitle):
  self.n=n;self.svg=[];self.ports={};self.routes=[];self.tags=[]
  self.rect(0,0,W,H,stroke='white');self.rect(22,22,W-44,H-44)
  self.text(42,51,'FAST SALT SYSTEM',13,bold=True)
  self.text(42,83,title,25,bold=True);self.text(42,108,subtitle,12,color=MUTED)
 def line(self,pts,color=INK,width=1.7,dash=False):
  self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
  PDF.setStrokeColor(HexColor(color));PDF.setLineWidth(width);PDF.setDash([6,4] if dash else [])
  p=PDF.beginPath();p.moveTo(pts[0][0],H-pts[0][1])
  for x,y in pts[1:]:p.lineTo(x,H-y)
  PDF.drawPath(p);PDF.setDash([])
 def rect(self,x,y,w,h,stroke=INK,fill='white',dash=False):
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" stroke="{stroke}" fill="{fill}" stroke-width="1.3"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
  PDF.setStrokeColor(HexColor(stroke));PDF.setFillColor(HexColor(fill));PDF.setLineWidth(1.3);PDF.setDash([6,4] if dash else []);PDF.rect(x,H-y-h,w,h,stroke=1,fill=1);PDF.setDash([])
 def circle(self,x,y,r,stroke=INK,fill='white',width=1.4):
  self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{stroke}" fill="{fill}" stroke-width="{width}"/>')
  PDF.setStrokeColor(HexColor(stroke));PDF.setFillColor(HexColor(fill));PDF.setLineWidth(width);PDF.circle(x,H-y,r,stroke=1,fill=1)
 def text(self,x,y,t,size=12,bold=False,anchor='start',color=INK):
  t=str(t);font='Helvetica-Bold' if bold else 'Helvetica';tw=stringWidth(t,font,size)
  left=x if anchor=='start' else x-tw/2 if anchor=='middle' else x-tw
  assert left>=22 and left+tw<=W-22, f'Text outside page: {t}'
  self.svg.append(f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="{color}">{html.escape(t)}</text>')
  PDF.setFillColor(HexColor(color));PDF.setFont(font,size)
  {'start':PDF.drawString,'middle':PDF.drawCentredString,'end':PDF.drawRightString}[anchor](x,H-y,t)
 def wrap(self,x,y,t,width,size=12,leading=18,bold=False,color=INK):
  words=t.split(); rows=[]; row=''
  for word in words:
   candidate=(row+' '+word).strip()
   if stringWidth(candidate,'Helvetica-Bold' if bold else 'Helvetica',size)>width and row: rows.append(row);row=word
   else:row=candidate
  if row:rows.append(row)
  for i,row in enumerate(rows):self.text(x,y+i*leading,row,size,bold,color=color)
  return y+len(rows)*leading
 def dot(self,x,y,color=INK):self.circle(x,y,3,stroke=color,fill=color)
 def arrow(self,x,y,d='right',color=INK):
  a,b={'right':(1,0),'left':(-1,0),'up':(0,-1),'down':(0,1)}[d]
  self.line([(x-9*a+4*b,y-9*b-4*a),(x,y),(x-9*a-4*b,y-9*b+4*a)],color,1.6)
 def port(self,name,x,y):
  assert name not in self.ports;self.ports[name]=(x,y);return (x,y)
 def wire(self,tag,start,end,via=(),service='',color=INK):
  assert start in self.ports and end in self.ports, f'Unknown port {tag}'
  pts=[self.ports[start],*via,self.ports[end]]
  assert all(a[0]==b[0] or a[1]==b[1] for a,b in zip(pts,pts[1:])), f'Nonorthogonal {tag}'
  self.line(pts,color,2);self.routes.append(dict(tag=tag,start=start,end=end,points=pts))
  add('lines',tag,service,f'{start} -> {end}',self.n)
 def instrument(self,x,y,tag,tap,host,desc):
  # Solid thin line is a process measurement connection, not an electrical signal.
  tx,ty=tap; r=27
  if x==tx:self.line([(tx,ty),(x,y-r if ty<y else y+r)],width=1)
  elif y==ty:self.line([(tx,ty),(x-r if tx<x else x+r,y)],width=1)
  else:self.line([(tx,ty),(x,ty),(x,y+r if ty>y else y-r)],width=1)
  self.circle(x,y,r);kind,num=tag.split('-',1)
  self.text(x,y-3,kind,12,bold=True,anchor='middle');self.text(x,y+12,num,10,anchor='middle')
  add('instruments',tag,desc,host,self.n);self.tags.append(tag)
 def connector(self,x,y,ref,other,label,d='right',color=INK):
  self.line([(x-23,y-12),(x+14,y-12),(x+24,y),(x+14,y+12),(x-23,y+12),(x-23,y-12)],color,1.3)
  self.text(x,y+4,ref,10,bold=True,anchor='middle',color=color)
  self.text(x,y+31,other,10,anchor='middle',color=MUTED)
  self.text(x+38,y-18,label,11,color=color) if d=='right' else self.text(x-38,y-18,label,11,anchor='end',color=color)
 def selector(self,x,y,tag,core):
  # Multiport selector symbol; paths selected by the position schedule, not fixed internally.
  self.circle(x,y,25);self.text(x,y+4,'SEL',10,bold=True,anchor='middle')
  self.text(x+40,y+47,tag,12,bold=True);self.text(x+40,y+66,'4 positions',10,color=MUTED)
  self.port(tag+'.P',x-25,y);self.port(tag+'.S',x,y-25);self.port(tag+'.C',x,y+25)
  self.port(tag+'.O',x+25,y)
  add('valves',tag,'Core gas selector, 4 positions' if core else 'Storage gas selector, 4 positions; off-gas by operator selection only','Position schedule: sheet 3',self.n)
 def vessel(self,x,y,w,h,tag,label):
  # Dished-end vessel outline; no construction dimensions are implied.
  q=18
  path=f'M{x} {y+q} C{x} {y-q/3} {x+w} {y-q/3} {x+w} {y+q} L{x+w} {y+h-q} C{x+w} {y+h+q/3} {x} {y+h+q/3} {x} {y+h-q} Z'
  self.svg.append(f'<path d="{path}" fill="white" stroke="{INK}" stroke-width="1.4"/>')
  PDF.setStrokeColor(HexColor(INK));PDF.setFillColor(HexColor('white'));PDF.setLineWidth(1.4)
  p=PDF.beginPath();p.moveTo(x,H-y-q);p.curveTo(x,H-y+q/3,x+w,H-y+q/3,x+w,H-y-q);p.lineTo(x+w,H-y-h+q);p.curveTo(x+w,H-y-h-q/3,x,H-y-h-q/3,x,H-y-h+q);p.close();PDF.drawPath(p,stroke=1,fill=1)
  self.text(x+w/2,y+h/2-5,tag,13,bold=True,anchor='middle');self.text(x+w/2,y+h/2+18,label,12,anchor='middle')
 def pump(self,x,y,tag,label,kind='PD'):
  self.circle(x,y,30);self.text(x,y+5,kind,14,bold=True,anchor='middle')
  self.line([(x-28,y+20),(x-38,y+40),(x+38,y+40),(x+28,y+20)],width=1.3)
  self.text(x,y+65,tag,14,bold=True,anchor='middle');self.text(x,y+86,label,12,anchor='middle')
  self.port(tag+'.left',x-30,y);self.port(tag+'.right',x+30,y)
  add('equipment',tag,label,'',self.n)
 def footer(self):
  y=1090;self.line([(22,y),(W-22,y)],width=1)
  self.text(42,y+25,'PRELIMINARY - FOR REVIEW',13,bold=True)
  self.text(42,y+49,'Owner-defined process arrangement. Sizes, ratings, fail positions and detailed controls TBD.',11,color=MUTED)
  self.text(42,y+69,'Functional schematic; not to scale. Solid-dot crossings connect; other crossings do not.',11,color=MUTED)
  self.line([(1100,y),(1100,H-22)],width=1)
  self.text(1120,y+24,'WISTR / FUEL MAINTENANCE',15,bold=True)
  self.text(1120,y+49,f'FS-FM-00{self.n}     REV {M["revision"]}     {M["date"]}',12)
  self.text(W-42,y+70,f'SHEET {self.n} OF 3',12,bold=True,anchor='end')
  self.svg.insert(0,f'<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 {W} {H}"><title>WISTR fuel maintenance P&amp;ID sheet {self.n}</title>')
  self.svg.append('</svg>');(OUT/f'FS-FM-00{self.n}.svg').write_text('\n'.join(self.svg));PDF.showPage()
  checks.append(dict(sheet=self.n,ports=self.ports,routes=self.routes))

# Sheet 1: representative sector, all three paired circuits connected to the gas headers.
d=Drawing(1,'FUEL TRANSFER AND PRESSURE VALVES','Sector 1 / TK-FM-01 (3D F6). Gas unit 3 is shared with sector 6 / TK-FM-06 (3D F5). Six-sector schedule: sheet 3.')
for y,ref,label,color in zip(L['header_ys'],['HP','HS','OG'],['H-P  Pressure-tank gas','H-S  Surge-tank gas','H-O  To off-gas'],[GAS,GAS,OFF]):
 d.connector(70,y,ref,'02','',color=color);d.line([(94,y),(1600,y)],color,2)
 d.text(495,y-12,label,11,color=color)
add('equipment','R-101','Reactor core fuel-region boundaries','Representative sector 1',1)
add('equipment','TK-FM-01','Maintenance tank with three storage regions','Compartments A/B/C',1)
for j,off in enumerate(L['pair_offsets']):
 idx=j+1;pair=M['pairs'][j];cx=205+off;sx=465+off;cv=ident('core_valve',idx);sv=ident('storage_valve',idx)
 d.text(330+off,495,f'CIRCUIT {idx}  /  {pair["label"]}',14,bold=True,anchor='middle')
 d.selector(cx,370,cv,True);d.selector(sx,370,sv,False)
 for tag,x,core in [(cv,cx,True),(sv,sx,False)]:
  for suffix,h_y,x_tap,target,via in [('P',145,x-55,tag+'.P',[(x-55,370)]),('S',195,x,tag+'.S',[])]+[('O',245,x+55,tag+'.O',[(x+55,370)])]:
   pn=f'{tag}.H{suffix}';d.port(pn,x_tap,h_y)
   d.wire('G-'+tag+'-'+suffix,pn,target,via,service={'P':'Pressure header branch','S':'Surge header branch','O':'Off-gas branch'}[suffix],color=OFF if suffix=='O' else GAS)
   d.dot(x_tap,h_y,OFF if suffix=='O' else GAS)
   # Bridge over all intervening horizontal headers without a junction.
   for other_y in L['header_ys']:
    if other_y>h_y and other_y<345:
     d.circle(x_tap,other_y,4,stroke='white',fill='white');d.line([(x_tap,other_y-6),(x_tap,other_y+6)],GAS if suffix!='O' else OFF,2)
 core_id=f'CORE-S1-{pair["label"].replace("/", "-")}'
 d.rect(115+off,535,180,150,dash=True)
 d.text(cx,568,'R-101 / SECTOR 1',12,bold=True,anchor='middle');d.text(cx,600,pair['label'],21,bold=True,anchor='middle');d.text(cx,630,'Core fuel regions',11,anchor='middle')
 d.port(core_id+'.gas',cx,535);d.port(core_id+'.fuel',cx,685)
 d.wire('G-FM-C'+str(idx).zfill(2),cv+'.C',core_id+'.gas',service='Core pressure gas',color=GAS)
 tank=ident('storage_tank',sector=1);comp=tank+pair['compartment']
 d.vessel(375+off,655,180,190,comp,pair['label']+' storage')
 d.text(sx,811,'Compartment '+pair['compartment'],10,anchor='middle')
 for name,x,y in [('gas',sx,655),('bottom',sx,845),('pressure',sx+50,675),('level',sx+90,750)]:d.port(comp+'.'+name,x,y)
 add('equipment',comp,'Maintenance-tank compartment '+pair['label'],tank,1)
 d.wire('G-FM-S'+str(idx).zfill(2),sv+'.C',comp+'.gas',service='Storage pressure gas',color=GAS)
 d.instrument(sx+55,592,ident('pressure_sensor',idx),d.ports[comp+'.pressure'],comp,'Storage-region pressure')
 d.instrument(sx+145,750,ident('level_sensor',idx),d.ports[comp+'.level'],comp,'Storage-region level')
 d.wire(ident('transfer_line',idx),core_id+'.fuel',comp+'.bottom',[(cx,920),(sx,920)],'Bidirectional fuel transfer',FUEL)
 d.arrow(cx+95,920,'right');d.arrow(cx+65,920,'left')
 d.instrument(cx+120,865,ident('gas_sensor',idx),(cx+120,920),ident('transfer_line',idx),'Gas presence in bottom transfer line')
 d.text(cx+130,948,ident('transfer_line',idx),12,bold=True,anchor='middle')
 if j==0:
  d.dot(cx,920);d.port('F-REM.tee',cx,920);d.port('F-REM.offpage',100,1010)
  d.wire('F-REM-01','F-REM.tee','F-REM.offpage',[(cx,1010)],'Measured removal from R1/R2 core fuel line')
  d.connector(76,1010,'FR','02','To removal pump P-FM-02');d.arrow(145,1010,'left')
 if j==2:
  d.dot(sx,920);d.port('F-ADD.tee',sx,920);d.port('F-ADD.offpage',1580,1010)
  d.wire('F-ADD-01','F-ADD.offpage','F-ADD.tee',[(sx,1010)],'Metered addition to R5/R6 storage')
  d.connector(1604,1010,'FA','02','From add pump P-FM-01',d='left');d.arrow(1515,1010,'left')
d.text(650,1010,'GD = gas-presence detector (project designation).',11,color=MUTED)
d.text(650,1031,'Tank A/B/C are compartments, not three separate tanks.',11,color=MUTED)
d.text(42,1064,'Cooling-air connections for the common maintenance-tank enclosure are on sheet 2. No unshown liquid junction is implied within a core pair.',11,color=MUTED)
d.footer()

# Sheet 2: gas service train, removal/addition pumps and cooling-air interfaces.
d=Drawing(2,'GAS SERVICES AND METERED FUEL CONNECTIONS','Connection markers HP / HS / OG / FA / FR continue on sheet 1. Gas unit 3 serves TK-FM-06 / TK-FM-01 (3D F5/F6); three shared units total.')
E=M['equipment'];pv=E['pressure_tank'];sv=E['surge_tank'];k=E['compressor'];ctl=M['compressor_control'];controller=ctl['controller']
d.text(45,155,'PRESSURE / SURGE GAS SYSTEM',14,bold=True)
d.vessel(200,235,180,175,pv,'Pressure tank');add('equipment',pv,'Pressure tank','',2)
d.vessel(1220,235,180,175,sv,'Surge tank');add('equipment',sv,'Surge tank','',2)
d.pump(650,320,k,'Gas compressor','K')
d.port(pv+'.compressor',380,320);d.port(sv+'.compressor',1220,320)
d.wire('G-FM-91',pv+'.compressor',k+'.left',service='Pressure tank / compressor',color=GAS)
d.wire('G-FM-92',k+'.right',sv+'.compressor',service='Compressor / surge tank',color=GAS)
d.instrument(290,180,ctl['pressure_input'],(290,235),pv,'Pressure-tank pressure')
d.instrument(1310,180,ctl['surge_input'],(1310,235),sv,'Surge-tank pressure')
# Functional electronic signals. Setpoint, switching band and implementation remain TBD.
d.circle(850,180,32);d.text(850,176,'PDC',12,bold=True,anchor='middle');d.text(850,194,controller.split('-',1)[1],10,anchor='middle')
d.text(850,135,'Pressure-difference controller',12,bold=True,anchor='middle')
d.line([(317,180),(818,180)],width=1.2,dash=True);d.arrow(800,180)
d.line([(1283,180),(882,180)],width=1.2,dash=True);d.arrow(900,180,'left')
d.line([(850,212),(850,260),(650,260),(650,290)],width=1.2,dash=True);d.arrow(650,287,'down')
d.text(710,247,'Start / stop',12)
add('instruments',controller,ctl['function'],ctl['pressure_input']+' and '+ctl['surge_input'],2)
for tag,src,dst,desc in [('S-FM-91',ctl['pressure_input'],controller,'Pressure measurement input'),('S-FM-92',ctl['surge_input'],controller,'Surge pressure measurement input'),('S-FM-93',controller,k,'Compressor start/stop command')]:
 add('signals',tag,desc,src+' -> '+dst,2)
d.port(sv+'.gas_supply',1400,370);d.port('GAS-SUPPLY.boundary',1556,370)
d.wire(M['gas_supply']['line'],'GAS-SUPPLY.boundary',sv+'.gas_supply',service='Gas supply to surge tank',color=GAS)
d.arrow(1460,370,'left',GAS);d.connector(1580,370,'GS','ROOM','',color=GAS)
d.text(1420,346,'From off-gas room',11,color=GAS);d.text(1450,397,M['gas_supply']['line'],11,bold=True,color=GAS)
for tag,x,ref in [(pv,290,'HP'),(sv,1310,'HS')]:
 d.port(tag+'.header',x,410);d.port(ref+'.offpage',x,475)
 d.wire('G-FM-'+ref,tag+'.header',ref+'.offpage',service=ref+' valve-bank header',color=GAS)
 d.connector(x,487,ref,'01','To TK-FM-01 banks',color=GAS)
 d.dot(x,440,GAS);d.port(ref+'.second_bank',x+145,440)
 d.wire('G-FM-'+ref+'-TK06',tag+'.header',ref+'.second_bank',[(x,440)],service=ref+' shared branch to TK-FM-06 valve banks',color=GAS)
 d.connector(x+169,440,ref,'S6','',color=GAS)
 d.text(x+45,424,'TK-FM-06 banks',10,color=GAS)
d.wrap(520,440,f"{controller} starts/stops {k} using {ctl['pressure_input']} and {ctl['surge_input']}. One unit serves two tanks (six storage regions). Setpoint and switching band TBD.",620,12)
d.wrap(520,497,'Gas supply: existing room supply interface and common header. Off-gas: existing separate return header to treatment; both use the shared duct.',620,11)
d.text(45,560,'CORE / STORAGE VALVE VENT CONNECTION',14,bold=True)
d.connector(95,605,'OG','01','',color=OFF);d.line([(119,605),(1460,605)],OFF,2);d.arrow(1410,605,'right',OFF)
d.text(420,588,'H-O  Core / storage position 4 vents - both associated sectors',12,color=OFF)
d.line([(1100,565),(1100,605)],OFF,2);d.dot(1100,605,OFF);d.connector(1100,553,'OG','S6','',color=OFF)
d.connector(1484,605,'OG','ROOM','Existing return to off-gas room',d='left',color=OFF)
d.text(45,670,'METERED FUEL ADDITION AND REMOVAL',14,bold=True)
for y,tag,label,leftref,rightref in [(740,E['add_pump'],'Add fuel displacement pump','EXT','FA'),(900,E['remove_pump'],'Remove fuel displacement pump','FR','EXT')]:
 d.pump(825,y,tag,label)
 d.port(tag+'.boundary_left',170,y);d.port(tag+'.boundary_right',1480,y)
 d.wire('F-'+tag+'-IN',tag+'.boundary_left',tag+'.left',service=label+' inlet')
 d.wire('F-'+tag+'-OUT',tag+'.right',tag+'.boundary_right',service=label+' outlet')
 d.arrow(610,y);d.arrow(1100,y)
 d.connector(146,y,leftref,'01' if leftref=='FR' else 'TBD','',d='right')
 d.connector(1504,y,rightref,'01' if rightref=='FA' else 'TBD','',d='left')
 if leftref=='EXT':
  d.text(200,y-18,'Fuel source / tie-in TBD',12);d.text(1160,y-18,'To R5/R6 storage (01)',12)
 else:
  d.text(200,y-18,'From R1/R2 core fuel line (01)',12);d.text(1160,y-18,'Removed fuel destination TBD',12)
d.text(45,1033,'COOLING AIR',12,bold=True)
d.line([(230,1028),(500,1028)],width=2);d.arrow(450,1028)
d.text(240,1014,'Fresh-air connection',11)
d.rect(500,1000,500,54);d.text(750,1023,'TK-FM-01 cooling enclosure',13,bold=True,anchor='middle');d.text(750,1043,'Common enclosure for storage regions A / B / C',11,anchor='middle')
d.line([(1000,1028),(1420,1028)],width=2);d.arrow(1350,1028);d.text(1090,1014,'Exhaust-air connection',11)
d.text(45,1072,'Air connections retained from reference; detailed dampers, cooling internals and external air-header tags remain TBD.',11,color=MUTED)
d.footer()

# Sheet 3: concise owner-defined state matrix and drawing conventions.
d=Drawing(3,'VALVE POSITIONS, OPERATING STATES AND TAG SCHEDULE','Owner-defined states; compressor pressure-difference start/stop control on sheet 2. Setpoints and fail positions TBD.')
d.text(45,153,'SELECTOR POSITION SCHEDULE',14,bold=True)
xs=[45,250,590,950]; widths=[205,340,360,689]
rows=[['Position','Core selectors XV-FM-Cxx','Storage selectors XV-FM-Sxx','Connection intent'],
['1 - Add pressure','Available','Available','Common gas port C to pressure header H-P'],
['2 - Maintain','Available','Available','Maintain position; internal port isolation details TBD'],
['3 - Reduce pressure','Available','Available','Common gas port C to surge header H-S'],
['4 - Vent to off-gas','Available','Operator selection only','Selected common gas port C to off-gas header H-O']]
y=170
for ri,row in enumerate(rows):
 for x,w,t in zip(xs,widths,row):d.rect(x,y,w,38,fill='#eef1f2' if ri==0 else 'white');d.text(x+10,y+24,t,12,bold=ri==0)
 y+=38
d.text(45,402,'OWNER-DEFINED OPERATING STATES',14,bold=True)
xs=[45,270,560,830,1639]; headers=['State / scope','Core pressure valves','Storage pressure valves','Pump / completion description']
for x,x2,t in zip(xs,xs[1:],headers):d.rect(x,420,x2-x,36,fill='#eef1f2');d.text(x+9,443,t,12,bold=True)
remove=B['owner_states']['remove_fuel'];fill=B['owner_states']['fill_fuel'];small=B['owner_states']['add_small_fuel_r6'];measured=B['owner_states']['remove_measured_fuel_r1_r2']
states=[('Remove fuel / all pairs',remove['core_pressure_valves'],remove['maintenance_pressure_valves'],'Gas in a bottom line: corresponding two valves return to Maintain. All valves in Maintain when all tanks are empty.'),
('Fill fuel / all pairs',fill['core_pressure_valves'],fill['maintenance_pressure_valves'],'Gas in a maintenance-tank bottom line indicates empty: corresponding two valves return to Maintain. All valves in Maintain at completion.'),
('Small addition / R5/R6',small['core_pressure_valve'],small['maintenance_pressure_valve'],'P-FM-01 meters fuel into R5/R6 storage. Use Fill fuel positions until gas is detected, then both R5/R6 valves return to Maintain. Intended addition to R6.'),
('Measured removal / R1/R2','TBD','TBD','P-FM-02 removes a measured quantity from the R1/R2 core fuel line. Quantity, valve positions and further sequence are not specified.'),
('Off-gas vent','Position 4, if selected','Position 4: operator only','Storage vent is used only when selected by the operator; excluded from automatic transfer sequences. Core vent selection conditions remain unspecified.')]
y=456
for row in states:
 for x,x2,t in zip(xs,xs[1:],row):d.rect(x,y,x2-x,77);d.wrap(x+9,y+22,t,x2-x-20,12,17)
 y+=77
d.text(45,886,'THREE SHARED GAS UNITS / EXISTING 3D ASSOCIATIONS',14,bold=True)
for x,t in [(45,'Unit / server'),(190,'3D tanks'),(325,'P&ID tanks'),(570,'Sectors')]:d.text(x,913,t,11,bold=True)
for j,u in enumerate(M['pressure_units']):
 y=940+27*j
 d.text(45,y,str(u['unit'])+' / P'+str(u['unit']),12)
 d.text(190,y,' / '.join('F'+str(v) for v in u['tanks_3d']),12)
 d.text(325,y,' / '.join('TK-FM-'+str(v).zfill(2) for v in u['sectors']),12)
 d.text(570,y,' / '.join(str(v) for v in u['sectors']),12)
d.wrap(45,1021,'Each tank: A=R1/R2, B=R3/R4, C=R5/R6. Circuit index = 3 x (sector - 1) + pair. Existing provisional sector/tank mapping retained (D-035).',735,11,15)
d.text(860,886,'SYMBOLS AND OPEN DETAILS',14,bold=True)
d.wrap(860,911,'LT / PT: level / pressure sensing functions. GD: project-defined gas-presence detector. Circular multiport valve symbol: selector; actual actuation and internal trim TBD. PD pump: positive displacement.',755,12,18)
d.wrap(860,974,'Solid heavy lines: process piping. Solid thin lines: instrument process connections. Dashed lines: functional measurement/command signals. Dashed boxes: core boundaries. PDC: pressure-difference controller. Dot = junction; other crossings do not connect.',755,12,18)
d.text(45,1055,'R6-only distribution and metering-pump sharing remain TBD. Unit internals are detailed here; 3D servers remain exterior envelopes.',11,color=MUTED)
d.text(45,1073,'Notation reference: ISA5.1 public guidance; project-specific selector and GD conventions are defined here. No full-standard compliance claim.',10,color=MUTED)
d.footer();PDF.save()

# Complete sector repetition register, independent of the representative drawing.
expanded=[]
for sector in range(1,7):
 for j,pair in enumerate(M['pairs'],1):
  index=3*(sector-1)+j
  unit=next(u for u in M['pressure_units'] if sector in u['sectors'])
  expanded.append(dict(sector=sector,pressure_unit=unit['unit'],tank_3d='F'+str(M['sharing']['sector_to_3d_tank'][sector-1]),pair=pair['label'],storage=ident('storage_tank',sector=sector)+pair['compartment'],**{k:ident(k,index=index,sector=sector) for k in ['core_valve','storage_valve','level_sensor','pressure_sensor','gas_sensor','transfer_line']}))
assert len({r['core_valve'] for r in expanded})==18
assert B['owner_removal_connection']['suction']=='R1/R2 core fuel line'
assert B['owner_instrumentation']['source_storage_clarification']=='One level and pressure sensor per storage region'
assert len(B['owner_valve_positions']['core'])==4 and len(B['owner_valve_positions']['storage'])==4
unit_rows=[{**u,'tanks_3d':' / '.join('F'+str(i) for i in u['tanks_3d']),'sectors':' / '.join(map(str,u['sectors'])),'pid_tanks':' / '.join('TK-FM-'+str(i).zfill(2) for i in u['sectors'])} for u in M['pressure_units']]
interface_rows=[]
for u in M['pressure_units']:
 for service,key,branch in [('Supply gas','supply_3d_common','supply'),('Off-gas','offgas_3d_common','return')]:
  interface_rows.append(dict(unit=u['unit'],service=service,room=M['sharing']['room'],common_object=M['sharing'][key],branch_object=f"site.fuel_pressure.server_{u['unit']}_{branch}",server_object=u['server_3d']))
assert sorted(s for u in M['pressure_units'] for s in u['sectors'])==list(range(1,7))
assert all(len(u['sectors'])==2 and len(u['tanks_3d'])==2 for u in M['pressure_units'])
for u in M['pressure_units']:
 assert [M['sharing']['sector_to_3d_tank'][s-1] for s in u['sectors']]==u['tanks_3d']
for name,rows in {**registers,'sector-tag-schedule':expanded,'pressure-unit-schedule':unit_rows,'3d-interface-register':interface_rows}.items():
 with (OUT/(name+'.csv')).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
inputs=[ROOT/'pid.toml',ROOT/M['basis'],ROOT/'layout.toml',Path(__file__),ROOT/B['source']]
manifest={'revision':M['revision'],'sheet_count':3,'original_svg_sha256':hashlib.sha256((ROOT/B['source']).read_bytes()).hexdigest(),'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'counts':{k:len(v) for k,v in registers.items()},'sector_circuits':len(expanded),'shared_units':M['pressure_units'],'existing_3d_interfaces':interface_rows,'drawings':checks,'validation_scope':'Tag uniqueness, connected route endpoints, orthogonal routes, owner-defined positions, sector counts and source identity; not engineering qualification.'}
assert manifest['original_svg_sha256']==B['source_sha256']
(OUT/'pid-checks.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:manifest[k] for k in ['revision','sheet_count','counts','sector_circuits']},indent=2))
