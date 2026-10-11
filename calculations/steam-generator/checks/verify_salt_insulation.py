"""Independent SI check of saved Hurmet pipe-insulation results (stdlib only)."""
import math
import re
import sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'Molten-salt coolant insulation - Hurmet.md'
text = path.read_text()
sigma = 5.670374419e-8
expected = {}

def heat(D, t, T, Ts, k):
    return 2 * math.pi * k * (T - Ts) / math.log1p(2*t/D)

def surface(D, t, T, k, Ta=313.15, h=4, e=.2):
    # Newton solve in kelvin; independent of the worksheet's bisection.
    Ts = (Ta+T)/2
    conductance = 2*math.pi*k/math.log1p(2*t/D)
    perimeter = math.pi*(D+2*t)
    for _ in range(40):
        residual = conductance*(T-Ts)-perimeter*(h*(Ts-Ta)+e*sigma*(Ts**4-Ta**4))
        slope = -conductance-perimeter*(h+4*e*sigma*Ts**3)
        step = residual/slope
        Ts -= step
        if abs(step)<1e-11:
            break
    assert Ta < Ts < T
    assert abs(heat(D,t,T,Ts,k)-perimeter*(h*(Ts-Ta)+e*sigma*(Ts**4-Ta**4))) < 1e-7
    return Ts

def minimum(D,T,k):
    # Newton solve thickness at 333.15 K surface, starting beyond the solution.
    t = .5
    flux = 4*20+.2*sigma*(333.15**4-313.15**4)
    for _ in range(40):
        log = math.log1p(2*t/D)
        residual = 2*k*(T-333.15)/log-(D+2*t)*flux
        slope = -4*k*(T-333.15)/((D+2*t)*log**2)-2*flux
        step=residual/slope
        t=max(.001,t-step)
        if abs(step)<1e-12:
            break
    return t

for tag,T in [('Hot',875),('Cold',810)]:
    expected[tag+'Minimum']=minimum(1.5,T,.09)*1000
    t=math.ceil(expected[tag+'Minimum']/50)*.05
    expected[tag+'Thickness']=t*1000
    expected[tag+'Jacket']=1.5+2*t
    Ts=surface(1.5,t,T,.09)
    expected[tag+'Surface']=Ts-273.15
    expected[tag+'Loss']=heat(1.5,t,T,Ts,.09)
    expected[tag+'SmallODMinimum']=minimum(1.4,T,.09)*1000
    for name,Ta,h,e,Tp in [('WarmRoom',323.15,4,.2,T),('QuietAir',313.15,2,.2,T),('ShinyJacket',313.15,4,.1,T),('WarmerSalt',313.15,4,.2,T+25),('Combined',323.15,2,.1,T)]:
        expected[tag+name+'Surface']=surface(1.5,t,Tp,.09,Ta,h,e)-273.15
expected['CommonThickness']=max(expected['HotThickness'],expected['ColdThickness'])
t=expected['CommonThickness']/1000
expected['CommonJacket']=1.5+2*t
Ts=surface(1.5,t,810,.09)
expected['CommonColdSurface']=Ts-273.15
expected['CommonColdLoss']=heat(1.5,t,810,Ts,.09)
expected['HotRoomHeat']=45*expected['HotLoss']/1000
expected['ColdRoomHeat']=45*expected['ColdLoss']/1000
expected['TotalRoomHeat']=expected['HotRoomHeat']+expected['ColdRoomHeat']
expected['CommonRoomHeat']=45*(expected['HotLoss']+expected['CommonColdLoss'])/1000
for name,value in expected.items():
    match=re.search(r'¢\?\?` '+name+r' = (?:(?!`).)*?〔([^〕]+)〕',text,re.S)
    assert match,name
    actual=float(match[1].replace(',',''))
    assert math.isclose(value,actual,rel_tol=6e-7,abs_tol=5e-8),(name,value,actual)
assert len(re.findall(r'¢\?\?`',text))==len(expected)
print(f'All {len(expected)} saved results match independent Newton solves and heat-balance checks.')
for name,value in expected.items():
    print(name,round(value,5))
