"""Preliminary balance-of-plant sizing; no pressure-boundary or turbine blade design.
Run with a power-cycle directory as argv[1], or beside the selected-cycle JSON.
CoolProp 7.2.0 / numpy; dimensions SI; sources and assumptions in published worksheet.
"""
from pathlib import Path
import sys,json,math,hashlib,csv
import numpy as np
from CoolProp.CoolProp import PropsSI as P
import CoolProp
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
OUT=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT
R=json.loads((ROOT/'reheat-selection.json').read_text()); s=R['selected_at_5kPa']; st=s['states']; m=s['mass']; y=s['fractions'];F='HEOS::Water';g=9.80665
cool=json.loads((ROOT/'cooling-cases.json').read_text())
def rho(k):return P('D','P',st[k]['p'],'H',st[k]['h'],F)
def pipe(name,key,flow,limit,n=1,bore=None):
 density=rho(key);vflow=flow/density;dmin=math.sqrt(4*vflow/n/math.pi/limit)
 bore=bore or math.ceil(dmin/.025)*.025
 velocity=4*vflow/n/math.pi/bore**2
 # A route allowance, not a piping-network solution. Constant properties.
 length=40.; K=5.; friction=.015
 dp=(friction*length/bore+K)*density*velocity**2/2
 return dict(service=name,state=key,mass_kg_s=flow,rho_kg_m3=density,volume_m3_s=vflow,parallel=n,velocity_limit_m_s=limit,min_bore_m=dmin,bore_m=bore,velocity_m_s=velocity,screen_length_m=length,screen_K=K,screen_Darcy_f=friction,screen_dp_kPa=dp/1000,screen_dp_fraction=dp/st[key]['p'],phase='two-phase homogeneous screen' if key in ['LP1','pump_bleed1','pump_exhaust'] else 'single-phase')
pipes=[pipe('Main steam header (existing bore)','main',m,25,bore=.725),pipe('Main steam branch (each of 3)','main',m/3,25,bore=.425),pipe('HP admission after reheat split','main',m*(1-y['reheat']),30),pipe('Reheater heating supply','main',m*y['reheat'],30),pipe('Reheater heating return','reheat_return',m*y['reheat'],3),pipe('Cold reheat','reheat_cold',s['reheat_flow'],40,2),pipe('Hot reheat','reheat_hot',s['reheat_flow'],40,2),pipe('IP-to-LP crossover','IPex',s['condenser_mass'],40,3),pipe('Feedwater header (existing bore)','feedwater',m,3,bore=.65),pipe('Feedwater branch (each of 3)','feedwater',m/3,3,bore=.375),pipe('Deaerator to feed pumps','deaerator',m,2,2),pipe('Condensate through LP heater bank','condensate_pump',s['condenser_mass'],2.5)]
for tag,key in [('HP4','HP4'),('HP3','HPex'),('HP2','pump_bleed2'),('HP1','pump_bleed1'),('LP3','LP3'),('LP2','LP2'),('LP1','LP1')]:pipes.append(pipe(tag+' extraction',key,m*y[tag],35))
pipes.append(pipe('Feed-pump turbine supply','HP4',m*y['pump_turbine'],35))
pipes.append(pipe('Feed-pump turbine exhaust to DA','pump_exhaust',m*(y['pump_turbine']-y['HP2']-y['HP1']),35))
# Closed-heater thermal proxies: pre-mix bleed and incoming drains at shell P.
# Then integrate a countercurrent temperature profile. This is NOT a zone design.
heaters=[]
for bank,sequence,feed,flow in [('HP',[4,3,2,1],s['hp_feed'],m),('LP',[3,2,1],s['lp_feed'],s['condenser_mass'])]:
 incoming=m*y['reheat'] if bank=='HP' else 0.;hin=st['reheat_return']['h'] if bank=='HP' else 0.
 for i in sequence:
  name=bank+str(i); key={'HP4':'HP4','HP3':'HPex','HP2':'pump_bleed2','HP1':'pump_bleed1','LP3':'LP3','LP2':'LP2','LP1':'LP1'}[name]
  p=st[key]['p'];bleed=m*y[name]; total=incoming+bleed;hf=P('H','P',p,'Q',0,F)
  hmix=(incoming*hin+bleed*st[key]['h'])/total
  q=flow*(feed[i]['h']-feed[i-1]['h']);qh=total*(hmix-hf)
  assert abs(qh/q-1)<1e-8
  def profile(n):
   z=np.linspace(0,1,n);a=np.array([P('T','P',p,'H',hf+t*(hmix-hf),F)-P('T','P',feed[i]['p'],'H',feed[i-1]['h']+t*(feed[i]['h']-feed[i-1]['h']),F) for t in z]);assert min(a)>0
   return q*np.trapezoid(1/a,x=z),float(min(a))
  ua,approach=profile(1601);ua2,_=profile(3201);assert abs(ua/ua2-1)<.001
  U=2000.;margin=1.2;area=ua/U*margin
  heaters.append(dict(name=name,duty_MW=q/1e6,bleed_kg_s=bleed,drain_out_kg_s=total,shell_MPa=p/1e6,feed_MPa=feed[i]['p']/1e6,feed_flow_kg_s=flow,feed_in_C=feed[i-1]['t']-273.15,feed_out_C=feed[i]['t']-273.15,min_approach_K=approach,UA_W_K=ua,U_assumed_W_m2K=U,area_margin=margin,area_m2=area,area_U1000_m2=ua/1000*margin,area_U3000_m2=ua/3000*margin))
  incoming=total;hin=hf
