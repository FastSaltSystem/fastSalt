"""Frame the supplied drawing and owner clarifications without designing new circuits."""
from pathlib import Path
import csv, hashlib, html, json, os, subprocess, tomllib, textwrap
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

HERE=Path(__file__).resolve().parent
OUT=HERE/'outputs/current'
OUT.mkdir(parents=True,exist_ok=True)
basis=tomllib.loads((HERE/'fuel-maintenance.toml').read_text())
source=HERE/basis['source'];raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()==basis['source_sha256']
SVG='http://www.w3.org/2000/svg';ET.register_namespace('',SVG)
root=ET.fromstring(raw)
path_before=[dict(e.attrib) for e in root.iter('{'+SVG+'}path')]
# Replace the old partial left-hand region label with the owner's six-region
# clarification. The source file itself is preserved byte-for-byte.
for parent in root.iter():
 for child in list(parent):
  if child.tag=='{'+SVG+'}text' and '52.838, 446.516' in child.get('transform',''):
   parent.remove(child)
for i,x in enumerate((44,88,130,171,208,244),1):
 t=ET.SubElement(root,'{'+SVG+'}text',{'x':str(x),'y':'470','font-family':'Helvetica, Arial, sans-serif','font-size':'10','text-anchor':'middle','fill':'#172b3a'})
 t.text='R'+str(i)
# Update the derivative legend to reflect the owner-added fourth core position.
for elem in root.iter('{'+SVG+'}text'):
 if 'Each valve with 3 positions:' in ''.join(elem.itertext()):
  for child in list(elem): elem.remove(child)
  for j,line in enumerate(['Core valves: 4 positions','1 Add pressure','2 Maintain','3 Reduce pressure','4 Vent to off-gas','Storage valves: positions 1-3']):
   t=ET.SubElement(elem,'{'+SVG+'}tspan',{'x':'-61.421','y':str(-15+j*10),'font-family':'Helvetica','font-size':'8','fill':'#000000'})
   t.text=line
assert path_before==[dict(e.attrib) for e in root.iter('{'+SVG+'}path')]
root.set('x','30');root.set('y','137');root.set('width','850');root.set('height','657');root.set('overflow','hidden')
art=ET.tostring(root,encoding='unicode')
W,H=1190,842

def text(x,y,value,size=12,weight='normal',color='#233746'):
 return f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(value)}</text>'
