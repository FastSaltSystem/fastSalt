"""Reproduce source volume balance and screen current geometry; no transient timing fit."""
from pathlib import Path
import hashlib,json,math,tomllib
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASIS=ROOT/'design/engineering/absorber-system.toml'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate(b):
 g=b['geometry'];s=b['screen'];a=b['architecture'];grav=s['gravity_m_s2'];ps=s['surge_initial_abs_Pa']
 rho=(s['source_pressure_abs_Pa']-ps)/(grav*s['source_head_m']);k=rho*grav
 area=math.pi*g['reservoir_diameter_m']**2/4; rv=area*g['reservoir_height_m']
 mv=math.pi*g['module_tank_diameter_m']**2/4*g['module_tank_height_m']
 height=g['absorber_top_z_m']-g['absorber_bottom_z_m'];t=s['absorber_tank_wall_trial_m']
 net=(g['absorber_radial_length_m']-3*t)*(g['absorber_width_m']-2*t)*g['active_height_m']
 cases=[]
 for label,gas_height in [('active_band',0.0),('upper_gas_space',g['absorber_top_z_m']-g['core_top_z_m'])]:
  bottom=g['core_bottom_z_m'];top=g['core_top_z_m'];scale=1.0
  for typ,v0 in [('primary',a['primary_volume_m3']),('secondary',a['secondary_volume_m3'])]:
   v=v0*scale;h=v/area;hp=g['reservoir_bottom_z_m']-bottom;hf=g['reservoir_bottom_z_m']-top
   p0=ps+k*(hp+h);vp=v;gas0=rv-v
   assert gas0>0
   pr=(p0*vp+ps*gas0)/(vp+rv)
   final=pr+k*hf
   va=v/g['active_height_m']*gas_height
   vs=(p0*v+(p0-final)*va)/(final-ps)
   closure=pr+k*hf-(ps*vs+p0*(v+va))/(vs+va)
   assert abs(closure)<1e-7
   cases.append(dict(case=label,chamber=typ,volume_m3=v,upper_gas_height_m=gas_height,upper_gas_volume_m3=va,salt_depth_m=h,hp_m=hp,hf_m=hf,pressure_initial_abs_Pa=p0,reservoir_initial_gas_m3=gas0,reservoir_final_abs_Pa=pr,surge_final_abs_Pa=final,pressure_vessel_m3=vp,surge_vessel_m3=vs,gas_vessels_total_m3=vp+vs,module_lower_gross_fraction=(vp+vs)/mv,closure_Pa=closure))
 source_vs=[s['source_pressure_abs_Pa']*v/(s['source_pressure_abs_Pa']/2+k*s['source_floor_above_absorber_m']-ps) for v in (a['primary_volume_m3'],a['secondary_volume_m3'])]
 return dict(inferred_density_kg_m3=rho,head_gradient_Pa_m=k,reservoir_gross_m3=rv,module_lower_gross_m3=mv,module_box_gross_m3=math.prod(g['module_box_dimensions_m']),absorber_tank_gross_m3=g['absorber_radial_length_m']*g['absorber_width_m']*height,absorber_tank_active_gross_m3=g['absorber_radial_length_m']*g['absorber_width_m']*g['active_height_m'],absorber_tank_trial_net_active_m3=net,required_primary_secondary_m3=a['primary_volume_m3']+a['secondary_volume_m3'],reservoir_trial_working_m3=rv*s['reservoir_working_fraction_trial'],source_surge_volumes_m3=source_vs,cases=cases)

