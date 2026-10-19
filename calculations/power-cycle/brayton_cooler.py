"""Preliminary non-condensing steam Brayton heat-removal screen.

Real water properties from CoolProp HEOS / IAPWS-95. Retains the current
steam-generator TEMPERATURE endpoints, not its normal Rankine pressure.
No exchanger, salt-freezing, startup or turbomachinery-map qualification.
"""
from pathlib import Path
import json,hashlib,csv
import CoolProp
from CoolProp.CoolProp import PropsSI,PhaseSI
ROOT=Path(__file__).resolve().parent
F='HEOS::Water'
def prop(out,a,x,b,y):return PropsSI(out,a,x,b,y,F)
def state(p,t=None,h=None):
    if h is None:h=prop('H','P',p,'T',t)
    t=prop('T','P',p,'H',h)
    return dict(pressure_Pa=p,temperature_K=t,temperature_C=t-273.15,enthalpy_J_kg=h,
                entropy_J_kg_K=prop('S','P',p,'H',h),density_kg_m3=prop('D','P',p,'H',h),
                superheat_K=t-prop('T','P',p,'Q',1) if p<prop('Pcrit','T',300,'P',1e5) else None,phase=PhaseSI('P',p,'H',h,F))

def solve(ratio=2,p_low=5e5,eta_c=.85,eta_t=.88,eta_shaft=.98,loss=.02,t_heater_in=560,t_hot=830,duty=1e7):
    p1=p_low;p2=p1*ratio;p3=p2*(1-loss);p4=p1/(1-loss)
    assert p3>p4
    b=state(p2,t=t_heater_in)
    if b['superheat_K']<=0:return dict(state_solution_valid=False,reason='Heater inlet is not dry steam')
    def residual(t):
        a=state(p1,t=t);hs=prop('H','P',p2,'S',a['entropy_J_kg_K'])
        return a['enthalpy_J_kg']+(hs-a['enthalpy_J_kg'])/eta_c-b['enthalpy_J_kg']
    lo=prop('T','P',p1,'Q',1)+.01;hi=t_heater_in-.01
    if lo>=hi or residual(lo)>0:return dict(state_solution_valid=False,reason='Specified heater inlet requires a wet compressor inlet')
    assert residual(hi)>0
    for _ in range(55):
        mid=(lo+hi)/2
        if residual(mid)>0:hi=mid
        else:lo=mid
    a=state(p1,t=(lo+hi)/2);c=state(p3,t=t_hot)
    h4s=prop('H','P',p4,'S',c['entropy_J_kg_K'])
    d=state(p4,h=c['enthalpy_J_kg']-eta_t*(c['enthalpy_J_kg']-h4s))
    h1,h2,h3,h4=[s['enthalpy_J_kg'] for s in (a,b,c,d)]
    wc=h2-h1;wt=h3-h4;qin=h3-h2;qout=h4-h1
    assert min(wc,wt,qin,qout)>0
    energy=qin-qout-wt+wc;assert abs(energy)<1e-6
    assert b['entropy_J_kg_K']>=a['entropy_J_kg_K'] and d['entropy_J_kg_K']>=c['entropy_J_kg_K']
    # Check dry vapor along both exchanger paths and actual/isentropic
    # turbomachinery paths. HX paths assume linear p(h); no UA is inferred.
    min_superheat=1e9
    for j in range(41):
        f=j/40
        for start,end in [(b,c),(d,a)]:
            pp=start['pressure_Pa']+f*(end['pressure_Pa']-start['pressure_Pa'])
            hh=start['enthalpy_J_kg']+f*(end['enthalpy_J_kg']-start['enthalpy_J_kg'])
            ss=state(pp,h=hh);min_superheat=min(min_superheat,ss['superheat_K'])
        pp=p1+f*(p2-p1);his=prop('H','P',pp,'S',a['entropy_J_kg_K'])
        for hh in [his,h1+(his-h1)/eta_c]:min_superheat=min(min_superheat,state(pp,h=hh)['superheat_K'])
        pp=p3+f*(p4-p3);his=prop('H','P',pp,'S',c['entropy_J_kg_K'])
        for hh in [his,h3-eta_t*(h3-his)]:min_superheat=min(min_superheat,state(pp,h=hh)['superheat_K'])
    assert min_superheat>0
    mass=duty/qin;available=mass*(eta_shaft*wt-wc)
    # Optional air-fan screen: not an exchanger design or an established load.
    rho_air=101325/(287.05*303.15);air_mass=mass*qout/(1007*100)
    fan=air_mass/rho_air*500/.65
    return dict(state_solution_valid=True,self_sustaining_before_auxiliaries=available>0,inputs=dict(compressor_ratio=ratio,compressor_inlet_Pa=p_low,
        compressor_efficiency=eta_c,turbine_efficiency=eta_t,shaft_transfer_efficiency=eta_shaft,
        fractional_pressure_loss_each_exchanger=loss,heater_inlet_K=t_heater_in,turbine_inlet_K=t_hot,heat_input_W=duty),
        states=dict(compressor_inlet=a,steam_generator_inlet=b,turbine_inlet=c,air_cooler_inlet=d),
        specific=dict(heat_added_J_kg=qin,heat_rejected_J_kg=qout,turbine_work_J_kg=wt,compressor_work_J_kg=wc),
        steam_flow_kg_s=mass,compressor_inlet_volume_m3_s=mass/a['density_kg_m3'],
        turbine_power_W=mass*wt,compressor_power_W=mass*wc,shaft_losses_W=mass*wt*(1-eta_shaft),
        available_shaft_W=available,heat_rejected_air_cooler_W=mass*qout,
        illustrative_air=dict(inlet_C=30,rise_K=100,cp_J_kg_K=1007,density_inlet_kg_m3=rho_air,
             pressure_drop_Pa=500,fan_efficiency=.65,mass_kg_s=air_mass,fan_power_W=fan),
        after_illustrative_fan_W=available-fan,minimum_sampled_superheat_K=min_superheat,
        energy_residual_J_kg=energy,compressor_inverse_residual_J_kg=residual(a['temperature_K']))

