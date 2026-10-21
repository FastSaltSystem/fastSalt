"""Simple unrecuperated high-pressure CO2 heat-removal screen; separate dry cooler.
Does not calculate the students' steam-generator emergency air passages.
"""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json,math,hashlib,re
import CoolProp
from CoolProp.CoolProp import PropsSI as P
from nitrogen_brayton import solve as nitrogen_solve,cooler as nitrogen_cooler
D=Path(__file__).resolve().parent;F='HEOS::CO2'
def state(p,t=None,h=None):
 if h is None:h=P('H','P',p,'T',t,F)
 t=P('T','P',p,'H',h,F)
 return dict(p_Pa=p,T_K=t,T_C=t-273.15,h_J_kg=h,s_J_kgK=P('S','P',p,'H',h,F),rho_kg_m3=P('D','P',p,'H',h,F))
def solve(t1,p1=10e6,p2=20e6,duty=30e6,ec=.85,et=.88,loss=.02,steps=600):
 p3=p2*(1-loss);p4=p1/(1-loss)
 a=state(p1,t=t1);h2=a['h_J_kg']+(P('H','P',p2,'S',a['s_J_kgK'],F)-a['h_J_kg'])/ec;b=state(p2,h=h2)
 c=state(p3,t=830);h4=c['h_J_kg']-et*(c['h_J_kg']-P('H','P',p4,'S',c['s_J_kgK'],F));d=state(p4,h=h4)
 q=c['h_J_kg']-h2;out=h4-a['h_J_kg'];wc=h2-a['h_J_kg'];wt=c['h_J_kg']-h4;m=duty/q
 assert abs(q-out-wt+wc)<1e-6 and min(q,out,wc,wt)>0
 assert b['s_J_kgK']>a['s_J_kgK'] and d['s_J_kgK']>c['s_J_kgK']
 assert min(p1,p2,p3,p4)>P('Pcrit',F) and min(s['T_K'] for s in [a,b,c,d])>P('Tcrit',F)
 ds=[]
 for j in range(steps+1):
  x=j/steps;ds.append(P('T','P',p1+x*(p4-p1),'H',a['h_J_kg']+x*out,F)-(303.15+100*x))
 assert min(ds)>0
 rejected=m*out;airflow=rejected/(1007*100)/(101325/(287.05*303.15));fan=airflow*500/.65/.96
 ua=rejected*sum((1/ds[i]+1/ds[i+1])/2/steps for i in range(steps))
 shaft=m*(.98*wt-wc)
 return dict(inputs=dict(T1_K=t1,p_low_Pa=p1,p_high_Pa=p2,heat_W=duty,eta_c=ec,eta_t=et,loss_each=loss),states=dict(compressor_inlet=a,heater_inlet=b,turbine_inlet=c,cooler_inlet=d),mass_kg_s=m,inlet_m3_s=m/a['rho_kg_m3'],hot_return_m3_s=m/d['rho_kg_m3'],compressor_W=m*wc,turbine_W=m*wt,available_shaft_W=shaft,electric_W=.95*shaft,air_heat_W=rejected,air_volume_m3_s=airflow,face_m2=airflow/3,fan_electric_W=fan,electric_after_fan_W=.95*shaft-fan,cooler_UA_W_K=ua,minimum_air_approach_K=min(ds),energy_residual_J_kg=q-out-wt+wc)

def main():
 lo,hi=373.15,573.15
 for _ in range(55):
  mid=(lo+hi)/2
  # Avoid repeating cooler integration during temperature root solve.
  a=state(10e6,t=mid);h2=a['h_J_kg']+(P('H','P',20e6,'S',a['s_J_kgK'],F)-a['h_J_kg'])/.85
  if state(20e6,h=h2)['T_K']<560:lo=mid
  else:hi=mid
 matched=solve((lo+hi)/2);warm=solve(373.15);dense=solve(313.15)
 pump=json.loads((D/'brayton-fan-pump-results.json').read_text())['cases'][0]['pump_electric_W']
 for c in [matched,warm,dense]:c['margin_after_pump_W']=c['electric_after_fan_W']-pump
 assert abs(matched['states']['heater_inlet']['T_K']-560)<1e-7
 double=solve((lo+hi)/2,duty=60e6)
 assert abs(double['available_shaft_W']/matched['available_shaft_W']-2)<1e-9
 fine=solve(313.15,steps=1200);grid_error=abs(fine['cooler_UA_W_K']/dense['cooler_UA_W_K']-1);assert grid_error<.001
 high_n=nitrogen_cooler(nitrogen_solve(ratio=2,p_low=10e6,duty=30e6));high_n['margin_after_pump_W']=high_n['electric_after_fan_W']-pump
 bad=solve((lo+hi)/2,ec=.8,et=.85);bad['margin_after_pump_W']=bad['electric_after_fan_W']-pump
 lines=[];checks={}
 def add(s):lines.append(s)
 def inp(n,v,u=''):add(f'¢` {n} = {v:.14g} {u} `')
 def calc(n,e,v,u=''):add(f'¢` {n} = {e} = ?? {u} `');checks[n]=v
 add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-13
