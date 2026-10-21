---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Coolant inventory, expansion and TK-401 capacity

¢` format = "h3" `

14 October 2026. Preliminary volume and mass balance for the current three-leg
installation. **TK-401 is an expansion-storage concept and a proposed
full-drain receiver; those are different capacity requirements.** The 4 m
diameter × 8 m bare tank in Blender is an external visual envelope, not a
specified internal capacity.

D-063 adopts counterSG tube geometry, 810/890 K temperatures and UM density
coefficients consistent with the pump/core calculations. The owner-selected 8.2
× 16 m tank reservation is checked separately from the smaller tank still drawn
in Blender. No tank or building is resized. Editable allowances are identified
below. Open this Markdown file in Hurmet to recalculate; saved answers are not
a certified inventory or an operating instruction.

## Inputs and their provenance

Current reactor and installation geometry is imported from the sibling Python
models, with hashes in `coolant-inventory-results.json`. Route lengths are
computed externally from resolved connections using the current bend-radius and
trim rules; Hurmet computes volume from those lengths. Insulation is excluded
from fluid volume.

### Reactor coolant spaces

Bottom plenum and hot plenum are gross fluid envelopes, without deductions for
supports, links and service hardware. The downcomer excludes the 40 mm
separator thickness and starts above the bottom plenum, avoiding overlap. These
are conservative geometric allowances, not exact net cavities.

Use 24,576 × 14 mm reactor channels, giving **3.78318 m²**, consistently with
the checked core pressure-loss calculation. Extend the area through the current
3.4 m core and 0.30/0.25 m reflectors. The report's tabulated 3.86 m² differs
by about 2%; the active estimate uses count and bore. Do not count the fuel
volume as coolant. The coarse Blender hole pattern is illustrative and is not
used as the engineering tube count.

¢` Legs = 3 `

¢` LowerRadius = 3.2 m `

¢` ReflectorRadius = 2.2 m `

¢` HotRadius = 3.83163966835 m `

¢` BottomHeight = 0.75 m `

¢` DownHeight = 3.91 m `

¢` HotHeight = 1.6 m `

¢` CoreHeight = 3.4 m `

¢` LowerReflector = 0.3 m `

¢` UpperReflector = 0.25 m `

¢` CoreFlowArea = 3.78318127168 m2 `

¢%%` BottomVolume = pi * LowerRadius^2 * BottomHeight = 〔24.1〕 m3 `

¢%%` DownVolume = pi * (LowerRadius^2 - ReflectorRadius^2) * DownHeight = 〔66.3〕 m3 `

¢%%` HotVolume = pi * HotRadius^2 * HotHeight = 〔73.8〕 m3 `

¢%%` ChannelVolume = CoreFlowArea * (CoreHeight + LowerReflector +
UpperReflector) = 〔14.9〕 m3 `

¢%%` ReactorVolume = BottomVolume + DownVolume + HotVolume + ChannelVolume =
〔179〕 m3 `

### Steam generators

The adopted counterSG workbook calculates **4,902 salt tubes per generator**, 20
mm bore and 11.920866 m tube length. Only the salt tubes are counted; the
water/steam tubes are excluded. The current 17 m graphic casing height is not a
validated replacement for tube length. The 17 m full-casing-length alternative
is only a sensitivity; MSU's eventual internal design should replace this basis.

¢` SGTubeCount = 4902 `

¢` SGTubeBore = 0.02 m `

¢` SGTubeLength = 11.9208662442 m `

¢` SGCasingLength = 17 m `

¢%%` SGVolumeEach = SGTubeCount * pi * SGTubeBore^2 * SGTubeLength / 4 = 〔18.4〕 m3 `

¢%%` SGVolume = Legs * SGVolumeEach = 〔55.1〕 m3 `

¢%%` SGCasingVolume = Legs * SGTubeCount * pi * SGTubeBore^2 * SGCasingLength /
4 = 〔78.5〕 m3 `

