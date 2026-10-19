"""Couple imported Brayton surplus to the existing salt hydraulic correlation.

Stdlib only. Publishes independently recalculable hydraulic checks in Hurmet;
flow roots are explicitly imported, not claimed to be solved inside Hurmet.
"""
from pathlib import Path
import hashlib,json,math,re
D=Path(__file__).resolve().parent
ROOT=D.parent.parent
R=json.loads((D/'brayton-cooler-results.json').read_text())
T=842.5
rho=2112.68-.5635*T
cp=(1.43788-.0005*T)*1000
mu=.00070645*math.exp(1204.1/T)
N=12090; diameter=.014; length=19.8790057; roughness=1e-6
area=N*math.pi*diameter**2/4
loop_factor=1.5; gen_eta=.95; motor_eta=.96; pump_eta=.80
salt_drop=65; duty=10e6

def hydraulics(flow,allowance=loop_factor):
    speed=flow/area
    reynolds=rho*speed*diameter/mu
    friction=(8/6.0516)/math.log(roughness/diameter+(7/reynolds)**.9)**2
    sg_dp=friction*length/diameter*.5*rho*speed**2
    return dict(volume_m3_s=flow,mass_kg_s=flow*rho,velocity_m_s=speed,
                reynolds=reynolds,friction=friction,sg_drop_Pa=sg_dp,
                loop_drop_Pa=allowance*sg_dp,hydraulic_W=flow*allowance*sg_dp)

def solve(cycle,heat=duty,eta=pump_eta,allowance=loop_factor):
    scale=heat/cycle['inputs']['heat_input_W']
    shaft=cycle['after_illustrative_fan_W']*scale
    electric=shaft*gen_eta
    pump_shaft=electric*motor_eta
    target=pump_shaft*eta
    if target<=0: raise ValueError('No positive power available for salt circulation')
    lo,hi=1e-8,10.
    while hydraulics(hi,allowance)['hydraulic_W']<target: hi*=2
    for _ in range(90):
        mid=(lo+hi)/2
        if hydraulics(mid,allowance)['hydraulic_W']<target:lo=mid
        else:hi=mid
    out=hydraulics((lo+hi)/2,allowance)
    # The inherited turbulent correlation is not extrapolated as a reported result.
    if out['reynolds']<4000:raise ValueError('Reported flow requires a low-Re correlation')
    assert abs(out['hydraulic_W']/target-1)<1e-10
    out.update(heat_into_brayton_W=heat,after_fan_shaft_W=shaft,electric_W=electric,
               pump_shaft_W=pump_shaft,pump_efficiency=eta,
               heat_transport_at_65K_W=out['mass_kg_s']*cp*salt_drop,
               salt_drop_for_gross_heat_K=heat/(out['mass_kg_s']*cp),
               net_reactor_heat_min_W=heat-pump_shaft,
               net_reactor_heat_max_W=heat-out['hydraulic_W'])
    return out

reference=hydraulics(500e6/(rho*cp*salt_drop))
assert abs(reference['sg_drop_Pa']/190872.791-1)<1e-7
results={k:solve(R[k]) for k in ['base','high_ratio']}
# Three independent, equal legs sharing a single 10 MW trial's total surplus.
shared={k:solve(R[k],heat=duty/3) for k in results}
sensitivity={k:{'pump_efficiency_60_percent':solve(R[k],eta=.6),
                'loop_allowance_100_percent':solve(R[k],allowance=2.)} for k in results}
checks={};lines=[]
def add(s):lines.append(s)
def inp(n,v,u=''):add(f'¢` {n} = {v:.14g} {u} `')
def calc(n,e,v,u=''):add(f'¢` {n} = {e} = ?? {u} `');checks[n]=v
add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-12
---------------

# Brayton-driven salt pony pump — preliminary estimate

12 October 2026. Use the [steam-generator hydraulic worksheet](../steam-generator/Generator%20sizing%20-%20Hurmet.md), with the owner's **50% additional pressure-drop allowance for the entire salt loop**, to estimate circulation powered by the [Brayton trial](Steam%20Brayton%20cooler%20-%20Hurmet.md). This is a power-balance estimate; it does not select a pump or demonstrate a reactor cooling system.

