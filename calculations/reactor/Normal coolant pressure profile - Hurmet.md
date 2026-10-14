---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Normal coolant pressure profile

**Itemized revision, 14 October 2026.** Replaces the earlier 50%-allowance
pressure envelope, preserved in
`revisions/pressure-before-itemized-2026-10-14/`. All pressures are gauge.
Reference: **1 bar(g) at the SG tops**, provisionally 17 m above floor.

Use the checked [itemized pump estimate][1]: total flow 18,500 kg/s, three equal
legs, 810–890 K, and the required pump pressure rise shown below in the base
case. D-063 replaces the earlier SG geometry with the counterSG workbook's
4,902 salt tubes, 20 mm bore and 11.920866 m straight hydraulic length. Its
individual loss terms are explicitly imported; this sheet allocates them and
calculates station pressures. D-063 adopts this revised case into the shared
graphics/P&ID records; this calculation continues to import the checked
itemized budget directly.

This remains a mean-density hydraulic-grade screen. Use 1633.7825 kg/m³ (850 K)
for elevation effects, retaining hot/cold properties already used for the
upstream loss calculation. Neglect local velocity-head changes, acceleration
and thermosiphon credit. No pressure rating, relief setting, pump curve or NPSH
qualification is established.

## Loss locations

*   **SG hot connection → SG cold connection:** SG tube friction, tube
    entrance/exit, both collector/distribution allowances.
*   **SG cold connection → pump suction:** Suction share of cold straight-pipe
    friction and two bends.
*   **Pump discharge → reactor cold-nozzle outer connection:** Remaining cold-pipe
    friction, two bends and the cold isolation-valve allowance.
*   **Reactor cold connection → bottom-plenum midpoint:** Cold nozzle
    friction/discharge, downcomer friction and bulk-turn allowance.
*   **Bottom-plenum midpoint → reactor hot-nozzle outer connection:** Core/reflector
    passage with its end losses, hot nozzle entrance and friction.
*   **Reactor hot connection → SG hot connection:** Hot-pipe friction, three bends
    and hot isolation-valve allowance.

The isolation valves are downstream of the pump and in the hot return
respectively, consistent with the draft P&ID. Both SG collector allowances are
grouped across the SG. The top pressure reference is related hydrostatically to
the hot connection; its exact gas tap/free-surface relationship to the
collector remains unresolved. These are schematic allocations, not detailed
internal pressure profiles.

The bottom point is the **bottom-plenum midpoint**, not the lowest vessel wall
or the maximum pressure anywhere. Tube-entry pressures and local nozzle
velocities are not resolved. Core height stays 3.4 m, as corrected by the owner.

## Imported inputs and geometry

Elevations are current visual-layout values. Suction straight loss is split by
route length; bend counts come from the three-leg assembly. Actual accumulator
salt level is not yet modeled, so casing-top height is provisional.

¢` format = "h7" `

¢` TopPressure = 100000 Pa `

¢` Density = 1633.7825 kg/m3 `

¢` Gravity = 9.80665 m/s2 `

¢` TopZ = 17 m `

¢` SGInZ = 15.5 m `

¢` SGOutZ = 1.9 m `

¢` SuctionZ = 3.61 m `

¢` DischargeZ = 4.51 m `

¢` ReactorInZ = 4.51 m `

¢` BottomZ = 1.155 m `

¢` ReactorOutZ = 6.28 m `

¢` SuctionLengthFraction = 0.475820677444 `

¢` SuctionBends = 2 `

¢` ReturnBends = 2 `

¢` HotBends = 3 `

¢` CorePassageLoss = 62713.5660789 Pa `

¢` SGFriction = 70490.644494 Pa `

¢` SGDynamic = 4907.1615146 Pa `

¢` HotDynamic = 4639.50195281 Pa `

¢` ColdDynamic = 4513.21793899 Pa `

¢` HotStraight = 533.902742744 Pa `

¢` ColdStraight = 545.115000895 Pa `

¢` HotNozzleDynamic = 6113.98340173 Pa `

¢` ColdNozzleDynamic = 5947.5650292 Pa `

¢` HotNozzleFriction = 83.9197924731 Pa `

¢` ColdNozzleFriction = 129.565784162 Pa `

¢` DownFriction = 7.47554445387 Pa `

