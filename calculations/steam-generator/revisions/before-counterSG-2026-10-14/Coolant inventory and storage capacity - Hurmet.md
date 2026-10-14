---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Coolant inventory, expansion and TK-401 capacity

14 October 2026. Preliminary volume and mass balance for the current three-leg
installation. **TK-401 is an expansion-storage concept and a proposed
full-drain receiver; those are different capacity requirements.** The 4 m
diameter × 8 m bare tank in Blender is an external visual envelope, not a
specified internal capacity.

The worksheet retains the existing generator salt-property correlation and
810/875 K coolant temperatures. No tank or building is resized. Editable
allowances are identified below. Open this Markdown file in Hurmet to
recalculate; saved answers are not a certified inventory or an operating
instruction.

¢` format = "h7" `

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

The UM report's Appendix B, Table 58, supplies **3.86 m² coolant flow area** as
a provisional reactor channel-area reference. Here it is extended through the
current 3.4 m core and 0.30/0.25 m reflectors. Report dimensions/conditions do
not all match the current layout; that area needs confirmation. Do not count
the fuel volume as coolant. The coarse Blender hole pattern is illustrative and
is not used as the engineering tube count.

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

¢` CoreFlowArea = 3.86 m2 `

¢??` BottomVolume = pi * LowerRadius^2 * BottomHeight = 〔24.12743〕 m3 `

¢??` DownVolume = pi * (LowerRadius^2 - ReflectorRadius^2) * DownHeight =
〔66.33159〕 m3 `

¢??` HotVolume = pi * HotRadius^2 * HotHeight = 〔73.79708〕 m3 `

¢??` ChannelVolume = CoreFlowArea * (CoreHeight + LowerReflector +
UpperReflector) = 〔15.247〕 m3 `

¢??` ReactorVolume = BottomVolume + DownVolume + HotVolume + ChannelVolume =
〔179.5031〕 m3 `

### Steam generators

The existing generator worksheet calculates **12,090 salt tubes per generator**,
14 mm bore and 19.879 m tube length. Only the salt tubes are counted; the
water/steam tubes are excluded. The current 17 m graphic casing height is not a
validated replacement for tube length. Both lengths are tested below; MSU's
eventual internal design should replace this basis.

¢` SGTubeCount = 12090 `

¢` SGTubeBore = 0.014 m `

¢` SGTubeLength = 19.8790057 m `

¢` SGShortLength = 17 m `

¢??` SGVolumeEach = SGTubeCount * pi * SGTubeBore^2 * SGTubeLength / 4 =
〔36.99703〕 m3 `

¢??` SGVolume = Legs * SGVolumeEach = 〔110.9911〕 m3 `

¢??` SGShortVolume = Legs * SGTubeCount * pi * SGTubeBore^2 * SGShortLength / 4
= 〔94.91666〕 m3 `

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

¢??` HotPipeVolume = pi * MainBore^2 * HotLength / 4 = 〔75.36207〕 m3 `

¢??` ColdPipeVolume = pi * MainBore^2 * ColdLength / 4 = 〔77.43142〕 m3 `

¢??` HotNozzleVolume = Legs * pi * NozzleBore^2 * HotNozzleLength / 4 =
〔7.38547〕 m3 `

¢??` ColdNozzleVolume = Legs * pi * NozzleBore^2 * ColdNozzleLength / 4 =
〔11.47682〕 m3 `

¢??` PolylineVolume = pi * MainBore^2 * PolylineLength / 4 = 〔171.6521〕 m3 `

¢??` BendVolumeDifference = PolylineVolume - HotPipeVolume - ColdPipeVolume =
〔18.85861〕 m3 `

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

¢??` CollectorBore = CollectorOD - 2 * CollectorWall = 〔2.05〕 m `

¢??` CollectorVolumeEach = pi * CollectorBore^2 * CollectorLength / 8 =
〔4.62089〕 m3 `

¢??` CollectorVolume = 2 * Legs * CollectorVolumeEach = 〔27.72534〕 m3 `

¢??` PumpEnvelopeVolume = Legs * pi * PumpDiameter^2 * PumpHeight / 4 =
〔33.25062〕 m3 `

¢??` PumpVolume = PumpEnvelopeVolume * PumpVoidFraction = 〔16.62531〕 m3 `

¢??` LoopVolume = ReactorVolume + SGVolume + HotPipeVolume + ColdPipeVolume +
HotNozzleVolume + ColdNozzleVolume + CollectorVolume + PumpVolume +
ServiceVolume = 〔508.5006〕 m3 `

## Temperature cases and fixed-mass balance

