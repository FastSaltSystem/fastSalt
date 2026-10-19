"""Publish imported real-steam states and editable Hurmet heat-duty scaling."""
from pathlib import Path
import json,re
D=Path(__file__).resolve().parent
r=json.loads((D/'brayton-cooler-results.json').read_text());b=r['base'];eight=r['high_ratio'];lines=[];checks={}
def add(x):lines.append(x)
def inp(n,v,u=''):add(f'¢` {n} = {v:.13g} {u} `')
def calc(n,expr,v,u=''):add(f'¢` {n} = {expr} = ?? {u} `');checks[n]=v
add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-12
---------------

# Steam Brayton auxiliary cooler — preliminary screen

12 October 2026. Exploratory calculation requested by the project owner, not an adopted cooling-system design. The purpose is to determine whether a non-condensing steam loop can power its compressor and reject substantial heat to air.

The [current generator worksheet](../steam-generator/Generator%20sizing%20-%20Hurmet.md) uses **560 K (286.85°C) inlet and 830 K (556.85°C) outlet**, rather than the approximately 260°C recalled in discussion. Those temperature endpoints are retained. Normal steam-plant pressure is **not** retained: the auxiliary trial compresses steam from **5 to 10 bar absolute**. At the normal 24 MPa and 560 K, water is liquid-like, not the vapor required by this trial. Using the existing generator in this mode would require an isolated, lower-pressure operating arrangement; it cannot be connected directly to live 24 MPa headers.

Steam enthalpies, temperatures, density and sensitivity results below are imported from [brayton_cooler.py](brayton_cooler.py), using CoolProp 7.2.0 HEOS water / IAPWS-95. Hurmet recalculates duty scaling and the fan allowance; it does not solve the steam properties. Changing cycle temperatures, pressures or component efficiencies requires rerunning Python and this publisher, then the Hurmet checker.

## Trial assumptions

- Compressor pressure ratio: 2.0.
- Compressor/turbine isentropic efficiencies: 85% / 88%; assumptions requiring equipment confirmation.
- Shaft power transfer efficiency: 98%.
- Steam-side pressure loss: 2% across each exchanger, including its associated piping allowance.
- Heat input: 10 MW for convenient scaling, not a selected decay-heat duty.
- No recuperator, condensation or feedwater pump.

## Calculated cycle states

