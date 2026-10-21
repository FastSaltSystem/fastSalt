"""Publish the selected reheat case; properties and coupled solutions are imports."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json
from CoolProp.CoolProp import PropsSI
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'reheat-selection.json').read_text());s=r['selected_at_5kPa'];st=s['states']
lines=['''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Selected reheat and LP wetness - preliminary design

11 October 2026. This selects a working thermal-cycle configuration after the
owner requested resolution of reheat feasibility and LP wetness. It supersedes
the 4 MPa / 470°C first trial for future equipment studies. Earlier worksheets
and results remain preserved as comparisons.

**Selected inputs:** 2.8 MPa HP exhaust; 2.66 MPa hot reheat after a 5% pressure
allowance; 510°C reheated steam; 380°C heating-stream return at 24 MPa. Retain
main-steam reheat, 1,500 MW heat input, 830 K main steam and 560 K feedwater.
The two feed-pump-turbine extractions move from 2.0/1.2 MPa to 1.6/1.0 MPa.
The deaerator remains 0.6 MPa. The highest LP heater extraction is solved to close
the deaerator heat balance, then held fixed across cooling and efficiency cases.

Use **5 kPa absolute as a provisional minimum condenser pressure** at these
reheat conditions. It is a modeling constraint, not an equipment operating limit
approved by a supplier. The screening target is at most 10% equilibrium exhaust
moisture. No moisture separator or additional reheater has been added.

**Imported boundary:** steam properties, coupled flow fractions, cycle-specific
work, the reheater temperature profile/integrated UA, and cooling-case pressures
are calculated in Python/CoolProp. Hurmet independently reproduces mass flow,
gross power, reheater duty, exhaust moisture from enthalpies, and area sensitivity.
Changing pressure, reheat temperature, heating-return temperature or efficiencies
requires rerunning the Python model and republishing. Duty changes here only scale
the fixed cycle and do not describe off-design turbine performance.

## Imported properties and selected-cycle inputs

¢` format = "h7" `
''']
def inp(n,v,u=''):lines.append(f'¢` {n} = {v:.12g} {u} `\n')
def calc(n,e,u=''):lines.append(f'¢` {n} = {e} = ?? {u} `\n')
inp('ReactorDuty',1500,'MW')
for n,v in [('MainH',st['main']['h']),('FeedH',st['feedwater']['h']),('HPwork',s['specific_work']['HP']),('IPwork',s['specific_work']['IP']),('LPwork',s['specific_work']['LP']),('ColdReheatH',st['reheat_cold']['h']),('HotReheatH',st['reheat_hot']['h']),('HeatingReturnH',st['reheat_return']['h']),('LPExhaustH',st['LPex']['h']),('SatLiquidH',st['condenser']['h']),('SatVaporH',PropsSI('H','P',5000,'Q',1,'HEOS::Water'))]:inp(n,v,"'J/kg'")
inp('HeatingFraction',s['fractions']['reheat']);inp('ReheatedFraction',s['reheat_flow']/s['mass']);inp('ShaftEfficiency',.99);inp('GeneratorEfficiency',.985);inp('MoistureTarget',.10)
lines.append('## Flow, power and reheat duty at 5 kPa\n')
calc('MainFlow','ReactorDuty / (MainH - FeedH)',"'kg/s'")
calc('GrossElectric','MainFlow * (HPwork + IPwork + LPwork) * ShaftEfficiency * GeneratorEfficiency','MW')
calc('GrossEfficiency','GrossElectric / ReactorDuty')
calc('HeatingSteam','MainFlow * HeatingFraction',"'kg/s'")
calc('ReheatedSteam','MainFlow * ReheatedFraction',"'kg/s'")
calc('ReheatColdDuty','ReheatedSteam * (HotReheatH - ColdReheatH)','MW')
calc('ReheatHotDuty','HeatingSteam * (MainH - HeatingReturnH)','MW')
calc('ReheatBalance','ReheatHotDuty - ReheatColdDuty','MW')
calc('ExhaustQuality','(LPExhaustH - SatLiquidH) / (SatVaporH - SatLiquidH)')
calc('ExhaustMoisture','1 - ExhaustQuality')
calc('WetnessPass','ExhaustMoisture <= MoistureTarget')
lines.append('''The gross result includes the steam diverted to reheating and the steam-driven
BFP. Do not subtract BFP shaft work again. Net export awaits the station auxiliary
load list. The normal 20°C cooling case settles slightly above 5 kPa, so its power
is slightly below this reference value.

## Reheater thermal margin and area sensitivity

The 1,601-point counterflow enthalpy-temperature check was repeated at 3,201 points.
The hot and cold streams remain separated by more than 20 K. This exceeds the
provisional 10 K screen. Unlike an endpoint-only LMTD estimate, the imported
UA integrates Q * integral[1/(Th - Tc)] over the actual nonlinear temperature
profiles. No tube material, heat-transfer correlation or pressure-boundary design
is selected here. The following U values are explicit sensitivity assumptions,
not claimed representative performance; resulting areas exclude design margins.
''')
inp('MinimumApproach',s['pinch'],'K');inp('ImportedUA',r['reheater_UA_W_K'],"'W/K'")
for i,u in enumerate([500,1000,1500],1):
 inp('AssumedU'+str(i),u,"'W.m-2.K-1'");calc('ReheaterArea'+str(i),f'ImportedUA / AssumedU{i}',"'m2'")
lines.append('## Coupled cooling-water cases, unchanged condenser\n')
for c in r['cooling_cases']:
 lines.append(f"- **{c['inlet_C']}°C inlet water:** {c['condenser_kPa']:.3f} kPa condenser; {c['gross_MW']:.2f} MW gross; {c['moisture_percent']:.3f}% LP moisture; {c['condenser_MW']:.2f} MW condenser duty.\n")
lines.append('''The existing 38,513 m² condenser and 23.76 m³/s cooling-water flow are retained
with constant U. These thermal cases rebalance extraction flows at fixed pressures
and assumed interval efficiencies; they are not supplier off-design maps.

## Sensitivity and cold-weather control requirement
''')
for c in r['LP_efficiency_sensitivity']:
 lines.append(f"- LP interval efficiency {c['LP_interval_efficiency']:.2f} at 5 kPa: {c['moisture_percent']:.3f}% moisture; {c['gross_MW']:.2f} MW gross.\n")
c=r['illustrative_15C_case'];cold=r['uncontrolled_3kPa']
lines.append(f'''At 3 kPa with LP interval efficiency 0.90, calculated moisture rises to
{cold['moisture_percent']:.2f}%, above the screen. Thus the minimum-pressure condition
is part of the selected preliminary cycle, not optional.

For an illustrative 15°C supply, ideal mixing of approximately
{100*c['return_recycle_fraction']:.1f}% warm return with fresh supply would give a
{c['effective_mixed_inlet_C']:.2f}°C effective inlet and maintain 5 kPa at the nominal
case, with the same total condenser flow. This is only a heat/mass-balance example.
Actual bypass, tower/fan controls, pump head, fouling and operating protections are
not designed. Lower reheat temperature or other turbine efficiencies also require
rechecking the pressure floor; this worksheet does not define a startup envelope.

## Selection and remaining work

Relative to the original 5 kPa case, the selected case loses about
{r['comparison']['gross_penalty_MW']:.2f} MW gross. Reheater heating flow rises from
{r['comparison']['baseline_reheat_supply_percent']:.2f}% to {100*s['fractions']['reheat']:.2f}%
of total main flow, and reheater duty rises from
{r['comparison']['baseline_reheat_MW']:.1f} MW to {s['reheat_duty']/1e6:.1f} MW.
This is the price of meeting the wetness screen with more thermal margin while
retaining the requested single main-steam reheater.

The study compared 45 combinations at fixed provisional heater pressures;
selection favors thermal and flow margin, not the highest calculated output.
[Trial results](reheat-trials.csv) retain rejected cases. All selected bleeds are
positive, including the previously problematic intermediate HP heater.

This resolves the two issues **within the preliminary thermal model**. Turbine
supplier wetness/erosion and exhaust-volume limits, performance maps, reheater
construction and pressure drop, control design and transient operation remain
engineering tasks. The 10% criterion is a project screen, not an industry-wide
acceptance limit. Original reactor/steam-generator conditions and Blender geometry
are not changed by this worksheet.

Reproduce with `python resolve_reheat.py`, `python publish_reheat_selection.py`,
then `node check_reheat_hurmet.cjs` with the official Hurmet engine environment
variables described in [the basis](README.md). Dependencies use CoolProp 7.2.0
HEOS water ([IAPWS-95](https://coolprop.org/fluid_properties/fluids/Water.html)).
The source hashes, checks, selected state table and full results are saved alongside.
''')
write_worksheet(ROOT/'Selected reheat and wetness - Hurmet.md', '\n'.join(lines)+'\n')