def rect(x,y,w,h,fill='#f0f4f6',stroke='none'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>'
def frame(number,subtitle):
 return [f'<svg xmlns="{SVG}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',rect(0,0,W,H,'white'),
 text(30,38,'FAST SALT SYSTEM | Fuel maintenance',24,'bold'),text(30,65,subtitle,15),
 text(30,88,'A5 draft | 15 October 2026 | Original paths retained; owner additions on sheet 7',11,color='#536979'),
 '<path d="M30 102 H1160" stroke="#aebfc9"/>',text(30,824,'Source: owner-supplied Fuel Maintenance.svg + owner clarifications and state description',10,color='#536979'),
 text(1020,824,f'FS-FM-00{number} | {number} / 7',10,color='#536979')]

a=frame(1,'Representative core sector and its associated maintenance tank')
a += [text(30,122,'Six core regions -> three paired storage regions. Region numbers are local to each sector.',12,'bold'),art]
a += [rect(900,132,260,662),text(915,156,'SOURCE REFERENCE INDEX',13,'bold')]
y=180
for item in basis['items']:
 a.append(text(915,y,item['ref']+'  '+item['label'],11,'bold'))
 a.append(text(938,y+15,item['location'],10,color='#536979'));y+=44
for i,line in enumerate(['References identify source labels,','not approved plant equipment tags.','','The left-hand R1-R6 labels reflect','the owner clarification. Core valve','legend updated; additions on sheet 7.','','Service-equipment sharing across','sectors remains unspecified.']):
 a.append(text(915,650+i*14,line,10,color='#536979'))
a.append('</svg>')

b=frame(2,'Confirmed repetition, source register and open points')
b += [text(30,132,'CONFIRMED SECTOR / STORAGE GROUPING',15,'bold')]
cols=[30,155,385,635]
for x,label in zip(cols,['Core sector','Core regions','Storage regions in associated tank','Maintenance tank']):b.append(text(x,163,label,12,'bold'))
for i in range(6):
 y=180+i*34;b.append(rect(30,y-8,850,32,'#f0f4f6' if i%2==0 else '#ffffff'))
 for x,label in zip(cols,[f'Sector {i+1}','R1, R2, R3, R4, R5, R6','R1/R2; R3/R4; R5/R6',f'One for sector {i+1}']):b.append(text(x,y+13,label,12))
b += [text(30,409,'Six sectors and six maintenance tanks; internal regions are not yet represented in 3D.',12,'bold'),
 text(30,432,'The three valve symbols in each bank represent one shared valve per region pair.',12),
 text(30,455,'This table does not multiply or assign the source pressure/surge vessels, compressor or fuel pumps.',11,color='#536979')]
b += [text(30,494,'SOURCE SYMBOL REGISTER',15,'bold')]
y=520
for item in basis['items']:
 b += [text(30,y,item['ref'],11,'bold'),text(62,y,item['label'],11),text(435,y,item['shown'],11,color='#536979')];y+=24
b += [rect(900,132,260,654),text(915,157,'OPEN POINTS',14,'bold')]
notes=[['Service-equipment assignment','Sharing or repetition across sectors','is not specified by the drawing.'],['External fuel interfaces','The right-hand line endpoints do not','identify the connected equipment.'],['Valves and instruments','Owner additions are on sheet 7.','Detailed hardware and tags are open.'],['Crossings','Paths are preserved. A crossing is','not inferred to be a junction.'],['3D cross-reference','The existing tank F-number mapping','and internal regions need recording.'],['Draft status','This is a source-transcribed drawing,','not a completed engineering P&ID.']]
y=188
for note in notes:
 b.append(text(915,y,note[0],11,'bold'))
 for j,line in enumerate(note[1:],1):b.append(text(915,y+j*16,line,10,color='#536979'))
 y+=91
b.append('</svg>')
state=basis['owner_states']['remove_fuel']
c=frame(3,'Remove fuel | owner-described state')
c += [text(30,144,'VALVE POSITIONS DURING REMOVAL',16,'bold')]
for y,label,value in [(185,'All core-pressure valves',state['core_pressure_valves']),
                      (243,'All maintenance-pressure valves',state['maintenance_pressure_valves'])]:
 c += [rect(30,y-23,1130,48),text(48,y+7,label,16),text(650,y+7,value,18,'bold')]
c += [text(30,324,'RETURN TO MAINTAIN FOR EACH PAIR',16,'bold'),
      text(30,361,'Owner-specified empty indication: '+state['empty_indication']+'.',16)]
for j,line in enumerate(textwrap.wrap(state['on_empty'],95)):
 c.append(text(30,395+24*j,line,16))
c += [text(30,472,'COMPLETION',16,'bold'),text(30,508,state['completion'],16),
      text(30,566,'OWNER DESCRIPTION - SOURCE TEXT',13,'bold')]
for j,line in enumerate(textwrap.wrap(state['verbatim'],135)):
 c.append(text(30,594+21*j,line,13))
c += [text(30,748,'Recorded from the owner description, 15 October 2026. Sensor functions are on sheet 7; automation is not specified.',12,color='#536979'),
      text(30,771,'Maintenance-pressure valves correspond to the storage-pressure valve bank on sheet 1.',12,color='#536979'),'</svg>']
state=basis['owner_states']['fill_fuel']
d=frame(4,'Fill fuel | owner-described state')
d += [text(30,144,'VALVE POSITIONS DURING FILLING',16,'bold')]
for y,label,value in [(185,'All core-pressure valves',state['core_pressure_valves']),
                      (243,'All maintenance-pressure valves',state['maintenance_pressure_valves'])]:
 d += [rect(30,y-23,1130,48),text(48,y+7,label,16),text(650,y+7,value,18,'bold')]
d += [text(30,324,'RETURN TO MAINTAIN FOR EACH PAIR',16,'bold'),
      text(30,359,state['empty_indication']+' '+state['indication_meaning'],16)]
for j,line in enumerate(textwrap.wrap(state['on_empty'],100)):
 d.append(text(30,393+24*j,line,16))
d += [text(30,462,'COMPLETION',16,'bold'),text(30,498,state['completion'],16),
      text(30,550,'OWNER DESCRIPTION - SOURCE TEXT',13,'bold')]
for j,line in enumerate(textwrap.wrap(state['verbatim']+' '+state['completion_verbatim'],135)):
 d.append(text(30,578+21*j,line,13))
d += [text(30,748,'Recorded from the owner description, 15 October 2026.',12,color='#536979'),
      text(30,771,'Maintenance-pressure valves correspond to the storage-pressure valve bank on sheet 1.',12,color='#536979'),'</svg>']
state=basis['owner_states']['add_small_fuel_r6']
e=frame(5,'Small fuel addition to R6 | owner-described state')
e += [text(30,144,'METERED ADDITION',16,'bold')]
for j,line in enumerate(textwrap.wrap(state['metering'],105)):
 e.append(text(30,179+24*j,line,16))
e += [text(30,240,'R5/R6 VALVE POSITIONS',16,'bold')]
for y,label,value in [(280,'R5/R6 core-pressure valve',state['core_pressure_valve']),
                      (338,'R5/R6 maintenance-pressure valve',state['maintenance_pressure_valve'])]:
 e += [rect(30,y-23,1130,48),text(48,y+7,label,16),text(650,y+7,value,18,'bold')]
e += [text(30,395,state['valve_position_basis'],12,color='#536979'),
      text(30,450,'COMPLETION',16,'bold'),
      text(30,485,state['completion_indication']+': '+state['on_completion'],16),
      text(30,550,'OWNER DESCRIPTION - SOURCE TEXT',13,'bold')]
for j,line in enumerate(textwrap.wrap(state['source_metering']+' '+state['source_valves'],135)):
 e.append(text(30,578+21*j,line,13))
for j,line in enumerate(textwrap.wrap(state['open_point'],140)):
 e.append(text(30,748+20*j,line,12,color='#536979'))
e.append('</svg>')
state=basis['owner_states']['remove_measured_fuel_r1_r2']
f_sheet=frame(6,'Measured fuel removal from R1/R2 | owner-described state')
f_sheet += [text(30,144,'METERED REMOVAL',16,'bold')]
for y,label,value in [(190,'Region pair',state['region_pair']),
                      (248,'Pump',state['pump'])]:
 f_sheet += [rect(30,y-23,1130,48),text(48,y+7,label,16),text(450,y+7,value,18,'bold')]
f_sheet += [text(30,330,state['action'],16),
            text(30,440,'OWNER DESCRIPTION - SOURCE TEXT',13,'bold')]
for j,line in enumerate(textwrap.wrap(state['verbatim'],135)):
 f_sheet.append(text(30,478+21*j,line,13))
f_sheet += [text(30,748,'Recorded from the owner description, 15 October 2026.',12,color='#536979'),'</svg>']
inst=basis['owner_instrumentation']
g=frame(7,'Instrumentation and core-valve off-gas position | owner additions')
def line(x1,y1,x2,y2,color='#607d8b'):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"/>'
def sensor(x,y,label):
 return [f'<circle cx="{x}" cy="{y}" r="19" fill="white" stroke="#236b87" stroke-width="2"/>',text(x-5,y+5,label,14,'bold')]
g += [text(30,135,'ONE MAINTENANCE TANK: THREE STORAGE REGIONS',15,'bold'),
      text(30,160,'L = level sensor     P = pressure sensor     G = gas-in-line sensor (functional symbols; tags not assigned)',12)]
for x,pair in zip((30,415,800),basis['pairs']):
 g += [rect(x,185,330,125,'#f0f4f6','#607d8b'),text(x+22,211,pair['label']+' storage region',15,'bold')]
 g += sensor(x+100,259,'L')+sensor(x+230,259,'P')
 g += [line(x+165,310,x+165,350),line(x+165,350,x+270,350)]
 g += sensor(x+270,350,'G')
 g += [text(x+22,389,'Bottom line for this region pair',12)]
g += [text(30,420,'Six tanks: 18 level sensors, 18 storage-pressure sensors and 18 bottom-line gas sensors.',12,'bold'),
      text(30,456,'GAS EQUIPMENT: PRESSURE SENSING AND REGULATOR LOCATION',15,'bold')]
for x,w,title in [(30,190,'Pressure tank'),(310,180,'Compressor'),(580,190,'Pressure regulator'),(900,230,'Surge tank')]:
 g += [rect(x,486,w,65,'#f0f4f6','#607d8b'),text(x+12,524,title,14,'bold')]
g += [line(490,518,580,518),line(770,518,900,518)]
g += [line(125,551,125,561),line(1015,551,1015,561)]
g += sensor(125,580,'P')+sensor(1015,580,'P')
g += [text(503,578,'Regulator sets pressure difference.',12),
      text(310,607,'Differential-pressure reference points and sensing connections remain unspecified.',11,color='#536979'),
      text(30,646,'CORE PRESSURE VALVES: FOUR SELECTABLE POSITIONS',15,'bold')]
for x,w,label in [(30,200,'1  Add pressure'),(245,180,'2  Maintain'),(440,215,'3  Reduce pressure'),(670,230,'4  Vent to off-gas')]:
 g += [rect(x,665,w,44),text(x+12,693,label,14,'bold')]
g += [line(900,687,952,687),'<path d="M944 682 L954 687 L944 692" fill="none" stroke="#607d8b" stroke-width="2"/>',
      text(965,692,'Off-gas system',14,'bold'),
      text(30,737,'Storage pressure valves retain positions 1-3. The four core positions are alternatives, not a sequence.',12),
      text(30,765,'Functional locations only; source-equipment sharing across sectors remains open.',11,color='#536979'),'</svg>']
for i,parts in enumerate((a,b,c,d,e,f_sheet,g),1):(OUT/f'FS-FM-00{i}.svg').write_text('\n'.join(parts))
# Rasterize native SVG artwork at 2400 pixels for printable previews/PDF.
node=os.environ.get('NODE','node')
code="""const sharp=require('sharp');const p=process.argv.slice(1);(async()=>{for(const f of p)await sharp(f,{density:150}).resize({width:2400}).flatten({background:'#ffffff'}).png().toFile(f.replace(/svg$/,'png'));})().catch(e=>{console.error(e);process.exit(1)});"""
subprocess.run([node,'-e',code,*[str(OUT/f'FS-FM-00{i}.svg') for i in (1,2,3,4,5,6,7)]],check=True)
pdf=canvas.Canvas(str(OUT/'WISTR-fuel-maintenance-source-draft.pdf'),pagesize=(W,H))
pdf.setTitle('Fuel maintenance - source-transcribed P&ID-style draft')
for i in (1,2,3,4,5,6,7):pdf.drawImage(ImageReader(str(OUT/f'FS-FM-00{i}.png')),0,0,width=W,height=H);pdf.showPage()
pdf.save()
with (OUT/'source-register.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['ref','label','shown','location']);w.writeheader();w.writerows(basis['items'])
checks={'source_sha256':basis['source_sha256'],'source_paths_unchanged':True,'source_path_count':len(path_before),'owner_confirmed_grouping':basis['owner_clarification'],'owner_states':basis['owner_states'],'sheet_count':7,'owner_instrumentation':basis['owner_instrumentation'],'owner_valve_positions':basis['owner_valve_positions'],'scope':'Source preservation, transcription and document checks only; no engineering validation.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Source-transcribed sheets generated; original path attributes preserved.')
