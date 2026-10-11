"""Independent SI pressure-wall check against saved Hurmet results; stdlib only."""
from pathlib import Path
import math,re,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'Molten-salt coolant pipe wall - Hurmet.md'
s=p.read_text()
Q=4.619533; S=50e6; P=1e6; y=.4; A=.003; m=.125
minimum=math.sqrt(4*Q/(math.pi*3)); bore=math.ceil(minimum/.025)*.025
# Independently solve the original delivered-wall inequality by bisection.
def required(pressure,stress):
    lo,hi=0.,1.
    for _ in range(80):
        t=(lo+hi)/2
        available=(1-m)*t
        demand=pressure*(bore+2*t)/(2*(stress+pressure*y))+A
        if available<demand:lo=t
        else:hi=t
    return hi
req=required(P,S);t=math.ceil(req/.005)*.005;od=bore+2*t
avail=(1-m)*t; demand=P*od/(2*(S+P*y))+A;net=avail-A
capacity=2*S*net/(od-2*y*net)
e={'MinimumBore':minimum,'Bore':bore,'Velocity':4*Q/(math.pi*bore*bore),'RequiredNominal':req*1000,'NominalWall':t*1000,'Outside':od,'DeliveredMinimum':avail*1000,'RequiredMinimum':demand*1000,'WallMargin':(avail-demand)*1000,'NetPressureWall':net*1000,'PressureCapacity':capacity/1e6}
for name,pressure in [('Half',.5e6),('One',1e6),('Two',2e6)]:e['WallAt'+name+'MPa']=required(pressure,S)*1000
for stress in [30,50,80]:e['WallAtStress'+str(stress)]=required(P,stress*1e6)*1000
e.update(HotInsulatedOutside=od+.8,ColdInsulatedOutside=od+.7,CommonInsulation=400,CommonInsulatedOutside=od+.8)
for name,value in e.items():
    match=re.search(r'¢\?\?` '+name+r' = (?:(?!`).)*?〔([^〕]+)〕',s,re.S)
    assert match,name
    actual=float(match[1].replace(',',''))
    assert math.isclose(value,actual,rel_tol=6e-7,abs_tol=5e-8),(name,value,actual)
flag=re.search(r'¢\?\?` PressureCheck = (?:(?!`).)*?〔([^〕]+)〕',s,re.S)
assert flag and flag[1]=='true' and avail>=demand and capacity>=P
assert len(re.findall(r'¢\?\?`',s))==len(e)+1
# Inverse capacity must close the original wall equation at the fixed selected OD.
assert abs(capacity*od/(2*(S+capacity*y))+A-avail)<1e-12
print(f'{len(e)} numerical cells and one Boolean match independent SI checks.')
for name in ['RequiredNominal','NominalWall','Outside','Velocity','PressureCapacity','WallAtHalfMPa','WallAtOneMPa','WallAtTwoMPa','WallAtStress30']:
 print(name,e[name])
