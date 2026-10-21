
# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json,sys
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
r=json.loads((ROOT/'motor-equipment-sizing.json').read_text());lines=[];checks={}
def add(t):lines.append(t)
def inp(n,v,u=''):add(f'¢` {n} = {v:.12g} {u} `')
def calc(n,expr,v,u=''):add(f'¢` {n} = {expr} = ?? {u} `');checks[n]=v
add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-11
---------------

# Motor-BFP power-plant equipment — revised working draft

11 October 2026. D-029 updates the equipment schedule after the owner authorized
resizing for the motor-driven boiler feed pumps. Prior steam-drive calculations
and presentation snapshots remain preserved. This worksheet is the current
preliminary equipment basis; it does not select vendor equipment.

The external Python calculation imports the checked motor cycle at exactly 5 kPa,
1,500 MW heat input and 26.5/1.0 MPa BFP/condensate discharge. Gross output is
697.1 MW. Output after BFP and condensate pumps is 671.6 MW; other station loads
remain excluded. Heater properties, densities, coupled flows, UA and cooling cases
are external results. Hurmet checks the sizing arithmetic below. A cycle-state
change requires rerunning Python, not just recalculating this worksheet.

The 26.5 MPa pressure budget is represented as an adiabatic aggregate pressure
loss after the HP heaters to the unchanged 24 MPa SG inlet. Its earlier allocation
among piping, heaters, SG and main-steam piping has not been physically resolved.
It is a pump-duty allowance, not a validated distributed pressure network.

## Reheater and generators
''')
add('¢` format = "h7" `');inp('Pi',3.141592653589793)
h=r['reheater'];t=r['turbines'];el=r['electrical']
inp('ReheatUA',h['UA_W_K'],"'W/K'");inp('ReheatU',1000,"'W.m-2.K-1'");inp('AreaFactor',1.2);inp('ReheatCount',4)
calc('ReheatArea','ReheatUA / ReheatU * AreaFactor',h['area_m2'],"'m2'");calc('AreaPerModule','ReheatArea / ReheatCount',h['area_per_module_m2'],"'m2'")
inp('ReheatDuty',h['duty_MW'],'MW');calc('DutyPerModule','ReheatDuty / ReheatCount',h['duty_per_module_MW'],'MW')
add(f"Four reheaters now reserve **16 × 3.25 × 3.25 m each**, plus 13 m straight tube withdrawal. About {h['tubes_per_module']:,} assumed 25.4 mm OD / 12 m tubes per module give a {h['bundle_eq_diameter_m']:.2f} m equivalent bundle. U and packing remain assumptions; shell wall, tube wall, pressure loss and vibration are not designed. At U=500, required surface doubles; at U=1,500 it is two-thirds. The prior 16 × 3 × 3 m boxes are superseded.")
inp('HPIPPower',t['HP_IP_electrical_MW'],'MW');inp('LPPower',t['electrical_MW']['LP'],'MW');inp('PowerFactor',.9);inp('CapacityFactor',1.1)
calc('HPIPRequired','HPIPPower / PowerFactor * CapacityFactor',t['HP_IP_generator_min_MVA'],'MW');calc('LPRequired','LPPower / PowerFactor * CapacityFactor',t['LP_generator_min_MVA'],'MW')
add('The last two calculated numerical values express apparent-power requirements in **MVA** (Hurmet uses MW as the power-dimension unit). Reserve **550 MVA HP/IP and 350 MVA LP**. Both include the same 0.90 power factor and 10% capacity allowance; these are not purchased nameplate ratings. The HP/IP allowance replaces 500 MVA. Turbine outlines and shaft arrangement remain provisional.')
add('## Pumps and electrical supply')
inp('BFPshaft',r['pumps']['feedwater']['shaft_MW'],'MW');inp('DriveEfficiency',.95);inp('DutyPumps',2);inp('MotorRating',15,'MW')
calc('BFPinput','BFPshaft / DriveEfficiency',el['operating_BFP_load_MW'],'MW');calc('ShaftPerPump','BFPshaft / DutyPumps',r['pumps']['feedwater']['per_duty_shaft_MW'],'MW');calc('ElectricPerPump','BFPinput / DutyPumps',r['pumps']['feedwater']['per_duty_electric_MW'],'MW')
inp('MotorPowerFactor',.95);inp('ElectricalMargin',1.1)
calc('RatedInputPerTrain','MotorRating / DriveEfficiency',el['per_train_rated_electric_MW'],'MW');calc('TransformerRequirement','RatedInputPerTrain / MotorPowerFactor * ElectricalMargin',el['per_train_transformer_required_MVA'],'MW')
add('Reserve **three 15 MW motor/pump trains, two duty and one standby**. Each BFP supply train has a **20 MVA transformer allowance**, above the calculated MVA requirement. The allowance uses assumed 0.95 supply power factor and 95% combined drive efficiency; vendor motor/drive maps, voltage, harmonics, losses and protection are unresolved. The idle standby train is not counted at full operating consumption. No full-station N+1 electrical capability is claimed. Reserve a **20 × 10 × 7 m annex** for BFP electrical equipment; partition, fire separation, ventilation and transformer placement remain to design.')
add(f"BFP hydraulic sizes stay at 0.783 m³/s total and 26.5 MPa discharge. Retain 355 kW condensate motors (three 50% pumps), 3.5 MW cooling-water motor allowances (three 50% pumps at assumed 20 m head), and two 4.5 m ID × 22 m straight deaerator storage shells. Condensate load is {r['pumps']['condensate']['electric_MW']:.3f} MW; cooling-water load is {r['pumps']['cooling_water']['electric_MW']:.2f} MW. Even subtracting both water-pump systems and BFP leaves {r['performance']['after_BFP_CEP_CW_MW']:.1f} MW **before remaining station loads**, not final net export.")
add('## Heater and condenser schedule')
add('HP2 and HP1 now receive main-IP bleeds at about 435°C and 371°C. Their duties are similar but their inlet/desuperheating regions require redesign. The premixed-stream areas below are proxies, not separate-zone designs. LP3 operates at 0.12186 MPa; retain its former larger box pending detailed design.')
rows=['| Heater | Duty MW | Area m² | Bleed °C |','| --- | --- | --- | --- |']
for x in r['heaters']:rows.append(f"| {x['name']} | {x['duty_MW']:.2f} | {x['area_m2']:.0f} | {x['bleed_C']:.1f} |")
rows.append('{.grid colWidths="100 110 110 110"}');add('\n'.join(rows))
co=r['condenser'];add(f"Retain three **16 × 7 × 9 m condenser envelopes**, each with 13 m withdrawal, {co['provided_area_m2']:.0f} m² total surface and the same 23.76 m³/s cooling flow. Duties become {co['reference_duty_MW']:.1f} MW at 5 kPa, {co['hot_duty_MW']:.1f} MW at 30°C inlet and {co['extreme_duty_MW']:.1f} MW at 35°C inlet. The latter two use their recalculated backpressures. Six LP exhaust flows remain a candidate; total volumetric flow is {t['LP_exhaust_volume_m3_s']:.0f} m³/s at 5 kPa. The final heat sink and cooling-water pump location remain outside the hall arrangement.")
add('## Revised pipe-bore register')
add('Bores are internal, with walls, insulation and supports additional. Keep existing bore allowances where the new flow is lower. Increase bores that fail the prior velocity limits in the 5 kPa reference or any of the three cooling cases. The former pump-turbine supply is removed; its exhaust service is replaced by main-IP outlet steam to the deaerator. No reactor/SG main-header flow change is introduced.')
rows=['| Service | Count | Bore mm | Velocity m/s |','| --- | --- | --- | --- |']
for x in r['pipes']:rows.append(f"| {x['service']} | {x['parallel']} | {x['bore_m']*1000:.0f} | {x['velocity_m_s']:.2f} |")
rows.append('{.grid colWidths="280 60 80 120"}');add('\n'.join(rows))
add('Executable velocity and constant-property pressure-loss screens follow. Each uses the reference density/volume imported from CoolProp, 40 m route length, Darcy f=0.015 and K=5. These are not actual routed losses. Wet LP1 uses homogeneous density. Drain, vent, startup, thermal expansion, nozzle and relief services remain unsized; pressure walls and insulation are not inferred from these bores.')
inp('RouteLength',40,'m');inp('DarcyFactor',.015);inp('LocalK',5)
for i,x in enumerate(r['pipes'],1):
 add(f"**P{i}: {x['service']}**")
 inp(f'Q{i}',x['volume_m3_s'],"'m3/s'");inp(f'D{i}',x['bore_m'],'m');inp(f'N{i}',x['parallel']);inp(f'Rho{i}',x['rho_kg_m3'],"'kg/m3'")
 calc(f'V{i}',f'4 * Q{i} / (N{i} * Pi * D{i}^2)',x['velocity_m_s'],"'m/s'")
 calc(f'Drop{i}',f'(DarcyFactor * RouteLength / D{i} + LocalK) * Rho{i} * V{i}^2 / 2',x['screen_dp_kPa'],'kPa')
add('''## First dimensional building check

