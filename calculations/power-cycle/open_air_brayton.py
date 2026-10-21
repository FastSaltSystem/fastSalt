"""Externally heated open-air Brayton comparison. No combustion or recuperator."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import json,math,hashlib,re
import CoolProp
from CoolProp.CoolProp import PropsSI as P
D=Path(__file__).resolve().parent;F='HEOS::Air'
def state(p,t=None,h=None):
 if h is None:h=P('H','P',p,'T',t,F)
 t=P('T','P',p,'H',h,F)
 return dict(p_Pa=p,T_K=t,T_C=t-273.15,h_J_kg=h,s_J_kgK=P('S','P',p,'H',h,F),rho_kg_m3=P('D','P',p,'H',h,F))
def solve(ratio,ambient=303.15,eta_c=.85,eta_t=.88,intake_loss=500,exhaust_loss=1000,heater_loss=.02,duty=1e7):
 p0=101325;p1=p0-intake_loss;p2=p1*ratio;p3=p2*(1-heater_loss);p4=p0+exhaust_loss
 a0=state(p0,t=ambient);a=state(p1,h=a0['h_J_kg'])
 h2=a['h_J_kg']+(P('H','P',p2,'S',a['s_J_kgK'],F)-a['h_J_kg'])/eta_c;b=state(p2,h=h2)
 c=state(p3,t=830);h4=c['h_J_kg']-eta_t*(c['h_J_kg']-P('H','P',p4,'S',c['s_J_kgK'],F));d=state(p4,h=h4);e=state(p0,h=h4)
 q=c['h_J_kg']-h2;wc=h2-a['h_J_kg'];wt=c['h_J_kg']-h4;out=h4-a0['h_J_kg'];m=duty/q
 assert min(q,wc,wt,out)>0 and abs(q-out-wt+wc)<1e-6
 assert b['s_J_kgK']>a['s_J_kgK'] and d['s_J_kgK']>c['s_J_kgK']
 return dict(ratio=ratio,inputs=dict(ambient_K=ambient,intake_loss_Pa=intake_loss,exhaust_loss_Pa=exhaust_loss,heater_fractional_loss=heater_loss,eta_c=eta_c,eta_t=eta_t,heat_W=duty),states=dict(ambient=a0,compressor_inlet=a,heater_inlet=b,turbine_inlet=c,turbine_outlet=d,atmospheric_exhaust=e),mass_kg_s=m,inlet_volume_m3_s=m/a['rho_kg_m3'],exhaust_volume_m3_s=m/e['rho_kg_m3'],compressor_W=m*wc,turbine_W=m*wt,shaft_loss_W=.02*m*wt,available_shaft_W=m*(.98*wt-wc),electric_W=.95*m*(.98*wt-wc),exhaust_heat_above_ambient_W=m*out,energy_residual_J_kg=q-out-wt+wc)

def main():
 lo,hi=2.,8.
 for _ in range(55):
  mid=(lo+hi)/2
  if solve(mid)['states']['heater_inlet']['T_K']<560:lo=mid
  else:hi=mid
 matched=solve((lo+hi)/2);cases=[solve(2),solve(4),matched,solve(8)]
 pump=json.loads((D/'brayton-fan-pump-results.json').read_text())['cases'][0]['pump_electric_W']
 for c in cases:c['margin_at_30MW_W']=3*c['electric_W']-pump
 sensitivity=[solve(matched['ratio'],ambient=318.15),solve(matched['ratio'],eta_c=.8,eta_t=.85),solve(matched['ratio'],heater_loss=.05,exhaust_loss=5000)]
 assert abs(matched['states']['heater_inlet']['T_K']-560)<1e-7
 assert abs(solve(matched['ratio'],duty=2e7)['electric_W']/matched['electric_W']-2)<1e-9
 n=json.loads((D/'nitrogen-brayton-results.json').read_text())['cases'];checks={};lines=[]
 def add(s):lines.append(s)
 def inp(n,v,u=''):add(f'¢` {n} = {v:.14g} {u} `')
 def calc(n,e,v,u=''):add(f'¢` {n} = {e} = ?? {u} `');checks[n]=v
 add('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
saveDate: 2026-10-13
---------------

# Open-air Brayton auxiliary cooler — preliminary comparison

13 October 2026. Compare an externally heated open cycle with the preserved [closed steam](Steam%20Brayton%20cooler%20-%20Hurmet.md) and [closed nitrogen](Nitrogen%20versus%20steam%20Brayton%20-%20Hurmet.md) trials. Flow is **outside air → intake/filter → compressor → salt-to-air heater → turbine → exhaust duct → atmosphere**. The turbine drives the compressor and an alternator serving the salt pump. There is no combustion, recuperator, separate air cooler or separate cooler fan in this trial.

Real dry-air properties use CoolProp 7.2.0 HEOS::Air and its [Lemmon et al. equation of state](https://coolprop.sourceforge.net/fluid_properties/fluids/Air.html). Humidity and weather-related intake-system behavior are not modeled. Outside air is 30°C at 101.325 kPa. Intake/filter loss is provisionally 500 Pa; turbine exhaust backpressure is 1,000 Pa above atmosphere. Heater pressure loss is 2% of compressor discharge. These are assumed total-pressure budgets, not verified duct/filter/exchanger losses. Gas kinetic and elevation terms are neglected in the station energy balances. Intake and final exhaust pressure losses are treated as adiabatic throttles.

Compressor/turbine isentropic efficiencies remain 85%/88%; turbine shaft-transfer efficiency is 98% and alternator efficiency 95%. Turbine inlet stays at 830 K (556.85°C). Unlike the closed trials, compressor inlet temperature is set by outside air, so heater inlet temperature follows from compression ratio. The compressor supplies the pressure needed for the complete air path; adding another fan deduction would double-count that duty unless additional hardware/losses are introduced.

## Pressure-ratio comparison, each at 10 MW salt-to-air heat input''')
 add('| Quantity | 2:1 | 4:1 | Matched heater inlet | 8:1 |\n| --- | --- | --- | --- | --- |')
 for label,fn in [('Compressor pressure ratio',lambda c:c['ratio']),('Heater inlet, °C',lambda c:c['states']['heater_inlet']['T_C']),('Turbine exhaust, °C',lambda c:c['states']['turbine_outlet']['T_C']),('Air mass flow, kg/s',lambda c:c['mass_kg_s']),('Compressor-inlet volume, m³/s',lambda c:c['inlet_volume_m3_s']),('Atmospheric exhaust volume, m³/s',lambda c:c['exhaust_volume_m3_s']),('Compressor shaft demand, MW',lambda c:c['compressor_W']/1e6),('Surplus shaft power, MW',lambda c:c['available_shaft_W']/1e6),('Available electricity, MW',lambda c:c['electric_W']/1e6)]:add('| '+label+' | '+' | '.join(f'{fn(c):.4g}' for c in cases)+' |')
 add('''The approximately 6.8:1 case reproduces the existing 560/830 K heater endpoints and is the principal comparison. The 4:1 case has slightly more surplus per unit heat in this limited sweep but admits air to the heater at about 202°C. Its larger cold-end temperature difference requires a new local wall-temperature and salt-freezing assessment. Neither case establishes the optimal ratio.

## Comparison at the same 287/557°C heater endpoints''')
 add('| Per 10 MW heat input | Closed steam 2:1 | Closed nitrogen 4:1 | Open air matched |\n| --- | --- | --- | --- |')
 add('| Compressor pressure range, bar absolute | 5→10 | 10→40 | '+f'{matched["states"]["compressor_inlet"]["p_Pa"]/1e5:.3f}→{matched["states"]["heater_inlet"]["p_Pa"]/1e5:.3f}'+' |')
 for label,vals in [('Compressor inlet, °C',[n['steam_two']['states']['compressor_inlet']['temperature_C'],n['nitrogen_four']['states']['compressor_inlet']['temperature_C'],matched['states']['compressor_inlet']['T_C']]),('Electricity after air-cooler fan, before salt pump, MW',[n['steam_two']['electric_after_fan_W']/1e6,n['nitrogen_four']['electric_after_fan_W']/1e6,matched['electric_W']/1e6]),('Compressor inlet volume, m³/s',[n['steam_two']['inlet_volume_m3_s'],n['nitrogen_four']['inlet_volume_m3_s'],matched['inlet_volume_m3_s']])]:add('| '+label+' | '+' | '.join(f'{x:.4g}' for x in vals)+' |')
 add('''This compares complete candidate operating points; it does not attribute the gain solely to replacing nitrogen with air. The open cycle draws colder ambient air directly, changes the pressure ratio and removes the closed-loop cooler pressure loss and fan. A closed loop cannot cool exactly to ambient with a finite dry exchanger. Open-air inlet volume is about 8.4 times the pressurized nitrogen candidate's volume, although total installed footprints cannot be inferred from volume alone. The nitrogen alternative still has its separate large air cooler and fan.

## 30 MW-per-leg illustration''')
 add(f'''Scaling the matched-temperature open cycle to 30 MW gives **{3*matched['mass_kg_s']:.1f} kg/s** of air, **{3*matched['inlet_volume_m3_s']:.1f} m³/s** compressor inlet volume and **{3*matched['exhaust_volume_m3_s']:.1f} m³/s** atmospheric hot exhaust. Available electricity is **{3*matched['electric_W']/1e6:.3f} MW**. Subtract the prior **{pump/1000:.0f} kW** salt-pump demand for a 10 K salt drop and retain **{matched['margin_at_30MW_W']/1e6:.3f} MW**. The closed nitrogen 4:1 case retained 2.379 MW, and closed steam 2:1 retained 0.432 MW under their respective assumptions.

The exhaust carries approximately **{3*matched['exhaust_heat_above_ambient_W']/1e6:.2f} MW** above inlet-air enthalpy. The balance leaves as work and machinery losses. This is not an additional heat-removal duty to add to the 30 MW taken from salt. Net reactor cooling remains about 29.88–29.90 MW after heat returned by the same salt pump, before other heat gains.

At a purely illustrative 15 m/s exhaust-duct velocity, the matched 30 MW case needs about {3*matched['exhaust_volume_m3_s']/15:.1f} m² flow area, equivalent to a {math.sqrt(4*(3*matched['exhaust_volume_m3_s']/15)/math.pi):.2f} m round duct. This is a flow-area allowance, not a stack design; duct length, bends, discharge velocity, noise treatment, weather and recirculation must fit within a verified backpressure budget. Cooler removal does not eliminate hot-air discharge routing.''')
 add('''## Implications for the reactor installation

The component arrangement is simpler: no secondary air cooler, its fan or closed working-gas inventory system. The open process air passes through the heater on the other side of a metal boundary from salt; it is not direct air contact with salt or reactor-room ventilation. The heater boundary must keep process contaminants out of the discharged stream. Leak detection, isolation and the response to a failed boundary therefore matter to deciding whether open discharge is acceptable. This calculation assumes an intact separating heat exchanger and does not characterize exhaust releases.

Open operation gives up adjustable high suction pressure as a way to shrink turbomachinery. It also introduces outside-air moisture and oxygen into the gas-side equipment, so materials and the shared-generator drying/isolation arrangement need checking. Salt-to-air heat-transfer performance and pressure loss must be verified; the existing steam-generator pressure rating alone does not establish this service. A dedicated exchanger remains an option rather than an adopted design.

Startup still needs an initial drive source, and cooler outlet/salt freeze controls remain required. Ambient-temperature changes alter compressor discharge and power margin; these are fixed-state capacity comparisons, not validated startup, cooldown or off-design maps. Residual electricity needs a useful load or a defined control strategy. A recuperator would be an additional component and is not assumed for this heat-removal objective.

## Sensitivities at the matched pressure ratio

These trials keep turbine inlet at 557°C, compressor ratio fixed and heat input at 10 MW; the heater inlet temperature is allowed to change.''')
 add('| Separate sensitivity | Heater inlet, °C | Surplus shaft power, MW |\n| --- | --- | --- |')
 for label,c in zip(['45°C outside air','80% compressor / 85% turbine efficiency','5% heater loss / 5 kPa exhaust backpressure'],sensitivity):add(f'| {label} | {c["states"]["heater_inlet"]["T_C"]:.1f} | {c["available_shaft_W"]/1e6:.3f} |')
 add('## Hurmet verification of the matched-temperature 10 MW case')
 for name,v,u in [('HeatDuty',10,'MW'),('ShaftEfficiency',.98,''),('GeneratorEfficiency',.95,''),('PumpAtThirtyMW',pump/1000,'kW'),('InletDensity',matched['states']['compressor_inlet']['rho_kg_m3'],'kg/m3'),('ExhaustDensity',matched['states']['atmospheric_exhaust']['rho_kg_m3'],'kg/m3')]:inp(name,v,u)
 for name,k in [('HOne','compressor_inlet'),('HTwo','heater_inlet'),('HThree','turbine_inlet'),('HFour','turbine_outlet')]:inp(name,matched['states'][k]['h_J_kg'],'J/kg')
 for name,e,v,u in [('MassFlow','HeatDuty / (HThree - HTwo)',matched['mass_kg_s'],'kg/s'),('CompressorPower','MassFlow * (HTwo - HOne)',matched['compressor_W']/1e6,'MW'),('TurbinePower','MassFlow * (HThree - HFour)',matched['turbine_W']/1e6,'MW'),('AvailableShaft','ShaftEfficiency * TurbinePower - CompressorPower',matched['available_shaft_W']/1e6,'MW'),('AvailableElectricity','GeneratorEfficiency * AvailableShaft',matched['electric_W']/1e6,'MW'),('ExhaustHeat','MassFlow * (HFour - HOne)',matched['exhaust_heat_above_ambient_W']/1e6,'MW'),('EnergyResidual','HeatDuty - ExhaustHeat - TurbinePower + CompressorPower',0,'MW'),('InletFlow','MassFlow / InletDensity',matched['inlet_volume_m3_s'],'m3/s'),('ExhaustFlow','MassFlow / ExhaustDensity',matched['exhaust_volume_m3_s'],'m3/s'),('ThirtyMWMargin','3 * AvailableElectricity - PumpAtThirtyMW',matched['margin_at_30MW_W']/1e6,'MW')]:calc(name,e,v,u)
 add('''Real-air state enthalpies are imported from Python; Hurmet recalculates energy and flow at those fixed states. The last formula specifically assumes the 10 MW normalization and uses the prior 30 MW salt-pump demand. Summary tables are imported snapshots. Change temperatures, efficiencies or pressure losses in Python and rerun rather than treating imported states as live property calls.

## Reproduction and status

Run `open_air_brayton.py` in the project's CoolProp environment, then `check_open_air_brayton.cjs` with the existing Hurmet/Temml engine paths. Python checks energy, entropy, matching the heater inlet and duty scaling. JSON preserves all states, source hashes and sensitivities. Hurmet checks ten numerical results, save/reopen and alternator-efficiency sensitivity. No cooling architecture, exchanger or turbine rating is selected by this preliminary screen.''')
 text='\n\n'.join(lines)+'\n';text=re.sub(r'(?m)(^\|.*\|)\n\n(?=\|)',r'\1\n',text)
 # Use standard pipe tables for VS Code and GitHub; the checker preserves them.
 write_worksheet(D/'Open-air Brayton cooler - Hurmet.md', text)
 out=dict(date='2026-10-13',property_model='CoolProp '+CoolProp.__version__+' HEOS::Air',cases=cases,matched=matched,sensitivity=sensitivity,checks=dict(energy_entropy=True,matched_heater_inlet=True,duty_scaling=True),hurmet_checks=checks,source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'open_air_brayton.py',D/'nitrogen-brayton-results.json',D/'brayton-fan-pump-results.json']})
 (D/'open-air-brayton-results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'matched_ratio':matched['ratio'],'shaft_MW':matched['available_shaft_W']/1e6,'electric_30MW_margin_MW':matched['margin_at_30MW_W']/1e6,'sensitivities_MW':[x['available_shaft_W']/1e6 for x in sensitivity],'checks':len(checks)},indent=2))
if __name__=='__main__':main()