# Preserve condenser surface used in the accepted cooling cases, geometry only.
A=cool['area_m2'];Nmod=3;od=.0254;tid=.0234;L=12.;passes=2;pitch=1.25*od;pack=.75
Nt=math.ceil(A/Nmod/(math.pi*od*L)/passes)*passes;actualA=Nmod*Nt*math.pi*od*L
v=cool['water_volume_m3_s']/Nmod/(Nt/passes*math.pi*tid**2/4)
mu=P('V','T',297.15,'P',101325,F);re=998*v*tid/mu;fd=(-1.8*math.log10((.0000015/tid/3.7)**1.11+6.9/re))**-2
head=(fd*passes*L/tid+4)*v*v/(2*g)
cond=dict(reference_duty_MW=s['qcond']/1e6,hot_duty_MW=R['cooling_cases'][1]['condenser_MW'],extreme_duty_MW=R['cooling_cases'][2]['condenser_MW'],reference_area_m2=A,provided_area_m2=actualA,assumed_U_W_m2K=2500,modules=Nmod,area_per_module_m2=actualA/Nmod,tube_OD_m=od,tube_ID_m=tid,tube_length_m=L,tube_passes=passes,tubes_per_module=Nt,total_tubes=Nt*Nmod,water_m3_s=cool['water_volume_m3_s'],tube_water_velocity_m_s=v,tube_loss_head_m=head,bundle_cross_section_m2=Nt*math.sqrt(3)/2*pitch*pitch/pack,bundle_eq_diameter_m=math.sqrt(4*Nt*math.sqrt(3)/2*pitch*pitch/pack/math.pi),provisional_module_envelope_m=[16,7,9],tube_withdrawal_clearance_m=13.,water_main_count=2,water_main_bore_m=2.25,water_module_branch_bore_m=2.,area_with_20percent_spare_m2=A*1.2)
assert actualA>=A and actualA/A<1.001 and 2<v<3.5
# Turbine capacities and LP volumetric flow (homogeneous equilibrium mixture).
vol=s['exhaust_mass']/rho('LPex');axial=180.;hub=.5
ann=[]
for count in [4,6,8]:
 af=vol/axial/count; tip=math.sqrt(4*af/math.pi/(1-hub**2));ann.append(dict(exhaust_flows=count,annulus_total_m2=vol/axial,annulus_each_m2=af,tip_diameter_m=tip,hub_diameter_m=hub*tip,blade_length_m=tip*(1-hub)/2))
fac=m*.99*.985
power={k:s['specific_work'][k]*fac/1e6 for k in ['HP','IP','LP']}
turb=dict(electrical_MW=power,HP_IP_electrical_MW=power['HP']+power['IP'],gross_MW=sum(power.values()),LP_exhaust_mass_kg_s=s['exhaust_mass'],LP_exhaust_volume_m3_s=vol,assumed_axial_velocity_m_s=axial,hub_tip_ratio=hub,annuli=ann,generator_power_factor=.9,generator_capacity_margin=1.1,HP_IP_generator_min_MVA=(power['HP']+power['IP'])/.9*1.1,LP_generator_min_MVA=power['LP']/.9*1.1,provisional_HP_IP_generator_MVA=500,provisional_LP_generator_MVA=350)
# Pressure-budget sizing separate from frozen cycle; it requires subsequent reclosure.
def duty_pump(key,pout,eff):
 v=st[key];his=P('H','P',pout,'S',v['s'],F);dh=(his-v['h'])/eff;return dh