### Main pipes and vessel nozzles

These are all three legs combined. Rounded lengths run from the vessel nozzle
ends to SG manifold ports and pump casing ports. Separate nozzle lengths cover
the vessel inner wall to those ends; the small CAD overlap inside the vessel is
excluded. Hot/cold pipe bend fillets replace corner chords with arcs. The old
1.33 m nozzle bore and the installation's 1.425 m pipe bore remain a known
interface mismatch.

¢` MainBore = 1.425 m `

¢` HotLength = 47.253415924 m `

¢` ColdLength = 48.5509352093 m `

¢` PolylineLength = 107.629050936 m `

¢` NozzleBore = 1.33 m `

¢` HotNozzleLength = 1.772 m `

¢` ColdNozzleLength = 2.75363966835 m `

¢%%` HotPipeVolume = pi * MainBore^2 * HotLength / 4 = 〔75.4〕 m3 `

¢%%` ColdPipeVolume = pi * MainBore^2 * ColdLength / 4 = 〔77.4〕 m3 `

¢%%` HotNozzleVolume = Legs * pi * NozzleBore^2 * HotNozzleLength / 4 = 〔7.39〕 m3 `

¢%%` ColdNozzleVolume = Legs * pi * NozzleBore^2 * ColdNozzleLength / 4 = 〔11.5〕 m3 `

¢%%` PolylineVolume = pi * MainBore^2 * PolylineLength / 4 = 〔172〕 m3 `

¢%%` BendVolumeDifference = PolylineVolume - HotPipeVolume - ColdPipeVolume =
〔18.9〕 m3 `

### Unresolved equipment allowances

Approximate each of the six salt collectors by a 2.8 m long half cylinder, using
the modeled 2.1 m bare diameter and an **assumed** 25 mm wall. Actual
transitions are not integrated; they are part of inventory uncertainty. Count
three hot and three cold collectors, with no air, steam or feedwater collector
volume.

Pump liquid cavities are unresolved: use **50% of the modeled cylindrical pump
envelopes**, and test 0–100% below. Add **2 m³** for small service lines,
valves and salt held in nominal gas vessels; this is an editable aggregate
allowance, not a selected gas-vessel volume. The modeled transfer line is only
44 mm bore. No additional coolant inside the separate fuel tanks or other
unconnected systems is assumed.

¢` CollectorOD = 2.1 m `

¢` CollectorWall = 0.025 m `

¢` CollectorLength = 2.8 m `

¢` PumpDiameter = 2.8 m `

¢` PumpHeight = 1.8 m `

¢` PumpVoidFraction = 0.5 `

¢` ServiceVolume = 2 m3 `

¢%%` CollectorBore = CollectorOD - 2 * CollectorWall = 〔2.05〕 m `

¢%%` CollectorVolumeEach = pi * CollectorBore^2 * CollectorLength / 8 = 〔4.62〕 m3 `

¢%%` CollectorVolume = 2 * Legs * CollectorVolumeEach = 〔27.7〕 m3 `

¢%%` PumpEnvelopeVolume = Legs * pi * PumpDiameter^2 * PumpHeight / 4 = 〔33.3〕 m3 `

¢%%` PumpVolume = PumpEnvelopeVolume * PumpVoidFraction = 〔16.6〕 m3 `

¢%%` LoopVolume = ReactorVolume + SGVolume + HotPipeVolume + ColdPipeVolume +
HotNozzleVolume + ColdNozzleVolume + CollectorVolume + PumpVolume +
ServiceVolume = 〔452〕 m3 `

## Temperature cases and fixed-mass balance

Use an editable **450°C (723.15 K) cold-fill/storage case**. It is above the
inherited 674 K liquidus, but is not a selected operating minimum or a verified
property-correlation validity limit. The existing density correlation is ρ =
2112.8 − 0.56355 T, with T in kelvin; coefficients follow UM Table 43 and the
current pump/core basis.

