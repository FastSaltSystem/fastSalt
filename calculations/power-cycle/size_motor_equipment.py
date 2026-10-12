"""Motor-BFP equipment revision; preserves the historical equipment-sizing.json.
Uses D-028 cycle states, same screening criteria and explicit layout allowances.
"""
from pathlib import Path
import json,math,csv,hashlib,copy,sys
from CoolProp.CoolProp import PropsSI as P
from reheat_model import turb
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
OUT=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT
old=json.loads((ROOT/'equipment-sizing.json').read_text());study=json.loads((ROOT/'bfp-drive-comparison.json').read_text());base=json.loads((ROOT/'reheat-selection.json').read_text())['selected_at_5kPa'];e=study['proposed_pressure_comparison']['electric'];out=copy.deepcopy(old)
def states(case):
 s=copy.deepcopy(base['states']);s.update(case['heater_bleed_states']);s['HPex']=s['HP3'];s['IPex']=s['DA'];s['boiler_feed_pump']=case['hp_feed'][0];s['condensate_pump']=case['lp_feed'][0];s['LPex']=turb(s['LP1'],case['inputs']['pc'],case['inputs']['lp_eff']);s['condenser']={'p':case['inputs']['pc'],'h':P('H','P',case['inputs']['pc'],'Q',0,'Water')};return s
cases=[e]+[x['electric'] for x in study['same_condenser_cooling_cases']]
st=states(e)
def flow(row,c):
 name=row['service'];m=c['mass_kg_s'];f=c['flows_kg_s']
 if name.endswith(' extraction'):return f[name.split()[0]]
 return {'Main steam header (existing bore)':m,'Main steam branch (each of 3)':m/3,'HP admission after reheat split':m-f['reheat'],'Reheater heating supply':f['reheat'],'Reheater heating return':f['reheat'],'Cold reheat':c['reheat_flow_kg_s'],'Hot reheat':c['reheat_flow_kg_s'],'IP-to-LP crossover':c['condenser_flow_kg_s'],'Feedwater header (existing bore)':m,'Feedwater branch (each of 3)':m/3,'Deaerator to feed pumps':m,'Condensate through LP heater bank':c['condenser_flow_kg_s'],'IP outlet steam to deaerator':f['DA']}[name]
pipes=[]
for row in old['pipes']:
 if row['service']=='Feed-pump turbine supply':continue
 r=copy.deepcopy(row);r['previous_bore_m']=r['bore_m']
 if r['service']=='Feed-pump turbine exhaust to DA':r.update(service='IP outlet steam to deaerator',state='DA')
 r['state']={'pump_bleed2':'HP2','pump_bleed1':'HP1'}.get(r['state'],r['state'])
 data=[]
 for c in cases:
  s=states(c)[r['state']];density=P('D','P',s['p'],'H',s['h'],'Water');mf=flow(r,c);volume=mf/density;minimum=math.sqrt(4*volume/r['parallel']/math.pi/r['velocity_limit_m_s']);data.append((minimum,volume,density,mf,s))
 bore=max(r['previous_bore_m'],math.ceil(max(x[0] for x in data)/.025)*.025)
 minimum,volume,density,mf,s=data[0];v=4*volume/(r['parallel']*math.pi*bore**2);dp=(.015*40/bore+5)*density*v*v/2
 r.update(bore_m=bore,min_bore_m=minimum,mass_kg_s=mf,volume_m3_s=volume,rho_kg_m3=density,velocity_m_s=v,screen_dp_kPa=dp/1000,screen_dp_fraction=dp/s['p'],pressure_MPa=s['p']/1e6,temperature_C=P('T','P',s['p'],'H',s['h'],'Water')-273.15,phase='homogeneous wet-steam screen' if r['state']=='LP1' else 'single-phase',max_cooling_case_velocity_fraction=max(4*x[1]/(r['parallel']*math.pi*bore*bore)/r['velocity_limit_m_s'] for x in data))
 assert r['max_cooling_case_velocity_fraction']<=1+1e-10
 pipes.append(r)
out['pipes']=pipes
rh=out['reheater'];ratio=e['reheat_MW']/rh['duty_MW']
for k in ['duty_MW','UA_W_K','area_m2','duty_per_module_MW','area_per_module_m2']:rh[k]*=ratio
rh['area_sensitivity_m2']={k:v*ratio for k,v in rh['area_sensitivity_m2'].items()};rh['tubes_per_module']=math.ceil(rh['area_per_module_m2']/(math.pi*.0254*12));rh['bundle_eq_diameter_m']=math.sqrt(4*rh['tubes_per_module']*math.sqrt(3)/2*(1.25*.0254)**2/.70/math.pi);rh['provisional_module_envelope_m']=[16,3.25,3.25]
assert abs(rh['area_m2']-e['reheater_area_proxy_m2'])<.01
out['heaters']=[]
for h in e['heaters']:
 r=copy.deepcopy(next(x for x in old['heaters'] if x['name']==h['name']));r.update(duty_MW=h['duty_MW'],bleed_kg_s=h['bleed_kg_s'],area_m2=h['area_proxy_m2'],UA_W_K=h['area_proxy_m2']*2000/1.2,min_approach_K=h['min_approach_K'],bleed_C=h['bleed_C']);bank=h['name'][:2];i=int(h['name'][-1]);feed=e['hp_feed'] if bank=='HP' else e['lp_feed'];r.update(shell_MPa=e['heater_bleed_states'][h['name']]['p']/1e6,feed_MPa=feed[i]['p']/1e6,feed_flow_kg_s=e['mass_kg_s'] if bank=='HP' else e['condenser_flow_kg_s'],feed_in_C=feed[i-1]['t']-273.15,feed_out_C=feed[i]['t']-273.15,area_U1000_m2=h['area_proxy_m2']*2,area_U3000_m2=h['area_proxy_m2']*2/3)
 r.pop('drain_out_kg_s',None);out['heaters'].append(r)
