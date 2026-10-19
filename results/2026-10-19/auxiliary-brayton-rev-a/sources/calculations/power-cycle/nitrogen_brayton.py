"""Real-nitrogen comparison with preserved steam Brayton trials."""
from pathlib import Path
import math,json,hashlib
import CoolProp
from CoolProp.CoolProp import PropsSI as P,PhaseSI
D=Path(__file__).resolve().parent
F='HEOS::Nitrogen'
def state(p,t=None,h=None):
 if h is None:h=P('H','P',p,'T',t,F)
 t=P('T','P',p,'H',h,F)
 return dict(pressure_Pa=p,temperature_K=t,temperature_C=t-273.15,enthalpy_J_kg=h,entropy_J_kg_K=P('S','P',p,'H',h,F),density_kg_m3=P('D','P',p,'H',h,F),phase=PhaseSI('P',p,'H',h,F))
def solve(ratio=4,p_low=1e6,T2=560,T1=None,eta_c=.85,eta_t=.88,loss=.02,duty=1e7):
 p1=p_low;p2=p1*ratio;p3=p2*(1-loss);p4=p1/(1-loss)
 def comp(t):
  a=state(p1,t=t);return a['enthalpy_J_kg']+(P('H','P',p2,'S',a['entropy_J_kg_K'],F)-a['enthalpy_J_kg'])/eta_c
 if T1 is None:
  target=state(p2,t=T2)['enthalpy_J_kg'];lo,hi=150,T2
  assert comp(lo)<target<comp(hi)
  for _ in range(60):
   mid=(lo+hi)/2
   if comp(mid)>target:hi=mid
   else:lo=mid
  T1=(lo+hi)/2
 a=state(p1,t=T1);b=state(p2,h=comp(T1));c=state(p3,t=830)
 h4=c['enthalpy_J_kg']-eta_t*(c['enthalpy_J_kg']-P('H','P',p4,'S',c['entropy_J_kg_K'],F));d=state(p4,h=h4)
 h1,h2,h3,h4=[s['enthalpy_J_kg'] for s in [a,b,c,d]]
 q=h3-h2;out=h4-h1;wc=h2-h1;wt=h3-h4;m=duty/q
 assert min(q,out,wc,wt)>0
 assert abs(q-out-wt+wc)<1e-6
 assert b['entropy_J_kg_K']>=a['entropy_J_kg_K'] and d['entropy_J_kg_K']>=c['entropy_J_kg_K']
 return dict(fluid='Nitrogen',inputs=dict(ratio=ratio,p_low_Pa=p_low,eta_c=eta_c,eta_t=eta_t,loss_each=loss,duty_W=duty),states=dict(compressor_inlet=a,heater_inlet=b,turbine_inlet=c,cooler_inlet=d),specific=dict(heat_in_J_kg=q,heat_out_J_kg=out,compressor_J_kg=wc,turbine_J_kg=wt),mass_kg_s=m,inlet_volume_m3_s=m/a['density_kg_m3'],compressor_W=m*wc,turbine_W=m*wt,available_shaft_W=m*(.98*wt-wc),air_heat_W=m*out,energy_residual_J_kg=q-out-wt+wc)
def cooler(case):
 fluid='HEOS::'+case['fluid'];a=case['states']['compressor_inlet'];d=case['states']['cooler_inlet'];deltas=[]
 # Counterflow profiles: x=0 at cold gas end, x=1 at hot gas end.
 for j in range(301):
  x=j/300;p=a['pressure_Pa']+x*(d['pressure_Pa']-a['pressure_Pa']);h=a['enthalpy_J_kg']+x*(d['enthalpy_J_kg']-a['enthalpy_J_kg'])
  deltas.append(P('T','P',p,'H',h,fluid)-(303.15+100*x))
 case['minimum_air_approach_K']=min(deltas)
 case['air_cooling_feasible']=min(deltas)>0
 case['required_counterflow_UA_W_K']=case['air_heat_W']*sum((1/deltas[i]+1/deltas[i+1])/2/300 for i in range(300)) if min(deltas)>0 else None
 rho=101325/(287.05*303.15);case['fan_electric_W']=case['air_heat_W']/(1007*100)/rho*500/.65/.96
 case['electric_after_fan_W']=.95*case['available_shaft_W']-case['fan_electric_W']
 return case

def main():
 steam=json.loads((D/'brayton-cooler-results.json').read_text());candidates={}
 for key,src in [('steam_two','base'),('steam_eight','high_ratio')]:
  b=steam[src];st=b['states'];s=dict(fluid='Water',states=dict(compressor_inlet=st['compressor_inlet'],heater_inlet=st['steam_generator_inlet'],turbine_inlet=st['turbine_inlet'],cooler_inlet=st['air_cooler_inlet']),mass_kg_s=b['steam_flow_kg_s'],inlet_volume_m3_s=b['compressor_inlet_volume_m3_s'],available_shaft_W=b['available_shaft_W'],air_heat_W=b['heat_rejected_air_cooler_W'])
  candidates[key]=cooler(s)
 for key,kw in [('nitrogen_two_same_pressure',dict(ratio=2,p_low=5e5)),('nitrogen_four',{}),('nitrogen_eight_fixed',dict(ratio=8)),('nitrogen_eight_warm',dict(ratio=8,T1=318.15))]:candidates[key]=cooler(solve(**kw))
 pressure=[cooler(solve(p_low=p)) for p in [5e5,1e6,2e6]]
 sensitivity=[cooler(solve(eta_c=.80,eta_t=.85)),cooler(solve(loss=.05))]
 b=candidates['nitrogen_four'];double=solve(duty=2e7)
 assert abs(double['available_shaft_W']/b['available_shaft_W']-2)<1e-9
 assert candidates['nitrogen_eight_fixed']['minimum_air_approach_K']<0
 assert candidates['nitrogen_eight_warm']['minimum_air_approach_K']>0
 # Low-pressure ideal-gas sanity check: density close to p/(R*T).
 low=state(1e5,t=560);ideal=1e5/(8.314462618/.02801348*560)
 assert abs(low['density_kg_m3']/ideal-1)<.005
 pump=json.loads((D/'brayton-fan-pump-results.json').read_text())['cases'][0]['pump_electric_W']
 for c in candidates.values():c['remaining_electric_30MW_W']=3*c['electric_after_fan_W']-pump
 out=dict(date='2026-10-13',property_model='CoolProp '+CoolProp.__version__+' HEOS::Nitrogen',cases=candidates,pressure_sensitivity=pressure,machine_loss_sensitivity=sensitivity,pump_30MW_electric_W=pump,checks=dict(energy_and_entropy=True,duty_scaling=True,ideal_gas_density_relative_error=abs(low['density_kg_m3']/ideal-1),eight_fixed_air_cooling_rejected=True),sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'nitrogen_brayton.py',D/'brayton-cooler-results.json',D/'brayton-fan-pump-results.json']})
 (D/'nitrogen-brayton-results.json').write_text(json.dumps(out,indent=2)+'\n')
 for k,c in candidates.items():print(k, 'shaft kW',round(c['available_shaft_W']/1000,2),'air approach K',round(c['minimum_air_approach_K'],2),'UA kW/K',None if c['required_counterflow_UA_W_K'] is None else round(c['required_counterflow_UA_W_K']/1000,2),'30MW margin kW',round(c['remaining_electric_30MW_W']/1000,2))
 print('sensitivity shaft kW',[x['available_shaft_W']/1000 for x in sensitivity])
if __name__=='__main__':main()