¢` DownDynamic = 358.988693254 Pa `

¢??` Gradient = Density * Gravity = 〔0.1602193〕 'bar/m' `

¢??` SuctionStraight = ColdStraight * SuctionLengthFraction = 〔0.259377〕 kPa `

¢??` ReturnStraight = ColdStraight - SuctionStraight = 〔0.285738〕 kPa `

## Base fitting-loss case

This is the current working profile. The segment losses must sum to the
independently published itemized pump rise.

¢` BaseSGEndK = 1.5 `

¢` BaseBendK = 0.3 `

¢` BaseCollectorK = 1 `

¢` BaseReactorEntryK = 1 `

¢` BaseReactorExitK = 0.5 `

¢` BaseValveK = 0.2 `

¢` BaseBulkK = 2 `

¢??` BaseSGSegment = SGFriction + BaseSGEndK * SGDynamic + BaseCollectorK *
(HotDynamic + ColdDynamic) = 〔87.00411〕 kPa `

¢??` BaseSuctionSegment = SuctionStraight + SuctionBends * BaseBendK *
ColdDynamic = 〔2.967308〕 kPa `

¢??` BaseReturnSegment = ReturnStraight + ReturnBends * BaseBendK *
ColdDynamic + BaseValveK * ColdDynamic = 〔3.896312〕 kPa `

¢??` BaseDownSegment = ColdNozzleFriction + BaseReactorEntryK *
ColdNozzleDynamic + DownFriction + BaseBulkK * DownDynamic = 〔6.802584〕 kPa `

¢??` BaseUpSegment = CorePassageLoss + HotNozzleFriction + BaseReactorExitK *
HotNozzleDynamic = 〔65.85448〕 kPa `

¢??` BaseHotSegment = HotStraight + HotBends * BaseBendK * HotDynamic +
BaseValveK * HotDynamic = 〔5.637355〕 kPa `

¢??` BasePumpRise = BaseSGSegment + BaseSuctionSegment + BaseReturnSegment +
BaseDownSegment + BaseUpSegment + BaseHotSegment = 〔172.1621〕 kPa `

¢??` BaseSGIn = TopPressure + Density * Gravity * (TopZ - SGInZ) = 〔1.240329〕 bar `

¢??` BaseSGOut = BaseSGIn + Density * Gravity * (SGInZ - SGOutZ) - BaseSGSegment
= 〔2.549271〕 bar `

¢??` BaseSuction = BaseSGOut + Density * Gravity * (SGOutZ - SuctionZ) -
BaseSuctionSegment = 〔2.245623〕 bar `

¢??` BaseDischarge = BaseSuction + Density * Gravity * (SuctionZ - DischargeZ) +
BasePumpRise = 〔3.823047〕 bar `

¢??` BaseReactorIn = BaseDischarge + Density * Gravity * (DischargeZ -
ReactorInZ) - BaseReturnSegment = 〔3.784084〕 bar `

¢??` BaseBottom = BaseReactorIn + Density * Gravity * (ReactorInZ - BottomZ) -
BaseDownSegment = 〔4.253594〕 bar `

¢??` BaseReactorOut = BaseBottom + Density * Gravity * (BottomZ - ReactorOutZ) -
BaseUpSegment = 〔2.773925〕 bar `

¢??` BaseReturnToSG = BaseReactorOut + Density * Gravity * (ReactorOutZ -
SGInZ) - BaseHotSegment = 〔1.240329〕 bar `

¢??` BaseClosureError = BaseReturnToSG - BaseSGIn = 〔0〕 Pa `

## Low fitting-loss case

Sensitivity only: change the same local coefficients as the itemized pump
worksheet. Each case has its own required pump head at fixed flow. This is not
operation on one unchanged pump curve or a statistical confidence bound. Core
passage loss and SG friction stay fixed.

¢` LowSGEndK = 1 `

¢` LowBendK = 0.15 `

¢` LowCollectorK = 0.5 `

¢` LowReactorEntryK = 0.5 `

¢` LowReactorExitK = 0.25 `

¢` LowValveK = 0.05 `

¢` LowBulkK = 1 `

¢??` LowSGSegment = SGFriction + LowSGEndK * SGDynamic + LowCollectorK *
(HotDynamic + ColdDynamic) = 〔79.97417〕 kPa `