The principal comparison is **one salt leg through one generator, with 10 MW transferred from salt into its auxiliary Brayton loop**. The heat input is a normalization, not a specified decay-heat requirement. Three such independent sets would transfer 30 MW gross in total. A separate shared-power case below instead keeps the entire installation at 10 MW.

## Assumptions and calculation method

The current generator basis uses salt at 875/810 K, a 65 K drop, and properties at 842.5 K. It contains 12,090 parallel salt tubes, 14 mm bore, 19.879 m hydraulic length and 0.001 mm roughness. The later 17 m visual casing height has not revised that hydraulic length. At 500 MW per leg this reproduces 4.6195 m³/s and 190.873 kPa across the generator, or 286.309 kPa including the additional loop allowance.

Pressure loss is recalculated at the reduced flow with the **original worksheet's friction correlation**, including its Reynolds-number dependence. Holding the full-flow head constant would substantially underpredict circulation. A closed circulation loop has no net geometric lift; this estimate neglects buoyancy assistance. The 50% allowance remains a lumped assumption for reactor, piping, valves and the installed pump path. See the [DOE pumping-system sourcebook](https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf) for the distinction between friction and static head.

The Brayton turbine already powers its compressor and includes its shaft-transfer loss. Retain the preceding illustrative air fan as a **shaft-power deduction**, then convert the remaining power to electricity at an assumed 95% alternator efficiency. The pony-pump motor is 96% efficient and the pump is 80% efficient. These are provisional efficiencies for appropriately selected machinery; no actual pump, motor or drive curve has been applied. An electric fan, variable-frequency drive, controls, heat tracing or other consumers would require extra deductions.

Python solves `flow × loop_pressure_drop(flow) = remaining_shaft_power × generator_efficiency × motor_efficiency × pump_efficiency`. The flow roots and Brayton power fractions are imported below. Hurmet independently recalculates friction, power closure, heat transport and temperature change. **After changing a physical input, rerun `brayton_salt_pump.py` and the checker to solve new roots**; changing the inputs in Hurmet alone does not update the imported flow roots. Real-steam cycle state changes require rerunning `brayton_cooler.py` first.

