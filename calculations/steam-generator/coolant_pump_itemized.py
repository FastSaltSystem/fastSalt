"""Itemized three-leg coolant pump estimate at owner-selected UM flow."""

# Shared Hurmet publication style; calculation inputs retain full precision.
import sys as _hurmet_sys
from pathlib import Path as _HurmetPath
_hurmet_sys.path.insert(0, str(_HurmetPath(__file__).resolve().parents[1]))
from hurmet_style import write_worksheet

from pathlib import Path
import argparse,hashlib,json,math,re,sys
HERE=Path(__file__).resolve().parent

def publish(hub,models,out):
    sys.path[:0]=[str(hub/'calculations/reactor'),str(models/'models'),str(models/'src')]
    from core_coolant_loss import darcy
    from coolant_inventory import rounded_length
    import wistr_installation as layout,coolant_assembly
    from textual_graphics.assembly_model import document
    core_path=hub/'calculations/reactor/core-coolant-loss-results.json'
    core=json.loads(core_path.read_text());ci=core['inputs'];cr=core['hurmet_checks']
    from counter_sg_basis import read_basis, SOURCE as sg_path
    sg=read_basis()
    assert (sg['salt_hot_K'],sg['salt_cold_K']) == (ci['OutletTemperature']['value'],ci['InletTemperature']['value'])
    doc=document(coolant_assembly.build_model(layout,coolant_assembly.reactor_interface(layout,models),models))
    report_path=models/layout.REACTOR['baseline']/'reactor-study-report.json'
    report=json.loads(report_path.read_text());d=report['derived_dimensions']
    routes=[]
    for name,c in doc['connections'].items():
        pts=c['points_m'];angles=[]
        for a,b,e in zip(pts,pts[1:],pts[2:]):
            u=[b[i]-a[i] for i in range(3)];v=[e[i]-b[i] for i in range(3)]
            angle=math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(u,v))/math.dist(a,b)/math.dist(b,e)))))
            if angle>.01:angles.append(angle)
        routes.append({'name':name,'service':c['service'],'length_m':rounded_length(pts,max(1.5,c['spec']['jacket_od'])),'bend_angles_deg':angles})
    legs={i:[r for r in routes if r['name'].startswith(f'leg_{i}.')] for i in (1,2,3)}
    for i in (2,3):
        assert abs(sum(r['length_m'] for r in legs[i])-sum(r['length_m'] for r in legs[1]))<1e-6
    one=legs[1]
    inp={
      'TotalMassFlow':(ci['MassFlow']['value'],'kg/s'),'Legs':(3,''),
      'HotTemperature':(ci['OutletTemperature']['value'],'K'),'ColdTemperature':(ci['InletTemperature']['value'],'K'),
      'DensityIntercept':(ci['DensityIntercept']['value'],"'kg/m3'"),'DensitySlope':(ci['DensitySlope']['value'],"'kg.m-3.K-1'"),
      'ViscosityScale':(ci['ViscosityScale']['value'],'Pa.s'),'ViscosityTemperature':(ci['ViscosityTemperature']['value'],'K'),
      'SGTubeCount':(sg['salt_tubes_per_generator'],''),'SGTubeBore':(sg['tube_bore_m'],'m'),'SGTubeLength':(sg['tube_length_m'],'m'),
      'TubeRoughness':(1e-6,'m'),'PipeRoughness':(2e-6,'m'),
      'CorePassageLoss':(cr['TotalLoss']*1000,'Pa'),
      'MainBore':(layout.PIPE_SPECS['hot']['bore'],'m'),
      'HotPipeLength':(sum(r['length_m'] for r in one if r['service']=='hot'),'m'),
      'ColdPipeLength':(sum(r['length_m'] for r in one if r['service']=='cold'),'m'),
      'HotBends':(sum(len(r['bend_angles_deg']) for r in one if r['service']=='hot'),''),
      'ColdBends':(sum(len(r['bend_angles_deg']) for r in one if r['service']=='cold'),''),
      'NozzleBore':(report['connections']['pipe_diameter']-2*.035,'m'),
      'HotNozzleLength':(d['pipe_end_radius']-d['hot_inner_radius'],'m'),
      'ColdNozzleLength':(d['pipe_end_radius']+.35-d['vessel_inner_radius'],'m'),
      'DownOuterRadius':(d['vessel_inner_radius'],'m'),'DownInnerRadius':(d['reflector_radius'],'m'),
      'DownLength':(d['cold_inlet_z']-.375,'m'),
      'SGEndK':(1.5,''),'BendK':(.3,''),'CollectorK':(1.,''),
      'ReactorEntryK':(1.,''),'ReactorExitK':(.5,''),'ValveK':(.2,''),'BulkTurnK':(2.,''),
      'PumpEfficiency':(.80,''),'MotorEfficiency':(.96,''),'Gravity':(9.80665,'m/s2'),
    }
    values={n:x for n,(x,u) in inp.items()};checks={};md=[]
    def text(s):md.append(s.strip())
    def C(n,expr,u='',scale=1):
        x=eval(expr.replace('^','**'),{'__builtins__':{},'pi':math.pi,'exp':math.exp,'Darcy':darcy},values)
        values[n]=x;checks[n]=x/scale;text(f'¢??` {n} = {expr} = 〔{x/scale:.10g}〕 {u} `')
    text('''---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Itemized coolant pump estimate

Preliminary normal-duty estimate, 14 October 2026. Replaces the blanket SG-loss × 1.5 estimate for this calculation with individually identified loss terms. **All three circulation pumps** are included; P-401 and auxiliary pumps are excluded.

Use the owner-selected UM total core flow of 18,500 kg/s and 810–890 K temperatures. Each SG/pump leg carries one third of that mass flow. All pumps overcome the same common-core pressure loss; that loss is not multiplied by three when calculating the head for one loop.

## Scope and assumptions

D-063 adopts the newer counterSG workbook: 4,902 parallel salt tubes per generator, 20 mm bore, 24 mm OD and 11.920866 m calculated heat-transfer length. Use that length provisionally as the straight hydraulic length, with separate end/collector losses; additional unheated tube extensions are not yet defined. Friction is recalculated at 18,500/3 kg/s and 850 K using Colebrook. The 17 m casing remains a visual envelope. The workbook uses 6,170.52 kg/s per generator; hydraulics retain 6,166.67 kg/s. UM properties are retained for consistency with the core. Thermal-length arithmetic is independently checked, not qualified for actual contact conductance or heat-transfer correlations.

CorePassageLoss is explicitly imported from the checked core Hurmet estimate: 3.4 m core + 0.55 m reflector passages + provisional entrance/exit losses. It is not recomputed from graphics. Downcomer and nozzle losses below are additional; the core entrance/exit terms are not added a second time.

Pipe lengths and seven direction changes per leg come from the current resolved assembly. Three bends are on the hot route; four on the cold suction/return routes. One angle is shallow, and bend radii are visual geometry; use an editable K = 0.3 per bend as a preliminary allowance, not a fitting qualification. Arc length is retained in pipe friction while K represents additional bend loss.

Other editable local coefficients: SG tube entrance/exit combined 1.5 (based on tube velocity); one SG collector allowance K = 1 on each hot/cold main-pipe velocity; reactor cold-nozzle discharge K = 1 and hot-nozzle entry K = 0.5 (based on nozzle velocity); one proposed fully open isolation valve on each main hot/cold branch, K = 0.2 each; and reactor bulk-turn K = 2 based on downcomer velocity. Collector allowances cover main-pipe transitions/distribution, separate from tube ends. Valve type and flow control are unselected. These are itemized assumptions, not measured losses.

Use clean tubing roughness 1 micrometre, as in existing core/SG estimates, and 2 micrometres for main pipe/nozzles. Actual deposits and surface condition remain open. Use uniform annular downcomer geometry for a small bulk-loss screen; supports, reduced local area and uneven entry distribution may change it.

No full-height static lift is added to a filled closed loop. No favorable thermosiphon-head credit is taken. The small variable-density loop head and segment pressure-to-energy conversion need a detailed hydraulic network; this estimate sums loss pressures and uses **cold-leg volume flow at the pump** for shaft power.
''')
    text('¢` format = "h7" `')
    for n,(x,u) in inp.items():text(f'¢` {n} = {x:.12g} {u} `')
    text('''¢` function Darcy(rey, relative)
    if rey < 4000 throw "Turbulent model requires Re above 4000"
    x = 8
    for i in 1:30
        x = -2 * ln(relative / 3.7 + 2.51 * x / rey) / ln(10)
    end
    return 1 / x^2
end `''')
    text('## Properties and flow')
    for n,e,u,s in [
        ('MeanTemperature','(HotTemperature + ColdTemperature) / 2','K',1),
        ('MeanDensity','DensityIntercept - DensitySlope * MeanTemperature','kg/m3',1),
        ('HotDensity','DensityIntercept - DensitySlope * HotTemperature','kg/m3',1),
        ('ColdDensity','DensityIntercept - DensitySlope * ColdTemperature','kg/m3',1),
        ('MeanViscosity','ViscosityScale * exp(ViscosityTemperature / MeanTemperature)','Pa.s',1),
        ('HotViscosity','ViscosityScale * exp(ViscosityTemperature / HotTemperature)','Pa.s',1),
        ('ColdViscosity','ViscosityScale * exp(ViscosityTemperature / ColdTemperature)','Pa.s',1),
        ('LegMassFlow','TotalMassFlow / Legs','kg/s',1),
        ('PumpVolumeFlow','LegMassFlow / ColdDensity','m3/s',1),
        ('SGVelocity','LegMassFlow / (MeanDensity * SGTubeCount * pi * SGTubeBore^2 / 4)','m/s',1),
        ('SGReynolds','MeanDensity * SGVelocity * SGTubeBore / MeanViscosity','',1),
        ('SGFactor','Darcy(SGReynolds, TubeRoughness / SGTubeBore)','',1),
        ('SGDynamic','MeanDensity * SGVelocity^2 / 2','kPa',1000),
        ('SGFriction','SGFactor * SGTubeLength / SGTubeBore * SGDynamic','kPa',1000),
        ('SGEnds','SGEndK * SGDynamic','kPa',1000),
    ]:C(n,e,u,s)
    text('## Main piping and connections')
    for prefix in ['Hot','Cold']:
        C(prefix+'Velocity',f'LegMassFlow / ({prefix}Density * pi * MainBore^2 / 4)','m/s')
        C(prefix+'Dynamic',f'{prefix}Density * {prefix}Velocity^2 / 2','kPa',1000)
        C(prefix+'Factor',f'Darcy({prefix}Density * {prefix}Velocity * MainBore / {prefix}Viscosity, PipeRoughness / MainBore)')
        C(prefix+'Straight',f'{prefix}Factor * {prefix}PipeLength / MainBore * {prefix}Dynamic','kPa',1000)
        C(prefix+'NozzleVelocity',f'LegMassFlow / ({prefix}Density * pi * NozzleBore^2 / 4)','m/s')
        C(prefix+'NozzleDynamic',f'{prefix}Density * {prefix}NozzleVelocity^2 / 2','kPa',1000)
        C(prefix+'NozzleFactor',f'Darcy({prefix}Density * {prefix}NozzleVelocity * NozzleBore / {prefix}Viscosity, PipeRoughness / NozzleBore)')
        C(prefix+'NozzleFriction',f'{prefix}NozzleFactor * {prefix}NozzleLength / NozzleBore * {prefix}NozzleDynamic','kPa',1000)
    C('StraightLoss','HotStraight + ColdStraight + HotNozzleFriction + ColdNozzleFriction','kPa',1000)
    C('BendLoss','BendK * (HotBends * HotDynamic + ColdBends * ColdDynamic)','kPa',1000)
    C('CollectorLoss','CollectorK * (HotDynamic + ColdDynamic)','kPa',1000)
    C('ReactorNozzleLoss','ReactorEntryK * ColdNozzleDynamic + ReactorExitK * HotNozzleDynamic','kPa',1000)
    C('ValveLoss','ValveK * (HotDynamic + ColdDynamic)','kPa',1000)
    text('## Bulk reactor passage and total duty')
    for n,e,u,s in [
        ('DownArea','pi * (DownOuterRadius^2 - DownInnerRadius^2)','m2',1),
        ('DownDiameter','2 * (DownOuterRadius - DownInnerRadius)','m',1),
        ('DownVelocity','TotalMassFlow / (ColdDensity * DownArea)','m/s',1),
        ('DownDynamic','ColdDensity * DownVelocity^2 / 2','kPa',1000),
        ('DownFactor','Darcy(ColdDensity * DownVelocity * DownDiameter / ColdViscosity, PipeRoughness / DownDiameter)','',1),
        ('DownFriction','DownFactor * DownLength / DownDiameter * DownDynamic','kPa',1000),
        ('BulkTurnLoss','BulkTurnK * DownDynamic','kPa',1000),
        ('KnownGeometryLoss','SGFriction + CorePassageLoss + StraightLoss + DownFriction','kPa',1000),
        ('LocalLoss','SGEnds + BendLoss + CollectorLoss + ReactorNozzleLoss + ValveLoss + BulkTurnLoss','kPa',1000),
        ('PumpRise','KnownGeometryLoss + LocalLoss','kPa',1000),
        ('PumpHead','PumpRise / (ColdDensity * Gravity)','m',1),
        ('HydraulicPerPump','PumpRise * PumpVolumeFlow','kW',1000),
        ('ShaftPerPump','HydraulicPerPump / PumpEfficiency','kW',1000),
        ('ElectricalPerPump','ShaftPerPump / MotorEfficiency','kW',1000),
        ('TotalHydraulic','Legs * HydraulicPerPump','MW',1e6),
        ('TotalShaft','Legs * ShaftPerPump','MW',1e6),
        ('TotalElectrical','Legs * ElectricalPerPump','MW',1e6),
        ('BareSubtotalElectrical','Legs * KnownGeometryLoss * PumpVolumeFlow / (PumpEfficiency * MotorEfficiency)','MW',1e6),
    ]:C(n,e,u,s)
    text('''KnownGeometryLoss is a subtotal, not a validated lower bound: it includes the already-provisional core end allowance. LocalLoss adds only the additional listed items. PumpHead is differential head, not system operating/design pressure. Shaft power is motor mechanical output; electrical power is supply input. Motor nameplate margin, starting duty and supplier selection are not determined here.

## Local-loss sensitivity

Use these deliberately broad coefficient cases for uncertainty in unselected fittings. They are not statistical confidence bounds. Both retain baseline core loss, SG length/roughness and efficiencies. Low/high: SG tube ends 1/2; bend K 0.15/0.6; each collector 0.5/2; reactor cold entry 0.5/2 and hot exit 0.25/1; each open valve 0.05/1; bulk turn 1/5.
''')
    C('LowLocalLoss','SGDynamic + 0.15 * (HotBends * HotDynamic + ColdBends * ColdDynamic) + 0.5 * (HotDynamic + ColdDynamic) + 0.5 * ColdNozzleDynamic + 0.25 * HotNozzleDynamic + 0.05 * (HotDynamic + ColdDynamic) + DownDynamic','kPa',1000)
    C('HighLocalLoss','2 * SGDynamic + 0.6 * (HotBends * HotDynamic + ColdBends * ColdDynamic) + 2 * (HotDynamic + ColdDynamic) + 2 * ColdNozzleDynamic + HotNozzleDynamic + HotDynamic + ColdDynamic + 5 * DownDynamic','kPa',1000)
    for prefix in ['Low','High']:
        C(prefix+'Rise',f'KnownGeometryLoss + {prefix}LocalLoss','kPa',1000)
        C(prefix+'Electrical',f'Legs * {prefix}Rise * PumpVolumeFlow / (PumpEfficiency * MotorEfficiency)','MW',1e6)
    text('## Comparison with the earlier allowance')
    C('SameFlowOldMethod','1.5 * SGFriction','kPa',1000)
    C('SameFlowOldElectrical','Legs * SameFlowOldMethod * PumpVolumeFlow / (PumpEfficiency * MotorEfficiency)','MW',1e6)
    text('''The old sheet's 5.166 MW total electrical estimate also used the larger 22,699 kg/s total flow. Separate that operating-basis change from replacing the 50% allowance: at the same adopted flow and newer SG geometry, SG friction × 1.5 is below the itemized working estimate. The pre-counterSG itemized case was 3.355 MW; its archived revision isolates the geometry change. No blanket percentage has been added to the new total.

## Sources, checks and remaining work

- Owner-selected UM case and [core loss](../reactor/Core%20coolant%20pressure%20loss%20-%20Hurmet.md), D-060. Core loss is imported explicitly and must be recalculated if flow, tube count/bore or temperature changes.
- [Adopted counterSG workbook](sources/counterSG.xlsx), sheet counter: AC20 salt-tube count, AC8 bore, Y66 length. The two salt inlet/outlet labels were corrected with no numerical/formula change. `counter_sg_basis.py` independently reproduces all 62 length increments. [Source record](sources/README.md). The original Generator sizing Hurmet sheet remains historical.
- Current resolved geometry from `fastSaltModels/models/coolant_assembly.py` and `wistr_installation.py`; isolated nozzle bore remains a provisional 1.33 m (1.4 m OD less 35 mm walls), differing from the installation's 1.425 m main bore. Transition details are included only in provisional local terms.
- [NASA KSC-STD-Z-0017 Rev A](https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017_RevA_Final.pdf), §§7.4–8.1: Colebrook/Darcy methods, accounting for fitting losses, and representative clean stainless roughness. Local coefficients chosen here are engineering assumptions, not values certified by that standard for this plant.

The calculation is suitable for a preliminary power budget. Detailed SG collectors, valve selection, actual bends, restrictions, bypass/flow balance, pump efficiency/curve/NPSH, off-normal states and variable-density network closure remain unresolved. No motor downsizing, Blender change, pressure-protection design or SG failure assessment is made. D-063 supersedes the D-061 SG geometry and adopts this preliminary duty into the shared graphics/P&ID model; existing 2 MW motor reservations and geometric envelopes are retained.

Run `python calculations/steam-generator/coolant_pump_itemized.py`, then `node calculations/steam-generator/check_coolant_pump_itemized.cjs` with the project HURMET_ENGINE/TEMML_ENGINE bundles. Inputs, source hashes, routes and external roughness/efficiency sensitivities are saved in `coolant-pump-itemized-results.json`; Hurmet results are verified independently in SI arithmetic. Generated HTML is ignored output.
''')
    v=values
    assert 0<v['LowElectrical']<v['TotalElectrical']<v['HighElectrical']
    assert abs(v['TotalElectrical']*v['PumpEfficiency']*v['MotorEfficiency']-v['TotalHydraulic'])<1e-6
    sensitivity=[]
    for rough in [1e-6,1e-5,4.5e-5]:
        sgfr=darcy(v['SGReynolds'],rough/v['SGTubeBore'])*v['SGTubeLength']/v['SGTubeBore']*v['SGDynamic']
        # Recompute core resistance at same roughness, same K=1.5.
        corefr=(darcy(cr['Reynolds'],rough/ci['TubeBore']['value'])*cr['PassageLength']/ci['TubeBore']['value']+1.5)*cr['DynamicPressure']*1000
        rise=v['PumpRise']-v['SGFriction']-v['CorePassageLoss']+sgfr+corefr
        sensitivity.append({'tube_roughness_m':rough,'SG_friction_kPa':sgfr/1000,'core_with_ends_kPa':corefr/1000,'total_electrical_MW':3*rise*v['PumpVolumeFlow']/.8/.96/1e6})
    sources=[core_path,sg_path,HERE/'counter_sg_basis.py',models/'models/wistr_installation.py',models/'models/coolant_assembly.py',report_path]
    result_data={'date':'2026-10-14','status':'Preliminary itemized normal-duty power; no blanket allowance or motor selection','inputs':{n:{'value':x,'unit':u} for n,(x,u) in inp.items()},'hurmet_checks':checks,'routes':routes,'roughness_sensitivity_external':sensitivity,'efficiency_sensitivity_external':[{'pump_efficiency':eta,'motor_efficiency':.96,'total_electrical_MW':v['TotalHydraulic']/eta/.96/1e6} for eta in [.75,.8,.85]],'sources':[{'path':str(p.relative_to(hub)) if p.is_relative_to(hub) else '../fastSaltModels/'+str(p.relative_to(models)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources]}
    out.mkdir(parents=True,exist_ok=True)
    write_worksheet(out/'Itemized coolant pump estimate - Hurmet.md', '\n\n'.join(md)+'\n')
    (out/'coolant-pump-itemized-results.json').write_text(json.dumps(result_data,indent=2)+'\n')
    for n in ['SGFriction','SGEnds','CorePassageLoss','StraightLoss','BendLoss','CollectorLoss','ReactorNozzleLoss','ValveLoss','DownFriction','BulkTurnLoss','PumpRise','PumpHead','ShaftPerPump','ElectricalPerPump','TotalElectrical','LowElectrical','HighElectrical','SameFlowOldElectrical']:
        print(n,checks.get(n,v[n]))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--hub',type=Path,default=HERE.parents[1]);p.add_argument('--models',type=Path);p.add_argument('--output',type=Path,default=HERE)
    a=p.parse_args();publish(a.hub.resolve(),(a.models or a.hub.parent/'fastSaltModels').resolve(),a.output.resolve())