¢??` LowSuctionSegment = SuctionStraight + SuctionBends * LowBendK * ColdDynamic
= 〔1.613342〕 kPa `

¢??` LowReturnSegment = ReturnStraight + ReturnBends * LowBendK * ColdDynamic +
LowValveK * ColdDynamic = 〔1.865364〕 kPa `

¢??` LowDownSegment = ColdNozzleFriction + LowReactorEntryK *
ColdNozzleDynamic + DownFriction + LowBulkK * DownDynamic = 〔3.469813〕 kPa `

¢??` LowUpSegment = CorePassageLoss + HotNozzleFriction + LowReactorExitK *
HotNozzleDynamic = 〔64.32598〕 kPa `

¢??` LowHotSegment = HotStraight + HotBends * LowBendK * HotDynamic +
LowValveK * HotDynamic = 〔2.853654〕 kPa `

¢??` LowPumpRise = LowSGSegment + LowSuctionSegment + LowReturnSegment +
LowDownSegment + LowUpSegment + LowHotSegment = 〔154.1023〕 kPa `

¢??` LowSGIn = TopPressure + Density * Gravity * (TopZ - SGInZ) = 〔1.240329〕 bar `

¢??` LowSGOut = LowSGIn + Density * Gravity * (SGInZ - SGOutZ) - LowSGSegment =
〔2.61957〕 bar `

¢??` LowSuction = LowSGOut + Density * Gravity * (SGOutZ - SuctionZ) -
LowSuctionSegment = 〔2.329462〕 bar `

¢??` LowDischarge = LowSuction + Density * Gravity * (SuctionZ - DischargeZ) +
LowPumpRise = 〔3.726288〕 bar `

¢??` LowReactorIn = LowDischarge + Density * Gravity * (DischargeZ -
ReactorInZ) - LowReturnSegment = 〔3.707634〕 bar `

¢??` LowBottom = LowReactorIn + Density * Gravity * (ReactorInZ - BottomZ) -
LowDownSegment = 〔4.210472〕 bar `

¢??` LowReactorOut = LowBottom + Density * Gravity * (BottomZ - ReactorOutZ) -
LowUpSegment = 〔2.746088〕 bar `

¢??` LowReturnToSG = LowReactorOut + Density * Gravity * (ReactorOutZ - SGInZ) -
LowHotSegment = 〔1.240329〕 bar `

¢??` LowClosureError = LowReturnToSG - LowSGIn = 〔0〕 Pa `

## High fitting-loss case

Sensitivity only: change the same local coefficients as the itemized pump
worksheet. Each case has its own required pump head at fixed flow. This is not
operation on one unchanged pump curve or a statistical confidence bound. Core
passage loss and SG friction stay fixed.

¢` HighSGEndK = 2 `

¢` HighBendK = 0.6 `

¢` HighCollectorK = 2 `

¢` HighReactorEntryK = 2 `

¢` HighReactorExitK = 1 `

¢` HighValveK = 1 `

¢` HighBulkK = 5 `

¢??` HighSGSegment = SGFriction + HighSGEndK * SGDynamic + HighCollectorK *
(HotDynamic + ColdDynamic) = 〔98.61041〕 kPa `

¢??` HighSuctionSegment = SuctionStraight + SuctionBends * HighBendK *
ColdDynamic = 〔5.675239〕 kPa `

¢??` HighReturnSegment = ReturnStraight + ReturnBends * HighBendK *
ColdDynamic + HighValveK * ColdDynamic = 〔10.21482〕 kPa `

¢??` HighDownSegment = ColdNozzleFriction + HighReactorEntryK *
ColdNozzleDynamic + DownFriction + HighBulkK * DownDynamic = 〔13.82711〕 kPa `

¢??` HighUpSegment = CorePassageLoss + HotNozzleFriction + HighReactorExitK *
HotNozzleDynamic = 〔68.91147〕 kPa `

¢??` HighHotSegment = HotStraight + HotBends * HighBendK * HotDynamic +
HighValveK * HotDynamic = 〔13.52451〕 kPa `

¢??` HighPumpRise = HighSGSegment + HighSuctionSegment + HighReturnSegment +
HighDownSegment + HighUpSegment + HighHotSegment = 〔210.7636〕 kPa `