---------------

# Simple supercritical CO₂ loop — compact heat-removal screen

13 October 2026. Investigate compact heat removal, rather than maximizing electrical efficiency. **The emergency air passages built into the steam generators are reserved for the student team's educational calculation and are not analyzed here.** This screen concerns a separate closed CO₂ working-fluid loop and its own outdoor heat-rejection exchanger.

Flow is **CO₂ compressor → salt-to-CO₂ heater → turbine → separate dry cooler → compressor**. The turbine drives the compressor and an alternator serving the salt pump and cooler fan. There is no recuperator, recompressor or intercooler. Omitting recuperators avoids components used primarily to improve power-cycle efficiency; it does not remove the requirement to reject heat to the environment.

Use CoolProp 7.2.0 HEOS::CO₂ and the [Span–Wagner property model](https://coolprop.org/fluid_properties/fluids/CarbonDioxide.html). CO₂ critical conditions are about 31°C and 7.38 MPa. All four state points here remain above both. [DOE describes high working-fluid density as a source of compact turbomachinery](https://www.energy.gov/sco2-rd-focus-areas); that does not establish complete-system footprint.

## Common assumptions

Low/high compressor pressure: **10/20 MPa (100/200 bar)**. Turbine inlet: 830 K (556.85°C). Compressor/turbine efficiencies: 85%/88%; shaft transfer 98%; alternator 95%. Pressure loss is 2% through each exchanger. Salt heat transfer is 30 MW per train, a comparison duty rather than a specified emergency load.

The outdoor cooler retains 30→130°C air, 500 Pa total air loss, 65% fan efficiency and 96% motor efficiency. Salt-pump electricity remains 130 kW from the earlier 30 MW case with a 10 K salt drop and generator pressure loss plus 50%. There is no credit for heat rejection through the students' steam-generator air passages. Constant machine efficiencies and exchanger losses are provisional, not selected equipment performance.

## Compare warm and near-critical compressor inlets''')
 add('| Per 30 MW heat input | Match existing heater inlet | 100°C compressor inlet | 40°C compressor inlet |\n| --- | --- | --- | --- |')
 cases=[matched,warm,dense]
 for label,fn in [('Compressor inlet, °C',lambda c:c['states']['compressor_inlet']['T_C']),('Heater inlet, °C',lambda c:c['states']['heater_inlet']['T_C']),('Compressor inlet density, kg/m³',lambda c:c['states']['compressor_inlet']['rho_kg_m3']),('CO₂ mass flow, kg/s',lambda c:c['mass_kg_s']),('Compressor inlet volume, m³/s',lambda c:c['inlet_m3_s']),('Hot low-pressure return volume, m³/s',lambda c:c['hot_return_m3_s']),('Compressor shaft demand, MW',lambda c:c['compressor_W']/1e6),('Turbine shaft power, MW',lambda c:c['turbine_W']/1e6),('Available shaft power, MW',lambda c:c['available_shaft_W']/1e6),('Electrical margin after fan and salt pump, MW',lambda c:c['margin_after_pump_W']/1e6),('Heat to separate air cooler, MW',lambda c:c['air_heat_W']/1e6),('Air cooler face at 3 m/s, m²',lambda c:c['face_m2']),('Ideal-counterflow cooler UA, kW/K',lambda c:c['cooler_UA_W_K']/1000)]:add('| '+label+' | '+' | '.join(f'{fn(c):,.4g}' for c in cases)+' |')
 add('''The matched-temperature case holds the prior 287/557°C heater endpoints and obtains approximately 204°C compressor inlet. It gives 0.75 m³/s inlet volume and 1.27 m³/s hot return, compared with 10.7/17.8 m³/s for the earlier 10→40 bar nitrogen candidate and 21.6/34.2 m³/s for steam. At an illustrative 30 m/s velocity, the CO₂ equivalent flow bores are about 0.18 and 0.23 m. These exclude pressure wall, insulation and fittings; they are not turbine or compressor diameters and do not validate a pipe design at 20 MPa.

The cold 40°C case makes the compressor exceptionally small in flow terms, but requires about **770 kW/K of cooler UA**, versus **114 kW/K** in the warm matched case. The sharp near-critical property variation creates a small internal temperature approach (about 9 K for this air profile). Chasing maximum density or efficiency can therefore worsen the external heat-rejection requirement. The 100°C inlet is an intermediate trial with a 168°C heater inlet; it changes the salt-side cold-end thermal conditions and requires a fresh local wall/freezing check. No such check is inferred from low overall duty.

## How much of the compactness comes from pressure?

The original nitrogen comparison used 10–40 **bar**, whereas this CO₂ loop uses 100–200 **bar**. It would be misleading to attribute the entire volume reduction to the choice of CO₂. A supplementary nitrogen case at the same 100–200 bar and 287/557°C heater endpoints gives approximately **1.35 m³/s** compressor inlet, **12.46 MW** compressor duty and **0.375 MW** electrical margin after the same fan/pump allowances. CO₂ gives 0.75 m³/s, 6.64 MW and 0.655 MW respectively. It still has an advantage in this screen, but the same-pressure comparison is much less dramatic than comparison with lower-pressure nitrogen.

## Compact machinery does not mean a tiny heat sink

The warm CO₂ case still sends about **28.8 MW** to the air cooler, requiring about **246 m³/s** of cold air under the retained 100 K air-rise assumption. The approximately **82 m² airflow face** is almost unchanged from the steam case. This is a flow-area screen, not a thermal exchanger rating or installed footprint. A selected gas-side coefficient, fin area, core depth, manifolds and fan/duct arrangement must satisfy both heat transfer and the pressure-loss budget.

The smaller process-flow passages and lower compressor shaft power support investigating a smaller machinery package; they do not justify scaling the earlier machinery box directly by volume flow or claiming a vendor footprint. Pressure containment, bearings, seals, rotational speed and stage arrangement remain unselected. The earlier 500–600 m² layout reservations should not be copied to CO₂ as established dimensions.

Higher air outlet temperature could reduce required airflow, but that option also exists for steam and nitrogen. It would change cooler driving temperatures and discharge constraints; it is not a unique benefit of CO₂. Lower power-cycle efficiency is acceptable if enough work remains for auxiliaries, but it also means most salt heat must be rejected through the cooler rather than exported electrically.

## Integration and operating scope

A simple high-pressure loop is the candidate being screened, not the more complex recuperated cycles used to maximize generation efficiency. The salt-to-CO₂ heater may reuse existing generator passages only if heat transfer, pressure loss, materials and isolation/changeover are verified; otherwise a dedicated heater is another unsized component. CO₂ suitability and a failed separating-boundary response require review. A nominal pressure below the normal steam operating pressure alone does not establish compatibility.

Warm compression avoids making the normal operating point depend on cooling within a few degrees of the critical temperature. Charge/inventory control, startup drive and pressure containment remain required. Colder shutdown conditions can enter other fluid regimes. Maintaining the modeled hot temperature as reactor temperature falls is not assumed to be an established operating map. At the same compressor-inlet temperature, reducing compressor/turbine efficiencies to 80%/85% leaves only about **12 kW** after the modeled fan and salt pump, before controls or other loads. The nominal matched case therefore has limited robustness to machine performance; positive nominal margin is not a reliability demonstration. The student emergency-air-passage study remains an independent alternative.

## Hurmet verification of the matched-temperature case''')
 for name,v,u in [('HeatDuty',30,'MW'),('ShaftEfficiency',.98,''),('GeneratorEfficiency',.95,''),('FanEfficiency',.65,''),('MotorEfficiency',.96,''),('AirRise',100,'K'),('AirHeatCapacity',1007,'J.kg-1.K-1'),('AirDensity',101325/(287.05*303.15),'kg/m3'),('AirPressureDrop',500,'Pa'),('FaceVelocity',3,'m/s'),('PumpPower',pump/1000,'kW'),('InletDensity',matched['states']['compressor_inlet']['rho_kg_m3'],'kg/m3'),('HotDensity',matched['states']['cooler_inlet']['rho_kg_m3'],'kg/m3')]:inp(name,v,u)
 for name,k in [('HOne','compressor_inlet'),('HTwo','heater_inlet'),('HThree','turbine_inlet'),('HFour','cooler_inlet')]:inp(name,matched['states'][k]['h_J_kg'],'J/kg')
 for name,e,v,u in [('MassFlow','HeatDuty / (HThree - HTwo)',matched['mass_kg_s'],'kg/s'),('InletFlow','MassFlow / InletDensity',matched['inlet_m3_s'],'m3/s'),('HotFlow','MassFlow / HotDensity',matched['hot_return_m3_s'],'m3/s'),('CompressorPower','MassFlow * (HTwo - HOne)',matched['compressor_W']/1e6,'MW'),('TurbinePower','MassFlow * (HThree - HFour)',matched['turbine_W']/1e6,'MW'),('AvailableShaft','ShaftEfficiency * TurbinePower - CompressorPower',matched['available_shaft_W']/1e6,'MW'),('CoolerHeat','MassFlow * (HFour - HOne)',matched['air_heat_W']/1e6,'MW'),('EnergyResidual','HeatDuty - CoolerHeat - TurbinePower + CompressorPower',0,'MW'),('AirFlow','CoolerHeat / (AirHeatCapacity * AirRise * AirDensity)',matched['air_volume_m3_s'],'m3/s'),('FaceArea','AirFlow / FaceVelocity',matched['face_m2'],'m2'),('FanPower','AirFlow * AirPressureDrop / (FanEfficiency * MotorEfficiency)',matched['fan_electric_W']/1000,'kW'),('RemainingElectricity','GeneratorEfficiency * AvailableShaft - FanPower - PumpPower',matched['margin_after_pump_W']/1000,'kW')]:calc(name,e,v,u)
 add('''Real-fluid states and integrated counterflow UA are imported from Python; Hurmet independently checks power, heat and flow. Changing state temperatures/pressures requires a Python rerun. Changing heat duty alone scales fixed-state machinery, while the pump input remains the specific 30 MW estimate and must also be recalculated for a different salt duty. Summary tables are snapshots.

Run `co2_brayton.py` in the existing CoolProp environment, then `check_co2_brayton.cjs` with Hurmet/Temml configured. JSON records the matched-temperature solve, pressure/temperature states, source hashes, energy/entropy checks, duty scaling and cooler-integration convergence. Twelve Hurmet numerical checks, save/reopen and air-pressure sensitivity are verified. These establish numerical consistency, not selected hardware or qualified emergency cooling.''')
 t='\n\n'.join(lines)+'\n';t=re.sub(r'(?m)(^\|.*\|)\n\n(?=\|)',r'\1\n',t)
 def widths(m):
  b=m.group(0);count=b.splitlines()[0].count('|')-1
  return b+'\n{.grid colWidths="'+' '.join(['250']+['125']*(count-1))+'"}'
 t=re.sub(r'(?m)^\|.*(?:\n\|.*)*',widths,t)
 write_worksheet(D/'Simple CO2 Brayton cooler - Hurmet.md', t)
 sources=[D/'co2_brayton.py',D/'nitrogen_brayton.py',D/'brayton-fan-pump-results.json']
 out=dict(date='2026-10-13',property_model='CoolProp '+CoolProp.__version__+' HEOS::CO2',matched=matched,warm=warm,near_critical=dense,same_pressure_nitrogen=high_n,lower_machine_efficiencies=bad,checks=dict(energy_entropy=True,above_critical_state_points=True,duty_scaling=True,UA_grid_relative_change=grid_error),hurmet_checks=checks,source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
 (D/'co2-brayton-results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'matched_margin_kW':matched['margin_after_pump_W']/1000,'matched_inlet_m3_s':matched['inlet_m3_s'],'nitrogen_same_pressure_margin_kW':high_n['margin_after_pump_W']/1000,'lower_efficiencies_margin_kW':bad['margin_after_pump_W']/1000,'grid_error':grid_error,'hurmet_checks':len(checks)},indent=2))
if __name__=='__main__':main()
