"""Publish fixed-condenser results to Hurmet; rerun the Python solve after changes."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json
root=Path(__file__).resolve().parent
r=json.loads((root/'cooling-cases.json').read_text())
s=['''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Cooling-water cases - one condenser envelope

11 October 2026. Owner-accepted condenser-water inlet cases: 20°C normal,
30°C hot design check, 35°C extreme check. These are provisional water conditions,
not outdoor air temperatures or statistical site percentiles.

This sheet screens the **existing** condenser allowance, approximately 38,500 m²,
with the same U and cooling-water flow at each condition. It does not claim that
this is the final hot-weather condenser size. Thermal input remains 1,500 MW.
No reactor-power reduction or additional cooling equipment is assumed.

**Imported result boundary:** condenser pressures, gross power, moisture and
heat rejection are imported from `cooling_cases.py`, which couples the Rankine
cycle to condenser heat transfer. Hurmet independently checks water temperature
rise, LMTD and required area at those imported operating states. Changing an
input here does not update pressure, turbine power or steam properties: rerun
the Python coupling and republish before interpreting changed operating cases.

The cycle retains its extraction pressures and 470°C reheat. Bleed flows are
rebalanced; turbine section efficiencies and U stay fixed. This is a preliminary
thermal screening, not a manufacturer's fixed-machine off-design performance map.

## Common condenser assumptions

¢` format = "h7" `
''']
def inp(n,v,u=''):s.append(f'¢` {n} = {v:.12g} {u} `\n')
def calc(n,e,u=''):s.append(f'¢` {n} = {e} = ?? {u} `\n')
inp('Area',r['area_m2'],"'m2'");inp('OverallU',r['U_W_m2K'],"'W.m-2.K-1'");inp('WaterMass',r['water_mass_kg_s'],"'kg/s'");inp('WaterCp',4180,"'J.kg-1.K-1'");inp('WaterDensity',998,"'kg/m3'")
calc('WaterVolume','WaterMass / WaterDensity',"'m3/s'")
calc('CapacityRate','WaterMass * WaterCp',"'MW/K'")
for i,c in enumerate(r['cases'],1):
 s.append('## '+c['label']+'\n')
 for n,v,u in [('Inlet',c['inlet_C']+273.15,'K'),('CondensingT',c['condensing_C']+273.15,'K'),('Pressure',c['condenser_kPa'],'kPa'),('Gross',c['gross_MW'],'MW'),('Duty',c['condenser_MW'],'MW'),('Moisture',c['exhaust_moisture_percent']/100,'')]:inp(n+str(i),v,u)
 calc('WaterRise'+str(i),f'Duty{i} / CapacityRate','K')
 calc('WaterOutlet'+str(i),f'Inlet{i} + WaterRise{i}','K')
 calc('TerminalApproach'+str(i),f'CondensingT{i} - WaterOutlet{i}','K')
 calc('ColdApproach'+str(i),f'CondensingT{i} - Inlet{i}','K')
 calc('LMTD'+str(i),f'(ColdApproach{i} - TerminalApproach{i}) / ln(ColdApproach{i} / TerminalApproach{i})','K')
 calc('RequiredArea'+str(i),f'Duty{i} / (OverallU * LMTD{i})',"'m2'")
 calc('AreaRatio'+str(i),f'RequiredArea{i} / Area')
 if i>1:calc('GrossReduction'+str(i),f'Gross1 - Gross{i}','MW')
s.append('''## Interpretation and next decision

The same condenser rejects heat at warmer saturation temperature and higher
pressure as inlet water warms. The cooler reference case gives the highest gross
output and highest LP wetness of these three cases. Gross output reductions here
are caused by higher exhaust pressure at fixed thermal input; they are not modeled
reactor deratings. Cooling-system electricity and net export remain unresolved.

No case establishes acceptable turbine operation. The minimum permitted condenser
pressure, wetness and exhaust-volume limits still need to be set. Cooler-than-20°C
conditions require a later low-pressure limit check. The 30°C case is the sizing
reference to use when choosing a permissible hot-weather pressure/output; it does
not by itself specify that permissible value. The 35°C case tests the extreme.

The water flow is fixed at the baseline value, so water temperature rise changes
slightly with condenser duty instead of being forced to 8 K in every case. U is
held constant; fouling, cooling-tower performance, pump/fan curves, pressure drop,
site weather, air leakage and turbine maps remain to develop.

## Reproduction

Run `python cooling_cases.py`, then `python publish_cooling_cases.py`, then
`node check_cooling_hurmet.cjs` with HURMET_ENGINE and TEMML_ENGINE set to the
local official Hurmet bundles. The model dependencies and the initial-cycle
reproduction are documented in [the cycle basis](README.md).

The external solver verifies the condenser relation with an independent LMTD
check, recovers the 5 kPa reference case, retains physical flow fractions and
closes the cycle energy balance. The Hurmet checker independently reproduces
all three required areas and water temperature rises from the imported states.
''')
write_worksheet(root/'Cooling-water cases - Hurmet.md', '\n'.join(s)+'\n')
