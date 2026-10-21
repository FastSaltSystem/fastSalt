"""Publish imported cycle results and executable Hurmet comparison arithmetic."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json
import sys
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
r=json.loads((ROOT/'bfp-drive-comparison.json').read_text())
c=r['proposed_pressure_comparison'];s=c['steam'];e=c['electric']; expected={}
parts=['''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Boiler-feed-pump drive comparison

11 October 2026. **Preliminary alternative study**, requested to assess whether
electric drive offers simpler operation without a significant efficiency loss.
The existing selected cycle, diagram and equipment schedule remain preserved.

**Finding:** an electric BFP drive gives about 4 MW less output at the proposed
pump pressures: approximately 0.6% of comparison output, or 0.27 percentage points
of thermal efficiency. This is a modest modeled penalty, not zero. Recommendation:
carry variable-speed electric drive forward as the preferred candidate for review.
No supplier-qualified motor, turbine or final plant efficiency is established.

## Basis and calculation boundary

Both alternatives use 1,500 MW thermal input; 24 MPa / 556.85°C main steam;
24 MPa / 286.85°C SG-inlet feedwater; 2.8 MPa HP exhaust; 2.66 MPa / 510°C
reheat; 380°C heating-stream return; and a 5 kPa condenser reference. All
pressures are absolute. Main steam flow remains about 711.7 kg/s.

Use the proposed **26.5 MPa BFP discharge and 1.0 MPa condensate-pump discharge**
for both alternatives. Pump hydraulic efficiencies are 85% and 80%, respectively.
The BFP-to-SG pressure allowance is represented by an adiabatic pressure drop
after the high-pressure heaters, retaining the accepted SG-inlet enthalpy.
A distributed loss/elevation model could shift heater duties slightly.

The steam-drive case uses 80% interval isentropic efficiency and 99% shaft transfer.
The electric case assumes **95% combined electrical-input-to-pump-shaft efficiency**
(motor, drive and associated supply losses in aggregate). This is an editable
screening assumption; it is not a supplier value. Main turbine HP/IP/LP efficiencies
remain 88/90/88%, with 99% shaft transfer and 98.5% generator efficiency.

The old cycle's LP3 heater pressure cannot simply be retained when the larger
steam-driven pump is introduced: the increased auxiliary exhaust over-heats the
deaerator in the original idealized balance. For the matched comparison, lower LP3
from 0.15525 to **0.12186 MPa**, making the steam case's supplemental DA bleed zero.
**Both alternatives use that same new LP3 pressure.** Other heater pressures stay
fixed. Sensitivity cases reselect LP3 for each auxiliary-turbine efficiency, then
hold it common to the paired electric case. This is a conceptual heater redesign,
not an off-design operating prediction for the old equipment.

**Imported boundary:** Python/CoolProp 7.2.0 calculates water properties,
expansion states, coupled heater/reheater/DA flows, condenser duty and gross
power. Hurmet executes the power subtraction, efficiencies and capacity ratios
below. Changing steam states, pump pressures, heater arrangement or turbine
efficiencies requires rerunning Python; editing motor efficiency alone does not.
The reproducible source is `compare_bfp_drives.py`; all states, sensitivity cases,
checks and input hashes are in `bfp-drive-comparison.json`.

## 1. Equal-duty comparison

“Comparison output” subtracts the BFP electrical load, where applicable, and
condensate-pump electrical load from main-generator output. It **excludes cooling
water, salt pumps, fans and other station services** and is not final net export.
The steam BFP's duty is already charged through steam diversion; do not subtract
its shaft power again.
''']
def add(s):
 if s.startswith('|') and parts[-1].rstrip().endswith('|'):parts[-1]+='\n'+s
 else:parts.append(s)
def inp(n,v,u=''):
 add(f'¢` {n} = {v:.12g} {u} `')
def calc(n,expr,v,u=''):
 add(f'¢` {n} = {expr} = ?? {u} `');expected[n]=v
add('¢` format = "h7" `')
inp('ThermalInput',1500,'MW')
inp('SteamGross',s['gross_MW'],'MW');inp('ElectricGross',e['gross_MW'],'MW')
inp('PumpShaft',e['bfp_shaft_MW'],'MW');inp('DriveEfficiency',.95)
inp('SteamCondensateLoad',s['cep_electric_MW'],'MW');inp('ElectricCondensateLoad',e['cep_electric_MW'],'MW')
calc('ElectricPumpLoad','PumpShaft / DriveEfficiency',e['bfp_electric_MW'],'MW')
calc('SteamComparisonOutput','SteamGross - SteamCondensateLoad',s['partial_net_MW'],'MW')
calc('ElectricComparisonOutput','ElectricGross - ElectricPumpLoad - ElectricCondensateLoad',e['partial_net_MW'],'MW')
calc('OutputPenalty','SteamComparisonOutput - ElectricComparisonOutput',-c['net_change_MW'],'MW')
calc('RelativeOutputPenalty','100 * OutputPenalty / SteamComparisonOutput',-c['net_change_MW']/s['partial_net_MW']*100)
calc('SteamEfficiencyPercent','100 * SteamComparisonOutput / ThermalInput',s['partial_efficiency_percent'])
calc('ElectricEfficiencyPercent','100 * ElectricComparisonOutput / ThermalInput',e['partial_efficiency_percent'])
calc('EfficiencyPenaltyPoints','SteamEfficiencyPercent - ElectricEfficiencyPercent',-c['efficiency_change_percentage_points'])
add('RelativeOutputPenalty is percent of comparison output; EfficiencyPenaltyPoints is an absolute percentage-point difference.')
add(f'''| At 5 kPa, proposed pump pressures | Steam drive | Electric drive |
| --- | --- | --- |
| Main-generator gross output, MW | {s['gross_MW']:.2f} | {e['gross_MW']:.2f} |
| BFP shaft demand, MW | {s['bfp_shaft_MW']:.2f} | {e['bfp_shaft_MW']:.2f} |
| BFP electric demand, MW | 0 | {e['bfp_electric_MW']:.2f} |
| Condensate-pump electric demand, MW | {s['cep_electric_MW']:.3f} | {e['cep_electric_MW']:.3f} |
| Comparison output, MW | {s['partial_net_MW']:.2f} | {e['partial_net_MW']:.2f} |
| Comparison thermal efficiency | {s['partial_efficiency_percent']:.3f}% | {e['partial_efficiency_percent']:.3f}% |
| Condenser rejection, MW | {s['condenser_MW']:.2f} | {e['condenser_MW']:.2f} |
| LP exhaust moisture | {s['moisture_percent']:.2f}% | {e['moisture_percent']:.2f}% |

Electric drive frees steam for the main turbine, increasing gross output by
{e['gross_MW']-s['gross_MW']:.2f} MW. Its {e['bfp_electric_MW']:.2f} MW electrical
consumption is therefore largely offset. Some freed steam also supplies additional
main-steam reheat, so the change is more than an electrical-conversion loss.

The original 24 MPa / 0.72 MPa pump-pressure case was separately reproduced exactly.
At those original pressures the electric penalty is
{-r['original_pressure_comparison']['net_change_MW']:.2f} MW. Do not compare
this new electric result directly against the old 678.72 MW gross figure;
that would mix drive changes, pressure budgets and gross/net accounting.

## 2. Heater routing and equipment consequences

Remove the feed-pump turbine and its supply, exhaust, governing and associated
auxiliary systems. Supply HP2 at 1.6 MPa and HP1 at 1.0 MPa from extraction ports
on the reheated main IP turbine, and the deaerator at 0.6 MPa from the IP outlet.
These are separate extraction services, not successive throttles from one header.
The heater train and its drain cascades remain. Startup heating still needs an
auxiliary steam supply even though the feed pumps can start electrically.

| Service | Steam-drive source / flow | Electric-drive source / flow |
| --- | --- | --- |
| HP2 | Pump-turbine bleed / {s['flows_kg_s']['HP2']:.2f} kg/s | IP extraction / {e['flows_kg_s']['HP2']:.2f} kg/s |
| HP1 | Pump-turbine bleed / {s['flows_kg_s']['HP1']:.2f} kg/s | IP extraction / {e['flows_kg_s']['HP1']:.2f} kg/s |
| Deaerator steam | Pump-turbine exhaust / {s['pump_turbine_exhaust_kg_s']:.2f} kg/s | IP outlet / {e['flows_kg_s']['DA']:.2f} kg/s |

The new HP2/HP1 bleeds are hotter, at approximately
{e['heater_bleed_states']['HP2']['t']-273.15:.1f} / {e['heater_bleed_states']['HP1']['t']-273.15:.1f}°C.
Their inlet regions need desuperheating capability. Lower bleed mass alone does
not establish smaller piping or heaters. The seven heater energy balances and
positive local approaches were checked; area proxies are in the JSON. These
premixed-stream proxies do not replace a desuperheating/condensing/drain-cooling
zone design.
''')
inp('SteamReheatDuty',s['reheat_MW'],'MW');inp('ElectricReheatDuty',e['reheat_MW'],'MW')
calc('ReheaterDutyIncreasePercent','100 * (ElectricReheatDuty / SteamReheatDuty - 1)',100*(e['reheat_MW']/s['reheat_MW']-1))
inp('ElectricReheaterArea',e['reheater_area_proxy_m2'],"'m2'")
inp('OperatingPumps',2);inp('InstalledPumps',3);inp('MotorRating',15,'MW')
calc('DutyPerPump','PumpShaft / OperatingPumps',e['bfp_shaft_MW']/2,'MW')
calc('ElectricalDutyPerPump','ElectricPumpLoad / OperatingPumps',e['bfp_electric_MW']/2,'MW')
calc('MotorShaftMarginPercent','100 * (MotorRating / DutyPerPump - 1)',100*(15/(e['bfp_shaft_MW']/2)-1))
add(f'''Retain the preliminary **3 × 50% arrangement: two duty pumps and one standby**,
with **15 MW motor shaft ratings** as layout allowances. Normal per-pump electrical
input and motor nameplate shaft rating are different quantities. Electrical
service must be sized for full-rated input, overload/starting and standby policy;
the duty calculation is not its nameplate rating. Motor/drive cooling, supply
transformers and switchgear remain to size. Emergency feedwater and loss-of-power
provisions require separate design.

Reheater heat-transfer area is approximately **{e['reheater_area_proxy_m2']:.0f} m²**
versus **{s['reheater_area_proxy_m2']:.0f} m²** for the matched steam case, using the
same U=1,000 W/(m² K) and 20% allowance. Relative to the previously published
8,179 m² allowance the electric case adds about
{100*(e['reheater_area_proxy_m2']/8179.469947644-1):.1f}%. Four candidate modules
would each need roughly {e['reheater_area_proxy_m2']/4:.0f} m². The temperature
profile is unchanged, so the minimum approach remains about {e['reheater_min_approach_K']:.2f} K;
UA scales with duty in this comparison. More flow also requires checking reheater
pressure loss, pipe bores and the IP turbine flow capacity. We have not assumed
the existing envelopes can absorb these changes.

## 3. Sensitivities

First hold auxiliary-turbine efficiency at 80%, changing only the assumed combined
electric-drive efficiency. Positive numbers below are an electric-drive penalty.

| Electric-drive efficiency | Output penalty, MW | Efficiency penalty, percentage points |
| --- | --- | --- |''')
for row in r['efficiency_sensitivity']:
 if row['aux_turbine_eff']==.8:add(f"| {row['electric_eff']*100:.0f}% | {-row['delta_MW']:.2f} | {-row['delta_pp']:.3f} |")
add('''Changing auxiliary-turbine efficiency over 75–85% and electric efficiency over
93–98% gives approximately **2.3–5.4 MW** penalty, or **0.15–0.36 percentage points**.
This is a sensitivity envelope, not a statistical confidence interval. The
comparison does not show an efficiency advantage for motor drive within that range.
Main IP/LP efficiency sensitivities are also recorded in the JSON; their interval
models are assumptions rather than supplier performance maps.

The same installed condenser area, U and water flow were then used for both drives,
allowing condenser pressures to differ as heat rejection changes:

| Cooling-water inlet | Steam-case condenser | Electric-case condenser | Electric output penalty |
| --- | --- | --- | --- |''')
for row in r['same_condenser_cooling_cases']:
 a,b=row['steam'],row['electric'];add(f"| {a['cooling_inlet_C']:.0f}°C | {a['inputs']['pc']/1000:.3f} kPa | {b['inputs']['pc']/1000:.3f} kPa | {-row['net_change_MW']:.2f} MW |")
add('''These three cases retain the same base heater pressures and a 5 kPa pressure
floor. The approximately 4.1–4.2 MW penalty includes the small condenser-pressure
increase from additional heat rejection. Cooling-water pump power is common and
excluded; cooling tower/fan control, electrical auxiliary differences and changing
heat-transfer coefficients are not modeled.

## 4. Recommendation and limits

**Prefer electric drive for the next design iteration**, subject to accepting
roughly a 4 MW trade and the increased reheater capacity. It removes the auxiliary
turbine and its steam controls, decouples pump starting from steam availability,
and retains a straightforward duty/standby arrangement. It adds substantial
electrical equipment and does not remove the need for startup heater steam.

The steam-drive reference remains an alternative until the equipment/cycle update
is adopted. The next detailed comparison should use supplier pump/motor/VFD and
turbine maps, revised heater zones, pressure losses and station electrical loads.
No part-load advantage, lifecycle cost, availability advantage or final net output
has been quantified. Electrical trip/ride-through, coastdown and emergency water
supply must be handled separately from this normal-operation heat balance.

## 5. Verification and reproduction

Run in this directory with `requirements.txt` installed:

```sh
python compare_bfp_drives.py
python publish_bfp_comparison.py
HURMET_ENGINE=/path/to/hurmet.cjs TEMML_ENGINE=/path/to/temml.cjs \\
  node check_bfp_hurmet.cjs
```

The solver regresses all original steam-cycle bleed flows and gross/BFP/CEP/
condenser duties; verifies coupled component energy balances, independent
DA/condenser mass balances and whole-cycle first-law closure; and rejects negative
flows. Seven heater thermal profiles have positive approaches and converged UA.
The equal-pressure and unchanged-condenser comparisons are separate, and the
latter independently satisfies effectiveness and LMTD heat transfer.

IP extraction enthalpies are located on the same inlet-referenced expansion curve
for both drives, preserving the previous IP outlet state. Adding extraction ports
therefore does not silently improve the assumed turbine efficiency through extra
numerical stages. Only flow distribution and work change.

Hurmet verification recalculates, saves and reopens the worksheet, compares the
calculated outputs against Python, and checks an independent drive-efficiency
edit. The physical model remains a preliminary steady-state approximation.

## Sources and provenance

- Project basis: [selected cycle](Selected%20reheat%20and%20wetness%20-%20Hurmet.md)
  and [pump/equipment allowances](Power%20plant%20equipment%20sizing%20-%20Hurmet.md).
- Properties: [CoolProp water / IAPWS-95](https://coolprop.org/fluid_properties/fluids/Water.html),
  pinned calculation version 7.2.0; current website documentation may be newer.
- Technology availability: [ABB ACS5000](https://www.abb.com/global/en/areas/motion/drives/medium-voltage-ac-drives/acs5000)
  lists 5–36 MW drives and converter efficiency over 99%. This supports the
  availability of the power range; it does **not** establish our whole-drive 95%
  assumption or constitute motor/drive selection. Accessed 11 October 2026.
''')
# Hurmet tables need plain separators and explicit column widths.
lines='\n\n'.join(parts).splitlines(); formatted=[]
for i,line in enumerate(lines):
 formatted.append(line)
 if line.startswith('|') and (i+1==len(lines) or not lines[i+1].startswith('|')):
  cols=line.count('|')-1
  widths='260 150 150' if cols==3 else '140 140 140 140'
  formatted.append('{.grid colWidths="'+widths+'"}')
write_worksheet(ROOT/'BFP drive comparison - Hurmet.md', '\n'.join(formatted)+'\n')
(ROOT/'bfp-hurmet-checks.json').write_text(json.dumps(expected,indent=2)+'\n')
