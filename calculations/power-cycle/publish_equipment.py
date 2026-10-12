"""Publish editable Hurmet sizing equations; imported property/profile boundaries explicit."""
from pathlib import Path
import json,sys
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
r=json.loads((ROOT/'equipment-sizing.json').read_text());c=r['condenser'];rh=r['reheater'];t=r['turbines'];da=r['deaerator'];p=r['pumps'];lines=[];expected={}
def para(s):lines.append(s+'\n')
def inp(n,v,u=''):lines.append(f'¢` {n} = {v:.12g} {u} `\n')
def calc(n,e,u='',v=None):
 lines.append(f'¢` {n} = {e} = ?? {u} `\n')
 if v is not None:expected[n]=v
para('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Power-plant equipment sizing — preliminary

11 October 2026. Sizes supported by the selected 1,500 MWt cycle: exchanger surface, flow passages, storage inventory, pump duties and generator capacity. This is a preliminary equipment study for the layout, not selected manufactured equipment or a pressure-boundary design.

**Basis:** D-026 / `reheat-selection.json`, exactly 5 kPa reference; 24 MPa / 556.85°C main steam, 510°C reheat. Pressures are absolute. Existing performance, piping walls and Blender geometry are not overwritten. The higher pump discharge pressures proposed below require a new coupled heat balance before updating the 679 MW gross result or extraction flows.

**Imported boundary:** CoolProp 7.2.0 water densities and pump enthalpy increments, turbine work, flow fractions and integrated exchanger UA are external Python results. Hurmet executes the equations for volumes, bores, areas, inventory, capacity and power from those imports. A pressure/temperature/cycle change requires rerunning Python. The source hashes and detailed checks are in `equipment-sizing.json`; [method and limitations](equipment-sizing-notes.md).

¢` format = "h7" `
''')
inp('Gravity',9.80665,"'m/s2'")
inp('Pi',3.141592653589793)
para('## 1. Reheater surface and module count\n\nAssume U = 1,000 W/(m² K) and a 20% surface allowance. U is an editable sensitivity input, not a demonstrated coefficient. The integrated UA retains the nonlinear supercritical heating-stream profile and 20.3 K minimum local approach. Four modules are a provisional layout division, all operating, not standby capacity.')
inp('ReheatUA',rh['UA_W_K'],"'W/K'");inp('ReheatU',1000,"'W.m-2.K-1'");inp('SurfaceFactor',1.2);inp('ReheatModules',4);inp('ReheatDuty',rh['duty_MW'],'MW')
calc('ReheatArea','SurfaceFactor * ReheatUA / ReheatU',"'m2'",rh['area_m2']);calc('ReheatModuleArea','ReheatArea / ReheatModules',"'m2'",rh['area_per_module_m2']);calc('ReheatModuleDuty','ReheatDuty / ReheatModules','MW',rh['duty_per_module_MW'])
para(f"At U = 500 / 1,000 / 1,500 W/(m² K), required areas including the allowance are **16,359 / 8,179 / 5,453 m²**. At the middle case each of four modules contains approximately {rh['tubes_per_module']:,} tubes, 25.4 mm OD × 12 m effective length. The equivalent packed bundle diameter is {rh['bundle_eq_diameter_m']:.2f} m at 1.25D triangular pitch and 70% bundle utilization. Reserve **16 × 3 × 3 m per module**, plus 13 m withdrawal space. These dimensions are packing-based placeholders; tube wall, manifolds, 24 MPa pressure boundary, shell-side velocity, vibration and pressure drop are not yet designed.")
para('## 2. Condenser\n\nKeep the surface used in the accepted cooling cases; do not silently change its pressure/performance map. It rejects 804 MW at the exact 5 kPa reference, 826 MW at 30°C water inlet and 838 MW at 35°C. Three equal condenser modules are a layout option. U = 2,500 W/(m² K) remains an unverified effective assumption with no separately established fouling allowance. A 20% extra-area option would be 46,216 m² and needs a revised cooling/control check.')
inp('CondenserAreaRequired',c['reference_area_m2'],"'m2'");inp('CondenserModules',3);inp('CondenserTubeOD',.0254,'m');inp('CondenserTubeID',.0234,'m');inp('CondenserTubeLength',12,'m');inp('CondenserPasses',2);inp('CondenserTubeCount',c['tubes_per_module']);inp('CoolingFlow',c['water_m3_s'],"'m3/s'")
calc('CondenserAreaProvided','CondenserModules * CondenserTubeCount * Pi * CondenserTubeOD * CondenserTubeLength',"'m2'",c['provided_area_m2'])
calc('CondenserTubeVelocity','(CoolingFlow / CondenserModules) / ((CondenserTubeCount / CondenserPasses) * Pi * CondenserTubeID^2 / 4)',"'m/s'",c['tube_water_velocity_m_s'])
para(f"Each module has **{c['tubes_per_module']:,} tubes**, two passes, 12 m effective length; total {c['total_tubes']:,} tubes. The 23.4 mm ID is a provisional hydraulic geometry, not a verified material/wall choice. Calculated water velocity is {c['tube_water_velocity_m_s']:.2f} m/s. A smooth-tube Darcy estimate (1.5 µm roughness, K=4, 24 m flow length) gives {c['tube_loss_head_m']:.1f} m head before external piping and final water-box losses. A packed tube section is {c['bundle_cross_section_m2']:.1f} m² per module, equivalent to {c['bundle_eq_diameter_m']:.2f} m circular diameter. Reserve **16 × 7 × 9 m per module** including provisional water-box, steam-space and hotwell allowance, plus **13 m tube withdrawal**. This reserve is not a final shell dimension; vacuum buckling, inlet-neck area, air removal and lifting are unresolved.")
inp('CoolingMainCount',2);inp('CoolingMainBore',2.25,'m');inp('CoolingBranchBore',2,'m')
calc('CoolingMainVelocity','CoolingFlow / (CoolingMainCount * Pi * CoolingMainBore^2 / 4)',"'m/s'",c['water_m3_s']/(2*3.141592653589793*2.25**2/4))
calc('CoolingBranchVelocity','(CoolingFlow / CondenserModules) / (Pi * CoolingBranchBore^2 / 4)',"'m/s'",c['water_m3_s']/(3*3.141592653589793))
para('Use two 2.25 m bore parallel mains **for each of supply and return**, and one 2.0 m bore supply/return pair per condenser module. These are internal bores; wall, burial/support and water-hammer design are separate. The final heat sink/tower size cannot be established without an ambient/water-source basis; 838 MW is the largest rejection load among the accepted full-load cases.')
para('## 3. Turbines and generators\n\nThe source diagram has HP/IP and LP generator groups. These capacity estimates retain that grouping. Mechanical turbine dimensions cannot be selected from MW alone.')
inp('HPIPelectric',t['HP_IP_electrical_MW'],'MW');inp('LPelectric',t['electrical_MW']['LP'],'MW');inp('PowerFactor',.9);inp('GeneratorMargin',1.1)
# Hurmet VA may differ in units: MVA is expressed explicitly via a numeric MW input.
inp('HPIP_MW_number',t['HP_IP_electrical_MW']);inp('LP_MW_number',t['electrical_MW']['LP'])
calc('HPIP_MVA_number','HPIP_MW_number * GeneratorMargin / PowerFactor','',t['HP_IP_generator_min_MVA']);calc('LP_MVA_number','LP_MW_number * GeneratorMargin / PowerFactor','',t['LP_generator_min_MVA'])
para('The last two numeric results are MVA. Reserve **500 MVA HP/IP and 350 MVA LP generators**, using 0.90 power factor and 10% capacity margin. The respective calculated outputs are 398.25 and 280.48 MWe. Generator cooling, fault capability, excitation and grid requirements remain unresolved.')
inp('ExhaustMass',t['LP_exhaust_mass_kg_s'],"'kg/s'");inp('ExhaustDensity',t['LP_exhaust_mass_kg_s']/t['LP_exhaust_volume_m3_s'],"'kg/m3'");inp('AxialVelocity',180,"'m/s'");inp('ExhaustFlows',6);inp('HubTipRatio',.5)
calc('ExhaustVolume','ExhaustMass / ExhaustDensity',"'m3/s'",t['LP_exhaust_volume_m3_s']);calc('TotalAnnulus','ExhaustVolume / AxialVelocity',"'m2'",t['annuli'][1]['annulus_total_m2']);calc('TipDiameter','sqrt(4 * TotalAnnulus / (ExhaustFlows * Pi * (1 - HubTipRatio^2)))','m',t['annuli'][1]['tip_diameter_m']);calc('BladeLength','TipDiameter * (1 - HubTipRatio) / 2','m',t['annuli'][1]['blade_length_m'])
para('At 180 m/s assumed axial speed and hub/tip ratio 0.5, four / six / eight exhaust flows imply tip diameters **4.67 / 3.81 / 3.30 m** and blade lengths **1.17 / 0.95 / 0.83 m**. Six flows, provisionally three double-flow LP casings, are a useful layout candidate. This is a continuity screen using homogeneous wet-steam density, not a blade/rotor design or supplier choice; axial velocity, speed, stress, blockage, exhaust losses, wetness and annulus geometry must be determined together. Do not interpret 3.81 m as casing OD or an exhaust-pipe size.')
para('## 4. Closed feedwater heaters\n\nHot and cold duties close for each heater including cascading drains. The area model ideally pre-mixes incoming bleed and throttled drains at shell pressure, then integrates a countercurrent temperature profile. This is an area proxy, not a three-zone design. U = 2,000 W/(m² K), with 20% surface allowance, is assumed for every heater; no correlation or fouling allowance has been verified. Final desuperheating/condensing/drain zones, feed-side velocity, number of shells, pressure walls and extraction nozzles may change these estimates.')
para('| Heater | Duty MW | Bleed kg/s | Shell MPa | Area m² at assumed U |\n| --- | ---: | ---: | ---: | ---: |')
for h in r['heaters']:lines.append(f"| {h['name']} | {h['duty_MW']:.1f} | {h['bleed_kg_s']:.2f} | {h['shell_MPa']:.3f} | {h['area_m2']:,.0f} |")
para('\nEditable area calculations (UA imported from the detailed thermal profiles):');inp('HeaterU',2000,"'W.m-2.K-1'")
for h in r['heaters']:
 inp(h['name']+'UA',h['UA_W_K'],"'W/K'");calc(h['name']+'Area',f"SurfaceFactor * {h['name']}UA / HeaterU","'m2'",h['area_m2'])
para('At U = 1,000 the areas double; at 3,000 they are two-thirds of the listed values. Large LP extraction volumes favor short, direct connections near the turbine. These heater thermal areas do not yet define shell dimensions.')
para('## 5. Pumps and elevation\n\nProvisionally use three 50% pumps per service: two operating, one standby. This is an analyst-selected availability/layout assumption. Driver margins do not guarantee pump curves or startup capability. Pressure losses below are budgets, not measured losses. Existing cycle fractions and gross output are frozen until reclosure.')
inp('MainMass',da['flow_kg_s'],"'kg/s'");inp('DADensity',da['water_density_kg_m3'],"'kg/m3'");calc('FeedPumpFlow','MainMass / DADensity',"'m3/s'",da['flow_m3_s'])
inp('BFPspecificWork',p['feedwater']['shaft_MW']*1e6/da['flow_kg_s'],"'J/kg'");calc('BFPshaft','MainMass * BFPspecificWork','MW',p['feedwater']['shaft_MW']);calc('BFPshaftEach','BFPshaft / 2','MW',p['feedwater']['per_duty_shaft_MW'])
para('**Feedwater:** 26.5 MPa discharge, 0.6 MPa suction, about 2,907 m pressure head; 85% hydraulic efficiency. The 2.5 MPa above main-turbine inlet pressure budgets 0.4 MPa main-steam piping, 1.5 MPa generator, 0.4 MPa heaters and 0.2 MPa feedwater piping. This also implies SG steam pressure above the earlier 24 MPa value. Each duty pump carries 0.392 m³/s and about 11.85 MW shaft; reserve a **15 MW driver per pump**. Steam drive remains the working preference, with electric startup/backup unresolved. Total shaft duty rises by **2.28 MW** relative to the frozen cycle; the feed-pump turbine and its heater bleeds must be rebalanced before adopting the new pressures.')
inp('BFP_NPSHr',8,'m');inp('BFP_NPSHmargin',3,'m');inp('BFP_suction_loss',2,'m');calc('BFP_min_level','BFP_NPSHr + BFP_NPSHmargin + BFP_suction_loss','m',13)
para('Saturated deaerator water has no pressure-above-vapor-pressure cushion. With assumed NPSHr=8 m, 3 m margin and 2 m suction loss, the minimum water level must be 13 m above the pump datum; reserve **14 m** for layout. All three quantities require pump/suction-line verification. A booster pump is an alternative to the elevated storage arrangement.')
inp('DApressure',.6,'MPa');inp('DAlevel',14,'m');inp('CondensateDensity',995.0002,"'kg/m3'");inp('LPHeaterLoss',.1,'MPa');inp('CondensateLineLoss',.05,'MPa')
calc('CondensatePressureRequired','DApressure + CondensateDensity * Gravity * DAlevel + LPHeaterLoss + CondensateLineLoss','MPa',p['condensate']['required_pressure_MPa'])
para(f"**Condensate:** 1.0 MPa discharge is a provisional replacement for 0.72 MPa. The elevation and loss budget alone require {p['condensate']['required_pressure_MPa']:.3f} MPa. Total flow {p['condensate']['flow_m3_s']:.3f} m³/s; total electrical load {p['condensate']['electric_MW']:.3f} MW at 80% hydraulic / 96% motor efficiency; reserve **355 kW per motor**. A vertical-can arrangement with hotwell level 4 m above the first-stage datum allows 2 m assumed NPSHr + 1 m suction loss + 1 m margin. Actual NPSHr, hotwell levels and transients are unresolved.")
inp('CoolingDensity',998,"'kg/m3'");inp('CoolingHead',20,'m');inp('CoolingPumpEfficiency',.88);inp('MotorEfficiency',.96)
calc('CoolingPumpElectric','CoolingDensity * Gravity * CoolingFlow * CoolingHead / (CoolingPumpEfficiency * MotorEfficiency)','MW',p['cooling_water']['electric_MW']);calc('CoolingPumpEach','CoolingPumpElectric / 2','MW',p['cooling_water']['electric_MW']/2)
para('**Cooling water:** at an assumed 20 m total head, total operating electrical load is 5.51 MW. Each duty pump carries 11.88 m³/s; reserve **3.5 MW per motor**. At 15 / 20 / 30 m head, total load is 4.13 / 5.51 / 8.26 MW; the proposed motors do not cover the 30 m case. The condenser tube estimate consumes about 9.2 m of the 20 m budget. Source/tower elevation, piping and intake losses must complete the budget. These are service loads, not a complete net-power estimate; do not subtract steam-driven BFP work twice.')
para('## 6. Deaerator storage\n\nAssume ten minutes usable inventory at full feedwater flow. This is a project planning choice, not a code requirement. Usable volume is the operating drawdown range, not the volume to the top of the tank.')
inp('StorageTime',600,'s');inp('StorageVessels',2);inp('StorageDiameter',4.5,'m');inp('StorageLength',22,'m');inp('UsableFraction',.7)
calc('StorageRequired','FeedPumpFlow * StorageTime',"'m3'",da['usable_required_m3']);calc('StorageGross','StorageVessels * Pi * StorageDiameter^2 * StorageLength / 4',"'m3'",da['gross_cylinder_volume_m3']);calc('StorageUsable','StorageGross * UsableFraction',"'m3'",da['usable_provided_m3']);calc('StorageDuration','StorageUsable / FeedPumpFlow','s',da['hold_up_minutes']*60)
para('A candidate is **two 4.5 m diameter × 22 m straight-length vessels**, excluding heads and the deaerating sections. Together their 70% usable range provides 490 m³, about 10.4 minutes. That drawdown inventory alone weighs about 445 tonnes; actual operating water and structural loads include the minimum heel. Reserve the minimum water level 14 m above feed-pump datum under the NPSH assumptions above. Five minutes would require about 235 m³ usable; the final reserve time should be selected with the operating philosophy. Storage and support elevations are major building-layout constraints.')
para('## 7. Pipe flow passages\n\nAll dimensions here are **internal bores**, before pressure wall, insulation and supports. Velocity screens: main steam 25 m/s; HP admission/heating steam 30; reheat/crossover 40; extraction lines 35; hot liquid return/feedwater 3; DA suction 2; condensate 2.5. These are provisional analyst choices. Existing SG branch/header bores are retained for comparison; their earlier custom walls are not redesigned here. New line walls require selected materials, design pressures, code and transients.')
para('| Service | Parallel paths | Flow total kg/s | Bore each mm | Velocity m/s |\n| --- | ---: | ---: | ---: | ---: |')
for q in r['pipes']:lines.append(f"| {q['service']} | {q['parallel']} | {q['mass_kg_s']:.2f} | {q['bore_m']*1000:.0f} | {q['velocity_m_s']:.2f} |")
para('\nDetailed pipe formulas use imported densities at each named state. Bores are rounded upward in Python in 25 mm steps; existing main/feedwater pipes keep their prior bores. A generic 40 m route, K=5, Darcy factor 0.015 screens loss magnitude; this is not the actual route budget and must not be added indiscriminately to the existing piping losses.')
for i,q in enumerate(r['pipes'],1):
 tag=f'Pipe{i}';para(f"**{q['service']}** ({q['state']}; {q['phase']}).")
 inp(tag+'Mass',q['mass_kg_s'],"'kg/s'");inp(tag+'Density',q['rho_kg_m3'],"'kg/m3'");inp(tag+'Count',q['parallel']);inp(tag+'Limit',q['velocity_limit_m_s'],"'m/s'");inp(tag+'Bore',q['bore_m'],'m')
 calc(tag+'MinBore',f'sqrt(4 * {tag}Mass / (Pi * {tag}Density * {tag}Count * {tag}Limit))','m',q['min_bore_m'])
 calc(tag+'Velocity',f'4 * {tag}Mass / (Pi * {tag}Density * {tag}Count * {tag}Bore^2)',"'m/s'",q['velocity_m_s'])
para('HP1, LP1 and feed-pump-turbine exhaust are screened with homogeneous wet-steam properties; real drainage, erosion, slip and flashing losses need separate analysis. Reheater return must remain pressurized upstream of its throttle; do not use its dense-liquid bore for the flashed downstream mixture. HP4 incoming drains include that return, and all drain/vent/control lines are still unsized. LP1 extraction is approximately **2.03 m bore** under the 35 m/s assumption; it needs a short, direct heater connection, not a long small pipe.')
para('''## 8. Layout and follow-up

The condenser reserves about 336 m² of equipment plan area across three modules, before operating aisles or withdrawal space. Four reheater reserves add 192 m². These are not additive building floor requirements if equipment is stacked, and are not proof that the existing **45 × 24 × 20 m** turbine building fits. The storage vessels, elevated water levels, three candidate double-flow LP casings, both generators, heaters, cranes and laydown space must be arranged explicitly before setting a new building size.

The present work establishes numerical starting points for that arrangement. Keep turbine casing and generator envelopes supplier-dependent. Final heater shells, piping walls, exhaust necks, cooling tower, air-removal system, water treatment, electrical switchgear, foundations and crane capacities remain unsized. No purchase specification or construction drawing is implied.

## Sources and verification

- Selected cycle and cooling cases: [reheat-selection.json](reheat-selection.json), [selected Hurmet basis](Selected%20reheat%20and%20wetness%20-%20Hurmet.md); exact source hashes are in [equipment-sizing.json](equipment-sizing.json).
- Properties: pinned CoolProp 7.2.0 HEOS water; [official water/IAPWS-95 reference](https://coolprop.org/fluid_properties/fluids/Water.html). The current documentation version may differ from the pinned calculation version.
- [Spirax Sarco, pressurised deaerators](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/pressurised-deaerators?sc_lang=en-GB) gives storage context for typical boiler installations. Its typical low-pressure conditions are not adopted here; our 0.6 MPa cycle and ten-minute usable-inventory assumption are explicit project choices.
- [Graham, surface condensers](https://graham-mfg.com/solutions/products/surface-condensers/) describes modular large condensers and configuration dependence. Our tube count and envelope are calculations/allowances, not Graham product dimensions.
- [Siemens Energy, utility steam turbines](https://www.siemens-energy.com/global/en/home/products-services/product/utility-steam-turbines.html) illustrates multiple LP casings and down-exhaust arrangements. It does not validate our annulus screen, select a model or establish a footprint.

Python checks seven heater heat balances, positive local temperature approaches, numerical UA convergence, condenser tube geometry and velocity, drive margins, and usable storage. Hurmet is saved, reopened and recalculated, then compared to the Python values. `size_equipment.py`, `publish_equipment.py` and `check_equipment_hurmet.cjs` reproduce this worksheet. Sensitivity checks change U, cooling head and storage time; no turbine manufacturer performance map is asserted.
''')
(ROOT/'Power plant equipment sizing - Hurmet.md').write_text('\n'.join(lines)+'\n');(ROOT/'equipment-hurmet-checks.json').write_text(json.dumps(expected,indent=2)+'\n')
print('Published worksheet and',len(expected),'comparison targets.')