def main():
    base=solve();trials=[]
    for eta_c,eta_t in [(.8,.85),(.85,.88),(.85,.9)]:
        for ratio in (1.5,2,2.5,3):
            q=solve(ratio=ratio,eta_c=eta_c,eta_t=eta_t)
            trials.append(dict(ratio=ratio,eta_c=eta_c,eta_t=eta_t,result=q))
    losses=[dict(loss=x,result=solve(loss=x)) for x in (0,.02,.05)]
    pressures=[dict(p_low=p,result=solve(p_low=p)) for p in (2e5,5e5,1e6)]
    high_ratio_trials=[dict(p_low=p,result=solve(ratio=8,p_low=p)) for p in (5e5,1e5,1e4,5e3)]
    high_ratio=high_ratio_trials[-1]['result']
    assert high_ratio['state_solution_valid']
    h_normal=prop('H','P',24e6,'T',830)
    throttle_trials=[state(p,h=h_normal) for p in (3e6,1e6,4e4)]
    # An independent property formulation checks the four HEOS state enthalpies.
    if97_differences=[]
    for s in list(base['states'].values())+list(high_ratio['states'].values()):
        h=PropsSI('H','P',s['pressure_Pa'],'T',s['temperature_K'],'IF97::Water')
        if97_differences.append(abs(h-s['enthalpy_J_kg'])/abs(s['enthalpy_J_kg']))
    assert max(if97_differences)<.002
    double=solve(duty=2e7)
    assert abs(double['available_shaft_W']-2*base['available_shaft_W'])<1e-5
    # At normal 24 MPa / 560 K, water is liquid-like, not a vapor compressor inlet/output basis.
    normal_phase=PhaseSI('P',24e6,'T',560,F)
    high_double=solve(ratio=8,p_low=5e3,duty=2e7)
    assert abs(high_double['available_shaft_W']-2*high_ratio['available_shaft_W'])<1e-5
    sources={str(p.relative_to(ROOT.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
             for p in (ROOT/'brayton_cooler.py',ROOT.parent/'steam-generator/Generator sizing - Hurmet.md')}
    result=dict(title='Steam Brayton auxiliary cooler feasibility screen',date='2026-10-12',
      property_model='CoolProp '+CoolProp.__version__+' HEOS::Water (IAPWS-95)',source_hashes=sources,
      base=base,high_ratio=high_ratio,high_ratio_pressure_trials=high_ratio_trials,normal_steam_throttle=dict(inlet=state(24e6,t=830),outlets=throttle_trials),efficiency_ratio_trials=trials,pressure_loss_trials=losses,absolute_pressure_trials=pressures,
      checks=dict(IF97_max_relative_enthalpy_difference=max(if97_differences),duty_scaling_pass=True,
        normal_24MPa_560K_phase=normal_phase),
      limitations=['Fixed SG temperature endpoints; no salt-side heat-transfer or freezing calculation',
        '10 MW is a normalization, not a selected reactor decay-heat duty',
        'Lower auxiliary-cycle pressures require isolation/depressurization or a separate heat exchanger; no direct connection to operating 24 MPa headers',
        'No compressor/turbine maps, startup system, inventory control, overspeed control, or cooldown validation',
        'Fan pressure drop and temperature rise are assumptions, not equipment sizing',
        'Salt-circulation power and other station loads are not included in available-shaft result',
        'Duty scaling holds cycle states fixed; it is not a part-load performance model'])
    (ROOT/'brayton-cooler-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(base=base,checks=result['checks'],sensitivity=[dict(ratio=q['ratio'],eta_c=q['eta_c'],eta_t=q['eta_t'],available_W=q['result'].get('available_shaft_W'),reason=q['result'].get('reason')) for q in trials]),indent=2))
if __name__=='__main__':main()
