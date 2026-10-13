"""Render the coolant model and its independent layout. See README.md for workflow."""
from pathlib import Path
import argparse, csv, hashlib, html, json, re
import tomllib
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"engineering"))
from fast_salt_engineering import coolant as shared_coolant
from reportlab.pdfgen import canvas
from reportlab.lib.colors import toColor as HexColor
from reportlab.lib.pagesizes import A3, landscape
ROOT = Path(__file__).resolve().parent
INK='#173345'; MUTED='#546772'; HOT='#b7442e'; COLD='#147689'; PROP='#946200'; LINE='#274453'; LIGHT='#edf3f6'

class ModelError(ValueError):
    pass

def restore_unresolved(value, path='root'):
    """Decode our explicit unresolved_fields convention, without losing values."""
    if isinstance(value, dict):
        fields=value.pop('unresolved_fields', [])
        if not isinstance(fields,list) or any(not isinstance(k,str) for k in fields):
            raise ModelError(f'{path}: unresolved_fields must be a list of field names')
        if len(fields)!=len(set(fields)):
            raise ModelError(f'{path}: duplicate unresolved field')
        for key in fields:
            if key == 'unresolved_fields' or key in value:
                raise ModelError(f'{path}.{key}: cannot be both assigned and unresolved')
            value[key]=None
        for key,item in value.items():restore_unresolved(item, f'{path}.{key}')
    elif isinstance(value,list):
        for i,item in enumerate(value):restore_unresolved(item, f'{path}[{i}]')
    return value

def parse(text):
    try:
        return restore_unresolved(tomllib.loads(text))
    except tomllib.TOMLDecodeError as error:
        raise ModelError(f'Invalid TOML: {error}') from error

def load(path):
    path=Path(path)
    data=parse(path.read_text(encoding='utf-8'))
    if 'shared_engineering' in data:
        source=(path.parent/data['shared_engineering']['model']).resolve()
        try:
            data=shared_coolant.merge_pid(data,shared_coolant.read(source))
        except ValueError as error:
            raise ModelError(str(error)) from error
    return data

def context(model):
    # Tags are the TOML table keys, so renaming never leaves a second tag field to update.
    return {**model, **{group: {tag: {**item, 'tag': tag} for tag, item in model[group].items()}
                       for group in ('equipment', 'boundaries', 'lines', 'instruments', 'valves')}}

TOKEN = re.compile(r'\$\{([^}:]+)(?::([^}]+))?\}')
def expand(value, ctx):
    if isinstance(value, str):
        def replace(match):
            node = ctx
            for key in match[1].split('.'):
                if not isinstance(node, dict) or key not in node:
                    raise ModelError(f'Unknown label reference: {match[1]}')
                node = node[key]
            if node is None:
                return 'TBD'
            return format(node, match[2] or '')
        return TOKEN.sub(replace, value)
    if isinstance(value, list): return [expand(x, ctx) for x in value]
    if isinstance(value, dict): return {k: expand(v, ctx) for k, v in value.items()}
    return value

def segments(line):
    start = line['from']; result = []
    for pump in line.get('via', []):
        result.append((start, pump + '.suction'))
        start = pump + '.discharge'
    return result + [(start, line['to'])]

