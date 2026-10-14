---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Itemized coolant pump estimate

Preliminary normal-duty estimate, 14 October 2026. Replaces the blanket SG-loss
× 1.5 estimate for this calculation with individually identified loss terms.
**All three circulation pumps** are included; P-401 and auxiliary pumps are
excluded.

Use the owner-selected UM total core flow of 18,500 kg/s and 810–890 K
temperatures. Each SG/pump leg carries one third of that mass flow. All pumps
overcome the same common-core pressure loss; that loss is not multiplied by
three when calculating the head for one loop.

## Scope and assumptions

The SG retains its previously calculated 12,090 parallel salt tubes per
generator, 14 mm bore and 19.879 m hydraulic length. Its friction is
recalculated at the revised flow and 850 K mean temperature using Colebrook,
not simply scaled by flow squared. The 17 m visible casing is not substituted
for tube length. SG thermal performance at the revised temperatures is not
requalified here.

CorePassageLoss is explicitly imported from the checked core Hurmet estimate:
3.4 m core + 0.55 m reflector passages + provisional entrance/exit losses. It
is not recomputed from graphics. Downcomer and nozzle losses below are
additional; the core entrance/exit terms are not added a second time.

Pipe lengths and seven direction changes per leg come from the current resolved
assembly. Three bends are on the hot route; four on the cold suction/return
routes. One angle is shallow, and bend radii are visual geometry; use an
editable K = 0.3 per bend as a preliminary allowance, not a fitting
qualification. Arc length is retained in pipe friction while K represents
additional bend loss.

Other editable local coefficients: SG tube entrance/exit combined 1.5 (based on
tube velocity); one SG collector allowance K = 1 on each hot/cold main-pipe
velocity; reactor cold-nozzle discharge K = 1 and hot-nozzle entry K = 0.5
(based on nozzle velocity); one proposed fully open isolation valve on each
main hot/cold branch, K = 0.2 each; and reactor bulk-turn K = 2 based on
downcomer velocity. Collector allowances cover main-pipe
transitions/distribution, separate from tube ends. Valve type and flow control
are unselected. These are itemized assumptions, not measured losses.

Use clean tubing roughness 1 micrometre, as in existing core/SG estimates, and 2
micrometres for main pipe/nozzles. Actual deposits and surface condition remain
open. Use uniform annular downcomer geometry for a small bulk-loss screen;
supports, reduced local area and uneven entry distribution may change it.

No full-height static lift is added to a filled closed loop. No favorable
thermosiphon-head credit is taken. The small variable-density loop head and
segment pressure-to-energy conversion need a detailed hydraulic network; this
estimate sums loss pressures and uses **cold-leg volume flow at the pump** for
shaft power.

¢` format = "h7" `

¢` TotalMassFlow = 18500 kg/s `

¢` Legs = 3 `

¢` HotTemperature = 890 K `

¢` ColdTemperature = 810 K `

¢` DensityIntercept = 2112.8 'kg/m3' `

¢` DensitySlope = 0.56355 'kg.m-3.K-1' `

¢` ViscosityScale = 0.0007064 Pa.s `

¢` ViscosityTemperature = 1204.1 K `

¢` SGTubeCount = 12090 `

¢` SGTubeBore = 0.014 m `

¢` SGTubeLength = 19.8790057 m `

¢` TubeRoughness = 1e-06 m `

¢` PipeRoughness = 2e-06 m `

¢` CorePassageLoss = 62713.5660789 Pa `

¢` MainBore = 1.425 m `

¢` HotPipeLength = 15.7511386413 m `

¢` ColdPipeLength = 16.1836450698 m `

¢` HotBends = 3 `

¢` ColdBends = 4 `

¢` NozzleBore = 1.33 m `

¢` HotNozzleLength = 1.772 m `

¢` ColdNozzleLength = 2.75363966835 m `

¢` DownOuterRadius = 3.2 m `

¢` DownInnerRadius = 2.2 m `

¢` DownLength = 3.355 m `

¢` SGEndK = 1.5 `

¢` BendK = 0.3 `

¢` CollectorK = 1 `

¢` ReactorEntryK = 1 `

¢` ReactorExitK = 0.5 `

¢` ValveK = 0.2 `

¢` BulkTurnK = 2 `

