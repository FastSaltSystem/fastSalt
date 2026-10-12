"""Parameterized reheat study derived from the preserved rankine_cycle.py baseline.

All calculations SI. CoolProp 7.2.0 HEOS water (IAPWS-95); numpy linear solve.
Fractions use total steam-generator mass flow, not individual turbine flows.
No reactor/neutronics or fuel-process analysis is performed here.
See README.md for provisional component routing, losses and exclusions.
"""
import sys,json,math
from pathlib import Path
import hashlib
from functools import lru_cache
import CoolProp
from CoolProp.CoolProp import PropsSI as P
import numpy as np
F='HEOS::Water'
@lru_cache(maxsize=200000)
def prop(out,a,x,b,y):return P(out,a,x,b,y,F)
def st(p,h=None,t=None,q=None):
 if h is None:h=prop('H','P',p,'T',t) if t else prop('H','P',p,'Q',q)
 return dict(p=p,h=h,t=prop('T','P',p,'H',h),s=prop('S','P',p,'H',h))
def turb(s,p,e):return st(p,s['h']-e*(s['h']-prop('H','P',p,'S',s['s'])))
def pump(s,p,e):return st(p,s['h']+(prop('H','P',p,'S',s['s'])-s['h'])/e)
def solve(pc=5000,tr=743.15,thr=633.15,pda=.6e6,plp3=.25e6,p3=4e6,lp_eff=.88,pinch_points=81,p2=2e6,p1=1.2e6):
 pmain=24e6;tmain=830; tfw=560;ttd=5
 p4=prop('P','T',tfw+ttd,'Q',0)
 main=st(pmain,t=tmain); fw=st(pmain,t=tfw)
 hp4=turb(main,p4,.88);hp3=turb(hp4,p3,.88)
 cr=st(p3*.95,h=hp3['h']);rh=st(p3*.95,t=tr);rhd=st(pmain,t=thr)
 ip=turb(rh,pda,.90); lp3=turb(ip,plp3,lp_eff);lp2=turb(lp3,.10e6,lp_eff);lp1=turb(lp2,.03e6,lp_eff);ex=turb(lp1,pc,lp_eff)
 fp2=turb(hp4,p2,.80);fp1=turb(fp2,p1,.80);fpex=turb(fp1,pda,.80)
 cond=st(pc,q=0);cp=pump(cond,pda*1.2,.80);da=st(pda,q=0);bp=pump(da,pmain,.85)
 lp_fw=[cp]+[st(cp['p'],t=prop('T','P',p,'Q',0)-ttd) for p in (.03e6,.1e6,plp3)]
 hp_fw=[bp]+[st(pmain,t=prop('T','P',p,'Q',0)-ttd) for p in (p1,p2,p3,p4)]
 drains={p:st(p,q=0)['h'] for p in (p1,p2,p3,p4,.03e6,.10e6,plp3)}
 def eq(y):
  R,H4,H3,F,H2,H1,D,L3,L2,L1=y
  mr=1-R-H4-H3-F; ml=mr-D; d4=R+H4;d3=d4+H3;d2=d3+H2;d1=d2+H1
  return np.array([
   R*(main['h']-rhd['h'])-mr*(rh['h']-cr['h']),
   H4*(hp4['h']-drains[p4])+R*(rhd['h']-drains[p4])-(hp_fw[4]['h']-hp_fw[3]['h']),
   H3*(hp3['h']-drains[p3])+d4*(drains[p4]-drains[p3])-(hp_fw[3]['h']-hp_fw[2]['h']),
   H2*(fp2['h']-drains[p2])+d3*(drains[p3]-drains[p2])-(hp_fw[2]['h']-hp_fw[1]['h']),
   H1*(fp1['h']-drains[p1])+d2*(drains[p2]-drains[p1])-(hp_fw[1]['h']-hp_fw[0]['h']),
   .99*(F*(hp4['h']-fp2['h'])+(F-H2)*(fp2['h']-fp1['h'])+(F-H2-H1)*(fp1['h']-fpex['h']))-(bp['h']-da['h']),
   ml*lp_fw[3]['h']+d1*drains[p1]+(F-H2-H1)*fpex['h']+D*ip['h']-da['h'],
   L3*(lp3['h']-drains[plp3])-ml*(lp_fw[3]['h']-lp_fw[2]['h']),
   L2*(lp2['h']-drains[.1e6])+L3*(drains[plp3]-drains[.1e6])-ml*(lp_fw[2]['h']-lp_fw[1]['h']),
   L1*(lp1['h']-drains[.03e6])+(L3+L2)*(drains[.1e6]-drains[.03e6])-ml*(lp_fw[1]['h']-lp_fw[0]['h'])])
 zero=eq(np.zeros(10));A=np.column_stack([eq(np.eye(10)[i])-zero for i in range(10)])
 y=np.linalg.solve(A,-zero);R,H4,H3,F,H2,H1,D,L3,L2,L1=y
 mr=1-R-H4-H3-F;ml=mr-D
 wHP=(1-R)*(main['h']-hp4['h'])+(1-R-H4-F)*(hp4['h']-hp3['h'])
 wIP=mr*(rh['h']-ip['h']); wLP=ml*(ip['h']-lp3['h'])+(ml-L3)*(lp3['h']-lp2['h'])+(ml-L3-L2)*(lp2['h']-lp1['h'])+(ml-L3-L2-L1)*(lp1['h']-ex['h'])
 qSG=main['h']-fw['h'];mass=1.5e9/qSG
 qcond=(ml-L3-L2-L1)*ex['h']+(L3+L2+L1)*drains[.03e6]-ml*cond['h']
 # Local counterflow approach along the reheater, hot end at f=1.
 approaches=[prop('T','P',pmain,'H',rhd['h']+f*(main['h']-rhd['h']))-prop('T','P',rh['p'],'H',cr['h']+f*(rh['h']-cr['h'])) for f in np.linspace(0,1,pinch_points)]
 gross=.985*.99*(wHP+wIP+wLP)*mass;cep=ml*(cp['h']-cond['h'])*mass/.96
 out=dict(inputs=dict(pc=pc,tr=tr,thr=thr,pda=pda,plp3=plp3,p3=p3,lp_eff=lp_eff,p2=p2,p1=p1),fractions=dict(zip(['reheat','HP4','HP3','pump_turbine','HP2','HP1','DA','LP3','LP2','LP1'],y)),mass=mass,main=dict(main),qcond=qcond*mass,gross=gross,cep=cep,bfp=(bp['h']-da['h'])*mass,moisture=1-prop('Q','P',pc,'H',ex['h']),pinch=min(approaches),reheater_approaches=approaches,reheat_flow=mr*mass,reheat_duty=R*(main['h']-rhd['h'])*mass,energy_residual=qSG-(wHP+wIP+wLP)-qcond+ml*(cp['h']-cond['h'])-(bp['h']-da['h'])*(1/.99-1),balance_residual=max(abs(eq(y))),specific_work=dict(HP=wHP,IP=wIP,LP=wLP,CEP=ml*(cp['h']-cond['h']),BFP=bp['h']-da['h']),condenser_mass=ml*mass,exhaust_mass=(ml-L3-L2-L1)*mass,condenser_specific_heat=qcond,drain_enthalpies=drains,states=dict(main=main,feedwater=fw,HP4=hp4,HPex=hp3,reheat_cold=cr,reheat_hot=rh,reheat_return=rhd,IPex=ip,LP3=lp3,LP2=lp2,LP1=lp1,LPex=ex,pump_bleed2=fp2,pump_bleed1=fp1,pump_exhaust=fpex,condenser=cond,condensate_pump=cp,deaerator=da,boiler_feed_pump=bp),lp_feed=lp_fw,hp_feed=hp_fw)
 return out