def validate(model, layout):
    """Check topology, source completeness, tag use and coolant route end points."""
    def require(ok, message):
        if not ok: raise ModelError(message)
    require(model.get('schema_version') == 1 and layout.get('schema_version') == 1, 'Unsupported schema_version')
    groups = ('equipment','boundaries','lines','instruments','valves')
    all_tags = [tag for group in groups for tag in model[group]]
    require(len(all_tags) == len(set(all_tags)), 'Tags must be unique across groups')
    ports = set()
    for tag, item in {**model['equipment'], **model['boundaries']}.items():
        require(item.get('name'), f'{tag}: missing name')
        require(len(item['ports']) == len(set(item['ports'])), f'{tag}: duplicate ports')
        ports.update(tag + '.' + port for port in item['ports'])
    for tag, line in model['lines'].items():
        for key in ('from','to','sheet','status','bore_mm','od_mm','wall_mm','radial_insulation_mm','temperature_C'):
            require(key in line, f'{tag}: missing {key}; list unresolved quantities in unresolved_fields')
        for start, end in segments(line):
            require(start in ports and end in ports, f'{tag}: unknown endpoint {start} -> {end}')
        for pump in line.get('via', []):
            require(model['equipment'].get(pump, {}).get('type') == 'pump', f'{tag}: via must reference a pump')
        for key in ('bore_mm','od_mm','wall_mm','radial_insulation_mm'):
            value = line[key]
            require(value is None or isinstance(value, (int,float)) and value > 0, f'{tag}: {key} must be positive or explicitly unresolved')
        b,o,w = (line[k] for k in ('bore_mm','od_mm','wall_mm'))
        if None not in (b,o,w): require(abs(b+2*w-o)<1e-6, f'{tag}: bore + 2*wall must equal OD')
    for group in ('instruments','valves'):
        for tag,item in model[group].items():
            require(item.get('status') in ('proposed','accepted_for_concept'), f'{tag}: status must be proposed or accepted_for_concept')
    for tag, item in model['instruments'].items():
        require(item.get('type') in ('TT','PT','FT','LT'), f'{tag}: unrecognized measurement type')
        require(tag.startswith(item['type']+'-'), f'{tag}: type does not match tag')
        require(item.get('on') in model['lines'] or item.get('on') in model['equipment'], f'{tag}: unknown measured item')
        for key in ('purpose','location','status','sheet'):require(item.get(key), f'{tag}: missing {key}')
    for tag, item in model['valves'].items():
        require(item.get('line') in model['lines'], f'{tag}: unknown line')
        for key in ('purpose','status','sheet'):require(item.get(key), f'{tag}: missing {key}')
    ctx = context(model); seen_inst=[];seen_valves=[];seen_routes=[]
    allowed = {'rect','text','line','circle','arrow','valve','instrument','pump','route'}
    require([s['number'] for s in layout['sheets']] == [1,2], 'This drawing set requires sheets 1 and 2')
    for sheet in layout['sheets']:
        anchors = sheet['ports']
        require(set(anchors) <= ports, f'Sheet {sheet["number"]}: unknown port anchor')
        routes = {}
        for e in sheet['elements']:
            if e['kind']=='route':routes.setdefault(e['line'],[]).append(e['args'][0])
        def on_route(point, tag):
            x,y=point
            for pts in routes.get(tag,[]):
                for (ax,ay),(bx,by) in zip(pts,pts[1:]):
                    cross=(x-ax)*(by-ay)-(y-ay)*(bx-ax)
                    if abs(cross)<1e-6 and min(ax,bx)<=x<=max(ax,bx) and min(ay,by)<=y<=max(ay,by):return True
            return False
        for e in sheet['elements']:
            require(e['kind'] in allowed, f'Unknown layout element: {e["kind"]}')
            expand(e, ctx)  # All dynamic labels must resolve before any files are written.
            kind=e['kind'];tag=e.get('tag')
            if kind in ('instrument','valve'):
                group='instruments' if kind=='instrument' else 'valves'
                require(tag in model[group], f'Unknown {kind}: {tag}')
                require(model[group][tag]['sheet']==sheet['number'], f'{tag}: sheet mismatch')
                (seen_inst if kind=='instrument' else seen_valves).append(tag)
                host=model[group][tag]['on' if kind=='instrument' else 'line']
                if host in model['lines']:
                    point=e['args'][2:4] if kind=='instrument' else e['args'][:2]
                    require(on_route(point,host), f'{tag}: symbol/tap is not on its model line {host}')
            if kind=='pump':require(model['equipment'].get(tag,{}).get('type')=='pump', f'Unknown pump: {tag}')
            if kind=='route':
                tag=e['line'];require(tag in model['lines'], f'Unknown route: {tag}')
                line=model['lines'][tag];seg=e['segment'];pairs=segments(line)
                require(line['sheet']==sheet['number'] and 0<=seg<len(pairs), f'{tag}: invalid route segment/sheet')
                start,end=pairs[seg];points=e['args'][0]
                require(start in anchors and end in anchors, f'{tag}: new endpoints need layout anchors')
                require(points[0]==anchors[start] and points[-1]==anchors[end], f'{tag}: route endpoints do not match model; update layout')
                seen_routes.append((tag,seg))
    for label,seen,expected in [('instruments',seen_inst,set(model['instruments'])),('valves',seen_valves,set(model['valves'])),('routes',seen_routes,{(tag,i) for tag,line in model['lines'].items() for i in range(len(segments(line)))})]:
        require(len(seen)==len(set(seen)), f'Duplicate drawn {label}')
        require(set(seen)==expected, f'Missing or extra drawn {label}: {set(seen)^expected}')
    return {'equipment':len(model['equipment']), 'lines':len(model['lines']), 'instruments':len(seen_inst), 'valves':len(seen_valves), 'route_segments':len(seen_routes)}

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
 def valve(self,x,y,tag,color=PROP):
  self.rect(x-12,y-9,24,18,stroke='white');self.line([(x-10,y-7),(x+10,y+7),(x+10,y-7),(x-10,y+7),(x-10,y-7)],color,1.6)
  self.text(x,y-16,tag,10,color,anchor='middle')
 def inst(self,x,y,kind,num,tapx,tapy,color=PROP):
  # Dashed line denotes measurement association, not tubing or a control signal.
  self.line([(tapx,tapy),(x,y-19 if tapy<y else y+19)],color,1,dash=True)
  self.circle(x,y,19,color);self.text(x,y-1,kind,10,color,True,'middle');self.text(x,y+11,num,9,color,anchor='middle')
 def pump(self,x,y,tag):
  self.circle(x,y,22);self.line([(x+9,y-10),(x-10,y),(x+9,y+10)],INK,1.7)
  self.text(x,y+51,tag,12,weight=True,anchor='middle')
 def footer(self):
  self.line([(35,804),(1165,804)],INK,1)
  self.text(35,824,f"FS-CS-00{self.n} | Rev {DOC['revision']} | {DOC['date']} | {DOC['status']}",11,weight=True)
  self.text(1165,824,f'Sheet {self.n} / 2 | Functional schematic; not to scale',11,anchor='end')
  self.svg.insert(0,f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 {W} {H}" role="img"><title>WISTR coolant system sheet {self.n}</title>')
  self.svg.append('</svg>');(OUTPUT/f'FS-CS-00{self.n}.svg').write_text('\n'.join(self.svg))
  PDF.restoreState();PDF.showPage()


def register(output, name, fields, rows):
    with (output/name).open('w', newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

def write_registers(model, output):
    for group in ('instruments','valves'):
        fields=['tag']+list(next(iter(model[group].values())))
        register(output,group+'.csv',fields,[{'tag':tag,**item} for tag,item in model[group].items()])
    fields=['tag','from','via','to','bore_mm','od_mm','wall_mm','radial_insulation_mm','temperature_C','heated','status','sheet']
    rows=[]
    for tag,item in model['lines'].items():
        row={field:('TBD' if item.get(field) is None else item[field]) for field in fields[1:]}
        row['tag']=tag;row['via']='; '.join(item['via']);rows.append(row)
    register(output,'lines.csv',fields,rows)
    register(output,'equipment.csv',['tag','name','type','status'],[{'tag':tag,**{k:item[k] for k in ('name','type','status')}} for tag,item in model['equipment'].items()])

def render(model, layout, output):
    global PDF, OUTPUT, DOC, W, H
    OUTPUT=output;DOC=model['document'];W=layout['page']['width'];H=layout['page']['height']
    output.mkdir(parents=True,exist_ok=True)
    PDF=canvas.Canvas(str(output/'WISTR-coolant-PID.pdf'),pagesize=landscape(A3),invariant=1)
    PDF.setTitle(DOC['title']+' - preliminary P&ID - '+DOC['revision']);PDF.setAuthor('Fast Salt System project')
    ctx=context(model)
    for sheet in layout['sheets']:
        d=Drawing(sheet['number'],expand(sheet['title'],ctx),expand(sheet['subtitle'],ctx))
        for raw in sheet['elements']:
            e=expand(raw,ctx);kind=e['kind'];a=e['args'];style=e.get('style',{})
            if kind=='instrument':
                tag=e['tag'];kind_code,number=tag.split('-',1)
                d.inst(a[0],a[1],kind_code,number,a[2],a[3],color=PROP if model['instruments'][tag]['status']=='proposed' else INK,**style)
            elif kind=='valve':d.valve(*a,e['tag'],color=PROP if model['valves'][e['tag']]['status']=='proposed' else INK,**style)
            elif kind=='pump':d.pump(*a,e['tag'],**style)
            else:getattr(d,'line' if kind=='route' else kind)(*a,**style)
        d.footer()
    PDF.save();write_registers(model,output)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',type=Path,default=ROOT/'coolant-system.toml')
    parser.add_argument('--layout',type=Path,default=ROOT/'layout.toml')
    parser.add_argument('--output',type=Path,default=ROOT/'outputs'/'current')
    parser.add_argument('--check',action='store_true',help='Validate without writing outputs')
    args=parser.parse_args()
    try:
        model,layout=load(args.model),load(args.layout);counts=validate(model,layout)
        if not args.check:
            # Routine builds must never overwrite the named Revision A package.
            if args.output.resolve()==ROOT:raise ModelError('Use an output subdirectory; the root holds the preserved Rev A snapshot')
            render(model,layout,args.output)
            inputs=[args.model,args.layout,Path(__file__)]
            (args.output/'build-manifest.json').write_text(json.dumps({'document':model['document'],'validated':counts,'shared_engineering':model.get('shared_provenance',{}),'inputs':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs]},indent=2)+'\n')
        print(('Validated' if args.check else 'Built')+': '+json.dumps(counts))
    except (ModelError, KeyError, TypeError) as error:
        parser.exit(1, f'P&ID validation failed: {error}\n')
if __name__=='__main__':main()