For the normal circuit, hot plenum/legs/nozzles/collectors use 890 K; bottom
plenum/downcomer/cold legs/nozzles/collectors/pumps/service allowance use 810
K; core/reflector channels and SG tubes use their mean 850 K. Temperature
profiles are screening approximations.

Hold **the total charge fixed** at the mass required to fill the loop at the
cold-fill temperature. At normal operation the loop contains less mass;
transfer the difference to storage. An all-hot 890 K loop bounds this modeled
thermal case. Full drain includes that already-transferred expansion salt
exactly once. Fixed geometric volumes neglect thermal expansion of the metal.

¢` FillTemperature = 723.15 K `

¢` StoreTemperature = 723.15 K `

¢` HotTemperature = 890 K `

¢` ColdTemperature = 810 K `

¢` DensityIntercept = 2112.8 'kg/m3' `

¢` DensitySlope = 0.56355 'kg.m-3.K-1' `

¢%%` MeanTemperature = (HotTemperature + ColdTemperature) / 2 = 〔850〕 K `

¢%%` FillDensity = DensityIntercept - DensitySlope * FillTemperature = 〔1,705〕
'kg/m3' `

¢%%` StoreDensity = DensityIntercept - DensitySlope * StoreTemperature = 〔1,705〕
'kg/m3' `

¢%%` HotDensity = DensityIntercept - DensitySlope * HotTemperature = 〔1,611〕
'kg/m3' `

¢%%` ColdDensity = DensityIntercept - DensitySlope * ColdTemperature = 〔1,656〕
'kg/m3' `

¢%%` MeanDensity = DensityIntercept - DensitySlope * MeanTemperature = 〔1,634〕
'kg/m3' `

¢%%` HotGroup = HotVolume + HotPipeVolume + HotNozzleVolume + Legs *
CollectorVolumeEach = 〔170〕 m3 `

¢%%` ColdGroup = BottomVolume + DownVolume + ColdPipeVolume + ColdNozzleVolume +
Legs * CollectorVolumeEach + PumpVolume + ServiceVolume = 〔212〕 m3 `

¢%%` MeanGroup = ChannelVolume + SGVolume = 〔70〕 m3 `

¢%%` VolumeClosure = LoopVolume - HotGroup - ColdGroup - MeanGroup = 〔0〕 m3 `

¢%%` ChargeMass = LoopVolume * FillDensity = 〔771,260〕 kg `

¢%%` NormalLoopMass = HotGroup * HotDensity + ColdGroup * ColdDensity +
MeanGroup * MeanDensity = 〔739,863〕 kg `

¢%%` NormalExpansionMass = ChargeMass - NormalLoopMass = 〔31,398〕 kg `

¢%%` NormalExpansionVolume = NormalExpansionMass / StoreDensity = 〔18.4〕 m3 `

¢%%` AllHotExpansionMass = ChargeMass - LoopVolume * HotDensity = 〔42,527〕 kg `

¢%%` AllHotExpansionVolume = AllHotExpansionMass / StoreDensity = 〔24.9〕 m3 `

¢%%` NormalMassClosure = NormalLoopMass + NormalExpansionMass - ChargeMass = 〔0〕 kg `

¢%%` NormalDrainVolume = NormalLoopMass / StoreDensity = 〔434〕 m3 `

¢%%` FullDrainStore = ChargeMass / StoreDensity = 〔452〕 m3 `

¢%%` FullDrainHot = ChargeMass / HotDensity = 〔479〕 m3 `

¢%%` DrainClosure = FullDrainStore - NormalDrainVolume - NormalExpansionVolume =
〔0〕 m3 `

`NormalDrainVolume` is the space for the circulating inventory after it reaches
the assumed storage temperature; `FullDrainStore` also includes the expansion
salt already there. `FullDrainHot` assumes the entire charge is at 890 K, an
inventory reservation rather than a claim that drain mixing reaches that
temperature. Additional purchased inventory or reserve beyond the stated heel
must be added separately.

