"""Matched steady-state BFP-drive comparison; SI, CoolProp via reheat_model.

Keeps the accepted main/IP expansion endpoint unchanged when introducing bleeds:
intermediate IP states lie on the same inlet-referenced 90% expansion curve.
This avoids an artificial efficiency gain from subdividing the turbine model.
The existing selected cycle and equipment schedule are not overwritten.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np
import CoolProp
from reheat_model import st, turb, pump, prop

ROOT = Path(__file__).resolve().parent

def solve(basis, drive='steam', pc=5000., pb=26.5e6, pcp=1e6,
          electric_eff=.95, aux_eff=.80, ip_eff=.90, lp_eff=.88, plp3=None, validate=True):
    assert drive in ('steam', 'electric')
    inp = basis['inputs']
    pmain, pda, p3, p2, p1, plp3 = 24e6, .6e6, inp['p3'], inp['p2'], inp['p1'], (inp['plp3'] if plp3 is None else plp3)
    p4 = basis['states']['HP4']['p']
    main, fw = st(pmain, t=830), st(pmain, t=560)
    hp4 = turb(main, p4, .88)
    hp3 = turb(hp4, p3, .88)
    cr, rh, rhd = st(.95*p3, h=hp3['h']), st(.95*p3, t=inp['tr']), st(pmain, t=inp['thr'])
    # Same trajectory for BOTH drives. Bleeds change mass, not turbine endpoints.
    ip2, ip1, ip = [turb(rh, p, ip_eff) for p in (p2, p1, pda)]
    lp3 = turb(ip, plp3, lp_eff)
    lp2 = turb(lp3, .1e6, lp_eff)
    lp1 = turb(lp2, .03e6, lp_eff)
    ex = turb(lp1, pc, lp_eff)
    fp2 = turb(hp4, p2, aux_eff)
    fp1 = turb(fp2, p1, aux_eff)
    fpex = turb(fp1, pda, aux_eff)
    b2, b1 = (fp2, fp1) if drive == 'steam' else (ip2, ip1)
    cond, da = st(pc, q=0), st(pda, q=0)
    cp, bp = pump(cond, pcp, .80), pump(da, pb, .85)
    lpfw = [cp] + [st(pcp, t=prop('T', 'P', p, 'Q', 0)-5) for p in (.03e6, .1e6, plp3)]
    hpfw = [bp] + [st(pb, t=prop('T', 'P', p, 'Q', 0)-5) for p in (p1, p2, p3)]
    # Locate aggregate BFP-to-SG loss after the heater bank. Adiabatic throttle
    # preserves the accepted SG-inlet enthalpy at 24 MPa / 560 K.
    hpfw.append(st(pb, h=fw['h']))
    drains = {p: st(p, q=0)['h'] for p in (p1,p2,p3,p4,.03e6,.1e6,plp3)}
    electric = drive == 'electric'
    def flow(y):
        R,H4,H3,F,H2,H1,D,L3,L2,L1 = y
        mr = 1-R-H4-H3-F
        ml = mr-D-(H2+H1 if electric else 0)
        return mr, ml
    def equations(y):
        R,H4,H3,F,H2,H1,D,L3,L2,L1 = y
        mr,ml = flow(y)
        d4=R+H4; d3=d4+H3; d2=d3+H2; d1=d2+H1
        aux = F*(hp4['h']-fp2['h'])+(F-H2)*(fp2['h']-fp1['h'])+(F-H2-H1)*(fp1['h']-fpex['h'])
        return np.array([
            R*(main['h']-rhd['h'])-mr*(rh['h']-cr['h']),
            H4*(hp4['h']-drains[p4])+R*(rhd['h']-drains[p4])-(hpfw[4]['h']-hpfw[3]['h']),
            H3*(hp3['h']-drains[p3])+d4*(drains[p4]-drains[p3])-(hpfw[3]['h']-hpfw[2]['h']),
            H2*(b2['h']-drains[p2])+d3*(drains[p3]-drains[p2])-(hpfw[2]['h']-hpfw[1]['h']),
            H1*(b1['h']-drains[p1])+d2*(drains[p2]-drains[p1])-(hpfw[1]['h']-hpfw[0]['h']),
            F*1e6 if electric else .99*aux-(bp['h']-da['h']),
            ml*lpfw[3]['h']+d1*drains[p1]+(0 if electric else (F-H2-H1)*fpex['h'])+D*ip['h']-da['h'],
            L3*(lp3['h']-drains[plp3])-ml*(lpfw[3]['h']-lpfw[2]['h']),
            L2*(lp2['h']-drains[.1e6])+L3*(drains[plp3]-drains[.1e6])-ml*(lpfw[2]['h']-lpfw[1]['h']),
            L1*(lp1['h']-drains[.03e6])+(L3+L2)*(drains[.1e6]-drains[.03e6])-ml*(lpfw[1]['h']-lpfw[0]['h'])])
    z = equations(np.zeros(10))
    A = np.column_stack([equations(np.eye(10)[i])-z for i in range(10)])
    y = np.linalg.solve(A, -z)
    R,H4,H3,F,H2,H1,D,L3,L2,L1 = y
    mr,ml = flow(y)
    wHP = (1-R)*(main['h']-hp4['h'])+(1-R-H4-F)*(hp4['h']-hp3['h'])
    wIP = mr*(rh['h']-ip['h'])
    if electric:
        wIP -= H2*(ip2['h']-ip['h'])+H1*(ip1['h']-ip['h'])
    wLP = ml*(ip['h']-lp3['h'])+(ml-L3)*(lp3['h']-lp2['h'])+(ml-L3-L2)*(lp2['h']-lp1['h'])+(ml-L3-L2-L1)*(lp1['h']-ex['h'])
    mass = 1.5e9/(main['h']-fw['h'])
    bfp = mass*(bp['h']-da['h'])
    cep_fluid = mass*ml*(cp['h']-cond['h'])
    qcond = mass*((ml-L3-L2-L1)*ex['h']+(L3+L2+L1)*drains[.03e6]-ml*cond['h'])
    work = mass*(wHP+wIP+wLP)
    aux_work = 0 if electric else bfp/.99
    gross = .99*.985*work
    bfp_elec = bfp/electric_eff if electric else 0
    cep = cep_fluid/.96
    partial_net = gross-bfp_elec-cep
    residual = 1.5e9+bfp+cep_fluid-work-aux_work-qcond
    # Independent mass accounting across deaerator and condenser.
    d1 = R+H4+H3+H2+H1
    aux_ex = 0 if electric else F-H2-H1
    assert abs(ml+d1+aux_ex+D-1)<1e-10
    assert abs((ml-L3-L2-L1)+(L3+L2+L1)-ml)<1e-10
    assert abs(residual)<.02, residual
    assert max(abs(equations(y)))<1e-5
    if validate: assert min(y)>-1e-8, dict(zip(['R','H4','H3','F','H2','H1','D','L3','L2','L1'],y))
    assert ml-L3-L2-L1>0 and (electric or aux_ex>0)
    assert all(hpfw[i+1]['h']>hpfw[i]['h'] for i in range(4))
    return dict(drive=drive,inputs=dict(pc=pc,pb=pb,pcp=pcp,electric_eff=electric_eff,aux_eff=aux_eff,ip_eff=ip_eff,lp_eff=lp_eff,plp3=plp3),
        mass_kg_s=mass,gross_MW=gross/1e6,bfp_shaft_MW=bfp/1e6,bfp_electric_MW=bfp_elec/1e6,cep_electric_MW=cep/1e6,
        partial_net_MW=partial_net/1e6,partial_efficiency_percent=partial_net/1.5e9*100,
        condenser_MW=qcond/1e6,reheat_MW=mass*R*(main['h']-rhd['h'])/1e6,reheat_flow_kg_s=mass*mr,
        condenser_flow_kg_s=mass*ml,exhaust_flow_kg_s=mass*(ml-L3-L2-L1),moisture_percent=100*(1-prop('Q','P',pc,'H',ex['h'])),
        flows_kg_s=dict(zip(['reheat','HP4','HP3','pump_turbine','HP2','HP1','DA','LP3','LP2','LP1'],mass*y)),
        pump_turbine_exhaust_kg_s=mass*aux_ex,section_electric_MW={k:v*mass*.99*.985/1e6 for k,v in dict(HP=wHP,IP=wIP,LP=wLP).items()},
        heater_bleed_states=dict(HP4=hp4,HP3=hp3,HP2=b2,HP1=b1,DA=ip,LP3=lp3,LP2=lp2,LP1=lp1),reheat_return=rhd,hp_feed=hpfw,lp_feed=lpfw,
        whole_cycle_residual_W=residual,max_component_specific_residual_J_kg=float(max(abs(equations(y)))))

def compare(s,e):
    return dict(steam=s,electric=e,net_change_MW=e['partial_net_MW']-s['partial_net_MW'],
        efficiency_change_percentage_points=e['partial_efficiency_percent']-s['partial_efficiency_percent'],
        breakeven_electric_efficiency=e['bfp_shaft_MW']/(e['gross_MW']-e['cep_electric_MW']-s['partial_net_MW']))

def balanced_steam(basis, **kwargs):
    # Re-select only LP3 pressure to use all auxiliary exhaust in the DA.
    # Both drive cases then use this SAME LP3 pressure for a matched comparison.
    lo, hi = .1001e6, .5e6
    def evaluate(p):
        return solve(basis, plp3=p, validate=False, **kwargs)
    assert evaluate(lo)['flows_kg_s']['DA']>0>evaluate(hi)['flows_kg_s']['DA']
    for _ in range(36):
        mid=(lo+hi)/2
        if evaluate(mid)['flows_kg_s']['DA']>0:lo=mid
        else:hi=mid
    return solve(basis, plp3=(lo+hi)/2, **kwargs)

def matched(basis, electric_eff=.95, **kwargs):
    s=balanced_steam(basis, **kwargs)
    e=solve(basis, 'electric', plp3=s['inputs']['plp3'], electric_eff=electric_eff, **kwargs)
    return compare(s,e)

def heater_checks(r):
    rows=[]
    for bank, feed, mass, count in [('HP',r['hp_feed'],r['mass_kg_s'],4),('LP',r['lp_feed'],r['condenser_flow_kg_s'],3)]:
        incoming=r['flows_kg_s']['reheat'] if bank=='HP' else 0
        hin=r['reheat_return']['h'] if bank=='HP' else 0
        for i in range(count,0,-1):
            name=bank+str(i); b=r['heater_bleed_states'][name]
            bleed=r['flows_kg_s'][name]; total=incoming+bleed
            hf=st(b['p'],q=0)['h']; hmix=(incoming*hin+bleed*b['h'])/total
            duty=mass*(feed[i]['h']-feed[i-1]['h'])
            assert abs(total*(hmix-hf)-duty)<.01
            def integrate(n):
                fractions=np.linspace(0,1,n)
                approaches=[prop('T','P',b['p'],'H',hf+f*(hmix-hf))-prop('T','P',feed[i]['p'],'H',feed[i-1]['h']+f*(feed[i]['h']-feed[i-1]['h'])) for f in fractions]
                assert min(approaches)>0
                return duty*np.trapezoid(1/np.array(approaches),x=fractions),min(approaches)
            ua,dt=integrate(801);dense,_=integrate(1601)
            assert abs(ua/dense-1)<.001
            rows.append(dict(name=name,duty_MW=duty/1e6,bleed_kg_s=bleed,bleed_C=b['t']-273.15,area_proxy_m2=ua/2000*1.2,min_approach_K=dt))
            incoming=total;hin=hf
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=ROOT);ap.add_argument('--output',type=Path,default=ROOT);args=ap.parse_args()
    selected=json.loads((args.source/'reheat-selection.json').read_text());basis=selected['selected_at_5kPa']
    # Exact regression to the previously published thermal cycle.
    old=solve(basis,pb=24e6,pcp=.72e6)
    for k,j in [('gross_MW','gross'),('bfp_shaft_MW','bfp'),('cep_electric_MW','cep'),('condenser_MW','qcond')]:
        assert math.isclose(old[k]*1e6,basis[j],rel_tol=1e-10,abs_tol=.01),(k,old[k],basis[j])
    for k,v in old['flows_kg_s'].items():assert abs(v-basis['fractions'][k]*basis['mass'])<1e-7
    matched_old=compare(old,solve(basis,'electric',pb=24e6,pcp=.72e6))
    current=matched(basis)
    for d in ['steam','electric']:
        current[d]['heaters']=heater_checks(current[d])
        current[d]['reheater_area_proxy_m2']=selected['reheater_UA_W_K']*(current[d]['reheat_MW']/(basis['reheat_duty']/1e6))/1000*1.2
        current[d]['reheater_min_approach_K']=basis['pinch']
    turbine_sensitivity=[]
    for ie in [.88,.90,.92]:
        for le in [.86,.88,.90]:
            r=matched(basis,ip_eff=ie,lp_eff=le)
            turbine_sensitivity.append(dict(ip_eff=ie,lp_eff=le,delta_MW=r['net_change_MW'],moisture_percent=r['electric']['moisture_percent']))
    sensitivity=[]
    for ae in [.75,.80,.85]:
        for ee in [.93,.95,.97,.98]:
            r=matched(basis,aux_eff=ae,electric_eff=ee)
            sensitivity.append(dict(aux_turbine_eff=ae,electric_eff=ee,delta_MW=r['net_change_MW'],delta_pp=r['efficiency_change_percentage_points']))
    pressure=[]
    for p in [5000,8841,11518]:
        r=matched(basis,pc=p)
        pressure.append(dict(condenser_kPa=p/1000,delta_MW=r['net_change_MW'],steam_net_MW=r['steam']['partial_net_MW'],electric_net_MW=r['electric']['partial_net_MW']))
    # Same installed condenser, not merely equal pressure. Respect the 5 kPa floor.
    c=json.loads((args.source/'cooling-cases.json').read_text())
    capacity=c['water_mass_kg_s']*c['water_cp_J_kgK']
    UA=c['U_W_m2K']*c['area_m2'];effectiveness=1-math.exp(-UA/capacity)
    cooling=[]
    for tin in [20,30,35]:
        cases=[]
        for d in ['steam','electric']:
            def evaluate(p):
                r=solve(basis,d,pc=p,plp3=current['steam']['inputs']['plp3'])
                residual=capacity*effectiveness*(prop('T','P',p,'Q',0)-tin-273.15)-r['condenser_MW']*1e6
                return residual,r
            lo,hi=5000.,20000.
            floor=bool(evaluate(lo)[0]>=0)
            if floor:r=evaluate(lo)[1]
            else:
                assert evaluate(hi)[0]>0
                for _ in range(32):
                    mid=(lo+hi)/2
                    if evaluate(mid)[0]>0:hi=mid
                    else:lo=mid
                res,r=evaluate((lo+hi)/2);assert abs(res)<1
            r['cooling_inlet_C']=tin;r['pressure_floor_active']=floor
            r['cooling_outlet_C']=tin+r['condenser_MW']*1e6/capacity
            if not floor:
                ts=prop('T','P',r['inputs']['pc'],'Q',0)-273.15
                a,b=ts-tin,ts-r['cooling_outlet_C'];lmtd=(a-b)/math.log(a/b)
                assert abs(UA*lmtd-r['condenser_MW']*1e6)<1
            cases.append(r)
        cooling.append(compare(*cases))
    result=dict(status='Comparative preliminary study; no equipment/diagram selection changed',property_library='CoolProp '+CoolProp.__version__,
        original_pressure_comparison=matched_old,proposed_pressure_comparison=current,efficiency_sensitivity=sensitivity,
        main_turbine_sensitivity=turbine_sensitivity,matched_pressure_sensitivity=pressure,same_condenser_cooling_cases=cooling,
        checks=['published-cycle power, flows and condenser regression','component and whole-cycle energy closure','positive flows and independent DA/condenser mass closure','unchanged IP endpoint with extra extraction ports','matched pump heads','seven heater energy balances, positive approaches and 801/1601-point UA convergence','fixed-condenser effectiveness/LMTD agreement'],
        source_hashes={n:hashlib.sha256((args.source/n).read_bytes()).hexdigest() for n in ['reheat_model.py','reheat-selection.json','cooling-cases.json','equipment-sizing.json']})
    result['source_hashes']['compare_bfp_drives.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'bfp-drive-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({d: {k: current[d][k] for k in ['gross_MW','bfp_shaft_MW','bfp_electric_MW','partial_net_MW','partial_efficiency_percent','reheat_MW','reheater_area_proxy_m2']} for d in ['steam','electric']},indent=2))
    print('NET CHANGE MW',current['net_change_MW'],'EFFICIENCY CHANGE pp',current['efficiency_change_percentage_points'])
    print('COOLING',[(r['steam']['cooling_inlet_C'],r['steam']['inputs']['pc'],r['electric']['inputs']['pc'],r['net_change_MW']) for r in cooling])

if __name__=='__main__':main()
