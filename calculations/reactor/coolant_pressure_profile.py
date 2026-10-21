"""Publish the itemized normal coolant pressure profile; no Blender required."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import argparse,hashlib,json,sys,tomllib
HERE=Path(__file__).resolve().parent

def publish(hub,models,out):
    sys.path[:0]=[str(models/'src'),str(models/'models')]
    import wistr_installation as layout,coolant_assembly
    from textual_graphics.assembly_model import document
    source=hub/'calculations/steam-generator/coolant-pump-itemized-results.json'
    budget=json.loads(source.read_text());b=budget['hurmet_checks'];bi={k:v['value'] for k,v in budget['inputs'].items()}
    # Stop if an upstream input changed without regenerating its loss budget.
    for s in budget['sources']:
        assert hashlib.sha256((hub/s['path']).read_bytes()).hexdigest()==s['sha256'],s['path']
    doc=document(coolant_assembly.build_model(layout,coolant_assembly.reactor_interface(layout,models),models))
    report_path=models/layout.REACTOR['baseline']/'reactor-study-report.json'
    report=json.loads(report_path.read_text())
    def z(port):return doc['ports'][port]['world_position_m'][2]-layout.FLOOR_Z
    pressure_path=hub/'design/pids/coolant-system/coolant-system.toml'
    pressure=tomllib.loads(pressure_path.read_text())['gas_pressure_control']
    assert pressure['bias_pressure_reference']=='gauge'
    routes={r['name']:r for r in budget['routes']}
    suction=routes['leg_1.cold_suction'];cold_return=routes['leg_1.cold_inlet'];hot=routes['leg_1.hot_outlet']
    inp={
        'TopPressure':(pressure['bias_pressure_Pa'],'Pa'),
        'Density':(b['MeanDensity'],'kg/m3'),'Gravity':(bi['Gravity'],'m/s2'),
        'TopZ':(layout.STEAM_GENERATORS['casing_bottom']+layout.STEAM_GENERATORS['height']-layout.FLOOR_Z,'m'),
        'SGInZ':(z('leg_1.generator.salt_inlet'),'m'),'SGOutZ':(z('leg_1.generator.salt_outlet'),'m'),
        'SuctionZ':(z('leg_1.pump.suction'),'m'),'DischargeZ':(z('leg_1.pump.discharge'),'m'),
        'ReactorInZ':(z('reactor.cold_inlet_1'),'m'),
        'BottomZ':(layout.REACTOR['origin_z']-layout.FLOOR_Z+report['derived_dimensions']['bottom_reflector_z']/2,'m'),
        'ReactorOutZ':(z('reactor.hot_outlet_1'),'m'),
        'SuctionLengthFraction':(suction['length_m']/(suction['length_m']+cold_return['length_m']),''),
        'SuctionBends':(len(suction['bend_angles_deg']),''),'ReturnBends':(len(cold_return['bend_angles_deg']),''),'HotBends':(len(hot['bend_angles_deg']),''),
        'CorePassageLoss':(bi['CorePassageLoss'],'Pa'),
    }
    for n in ['SGFriction','SGDynamic','HotDynamic','ColdDynamic','HotStraight','ColdStraight','HotNozzleDynamic','ColdNozzleDynamic','HotNozzleFriction','ColdNozzleFriction','DownFriction','DownDynamic']:
        inp[n]=(b[n]*1000,'Pa')
    v={n:x for n,(x,u) in inp.items()};checks={};md=[]
    def text(s):md.append(s.strip())
    def C(n,expr,u='',scale=1):
        x=eval(expr,{'__builtins__':{}},v);v[n]=x;checks[n]=x/scale
        text(f'¢??` {n} = {expr} = 〔{x/scale:.10g}〕 {u} `')
    text('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Normal coolant pressure profile

**Itemized revision, 14 October 2026.** Replaces the earlier 50%-allowance pressure envelope, preserved in `revisions/pressure-before-itemized-2026-10-14/`. All pressures are gauge. Reference: **1 bar(g) at the SG tops**, provisionally 17 m above floor.

Use the checked [itemized pump estimate](../steam-generator/Itemized%20coolant%20pump%20estimate%20-%20Hurmet.md): total flow 18,500 kg/s, three equal legs, 810–890 K, and the required pump pressure rise shown below in the base case. D-063 replaces the earlier SG geometry with the counterSG workbook's 4,902 salt tubes, 20 mm bore and 11.920866 m straight hydraulic length. Its individual loss terms are explicitly imported; this sheet allocates them and calculates station pressures. D-063 adopts this revised case into the shared graphics/P&ID records; this calculation continues to import the checked itemized budget directly.

This remains a mean-density hydraulic-grade screen. Use 1633.7825 kg/m³ (850 K) for elevation effects, retaining hot/cold properties already used for the upstream loss calculation. Neglect local velocity-head changes, acceleration and thermosiphon credit. No pressure rating, relief setting, pump curve or NPSH qualification is established.

## Loss locations

- **SG hot connection → SG cold connection:** SG tube friction, tube entrance/exit, both collector/distribution allowances.
- **SG cold connection → pump suction:** Suction share of cold straight-pipe friction and two bends.
- **Pump discharge → reactor cold-nozzle outer connection:** Remaining cold-pipe friction, two bends and the cold isolation-valve allowance.
- **Reactor cold connection → bottom-plenum midpoint:** Cold nozzle friction/discharge, downcomer friction and bulk-turn allowance.
- **Bottom-plenum midpoint → reactor hot-nozzle outer connection:** Core/reflector passage with its end losses, hot nozzle entrance and friction.
- **Reactor hot connection → SG hot connection:** Hot-pipe friction, three bends and hot isolation-valve allowance.

The isolation valves are downstream of the pump and in the hot return respectively, consistent with the draft P&ID. Both SG collector allowances are grouped across the SG. The top pressure reference is related hydrostatically to the hot connection; its exact gas tap/free-surface relationship to the collector remains unresolved. These are schematic allocations, not detailed internal pressure profiles.

The bottom point is the **bottom-plenum midpoint**, not the lowest vessel wall or the maximum pressure anywhere. Tube-entry pressures and local nozzle velocities are not resolved. Core height stays 3.4 m, as corrected by the owner.

## Imported inputs and geometry

Elevations are current visual-layout values. Suction straight loss is split by route length; bend counts come from the three-leg assembly. Actual accumulator salt level is not yet modeled, so casing-top height is provisional.
''')
    text('¢` format = "h7" `')
    for n,(x,u) in inp.items():text(f'¢` {n} = {x:.12g} {u} `')
    C('Gradient','Density * Gravity',"'bar/m'",1e5)
    C('SuctionStraight','ColdStraight * SuctionLengthFraction','kPa',1000)
    C('ReturnStraight','ColdStraight - SuctionStraight','kPa',1000)
    # Tuple order: SG end, bend, collector, reactor entry, reactor exit, valve, bulk turn.
    cases={'Base':(1.5,.3,1.,1.,.5,.2,2.),'Low':(1.,.15,.5,.5,.25,.05,1.),'High':(2.,.6,2.,2.,1.,1.,5.)}
    for case,ks in cases.items():
        text(f'## {case} fitting-loss case')
        if case=='Base':text('This is the current working profile. The segment losses must sum to the independently published itemized pump rise.')
        else:text('Sensitivity only: change the same local coefficients as the itemized pump worksheet. Each case has its own required pump head at fixed flow. This is not operation on one unchanged pump curve or a statistical confidence bound. Core passage loss and SG friction stay fixed.')
        for suffix,x in zip(['SGEndK','BendK','CollectorK','ReactorEntryK','ReactorExitK','ValveK','BulkK'],ks):
            n=case+suffix;v[n]=x;text(f'¢` {n} = {x:g} `')
        expressions={
          'SGSegment':f'SGFriction + {case}SGEndK * SGDynamic + {case}CollectorK * (HotDynamic + ColdDynamic)',
          'SuctionSegment':f'SuctionStraight + SuctionBends * {case}BendK * ColdDynamic',
          'ReturnSegment':f'ReturnStraight + ReturnBends * {case}BendK * ColdDynamic + {case}ValveK * ColdDynamic',
          'DownSegment':f'ColdNozzleFriction + {case}ReactorEntryK * ColdNozzleDynamic + DownFriction + {case}BulkK * DownDynamic',
          'UpSegment':f'CorePassageLoss + HotNozzleFriction + {case}ReactorExitK * HotNozzleDynamic',
          'HotSegment':f'HotStraight + HotBends * {case}BendK * HotDynamic + {case}ValveK * HotDynamic',
        }
        for suffix,e in expressions.items():C(case+suffix,e,'kPa',1000)
        C(case+'PumpRise',' + '.join(case+n for n in expressions),'kPa',1000)
        C(case+'SGIn','TopPressure + Density * Gravity * (TopZ - SGInZ)','bar',1e5)
        C(case+'SGOut',f'{case}SGIn + Density * Gravity * (SGInZ - SGOutZ) - {case}SGSegment','bar',1e5)
        C(case+'Suction',f'{case}SGOut + Density * Gravity * (SGOutZ - SuctionZ) - {case}SuctionSegment','bar',1e5)
        C(case+'Discharge',f'{case}Suction + Density * Gravity * (SuctionZ - DischargeZ) + {case}PumpRise','bar',1e5)
        C(case+'ReactorIn',f'{case}Discharge + Density * Gravity * (DischargeZ - ReactorInZ) - {case}ReturnSegment','bar',1e5)
        C(case+'Bottom',f'{case}ReactorIn + Density * Gravity * (ReactorInZ - BottomZ) - {case}DownSegment','bar',1e5)
        C(case+'ReactorOut',f'{case}Bottom + Density * Gravity * (BottomZ - ReactorOutZ) - {case}UpSegment','bar',1e5)
        C(case+'ReturnToSG',f'{case}ReactorOut + Density * Gravity * (ReactorOutZ - SGInZ) - {case}HotSegment','bar',1e5)
        C(case+'ClosureError',f'{case}ReturnToSG - {case}SGIn','Pa')
        assert abs(v[case+'ClosureError'])<1e-7
        expected=b['PumpRise' if case=='Base' else case+'Rise']*1000
        assert abs(v[case+'PumpRise']-expected)<1e-6
    text('''## Lower bias comparison and interpretation

Keeping all losses, density and duty fixed, lowering SG-top pressure from 1 to 0.5 bar(g) shifts every station downward by exactly 0.5 bar. This comparison is not an adopted operating target. The previous broad suction interval came from allowing all unlocated resistance to sit in the suction line; it is superseded by the itemized suction resistance here.
''')
    text('¢` LowerTopPressure = 50000 Pa `');v['LowerTopPressure']=50000
    C('LowerBiasSuction','BaseSuction + LowerTopPressure - TopPressure','bar',1e5)
    C('LowerBiasBottom','BaseBottom + LowerTopPressure - TopPressure','bar',1e5)
    text('''## Limits and verification

- Mean-density hydrostatics close the base loop exactly with the itemized pump rise. A true variable-density network changes the required pump head through buoyancy and pressure/energy conversion. This revision does not claim that analysis.
- Main-pipe velocity pressure is roughly 0.045–0.046 bar and nozzle values are roughly 0.06 bar. Neglected velocity changes and unresolved collector/reference geometry limit interpretation of hundredths of a bar.
- A 1 m change in the assumed top liquid reference shifts station pressures about 0.160 bar. Uniform hot/cold density perturbations check hydrostatic sensitivity only; they do not recalculate friction or model thermal stratification.
- Low/high fitting cases are correlated. A lower SG resistance raises pump suction, while higher downstream resistance raises required discharge pressure. They are not independently selectable station limits.
- TK-401 stays separate while transfer valves are closed; its pressure is not assigned the SG reference. Gas-vessel physical level, detailed suction conditions, pump curve, piping restrictions and flow maldistribution remain unresolved.
- No SG failure, relief sizing, motor selection, building change or Blender regeneration is included. D-063 adopts the revised normal duty and station-pressure basis into the shared P&ID/graphics records, with existing motor envelopes retained.

Sources: the checked itemized pump results, current assembly ports, D-059 pressure reference and D-060 flow/temperature/height basis. Original source hashes and loss-budget inputs are retained upstream; this sheet records hashes of what it imports. General method: [DOE Fluid Flow handbook](https://www.energy.gov/ehss/articles/doe-hdbk-10123-92), extended pressure/elevation/pump/loss balance.

Run `python calculations/reactor/coolant_pressure_profile.py`, then `node calculations/reactor/check_coolant_pressure.cjs` with the Hurmet bundles configured. Python checks source hashes, loss-budget closure and each pressure loop; Hurmet recalculates, saves/reopens and exercises pressure-datum, elevation and hydrostatic-density sensitivities. The earlier broad-range calculation is preserved as a historical snapshot, not a parallel active calculation.
''')
    sources=[source,pressure_path,models/'models/wistr_installation.py',models/'models/coolant_assembly.py',report_path]
    data={'date':'2026-10-14','revision':'itemized','status':'Preliminary mean-density station pressures; no relief or SG-failure analysis','inputs':{n:{'value':x,'unit':u} for n,(x,u) in inp.items()},'hurmet_checks':checks,'cases':{case:{'coefficients':list(ks),'pump_rise_kPa':v[case+'PumpRise']/1000,'pressures_bar_g':{n:v[case+n]/1e5 for n in ['SGIn','SGOut','Suction','Discharge','ReactorIn','Bottom','ReactorOut']},'segments_kPa':{n:v[case+n]/1000 for n in ['SGSegment','SuctionSegment','ReturnSegment','DownSegment','UpSegment','HotSegment']},'closure_error_Pa':v[case+'ClosureError']} for case,ks in cases.items()},'sources':[{'path':str(p.relative_to(hub)) if p.is_relative_to(hub) else '../fastSaltModels/'+str(p.relative_to(models)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources]}
    out.mkdir(parents=True,exist_ok=True)
    write_worksheet(out/'Normal coolant pressure profile - Hurmet.md', '\n\n'.join(md)+'\n')
    (out/'coolant-pressure-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data['cases'],indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--hub',type=Path,default=HERE.parents[1]);p.add_argument('--models',type=Path);p.add_argument('--output',type=Path,default=HERE)
    a=p.parse_args();publish(a.hub.resolve(),(a.models or a.hub.parent/'fastSaltModels').resolve(),a.output.resolve())