## Common inputs''')
for n,v,u in [('Density',rho,'kg/m3'),('HeatCapacity',cp,'J.kg-1.K-1'),('Viscosity',mu,'kg.m-1.s-1'),('TubeCount',N,''),('TubeDiameter',diameter,'m'),('TubeLength',length,'m'),('Roughness',roughness,'m'),('LoopFactor',loop_factor,''),('GeneratorEfficiency',gen_eta,''),('MotorEfficiency',motor_eta,''),('PumpEfficiency',pump_eta,''),('HeatDuty',10,'MW'),('ReferenceSaltDrop',salt_drop,'K')]:inp(n,v,u)
calc('FlowArea','TubeCount * π * TubeDiameter^2 / 4',area,'m2')
calc('ReferenceFlow',"500 'MW' / (Density * HeatCapacity * ReferenceSaltDrop)",reference['volume_m3_s'],'m3/s')
add('## Main comparison: all available surplus used for circulation')
add('| Quantity, per 10 MW trial | 2:1 steam cycle | 8:1 steam cycle |\n| --- | --- | --- |')
rows=[('Shaft surplus after fan, kW','after_fan_shaft_W',.001),('Pony-pump electricity, kW','electric_W',.001),('Salt flow, m³/s','volume_m3_s',1),('Salt mass flow, kg/s','mass_kg_s',1),('Whole-loop pressure drop, kPa','loop_drop_Pa',.001),('Salt tube Reynolds number','reynolds',1),('Heat transport if salt drops 65 K, MW','heat_transport_at_65K_W',1e-6),('Actual gross heat into the trial, MW','heat_into_brayton_W',1e-6),('Salt drop for that 10 MW, K','salt_drop_for_gross_heat_K',1)]
for label,key,factor in rows:add(f'| {label} | {results["base"][key]*factor:,.4g} | {results["high_ratio"][key]*factor:,.4g} |')
add('''**The 226 MW and 444 MW figures describe heat carried by the calculated salt flow at a hypothetical 65 K drop. They are not the heat-removal ratings of the 10 MW Brayton units.** Removing that much heat would require correspondingly larger steam flow, machinery and air coolers, and another coupled thermal/hydraulic analysis. The base 10 MW trial instead gives about 2.88 K salt cooling at maximum surplus-powered flow; the vacuum 8:1 trial gives about 1.47 K. These small drops also mean the salt properties near the hot end differ somewhat from the inherited mean; frozen mean properties are retained for this first screen.

For an actual 10 MW requirement, circulation need not consume all surplus. A smaller pump or suitable speed control can trade salt temperature drop against flow and preserve power for other loads. Very low flow would require a laminar/transition correlation and a new heat-transfer analysis; the original turbulent expression is not used to claim performance there.''')
for key,prefix in [('base','Two'),('high_ratio','Eight')]:
    a=results[key];c=R[key]
    add(f'## Recalculated checks: {c["inputs"]["compressor_ratio"]}:1 case')
    inp(prefix+'ShaftFraction',c['after_illustrative_fan_W']/c['inputs']['heat_input_W'])
    inp(prefix+'Flow',a['volume_m3_s'],'m3/s')
    calc(prefix+'Electrical',f'HeatDuty * {prefix}ShaftFraction * GeneratorEfficiency',a['electric_W']/1000,'kW')
    calc(prefix+'PumpShaft',f'{prefix}Electrical * MotorEfficiency',a['pump_shaft_W']/1000,'kW')
    calc(prefix+'HydraulicAvailable',f'{prefix}PumpShaft * PumpEfficiency',a['hydraulic_W']/1000,'kW')
    calc(prefix+'Velocity',f'{prefix}Flow / FlowArea',a['velocity_m_s'],'m/s')
    calc(prefix+'Reynolds',f'Density * {prefix}Velocity * TubeDiameter / Viscosity',a['reynolds'])
    calc(prefix+'Friction',f'(8/6.0516) * ln(Roughness/TubeDiameter + (7/{prefix}Reynolds)^0.9)^(-2)',a['friction'])
    calc(prefix+'GeneratorDrop',f'{prefix}Friction * TubeLength / TubeDiameter * Density * {prefix}Velocity^2 / 2',a['sg_drop_Pa']/1000,'kPa')
    calc(prefix+'LoopDrop',f'LoopFactor * {prefix}GeneratorDrop',a['loop_drop_Pa']/1000,'kPa')
    calc(prefix+'HydraulicRequired',f'{prefix}Flow * {prefix}LoopDrop',a['hydraulic_W']/1000,'kW')
    calc(prefix+'PowerClosure',f'{prefix}HydraulicRequired / {prefix}HydraulicAvailable',1.)
    calc(prefix+'MassFlow',f'Density * {prefix}Flow',a['mass_kg_s'],'kg/s')
    calc(prefix+'Transport65K',f'{prefix}MassFlow * HeatCapacity * ReferenceSaltDrop',a['heat_transport_at_65K_W']/1e6,'MW')
    calc(prefix+'SaltDrop',f'HeatDuty / ({prefix}MassFlow * HeatCapacity)',a['salt_drop_for_gross_heat_K'],'K')
    calc(prefix+'NetMinimum',f'HeatDuty - {prefix}PumpShaft',a['net_reactor_heat_min_W']/1e6,'MW')
    calc(prefix+'NetMaximum',f'HeatDuty - {prefix}HydraulicRequired',a['net_reactor_heat_max_W']/1e6,'MW')