## Current tank capacity and expansion-only margin

Deduct an assumed 25 mm radial wall and 100 mm total end/internal-height
allowance from the 4 × 8 m bare external envelope. This is not a pressure-wall
calculation. Reserve **20% gas freeboard** and a **5% unavailable heel** as
separate fractions of the internal geometric volume. The heel is a capacity
reservation, not a claim that 5% remains after a gas sweep. No head volume is
credited. Insulation is outside the tank and adds no salt capacity.

¢` TankOD = 4 m `

¢` TankHeight = 8 m `

¢` TankWall = 0.025 m `

¢` TankEndAllowance = 0.1 m `

¢` FreeboardFraction = 0.2 `

¢` HeelFraction = 0.05 `

¢` InventoryMargin = 0.1 `

¢%%` TankID = TankOD - 2 * TankWall = 〔3.95〕 m `

¢%%` TankClearHeight = TankHeight - TankEndAllowance = 〔7.9〕 m `

¢%%` TankGrossEnvelope = pi * TankOD^2 * TankHeight / 4 = 〔101〕 m3 `

¢%%` TankInternal = pi * TankID^2 * TankClearHeight / 4 = 〔96.8〕 m3 `

¢%%` Freeboard = TankInternal * FreeboardFraction = 〔19.4〕 m3 `

¢%%` Heel = TankInternal * HeelFraction = 〔4.84〕 m3 `

¢%%` TankWorking = TankInternal * (1 - FreeboardFraction - HeelFraction) =
〔72.6〕 m3 `

¢%%` ExpansionMargin = TankWorking - AllHotExpansionVolume = 〔47.7〕 m3 `

¢%%` NormalExpansionRise = NormalExpansionVolume / (pi * TankID^2 / 4) = 〔1.5〕 m `

¢%%` FullDrainDeficit = FullDrainHot - TankWorking = 〔406〕 m3 `

¢%%` FullDrainRatio = FullDrainHot / TankWorking = 〔6.59〕 `

Expansion-only margin assumes the tank starts at the reserved heel and has no
other inventory. The full-drain comparison credits no permanently trapped loop
salt: retaining it would not satisfy complete drainage. A final
receiving-temperature transient and total charge definition must be agreed.

## Conditional full-drain storage reservation

Apply a separate **10% inventory uncertainty allowance** to the entire hot drain
charge, then divide by the 75% working fraction. This allowance is not another
thermal-expansion addition. Show an equivalent single cylinder at the existing
8 m external height; it is a space estimate, not an adopted replacement tank.
Multiple tanks or an external store are alternatives to evaluate.

¢%%` RequiredWorking = FullDrainHot * (1 + InventoryMargin) = 〔527〕 m3 `

¢%%` RequiredInternal = RequiredWorking / (1 - FreeboardFraction - HeelFraction)
= 〔702〕 m3 `

¢%%` EquivalentID = sqrt(4 * RequiredInternal / (pi * TankClearHeight)) = 〔10.6〕 m `

¢%%` EquivalentOD = EquivalentID + 2 * TankWall = 〔10.7〕 m `

¢%%` EquivalentCurrentTanks = RequiredWorking / TankWorking = 〔7.25〕 `

## Selected TK-401 reservation — D-058

The 8.2 m diameter × 16 m high bare tank is the adopted planning envelope,
pending relocation. Apply the same provisional wall/end, 20% freeboard and 5%
heel allowances; compare its working acceptance against the hot charge plus 10%
inventory allowance. This does not change the saved Blender tank or qualify
tank construction.

¢` SelectedTankOD = 8.2 m `

¢` SelectedTankHeight = 16 m `

¢%%` SelectedTankInternal = pi * (SelectedTankOD - 2 * TankWall)^2 *
(SelectedTankHeight - TankEndAllowance) / 4 = 〔829〕 m3 `