Use an editable **450°C (723.15 K) cold-fill/storage case**. It is above the
inherited 674 K liquidus, but is not a selected operating minimum or a verified
property-correlation validity limit. The existing density correlation is ρ =
2112.68 − 0.5635 T, with T in kelvin; coefficients are retained from Generator
sizing. UM Table 43 gives nearly identical rounded coefficients, 2112.8 −
0.56355 T.

For the normal circuit, hot plenum/legs/nozzles/collectors use 875 K; bottom
plenum/downcomer/cold legs/nozzles/collectors/pumps/service allowance use 810
K; core/reflector channels and SG tubes use their mean 842.5 K. Temperature
profiles are screening approximations.

Hold **the total charge fixed** at the mass required to fill the loop at the
cold-fill temperature. At normal operation the loop contains less mass;
transfer the difference to storage. An all-hot 875 K loop bounds this modeled
thermal case. Full drain includes that already-transferred expansion salt
exactly once. Fixed geometric volumes neglect thermal expansion of the metal.

¢` FillTemperature = 723.15 K `

¢` StoreTemperature = 723.15 K `

¢` HotTemperature = 875 K `

¢` ColdTemperature = 810 K `

¢` DensityIntercept = 2112.68 'kg/m3' `

¢` DensitySlope = 0.5635 'kg.m-3.K-1' `

¢??` MeanTemperature = (HotTemperature + ColdTemperature) / 2 = 〔842.5〕 K `

¢??` FillDensity = DensityIntercept - DensitySlope * FillTemperature =
〔1,705.185〕 'kg/m3' `

¢??` StoreDensity = DensityIntercept - DensitySlope * StoreTemperature =
〔1,705.185〕 'kg/m3' `

¢??` HotDensity = DensityIntercept - DensitySlope * HotTemperature = 〔1,619.618〕
'kg/m3' `

¢??` ColdDensity = DensityIntercept - DensitySlope * ColdTemperature =
〔1,656.245〕 'kg/m3' `

¢??` MeanDensity = DensityIntercept - DensitySlope * MeanTemperature =
〔1,637.931〕 'kg/m3' `

¢??` HotGroup = HotVolume + HotPipeVolume + HotNozzleVolume + Legs *
CollectorVolumeEach = 〔170.4073〕 m3 `

¢??` ColdGroup = BottomVolume + DownVolume + ColdPipeVolume + ColdNozzleVolume +
Legs * CollectorVolumeEach + PumpVolume + ServiceVolume = 〔211.8552〕 m3 `

¢??` MeanGroup = ChannelVolume + SGVolume = 〔126.2381〕 m3 `

¢??` VolumeClosure = LoopVolume - HotGroup - ColdGroup - MeanGroup = 〔0〕 m3 `

¢??` ChargeMass = LoopVolume * FillDensity = 〔867,087.6〕 kg `

¢??` NormalLoopMass = HotGroup * HotDensity + ColdGroup * ColdDensity +
MeanGroup * MeanDensity = 〔833,648.1〕 kg `

¢??` NormalExpansionMass = ChargeMass - NormalLoopMass = 〔33,439.49〕 kg `

¢??` NormalExpansionVolume = NormalExpansionMass / StoreDensity = 〔19.61048〕 m3 `

¢??` AllHotExpansionMass = ChargeMass - LoopVolume * HotDensity = 〔43,511.11〕 kg `

¢??` AllHotExpansionVolume = AllHotExpansionMass / StoreDensity = 〔25.51695〕 m3 `

¢??` NormalMassClosure = NormalLoopMass + NormalExpansionMass - ChargeMass = 〔0〕 kg `

¢??` NormalDrainVolume = NormalLoopMass / StoreDensity = 〔488.8901〕 m3 `

¢??` FullDrainStore = ChargeMass / StoreDensity = 〔508.5006〕 m3 `

¢??` FullDrainHot = ChargeMass / HotDensity = 〔535.3657〕 m3 `

¢??` DrainClosure = FullDrainStore - NormalDrainVolume - NormalExpansionVolume =
〔0〕 m3 `

`NormalDrainVolume` is the space for the circulating inventory after it reaches
the assumed storage temperature; `FullDrainStore` also includes the expansion
salt already there. `FullDrainHot` assumes the entire charge is at 875 K, an
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

¢??` TankID = TankOD - 2 * TankWall = 〔3.95〕 m `

¢??` TankClearHeight = TankHeight - TankEndAllowance = 〔7.9〕 m `

¢??` TankGrossEnvelope = pi * TankOD^2 * TankHeight / 4 = 〔100.531〕 m3 `

¢??` TankInternal = pi * TankID^2 * TankClearHeight / 4 = 〔96.80798〕 m3 `

¢??` Freeboard = TankInternal * FreeboardFraction = 〔19.3616〕 m3 `

¢??` Heel = TankInternal * HeelFraction = 〔4.840399〕 m3 `

