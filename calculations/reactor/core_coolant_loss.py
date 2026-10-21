"""Publish the owner-selected UM-flow core pressure-loss estimate in Hurmet."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import argparse,hashlib,json,math,sys,tomllib

HERE=Path(__file__).resolve().parent
REPORT=Path('/Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Papers and Presentations/UMReport/Evolution_of_WISSR_design 2.pdf')

def darcy(re,relative):
    # Independent bracketed solve of Colebrook; Hurmet uses fixed-point iteration.
    assert re>4000
    lo,hi=2.,20.
    def residual(x):return x+2*math.log10(relative/3.7+2.51*x/re)
    assert residual(lo)<0<residual(hi)
    for _ in range(70):
        mid=(lo+hi)/2
        if residual(mid)>0:hi=mid
        else:lo=mid
    return 1/((lo+hi)/2)**2

def publish(hub,models,out):
    sys.path.insert(0,str(models/'models'))
    import wistr_reactor as reactor
    assert reactor.CORE['height']==3.4
    inputs={
        'MassFlow':(18500.,'kg/s'), 'TubeCount':(24576,''), 'TubeBore':(.014,'m'),
        'CoreLength':(reactor.CORE['height'],'m'),
        'BottomReflector':(reactor.LAYERS['bottom_reflector'],'m'),
        'TopReflector':(reactor.LAYERS['top_reflector'],'m'),
        'InletTemperature':(810.,'K'),'OutletTemperature':(890.,'K'),
        'DensityIntercept':(2112.8,"'kg/m3'"),'DensitySlope':(.56355,"'kg.m-3.K-1'"),
        'ViscosityScale':(.0007064,'Pa.s'),'ViscosityTemperature':(1204.1,'K'),
        'Roughness':(.000001,'m'),'EntranceK':(.5,''),'ExitK':(1.,''),
        'Gravity':(9.80665,'m/s2'),'VelocityLimit':(3.,'m/s'),
        'ReportedArea':(3.86,'m2'),
    }
    v={k:x for k,(x,u) in inputs.items()};md=[];checks={}
    def text(s):md.append(s.strip())
    def C(n,expr,u='',scale=1):
        x=eval(expr.replace('^','**'),{'__builtins__':{},'pi':math.pi,'exp':math.exp,'sqrt':math.sqrt,'Darcy':darcy},v)
        v[n]=x;checks[n]=x/scale
        text(f'¢??` {n} = {expr} = 〔{x/scale:.10g}〕 {u} `')
    text('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Core coolant pressure loss

Preliminary estimate, 14 October 2026. Owner selects the UM report's **18,500 kg/s total core flow**, with coolant at 810–890 K, and confirms **3.4 m active height**. The appendix's 3.8 m height is a typo, per the owner; it is not an alternative geometry. Current core diameter remains 3.8 m.

This calculation treats 24,576 identical, open 14 mm-bore tubes in parallel with equal flow. Pressure losses are the loss across one parallel passage, not that loss multiplied by tube count. Fuel-side wire spacers are not coolant-bore obstructions in this model.

## Basis

- UM report Table 58, printed p.139: tube count, total mass flow, 810/890 K temperatures, reported 3.86 m² total area and 2.94 m/s velocity.
- Tables 25 and 42, printed pp.87 and 109: 14 mm coolant bore, 16 mm tube OD. Table 43, p.110: density and viscosity correlations used below, with T in kelvin.
- Owner-confirmed active height 3.4 m; current lower/upper reflectors 0.30/0.25 m. A provisional continuous 14 mm bore through both reflectors gives a 3.95 m total straight passage. Actual reflector transitions remain to be specified.
- Roughness 1 micrometre is the inherited SG worksheet's clean-tube assumption, not measured core roughness. A 10 micrometre sensitivity is included.
- Entrance K = 0.5 and exit K = 1.0 are provisional sharp-entry/large-plenum allowances. They apply once at the full-passage ends, not at each reflector interface. Actual entry shape, exit recovery and any internal restrictions remain unresolved.

The main-generator worksheet previously used 22,699 kg/s total and an 875 K outlet. That earlier operating basis is not used here. Its pump and system-pressure estimates require reconciliation before this core result is incorporated into the whole-loop balance.
''')
    text('¢` format = "h7" `')
    for n,(x,u) in inputs.items():text(f'¢` {n} = {x:.12g} {u} `')
    text('''## Mean properties and velocity

Use arithmetic mean bulk temperature for this first estimate. The actual velocity rises along each heated tube as density falls.
''')
    for n,e,u,s in [
        ('MeanTemperature','(InletTemperature + OutletTemperature) / 2','K',1),
        ('Density','DensityIntercept - DensitySlope * MeanTemperature','kg/m3',1),
        ('Viscosity','ViscosityScale * exp(ViscosityTemperature / MeanTemperature)','Pa.s',1),
        ('SingleArea','pi * TubeBore^2 / 4','m2',1),
        ('FlowArea','TubeCount * SingleArea','m2',1),
        ('VolumeFlow','MassFlow / Density','m3/s',1),
        ('TubeMassFlow','MassFlow / TubeCount','kg/s',1),
        ('Velocity','VolumeFlow / FlowArea','m/s',1),
        ('InletDensity','DensityIntercept - DensitySlope * InletTemperature','kg/m3',1),
        ('OutletDensity','DensityIntercept - DensitySlope * OutletTemperature','kg/m3',1),
        ('InletVelocity','MassFlow / (InletDensity * FlowArea)','m/s',1),
        ('OutletVelocity','MassFlow / (OutletDensity * FlowArea)','m/s',1),
        ('ReportedAreaVelocity','MassFlow / (Density * ReportedArea)','m/s',1),
        ('AreaDifference','ReportedArea / FlowArea - 1','',1),
        ('Reynolds','Density * Velocity * TubeBore / Viscosity','',1),
    ]:C(n,e,u,s)
    text('''The exact tube count × bore gives 3.783 m², about 2% smaller than the report's listed 3.86 m². Keep the two bases explicit: 3.86 m² reproduces approximately 2.94 m/s, while the count/bore calculation is approximately 2.99 m/s. Neither value justifies claiming a strict below-3 m/s limit at every axial position or in every tube. Outlet velocity and flow maldistribution must be distinguished from mean velocity.

## Friction and local losses

Darcy–Weisbach: Δp = f (L/D) ρv²/2. The Darcy friction factor (not Fanning) is solved from Colebrook using the calculated Reynolds number and relative roughness. This is a steady, fully developed, single-phase approximation.
''')
    text('''¢` function Darcy(rey, relative)
    if rey < 4000 throw "Turbulent model requires Re above 4000"
    x = 8
    for i in 1:30
        x = -2 * ln(relative / 3.7 + 2.51 * x / rey) / ln(10)
    end
    return 1 / x^2
end `''')
    for n,e,u,s in [
        ('FrictionFactor','Darcy(Reynolds, Roughness / TubeBore)','',1),
        ('DynamicPressure','Density * Velocity^2 / 2','kPa',1000),
        ('PassageLength','CoreLength + BottomReflector + TopReflector','m',1),
        ('CoreFriction','FrictionFactor * CoreLength / TubeBore * DynamicPressure','kPa',1000),
        ('ReflectorFriction','FrictionFactor * (BottomReflector + TopReflector) / TubeBore * DynamicPressure','kPa',1000),
        ('PassageFriction','CoreFriction + ReflectorFriction','kPa',1000),
        ('EndLoss','(EntranceK + ExitK) * DynamicPressure','kPa',1000),
        ('TotalLoss','PassageFriction + EndLoss','kPa',1000),
        ('LossHead','TotalLoss / (Density * Gravity)','m',1),
        ('HydrostaticDifference','Density * Gravity * PassageLength','kPa',1000),
        ('MassFlux','MassFlow / FlowArea',"'kg.m-2.s-1'",1),
        ('AccelerationDifference','MassFlux^2 * (1 / OutletDensity - 1 / InletDensity)','kPa',1000),
        ('StaticPressureDifference','TotalLoss + HydrostaticDifference + AccelerationDifference','kPa',1000),
        ('HydraulicPower','TotalLoss * VolumeFlow','kW',1000),
    ]:C(n,e,u,s)
    text('''TotalLoss is irreversible passage loss including the provisional end losses. HydrostaticDifference is the approximate bottom-to-top pressure difference due to upward elevation; it is **not** extra closed-loop pump head. AccelerationDifference is a one-dimensional constant-area heated-flow estimate using endpoint densities; StaticPressureDifference is therefore an approximate plenum-to-plenum pressure difference, not additional friction. Detailed nozzle velocities and entry/exit recovery require refinement.

## Roughness and 3 m/s checks
''')
    text('¢` RougherSurface = 0.00001 m `');v['RougherSurface']=1e-5
    for n,e,u,s in [
        ('RougherFactor','Darcy(Reynolds, RougherSurface / TubeBore)','',1),
        ('RougherTotalLoss','(RougherFactor * PassageLength / TubeBore + EntranceK + ExitK) * DynamicPressure','kPa',1000),
        ('MeanFlowLimit','Density * FlowArea * VelocityLimit','kg/s',1),
        ('OutletFlowLimit','OutletDensity * FlowArea * VelocityLimit','kg/s',1),
        ('MeanCountThreshold','MassFlow / (Density * VelocityLimit * SingleArea)','',1),
        ('OutletCountThreshold','MassFlow / (OutletDensity * VelocityLimit * SingleArea)','',1),
    ]:C(n,e,u,s)
    text('''Count thresholds are real-valued hydraulic comparisons; round upward for whole tubes. They are not an adopted geometry change and include no maldistribution allowance. The average velocity is just below 3 m/s; outlet velocity is slightly above it with exact count/bore.

## Limits and reproduction

No entrance contour, tube-to-reflector step, blockage, bypass, nonuniform power/flow, roughness growth, downcomer, plenum, nozzle or external-piping loss has been resolved. Mean-temperature properties are sufficient for this preliminary estimate; an independently calculated axial property integration is recorded in the results JSON as a check, not as a Hurmet result.

The earlier 50%-above-SG pump allowance cannot be assessed by subtracting this loss alone: that estimate uses a different flow and temperature case. No SG failure, relief sizing, pump selection or geometry change is included.

Sources: UM/NRDSL-25/02, *Core Design Evolution of Wielenga Innovation Salt Tank Reactor*, November 15, 2025, Tables 25, 42, 43 and 58; owner corrections 14 October 2026; current `wistr_reactor.py`; inherited SG roughness assumption. Source hashes and explicit inputs are in `core-coolant-loss-results.json`.

Method reference: [NASA KSC-STD-Z-0017 Rev A, §§7.4–7.5](https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017_RevA_Final.pdf), Colebrook and Darcy loss equations. This is a general calculation method, not nuclear-system qualification.

Run `python calculations/reactor/core_coolant_loss.py`, followed by `node calculations/reactor/check_core_coolant_loss.cjs` with HURMET_ENGINE and TEMML_ENGINE pointing to the project Hurmet bundles. Python uses an independent bracketed Colebrook solve; Hurmet uses fixed-point iteration, recalculates all cells and checks save/reopen and sensitivities. The publisher restores the documented baseline; direct Hurmet input edits require updating the verification baseline before comparison.
''')
    # Uniform axial heating in active core, cold lower/hot upper reflector.
    def friction_segment(length,temp):
        rho=v['DensityIntercept']-v['DensitySlope']*temp
        mu=v['ViscosityScale']*math.exp(v['ViscosityTemperature']/temp)
        vel=v['MassFlow']/rho/v['FlowArea'];re=rho*vel*v['TubeBore']/mu
        return darcy(re,v['Roughness']/v['TubeBore'])*length/v['TubeBore']*rho*vel**2/2
    def integrate(n):
        return sum(friction_segment(v['CoreLength']/n,v['InletTemperature']+(i+.5)/n*(v['OutletTemperature']-v['InletTemperature'])) for i in range(n))
    integrated=integrate(400); fine=integrate(800)
    assert abs(fine-integrated)<.01
    assert abs(integrated/v['CoreFriction']-1)<.01
    assert v['Velocity']<3 and v['OutletVelocity']>3
    assert v['TotalLoss']>v['PassageFriction']>v['CoreFriction']>0
    scenarios=[]
    for rough in [0,1e-6,1e-5,4.5e-5]:
        f=darcy(v['Reynolds'],rough/v['TubeBore'])
        scenarios.append({'roughness_m':rough,'darcy_factor':f,'passage_and_ends_kPa':(f*v['PassageLength']/v['TubeBore']+1.5)*v['DynamicPressure']/1000})
    sources=[REPORT,models/'models/wistr_reactor.py',hub/'calculations/steam-generator/Generator sizing - Hurmet.md']
    result={'date':'2026-10-14','status':'Preliminary; owner-selected UM total flow, corrected 3.4 m height','inputs':{k:{'value':x,'unit':u} for k,(x,u) in inputs.items()},'hurmet_checks':checks,'roughness_sensitivity':scenarios,'axial_integration_external':{'temperature_profile':'Linear active-core heating; reflectors at respective endpoint temperatures','active_friction_kPa':fine/1000,'passage_friction_kPa':(fine+friction_segment(v['BottomReflector'],v['InletTemperature'])+friction_segment(v['TopReflector'],v['OutletTemperature']))/1000,'mean_temperature_relative_difference':fine/v['CoreFriction']-1,'convergence_400_to_800_Pa':fine-integrated},'sources':[{'path':str(p.relative_to(hub)) if p.is_relative_to(hub) else str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources]}
    out.mkdir(parents=True,exist_ok=True)
    write_worksheet(out/'Core coolant pressure loss - Hurmet.md', '\n\n'.join(md)+'\n')
    (out/'core-coolant-loss-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--hub',type=Path,default=HERE.parents[1]);p.add_argument('--models',type=Path);p.add_argument('--output',type=Path,default=HERE)
    a=p.parse_args();publish(a.hub.resolve(),(a.models or a.hub.parent/'fastSaltModels').resolve(),a.output.resolve())