def main():
 b=tomllib.loads(BASIS.read_text());r=calculate(b);g=b['geometry'];s=b['screen'];a=b['architecture']
 audit=json.loads((HERE/'absorber-geometry-audit.json').read_text());objs={o['name']:o for o in audit['objects']}
 # Recorded values must still agree with measured scene evidence to rounding precision.
 for key,name,axis in [('reservoir_bottom_z_m','equipment.absorber_reservoir_1.salt_vessel_envelope','world_min'),('observed_absorber_bottom_z_m','reactor.absorber_1.rectangular_tank','world_min'),('absorber_top_z_m','reactor.absorber_1.rectangular_tank','world_max')]:
  assert abs(g[key]-objs[name][axis][2])<1e-5,key
 assert sum(n.startswith('reactor.absorber_') and n.endswith('.rectangular_tank') for n in objs)==6
 assert sum(n.startswith('equipment.absorber_reservoir_') for n in objs)==12
 assert sum(n.startswith('equipment.absorber_module_') and n.endswith('.salt_vessel_envelope') for n in objs)==12
 assert r['absorber_tank_trial_net_active_m3']>r['required_primary_secondary_m3']
 # Independent source Eq 2 closure using published rounded surge sizes, within 100 Pa.
 for v,vs in zip([a['primary_volume_m3'],a['secondary_volume_m3']],[.3196,.3897]):
  err=s['source_pressure_abs_Pa']/2+r['head_gradient_Pa_m']*3-(s['surge_initial_abs_Pa']+s['source_pressure_abs_Pa']*v/vs)
  assert abs(err)<100
 r['sources']={str(p.relative_to(ROOT)):sha(p) for p in [BASIS,HERE/'absorber-geometry-audit.json',Path(__file__)]}
 r['source_document_sha256']=b['sources']['document']['sha256'];r['checks']=['Measured elevations and counts agree','Current 3 mm wall capacity sensitivity exceeds source charge','Source surge volumes reproduced within published rounding','All four final gas/hydrostatic balances close']
 r['hurmet_checks']={}
 lines=['---------------','decimalFormat: 1,000,000.','fontSize: 12','pageSize: letter','saveDate: 2026-10-15','---------------','','# Absorber capacity and gas module screen','','Preliminary review, 15 October 2026. Twelve circuits: primary A and secondary B at each of six radial assemblies. Source chamber volumes are 0.1589 and 0.1938 m³; their neutronic sufficiency is not reassessed. Current 3D elevations override the older sketch. The absorber bottom is raised 0.30 m to the active-core bottom; other equipment envelopes are retained.','','All editable equations below use **SI scalar values**: metres, cubic metres, pascals absolute, kg/m³ and m/s². Outputs ending L are litres; kPa outputs are absolute. These balance pressures are not adopted settings.','','## Geometry and assumptions','','The original measured absorber tank was 2.10 × 0.08 × 3.95 m, Z = -7.57 to -3.62 m. The owner excludes the bottom reflector: the adopted bottom is Z = -7.27 m and the remaining envelope is 3.65 m tall. The active core spans Z = -7.27 to -3.87 m, 3.4 m high. Reservoir bottoms are Z = -0.05 m. No salt volume below the active core is included. The second case estimates the 0.25 m upper region as retained gas space, using the source chamber cross-sections; it is not additional salt fill. Partition geometry remains unresolved.','','Density is inferred from document Eq 1, not independently specified. Reservoirs are provisionally treated as gross cylinders, with salt charge equal to chamber volume, zero heel, unchanged prefilled line inventory, and the remaining gas space initially at 100 kPa absolute. Pressure-vessel volume equals chamber volume as in the source. Gas is isothermal at equal temperature; real hot/cold gas differences and line volumes need review.']
 def inp(n,v):lines.extend(['',f'¢` {n} = {v:.12g} `'])
 def out(n,expr,v):lines.extend(['',f'¢??` {n} = {expr} = 〔{v:.12g}〕 `']);r['hurmet_checks'][n]=v
 for n,v in [('Gravity',s['gravity_m_s2']),('SourcePressure',s['source_pressure_abs_Pa']),('SurgeInitial',s['surge_initial_abs_Pa']),('SourceHead',s['source_head_m']),('PrimaryCharge',a['primary_volume_m3']),('SecondaryCharge',a['secondary_volume_m3']),('ActiveHeight',g['active_height_m']),('AbsorberTankLength',g['absorber_radial_length_m']),('AbsorberTankWidth',g['absorber_width_m']),('AbsorberTankHeight',g['absorber_top_z_m']-g['absorber_bottom_z_m']),('WallTrial',s['absorber_tank_wall_trial_m']),('TankDiameter',g['reservoir_diameter_m']),('TankHeight',g['reservoir_height_m']),('ReservoirBottom',g['reservoir_bottom_z_m']),('CoreBottom',g['core_bottom_z_m']),('CoreTop',g['core_top_z_m']),('AbsorberTankBottom',g['absorber_bottom_z_m']),('AbsorberTankTop',g['absorber_top_z_m']),('UpperGasHeight',g['absorber_top_z_m']-g['core_top_z_m'])]:inp(n,v)
 out('Density','(SourcePressure - SurgeInitial) / (Gravity SourceHead)',r['inferred_density_kg_m3'])
 out('Gradient','Density Gravity',r['head_gradient_Pa_m'])
 out('TankArea','π TankDiameter^2 / 4',math.pi*g['reservoir_diameter_m']**2/4)
 out('TankVolume','TankArea TankHeight',r['reservoir_gross_m3'])
 out('TankLitres','1000 TankVolume',1000*r['reservoir_gross_m3'])
 out('AbsorberTankGrossL','1000 AbsorberTankLength AbsorberTankWidth AbsorberTankHeight',1000*r['absorber_tank_gross_m3'])
 out('AbsorberTankActiveL','1000 AbsorberTankLength AbsorberTankWidth ActiveHeight',1000*r['absorber_tank_active_gross_m3'])
 out('TrialNetL','1000 (AbsorberTankLength - 3 WallTrial) (AbsorberTankWidth - 2 WallTrial) ActiveHeight',1000*r['absorber_tank_trial_net_active_m3'])
 out('ChargeTotalL','1000 (PrimaryCharge + SecondaryCharge)',1000*r['required_primary_secondary_m3'])
 out('ReservoirTrialL','0.8 TankLitres',1000*r['reservoir_trial_working_m3'])
 lines+=['','The 3 mm wall/partition trial and 80% reservoir allowance are capacity sensitivities only. No metal thickness, usable fill fraction or chamber division is adopted. The physical fit must also accommodate the separate bottom-fed external salt tubes.','','## Corrected source balance','','Eq 5 must include the hydrostatic term in its denominator. For the original 3 m gap and a zero-headspace full reservoir:']
 for typ,v in zip(['Primary','Secondary'],r['source_surge_volumes_m3']):out('Source'+typ+'SurgeL',f'1000 SourcePressure {typ}Charge / (SourcePressure / 2 + Gradient * 3 - SurgeInitial)',v*1000)
 lines+=['','The result reproduces about 319.6 and 389.7 litres. The source intermediate Eq 14 also has a sign inconsistency; its Eq 17 correctly gives head = hp + initial salt depth - filled height - reservoir level drop. Continuity means equal volume flow, not equal velocities in unequal areas.','','## Current reservoir and elevation screen','','For each circuit, p0 is the static pressure needed to hold its chamber empty. On switching, the pressure vessel mixes with the reservoir headspace. Final reservoir pressure is (p0 Vp + ps0 Vg0)/(Vp + Vg0 + charge). With retained chamber gas volume Va, the required surge volume is [p0 charge + (p0 - final gas pressure) Va] / (final gas pressure - initial surge pressure). This follows from final hydrostatic balance and conservation of gas. Equilibrium at exactly full is a mathematical screen, not a carryover-prevention design. D-071 adds separate charging and discharge services: both module service isolation valves are closed for this normal-duty gas balance. Shared headers are excluded; additional module-side dead-leg volume remains to include.']
 for c in r['cases']:
  pref=('Active' if c['case']=='active_band' else 'Upper')+c['chamber'].title(); src=c['chamber'].title()+'Charge';full=c['case']!='active_band'
  lines+=['',f"### {c['case'].replace('_',' ').title()} {c['chamber']}"]
  out(pref+'Volume',src,c['volume_m3'])
  out(pref+'GasVolume',f'{pref}Volume / ActiveHeight * UpperGasHeight' if full else '0',c['upper_gas_volume_m3'])
  out(pref+'Depth',pref+'Volume / TankArea',c['salt_depth_m'])
  out(pref+'Hp','ReservoirBottom - CoreBottom',c['hp_m'])
  out(pref+'Hf','ReservoirBottom - CoreTop',c['hf_m'])
  out(pref+'P0',f'SurgeInitial + Gradient ({pref}Hp + {pref}Depth)',c['pressure_initial_abs_Pa'])
  out(pref+'Final',f'({pref}P0 {pref}Volume + SurgeInitial (TankVolume - {pref}Volume)) / ({pref}Volume + TankVolume)',c['reservoir_final_abs_Pa'])
  out(pref+'Surge',f'({pref}P0 {pref}Volume + ({pref}P0 - {pref}Final - Gradient {pref}Hf) {pref}GasVolume) / ({pref}Final + Gradient {pref}Hf - SurgeInitial)',c['surge_vessel_m3'])
  out(pref+'PressureL',f'1000 {pref}Volume',1000*c['pressure_vessel_m3'])
  out(pref+'SurgeL',f'1000 {pref}Surge',1000*c['surge_vessel_m3'])
  out(pref+'TotalL',f'1000 ({pref}Volume + {pref}Surge)',1000*c['gas_vessels_total_m3'])
  out(pref+'P0kPa',f'{pref}P0 / 1000',c['pressure_initial_abs_Pa']/1000)
 lines+=['','## Interpretation','','The existing 643.4 litre salt reservoirs exceed both source charges, including an illustrative 80% working-volume screen. Filling them completely is not the modeled operating charge. The internal absorber tanks have enough gross geometric space for the source volumes, but their partitions, walls and upper gas spaces are not defined; no bottom-reflector liquid pocket is included.','','The active-band primary module requires about 515 litres of ideal pressure-plus-surge gas space; the secondary about 616 litres. The latter nearly consumes the entire 643 litre lower cylinder before walls, heads and fittings. Including the 0.25 m upper gas space increases these totals; see the Upper case cells above. This space stays gaseous when the active chamber is filled. The rejected bottom-reflector fill case is removed. The 0.765 × 0.810 × 1.50 m upper enclosure is additional gross space, not verified pressure-vessel accommodation. Retain the overall module reservation pending an internal arrangement; do not conclude that the single lower cylinder alone is adequate.','','There is no updated injection-time prediction. The document reports 18.2 and 22.2 s, but numerical bore, hydraulic length, viscosity, roughness, gas temperatures and valve/gas-line resistance are not supplied. The current 50 mm OD and 2 mm visual wall imply 46 mm bore only as a visualization assumption. External bottom routing must be completed before its hydraulic length is available. Required shutdown time and gas recovery time are also unresolved. No calibration to the reported times is used.','','## Sources and reproduction','','Source: AbsorberSaltInjectionTime.docx, pages 1-6; immutable source hash in design/engineering/absorber-system.toml. Current scene measurements: absorber-geometry-audit.json. Owner confirmed two separate chambers per assembly, external bottom-feed routing, and exclusion of the bottom-reflector region on 15 October 2026.','','General gas-law reference: [DOE Fundamentals Handbook, Thermodynamics volume 1](https://www.energy.gov/documents/doe-hdbk-1012-92vol1). Absolute pressures and temperatures are required. This does not validate the source isothermal assumption.','','Run absorber_capacity.py and then check_absorber_capacity.cjs with HURMET_ENGINE and TEMML_ENGINE set to the pinned project bundles. Python independently checks measured elevations, counts, original source rounding and final balance closure; Hurmet checks evaluation, reopening and parameter sensitivity. Generated HTML remains ignored.']
 # Preserve the team's manually maintained record when regenerating the sheet.
 worksheet=HERE/'Absorber capacity and gas modules - Hurmet.md'
 team_heading='## Michigan team input and results record'
 sources_heading='## Sources and reproduction'
 if worksheet.exists():
  previous=worksheet.read_text()
  if team_heading in previous:
   start=previous.index(team_heading)
   end=previous.index(sources_heading,start)
   lines.insert(lines.index(sources_heading),previous[start:end].rstrip()+'\n')
 worksheet.write_text('\n'.join(lines)+'\n')
 (HERE/'absorber-capacity-results.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k not in ('hurmet_checks','sources')},indent=2))
if __name__=='__main__':main()