co=out['condenser'];co.update(reference_duty_MW=e['condenser_MW'],hot_duty_MW=cases[2]['condenser_MW'],extreme_duty_MW=cases[3]['condenser_MW'])
t=out['turbines'];t['electrical_MW']=e['section_electric_MW'];t['HP_IP_electrical_MW']=sum(e['section_electric_MW'][k] for k in ['HP','IP']);t['gross_MW']=e['gross_MW'];t['HP_IP_generator_min_MVA']=t['HP_IP_electrical_MW']/.9*1.1;t['LP_generator_min_MVA']=e['section_electric_MW']['LP']/.9*1.1;t['provisional_HP_IP_generator_MVA']=550;t['provisional_LP_generator_MVA']=350
volume=e['exhaust_flow_kg_s']/P('D','P',st['LPex']['p'],'H',st['LPex']['h'],'Water');t.update(LP_exhaust_mass_kg_s=e['exhaust_flow_kg_s'],LP_exhaust_volume_m3_s=volume)
for a in t['annuli']:
 area=volume/180;a.update(annulus_total_m2=area,annulus_each_m2=area/a['exhaust_flows']);tip=math.sqrt(4*a['annulus_each_m2']/math.pi/(1-.5**2));a.update(tip_diameter_m=tip,hub_diameter_m=.5*tip,blade_length_m=.25*tip)
assert t['HP_IP_generator_min_MVA']<550 and t['LP_generator_min_MVA']<350
p=out['pumps'];p['feedwater'].update(driver='variable-speed electric motor',shaft_MW=e['bfp_shaft_MW'],electric_MW=e['bfp_electric_MW'],per_duty_shaft_MW=e['bfp_shaft_MW']/2,per_duty_electric_MW=e['bfp_electric_MW']/2)
p['condensate'].update(shaft_MW=e['cep_electric_MW']*.96,electric_MW=e['cep_electric_MW'],flow_m3_s=e['condenser_flow_kg_s']/P('D','P',5000,'Q',0,'Water'))
assert max(c['cep_electric_MW'] for c in cases)/2*1.1<.355
out['electrical']=dict(operating_BFP_load_MW=e['bfp_electric_MW'],installed_trains=3,operating_trains=2,motor_shaft_rating_MW=15,combined_efficiency=.95,assumed_power_factor=.95,capacity_margin=1.1,per_train_rated_electric_MW=15/.95,per_train_transformer_required_MVA=15/.95/.95*1.1,per_train_transformer_allowance_MVA=20,annex_envelope_m=[20,10,7],note='BFP-only supply allowance: one transformer/drive train per pump; switchgear, harmonics, motor speed, voltage, redundancy and station supply not selected. Standby train does not consume full load.')
out['reference']='D-029 motor BFP working equipment basis; bfp-drive-comparison.json proposed_pressure_comparison.electric'
out['status']='Preliminary revised schedule and dimensional reservations; supplier, pressure-boundary, piping and structural design pending'
out['performance']=dict(gross_MW=e['gross_MW'],after_BFP_CEP_MW=e['partial_net_MW'],after_BFP_CEP_CW_MW=e['partial_net_MW']-p['cooling_water']['electric_MW'],note='Even after cooling-water pumps this excludes salt pumps, fans and other station loads; not net export')
out['cooling_envelope_checks']=[dict(inlet_C=c['cooling_inlet_C'],condenser_kPa=c['inputs']['pc']/1000,condenser_MW=c['condenser_MW']) for c in cases[1:]]
out['checks']=['motor-cycle source consistency','all revised/retained bores meet velocity criteria at 5 kPa and three cooling-water cases','generator and pump capacity margins','reheater packing and required surface','retained condenser tube geometry; new duty/backpressure imported','heater thermal profiles from checked drive comparison']
out['source_hashes']={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['equipment-sizing.json','bfp-drive-comparison.json','reheat-selection.json','cooling-cases.json']};out['source_hashes']['size_motor_equipment.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'motor-equipment-sizing.json').write_text(json.dumps(out,indent=2)+'\n')
for name,rows in [('motor-equipment-pipes.csv',pipes),('motor-equipment-heaters.csv',out['heaters'])]:
 with (OUT/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Reheater',rh['area_m2'],'m2; generators',t['HP_IP_generator_min_MVA'],t['LP_generator_min_MVA'],'MVA required')
print('Changed bores',[(r['service'],r['previous_bore_m'],r['bore_m']) for r in pipes if r['bore_m']>r['previous_bore_m']+1e-9])
