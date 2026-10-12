"""Select a feasible preliminary main-steam reheat case; retain earlier results.

No supplier operating envelope is inferred. Screening targets: 10% equilibrium
LP exhaust moisture, minimum 10 K reheater approach, positive flows. Selected
case adds thermal margin and is checked at LP interval efficiencies 0.86-0.90.
"""
from pathlib import Path
import json, csv, hashlib, math
import numpy as np
import reheat_model as model
ROOT=Path(__file__).resolve().parent
SELECTED=dict(p3=2.8e6,tr=783.15,thr=653.15,p2=1.6e6,p1=1e6)

def summary(r):
 return dict(HP_exhaust_MPa=r['inputs']['p3']/1e6,reheat_C=r['inputs']['tr']-273.15,
  heating_return_C=r['inputs']['thr']-273.15,HP2_MPa=r['inputs']['p2']/1e6,
  HP1_MPa=r['inputs']['p1']/1e6,gross_MW=r['gross']/1e6,moisture_percent=100*r['moisture'],
  min_approach_K=r['pinch'],reheat_supply_percent=100*r['fractions']['reheat'],
  reheat_MW=r['reheat_duty']/1e6,min_HP_bleed_percent=100*min(r['fractions'][k] for k in ['HP1','HP2','HP3','HP4']))

