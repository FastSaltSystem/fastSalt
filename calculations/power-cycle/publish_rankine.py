"""Publish imported cycle results as a Hurmet calculation summary and state tables.

Run rankine_cycle.py first, then this script, then the Hurmet round-trip check.
Steam properties and extraction fractions remain Python results, not Hurmet solves.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'rankine-results.json').read_text())
st=r['states'];work=r['specific_work']
lines=['''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Rankine cycle - preliminary heat balance

11 October 2026. Main-steam reheat and a provisional water-cooled condenser at
5 kPa absolute follow the owner's confirmed instructions. This is a first design
case, not a net plant rating or a turbine purchase specification. See [basis][1].

**Imported calculation boundary:** water properties, extraction fractions and
specific component duties below come from the companion Python/CoolProp model.
Hurmet recalculates flow scaling, output and condenser estimates from these
imported inputs. Changing steam pressures, temperatures, turbine efficiencies or
heater routing requires rerunning Python and regenerating this sheet. Changing
heat duty here scales the fixed cycle; it does not predict part-load performance.

The diagram is retained: HP turbine, reheater heated by a main-steam branch,
reheat/IP turbine, LP turbine, three LP heaters, deaerator, four HP heaters and a
steam-driven feed pump. The LP heater pressure is selected to close the deaerator
balance without an extra main-turbine extraction. Pressure assignments remain
provisional. No salt-heated reheater is added.

## Adopted state assumptions

| Parameter | Value | Origin/status |
| --- | --- | --- |
| Steam-generator duty | 1,500 MW total, three generators | Existing project target; all delivered to water in this case |
| Main steam | 24 MPa absolute, 830 K (556.85°C) | Existing generator worksheet |
| Return feedwater | 24 MPa absolute, 560 K (286.85°C) | Existing generator worksheet |
| Reheat | 4 MPa HP exhaust; 3.8 MPa after 5% loss; 470°C hot reheat | Provisional |
| Reheater heating-stream return | 24 MPa, 360°C, then throttled to highest HP heater | Provisional |
| Condenser | 5 kPa absolute; saturated-liquid hotwell | Owner-approved starting case |
| Deaerator | 0.6 MPa, saturated liquid | Provisional |
| Section isentropic efficiencies | HP 0.88; IP 0.90; LP 0.88; pump turbine 0.80 | Per modeled expansion interval, not guaranteed overall casing efficiency |
| Pump efficiencies | BFP 0.85; condensate pump 0.80 | Provisional |
| Shaft/generator efficiencies | 0.99 / 0.985 | Provisional |
| Feedwater-heater terminal difference | 5 K; saturated drains cascade to next heater | No separate drain-cooling zone |

At 24 MPa the heating stream does not undergo constant-pressure two-phase
condensation. The reheater is modeled using its full enthalpy/temperature curve;
its cooled high-pressure return is throttled into the highest HP heater.

## Imported state and cycle inputs

¢` format = "h7" `
''']
def inp(name,value,unit=''):
    lines.append(f'¢` {name} = {value:.12g} {unit} `\n')
def calc(name,expression,unit=''):
    lines.append(f'¢` {name} = {expression} = ?? {unit} `\n')
inp('ReactorDuty',1500,'MW');inp('GeneratorCount',3)
for name,val in [('MainEnthalpy',st['main']['h']),('FeedEnthalpy',st['feedwater']['h']),('HPwork',work['HP']),('IPwork',work['IP']),('LPwork',work['LP']),('BFPwork',work['BFP']),('CEPwork',work['CEP']),('CondenserHeat',r['condenser_specific_heat']),('ReheatGain',st['reheat_hot']['h']-st['reheat_cold']['h'])]:inp(name,val,"'J/kg'")
inp('ReheatFraction',r['fractions']['reheat']);inp('ReheatedFraction',r['reheat_flow']/r['mass']);inp('LPExhaustFraction',r['exhaust_mass']/r['mass']);inp('PumpTurbineFraction',r['fractions']['pump_turbine'])
inp('ShaftEfficiency',.99);inp('GeneratorEfficiency',.985);inp('CEPMotorEfficiency',.96)
lines.append('## Heat, flow and power\n')
calc('TotalSteam','ReactorDuty / (MainEnthalpy - FeedEnthalpy)',"'kg/s'")
calc('PerGeneratorSteam','TotalSteam / GeneratorCount',"'kg/s'")
calc('ReheaterSupply','TotalSteam * ReheatFraction',"'kg/s'")
calc('ReheatedSteam','TotalSteam * ReheatedFraction',"'kg/s'")
calc('ReheatDuty','ReheatedSteam * ReheatGain','MW')
calc('PumpTurbineSteam','TotalSteam * PumpTurbineFraction',"'kg/s'")
calc('LPExhaustSteam','TotalSteam * LPExhaustFraction',"'kg/s'")
calc('HPIPGross','TotalSteam * (HPwork + IPwork) * ShaftEfficiency * GeneratorEfficiency','MW')
calc('LPGross','TotalSteam * LPwork * ShaftEfficiency * GeneratorEfficiency','MW')
calc('GrossElectric','HPIPGross + LPGross','MW')
calc('GrossEfficiency','GrossElectric / ReactorDuty')
calc('BFPShaft','TotalSteam * BFPwork','MW')
calc('CEPElectric','TotalSteam * CEPwork / CEPMotorEfficiency','MW')
calc('CondenserDuty','TotalSteam * CondenserHeat','MW')
lines.append('''The feed-pump turbine extraction already pays for BFP shaft power in the turbine
flow balance. Do **not** subtract BFP shaft power again from electrical generation.
Net export remains uncalculated: salt pumps, cooling-water pumps, cooling-system
fans, services, transformer losses and other station loads still need a load list.
No 600 MWe net-output claim is established by this gross result.

## Conditional condenser estimate

Cooling water at 20°C inlet and 28°C outlet is a provisional design case, not
site weather data. The total heat-transfer coefficient is an assumed 2.5 kW/(m² K),
not a selected condenser performance guarantee. The area below excludes design
margin and explicit fouling/air-removal allowances. Cooling-system head, pump
power, water supply and final heat sink remain open.
''')
inp('CondensingT',st['condenser']['t'],'K');inp('CoolingIn',293.15,'K');inp('CoolingOut',301.15,'K');inp('WaterHeatCapacity',4180,"'J.kg-1.K-1'");inp('WaterDensity',998,"'kg/m3'");inp('CondenserU',2500,"'W.m-2.K-1'")
calc('CoolingMass','CondenserDuty / (WaterHeatCapacity * (CoolingOut - CoolingIn))',"'kg/s'")
calc('CoolingVolume','CoolingMass / WaterDensity',"'m3/s'")
calc('ColdApproach','CondensingT - CoolingIn','K');calc('HotApproach','CondensingT - CoolingOut','K')
calc('CondenserLMTD','(ColdApproach - HotApproach) / ln(ColdApproach / HotApproach)','K')
calc('CondenserArea','CondenserDuty / (CondenserU * CondenserLMTD)',"'m2'")
lines.append(f'''## Feasibility checks and open decisions

- The linear heater/reheater/pump balances close to {r['balance_residual']:.3g} J per kg of main flow; whole-cycle first-law residual is {r['energy_residual']:.3g} J/kg.
- The reheater's 401-point counterflow check gives **{r['pinch']:.2f} K** minimum approach at 470°C reheat. A 500°C trial gives **{r['rejected_500C_case']['minimum_approach_K']:.2f} K** and is rejected for temperature crossover. This is thermodynamic screening, not heat-exchanger sizing.
- LP exhaust moisture is **{100*r['moisture']:.2f}% by mass** under the equilibrium-property model. Acceptable wetness, blade erosion, moisture separation and actual turbine performance require review; no universal allowable is assumed.
- The supercritical generator main-flow result differs slightly from the older property table: {r['mass']:.3f} kg/s versus 711.561 kg/s. Existing pipe geometry has not been revised for this small property-source difference.
- Condensate-pump discharge is 1.2 times deaerator pressure. All other feedwater and main-steam line losses, except the 5% cold-reheat allowance, are omitted. BFP and turbine work must be revised when pressure budgets are assigned.

## Condenser-pressure sensitivity

Each case recloses the deaerator heater balance; reheat temperature is held fixed.

| Condenser absolute pressure | Gross electrical power | Condenser duty | LP moisture |
| --- | --- | --- | --- |
''')
for case in r['sensitivity']:lines.append(f"| {case['condenser_kPa']:.1f} kPa | {case['gross_MW']:.1f} MW | {case['condenser_MW']:.1f} MW | {case['exhaust_moisture_percent']:.2f}% |")
lines+=['\n## References\n','[1]: README.md','[2]: https://coolprop.org/fluid_properties/fluids/Water.html','[3]: rankine-states.csv','\nThe imported steam properties use [CoolProp water / IAPWS-95][2], version '+r['property_library']['version']+'. The [state table][3], solver, extraction fractions, provenance hash and reproduction steps are kept alongside this worksheet.']
# Hurmet's table serializer does not accept these ordinary Markdown tables.
# Keep this worksheet portable using prose lists; the companion basis has tables.
text='\n'.join(lines)+'\n'
rows=[]
for line in text.splitlines():
    if line.startswith('|'):
        parts=[q.strip() for q in line.strip('|').split('|')]
        if parts[0] in ('Parameter','Condenser absolute pressure','---'):continue
        if len(parts)==3:rows.append('- **'+parts[0]+':** '+parts[1]+'. '+parts[2]+'.')
        else:rows.append('- '+parts[0]+': gross '+parts[1]+', condenser '+parts[2]+', LP moisture '+parts[3]+'.')
    else:rows.append(line)
(ROOT/'Rankine cycle - Hurmet.md').write_text('\n'.join(rows)+'\n')
print('Wrote Hurmet source; run check_rankine_hurmet.cjs to recalculate and save.')
