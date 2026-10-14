---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Normal coolant pressure profile

Preliminary steady-flow screen, 14 October 2026. One representative leg of the
three-leg coolant loop. All pressures below are **gauge**, unless stated
otherwise. Owner basis: approximately 1 bar(g) at the SG tops; tank normally
nearly empty; P-401 sets accumulator levels by transferring inventory.
Steam-generator failure assessment is explicitly deferred and excluded.

The calculation uses the existing pump/SG loss estimates and current visual
elevations. It does not select pressure ratings, relief settings or pump
suction requirements. The extra 50% loop loss has not been assigned to
individual components, so this sheet gives **correlated allocation bounds**,
not a predicted operating curve or statistical uncertainty interval.

## Inputs and reference location

The SG-top pressure reference is provisionally at casing-top elevation, 17 m
above the floor. The actual accumulator salt level and gas-tap elevation are
not modeled yet. A 1 m reference-level change shifts all calculated pressures
by about 0.16 bar at fixed gas pressure. All imported component elevations are
layout inputs, not surveyed hydraulic data.

The common representative density is the pump worksheet's mean-temperature
value. Its SG loss is friction only; hydrostatic pressure gain is added
separately. The inherited 19.879 m tube calculation is retained despite the 17
m visual casing.

¢` format = "h7" `

¢` TopPressure = 1 bar `

¢` Density = 1637.93125 kg/m3 `

¢` Gravity = 9.80665 m/s2 `

¢` SGLoss = 190.872791 kPa `

¢` PumpFactor = 1.5 `

¢` MassFlow = 7566.47718 kg/s `

¢` MainBore = 1.425 m `

¢` TopZ = 17 m `

¢` SGInZ = 15.5 m `

¢` SGOutZ = 1.9 m `

¢` SuctionZ = 3.61 m `

¢` DischargeZ = 4.51 m `

¢` ReactorInZ = 4.51 m `

¢` BottomZ = 1.155 m `

¢` ReactorOutZ = 6.28 m `

## Pressure balance

Use p₂ = p₁ + ρg(z₁ − z₂) + Δp_pump − Δp_loss. This first screen neglects
changes in velocity head and assumes uniform representative density. Total
closed-loop hydrostatic head cancels under that assumption: do not add the full
SG height to pump duty.

¢??` Gradient = Density * Gravity = 〔0.1606262〕 'bar/m' `

¢??` PumpRise = PumpFactor * SGLoss = 〔2.863092〕 bar `

¢??` OtherLoss = PumpRise - SGLoss = 〔0.954364〕 bar `

¢??` VolumeFlow = MassFlow / Density = 〔4.619533〕 m3/s `

¢??` PipeVelocity = 4 * VolumeFlow / (pi * MainBore^2) = 〔2.896533〕 m/s `

¢??` PipeDynamicPressure = Density * PipeVelocity^2 / 2 = 〔0.06871041〕 bar `

¢??` SGGravityGain = Density * Gravity * (SGInZ - SGOutZ) = 〔2.184516〕 bar `

¢??` SGNetPressureGain = SGGravityGain - SGLoss = 〔0.2757882〕 bar `

The velocity-pressure scale is only for the main bore; it does not bound local
tube/manifold effects. The pressure datum is related hydrostatically to the hot
inlet with negligible intervening loss. That connection and the actual
gas-vessel salt level need confirmation.

## SG and pump pressures

No extra loss is assigned inside the SG beyond SGLoss. Between SG outlet and
pump suction the unknown loss can range from zero to the entire OtherLoss
budget. Pump inlet/outlet elevations differ by 0.90 m; that elevation rise is
included when relating their pressures.

¢??` SGInPressure = TopPressure + Density * Gravity * (TopZ - SGInZ) =
〔1.240939〕 bar `

¢??` SGOutPressure = SGInPressure + SGGravityGain - SGLoss = 〔1.516727〕 bar `

¢??` SuctionHigh = SGOutPressure + Density * Gravity * (SGOutZ - SuctionZ) =
〔1.242057〕 bar `

¢??` SuctionLow = SuctionHigh - OtherLoss = 〔0.2876928〕 bar `

¢??` DischargeLow = SuctionLow + PumpRise + Density * Gravity * (SuctionZ -
DischargeZ) = 〔3.006221〕 bar `

¢??` DischargeHigh = SuctionHigh + PumpRise + Density * Gravity * (SuctionZ -
DischargeZ) = 〔3.960585〕 bar `

## Reactor pressures

Downstream of the pump, pressure equals the hydrostatic reference plus losses
still remaining before the SG inlet. Without allocating OtherLoss, the
remaining loss can range from zero to the entire budget. BottomZ is the
bottom-plenum mid-height; it is not the lowest wall location or a maximum
design pressure. Internal hydraulic losses are included only through the
inherited aggregate allowance.