def main():
 baseline=json.loads((ROOT/'rankine-results.json').read_text())
 cooling=json.loads((ROOT/'cooling-cases.json').read_text())
 # Regression: new parameterization must reproduce the original case.
 old=model.balanced_case(pinch_points=401)
 for key in ['mass','gross','qcond','moisture','pinch']:
  assert math.isclose(old[key],baseline[key],rel_tol=1e-8,abs_tol=1e-6),(key,old[key],baseline[key])
 # Bounded screening grid, not a global cycle optimization. Negative bleeds,
 # failed DA closure and temperature crosses are retained as rejected cases.
 trials=[]
 for p in [2.7,2.8,3.0,3.5,4.0]:
  for t in [490,500,510]:
   for ret in [360,370,380]:
    row=dict(HP_exhaust_MPa=p,reheat_C=t,heating_return_C=ret)
    try:
     r=model.balanced_case(p3=p*1e6,tr=t+273.15,thr=ret+273.15,p2=1.6e6,p1=1e6)
     row.update(summary(r));row['status']='pass' if r['pinch']>=10 and r['moisture']<=.10 else 'fails approach or moisture'
    except (AssertionError,ValueError):row['status']='infeasible heater/flow/property balance'
    trials.append(row)
 selected=model.balanced_case(**SELECTED,pinch_points=1601)
 dense=model.solve(**SELECTED,plp3=selected['inputs']['plp3'],pinch_points=3201)
 assert abs(dense['pinch']-selected['pinch'])<.01
 assert selected['pinch']>=20 and selected['moisture']<.10
 q=selected['reheat_duty']
 ua=q*np.trapezoid(1/np.array(selected['reheater_approaches']),dx=1/1600)
 ua_dense=q*np.trapezoid(1/np.array(dense['reheater_approaches']),dx=1/3200)
 assert abs(ua/ua_dense-1)<1e-4
 # Keep the same actual condenser area, heat-transfer coefficient and water flow.
 capacity=cooling['water_mass_kg_s']*cooling['water_cp_J_kgK']
 effectiveness=1-math.exp(-cooling['U_W_m2K']*cooling['area_m2']/capacity)
 cases=[]
 for tc in [20,30,35]:
  lo,hi=2000.,25000.
  def evaluate(p):
   r=model.solve(**SELECTED,pc=p,plp3=selected['inputs']['plp3'])
   ts=model.prop('T','P',p,'Q',0)
   return capacity*effectiveness*(ts-tc-273.15)-r['qcond'],r,ts
  assert evaluate(lo)[0]<0<evaluate(hi)[0]
  for _ in range(28):
   mid=(lo+hi)/2
   if evaluate(mid)[0]>0:hi=mid
   else:lo=mid
  residual,r,ts=evaluate((lo+hi)/2)
  assert abs(residual)/r['qcond']<1e-7
  assert min(r['fractions'].values())>-1e-9
  assert abs(r['energy_residual'])<1e-5 and r['moisture']<.10
  tout=tc+273.15+r['qcond']/capacity
  lmtd=((ts-tc-273.15)-(ts-tout))/math.log((ts-tc-273.15)/(ts-tout))
  assert abs(cooling['U_W_m2K']*cooling['area_m2']*lmtd/r['qcond']-1)<1e-7
  cases.append(dict(inlet_C=tc,outlet_C=tout-273.15,condenser_kPa=r['inputs']['pc']/1000,
   condensing_C=ts-273.15,gross_MW=r['gross']/1e6,condenser_MW=r['qcond']/1e6,
   moisture_percent=100*r['moisture'],reheat_approach_K=r['pinch']))
 sensitivity=[]
 for eff in [.86,.88,.90]:
  # Heater extraction pressures remain fixed: no geometric re-selection per case.
  r=model.solve(**SELECTED,pc=5000,plp3=selected['inputs']['plp3'],lp_eff=eff,pinch_points=401)
  assert r['moisture']<.10 and abs(r['fractions']['DA'])<1e-9
  sensitivity.append(dict(LP_interval_efficiency=eff,condenser_kPa=5,gross_MW=r['gross']/1e6,moisture_percent=100*r['moisture']))
 # A pressure floor is needed for cooling below the reference temperature.
 cold=model.solve(**SELECTED,pc=3000,plp3=selected['inputs']['plp3'],lp_eff=.90)
 assert cold['moisture']>.10
 effective_tin=selected['states']['condenser']['t']-selected['qcond']/(capacity*effectiveness)
 tout_at_floor=effective_tin+selected['qcond']/capacity
 # Illustrative winter check: maintain flow and U by mixing warm return water.
 fresh=288.15
 recycle=(effective_tin-fresh)/(tout_at_floor-fresh)
 assert 0<recycle<1
 mixed=(1-recycle)*fresh+recycle*tout_at_floor
 assert abs(mixed-effective_tin)<1e-10
 result=dict(status='Selected preliminary thermal cycle; not supplier-qualified equipment or operational authorization',
  selection=SELECTED,selected_at_5kPa=selected,summary=summary(selected),reheater_UA_W_K=ua,
  area_sensitivity=[dict(assumed_U_W_m2K=u,area_m2=ua/u) for u in [500,1000,1500]],
  cooling_cases=cases,LP_efficiency_sensitivity=sensitivity,
  minimum_condenser_pressure_kPa=5,
  uncontrolled_3kPa=dict(moisture_percent=100*cold['moisture'],LP_interval_efficiency=.90),
  illustrative_15C_case=dict(effective_mixed_inlet_C=effective_tin-273.15,outlet_C=tout_at_floor-273.15,
   return_recycle_fraction=recycle,note='Ideal mixing calculation only; cooling-water bypass/control equipment remains to design'),
  comparison=dict(baseline_gross_MW=baseline['gross']/1e6,selected_gross_MW=selected['gross']/1e6,
   gross_penalty_MW=(baseline['gross']-selected['gross'])/1e6,
   baseline_reheat_supply_percent=100*baseline['fractions']['reheat'],baseline_reheat_MW=baseline['reheat_duty']/1e6),
  trials=trials,checks=['Baseline reproduction','Positive mass fractions and coupled energy closure',
   '1601/3201-point reheater profile convergence','Fixed-condenser effectiveness/LMTD agreement',
   'LP efficiency range at fixed extraction pressures','Cold-condition pressure-floor necessity'],
  source_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['rankine-results.json','cooling-cases.json','reheat_model.py','resolve_reheat.py']})
 (ROOT/'reheat-selection.json').write_text(json.dumps(result,indent=2)+'\n')
 keys=sorted(set().union(*(row.keys() for row in trials)))
 with (ROOT/'reheat-trials.csv').open('w') as f:
  writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(trials)
 with (ROOT/'selected-cycle-states.csv').open('w') as f:
  writer=csv.writer(f);writer.writerow(['state','pressure_MPa_abs','temperature_C','enthalpy_kJ_kg','entropy_kJ_kgK'])
  for name,s in selected['states'].items():writer.writerow([name,s['p']/1e6,s['t']-273.15,s['h']/1000,s['s']/1000])
 print(json.dumps({k:result[k] for k in ['summary','reheater_UA_W_K','area_sensitivity','cooling_cases','LP_efficiency_sensitivity','illustrative_15C_case','comparison']},indent=2),flush=True)

if __name__=='__main__':main()
