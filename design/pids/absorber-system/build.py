"""Expand the absorber TOML pattern and draw its functional P&ID and review sheets."""
from pathlib import Path
import importlib.util, json,tomllib,hashlib,csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
ROOT=Path(__file__).resolve().parent
HUB=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('coolant_drawing',ROOT.parent/'coolant-system/build.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
INK=base.INK;MUTED=base.MUTED;PROP=base.PROP;GAS='#24768a';SALT='#a75330';RETURN='#795687'

def load():
 m=tomllib.loads((ROOT/'absorber-system.toml').read_text());l=tomllib.loads((ROOT/'layout.toml').read_text())
 b=tomllib.loads((ROOT/m['engineering']).read_text());r=json.loads((HUB/'calculations/reactor/absorber-capacity-results.json').read_text())
 assert m['schema_version']==l['schema_version']==1
 assert len(m['assemblies'])==6 and m['chambers']==['A','B']
 ports={k+'.'+p for k,e in m['equipment'].items() for p in e['ports']}
 assert set(l['sheet1']['boxes'])==set(m['equipment'])
 assert set(l['sheet1']['routes'])==set(m['lines'])
 for k,e in m['lines'].items():
  assert e['from'] in ports and e['to'] in ports,k
  assert len(l['sheet1']['routes'][k])>=2
 for k,e in m['instruments'].items():assert e['on'] in m['equipment'],k
 assert m['states']['inject']['connections']==['P-R','A-S']
 assert m['states']['remove']['connections']==['P-A','R-S']
 assert not m['states']['hold']['connections']
 records=[]
 for n in m['assemblies']:
  for chamber in m['chambers']:
   suffix=str(n)+chamber
   for kind,items in [('equipment',m['equipment']),('line',m['lines']),('instrument',m['instruments'])]:
    for key,item in items.items():
     tag=key+'-'+suffix
     if kind=='line':tag={'salt':'L-SALT','absorber_gas':'G-A','reservoir_gas':'G-R','pressure_gas':'G-P','surge_gas':'G-S','compressor_in':'G-CI','compressor_out':'G-CO'}[key]+'-'+suffix
     if kind=='instrument':tag={'PT_P':'PT-'+suffix+'P','PT_S':'PT-'+suffix+'S','LT_R':'LT-'+suffix+'R','LT_A':'LT-'+suffix+'A','TT_R':'TT-'+suffix+'R'}[key]
     row={'tag':tag,'kind':kind,'assembly':n-700,'chamber':'primary' if chamber=='A' else 'secondary',**{k:v for k,v in item.items() if k!='kind'},'measurement_kind':item.get('kind','')}
     for field in ('from','to'):
      if field in row:
       typ,port=row[field].split('.');row[field]=typ+'-'+suffix+'.'+port
     if 'on' in row:row['on']+='-'+suffix
     records.append(row)
 assert len({x['tag'] for x in records})==len(records)==216
 circuits=[str(n)+c for n in m['assemblies'] for c in m['chambers']]
 for tag,item in m['service_equipment'].items():
  record={'tag':tag,'kind':'equipment',**item}
  if item.get('branch_ports'):record['ports']=item['ports']+circuits
  records.append(record)
 for tag,item in m['service_lines'].items():records.append({'tag':tag,'kind':'line',**item})
 for circuit in circuits:
  for group,kind in [('service_branches','line'),('service_valves','valve')]:
   for item in m[group].values():
    records.append({'kind':kind,**{k:(v.format(circuit=circuit) if isinstance(v,str) else v) for k,v in item.items()}})
 assert len({x['tag'] for x in records})==len(records)==282
 all_ports={e['tag']+'.'+q for e in records if e['kind']=='equipment' for q in e['ports']}
 lines={e['tag']:e for e in records if e['kind']=='line'}
 for line in lines.values():assert line['from'] in all_ports and line['to'] in all_ports,line
 for valve in (e for e in records if e['kind']=='valve'):assert valve['line'] in lines,valve
 for circuit in circuits:
  assert lines['N-'+circuit]['from']=='H-700N.'+circuit
  assert lines['N-'+circuit]['to']=='SV-'+circuit+'.makeup'
  assert lines['G-'+circuit]['from']=='SV-'+circuit+'.service_return'
  assert lines['G-'+circuit]['to']=='H-700R.'+circuit
 assert lines['G-700']['to']=='B-700T.inlet'
 assert not any(e['to'].startswith(('H-700N.','B-700N.')) and e['tag']!='N-700' for e in lines.values())
 return m,l,b,r,records
class Drawing(base.Drawing):
 def footer(self):
  self.line([(35,804),(1165,804)],INK,1)
  self.text(35,824,f'FS-AS-00{self.n} | Rev A-draft | 2026-10-15 | Functional discussion draft',11,weight=True)
  self.text(1165,824,f'Sheet {self.n} / 4 | Not to scale',11,anchor='end')
  self.svg.insert(0,f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 1200 848" role="img"><title>WISTR absorber system sheet {self.n}</title>');self.svg.append('</svg>')
  (OUT/f'FS-AS-00{self.n}.svg').write_text('\n'.join(self.svg));base.PDF.restoreState();base.PDF.showPage()
 def texts(self,x,y,lines,size=13,step=21,color=INK):
  for i,line in enumerate(lines):self.text(x,y+i*step,line,size,color)
 def table(self,x,y,widths,headers,rows,rowheight=31,size=12):
  for i,row in enumerate([headers]+rows):
   xx=x
   for w,v in zip(widths,row):
    self.rect(xx,y+i*rowheight,w,rowheight,fill='#e5edf2' if i==0 else ('#f4f7f9' if i%2 else 'white'),stroke='#ced8df')
    self.text(xx+9,y+i*rowheight+rowheight*.66,str(v),size,weight=i==0);xx+=w

def draw_services(m,l):
 q=l['sheet4'];d=Drawing(4,q['title'],q['subtitle'])
 d.text(45,145,'SV service ports shown; one module per absorber chamber. All sizes and charging pressures remain unresolved.',12)
 xs=[q['module_first_x']+q['module_spacing']*i for i in range(12)]
 circuits=[str(n)+c for n in m['assemblies'] for c in m['chambers']]
 ny=q['charge_header_y'];ry=q['discharge_header_y'];y=q['module_y']
 # Gaps at clean-header crossings distinguish the discharge branches from junctions.
 for x,c in zip(xs,circuits):
  a=x-18;b=x+18
  d.line([(a,y+70),(a,ny)],GAS,1.8)
  d.line([(b,y+70),(b,ny-5)],RETURN,1.8);d.line([(b,ny+5),(b,ry)],RETURN,1.8)
  d.rect(x-33,y,66,70,fill='#f4f7f9')
  d.text(x,y+25,'SV-'+c,10,weight=True,anchor='middle');d.text(x,y+45,'Module',10,anchor='middle');d.text(x,y+61,c,10,anchor='middle')
  for xx,yy,tag,col in [(a,310,'V-'+c+'N',GAS),(b,290,'V-'+c+'R',RETURN)]:
   d.rect(xx-9,yy-11,18,22,fill='white',stroke='white')
   d.line([(xx-7,yy-9),(xx+7,yy-9),(xx-7,yy+9),(xx+7,yy+9),(xx-7,yy-9)],col,1.5)
   d.text(xx,yy+27,tag,8,col,anchor='middle')
  d.arrow(a,360,'up',GAS);d.line([(a-7,356),(a+7,356)],GAS,1.5);d.text(a,382,'NRV-'+c,8,GAS,anchor='middle')
  d.arrow(b,470,'down',RETURN)
  d.text(a,427,'N-'+c,9,GAS,anchor='middle');d.text(b,545,'G-'+c,9,RETURN,anchor='middle')
 d.line([(q['charge_header_ends'][0],ny),(q['charge_header_ends'][1],ny)],GAS,2.5)
 d.line([(q['discharge_header_ends'][0],ry),(q['discharge_header_ends'][1],ry)],RETURN,2.5)
 for x in xs:d.circle(x-18,ny,3,GAS,GAS);d.circle(x+18,ry,3,RETURN,RETURN)
 d.text(45,ny-12,'H-700N',11,GAS,weight=True);d.text(45,ry-12,'H-700R',11,RETURN,weight=True)
 d.line(q['charge_source_route'],GAS,2.3);d.line(q['discharge_receiving_route'],RETURN,2.3)
 d.arrow(45,455,'up',GAS);d.arrow(930,600,'down',RETURN)
 d.text(230,575,'N-700',11,GAS);d.text(1000,575,'G-700',11,RETURN)
 d.rect(*q['nitrogen_box'],fill='#edf6f8',stroke=GAS);d.rect(*q['treatment_box'],fill='#f3eff7',stroke=RETURN)
 d.texts(85,633,['B-700N  Nitrogen charging supply','From B-602 distribution in gas-treatment area','Supply isolation / conditioning: details pending'],11,20)
 d.texts(815,633,['B-700T  Gas-treatment inlet','Service discharge enters before treatment','Treatment capacity and backpressure: pending'],11,20)
 d.texts(420,630,['Separate lines run between the','gas-treatment area and modules.','No direct atmospheric discharge shown.'],12,21)
 d.texts(45,720,[
 'Normal duty: both module service isolation valves closed. Charge: N open / R closed. Discharge: N closed / R open.',
 'These are intended connection states, not procedures. Valve actuation, fail positions, sequencing and pressure limits are unresolved.',
 'NRV symbols reserve charging-branch nonreturn functions; device selection and backflow-protection design remain open.',
 'Surge-vessel service ports are provisional. Servicing other isolated gas spaces and module-side dead-leg volumes need review.'
 ],12,21)
 d.footer()


def render():
 global OUT
 m,l,b,r,records=load();OUT=ROOT/'outputs/current';OUT.mkdir(parents=True,exist_ok=True)
 base.W=1200;base.H=848;base.PDF=canvas.Canvas(str(OUT/'WISTR-absorber-PID.pdf'),pagesize=landscape(A3))
 base.PDF.setTitle('WISTR absorber system preliminary P&ID and capacity review')
 d=Drawing(1,l['sheet1']['title'],l['sheet1']['subtitle'])
 d.rect(445,135,690,510,fill='#f4f7f9',stroke=MUTED,dash=True)
 d.text(465,156,'MODULE-701A  /  separate pressure and surge volumes required',13,weight=True)
 for key,pts in l['sheet1']['routes'].items():d.line(pts,SALT if key=='salt' else GAS,2.8 if key=='salt' else 2)
 for key,(x,y,w,h) in l['sheet1']['boxes'].items():
  if key=='C':
   d.circle(x+w/2,y+h/2,26);d.text(x+w/2,y+h/2+5,'C',17,weight=True,anchor='middle');d.line([(1080,350),(1080,364)],GAS,2);d.line([(1080,416),(1080,430)],GAS,2);d.text(1035,394,'C-701A',12,weight=True,anchor='end')
  else:
   d.rect(x,y,w,h,fill='white',stroke=SALT if key in ('AT','RS') else INK)
   d.text(x+w/2,y+26,key+'-701A',15,weight=True,anchor='middle')
   names={'AT':['Primary chamber','core-bottom salt feed','top gas return'],'RS':['Heated reservoir','salt + gas space'],'PV':['Pressure gas'],'SV':['Surge gas'],'XV':['Gas-routing block','3 positions (sheet 2)']}
   for j,t in enumerate(names[key]):d.text(x+w/2,y+51+j*21,t,12,anchor='middle')
 for tag,x,y in [('R',478,390),('A',478,430),('P',617,390),('S',617,430)]:d.text(x,y+4,tag,12,GAS,True,'middle')
 d.text(75,685,'L-SALT-701A: 50 mm OD; heated and insulated; reversible',12,SALT)
 d.text(77,350,'To active-core bottom',11,SALT)
 d.arrow(70,550,'down',SALT);d.arrow(205,642,'up',SALT)
 d.text(302,142,'G-R-701A',10,GAS);d.text(312,420,'G-A-701A',10,GAS)
 d.text(646,380,'G-P-701A',10,GAS);d.text(646,454,'G-S-701A',10,GAS)
 d.arrow(1080,470,'up',GAS);d.arrow(1020,235,'left',GAS)
 d.text(1092,500,'G-CI-701A',10,GAS,anchor='middle');d.text(1037,222,'G-CO-701A',10,GAS,anchor='middle')
 d.text(1035,582,'Gas recovery',11,GAS,anchor='middle')
 d.inst(335,270,'LT','701AR',290,270,color=PROP);d.inst(335,200,'TT','701AR',290,200,color=PROP)
 d.inst(335,545,'LT','701AA',290,545,color=PROP)
 d.inst(760,183,'PT','701AP',820,190,color=PROP);d.inst(760,605,'PT','701AS',820,590,color=PROP)
 d.text(474,495,'Valve hardware, actuation and',12,PROP);d.text(474,514,'loss-of-power state: unresolved',12,PROP)
 # Separate service ports on the surge vessel; provisional internal module connection.
 for key,colour in [('charge',GAS),('discharge',RETURN)]:d.line(l['sheet1']['services'][key],colour,2)
 d.valve(*l['sheet1']['services']['charge_valve'],'V-701AN',color=GAS)
 d.valve(*l['sheet1']['services']['discharge_valve'],'V-701AR',color=RETURN)
 d.arrow(780,660,'right',GAS);d.line([(784,652),(784,668)],GAS,1.5);d.text(780,642,'NRV-701A',9,GAS,anchor='middle')
 d.text(700,682,'N-701A from H-700N (sheet 4)',10,GAS)
 d.text(1105,708,'G-701A to H-700R (sheet 4)',10,RETURN,anchor='end')
 d.arrow(1085,690,'right',RETURN)
 d.texts(45,729,[
 'Arrows on salt line show injection; recovery reverses flow. Gas lines from reservoir/chamber: 25 mm OD visual allowance.',
 'Amber instruments are proposals. Heater controls, relief paths and compressor nonreturn details remain open.',
 'Charge and discharge service valves are closed in normal duty. Separate return goes to gas treatment before any release.',
 'This sheet defines functions and endpoints. It does not assign shutdown logic, pressure ratings, valve sizing or insertion time.'
 ],12,17)
 d.footer()
 d=Drawing(2,'Circuit repetition and operating functions','A = primary, B = secondary; radial centre/outer assignment remains to be confirmed')
 d.text(40,145,'GAS ROUTING FUNCTION',14,weight=True)
 d.table(40,160,[140,235,745],['Position','Connected ports','Intended effect'],[
 ['Remove','P-A and R-S','Pressure on absorber; salt returns to reservoir; reservoir gas enters surge vessel'],
 ['Hold','All four blocked (proposed)','Isolated process gas; confirm hold behavior and loss-of-power response'],
 ['Inject','P-R and A-S','Pressure on reservoir; displaced absorber gas enters surge vessel']],34,12)
 d.text(40,325,'TWELVE INDEPENDENT CIRCUITS',14,weight=True)
 rows=[]
 for n in m['assemblies']:rows.append([n-700,f'AT / RS / PV / SV / C / XV - {n}A',f'AT / RS / PV / SV / C / XV - {n}B'])
 d.table(40,340,[100,510,510],['Assembly','Primary circuit','Secondary circuit'],rows,34,12)
 d.texts(40,620,[
 'Each circuit has one absorber chamber, one salt reservoir, two gas volumes, one recovery compressor and a routing function.',
 'Six stationary absorber tanks each contain two chambers. Each chamber has its own reservoir and absorber module.',
 'Suggested monitoring: pressure in each gas vessel; reservoir temperature and inventory; chamber fill indication (method unresolved).',
 'Gas recovery is from surge to pressure vessel. Compressor duty, reset sequence and isolation/check arrangements remain unselected.',
 'Normal duty: isolate both service lines per module. Charging and discharge functions and unresolved controls are on sheet 4.',
 'Machine-readable equipment, line and instrument records expand all twelve circuits; a register accompanies this drawing.'
 ],13,24)
 d.footer()
 d=Drawing(3,'Capacity check against the current 3D model','Source charges retained; measured site elevations; owner excludes the 0.30 m bottom-reflector region')
 d.text(45,149,'VERTICAL GEOMETRY',14,weight=True)
 # Diagram: schematic elevations, emphasizing actual free-surface differences rather than drawing distance.
 d.rect(80,185,110,65,fill='#f3e1d7',stroke=SALT);d.text(135,210,'Reservoir',12,anchor='middle');d.text(135,231,'643 L gross',12,anchor='middle')
 d.rect(100,430,90,185,fill='#edf3f6');d.rect(100,443,90,172,fill='#d6e5e6',stroke=GAS)
 for yy,label in [(250,'Reservoir bottom Z = -0.05 m'),(430,'Tank top Z = -3.62 m'),(458,'Core top Z = -3.87 m'),(603,'Chamber/core bottom = -7.27 m')]:
  d.line([(190,yy),(215,yy)],MUTED,1);d.text(220,yy+4,label,12)
 d.line([(65,250),(65,430)],MUTED,1);d.text(75,355,'3.57 m',12,MUTED)
 d.text(102,520,'Active',12);d.text(102,540,'3.4 m',12);d.text(102,560,'band',12)
 d.text(530,149,'VOLUMES PER ASSEMBLY / CIRCUIT',14,weight=True)
 d.table(530,165,[330,270],['Item','Volume'],[
 ['Absorber tank (both chambers)',f"{1000*r['absorber_tank_gross_m3']:.1f} L gross"],['Active-height absorber tank envelope',f"{1000*r['absorber_tank_active_gross_m3']:.1f} L gross"],['Source primary + secondary',f"{1000*r['required_primary_secondary_m3']:.1f} L salt"],['3 mm wall/partition trial',f"{1000*r['absorber_tank_trial_net_active_m3']:.1f} L active capacity"],['Each external salt reservoir',f"{1000*r['reservoir_gross_m3']:.1f} L gross"],['Each module lower cylinder',f"{1000*r['module_lower_gross_m3']:.1f} L gross"]],29,12)
 d.text(530,403,'IDEAL GAS SPACE PER MODULE',14,weight=True)
 d.table(530,420,[180,140,140,140],['Case','Pressure','Surge','Total'],[
 [c['chamber'].title()+(' active' if c['case']=='active_band' else ' + gas'),f"{1000*c['pressure_vessel_m3']:.1f} L",f"{1000*c['surge_vessel_m3']:.1f} L",f"{1000*c['gas_vessels_total_m3']:.1f} L"] for c in r['cases']],29,12)
 d.texts(530,590,['+ gas = 0.25 m upper space retained as gas, not salt.',
 'Lower-cylinder fit is tight for secondary; upper box space',
 'may be needed. Heads, walls and equipment are additional.'],12,20)
 d.texts(45,686,[
 'Gas-space estimates use equal-temperature isothermal balances, source-derived density, zero heel and prefilled salt lines.',
 'Both cases exclude the bottom reflector. The second includes provisional upper gas space; neither adds salt below the core.',
 'No updated injection time: viscosity, final hydraulic route, gas restrictions and required shutdown time remain unresolved.',
 'Source: AbsorberSaltInjectionTime.docx, pp. 1-6. See the editable Hurmet worksheet for equations, assumptions and checks.',
 'The existing 3D salt tubes stop at the absorber tank top. External connections at the active-core bottom are shown on sheet 1, pending 3D routing.'
 ],12,20)
 d.footer();draw_services(m,l);base.PDF.save()
 (OUT/'expanded-model.json').write_text(json.dumps(records,indent=2)+'\n')
 with (OUT/'register.csv').open('w') as f:
  fields=['tag','kind','assembly','chamber','name','service','from','to','on','line','type','normal_state','status'];w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(records)
 checks={'passed':True,'circuits':12,'equipment':76,'lines':110,'instruments':60,'service_valves':36,'checks':['Unique expanded tags','All line endpoints name declared ports','Every template line has a drawn route','All instruments name declared equipment','Inject and remove states retain documented endpoint pairing','All 12 modules have separate charge and discharge branches','Discharge terminates at treatment inlet','No discharge edge enters clean nitrogen header','All 36 service valve reservations reference valid lines'],
 'sources':{str(p.relative_to(HUB)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'absorber-system.toml',ROOT/'layout.toml',ROOT/m['engineering'],Path(__file__),ROOT.parent/'coolant-system/build.py',HUB/'calculations/reactor/absorber-capacity-results.json']}}
 (OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
if __name__=='__main__':render()