¢??` HighSGIn = TopPressure + Density * Gravity * (TopZ - SGInZ) = 〔1.240329〕 bar `

¢??` HighSGOut = HighSGIn + Density * Gravity * (SGInZ - SGOutZ) - HighSGSegment
= 〔2.433208〕 bar `

¢??` HighSuction = HighSGOut + Density * Gravity * (SGOutZ - SuctionZ) -
HighSuctionSegment = 〔2.10248〕 bar `

¢??` HighDischarge = HighSuction + Density * Gravity * (SuctionZ - DischargeZ) +
HighPumpRise = 〔4.065919〕 bar `

¢??` HighReactorIn = HighDischarge + Density * Gravity * (DischargeZ -
ReactorInZ) - HighReturnSegment = 〔3.96377〕 bar `

¢??` HighBottom = HighReactorIn + Density * Gravity * (ReactorInZ - BottomZ) -
HighDownSegment = 〔4.363035〕 bar `

¢??` HighReactorOut = HighBottom + Density * Gravity * (BottomZ - ReactorOutZ) -
HighUpSegment = 〔2.852796〕 bar `

¢??` HighReturnToSG = HighReactorOut + Density * Gravity * (ReactorOutZ -
SGInZ) - HighHotSegment = 〔1.240329〕 bar `

¢??` HighClosureError = HighReturnToSG - HighSGIn = 〔0〕 Pa `

## Lower bias comparison and interpretation

Keeping all losses, density and duty fixed, lowering SG-top pressure from 1 to
0.5 bar(g) shifts every station downward by exactly 0.5 bar. This comparison is
not an adopted operating target. The previous broad suction interval came from
allowing all unlocated resistance to sit in the suction line; it is superseded
by the itemized suction resistance here.

¢` LowerTopPressure = 50000 Pa `

¢??` LowerBiasSuction = BaseSuction + LowerTopPressure - TopPressure =
〔1.745623〕 bar `

¢??` LowerBiasBottom = BaseBottom + LowerTopPressure - TopPressure = 〔3.753594〕 bar `

## Limits and verification

*   Mean-density hydrostatics close the base loop exactly with the itemized pump
    rise. A true variable-density network changes the required pump head
    through buoyancy and pressure/energy conversion. This revision does not
    claim that analysis.
*   Main-pipe velocity pressure is roughly 0.045–0.046 bar and nozzle values are
    roughly 0.06 bar. Neglected velocity changes and unresolved
    collector/reference geometry limit interpretation of hundredths of a bar.
*   A 1 m change in the assumed top liquid reference shifts station pressures about
    0.160 bar. Uniform hot/cold density perturbations check hydrostatic
    sensitivity only; they do not recalculate friction or model thermal
    stratification.
*   Low/high fitting cases are correlated. A lower SG resistance raises pump
    suction, while higher downstream resistance raises required discharge
    pressure. They are not independently selectable station limits.
*   TK-401 stays separate while transfer valves are closed; its pressure is not
    assigned the SG reference. Gas-vessel physical level, detailed suction
    conditions, pump curve, piping restrictions and flow maldistribution remain
    unresolved.
*   No SG failure, relief sizing, motor selection, building change or Blender
    regeneration is included. D-063 adopts the revised normal duty and
    station-pressure basis into the shared P&ID/graphics records, with existing
    motor envelopes retained.

Sources: the checked itemized pump results, current assembly ports, D-059
pressure reference and D-060 flow/temperature/height basis. Original source
hashes and loss-budget inputs are retained upstream; this sheet records hashes
of what it imports. General method: [DOE Fluid Flow handbook][2], extended
pressure/elevation/pump/loss balance.

Run `python calculations/reactor/coolant_pressure_profile.py`, then `node
calculations/reactor/check_coolant_pressure.cjs` with the Hurmet bundles
configured. Python checks source hashes, loss-budget closure and each pressure
loop; Hurmet recalculates, saves/reopens and exercises pressure-datum,
elevation and hydrostatic-density sensitivities. The earlier broad-range
calculation is preserved as a historical snapshot, not a parallel active
calculation.

[1]: ../steam-generator/Itemized%20coolant%20pump%20estimate%20-%20Hurmet.md

[2]: https://www.energy.gov/ehss/articles/doe-hdbk-10123-92
