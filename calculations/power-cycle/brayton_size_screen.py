"""Flow-based sizes and explicitly provisional layout reservations, 30 MW per train."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json,math,re,hashlib
D=Path(__file__).resolve().parent
s=json.loads((D/'brayton-cooler-results.json').read_text())
n=json.loads((D/'nitrogen-brayton-results.json').read_text())
a=json.loads((D/'open-air-brayton-results.json').read_text())['matched']
fan=json.loads((D/'brayton-fan-pump-results.json').read_text())
flow_speed=30.;duct_speed=15.;face_speed=3.;scale=3.
def diameter(q,v):return math.sqrt(4*q/(math.pi*v))
cases={}
for key,label in [('steam','Closed steam, 2:1'),('nitrogen','Closed nitrogen, 4:1'),('air','Open air, matched 6.83:1')]:
 if key=='steam':
  b=s['base'];m=b['steam_flow_kg_s']*scale;vin=b['compressor_inlet_volume_m3_s']*scale;vhot=m/b['states']['air_cooler_inlet']['density_kg_m3'];pc=b['compressor_power_W']*scale;pt=b['turbine_power_W']*scale
  cooling=fan['cases'][0]['air_volume_m3_s'];UA=n['cases']['steam_two']['required_counterflow_UA_W_K']*scale
 elif key=='nitrogen':
  b=n['cases']['nitrogen_four'];m=b['mass_kg_s']*scale;vin=b['inlet_volume_m3_s']*scale;vhot=m/b['states']['cooler_inlet']['density_kg_m3'];pc=b['compressor_W']*scale;pt=b['turbine_W']*scale
  cooling=b['air_heat_W']*scale/(1007*100)/(101325/(287.05*303.15));UA=b['required_counterflow_UA_W_K']*scale
 else:
  m=a['mass_kg_s']*scale;vin=a['inlet_volume_m3_s']*scale;vhot=a['exhaust_volume_m3_s']*scale;pc=a['compressor_W']*scale;pt=a['turbine_W']*scale;cooling=0;UA=0
 cases[key]=dict(label=label,heat_W=30e6,mass_kg_s=m,inlet_volume_m3_s=vin,hot_low_pressure_volume_m3_s=vhot,compressor_W=pc,turbine_W=pt,
  inlet_equivalent_bore_m=diameter(vin,duct_speed if key=='air' else flow_speed),hot_equivalent_bore_m=diameter(vhot,duct_speed if key=='air' else flow_speed),
  cooler_air_m3_s=cooling,cooler_minimum_face_m2=cooling/face_speed,cooler_counterflow_UA_W_K=UA)
# Deliberately chosen reservations, not outputs of a machine/exchanger sizing method.
res={'steam':dict(machine_m=[15,6,5],cooler_m=[12,10,6],plot_m=[28,18]),
     'nitrogen':dict(machine_m=[15,6,5],cooler_m=[16,10,7],plot_m=[30,20]),
     'air':dict(machine_m=[22,7,5.5],cooler_m=None,plot_m=[32,16])}
for k in cases:
 cases[k]['provisional_reservations']=res[k]
 if res[k]['cooler_m']:assert math.prod(res[k]['cooler_m'][:2])>=cases[k]['cooler_minimum_face_m2']
vac=s['high_ratio']['compressor_inlet_volume_m3_s']*scale
lines=[];checks={}
def add(t):lines.append(t)
def inp(n,v,u=''):add(f'¢` {n} = {v:.14g} {u} `')
def calc(n,e,v,u=''):add(f'¢` {n} = {e} = ?? {u} `');checks[n]=v
add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-13
---------------

# Brayton cooler size comparison — 30 MW per train

13 October 2026. Preliminary scale check for the three candidate auxiliary cycles. **One train removes 30 MW gross from salt; three such trains provide 90 MW gross, not 30 MW total.** No duty or redundancy requirement has been selected. These trains are substantial industrial machinery, not small fans or pony-pump packages.

The estimates have two different evidence levels: flow areas, equivalent bores, shaft powers and counterflow cooler UA follow from the existing thermodynamic calculations; equipment boxes and overall plots below are **judgment-based reservations for a future layout**, not calculated or vendor-confirmed dimensions. Do not treat the reservations as selected equipment. No graphics or accepted site layout is changed.

## Calculated quantities''')
add('| At 30 MW per train | Closed steam 2:1 | Closed nitrogen 4:1 | Open air 6.83:1 |\n| --- | --- | --- | --- |')
for label,k,fac in [('Compressor shaft demand, MW','compressor_W',1e-6),('Turbine shaft output, MW','turbine_W',1e-6),('Compressor inlet volume, m³/s','inlet_volume_m3_s',1),('Hot low-pressure return / exhaust volume, m³/s','hot_low_pressure_volume_m3_s',1),('Compressor inlet equivalent bore, m','inlet_equivalent_bore_m',1),('Hot return / exhaust equivalent bore, m','hot_equivalent_bore_m',1),('Outdoor cooler air volume, m³/s','cooler_air_m3_s',1),('Minimum cooler airflow face at 3 m/s, m²','cooler_minimum_face_m2',1),('Ideal-counterflow cooler UA, kW/K','cooler_counterflow_UA_W_K',.001)]:add('| '+label+' | '+' | '.join(f'{c[k]*fac:,.3g}' for c in cases.values())+' |')
add('''Closed-loop working-fluid bores use 30 m/s; open-air intake and atmospheric exhaust use 15 m/s. They are equivalent circular **clear flow diameters**, excluding wall, insulation, casing, silencers and headers. They are not compressor rotor diameters. Velocity choices are provisional; losses, noise and available space must be checked together. The 3 m/s cooler face velocity is superficial velocity based on cold inlet air, not free-gap velocity between fins. Zero cooler area for open air means that the separate heat-rejection exchanger is absent, not that no intake/exhaust equipment is required.

For the closed cycles, the earlier 30→130°C cooling-air assumption and 500 Pa total air-system loss remain provisional. The 82 m² steam and 76 m² nitrogen values are airflow-based minimum face areas, not complete exchanger sizes. Nitrogen requires about 1.9 times the ideal-counterflow UA because of its closer approach to ambient. Fin area, gas-side coefficient, fin efficiency, depth and headers are not yet specified; particularly for nitrogen, a deeper core or more face area may be necessary without exceeding the pressure budget.

## Initial boxes for a space study — not equipment dimensions

All dimensions are metres. Machine reservations include compressor, turbine, alternator, coupling/gearing allowance and immediate mechanical auxiliaries. They do not define stage arrangement. Cooler reservations allow for a horizontal outdoor fin-fan bank, structure, plenums and fan depth; heights are guesses pending design. Overall plots allow additional local aisles and piping; they do not establish rotor withdrawal or lifting clearances.''')
add('| Provisional reservation | Steam 2:1 | Nitrogen 4:1 | Open air 6.83:1 |\n| --- | --- | --- | --- |')
add('| Machinery box, L × W × H | 15 × 6 × 5 | 15 × 6 × 5 | 22 × 7 × 5.5 |')
add('| Separate outdoor cooler box, L × W × H | 12 × 10 × 6 | 16 × 10 × 7 | None |')
add('| Local plot including access and connections, L × W | 28 × 18 | 30 × 20 | 32 × 16 |')
add('| Local plot area | 504 m² | 600 m² | 512 m² |')
add('''The closed-machine boxes are held equal because smaller nitrogen passages do not establish a shorter or smaller complete train: its compressor is doing more than twice the steam compressor's shaft work, and stage count, speed, seals and gearbox choices are unresolved. The larger nitrogen cooler reservation reflects the greater required UA, but is not a thermal design. The open-air plot includes an allowance for intake filters and local hot-exhaust routing. Intake orientation, silencing, exhaust separation and stack height are unselected and can increase its site requirement.

These plots intentionally put all three concepts in roughly the same **several-hundred-square-metre class**. Small differences between the figures cannot rank the options. A reasonable uncertainty is at least ±50% in reserved area until actual machinery and exchanger layouts exist. Larger changes are possible if separate heaters, long remote ducts or redundant trains are needed.

## Industrial size benchmark

Siemens Energy's [SGT-750 manufacturer data](https://www.siemensenergy.com/global/en/home/products-services/product/sgt-750.html) lists about 118 kg/s exhaust flow and a power-generation package approximately 20.3 × 4.8 × 4.1 m, excluding the intake filter housing and exhaust stack. Its mechanical-drive package is 12.8 × 4.3 × 4.1 m and excludes driven equipment. The [SGT-600](https://www.siemens-energy.com/global/en/home/products-services/product/sgt-600.html) lists 81.3 kg/s and a generation package 18.8 × 4.6 × 4.0 m, with similar exclusions. The open-air trial processes about 103 kg/s, between those mass flows.

These combustion-turbine packages provide a scale comparison only. They have different pressure ratios, turbine temperatures, rotor architecture and electrical output. They are not selected products, and they cannot be assumed to operate in our externally heated arrangement. Their dimensions do not validate the closed steam/nitrogen reservations or the proposed 22 × 7 m open-air box. They do show why a several-metre industrial package is a more credible starting point than a small standby generator enclosure, despite our few-megawatt net output.

## Scope and practicality

This comparison assumes reuse of one existing steam-generator heat-transfer train as the salt-to-working-fluid heater. **The existing generator, reactor, main salt piping and generator building are excluded from the additional plot areas.** Reuse is unverified: gas-side heat transfer, pressure loss and isolation/changeover must be checked. A dedicated salt-to-gas heater would add an as-yet-unsized major item; the boxes above would then be incomplete. Salt-pump equipment, startup electrical facilities, remote switchgear, redundant safety divisions and site-wide separation are also not sized here; only ordinary local service space is included.

Three independent 30 MW trains would reserve roughly **1,500–1,800 m² total** with these example plots, before shared access, separation or redundancy additions. This suggests an outdoor auxiliary plant or annex, rather than fitting all equipment into remaining reactor-building space. Whether that is practical depends on the required heat-removal duty and plot available. The calculations do not establish a decay-heat requirement.

If only 10 MW per train is required, the same-state flow areas and ideal-counterflow UA scale to one third; equivalent duct diameters scale by the square root of one third. Complete package dimensions and site area do not scale linearly because stage arrangements and service clearances remain. Reusing one 30 MW train for all three salt legs is a separate hydraulic and availability arrangement, not a reason to divide the above train duty by three.

The earlier vacuum steam 8:1 option is especially unattractive for compactness: at 30 MW its compressor-inlet volume is approximately 1,564 m³/s, corresponding to an 8.15 m equivalent pipe at 30 m/s. This is a flow-area illustration, not a proposed pipe design. That candidate is omitted from the main layout boxes.

## Hurmet verification

Volumes and UA are imported from the preserved cycle results. Editable velocities below recalculate areas and equivalent bores; they do not resize the provisional equipment boxes.''')
inp('ClosedVelocity',30,'m/s');inp('OpenVelocity',15,'m/s');inp('CoolerFaceVelocity',3,'m/s')
for prefix,k in [('Steam','steam'),('Nitrogen','nitrogen'),('Air','air')]:
 c=cases[k]
 inp(prefix+'InletVolume',c['inlet_volume_m3_s'],'m3/s');inp(prefix+'HotVolume',c['hot_low_pressure_volume_m3_s'],'m3/s')
 v='OpenVelocity' if k=='air' else 'ClosedVelocity'
 calc(prefix+'InletArea',f'{prefix}InletVolume / {v}',c['inlet_volume_m3_s']/(15 if k=='air' else 30),'m2')
 calc(prefix+'InletDiameter',f'sqrt(4 * {prefix}InletArea / π)',c['inlet_equivalent_bore_m'],'m')
 calc(prefix+'HotDiameter',f'sqrt(4 * {prefix}HotVolume / ({v} * π))',c['hot_equivalent_bore_m'],'m')
 if k!='air':
  inp(prefix+'CoolerVolume',c['cooler_air_m3_s'],'m3/s');calc(prefix+'CoolerFace',f'{prefix}CoolerVolume / CoolerFaceVelocity',c['cooler_minimum_face_m2'],'m2')
calc('NitrogenToSteamUARatio',f'{cases["nitrogen"]["cooler_counterflow_UA_W_K"]:.14g} / {cases["steam"]["cooler_counterflow_UA_W_K"]:.14g}',cases['nitrogen']['cooler_counterflow_UA_W_K']/cases['steam']['cooler_counterflow_UA_W_K'])
add('''## Reproduction and next step

Run `python brayton_size_screen.py`, then `node check_brayton_size.cjs` using the existing Hurmet/Temml environment. Twelve numerical checks, save/reopen, and diameter/velocity sensitivity are verified. Source hashes and the explicit reservation dimensions are in `brayton-size-results.json`.

Next establish the heat duty per train, obtain compressor/turbine envelopes for these actual flows and temperatures, and develop a coupled heat-transfer/pressure-drop cooler design. Only then use a site fit to choose between the options. No accepted site geometry or design decision is changed by these reservations.''')
t='\n\n'.join(lines)+'\n';t=re.sub(r'(?m)(^\|.*\|)\n\n(?=\|)',r'\1\n',t)
def widths(m):
 b=m.group(0);n=b.splitlines()[0].count('|')-1
 return b+'\n{.grid colWidths="'+' '.join(['250']+['125']*(n-1))+'"}'
t=re.sub(r'(?m)^\|.*(?:\n\|.*)*',widths,t)
write_worksheet(D/'Brayton cooler size comparison - Hurmet.md', t)
source_paths=[D/'brayton_size_screen.py',D/'brayton-cooler-results.json',D/'nitrogen-brayton-results.json',D/'open-air-brayton-results.json',D/'brayton-fan-pump-results.json']
output=dict(date='2026-10-13',heat_per_train_MW=30,cases=cases,vacuum_steam_inlet_m3_s=vac,hurmet_checks=checks,source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths})
(D/'brayton-size-results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'cases':cases,'checks':len(checks)},indent=2))