def balanced_case(pc=5000, tr=743.15, thr=633.15,p3=4e6,lp_eff=.88,pinch_points=81,p2=2e6,p1=1.2e6):
    # The drawing routes the feed-pump turbine exhaust to the deaerator.
    # Select the highest LP-heater extraction pressure to meet DA duty without
    # inventing an additional main-turbine extraction. D is a diagnostic only.
    lo, hi = .105e6, .5e6
    assert solve(pc,tr,thr,plp3=lo,p3=p3,lp_eff=lp_eff,pinch_points=pinch_points,p2=p2,p1=p1)['fractions']['DA'] > 0
    assert solve(pc,tr,thr,plp3=hi,p3=p3,lp_eff=lp_eff,pinch_points=pinch_points,p2=p2,p1=p1)['fractions']['DA'] < 0
    for _ in range(30):
        p=(lo+hi)/2
        if solve(pc,tr,thr,plp3=p,p3=p3,lp_eff=lp_eff,pinch_points=pinch_points,p2=p2,p1=p1)['fractions']['DA'] > 0: lo=p
        else: hi=p
    r=solve(pc,tr,thr,plp3=(lo+hi)/2,p3=p3,lp_eff=lp_eff,pinch_points=pinch_points,p2=p2,p1=p1)
    assert abs(r['fractions']['DA']) < 1e-9
    assert all(v>=-1e-9 for v in r['fractions'].values())
    assert r['fractions']['pump_turbine'] > r['fractions']['HP1']+r['fractions']['HP2']
    assert r['exhaust_mass'] > 0
    assert r['balance_residual'] < 1e-5
    assert abs(r['energy_residual']) < 1e-5
    return r