| Point | Temperature °C | Pressure bar absolute |
| --- | --- | --- |''')
for key,label in [('compressor_inlet','Air-cooler outlet / compressor inlet'),('steam_generator_inlet','Compressor outlet / generator inlet'),('turbine_inlet','Generator outlet / turbine inlet'),('air_cooler_inlet','Turbine outlet / air-cooler inlet')]:
 s=b['states'][key];add(f"| {label} | {s['temperature_C']:.1f} | {s['pressure_Pa']/1e5:.3f} |")
add('The compressor inlet is about 40 K above saturation at 5 bar. Sampled heat-exchanger and actual/isentropic machine paths remain dry. This is a steady-state check; shutdown condensation and restart inventory are not analyzed.')
add('## Editable duty scaling')
add('¢` format = "h7" `')
inp('HeatInput',10,'MW')
for n,key in [('hA','compressor_inlet'),('hB','steam_generator_inlet'),('hC','turbine_inlet'),('hD','air_cooler_inlet')]:inp(n,b['states'][key]['enthalpy_J_kg']/1000,"'kJ/kg'")
inp('ShaftEfficiency',.98)
calc('SteamFlow','HeatInput / (hC - hB)',b['steam_flow_kg_s'],"'kg/s'")
calc('TurbinePower','SteamFlow * (hC - hD)',b['turbine_power_W']/1e6,'MW')
calc('CompressorPower','SteamFlow * (hB - hA)',b['compressor_power_W']/1e6,'MW')
calc('ShaftLoss','TurbinePower * (1 - ShaftEfficiency)',b['shaft_losses_W']/1e6,'MW')
calc('AvailablePower','TurbinePower - CompressorPower - ShaftLoss',b['available_shaft_W']/1000,'kW')
calc('AirCoolerDuty','SteamFlow * (hD - hA)',b['heat_rejected_air_cooler_W']/1e6,'MW')
calc('EnergyResidual','HeatInput - AirCoolerDuty - TurbinePower + CompressorPower',0,'MW')
inp('InletDensity',b['states']['compressor_inlet']['density_kg_m3'],"'kg/m3'")
calc('InletVolumeFlow','SteamFlow / InletDensity',b['compressor_inlet_volume_m3_s'],"'m3/s'")
add('Available power is after compressor and shaft losses, before air fans, salt pumps and other auxiliaries. If remaining shaft power is ultimately dissipated within the cooling installation, the total environmental heat release approaches the full heat input. The air-cooler duty shown is only the steam-to-air exchanger duty. The turbine transfers approximately 3.52 MW internally to remove 10 MW of reactor heat; this is a multi-megawatt machine despite its small net output.')
add('## Illustrative air-fan allowance')
add('Use 30°C incoming air, a 100 K rise, 500 Pa air-path loss and 65% fan efficiency. These are placeholders, not a designed air cooler. Fan power uses inlet-air volume and assumes direct shaft drive; gearing or electrical conversion would add losses.')
a=b['illustrative_air']
inp('AirCp',1007,"'J.kg-1.K-1'");inp('AirRise',100,'K');inp('AirDensity',a['density_inlet_kg_m3'],"'kg/m3'");inp('AirPressureDrop',500,'Pa');inp('FanEfficiency',.65)
calc('AirFlow','AirCoolerDuty / (AirCp * AirRise)',a['mass_kg_s'],"'kg/s'")
calc('FanPower','AirFlow / AirDensity * AirPressureDrop / FanEfficiency',a['fan_power_W']/1000,'kW')
calc('RemainingPower','AvailablePower - FanPower',b['after_illustrative_fan_W']/1000,'kW')
add('The remaining approximately 203 kW per 10 MW heat input is an allowance for unspecified loads, not proof that the whole cooling system is self-powered. In particular, the existing salt-circulation pumps are not included.')
add('## Sensitivity — external real-steam calculations')
add('| Compressor / turbine efficiency | Pressure ratio | Available shaft kW per 10 MW heat input |\n| --- | --- | --- |')
for q in r['efficiency_ratio_trials']:
 d=q['result'];value=f"{d['available_shaft_W']/1000:.0f}" if d['state_solution_valid'] else 'Wet inlet required — rejected'
 add(f"| {q['eta_c']*100:.0f}% / {q['eta_t']*100:.0f}% | {q['ratio']:.1f} | {value} |")
add('Available shaft power is before fan and salt-pump loads. These are different fixed-temperature trial designs, not performance along one machine map. At ratio 2.5 and the base efficiencies, positive margin increases but compressor-inlet superheat decreases. Ratio 3 at 5 bar suction requires a wet inlet for the specified generator inlet temperature and is rejected.')
add('| Pressure loss in each exchanger | Available shaft kW per 10 MW |\n| --- | --- |')
for q in r['pressure_loss_trials']:add(f"| {q['loss']*100:.0f}% | {q['result']['available_shaft_W']/1000:.0f} |")
add('At 5% loss in each exchanger, the base 2:1 trial cannot drive its own compressor. Low pressure loss is a key feasibility condition.')
add('## Requested 8:1 comparison')
add('At the same 5 bar suction pressure, 8:1 compression cannot retain a 287°C compressor outlet with dry steam at the inlet. A vapor-only trial can retain the generator temperatures by reducing suction pressure to 0.05 bar absolute (5 kPa), with compressor discharge at 0.40 bar. Both sides of this trial are below atmospheric pressure; vacuum integrity and air ingress become additional requirements.')
add('| Quantity, per 10 MW heat input | 2:1 trial | 8:1 vacuum trial |\n| --- | --- | --- |')
for label,v2,v8,unit in [
 ('Compressor inlet pressure',5,.05,'bar absolute'),
 ('Compressor discharge pressure',10,.4,'bar absolute'),
 ('Compressor inlet temperature',b['states']['compressor_inlet']['temperature_C'],eight['states']['compressor_inlet']['temperature_C'],'°C'),
 ('Generator inlet temperature',286.85,286.85,'°C'),
 ('Generator outlet temperature',556.85,556.85,'°C'),
 ('Turbine outlet temperature',b['states']['air_cooler_inlet']['temperature_C'],eight['states']['air_cooler_inlet']['temperature_C'],'°C'),
 ('Steam flow',b['steam_flow_kg_s'],eight['steam_flow_kg_s'],'kg/s'),
 ('Compressor inlet volume flow',b['compressor_inlet_volume_m3_s'],eight['compressor_inlet_volume_m3_s'],'m³/s'),
 ('Turbine power',b['turbine_power_W']/1e6,eight['turbine_power_W']/1e6,'MW'),
 ('Compressor power',b['compressor_power_W']/1e6,eight['compressor_power_W']/1e6,'MW'),
 ('Available shaft power',b['available_shaft_W']/1e6,eight['available_shaft_W']/1e6,'MW'),
 ('Steam-to-air cooler duty',b['heat_rejected_air_cooler_W']/1e6,eight['heat_rejected_air_cooler_W']/1e6,'MW')]:
 add(f'| {label} ({unit}) | {v2:.3g} | {v8:.3g} |')
add('Efficiencies and fractional pressure-loss assumptions are the same in both trials. The 8:1 case gives more shaft surplus but about 72 times the compressor-inlet volume flow. Its air-cooler outlet is only about 45°C, with 12 K superheat above saturation and about 15 K approach to the assumed 30°C incoming air. Hot-weather performance, vacuum operation and very large passages are unverified. A 2% cooler pressure allowance is only about 102 Pa in this vacuum trial; that must not be assumed achievable in the existing equipment.')
add('### Editable scaling for the 8:1 trial')
for n,key in [('hEightA','compressor_inlet'),('hEightB','steam_generator_inlet'),('hEightC','turbine_inlet'),('hEightD','air_cooler_inlet')]:inp(n,eight['states'][key]['enthalpy_J_kg']/1000,"'kJ/kg'")
calc('EightFlow','HeatInput / (hEightC - hEightB)',eight['steam_flow_kg_s'],"'kg/s'")
calc('EightTurbinePower','EightFlow * (hEightC - hEightD)',eight['turbine_power_W']/1e6,'MW')
calc('EightCompressorPower','EightFlow * (hEightB - hEightA)',eight['compressor_power_W']/1e6,'MW')
calc('EightAvailable','ShaftEfficiency * EightTurbinePower - EightCompressorPower',eight['available_shaft_W']/1000,'kW')
calc('EightCoolerDuty','EightFlow * (hEightD - hEightA)',eight['heat_rejected_air_cooler_W']/1e6,'MW')
inp('EightDensity',eight['states']['compressor_inlet']['density_kg_m3'],"'kg/m3'")
calc('EightVolumeFlow','EightFlow / EightDensity',eight['compressor_inlet_volume_m3_s'],"'m3/s'")
calc('EightFanPower','EightCoolerDuty / (AirCp * AirRise) / AirDensity * AirPressureDrop / FanEfficiency',eight['illustrative_air']['fan_power_W']/1000,'kW')
calc('EightRemaining','EightAvailable - EightFanPower',eight['after_illustrative_fan_W']/1000,'kW')
add('## Normal 24 MPa supply and throttling')
add('The owner notes that normal 24 MPa steam provides ample pressure for a lower-pressure engine. Throttling can charge or feed a lower-pressure system, but continuously returning steam to a generator held at 24 MPa still requires recompression to that pressure, or condensation and liquid pumping. The isolated low-pressure closed cycles above do not include a continuously supplied 24 MPa branch. A one-time high-pressure charge also does not supply continuing shaft work.')
add('An adiabatic throttle approximately conserves enthalpy rather than temperature. With real steam at 24 MPa and 557°C, throttling to 1 MPa produces about 451°C steam; throttling to 0.04 MPa produces about 445°C. Thus a continuously throttled supply cannot be represented by simply retaining 557°C at the lower pressure without adding heat. These throttle results are separate from the lower-pressure heated-loop trials. Saturation/phase conditions at 24 MPa and the current 287°C generator inlet also prevent treating the normal feedwater state as dry steam.')
add('''## Checks, sources and unresolved work

