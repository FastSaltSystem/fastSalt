"""Independent SI check of saved Hurmet pipe-insulation results (stdlib only)."""
import math
import re
import sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'Steam and feedwater insulation - Hurmet.md'
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

cases=[('SB','Steam',.655,830,873.15,.09),('SH','Steam',1.115,830,873.15,.09),('WB','Water',.525,560,598.15,.075),('WH','Water',.89,560,598.15,.075)]
for tag,service,D,oper,check,k in cases:
    for name,T in [('Operating',oper),('Check',check)]:
        expected[tag+name+'Minimum']=minimum(D,T,k)*1000
for service,prefix in [('Steam','S'),('Water','W')]:
    expected[service+'Thickness']=math.ceil(max(expected[prefix+'BCheckMinimum'],expected[prefix+'HCheckMinimum'])/25)*25
for tag,service,D,oper,check,k in cases:
    t=expected[service+'Thickness']/1000
    expected[tag+'Jacket']=(D+2*t)*1000
    for name,T in [('Operating',oper),('Check',check)]:
        Ts=surface(D,t,T,k)
        expected[tag+name+'Surface']=Ts-273.15
        expected[tag+name+'Loss']=heat(D,t,T,Ts,k)
    if tag.endswith('H'):
        for name,Ta,h,e in [('WarmRoom',323.15,4,.2),('QuietAir',313.15,2,.2),('ShinyJacket',313.15,4,.1),('Combined',323.15,2,.1)]:
            expected[tag+name+'Surface']=surface(D,t,check,k,Ta,h,e)-273.15
expected['SteamRoomHeat']=(45*expected['SBOperatingLoss']+90*expected['SHOperatingLoss'])/1000
expected['WaterRoomHeat']=(45*expected['WBOperatingLoss']+90*expected['WHOperatingLoss'])/1000
expected['TotalRoomHeat']=expected['SteamRoomHeat']+expected['WaterRoomHeat']
for name,value in expected.items():
    match=re.search(r'¢\?\?` '+name+r' = (?:(?!`).)*?〔([^〕]+)〕',text,re.S)
    assert match, name
    actual=float(match[1].replace(',',''))
    assert math.isclose(value,actual,rel_tol=6e-7,abs_tol=5e-8),(name,value,actual)
assert len(re.findall(r'¢\?\?`',text))==len(expected)
print(f'All {len(expected)} saved results agree with independent SI Newton solves.')
for tag,*_ in cases:
    print(tag, {key:round(expected[tag+key],3) for key in ['Jacket','OperatingSurface','CheckSurface','OperatingLoss']})
print('Room heat kW:', expected['TotalRoomHeat'])
print('Sensitivities:', {n:round(v,2) for n,v in expected.items() if any(x in n for x in ['WarmRoom','QuietAir','ShinyJacket','Combined'])})
