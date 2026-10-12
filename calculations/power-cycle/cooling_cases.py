"""Couple the accepted cooling-water cases to one fixed condenser envelope.

Keep U, area, cooling flow, reheat conditions and extraction pressures fixed.
Rebalance bleed flows using the preliminary cycle model; this is not a turbine
manufacturer's off-design map. The accepted normal/hot/extreme inlet values are
20/30/35 Celsius and do not represent site weather percentiles.
"""
from pathlib import Path
import json
import math
import hashlib
import rankine_cycle as cycle

ROOT=Path(__file__).resolve().parent

def main():
    baseline=json.loads((ROOT/'rankine-results.json').read_text())
    assert hashlib.sha256((ROOT/'rankine_cycle.py').read_bytes()).hexdigest()==baseline['solver_sha256']
    cp=4180.0
    water_mass=baseline['qcond']/(cp*8.0)
    capacity=water_mass*cp
    tcond=baseline['states']['condenser']['t']
    d1=tcond-293.15;d2=tcond-301.15
    lmtd=(d1-d2)/math.log(d1/d2)
    u=2500.0
    area=baseline['qcond']/(u*lmtd)
    effectiveness=1-math.exp(-u*area/capacity)
    extraction_pressure=baseline['inputs']['plp3']
    cases=[]
    for label,tc in [('Normal reference',20),('Hot design check',30),('Extreme check',35)]:
        tin=tc+273.15
        # The condenser temperature must exceed its water outlet temperature.
        # Solve Q = C*(1-exp(-UA/C))*(Tsat(P)-Tin) with cycle Q(P).
        lo,hi=2000.0,25000.0
        def evaluate(pressure):
            r=cycle.solve(pc=pressure,plp3=extraction_pressure)
            ts=cycle.prop('T','P',pressure,'Q',0)
            residual=capacity*effectiveness*(ts-tin)-r['qcond']
            return residual,r,ts
        assert evaluate(lo)[0]<0<evaluate(hi)[0]
        for _ in range(28):
            mid=(lo+hi)/2
            if evaluate(mid)[0]>0:hi=mid
            else:lo=mid
        residual,r,ts=evaluate((lo+hi)/2)
        tout=tin+r['qcond']/capacity
        # Independent LMTD form verifies the effectiveness calculation.
        dt1,dt2=ts-tin,ts-tout
        assert dt2>0
        lmt=(dt1-dt2)/math.log(dt1/dt2)
        assert abs(u*area*lmt-r['qcond'])/r['qcond']<1e-7
        assert abs(residual)/r['qcond']<1e-7
        assert abs(r['fractions']['DA'])<1e-9
        assert all(v>=-1e-9 for v in r['fractions'].values())
        assert abs(r['energy_residual'])<1e-5
        assert r['pinch']>=10
        cases.append(dict(label=label,inlet_C=tc,outlet_C=tout-273.15,
            condenser_kPa=r['inputs']['pc']/1000,condensing_C=ts-273.15,
            terminal_approach_K=dt2,gross_MW=r['gross']/1e6,condenser_MW=r['qcond']/1e6,
            exhaust_moisture_percent=100*r['moisture'],thermal_residual_W=residual,
            energy_residual_J_kg=r['energy_residual']))
    assert abs(cases[0]['condenser_kPa']-5)<1e-6
    assert abs(cases[0]['gross_MW']-baseline['gross']/1e6)<1e-5
    assert all(a['gross_MW']>b['gross_MW'] and a['condenser_kPa']<b['condenser_kPa'] for a,b in zip(cases,cases[1:]))
    out=dict(scope='Fixed condenser screening; constant U, water flow and cycle section efficiencies. Not a rated off-design operating map.',
             U_W_m2K=u,area_m2=area,water_mass_kg_s=water_mass,water_volume_m3_s=water_mass/998,
             water_cp_J_kgK=cp,water_density_kg_m3=998,effectiveness=effectiveness,
             LP3_pressure_Pa=extraction_pressure,cases=cases,
             source_results_sha256=hashlib.sha256((ROOT/'rankine-results.json').read_bytes()).hexdigest(),
             solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/'cooling-cases.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
