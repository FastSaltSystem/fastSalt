"""Check the frozen-cycle pipe allowances over the accepted cooling cases."""
import sys,json,math
from pathlib import Path
from CoolProp.CoolProp import PropsSI
ROOT=Path(sys.argv[1]);OUT=Path(sys.argv[2])
sys.path.insert(0,str(ROOT));import reheat_model as model
r=json.loads((ROOT/'reheat-selection.json').read_text());e=json.loads((OUT/'equipment-sizing.json').read_text())
results=[]
for c in r['cooling_cases']:
 s=model.solve(**r['selection'],pc=c['condenser_kPa']*1000,plp3=r['selected_at_5kPa']['inputs']['plp3'])
 m=s['mass'];f=s['fractions'];condmass=s['condenser_mass']
 flows=[m,m/3,m*(1-f['reheat']),m*f['reheat'],m*f['reheat'],s['reheat_flow'],s['reheat_flow'],condmass,m,m/3,m,condmass]+[m*f[k] for k in ['HP4','HP3','HP2','HP1','LP3','LP2','LP1']]+[m*f['pump_turbine'],m*(f['pump_turbine']-f['HP2']-f['HP1'])]
 ratios=[]
 for q,mf in zip(e['pipes'],flows):
  st=s['states'][q['state']];rho=PropsSI('D','P',st['p'],'H',st['h'],'HEOS::Water');v=mf/rho/(q['parallel']*math.pi*q['bore_m']**2/4);ratios.append(v/q['velocity_limit_m_s']);assert v<=q['velocity_limit_m_s']*(1+1e-9),(c['inlet_C'],q['service'],v)
 st=s['states']['LPex'];vol=s['exhaust_mass']/PropsSI('D','P',st['p'],'H',st['h'],'HEOS::Water');assert vol<e['turbines']['LP_exhaust_volume_m3_s']
 results.append(dict(inlet_C=c['inlet_C'],max_pipe_velocity_fraction=max(ratios),LP_exhaust_volume_m3_s=vol))
e['cooling_envelope_checks']=results;e['checks'].append('all selected bores meet their assumed velocity screens in 20/30/35°C cooling cases; 5 kPa bounds LP volume')
(OUT/'equipment-sizing.json').write_text(json.dumps(e,indent=2)+'\n');print(json.dumps(results,indent=2))