¢` PumpEfficiency = 0.8 `

¢` MotorEfficiency = 0.96 `

¢` Gravity = 9.80665 m/s2 `

¢` function Darcy(rey, relative)
    if rey < 4000 throw "Turbulent model requires Re above 4000"
    x = 8
    for i in 1:30
        x = -2 * ln(relative / 3.7 + 2.51 * x / rey) / ln(10)
    end
    return 1 / x^2
end `

## Properties and flow

¢??` MeanTemperature = (HotTemperature + ColdTemperature) / 2 = 〔850〕 K `

¢??` MeanDensity = DensityIntercept - DensitySlope * MeanTemperature =
〔1,633.783〕 kg/m3 `

¢??` HotDensity = DensityIntercept - DensitySlope * HotTemperature = 〔1,611.241〕
kg/m3 `

¢??` ColdDensity = DensityIntercept - DensitySlope * ColdTemperature =
〔1,656.324〕 kg/m3 `

¢??` MeanViscosity = ViscosityScale * exp(ViscosityTemperature /
MeanTemperature) = 〔0.002912508〕 Pa.s `

¢??` HotViscosity = ViscosityScale * exp(ViscosityTemperature / HotTemperature)
= 〔0.002732857〕 Pa.s `

¢??` ColdViscosity = ViscosityScale * exp(ViscosityTemperature /
ColdTemperature) = 〔0.003123548〕 Pa.s `

¢??` LegMassFlow = TotalMassFlow / Legs = 〔6,166.667〕 kg/s `

¢??` PumpVolumeFlow = LegMassFlow / ColdDensity = 〔3.723103〕 m3/s `

¢??` SGVelocity = LegMassFlow / (MeanDensity * SGTubeCount * pi * SGTubeBore^2
/ 4) = 〔2.028075〕 m/s `

¢??` SGReynolds = MeanDensity * SGVelocity * SGTubeBore / MeanViscosity =
〔15,927.19〕 `

¢??` SGFactor = Darcy(SGReynolds, TubeRoughness / SGTubeBore) = 〔0.02752744〕 `

¢??` SGDynamic = MeanDensity * SGVelocity^2 / 2 = 〔3.359945〕 kPa `

¢??` SGFriction = SGFactor * SGTubeLength / SGTubeBore * SGDynamic = 〔131.3302〕 kPa `

¢??` SGEnds = SGEndK * SGDynamic = 〔5.039918〕 kPa `

## Main piping and connections

¢??` HotVelocity = LegMassFlow / (HotDensity * pi * MainBore^2 / 4) = 〔2.399775〕 m/s `

¢??` HotDynamic = HotDensity * HotVelocity^2 / 2 = 〔4.639502〕 kPa `

¢??` HotFactor = Darcy(HotDensity * HotVelocity * MainBore / HotViscosity,
PipeRoughness / MainBore) = 〔0.01041103〕 `

¢??` HotStraight = HotFactor * HotPipeLength / MainBore * HotDynamic =
〔0.5339027〕 kPa `

¢??` HotNozzleVelocity = LegMassFlow / (HotDensity * pi * NozzleBore^2 / 4) =
〔2.754844〕 m/s `

¢??` HotNozzleDynamic = HotDensity * HotNozzleVelocity^2 / 2 = 〔6.113983〕 kPa `

¢??` HotNozzleFactor = Darcy(HotDensity * HotNozzleVelocity * NozzleBore /
HotViscosity, PipeRoughness / NozzleBore) = 〔0.01030215〕 `

¢??` HotNozzleFriction = HotNozzleFactor * HotNozzleLength / NozzleBore *
HotNozzleDynamic = 〔0.08391979〕 kPa `

¢??` ColdVelocity = LegMassFlow / (ColdDensity * pi * MainBore^2 / 4) =
〔2.334455〕 m/s `

¢??` ColdDynamic = ColdDensity * ColdVelocity^2 / 2 = 〔4.513218〕 kPa `

¢??` ColdFactor = Darcy(ColdDensity * ColdVelocity * MainBore / ColdViscosity,
PipeRoughness / MainBore) = 〔0.01063507〕 `

¢??` ColdStraight = ColdFactor * ColdPipeLength / MainBore * ColdDynamic =
〔0.545115〕 kPa `

