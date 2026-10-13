"""Build editable SVG sheets and an A3 landscape PDF. Requires reportlab."""
from pathlib import Path
import math, html, csv, json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import toColor as HexColor
from reportlab.lib.pagesizes import A3, landscape
ROOT=Path(__file__).resolve().parent
W,H=1200,850
INK='#173345'; MUTED='#546772'; HOT='#b7442e'; COLD='#147689'; PROP='#946200'; LINE='#274453'; LIGHT='#edf3f6'
PDF=canvas.Canvas(str(ROOT/'WISTR-coolant-PID-rev-A.pdf'),pagesize=landscape(A3))
PDF.setTitle('WISTR coolant system - preliminary P&ID - Rev A')
PDF.setAuthor('Fast Salt System project')
class Drawing:
 def __init__(self,n,title,subtitle):
  self.n=n; self.svg=[]; PDF.saveState(); PDF.scale(landscape(A3)[0]/W,landscape(A3)[1]/H)
  self.rect(0,0,W,H,fill='white',stroke='white')
  self.text(35,37,'FAST SALT SYSTEM / WISTR',12,weight=True,color=MUTED)
  self.text(35,72,title,27,weight=True)
  self.text(35,99,subtitle,12,color=MUTED)
  self.line([(35,115),(1165,115)],color=INK,width=1)
 def rect(self,x,y,w,h,fill='white',stroke=INK,dash=False):
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
  PDF.setStrokeColor(HexColor(stroke));PDF.setFillColor(HexColor(fill));PDF.setLineWidth(1.3);PDF.setDash([6,4] if dash else []);PDF.rect(x,H-y-h,w,h,fill=1,stroke=1);PDF.setDash([])
 def text(self,x,y,t,size=12,color=INK,weight=False,anchor='start'):
  self.svg.append(f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{"bold" if weight else "normal"}" fill="{color}" text-anchor="{anchor}">{html.escape(str(t))}</text>')
  PDF.setFillColor(HexColor(color));PDF.setFont('Helvetica-Bold' if weight else 'Helvetica',size)
  {'start':PDF.drawString,'middle':PDF.drawCentredString,'end':PDF.drawRightString}[anchor](x,H-y,str(t))
 def line(self,pts,color=LINE,width=2,dash=False):
  self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="5 4"' if dash else '')+'/>')
  PDF.setStrokeColor(HexColor(color));PDF.setLineWidth(width);PDF.setDash([5,4] if dash else []);p=PDF.beginPath();p.moveTo(pts[0][0],H-pts[0][1])
  for x,y in pts[1:]:p.lineTo(x,H-y)
  PDF.drawPath(p);PDF.setDash([])
 def circle(self,x,y,r,color=INK,fill='white',width=1.5):
  self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{color}" fill="{fill}" stroke-width="{width}"/>');PDF.setLineWidth(width);PDF.setStrokeColor(HexColor(color));PDF.setFillColor(HexColor(fill));PDF.circle(x,H-y,r,fill=1,stroke=1)
 def arrow(self,x,y,d='right',color=LINE):
  v={'right':(1,0),'left':(-1,0),'up':(0,-1),'down':(0,1)}[d];a,b=v
  self.line([(x-8*a+4*b,y-8*b-4*a),(x,y),(x-8*a-4*b,y-8*b+4*a)],color,2)
 def valve(self,x,y,tag):
  self.rect(x-12,y-9,24,18,stroke='white');self.line([(x-10,y-7),(x+10,y+7),(x+10,y-7),(x-10,y+7),(x-10,y-7)],PROP,1.6)
  self.text(x,y-16,tag,10,PROP,anchor='middle')
 def inst(self,x,y,kind,num,tapx,tapy):
  # Dashed line denotes measurement association, not tubing or a control signal.
  self.line([(tapx,tapy),(x,y-19 if tapy<y else y+19)],PROP,1,dash=True)
  self.circle(x,y,19,PROP);self.text(x,y-1,kind,10,PROP,True,'middle');self.text(x,y+11,num,9,PROP,anchor='middle')
 def pump(self,x,y,tag):
  self.circle(x,y,22);self.line([(x+9,y-10),(x-10,y),(x+9,y+10)],INK,1.7)
  self.text(x,y+51,tag,12,weight=True,anchor='middle')
 def footer(self):
  self.line([(35,804),(1165,804)],INK,1)
  self.text(35,824,'FS-CS-00'+str(self.n)+' | Rev A | 13 October 2026 | Preliminary - for discussion',11,weight=True)
  self.text(1165,824,f'Sheet {self.n} / 2 | Functional schematic; not to scale',11,anchor='end')
  self.svg.insert(0,f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 {W} {H}" role="img"><title>WISTR coolant system sheet {self.n}</title>')
  self.svg.append('</svg>');(ROOT/f'FS-CS-00{self.n}-rev-A.svg').write_text('\n'.join(self.svg))
  PDF.restoreState();PDF.showPage()

d=Drawing(1,'Coolant circulation','Three established process legs; proposed measurement and isolation locations shown in amber.')
d.rect(35,152,205,525,fill=LIGHT)
d.text(137,184,'R-101',19,weight=True,anchor='middle');d.text(137,205,'WISTR reactor',15,weight=True,anchor='middle')
for y,t in [(255,'Shared hot plenum'),(276,'feeds H1 / H2 / H3.'),(328,'C1 / C2 / C3 return'),(349,'to shared downcomer.'),(403,'Internal coolant path:'),(427,'downcomer'),(450,'to bottom plenum'),(473,'up through core tubes'),(496,'to hot plenum.')]:d.text(52,y,t,12)
d.text(52,552,'Fuel is a separate fluid.',12,weight=True)
d.text(52,582,'Plenums are inside R-101;',11);d.text(52,600,'no external common salt',11);d.text(52,618,'header is implied.',11)
# Reactor drain continuation at bottom.
d.line([(138,677),(138,708)],LINE);d.arrow(138,704,'down');d.text(157,695,'A / reactor bottom',11);d.text(157,710,'to sheet 2, L-401',11)
for i,y in enumerate([215,395,575],1):
 n=100+i
 # SG simplified heat exchanger outline, salt on left, secondary boundary on right.
 d.rect(880,y-22,105,142,fill=LIGHT)
 d.text(932,y+25,f'SG-{n}',15,weight=True,anchor='middle');d.text(932,y+47,'500 MWth',11,anchor='middle')
 d.text(932,y+75,'Exchanger',11,anchor='middle')
 d.line([(240,y),(880,y)],HOT,2.7);d.arrow(830,y,color=HOT)
 d.text(250,y-11,f'H{i}',10,HOT,True)
 d.text(600,y-12,f'L-{n}  |  hot salt ~602 C',12,HOT,anchor='middle')
 d.valve(315,y,f'V-{n}H');d.inst(690,y+40,'TT',f'{n}H',690,y)
 # Return from SG routed downward into pump bottom inlet.
 ry=y+95
 d.line([(880,ry),(790,ry),(790,ry+30),(620,ry+30),(620,ry+22)],COLD,2.7)
 d.arrow(720,ry+30,'left',COLD);d.arrow(620,ry+23,'up',COLD)
 d.pump(620,ry,f'P-{n}')
 d.line([(598,ry),(240,ry)],COLD,2.7);d.arrow(270,ry,'left',COLD)
 d.text(250,ry-11,f'C{i}',10,COLD,True)
 d.text(520,ry-17,f'L-{200+i} | ~537 C',11,COLD,anchor='middle')
 d.valve(315,ry,f'V-{n}C')
 d.inst(385,ry+39,'FT',str(n),385,ry)
 d.inst(472,ry+39,'TT',f'{n}C',472,ry)
 d.inst(555,ry+39,'PT',f'{n}D',555,ry)
 d.inst(750,ry-7,'PT',f'{n}S',750,ry+30)
 # Direction and off-sheet secondary boundaries.
 d.line([(985,y+2),(1120,y+2)],INK,1.4);d.arrow(1114,y+2)
 d.text(1049,y-8,'Steam to power cycle',10,anchor='middle')
 d.line([(1120,ry),(985,ry)],INK,1.4);d.arrow(991,ry,'left')
 d.text(1049,ry-10,'Feedwater from cycle',10,anchor='middle')
 d.text(1010,y+40,'Salt / water boundary',10,MUTED)
 d.text(1010,y+57,'Air passages omitted',10,MUTED)

d.rect(35,734,1130,57,fill=LIGHT,stroke=LIGHT)
d.text(48,754,'PER LEG: 4.620 m3/s; pump rise 286 kPa; 1.65 MW shaft; provisional 2 MW motor. Main line bore 1425 mm.',11,weight=True)
d.text(48,773,'Main wall 25 mm; radial insulation hot 400 / return 350 mm (conditional estimates). Pump rise is not system design pressure.',11)
d.footer()

d=Drawing(2,'Coolant storage, transfer and review points','Established transfer direction retained. No reverse-flow, vent destination or automatic protection is assumed.')
# Sources and reactor transfer.
d.rect(35,165,225,90,fill=LIGHT)
d.text(52,190,'A / FROM R-101 BOTTOM',13,weight=True)
d.text(52,213,'Continuation from sheet 1',11)
d.text(52,235,'Transfer out of reactor',11)
d.line([(260,208),(550,208),(550,316)],LINE,2.7);d.arrow(410,208);d.arrow(550,299,'down')
d.valve(322,208,'V-401');d.inst(450,161,'TT','401',450,208)
d.text(588,223,'L-401',11);d.text(588,243,'Heated + insulated',11)
# Pump line approaches bottom then side discharge toward tank.
d.line([(550,316),(608,316)],LINE,2.7);d.arrow(595,316)
d.pump(630,316,'P-401')
# rightward discharge pump triangle also correct (pump symbol generic left pointing inherited -> override)
d.circle(630,316,22);d.line([(621,306),(640,316),(621,326)],INK,1.7)
d.line([(652,316),(815,316),(815,453),(934,453),(934,400)],LINE,2.7)
d.arrow(770,316);d.arrow(884,453);d.arrow(934,412,'up')
d.valve(740,316,'V-402');d.inst(691,269,'PT','401D',691,316)
d.text(717,375,'L-402',11);d.text(502,426,'Pump near tank bottom; geometry simplified.',11,MUTED)
# Tank.
d.rect(875,175,245,225,fill=LIGHT)
d.text(997,208,'TK-401',19,weight=True,anchor='middle');d.text(997,234,'Coolant storage',16,weight=True,anchor='middle')
d.text(997,270,'Insulated tank',12,anchor='middle');d.text(997,294,'350 mm visual allowance',11,anchor='middle')
d.text(997,321,'Two separate bottom ports',11,anchor='middle');d.text(997,343,'Tank duty / usable inventory',11,anchor='middle');d.text(997,360,'to be established',11,anchor='middle')
d.inst(1145,210,'LT','401',1120,240);d.inst(1145,316,'TT','402',1120,340)
# Proposed vessel PT at top but no vent drawn.
d.inst(1000,139,'PT','402',1000,175)
# Prep connection on lower lane independent storage nozzle.
d.rect(35,385,300,79,fill=LIGHT);d.text(51,409,'B / COOLANT SALT PREPARATION',12,weight=True)
d.text(51,431,'Through shared building service duct',11);d.text(51,450,'Liquid coolant supply only',11)
d.line([(335,442),(395,442),(395,491),(1040,491),(1040,400)],LINE,2.7)
d.arrow(690,491);d.arrow(1040,412,'up');d.valve(460,491,'V-403')
d.text(720,479,'L-403 | heated + insulated; near-floor route',12,anchor='middle')
d.text(35,291,'50 mm OD service tubes',14,weight=True)
d.text(35,315,'50 mm radial insulation: provisional layout allowance.',11)
d.text(35,336,'Transfer pump type, duty and thermal design remain open.',11)
# Separate note panels.
def panel(x,y,w,title,lines):
 d.rect(x,y,w,116,fill=LIGHT,stroke=LIGHT);d.text(x+12,y+22,title,13,weight=True)
 for j,t in enumerate(lines):d.text(x+12,y+44+j*17,t,11)
panel(35,533,550,'DRAWING CONVENTIONS',[
 'Solid pipes: established process connections; arrows show intended flow.',
 'Red = hot circulation; blue = cool return; dark = storage / service.',
 'Amber valves and instrument bubbles: proposals for review.',
 'Dashed amber: measurement association, not an impulse or signal line.'])
panel(610,533,555,'TAG KEY / PROPOSAL LIMITS',[
 'TT temperature; PT pressure; FT flow; LT level (measurement intent).',
 'V = candidate isolation valve; valve type and actuation not selected.',
 'R reactor; SG steam generator; P pump; TK storage; L process line.',
 'No control loops, alarm settings, trip logic or fail positions assigned.'])
panel(35,666,550,'OPEN: OPERATING AND MAINTENANCE STATES',[
 'Define reactor fill / refill path, complete draining and residual salt.',
 'Establish inventory, tank freeboard, gas space and expansion provision.',
 'Define preheat / heat tracing, freeze recovery and transfer sequencing.',
 'Check pump suction conditions and shared-plenum flow distribution.'])
panel(610,666,555,'OPEN: PRESSURE BOUNDARIES AND PROTECTION',[
 'Establish pressure profile; 1 MPa(g) is only a wall-screening case.',
 'Resolve SG tube-failure pressure from the 24 MPa(a) secondary side.',
 'Define vent / relief destinations and trapped-salt thermal protection.',
 'Review proposed isolation, measurement technology and remote access.'])
d.footer();PDF.save()

# Registers describe this drawing revision; proposal tags are not installed assets.
def csvout(name,fields,rows):
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
inst=[];valves=[];lines=[]
for i in range(1,4):
 n=100+i
 for kind,suffix,loc,purpose in [
  ('TT','H',f'L-{n}','Observe hot-leg temperature'),
  ('TT','C',f'L-{200+i}: pump discharge','Observe returning coolant temperature'),
  ('FT','',f'L-{200+i}: pump discharge','Observe per-leg circulation; technology unselected'),
  ('PT','S',f'L-{200+i}: pump suction','Observe suction pressure'),
  ('PT','D',f'L-{200+i}: pump discharge','Observe discharge pressure; compare with suction')]:
  inst.append(dict(tag=f'{kind}-{n}{suffix}',location=loc,purpose=purpose,status='Proposed',sheet=1))
 for suffix,loc in [('H',f'L-{n}'),('C',f'L-{200+i}')]:
  valves.append(dict(tag=f'V-{n}{suffix}',line=loc,purpose='Candidate branch isolation; not a complete maintenance isolation scheme',status='Proposed; type/actuation/fail position TBD',sheet=1))
 lines.extend([dict(tag=f'L-{n}',source=f'R-101 H{i}',destination=f'SG-{n} salt inlet',bore_mm=1425,od_mm=1475,wall_mm=25,radial_insulation_mm=400,temperature_C=601.85,status='Established topology; dimensions conditional',sheet=1),dict(tag=f'L-{200+i}',source=f'SG-{n} salt outlet',destination=f'P-{n} then R-101 C{i}',bore_mm=1425,od_mm=1475,wall_mm=25,radial_insulation_mm=350,temperature_C=536.85,status='Established topology; dimensions conditional; includes pump suction and discharge',sheet=1)])
for tag,loc,purpose in [('TT-401','L-401','Observe transfer-line temperature'),('PT-401D','L-402','Observe transfer discharge pressure'),('PT-402','TK-401 gas space','Observe storage pressure; gas system TBD'),('LT-401','TK-401','Observe storage inventory; measurement method TBD'),('TT-402','TK-401','Observe stored salt temperature; sensor coverage TBD')]:
 inst.append(dict(tag=tag,location=loc,purpose=purpose,status='Proposed',sheet=2))
for num,source,dest in [(401,'R-101 bottom','P-401 suction'),(402,'P-401 discharge','TK-401 bottom port 1'),(403,'Coolant preparation via shared duct','TK-401 bottom port 2')]:
 lines.append(dict(tag=f'L-{num}',source=source,destination=dest,bore_mm=44 if num<403 else 'TBD',od_mm=50,wall_mm=3 if num<403 else 'TBD',radial_insulation_mm=50,temperature_C='TBD',status='Established topology; OD/insulation visual allowances; heated; transfer wall provisional',sheet=2))
 valves.append(dict(tag=f'V-{num}',line=f'L-{num}',purpose='Candidate transfer/supply isolation',status='Proposed; type/actuation/fail position TBD',sheet=2))
csvout('instruments.csv',['tag','location','purpose','status','sheet'],inst)
csvout('valves.csv',['tag','line','purpose','status','sheet'],valves)
csvout('lines.csv',['tag','source','destination','bore_mm','od_mm','wall_mm','radial_insulation_mm','temperature_C','status','sheet'],lines)
