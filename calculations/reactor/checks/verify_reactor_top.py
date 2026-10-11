"""Independent SI Newton solution; checks all saved Hurmet results. Stdlib only."""
from pathlib import Path
import math,re,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'Reactor top insulation - Hurmet.md'
s=p.read_text()
k=.085;sig=5.670374419e-8;Th=875.;Ta=313.15;limit=333.15;h=4.;e=.2

def surface(t,th=Th,ta=Ta,h=h,e=e):
    ts=ta+20
    for _ in range(30):
        residual=k*(th-ts)/t-h*(ts-ta)-e*sig*(ts**4-ta**4)
        derivative=-k/t-h-4*e*sig*ts**3
        ts-=residual/derivative
    assert abs(k*(th-ts)/t-h*(ts-ta)-e*sig*(ts**4-ta**4))<1e-8
    return ts

def minimum(th=Th,ta=Ta,h=h,e=e):
    return k*(th-limit)/(h*(limit-ta)+e*sig*(limit**4-ta**4))

mn=minimum(); rounded=math.ceil(mn/.05)*.05; selected=rounded+.05;ts=surface(selected)
flux=k*(Th-ts)/selected;area=math.pi*4.121639668346854**2
expected=dict(TargetFlux=h*(limit-Ta)+e*sig*(limit**4-Ta**4),MinimumThickness=mn*1000,RoundedMinimum=rounded*1000,SelectedThickness=selected*1000,SelectedSurface=ts-273.15,SelectedFlux=flux)
for mm in [120,300,400,450,600]:
    x=surface(mm/1000)
    expected['Surface'+str(mm)]=x-273.15
    expected['Flux'+str(mm)]=k*(Th-x)/(mm/1000)
expected.update(CoverDiameter=2*4.121639668346854,CoverArea=area,TopHeat=flux*area/1000,InsulationVolume=area*selected,InsulationMass=area*selected*240,ArealMass=selected*240)
for name,th,ta,h,e in [('WarmRoom',875,323.15,4,.2),('QuietAir',875,313.15,2,.2),('ShinyJacket',875,313.15,4,.1),('WarmerSalt',898.15,313.15,4,.2),('Combined',875,323.15,2,.1)]:
    expected[name+'Surface']=surface(selected,th,ta,h,e)-273.15
    expected[name+'Minimum']=minimum(th,ta,h,e)*1000
for name,value in expected.items():
    match=re.search(r'¢\?\?` '+name+r' = (?:(?!`).)*?〔([^〕]+)〕',s,re.S)
    assert match,name
    actual=float(match[1].replace(',',''))
    assert math.isclose(value,actual,rel_tol=6e-7,abs_tol=5e-8),(name,value,actual)
assert len(re.findall(r'¢\?\?`',s))==len(expected)
print(f'All {len(expected)} numerical results agree with independent SI calculations.')