add('''## Heat returned by the salt pump

Hydraulic power ultimately dissipates as heat within the salt loop. Depending on pump construction, some or all of the remaining pump-shaft loss may also enter the salt. Assuming motor, alternator and fan losses are outside the salt, a gross 10 MW transfer into the Brayton unit leaves approximately **9.81–9.85 MW net reactor heat removal for 2:1**, and **8.81–9.05 MW for 8:1**, if all available surplus drives the pump. These are pump-loss bounds, not uncertainty bounds on the complete system. The air cooler's separate duties remain 9.663 and 8.445 MW; the rest of the cycle heat appears as work and equipment losses. Reducing unnecessary pumping would reduce heat returned to the salt.

## Three legs sharing one 10 MW auxiliary heat duty

For a comparison with only 10 MW total across the plant, divide its surplus equally among three independently modeled legs/pumps. Each leg receives one third of the power and transfers one third of the heat. Recompute each flow, rather than simply dividing the single-leg flow by three. Actual common-reactor losses and distribution require a network calculation.''')
add('| Quantity | 2:1 steam cycle | 8:1 steam cycle |\n| --- | --- | --- |')
for label,values in [('Flow per leg, m³/s',[shared[k]['volume_m3_s'] for k in results]),('Total salt flow, m³/s',[3*shared[k]['volume_m3_s'] for k in results]),('Salt temperature drop, K',[shared[k]['salt_drop_for_gross_heat_K'] for k in results])]:add(f'| {label} | {values[0]:.4g} | {values[1]:.4g} |')
add('## Sensitivity and limits')
add('| Single-leg 10 MW case | 2:1 salt flow, m³/s | 8:1 salt flow, m³/s |\n| --- | --- | --- |')
for label,k in [('Pump efficiency 60% instead of 80%','pump_efficiency_60_percent'),('Loop loss 2.0 × generator instead of 1.5 ×','loop_allowance_100_percent')]:add(f'| {label} | {sensitivity["base"][k]["volume_m3_s"]:.4g} | {sensitivity["high_ratio"][k]["volume_m3_s"]:.4g} |')
add('''All reported flow solutions remain above Reynolds number 4,000. The approximately 50% additional loss is assumed to scale with generator loss; it is not a separately modeled reactor resistance. No stopped-main-pump resistance, check-valve cracking head, pony-pump branch sizing, NPSH, thermal stratification, bypass distribution or natural-circulation credit has been resolved.

Salt-pumping power appears affordable **if the positive Brayton surplus is achieved**. The preceding cycle study shows that lower compressor/turbine efficiencies or greater steam-side pressure losses can eliminate the 2:1 surplus. The 8:1 trial still requires about 521 m³/s compressor-inlet steam volume per 10 MW, versus 7.19 m³/s for 2:1; its stronger pump margin does not make that vacuum machinery small. Maintaining the assumed 830 K turbine inlet at reduced heat duty also requires a generator heat-transfer and control check. Startup power, actual heat demand, freeze protection and heat-rejection performance remain unresolved.

## Reproduction and checks

Run `python brayton_salt_pump.py`, then `node check_brayton_salt_pump.cjs` with `HURMET_ENGINE` and `TEMML_ENGINE` pointing to the existing Hurmet/Temml bundles. The Python program uses only the standard library; its Brayton inputs come from `brayton-cooler-results.json`. It verifies the inherited full-flow pressure drop, positive turbulent flow roots and power balance. The checker recalculates and saves/reopens the Hurmet document, compares all named results with Python and verifies that changes to loop allowance and pump efficiency break the imported-root power balance as expected. This prevents silently treating the imported flow as a live Hurmet root solve. Source hashes, detailed results and expected checks are stored in `brayton-salt-pump-results.json`.''')
text='\n\n'.join(lines)+'\n'
text=re.sub(r'(?m)(^\|.*\|)\n\n(?=\|)',r'\1\n',text)
def widths(match):
    block=match.group(0);n=block.splitlines()[0].count('|')-1
    return block+'\n{.grid colWidths="'+' '.join(['250']+['135']*(n-1))+'"}'
text=re.sub(r'(?m)^\|.*(?:\n\|.*)*',widths,text)
(D/'Brayton-driven salt pump - Hurmet.md').write_text(text)
sources=[D/'brayton_salt_pump.py',D/'brayton-cooler-results.json',ROOT/'calculations/steam-generator/Generator sizing - Hurmet.md']
output=dict(date='2026-10-12',basis='Per leg; 10 MW gross salt-to-Brayton duty; frozen 842.5 K properties',
            source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            reference=reference,cases=results,shared_10MW_three_legs=shared,sensitivity=sensitivity,hurmet_checks=checks)
(D/'brayton-salt-pump-results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'cases':results,'shared_flows':{k:v['volume_m3_s'] for k,v in shared.items()},'checks':len(checks)},indent=2))