¢??` TankWorking = TankInternal * (1 - FreeboardFraction - HeelFraction) =
〔72.60599〕 m3 `

¢??` ExpansionMargin = TankWorking - AllHotExpansionVolume = 〔47.08904〕 m3 `

¢??` NormalExpansionRise = NormalExpansionVolume / (pi * TankID^2 / 4) =
〔1.60031〕 m `

¢??` FullDrainDeficit = FullDrainHot - TankWorking = 〔462.7597〕 m3 `

¢??` FullDrainRatio = FullDrainHot / TankWorking = 〔7.373575〕 `

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

¢??` RequiredWorking = FullDrainHot * (1 + InventoryMargin) = 〔588.9023〕 m3 `

¢??` RequiredInternal = RequiredWorking / (1 - FreeboardFraction - HeelFraction)
= 〔785.203〕 m3 `

¢??` EquivalentID = sqrt(4 * RequiredInternal / (pi * TankClearHeight)) =
〔11.24948〕 m `

¢??` EquivalentOD = EquivalentID + 2 * TankWall = 〔11.29948〕 m `

¢??` EquivalentCurrentTanks = RequiredWorking / TankWorking = 〔8.110932〕 `

## Sensitivity and checks

¢??` ShortTubeLoop = LoopVolume - SGVolume + SGShortVolume = 〔492.4262〕 m3 `

¢??` ZeroPumpLoop = LoopVolume - PumpVolume = 〔491.8753〕 m3 `

¢??` FullPumpLoop = LoopVolume - PumpVolume + PumpEnvelopeVolume = 〔525.1259〕 m3 `

¢??` SGOnlyDeficit = SGVolume - TankInternal = 〔14.18312〕 m3 `

¢??` ShortSGOnlyDeficit = SGShortVolume - TankWorking = 〔22.31067〕 m3 `

¢??` TenPercentPlenumDeduction = 0.1 * (BottomVolume + DownVolume + HotVolume) =
〔16.42561〕 m3 `

¢??` ReducedPlenumLoop = LoopVolume - TenPercentPlenumDeduction = 〔492.075〕 m3 `

The shorter SG tube case, pump-cavity extremes and a 10% deduction from gross
plenums/downcomer do not establish design bounds, but reveal the effect of
major provisional inputs. Even the three SG tube inventories alone exceed the
current working tank volume. The full-drain conclusion therefore does not
depend on the uncertain reactor channel count or precise plumbing allowance.

## Sources, differences and reproduction

*   [Generator sizing][1]: salt density, temperatures, tube bore/count and
    calculated length. These inputs are inherited, not newly validated.
*   `fastSaltModels/models/wistr_installation.py`, `models/wistr_reactor.py`,
    `models/coolant_assembly.py`: current placement and dimensions. See
    [assembly workflow][2].
*   UM/NRDSL-25/02, _Core Design Evolution of Wielenga Innovation Salt Tank
    Reactor_, November 15, 2025: Table 43 (printed p.110; PDF p.126), density;
    Table 58 (printed p.139; PDF p.155), 3.86 m² coolant area. [Library record
    W10][3]. Appendix B lists 3.80 m height / 3.40 m diameter, differing from
    the owner's current 3.40 m height / 3.80 m diameter; this sheet retains the
    current owner geometry and uses the reported flow area only as a
    provisional input. Its 890 K outlet is also not adopted here.
*   [NREL publication record][4] confirms the investigated 45.98/38.91/15.11 wt%
    MgCl₂/KCl/NaCl mixture. It does not independently validate the inherited
    density coefficients in this sheet.

The current reactor's coarse 48 mm holes at 85 mm pitch are presentation
geometry, not a replacement for the UM coolant-flow area. No fuel or absorber
inventory is calculated. SG manifolds, pumps, service inventory, internal tank
dimensions and freeboard remain provisional. This sheet does not size pressure
protection or establish drainage gradients, heating/cooling capacity, seismic
support or transfer timing.

Run `python coolant_inventory.py --models /path/to/fastSaltModels`, then run
`check_coolant_inventory.cjs` with `HURMET_ENGINE` and `TEMML_ENGINE` pointing
to matching Hurmet bundles. Python independently calculates the saved numerical
checks; Hurmet recalculates every worksheet equation, saves/reopens it and
exercises temperature/diameter sensitivities. No Blender build is required. If
the generated worksheet's inputs are edited directly, the checker comparisons
to the Python baseline will need a corresponding reviewed update.

[1]: ../steam-generator/Generator%20sizing%20-%20Hurmet.md

[2]: ../../../fastSaltModels/docs/assembly-models.md

[3]: ../../publications/index.md#w10

[4]: https://research-hub.nlr.gov/en/publications/thermophysical-properties-experimentally-tested-for-nacl-kcl-mgcl-2/