¢%%` SelectedTankWorking = SelectedTankInternal * (1 - FreeboardFraction -
HeelFraction) = 〔622〕 m3 `

¢%%` SelectedTankMargin = SelectedTankWorking - RequiredWorking = 〔95.6〕 m3 `

## Sensitivity and checks

¢%%` CasingLengthLoop = LoopVolume - SGVolume + SGCasingVolume = 〔476〕 m3 `

¢%%` ZeroPumpLoop = LoopVolume - PumpVolume = 〔436〕 m3 `

¢%%` FullPumpLoop = LoopVolume - PumpVolume + PumpEnvelopeVolume = 〔469〕 m3 `

¢%%` SGOnlyDeficit = SGVolume - TankInternal = 〔-41.7〕 m3 `

¢%%` CasingSGOnlyDeficit = SGCasingVolume - TankWorking = 〔5.93〕 m3 `

¢%%` TenPercentPlenumDeduction = 0.1 * (BottomVolume + DownVolume + HotVolume) =
〔16.4〕 m3 `

¢%%` ReducedPlenumLoop = LoopVolume - TenPercentPlenumDeduction = 〔436〕 m3 `

The full-casing SG tube-length case, pump-cavity extremes and a 10% deduction
from gross plenums/downcomer do not establish design bounds, but reveal the
effect of major provisional inputs. The full circuit exceeds the small tank
still drawn in Blender. The selected larger tank is assessed separately below.

## Sources, differences and reproduction

*   [counterSG workbook][1]: SG tube bore/count and length, independently reproduced
    by counter_sg_basis.py. UM properties and the adopted 810–890 K operating
    case are used here.
*   `fastSaltModels/models/wistr_installation.py`, `models/wistr_reactor.py`,
    `models/coolant_assembly.py`: current placement and dimensions. See
    [assembly workflow][2].
*   UM/NRDSL-25/02, _Core Design Evolution of Wielenga Innovation Salt Tank
    Reactor_, November 15, 2025: Table 43 (printed p.110; PDF p.126), density;
    Table 58 (printed p.139; PDF p.155), 3.86 m² coolant area. [Library record
    W10][3]. Appendix B lists 3.80 m height / 3.40 m diameter, differing from
    the owner's current 3.40 m height / 3.80 m diameter; this sheet retains
    owner geometry and the coolant area calculated from tube count and bore,
    matching the active core loss sheet. The 890 K outlet is adopted.
*   [NREL publication record][4] confirms the investigated 45.98/38.91/15.11 wt%
    MgCl₂/KCl/NaCl mixture. It does not independently validate the inherited
    density coefficients in this sheet.

The current reactor's coarse 48 mm holes at 85 mm pitch are presentation
geometry, not a replacement for the engineering coolant-flow area. No fuel or
absorber inventory is calculated. SG manifolds, pumps, service inventory,
internal tank dimensions and freeboard remain provisional. This sheet does not
size pressure protection or establish drainage gradients, heating/cooling
capacity, seismic support or transfer timing.

Run `python coolant_inventory.py --models /path/to/fastSaltModels`, then run
`check_coolant_inventory.cjs` with `HURMET_ENGINE` and `TEMML_ENGINE` pointing
to matching Hurmet bundles. Python independently calculates the saved numerical
checks; Hurmet recalculates every worksheet equation, saves/reopens it and
exercises temperature/diameter sensitivities. No Blender build is required. If
the generated worksheet's inputs are edited directly, the checker comparisons
to the Python baseline will need a corresponding reviewed update.

[1]: ../steam-generator/sources/counterSG.xlsx

[2]: ../../../fastSaltModels/docs/assembly-models.md

[3]: ../../publications/index.md#w10

[4]: https://research-hub.nlr.gov/en/publications/thermophysical-properties-experimentally-tested-for-nacl-kcl-mgcl-2/
