"""Publish a preliminary normal coolant pressure envelope, without Blender.

The extra loop loss is not spatially resolved. Bounds vary its nonnegative
allocation while preserving the inherited total pump/loss balance.
"""
from pathlib import Path
import argparse, hashlib, json, math, random, sys, tomllib

HERE = Path(__file__).resolve().parent

def publish(hub, models, out):
    sys.path[:0] = [str(models/'src'), str(models/'models')]
    import wistr_installation as layout, coolant_assembly
    from textual_graphics.assembly_model import document
    doc = document(coolant_assembly.build_model(layout, coolant_assembly.reactor_interface(layout, models), models))
    coolant_assembly.check_pid_links(doc, hub/'design/pids/coolant-system/coolant-system.toml')
    report_path = models/layout.REACTOR['baseline']/'reactor-study-report.json'
    report = json.loads(report_path.read_text())
    engineering = tomllib.loads((hub/'design/engineering/coolant-system.toml').read_text())['cases']['normal']
    pressure = tomllib.loads((hub/'design/pids/coolant-system/coolant-system.toml').read_text())['gas_pressure_control']
    assert pressure['bias_pressure_reference'] == 'gauge'
    def z(port): return doc['ports'][port]['world_position_m'][2] - layout.FLOOR_Z
    for suffix in ['pump.suction','pump.discharge','generator.salt_inlet','generator.salt_outlet']:
        assert all(abs(z(f'leg_{i}.{suffix}')-z(f'leg_1.{suffix}')) < 1e-8 for i in (2,3))
    inputs = {
        'TopPressure':(pressure['bias_pressure_Pa']/1e5,'bar'),
        'Density':(engineering['density']['value'],'kg/m3'),
        'Gravity':(9.80665,'m/s2'),
        'SGLoss':(engineering['generator_pressure_drop']['value']/1000,'kPa'),
        'PumpFactor':(engineering['loop_allowance']['value'],''),
        'MassFlow':(engineering['mass_flow']['value'],'kg/s'),
        'MainBore':(layout.PIPE_SPECS['hot']['bore'],'m'),
        'TopZ':(layout.STEAM_GENERATORS['casing_bottom']+layout.STEAM_GENERATORS['height']-layout.FLOOR_Z,'m'),
        'SGInZ':(z('leg_1.generator.salt_inlet'),'m'),
        'SGOutZ':(z('leg_1.generator.salt_outlet'),'m'),
        'SuctionZ':(z('leg_1.pump.suction'),'m'),
        'DischargeZ':(z('leg_1.pump.discharge'),'m'),
        'ReactorInZ':(z('reactor.cold_inlet_1'),'m'),
        'BottomZ':(layout.REACTOR['origin_z']-layout.FLOOR_Z+report['derived_dimensions']['bottom_reflector_z']/2,'m'),
        'ReactorOutZ':(z('reactor.hot_outlet_1'),'m'),
    }
    # Python arithmetic is SI; Hurmet inputs carry explicit display units.
    v={k:x for k,(x,u) in inputs.items()}
    for k in ['TopPressure']:v[k]*=1e5
    v['SGLoss']*=1000
    checks={};md=[]
    def text(s):md.append(s.strip())
    def calc(name, expr, unit='', scale=1):
        value=eval(expr.replace('^','**'), {'__builtins__':{},'pi':math.pi},v)
        v[name]=value; checks[name]=value/scale
        text(f'¢??` {name} = {expr} = 〔{value/scale:.10g}〕 {unit} `')
    text('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Normal coolant pressure profile

Preliminary steady-flow screen, 14 October 2026. One representative leg of the three-leg coolant loop. All pressures below are **gauge**, unless stated otherwise. Owner basis: approximately 1 bar(g) at the SG tops; tank normally nearly empty; P-401 sets accumulator levels by transferring inventory. Steam-generator failure assessment is explicitly deferred and excluded.

The calculation uses the existing pump/SG loss estimates and current visual elevations. It does not select pressure ratings, relief settings or pump suction requirements. The extra 50% loop loss has not been assigned to individual components, so this sheet gives **correlated allocation bounds**, not a predicted operating curve or statistical uncertainty interval.

## Inputs and reference location

The SG-top pressure reference is provisionally at casing-top elevation, 17 m above the floor. The actual accumulator salt level and gas-tap elevation are not modeled yet. A 1 m reference-level change shifts all calculated pressures by about 0.16 bar at fixed gas pressure. All imported component elevations are layout inputs, not surveyed hydraulic data.

The common representative density is the pump worksheet's mean-temperature value. Its SG loss is friction only; hydrostatic pressure gain is added separately. The inherited 19.879 m tube calculation is retained despite the 17 m visual casing.
''')
    text('¢` format = "h7" `')
    for k,(x,u) in inputs.items():text(f'¢` {k} = {x:.12g} {u} `')
    text('''## Pressure balance

Use p₂ = p₁ + ρg(z₁ − z₂) + Δp_pump − Δp_loss. This first screen neglects changes in velocity head and assumes uniform representative density. Total closed-loop hydrostatic head cancels under that assumption: do not add the full SG height to pump duty.
''')
    calc('Gradient','Density * Gravity',"'bar/m'",1e5)
    calc('PumpRise','PumpFactor * SGLoss','bar',1e5)
    calc('OtherLoss','PumpRise - SGLoss','bar',1e5)
    calc('VolumeFlow','MassFlow / Density','m3/s')
    calc('PipeVelocity','4 * VolumeFlow / (pi * MainBore^2)','m/s')
    calc('PipeDynamicPressure','Density * PipeVelocity^2 / 2','bar',1e5)
    calc('SGGravityGain','Density * Gravity * (SGInZ - SGOutZ)','bar',1e5)
    calc('SGNetPressureGain','SGGravityGain - SGLoss','bar',1e5)
    text('''The velocity-pressure scale is only for the main bore; it does not bound local tube/manifold effects. The pressure datum is related hydrostatically to the hot inlet with negligible intervening loss. That connection and the actual gas-vessel salt level need confirmation.

## SG and pump pressures

No extra loss is assigned inside the SG beyond SGLoss. Between SG outlet and pump suction the unknown loss can range from zero to the entire OtherLoss budget. Pump inlet/outlet elevations differ by 0.90 m; that elevation rise is included when relating their pressures.
''')
    calc('SGInPressure','TopPressure + Density * Gravity * (TopZ - SGInZ)','bar',1e5)
    calc('SGOutPressure','SGInPressure + SGGravityGain - SGLoss','bar',1e5)
    calc('SuctionHigh','SGOutPressure + Density * Gravity * (SGOutZ - SuctionZ)','bar',1e5)
    calc('SuctionLow','SuctionHigh - OtherLoss','bar',1e5)
    calc('DischargeLow','SuctionLow + PumpRise + Density * Gravity * (SuctionZ - DischargeZ)','bar',1e5)
    calc('DischargeHigh','SuctionHigh + PumpRise + Density * Gravity * (SuctionZ - DischargeZ)','bar',1e5)
    text('''## Reactor pressures

Downstream of the pump, pressure equals the hydrostatic reference plus losses still remaining before the SG inlet. Without allocating OtherLoss, the remaining loss can range from zero to the entire budget. BottomZ is the bottom-plenum mid-height; it is not the lowest wall location or a maximum design pressure. Internal hydraulic losses are included only through the inherited aggregate allowance.
''')
    for prefix,zz in [('ReactorIn','ReactorInZ'),('Bottom','BottomZ'),('ReactorOut','ReactorOutZ')]:
        calc(prefix+'Low',f'TopPressure + Density * Gravity * (TopZ - {zz})','bar',1e5)
        calc(prefix+'High',f'{prefix}Low + OtherLoss','bar',1e5)
    text('''## Pumps stopped: isothermal hydrostatic reference

These values assume a filled, equilibrated circuit at uniform Density, unchanged reference level and gas pressure. They do not model natural circulation or the transition after stopping a pump.
''')
    for prefix,zz in [('StaticSGOut','SGOutZ'),('StaticSuction','SuctionZ'),('StaticReactorIn','ReactorInZ'),('StaticBottom','BottomZ'),('StaticReactorOut','ReactorOutZ')]:
        calc(prefix,f'TopPressure + Density * Gravity * (TopZ - {zz})','bar',1e5)
    text('''## Lower gas-pressure sensitivity

Use 0.5 bar(g) as a comparison only, not an adopted target. Every pressure shifts downward by the same 0.5 bar in this fixed-density/fixed-duty screen. Negative gauge pressure is not itself a cavitation criterion: vapor pressure, local velocities, gas release and vendor NPSH requirements remain necessary.
''')
    text('¢` LowerTopPressure = 0.5 bar `');v['LowerTopPressure']=.5e5
    calc('LowerBiasSuctionLow','SuctionLow + LowerTopPressure - TopPressure','bar',1e5)
    calc('LowerBiasSuctionHigh','SuctionHigh + LowerTopPressure - TopPressure','bar',1e5)
    text('''## Limits and next work

- Bounds preserve the total loss budget. Maxima/minima at different stations are correlated and cannot be chosen independently. They are not an allowance for arbitrary larger actual losses. The inherited pump pressure rise is treated as the duty requirement, not a measured pump curve.
- Uniform density suppresses thermosiphon head. The inherited density correlation gives approximately 1620–1656 kg/m³ across 875–810 K. The checker repeats the screen at those two uniform densities; it does not model their spatial distribution.
- All legs have matching modeled elevations; equal flow/loss is assumed. No flow redistribution or one-pump-out case is calculated.
- TK-401 is isolated between transfers and does not inherit the SG gas pressure automatically. Its pressure and transfer differential are separate unresolved operating inputs. The selected larger tank's location remains deferred.
- No pressure rating, relief hardware/setpoint, blocked-pump case, gas-regulator failure, transient or SG failure is assessed here. Next resolve SG/accumulator hydraulic level, suction-line loss and allocation of reactor/piping losses before reducing the gas bias or selecting pump suction margins.

## Sources and reproduction

- Owner pressure clarification and D-059; `design/pids/coolant-system/coolant-system.toml`.
- [Coolant pump estimate](../steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md), [generator sizing](../steam-generator/Generator%20sizing%20-%20Hurmet.md), and shared `design/engineering/coolant-system.toml`.
- Current `fastSaltModels` assembly ports and verified reactor report; hashes and imported values in `coolant-pressure-results.json`.
- [DOE Fluid Flow handbook](https://www.energy.gov/ehss/articles/doe-hdbk-10123-92): extended Bernoulli balance between pressure, elevation, pump energy and friction. This general method does not qualify the reactor design.

Run `python coolant_pressure_profile.py`, then `node check_coolant_pressure.cjs` with HURMET_ENGINE and TEMML_ENGINE pointing to the existing Hurmet bundles. Python evaluates the balance independently; Hurmet recalculates and reopens the worksheet, checks all numerical outputs and reference-pressure/density sensitivities. No Blender generation is needed.
''')
    # Check all vertices of the unresolved loss allocation and random mixtures.
    # Order: suction, pump-to-reactor, reactor downflow, core/upflow, hot pipe.
    rng=random.Random(401); allocations=[[float(i==j) for i in range(5)] for j in range(5)]
    for _ in range(100):
        a=[rng.random() for _ in range(5)];allocations.append([x/sum(a) for x in a])
    def H(a,b):return v['Density']*v['Gravity']*(v[a]-v[b])
    for a in allocations:
        loss=[x*v['OtherLoss'] for x in a]
        s=v['SGOutPressure']+H('SGOutZ','SuctionZ')-loss[0]
        d=s+v['PumpRise']+H('SuctionZ','DischargeZ')
        ri=d+H('DischargeZ','ReactorInZ')-loss[1]
        b=ri+H('ReactorInZ','BottomZ')-loss[2]
        ro=b+H('BottomZ','ReactorOutZ')-loss[3]
        back=ro+H('ReactorOutZ','SGInZ')-loss[4]
        assert abs(back-v['SGInPressure'])<1e-7
        for n,x in [('Suction',s),('Discharge',d),('ReactorIn',ri),('Bottom',b),('ReactorOut',ro)]:
            assert v[n+'Low']-1e-7 <= x <= v[n+'High']+1e-7
    sources=[hub/'design/engineering/coolant-system.toml',hub/'design/pids/coolant-system/coolant-system.toml',hub/'calculations/steam-generator/Coolant pump estimate - Hurmet.md',hub/'calculations/steam-generator/Generator sizing - Hurmet.md',models/'models/wistr_installation.py',models/'models/coolant_assembly.py',report_path]
    result={'date':'2026-10-14','status':'Preliminary normal pressure envelope; no relief sizing or SG failure assessment','inputs':{k:{'value':x,'unit':u} for k,(x,u) in inputs.items()},'hurmet_checks':checks,'allocation_checks':{'passed':True,'vertices':5,'random_allocations':100,'checks':['closed-loop pressure closure','every station within correlated bounds','three legs have equal elevations']},'sources':[{'path':str(p.relative_to(hub)) if p.is_relative_to(hub) else '../fastSaltModels/'+str(p.relative_to(models)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources]}
    out.mkdir(parents=True,exist_ok=True)
    (out/'Normal coolant pressure profile - Hurmet.md').write_text('\n\n'.join(md)+'\n')
    (out/'coolant-pressure-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--hub',type=Path,default=HERE.parents[1]);parser.add_argument('--models',type=Path);parser.add_argument('--output',type=Path,default=HERE)
    args=parser.parse_args();hub=args.hub.resolve();publish(hub,(args.models or hub.parent/'fastSaltModels').resolve(),args.output.resolve())
