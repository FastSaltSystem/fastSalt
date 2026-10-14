"""Read the adopted counterSG workbook and independently verify its thermal length.

Standard-library reader of saved cell values; never executes workbook code.
The source workbook was recalculated during adoption. Stop on stale key caches.
"""
from pathlib import Path
import hashlib,json,math,zipfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'sources/counterSG.xlsx'

def read_basis():
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(SOURCE) as z:
        strings=[''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        cells={}
        for c in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:c',ns):
            v=c.find('m:v',ns)
            if v is None:continue
            cells[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else float(v.text)
    def close(x,y):
        if not math.isclose(x,y,rel_tol=1e-10,abs_tol=1e-10):raise ValueError(f'Workbook cache disagrees: {x} vs {y}')
    assert cells['AB16']=='salt inlet temperature (K)' and cells['AB17']=='salt outlet temperature (K)'
    n=cells['AC7'];bore=cells['AC8']/100;wall=cells['AC9']/1000
    area=math.pi*bore*bore/4;contact=3/6*math.pi*(bore+2*wall)
    duty=cells['AC2']*1000;hot=cells['AC16'];cold=cells['AC17']
    water=duty/(cells['F65']-cells['F3'])
    salt=duty/(cells['AC24']*(hot-cold)+.5*cells['AD24']*(hot*hot-cold*cold))
    salt_count=n*3/4
    for x,y in [(water,cells['AC5']),(salt,cells['AC19']),(salt_count,cells['AC20']),(contact,cells['AC31'])]:close(x,y)
    t_salt=cold;length=0.;prev=None;velocities=[]
    for r in range(3,66):
        t,rho,cp,mu,k,h=[cells[f'{c}{r}'] for c in 'ABCDEF']
        if prev:
            q=(h-prev['h'])*water/n
            t_salt+=q*(4/3)/(salt/salt_count)/prev['cp']
        rs=cells['AC23']+cells['AD23']*t_salt
        cps=cells['AC24']+cells['AD24']*t_salt
        mus=cells['AC25']*math.exp(cells['AD25']/t_salt)
        ks=cells['AC26']+cells['AD26']*t_salt
        vw=(water/n)/area/rho;vs=(salt/salt_count)/area/rs;velocities.append(vs)
        hw=.0266*(rho*vw*bore/(mu*1e-6))**.805*(1000*cp*mu*1e-6/k)**(1/3)*k/bore
        hs=.0266*(rs*vs*bore/mus)**.805*(1000*cps*mus/ks)**(1/3)*ks/bore
        resistance=1000/hw+1000/hs+2*wall/cells['AC28']*1000
        dt=t_salt-t
        if prev:
            lmtd=(prev['dt']-dt)/math.log(prev['dt']/dt)
            dl=q*resistance/lmtd/contact;length+=dl
            close(dl,cells[f'Y{r}']);close(length,cells[f'Z{r}'])
        close(t_salt,cells[f'M{r}'])
        prev=dict(h=h,dt=dt,cp=cps)
    close(length,cells['Y66'])
    return dict(source='sources/counterSG.xlsx',sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),sheet='counter',
        salt_tubes_per_generator=int(salt_count),steam_tubes_per_generator=int(n),
        tube_bore_m=bore,tube_wall_m=wall,tube_length_m=length,duty_MW=cells['AC2'],
        salt_hot_K=hot,salt_cold_K=cold,water_in_K=cells['AC4'],water_out_K=cells['AC3'],
        workbook_salt_flow_per_generator_kg_s=salt,workbook_water_flow_per_generator_kg_s=water,
        workbook_salt_velocity_m_s=[min(velocities),max(velocities)],
        calculated_hot_endpoint_K=t_salt,verified_length_increments=62,
        note='Independent arithmetic reproduces the workbook correlation and segmented method; not heat-transfer qualification. Hydraulic calculations retain adopted 18500 kg/s total and UM properties.')

if __name__=='__main__':
    result=read_basis()
    (HERE/'counter-sg-basis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
