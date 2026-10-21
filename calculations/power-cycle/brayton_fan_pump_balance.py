"""Size fan/pump demands against scalable Brayton surplus; not an equipment map."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json,math,re,hashlib
D=Path(__file__).resolve().parent
R=json.loads((D/'brayton-cooler-results.json').read_text())
rho=1637.93125;cp=1016.63;mu=.00070645*math.exp(1204.1/842.5)
d=.014;L=19.8790057;A=12090*math.pi*d*d/4
rho_air=101325/(287.05*303.15)
eta_g=.95;eta_m=.96;eta_p=.8;eta_f=.65;cp_air=1007

def solve(key,Q,dt=10,dp_air=500,air_rise=100):
 b=R[key];scale=Q/b['inputs']['heat_input_W']
 q=Q/(rho*cp*dt);v=q/A;Re=rho*v*d/mu
 f=(8/6.0516)/math.log(1e-6/d+(7/Re)**.9)**2
 dp=1.5*f*L/d*.5*rho*v*v
 hydraulic=q*dp;shaft=hydraulic/eta_p;pump=shaft/eta_m
 reject=b['heat_rejected_air_cooler_W']*scale
 air_mass=reject/(cp_air*air_rise);air_volume=air_mass/rho_air
 fan=air_volume*dp_air/(eta_f*eta_m)
 electric=b['available_shaft_W']*scale*eta_g
 return dict(cycle=key,heat_W=Q,salt_drop_K=dt,salt_flow_m3_s=q,salt_Re=Re,salt_loop_drop_Pa=dp,
  pump_hydraulic_W=hydraulic,pump_shaft_W=shaft,pump_electric_W=pump,
  air_cooler_W=reject,air_rise_K=air_rise,air_drop_Pa=dp_air,air_mass_kg_s=air_mass,
  air_volume_m3_s=air_volume,fan_electric_W=fan,available_electric_W=electric,
  remaining_electric_W=electric-pump-fan,net_reactor_min_W=Q-shaft,net_reactor_max_W=Q-hydraulic,
  cooler_face_at_3ms_m2=air_volume/3,
  steam_mass_kg_s=b['steam_flow_kg_s']*scale,steam_inlet_volume_m3_s=b['compressor_inlet_volume_m3_s']*scale)

cases=[solve('base',30e6),solve('base',50e6),solve('high_ratio',30e6)]
for c in cases:
 assert c['salt_Re']>4000
 assert abs(c['available_electric_W']-c['fan_electric_W']-c['pump_electric_W']-c['remaining_electric_W'])<1e-6
 assert c['remaining_electric_W']>0
lo,hi=30e6,100e6
for _ in range(90):
 mid=(lo+hi)/2
 if solve('base',mid)['remaining_electric_W']>0:lo=mid
 else:hi=mid
balance=solve('base',(lo+hi)/2)
assert abs(balance['remaining_electric_W'])<1e-6
sensitivity=[solve('base',30e6,dp_air=1000),solve('base',30e6,air_rise=50),solve('base',30e6,dp_air=1000,air_rise=50)]
fullflow=solve('base',500e6,dt=65)
assert abs(fullflow['salt_loop_drop_Pa']/286309.1865-1)<1e-7
assert fullflow['remaining_electric_W']>0
checks={};lines=[]
def add(s):lines.append(s)
def inp(n,v,u=''):add(f'¢` {n} = {v:.14g} {u} `')
def calc(n,e,v,u=''):add(f'¢` {n} = {e} = ?? {u} `');checks[n]=v
add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-13
---------------

# Steam Brayton cooler — balanced fan and salt-pump demand

**[Overview of steam, nitrogen, open-air and supercritical CO₂ alternatives](brayton-overview.md)** — common 30 MW comparison and links to all studies.

13 October 2026. Preliminary follow-up to the [cycle trial](Steam%20Brayton%20cooler%20-%20Hurmet.md) and [salt-pump estimate](Brayton-driven%20salt%20pump%20-%20Hurmet.md). Estimate heat duties whose compressor, air-cooler fan and salt pump can be powered together. No machinery or heat-exchanger rating is established by this power balance.

The prior salt-pump estimate already reserved fan shaft power. Here both fan and salt pump are electric: convert the cycle's **surplus before fan deduction** through a 95% alternator, then supply both motors at 96% efficiency. Pump hydraulic efficiency is 80%; fan efficiency is 65%. This avoids subtracting the fan twice. The compressor and cycle shaft losses remain included upstream.

## Trial choices

Use one existing salt leg and one generator. Retain the current generator hydraulic geometry, salt properties and original turbulent friction correlation, with total loop drop equal to 1.5 times generator drop. Choose a **10 K salt temperature drop** for the 30 and 50 MW trial duties. This is an editable circulation target, not a revised reactor operating temperature or a necessary optimum. At a nominal 875 K salt inlet it implies about 865 K outlet; properties are frozen at the earlier 842.5 K reference for comparability and should be updated in detailed work.

Ambient air is 30°C and leaves the cooler at 130°C; use 500 Pa total air-system loss, 1,007 J/(kg K) heat capacity and inlet density at 1 atmosphere. Assume a forced-draft fan at the cool inlet. Pressure drop includes the cooler and ductwork allowance. A fan after the hot exchanger would need a density correction. These air-side parameters are assumptions, not a vendor selection. The [DOE fan-system sourcebook](https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/fan_sourcebook.pdf) describes the importance of pressure losses and matching fans to the complete system.

Each heat-duty case scales steam flow and Brayton machinery to that duty while retaining the prior cycle states and efficiencies. A 30 MW case produces three times the 10 MW trial's surplus; it is **not the same 10 MW machine producing 30 MW cooling**. Similarly, holding 500 Pa air loss as duty increases assumes a correspondingly larger cooler/airflow area, not simply speeding up the same fan and exchanger. Steam-side 2% exchanger losses remain assumed and require verification against the existing generator's passages, especially for the vacuum 8:1 trial.

## Results per leg''')
add('| Quantity | 2:1, 30 MW | 2:1, 50 MW | 8:1, 30 MW |\n| --- | --- | --- | --- |')
for label,k,s in [('Available electricity after compressor, kW','available_electric_W',.001),('Salt flow, m³/s','salt_flow_m3_s',1),('Salt loop drop, kPa','salt_loop_drop_Pa',.001),('Pump electricity, kW','pump_electric_W',.001),('Fan electricity, kW','fan_electric_W',.001),('Electrical margin, kW','remaining_electric_W',.001),('Air-cooler heat rejection, MW','air_cooler_W',1e-6),('Airflow at cool inlet, m³/s','air_volume_m3_s',1),('Minimum net reactor cooling with pump losses, MW','net_reactor_min_W',1e-6),('Compressor-inlet steam volume, m³/s','steam_inlet_volume_m3_s',1)]:add('| '+label+' | '+' | '.join(f'{c[k]*s:,.4g}' for c in cases)+' |')
add('''At 30 MW and 2:1, the actual fan/pump demand splits approximately **60% to the fan and 40% to the salt pump**, using only about 43% of available electricity. The remaining 57% is unallocated margin for other consumers or export; no allowance has yet been assigned to controls, heat tracing, drive electronics or other station services.

Gross salt-to-cycle heat is distinguished from net heat removed from the reactor. Hydraulic work returns to the salt as heat; for the lower net estimate assume all pump shaft work ultimately enters the salt. Alternator and motor losses are assumed outside the salt. A 30 MW set then removes about **29.88–29.90 MW net** from the reactor. Three independent sets give 90 MW gross and approximately **89.63–89.70 MW net**, contingent on the same per-leg hydraulic assumption; the common reactor flow network is not modeled.

The dedicated air cooler rejects less than the heat entering the cycle because some becomes work. Ultimately residual electricity and equipment losses also need destinations; rejecting them locally adds to site heat rejection, not to the specified steam-to-air exchanger duty.

## How far can the power balance extend?

For the chosen 10 K salt drop and the base 2:1 cycle, the model's zero-reserve electrical balance occurs at about **69.6 MW per leg**. Pump demand rises much faster than heat duty, while fan demand and cycle surplus scale linearly only because cooler and machinery sizes are being scaled. This is a mathematical boundary with no auxiliary reserve, not a recommended operating point or a demonstrated capacity. At 50 MW it still leaves about 412 kW electrical margin.

There is no unique maximum cooling duty from surplus power alone. With the original 65 K salt drop, even the 500 MW design-duty salt flow remains below the extrapolated available-power budget. That does not establish 500 MW auxiliary-cooler feasibility; it means the power balance is no longer the useful sizing constraint. Exchanger thermal performance, steam passage pressure loss, compressor/turbine size, air-system size and operating temperatures must define the equipment limit.

## Air-cooler scale and sensitivity

At 30 MW with the 2:1 cycle, the steam-to-air exchanger rejects 28.99 MW using about 247 m³/s of inlet air. If a provisional 3 m/s superficial face velocity is selected, the required frontal area is about **82 m²**. At 50 MW it is about **137 m²**. These are airflow face areas, not fin surface areas or complete installed footprints. Multiple fan bays could provide this area. No heat-transfer coefficient, fin geometry or core depth has been selected; the assumed 500 Pa loss and the required thermal surface must be achieved together.

The 8:1 case has ample power in this idealized scaling but requires about **1,564 m³/s compressor-inlet steam volume at 30 MW**. Its cold-end steam temperature is only about 44.8°C against 30°C inlet air, so the close temperature approach also makes heat-exchanger performance consequential. This does not support calling that machinery small.''')
add('| 30 MW, 2:1 air-side assumption | Fan electricity, kW | Remaining electricity, kW |\n| --- | --- | --- |')
for label,c in zip(['1,000 Pa, 100 K air rise','500 Pa, 50 K air rise','1,000 Pa, 50 K air rise'],sensitivity):add(f'| {label} | {c["fan_electric_W"]/1000:.1f} | {c["remaining_electric_W"]/1000:.1f} |')
add('The last case has negative margin: it cannot power the fan and pump at the specified operating point. The result therefore depends on obtaining low air-side pressure loss and a suitable air-temperature rise, as well as the preceding cycle efficiency assumptions.')
add('## Hurmet verification of the 30 MW, 2:1 trial')
for n,v,u in [('HeatDuty',30,'MW'),('SaltDrop',10,'K'),('SaltDensity',rho,'kg/m3'),('SaltHeatCapacity',cp,'J.kg-1.K-1'),('SaltViscosity',mu,'kg.m-1.s-1'),('FlowArea',A,'m2'),('TubeDiameter',d,'m'),('TubeLength',L,'m'),('Roughness',1e-6,'m'),('LoopFactor',1.5,''),('GeneratorEfficiency',eta_g,''),('MotorEfficiency',eta_m,''),('PumpEfficiency',eta_p,''),('FanEfficiency',eta_f,''),('AirDensity',rho_air,'kg/m3'),('AirHeatCapacity',cp_air,'J.kg-1.K-1'),('AirRise',100,'K'),('AirPressureDrop',500,'Pa'),('FaceVelocity',3,'m/s'),('SurplusFraction',R['base']['available_shaft_W']/1e7,''),('RejectFraction',R['base']['heat_rejected_air_cooler_W']/1e7,'')]:inp(n,v,u)
c=cases[0]
for n,e,v,u in [('AvailableElectricity','HeatDuty * SurplusFraction * GeneratorEfficiency',c['available_electric_W']/1000,'kW'),('SaltFlow','HeatDuty / (SaltDensity * SaltHeatCapacity * SaltDrop)',c['salt_flow_m3_s'],'m3/s'),('SaltVelocity','SaltFlow / FlowArea',c['salt_flow_m3_s']/A,'m/s'),('SaltReynolds','SaltDensity * SaltVelocity * TubeDiameter / SaltViscosity',c['salt_Re'],''),('Friction','(8/6.0516) * ln(Roughness/TubeDiameter + (7/SaltReynolds)^0.9)^(-2)',(8/6.0516)/math.log(1e-6/d+(7/c['salt_Re'])**.9)**2,''),('LoopDrop','LoopFactor * Friction * TubeLength / TubeDiameter * SaltDensity * SaltVelocity^2 / 2',c['salt_loop_drop_Pa']/1000,'kPa'),('PumpHydraulic','SaltFlow * LoopDrop',c['pump_hydraulic_W']/1000,'kW'),('PumpShaft','PumpHydraulic / PumpEfficiency',c['pump_shaft_W']/1000,'kW'),('PumpElectricity','PumpShaft / MotorEfficiency',c['pump_electric_W']/1000,'kW'),('AirHeat','HeatDuty * RejectFraction',c['air_cooler_W']/1e6,'MW'),('AirMass','AirHeat / (AirHeatCapacity * AirRise)',c['air_mass_kg_s'],'kg/s'),('AirFlow','AirMass / AirDensity',c['air_volume_m3_s'],'m3/s'),('FanElectricity','AirFlow * AirPressureDrop / (FanEfficiency * MotorEfficiency)',c['fan_electric_W']/1000,'kW'),('RemainingElectricity','AvailableElectricity - PumpElectricity - FanElectricity',c['remaining_electric_W']/1000,'kW'),('NetReactorMinimum','HeatDuty - PumpShaft',c['net_reactor_min_W']/1e6,'MW'),('NetReactorMaximum','HeatDuty - PumpHydraulic',c['net_reactor_max_W']/1e6,'MW'),('FaceArea','AirFlow / FaceVelocity',c['cooler_face_at_3ms_m2'],'m2')]:calc(n,e,v,u)
add('''The heat duty, salt drop and air-system inputs recalculate directly in this Hurmet block, provided the resulting salt Reynolds number remains above 4,000. The summary tables and zero-reserve root are Python results and do not change automatically in Hurmet. Real-steam states and efficiencies are imported through the two cycle fractions; rerun the original real-steam solver for altered temperatures, pressures or machine efficiencies.

## Reproduction and limits

Run `python brayton_fan_pump_balance.py`, then `node check_brayton_fan_pump.cjs` using the existing HURMET_ENGINE and TEMML_ENGINE paths. Results and source hashes are in `brayton-fan-pump-results.json`. The checker verifies 17 results after save/reopen and exercises heat duty, air pressure drop and the power-deficit sensitivity. Python verifies the 500 MW hydraulic reference and zero-reserve root.

This is an exploratory energy/hydraulic screen. No assumption of a fixed-size cooler retaining constant pressure loss at arbitrary airflow is made. Heat-transfer capability of the generator and air cooler, operating maps, pressure losses, local salt freezing, stopped-main-pump resistance, startup and decay-heat requirements remain unresolved. The positive 2:1 balance can disappear with the less favorable machine efficiencies already tested in the preceding cycle study. No reactor-building geometry or adopted cooling design is changed.''')
s='\n\n'.join(lines)+'\n';s=re.sub(r'(?m)(^\|.*\|)\n\n(?=\|)',r'\1\n',s)
def widths(m):
 b=m.group(0);n=b.splitlines()[0].count('|')-1
 return b+'\n{.grid colWidths="'+' '.join(['250']+['125']*(n-1))+'"}'
s=re.sub(r'(?m)^\|.*(?:\n\|.*)*',widths,s)
write_worksheet(D/'Brayton fan and salt pump balance - Hurmet.md', s)
paths=[D/'brayton_fan_pump_balance.py',D/'brayton-cooler-results.json',D.parent/'steam-generator/Generator sizing - Hurmet.md']
out=dict(date='2026-10-13',cases=cases,zero_margin_10K=balance,sensitivity=sensitivity,design_flow_65K=fullflow,hurmet_checks=checks,source_hashes={str(p.relative_to(D.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
(D/'brayton-fan-pump-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'cases':cases,'zero_margin_MW':balance['heat_W']/1e6,'checks':len(checks)},indent=2))