Python verifies energy closure, nonnegative machine entropy production, inverse compressor closure, dry sampled paths and linear heat-duty scaling. HEOS state enthalpies agree with an IF97 property cross-check within 0.003%. Hurmet independently checks the power and fan arithmetic and duty/fan-loss sensitivities. Detailed inputs and results are in [the JSON report](brayton-cooler-results.json).

The UM report *Core Design Evolution of Wielenga Innovation Salt Tank Reactor*, November 15, 2025, section 3.3.1 and Table 3 (printed pages 21–22; PDF pages 37–38), gives 675 K (approximately 402°C) for the selected NaCl–KCl–MgCl2 coolant melting point. The inherited generator worksheet instead contains 674 K; the one-degree difference is immaterial for this screen. The [local UM report](</Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Papers and Presentations/UMReport/Evolution_of_WISSR_design 2.pdf>) remains the reference for the approximately 402°C value. No cutoff temperature is selected here.

- [CoolProp water property formulation](https://coolprop.org/fluid_properties/fluids/Water.html).
- [NASA compressor/turbine matching](https://www.grc.nasa.gov/WWW/K-12/BGP/ctmatch.html).
- Generator heat-transfer area, vapor distribution, salt flow, tube-wall temperature and freezing protection are not solved. At this lower duty the original full-power salt temperature drop must not simply be reused.
- The 2% pressure-loss assumptions and component efficiencies require checking against generator pressure drop and practical machine maps.
- Air-cooler area, salt-pump power, startup, restart, steam inventory, turndown and shutdown response remain open. A temperature cutoff is a control concept, not yet a demonstrated freeze-protection function.
- No change to the main Rankine cycle, reactor cooling architecture or Blender model is adopted by this calculation.

Reproduce with the existing power-cycle requirements: `python brayton_cooler.py`, then `python publish_brayton_cooler.py`, then `HURMET_ENGINE=/path/to/hurmet.cjs TEMML_ENGINE=/path/to/temml.cjs node check_brayton_hurmet.cjs`. Changing only HeatInput or the air-fan assumptions in Hurmet recalculates the scaling at the imported cycle states.
''')
text=re.sub(r'(?m)(^\|.*\|)\n\n(?=\|)', r'\1\n', '\n\n'.join(lines)+'\n')
def table_widths(match):
 block=match.group(0);count=block.splitlines()[0].count('|')-1
 widths=' '.join(['240']+['120']*(count-1))
 return block+'\n{.grid colWidths="'+widths+'"}'
text=re.sub(r'(?m)^\|.*(?:\n\|.*)*',table_widths,text)
(D/'Steam Brayton cooler - Hurmet.md').write_text(text)
(D/'brayton-hurmet-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