¢??` ColdNozzleVelocity = LegMassFlow / (ColdDensity * pi * NozzleBore^2 / 4) =
〔2.679859〕 m/s `

¢??` ColdNozzleDynamic = ColdDensity * ColdNozzleVelocity^2 / 2 = 〔5.947565〕 kPa `

¢??` ColdNozzleFactor = Darcy(ColdDensity * ColdNozzleVelocity * NozzleBore /
ColdViscosity, PipeRoughness / NozzleBore) = 〔0.01052194〕 `

¢??` ColdNozzleFriction = ColdNozzleFactor * ColdNozzleLength / NozzleBore *
ColdNozzleDynamic = 〔0.1295658〕 kPa `

¢??` StraightLoss = HotStraight + ColdStraight + HotNozzleFriction +
ColdNozzleFriction = 〔1.292503〕 kPa `

¢??` BendLoss = BendK * (HotBends * HotDynamic + ColdBends * ColdDynamic) =
〔9.591413〕 kPa `

¢??` CollectorLoss = CollectorK * (HotDynamic + ColdDynamic) = 〔9.15272〕 kPa `

¢??` ReactorNozzleLoss = ReactorEntryK * ColdNozzleDynamic + ReactorExitK *
HotNozzleDynamic = 〔9.004557〕 kPa `

¢??` ValveLoss = ValveK * (HotDynamic + ColdDynamic) = 〔1.830544〕 kPa `

## Bulk reactor passage and total duty

¢??` DownArea = pi * (DownOuterRadius^2 - DownInnerRadius^2) = 〔16.9646〕 m2 `

¢??` DownDiameter = 2 * (DownOuterRadius - DownInnerRadius) = 〔2〕 m `

¢??` DownVelocity = TotalMassFlow / (ColdDensity * DownArea) = 〔0.6583892〕 m/s `

¢??` DownDynamic = ColdDensity * DownVelocity^2 / 2 = 〔0.3589887〕 kPa `

¢??` DownFactor = Darcy(ColdDensity * DownVelocity * DownDiameter /
ColdViscosity, PipeRoughness / DownDiameter) = 〔0.01241365〕 `

¢??` DownFriction = DownFactor * DownLength / DownDiameter * DownDynamic =
〔0.007475544〕 kPa `

¢??` BulkTurnLoss = BulkTurnK * DownDynamic = 〔0.7179774〕 kPa `

¢??` KnownGeometryLoss = SGFriction + CorePassageLoss + StraightLoss +
DownFriction = 〔195.3438〕 kPa `

¢??` LocalLoss = SGEnds + BendLoss + CollectorLoss + ReactorNozzleLoss +
ValveLoss + BulkTurnLoss = 〔35.33713〕 kPa `

¢??` PumpRise = KnownGeometryLoss + LocalLoss = 〔230.6809〕 kPa `

¢??` PumpHead = PumpRise / (ColdDensity * Gravity) = 〔14.20187〕 m `

¢??` HydraulicPerPump = PumpRise * PumpVolumeFlow = 〔858.8488〕 kW `

¢??` ShaftPerPump = HydraulicPerPump / PumpEfficiency = 〔1,073.561〕 kW `

¢??` ElectricalPerPump = ShaftPerPump / MotorEfficiency = 〔1,118.293〕 kW `

¢??` TotalHydraulic = Legs * HydraulicPerPump = 〔2.576546〕 MW `

¢??` TotalShaft = Legs * ShaftPerPump = 〔3.220683〕 MW `

¢??` TotalElectrical = Legs * ElectricalPerPump = 〔3.354878〕 MW `

¢??` BareSubtotalElectrical = Legs * KnownGeometryLoss * PumpVolumeFlow /
(PumpEfficiency * MotorEfficiency) = 〔2.840957〕 MW `

KnownGeometryLoss is a subtotal, not a validated lower bound: it includes the
already-provisional core end allowance. LocalLoss adds only the additional
listed items. PumpHead is differential head, not system operating/design
pressure. Shaft power is motor mechanical output; electrical power is supply
input. Motor nameplate margin, starting duty and supplier selection are not
determined here.

## Local-loss sensitivity