The layout reserves a **66 × 40 × 28 m main hall** and a **20 × 10 × 7 m BFP
electrical annex**. Turbines/generators are at +12 m above the common equipment
floor; condenser tops are +9.5 m. The lowest deaerator water level remains +14 m.
Storage boxes include 3 m beyond the 22 m straight shells for heads. A provisional
crane underside at +25 m gives at least 6 m above the turbine boxes, with roof
at +28 m. Crane, floors, supports and lifting loads are not designed.

Tube withdrawal uses 13 m volumes beyond the north ends of condenser/reheater
boxes, extending through removable wall panels onto a 7 m external apron.
Heater withdrawal is directed south onto a 12 m apron. The first old 45 × 24 ×
20 m reservation does not contain this arrangement. The new dimensions are a
workable reservation for this particular placement, not a proven minimum.
Most of the increase is the first inclusion of actual equipment/access volumes,
not a consequence of changing the BFP drive alone.

The companion `turbine_layout.py` / `turbine-layout.json` checks 29 equipment
boxes and 16 service volumes for selected intersections, wall containment and
vertical separation. A dimensioned plan accompanies the Blender draft. Pipe
corridors have not been routed; structural columns, deck openings, stairs,
egress, crane reach, rotor handling and full installation transport remain open.
Thus passing box checks does not establish that a complete plant fits.

## Reproduction and sources

Use pinned `requirements.txt` and run `python size_motor_equipment.py`,
`python publish_motor_equipment.py`, then `node check_motor_equipment_hurmet.cjs`
with HURMET_ENGINE and TEMML_ENGINE set as in the cycle README.
The JSON records input hashes; Python screens all four operating cases. Hurmet
checks power/capacity/area and every pipe velocity/loss after save/reopen, plus
reheater-U and drive-efficiency sensitivities.

Sources: [motor-drive heat balance](BFP%20drive%20comparison%20-%20Hurmet.md),
[historical sizing assumptions](Power%20plant%20equipment%20sizing%20-%20Hurmet.md),
and their linked CoolProp/property references. No new vendor outlines or verified
material allowables are introduced by this revision.
''')
write_worksheet(ROOT/'Motor-BFP equipment sizing - Hurmet.md', '\n\n'.join(lines)+'\n');(ROOT/'motor-equipment-hurmet-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