¢??` ReactorInLow = TopPressure + Density * Gravity * (TopZ - ReactorInZ) =
〔3.006221〕 bar `

¢??` ReactorInHigh = ReactorInLow + OtherLoss = 〔3.960585〕 bar `

¢??` BottomLow = TopPressure + Density * Gravity * (TopZ - BottomZ) = 〔3.545122〕 bar `

¢??` BottomHigh = BottomLow + OtherLoss = 〔4.499486〕 bar `

¢??` ReactorOutLow = TopPressure + Density * Gravity * (TopZ - ReactorOutZ) =
〔2.721913〕 bar `

¢??` ReactorOutHigh = ReactorOutLow + OtherLoss = 〔3.676277〕 bar `

## Pumps stopped: isothermal hydrostatic reference

These values assume a filled, equilibrated circuit at uniform Density, unchanged
reference level and gas pressure. They do not model natural circulation or the
transition after stopping a pump.

¢??` StaticSGOut = TopPressure + Density * Gravity * (TopZ - SGOutZ) =
〔3.425455〕 bar `

¢??` StaticSuction = TopPressure + Density * Gravity * (TopZ - SuctionZ) =
〔3.150785〕 bar `

¢??` StaticReactorIn = TopPressure + Density * Gravity * (TopZ - ReactorInZ) =
〔3.006221〕 bar `

¢??` StaticBottom = TopPressure + Density * Gravity * (TopZ - BottomZ) =
〔3.545122〕 bar `

¢??` StaticReactorOut = TopPressure + Density * Gravity * (TopZ - ReactorOutZ) =
〔2.721913〕 bar `

## Lower gas-pressure sensitivity

Use 0.5 bar(g) as a comparison only, not an adopted target. Every pressure
shifts downward by the same 0.5 bar in this fixed-density/fixed-duty screen.
Negative gauge pressure is not itself a cavitation criterion: vapor pressure,
local velocities, gas release and vendor NPSH requirements remain necessary.

¢` LowerTopPressure = 0.5 bar `

¢??` LowerBiasSuctionLow = SuctionLow + LowerTopPressure - TopPressure =
〔-0.2123072〕 bar `

¢??` LowerBiasSuctionHigh = SuctionHigh + LowerTopPressure - TopPressure =
〔0.7420567〕 bar `

## Limits and next work

*   Bounds preserve the total loss budget. Maxima/minima at different stations are
    correlated and cannot be chosen independently. They are not an allowance
    for arbitrary larger actual losses. The inherited pump pressure rise is
    treated as the duty requirement, not a measured pump curve.
*   Uniform density suppresses thermosiphon head. The inherited density correlation
    gives approximately 1620–1656 kg/m³ across 875–810 K. The checker repeats
    the screen at those two uniform densities; it does not model their spatial
    distribution.
*   All legs have matching modeled elevations; equal flow/loss is assumed. No flow
    redistribution or one-pump-out case is calculated.
*   TK-401 is isolated between transfers and does not inherit the SG gas pressure
    automatically. Its pressure and transfer differential are separate
    unresolved operating inputs. The selected larger tank's location remains
    deferred.
*   No pressure rating, relief hardware/setpoint, blocked-pump case, gas-regulator
    failure, transient or SG failure is assessed here. Next resolve
    SG/accumulator hydraulic level, suction-line loss and allocation of
    reactor/piping losses before reducing the gas bias or selecting pump
    suction margins.

## Sources and reproduction

*   Owner pressure clarification and D-059;
    `design/pids/coolant-system/coolant-system.toml`.
*   [Coolant pump estimate][1], [generator sizing][2], and shared
    `design/engineering/coolant-system.toml`.
*   Current `fastSaltModels` assembly ports and verified reactor report; hashes and
    imported values in `coolant-pressure-results.json`.
*   [DOE Fluid Flow handbook][3]: extended Bernoulli balance between pressure,
    elevation, pump energy and friction. This general method does not qualify
    the reactor design.

Run `python coolant_pressure_profile.py`, then `node check_coolant_pressure.cjs`
with HURMET_ENGINE and TEMML_ENGINE pointing to the existing Hurmet bundles.
Python evaluates the balance independently; Hurmet recalculates and reopens the
worksheet, checks all numerical outputs and reference-pressure/density
sensitivities. No Blender generation is needed.

[1]: ../steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md

[2]: ../steam-generator/Generator%20sizing%20-%20Hurmet.md

[3]: https://www.energy.gov/ehss/articles/doe-hdbk-10123-92