Use these deliberately broad coefficient cases for uncertainty in unselected
fittings. They are not statistical confidence bounds. Both retain baseline core
loss, SG length/roughness and efficiencies. Low/high: SG tube ends 1/2; bend K
0.15/0.6; each collector 0.5/2; reactor cold entry 0.5/2 and hot exit 0.25/1;
each open valve 0.05/1; bulk turn 1/5.

¢??` LowLocalLoss = SGDynamic + 0.15 * (HotBends * HotDynamic + ColdBends *
ColdDynamic) + 0.5 * (HotDynamic + ColdDynamic) + 0.5 * ColdNozzleDynamic +
0.25 * HotNozzleDynamic + 0.05 * (HotDynamic + ColdDynamic) + DownDynamic =
〔18.05091〕 kPa `

¢??` HighLocalLoss = 2 * SGDynamic + 0.6 * (HotBends * HotDynamic + ColdBends *
ColdDynamic) + 2 * (HotDynamic + ColdDynamic) + 2 * ColdNozzleDynamic +
HotNozzleDynamic + HotDynamic + ColdDynamic + 5 * DownDynamic = 〔73.16493〕 kPa `

¢??` LowRise = KnownGeometryLoss + LowLocalLoss = 〔213.3947〕 kPa `

¢??` LowElectrical = Legs * LowRise * PumpVolumeFlow / (PumpEfficiency *
MotorEfficiency) = 〔3.103478〕 MW `

¢??` HighRise = KnownGeometryLoss + HighLocalLoss = 〔268.5087〕 kPa `

¢??` HighElectrical = Legs * HighRise * PumpVolumeFlow / (PumpEfficiency *
MotorEfficiency) = 〔3.905022〕 MW `

## Comparison with the earlier allowance

¢??` SameFlowOldMethod = 1.5 * SGFriction = 〔196.9954〕 kPa `

¢??` SameFlowOldElectrical = Legs * SameFlowOldMethod * PumpVolumeFlow /
(PumpEfficiency * MotorEfficiency) = 〔2.864977〕 MW `

The old sheet's 5.166 MW total electrical estimate also used the larger 22,699
kg/s total flow. Separate that operating-basis change from replacing the 50%
allowance: at the same new flow, SG friction × 1.5 is actually below the
itemized working estimate. No blanket percentage has been added to the new
total.

## Sources, checks and remaining work

*   Owner-selected UM case and [core loss][1], D-060. Core loss is imported
    explicitly and must be recalculated if flow, tube count/bore or temperature
    changes.
*   [Original SG sizing][2]: tube count/length retained; hydraulics recalculated
    here. Its thermal calculation is not rerun.
*   Current resolved geometry from `fastSaltModels/models/coolant_assembly.py` and
    `wistr_installation.py`; isolated nozzle bore remains a provisional 1.33 m
    (1.4 m OD less 35 mm walls), differing from the installation's 1.425 m main
    bore. Transition details are included only in provisional local terms.
*   [NASA KSC-STD-Z-0017 Rev A][3], §§7.4–8.1: Colebrook/Darcy methods, accounting
    for fitting losses, and representative clean stainless roughness. Local
    coefficients chosen here are engineering assumptions, not values certified
    by that standard for this plant.

The calculation is suitable for a preliminary power budget. Detailed SG
collectors, valve selection, actual bends, restrictions, bypass/flow balance,
pump efficiency/curve/NPSH, off-normal states and variable-density network
closure remain unresolved. No motor downsizing, Blender change,
pressure-protection design or SG failure assessment is made. D-061 adopts this
preliminary duty into the shared graphics/P&ID model; existing 2 MW motor
reservations and geometric envelopes are retained.

Run `python calculations/steam-generator/coolant_pump_itemized.py`, then `node
calculations/steam-generator/check_coolant_pump_itemized.cjs` with the project
HURMET_ENGINE/TEMML_ENGINE bundles. Inputs, source hashes, routes and external
roughness/efficiency sensitivities are saved in
`coolant-pump-itemized-results.json`; Hurmet results are verified independently
in SI arithmetic. Generated HTML is ignored output.

[1]: ../reactor/Core%20coolant%20pressure%20loss%20-%20Hurmet.md

[2]: Generator%20sizing%20-%20Hurmet.md

[3]: https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017\\\_RevA\\\_Final.pdf

[4]: https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017\_RevA\_Final.pdf
