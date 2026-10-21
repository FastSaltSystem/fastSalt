
# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json,re
D=Path(__file__).resolve().parent;r=json.loads((D/'nitrogen-brayton-results.json').read_text());b=r['cases']['nitrogen_four'];lines=[];checks={}
def add(s):lines.append(s)
def inp(n,v,u=''):add(f'¢` {n} = {v:.14g} {u} `')
def calc(n,e,v,u=''):add(f'¢` {n} = {e} = ?? {u} `');checks[n]=v
add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-13
---------------

# Nitrogen versus steam — closed Brayton cooler

13 October 2026. Exploratory comparison with the preserved [steam cycle](Steam%20Brayton%20cooler%20-%20Hurmet.md) and [fan/pump balance](Brayton%20fan%20and%20salt%20pump%20balance%20-%20Hurmet.md). No working fluid or cooling architecture has been adopted.

Nitrogen properties are calculated with CoolProp 7.2.0 HEOS using the [Span et al. nitrogen equation of state](https://coolprop.org/fluid_properties/fluids/Nitrogen.html). Water results are imported from the earlier HEOS water calculation. All quoted power figures are calculations, not manufacturer performance. The same compressor/turbine efficiencies of 85%/88%, 98% shaft transfer and 2% pressure loss across each exchanger are assumed. No recuperator or compressor intercooling is included.

## Like-for-like temperature comparison

Retain 560 K (286.85°C) heater inlet and 830 K (556.85°C) turbine inlet. Solve compressor-inlet temperature for each pressure ratio. Each case takes 10 MW heat from the salt. The first two cases also use identical 5→10 bar absolute compression pressures; the 4:1 nitrogen candidate uses 10→40 bar. Actual heater outlet/turbine inlet pressure is 2% below compressor discharge.

Air enters at 30°C and leaves at 130°C, with 500 Pa total air-system loss, 65% fan efficiency, 96% motor efficiency and 95% alternator efficiency. These are the same provisional electric-fan assumptions as the preceding balanced calculation.''')
keys=['steam_two','nitrogen_two_same_pressure','nitrogen_four']
add('| Per 10 MW heat input | Steam, 2:1 | Nitrogen, 2:1 | Nitrogen, 4:1 |\n| --- | --- | --- | --- |')
add('| Compressor pressures, bar absolute | 5→10 | 5→10 | 10→40 |')
for label,fn in [('Compressor inlet / cooler outlet, °C',lambda c:c['states']['compressor_inlet']['temperature_C']),('Turbine outlet / cooler inlet, °C',lambda c:c['states']['cooler_inlet']['temperature_C']),('Working-fluid mass flow, kg/s',lambda c:c['mass_kg_s']),('Compressor inlet volume, m³/s',lambda c:c['inlet_volume_m3_s']),('Surplus shaft power after compressor, kW',lambda c:c['available_shaft_W']/1000),('Air-cooler heat rejection, MW',lambda c:c['air_heat_W']/1e6),('Electricity after air fan, before salt pump, kW',lambda c:c['electric_after_fan_W']/1000),('Required ideal-counterflow UA, kW/K',lambda c:c['required_counterflow_UA_W_K']/1000)]:add('| '+label+' | '+' | '.join(f'{fn(r["cases"][k]):,.4g}' for k in keys)+' |')
add('''At 2:1 the power balances are almost identical. Nitrogen needs about twice the mass flow and about 25% more compressor-inlet volume at the same pressures. Thus simply substituting nitrogen does not inherently make the machinery smaller or increase the surplus.

Nitrogen's advantage is freedom to choose loop pressure and compressor-inlet temperature without steam condensation. Nitrogen's critical temperature is about 126 K, far below these cycle temperatures; no liquid-vapor transition occurs along these operating paths. At 4:1 the dry pressurized nitrogen trial gives more power with a readily air-coolable 84°C compressor inlet. The improvement combines a different pressure ratio and cold-end temperature; it is not an intrinsic factor-of-3.5 gain at identical cycle states.

## Absolute-pressure effect for 4:1 nitrogen''')
add('| Compressor pressures, bar absolute | Inlet volume per 10 MW, m³/s | Surplus shaft power, kW |\n| --- | --- | --- |')
for c in r['pressure_sensitivity']:
 p=c['inputs']['p_low_Pa']/1e5;add(f'| {p:g}→{4*p:g} | {c["inlet_volume_m3_s"]:.3f} | {c["available_shaft_W"]/1000:.1f} |')
add('''Raising charge pressure approximately reduces gas volume in inverse proportion while changing the calculated surplus only slightly. This is a way to reduce flow-passage sizes, with pressure containment and sealing tradeoffs; volume alone does not determine a compressor or turbine envelope.

## Why 8:1 needs a different comparison

At 10→80 bar and the same 287°C heater inlet, nitrogen would have to enter the compressor at **13.5°C**. This is below 30°C ambient and cannot be achieved by the proposed air cooler. Its formal positive shaft balance is rejected as an air-cooled operating case.

If compressor inlet is instead fixed at **45°C**, the 8:1 nitrogen compressor discharges at **346.1°C**. It can then absorb heat up to 556.85°C, but requires 42.39 kg/s per 10 MW and gives about **750 kW shaft surplus**, less than the 4:1 candidate's 944 kW. Its compressor inlet volume is about 4.00 m³/s and required ideal-counterflow cooler UA about 182 kW/K. This warmer-inlet case changes the generator temperature range and does not establish an optimum ratio. The preserved steam 8:1 trial at 5 kPa suction needs about 521 m³/s per 10 MW and has its own close cold-end approach to ambient.

## Air cooler and heat-exchanger consequences

The 4:1 nitrogen trial requires about **78.2 kW/K of counterflow UA per 10 MW**, versus **40.9 kW/K** for steam at 2:1. Although nitrogen rejects slightly less heat, its lower cooler outlet temperature reduces the temperature driving force. These values integrate real-fluid temperature against heat transfer, with linear pressure change and the assumed air heat capacity. All sampled counterflow temperature differences are positive for accepted cases. They are ideal-counterflow conductances, not selected surface areas or a verified pressure-drop design. Real flow arrangement, fouling and gas-side heat-transfer coefficients may increase the required area.

The existing generator also needs gas-side heat-transfer and pressure-drop checking for nitrogen; its water/steam service calculation and pressure rating do not establish nitrogen duty. A permanent nitrogen auxiliary loop would use its own gas inventory. Sharing the current steam-generator passages would require a defined water removal, purge, isolation and changeover arrangement; a separate salt-to-nitrogen exchanger is an alternative to assess, not selected here. Nitrogen avoids steam condensation management, but startup still needs an initial drive source and salt freeze protection remains necessary.

## A 30 MW-per-leg nitrogen trial

At 4:1 and 10→40 bar, scaling to 30 MW gives about **2.69 MW electrical surplus after the compressor**, with **182 kW** for the air fan and the previously calculated **130 kW** salt-pump demand (10 K salt drop; generator loss plus 50%). Approximately **2.38 MW remains**, versus 0.432 MW in the steam 2:1 case. Nitrogen circulation is about 100.45 kg/s and compressor-inlet volume 10.67 m³/s. The air cooler rejects 26.67 MW; electricity and machinery losses account for the balance and need their own destinations. This is machinery scaled to 30 MW, not the same 10 MW machine operated at triple capacity.

Two sensitivity checks at 4:1 retain positive surplus: lowering compressor/turbine efficiency to 80%/85% gives about 389 kW shaft surplus per 10 MW, and increasing each exchanger pressure loss to 5% gives about 631 kW. These are separate tests. Actual maps, combined adverse conditions and cooldown temperatures are not validated.

## Hurmet checks for the nitrogen 4:1 case

Thermodynamic states and the integrated cooler UA are imported from Python. Hurmet recalculates the cycle power and heat balance, fan demand and the 30 MW fan/pump margin. Changing pressure, temperature or machine efficiency requires rerunning the real-fluid solver; changing heat duty here only scales fixed-state machinery.''')
for n,v,u in [('HeatDuty',10,'MW'),('ShaftEfficiency',.98,''),('GeneratorEfficiency',.95,''),('FanEfficiency',.65,''),('MotorEfficiency',.96,''),('AirDensity',101325/(287.05*303.15),'kg/m3'),('AirHeatCapacity',1007,'J.kg-1.K-1'),('AirRise',100,'K'),('AirPressureDrop',500,'Pa'),('PumpAtThirtyMW',r['pump_30MW_electric_W']/1000,'kW')]:inp(n,v,u)
for n,k in [('HOne','compressor_inlet'),('HTwo','heater_inlet'),('HThree','turbine_inlet'),('HFour','cooler_inlet')]:inp(n,b['states'][k]['enthalpy_J_kg'],'J/kg')
s=b['specific']
for n,e,v,u in [('HeatPerMass','HThree - HTwo',s['heat_in_J_kg'],'J/kg'),('MassFlow','HeatDuty / HeatPerMass',b['mass_kg_s'],'kg/s'),('TurbinePower','MassFlow * (HThree - HFour)',b['turbine_W']/1000,'kW'),('CompressorPower','MassFlow * (HTwo - HOne)',b['compressor_W']/1000,'kW'),('SurplusPower','ShaftEfficiency * TurbinePower - CompressorPower',b['available_shaft_W']/1000,'kW'),('CoolerHeat','MassFlow * (HFour - HOne)',b['air_heat_W']/1e6,'MW'),('EnergyResidual','HeatDuty - CoolerHeat - TurbinePower + CompressorPower',0,'kW'),('AirFlow','CoolerHeat / (AirHeatCapacity * AirRise * AirDensity)',b['air_heat_W']/(1007*100)/(101325/(287.05*303.15)),'m3/s'),('FanPower','AirFlow * AirPressureDrop / (FanEfficiency * MotorEfficiency)',b['fan_electric_W']/1000,'kW'),('ElectricAfterFan','GeneratorEfficiency * SurplusPower - FanPower',b['electric_after_fan_W']/1000,'kW'),('MarginAtThirtyMW','3 * ElectricAfterFan - PumpAtThirtyMW',b['remaining_electric_30MW_W']/1000,'kW')]:calc(n,e,v,u)
add('''The last formula is specifically the 30 MW case when the normalization above is 10 MW; the fixed salt-pump input is not a pump scaling law. Summary tables are imported snapshots and do not update automatically in Hurmet.

## Reproduction

Run `nitrogen_brayton.py` with the project CoolProp environment, then `python publish_nitrogen_brayton.py`, and `node check_nitrogen_brayton.cjs` with the existing Hurmet/Temml engine paths. JSON preserves source hashes, all state points, air approaches, sensitivity cases, energy/entropy and duty-scaling checks. Hurmet verifies eleven named results after save/reopen and checks fan-pressure sensitivity. These checks establish numerical consistency, not a qualified cooling-system design.''')
t='\n\n'.join(lines)+'\n';t=re.sub(r'(?m)(^\|.*\|)\n\n(?=\|)',r'\1\n',t)
def widths(m):
 b=m.group(0);n=b.splitlines()[0].count('|')-1
 return b+'\n{.grid colWidths="'+' '.join(['250']+['125']*(n-1))+'"}'
t=re.sub(r'(?m)^\|.*(?:\n\|.*)*',widths,t)
write_worksheet(D/'Nitrogen versus steam Brayton - Hurmet.md', t)
(D/'nitrogen-hurmet-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