rhoDA=rho('deaerator');qDA=m/rhoDA
bfp=m*duty_pump('deaerator',26.5e6,.85)
cep=s['condenser_mass']*duty_pump('condenser',1e6,.80)
cwshaft=998*g*cool['water_volume_m3_s']*20/.88
pumps=dict(feedwater=dict(flow_m3_s=qDA,pressure_in_MPa=.6,pressure_out_MPa=26.5,head_m=(26.5e6-.6e6)/(rhoDA*g),shaft_MW=bfp/1e6,original_cycle_shaft_MW=s['bfp']/1e6,shaft_increase_MW=(bfp-s['bfp'])/1e6,arrangement='3 x 50% (2 duty, 1 standby)',per_duty_flow_m3_s=qDA/2,per_duty_shaft_MW=bfp/2e6,per_driver_reserved_MW=15.,driver='steam-driven working preference; startup/backup unresolved',NPSHr_assumed_m=8,NPSH_margin_m=3,suction_loss_m=2,min_level_above_pump_m=13,layout_level_above_pump_m=14),condensate=dict(flow_m3_s=s['condenser_mass']/rho('condenser'),pressure_out_MPa=1.,required_pressure_MPa=.6+rho('condensate_pump')*g*14/1e6+.1+.05,shaft_MW=cep/1e6,electric_MW=cep/.96/1e6,arrangement='3 x 50% (2 duty, 1 standby)',per_motor_MW=.355,hotwell_level_above_pump_m=4,NPSHr_assumed_m=2,suction_loss_m=1,margin_m=1),cooling_water=dict(flow_m3_s=cool['water_volume_m3_s'],head_m=20,shaft_MW=cwshaft/1e6,electric_MW=cwshaft/.96/1e6,arrangement='3 x 50% (2 duty, 1 standby)',per_duty_flow_m3_s=cool['water_volume_m3_s']/2,per_motor_MW=3.5,electric_head_cases_MW={str(h):cwshaft/.96/1e6*h/20 for h in [15,20,30]}))
assert pumps['condensate']['required_pressure_MPa']<1
assert bfp/2e6*1.1<15 and cep/.96/2e6*1.1<.355 and cwshaft/.96/2e6*1.1<3.5
# Storage using usable, not gross vessel volume; heads excluded conservatively.
vt=2*math.pi*4.5**2/4*22;usable=.70*vt
da=dict(flow_kg_s=m,water_density_kg_m3=rhoDA,flow_m3_s=qDA,target_minutes=10,usable_required_m3=qDA*600,vessels=2,diameter_m=4.5,straight_length_m=22.,gross_cylinder_volume_m3=vt,usable_fraction=.70,usable_provided_m3=usable,hold_up_minutes=usable/qDA/60,water_mass_at_usable_t=usable*rhoDA/1000,excludes='head volume, deaerating section, minimum heel, vessel steel, transients; 70% usable range must be reconciled with levels')
assert da['hold_up_minutes']>=10
# Reheater is four candidate modules, area from integrated nonlinear thermal profile.
rua=R['reheater_UA_W_K'];rh=dict(duty_MW=s['reheat_duty']/1e6,UA_W_K=rua,assumed_U_W_m2K=1000,area_margin=1.2,area_m2=rua/1000*1.2,area_sensitivity_m2={str(u):rua/u*1.2 for u in [500,1000,1500]},modules=4,duty_per_module_MW=s['reheat_duty']/4e6,area_per_module_m2=rua/1000*1.2/4,minimum_approach_K=s['pinch'])
# Illustrative tube-only packing envelope, no pressure-wall or shell-side verification.
rod=.0254;rlen=12;rn=math.ceil(rh['area_per_module_m2']/(math.pi*rod*rlen));rpackarea=rn*math.sqrt(3)/2*(1.25*rod)**2/.70
rh.update(tube_OD_assumed_m=rod,tube_length_assumed_m=rlen,tubes_per_module=rn,bundle_eq_diameter_m=math.sqrt(4*rpackarea/math.pi),provisional_module_envelope_m=[16,3,3],withdrawal_clearance_m=13)
result=dict(status='Preliminary equipment requirements and conditional layout allowances; pressure boundaries, blades and suppliers not selected',property_library='CoolProp '+CoolProp.__version__,reference='D-026 selected_at_5kPa; cycle performance frozen, pump allowances not fed back',pipes=pipes,heaters=heaters,condenser=cond,turbines=turb,pumps=pumps,deaerator=da,reheater=rh,checks=['seven heater hot/cold energy balances','positive local heater approaches','1601/3201-point heater UA convergence within 0.1%','condenser surface/count/pass/velocity closure','pump head and provisional drive margins','deaerator usable inventory >= 10 minutes'],source_hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['reheat-selection.json','cooling-cases.json','reheat_model.py']})
OUT.mkdir(parents=True,exist_ok=True);(OUT/'equipment-sizing.json').write_text(json.dumps(result,indent=2)+'\n')
for file,rows in [('equipment-pipes.csv',pipes),('equipment-heaters.csv',heaters)]:
 with (OUT/file).open('w') as f:wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
print(json.dumps({k:result[k] for k in ['reheater','condenser','turbines','pumps','deaerator']},indent=2));print('HEATERS',[(h['name'],round(h['duty_MW'],1),round(h['area_m2'])) for h in heaters]);print('PIPES',[(h['service'],h['parallel'],round(h['bore_m'],3),round(h['screen_dp_fraction']*100,1)) for h in pipes])
