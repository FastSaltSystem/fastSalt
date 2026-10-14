---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-14
---------------

# Core coolant pressure loss

Preliminary estimate, 14 October 2026. Owner selects the UM report's **18,500
kg/s total core flow**, with coolant at 810–890 K, and confirms **3.4 m active
height**. The appendix's 3.8 m height is a typo, per the owner; it is not an
alternative geometry. Current core diameter remains 3.8 m.

This calculation treats 24,576 identical, open 14 mm-bore tubes in parallel with
equal flow. Pressure losses are the loss across one parallel passage, not that
loss multiplied by tube count. Fuel-side wire spacers are not coolant-bore
obstructions in this model.

## Basis

*   UM report Table 58, printed p.139: tube count, total mass flow, 810/890 K
    temperatures, reported 3.86 m² total area and 2.94 m/s velocity.
*   Tables 25 and 42, printed pp.87 and 109: 14 mm coolant bore, 16 mm tube OD.
    Table 43, p.110: density and viscosity correlations used below, with T in
    kelvin.
*   Owner-confirmed active height 3.4 m; current lower/upper reflectors 0.30/0.25 m.
    A provisional continuous 14 mm bore through both reflectors gives a 3.95 m
    total straight passage. Actual reflector transitions remain to be specified.
*   Roughness 1 micrometre is the inherited SG worksheet's clean-tube assumption,
    not measured core roughness. A 10 micrometre sensitivity is included.
*   Entrance K = 0.5 and exit K = 1.0 are provisional sharp-entry/large-plenum
    allowances. They apply once at the full-passage ends, not at each reflector
    interface. Actual entry shape, exit recovery and any internal restrictions
    remain unresolved.

The main-generator worksheet previously used 22,699 kg/s total and an 875 K
outlet. That earlier operating basis is not used here. Its pump and
system-pressure estimates require reconciliation before this core result is
incorporated into the whole-loop balance.

¢` format = "h7" `

¢` MassFlow = 18500 kg/s `

¢` TubeCount = 24576 `

¢` TubeBore = 0.014 m `

¢` CoreLength = 3.4 m `

¢` BottomReflector = 0.3 m `

¢` TopReflector = 0.25 m `

¢` InletTemperature = 810 K `

¢` OutletTemperature = 890 K `

¢` DensityIntercept = 2112.8 'kg/m3' `

¢` DensitySlope = 0.56355 'kg.m-3.K-1' `

¢` ViscosityScale = 0.0007064 Pa.s `

¢` ViscosityTemperature = 1204.1 K `

¢` Roughness = 1e-06 m `

¢` EntranceK = 0.5 `

¢` ExitK = 1 `

¢` Gravity = 9.80665 m/s2 `

¢` VelocityLimit = 3 m/s `

¢` ReportedArea = 3.86 m2 `

## Mean properties and velocity

Use arithmetic mean bulk temperature for this first estimate. The actual
velocity rises along each heated tube as density falls.

¢??` MeanTemperature = (InletTemperature + OutletTemperature) / 2 = 〔850〕 K `

¢??` Density = DensityIntercept - DensitySlope * MeanTemperature = 〔1,633.783〕
kg/m3 `

¢??` Viscosity = ViscosityScale * exp(ViscosityTemperature / MeanTemperature) =
〔0.002912508〕 Pa.s `

¢??` SingleArea = pi * TubeBore^2 / 4 = 〔0.000153938〕 m2 `

¢??` FlowArea = TubeCount * SingleArea = 〔3.783181〕 m2 `

¢??` VolumeFlow = MassFlow / Density = 〔11.32342〕 m3/s `

¢??` TubeMassFlow = MassFlow / TubeCount = 〔0.7527669〕 kg/s `

¢??` Velocity = VolumeFlow / FlowArea = 〔2.993094〕 m/s `

¢??` InletDensity = DensityIntercept - DensitySlope * InletTemperature =
〔1,656.324〕 kg/m3 `

¢??` OutletDensity = DensityIntercept - DensitySlope * OutletTemperature =
〔1,611.241〕 kg/m3 `

¢??` InletVelocity = MassFlow / (InletDensity * FlowArea) = 〔2.952359〕 m/s `

¢??` OutletVelocity = MassFlow / (OutletDensity * FlowArea) = 〔3.034969〕 m/s `

¢??` ReportedAreaVelocity = MassFlow / (Density * ReportedArea) = 〔2.933528〕 m/s `

¢??` AreaDifference = ReportedArea / FlowArea - 1 = 〔0.02030533〕 `

¢??` Reynolds = Density * Velocity * TubeBore / Viscosity = 〔23,505.82〕 `

The exact tube count × bore gives 3.783 m², about 2% smaller than the report's
listed 3.86 m². Keep the two bases explicit: 3.86 m² reproduces approximately
2.94 m/s, while the count/bore calculation is approximately 2.99 m/s. Neither
value justifies claiming a strict below-3 m/s limit at every axial position or
in every tube. Outlet velocity and flow maldistribution must be distinguished
from mean velocity.

## Friction and local losses

Darcy–Weisbach: Δp = f (L/D) ρv²/2. The Darcy friction factor (not Fanning) is
solved from Colebrook using the calculated Reynolds number and relative
roughness. This is a steady, fully developed, single-phase approximation.

¢` function Darcy(rey, relative)
    if rey < 4000 throw "Turbulent model requires Re above 4000"
    x = 8
    for i in 1:30
        x = -2 * ln(relative / 3.7 + 2.51 * x / rey) / ln(10)
    end
    return 1 / x^2
end `

¢??` FrictionFactor = Darcy(Reynolds, Roughness / TubeBore) = 〔0.02505653〕 `

¢??` DynamicPressure = Density * Velocity^2 / 2 = 〔7.318211〕 kPa `

¢??` PassageLength = CoreLength + BottomReflector + TopReflector = 〔3.95〕 m `

¢??` CoreFriction = FrictionFactor * CoreLength / TubeBore * DynamicPressure =
〔44.53247〕 kPa `

¢??` ReflectorFriction = FrictionFactor * (BottomReflector + TopReflector) /
TubeBore * DynamicPressure = 〔7.203782〕 kPa `

¢??` PassageFriction = CoreFriction + ReflectorFriction = 〔51.73625〕 kPa `

¢??` EndLoss = (EntranceK + ExitK) * DynamicPressure = 〔10.97732〕 kPa `

¢??` TotalLoss = PassageFriction + EndLoss = 〔62.71357〕 kPa `

¢??` LossHead = TotalLoss / (Density * Gravity) = 〔3.914232〕 m `

¢??` HydrostaticDifference = Density * Gravity * PassageLength = 〔63.28664〕 kPa `

¢??` MassFlux = MassFlow / FlowArea = 〔4,890.064〕 'kg.m-2.s-1' `

¢??` AccelerationDifference = MassFlux^2 * (1 / OutletDensity - 1 /
InletDensity) = 〔0.4039669〕 kPa `

¢??` StaticPressureDifference = TotalLoss + HydrostaticDifference +
AccelerationDifference = 〔126.4042〕 kPa `

¢??` HydraulicPower = TotalLoss * VolumeFlow = 〔710.1318〕 kW `

TotalLoss is irreversible passage loss including the provisional end losses.
HydrostaticDifference is the approximate bottom-to-top pressure difference due
to upward elevation; it is **not** extra closed-loop pump head.
AccelerationDifference is a one-dimensional constant-area heated-flow estimate
using endpoint densities; StaticPressureDifference is therefore an approximate
plenum-to-plenum pressure difference, not additional friction. Detailed nozzle
velocities and entry/exit recovery require refinement.

## Roughness and 3 m/s checks

¢` RougherSurface = 0.00001 m `

¢??` RougherFactor = Darcy(Reynolds, RougherSurface / TubeBore) = 〔0.02650602〕 `

¢??` RougherTotalLoss = (RougherFactor * PassageLength / TubeBore + EntranceK +
ExitK) * DynamicPressure = 〔65.70644〕 kPa `

¢??` MeanFlowLimit = Density * FlowArea * VelocityLimit = 〔18,542.69〕 kg/s `

¢??` OutletFlowLimit = OutletDensity * FlowArea * VelocityLimit = 〔18,286.84〕
kg/s `

¢??` MeanCountThreshold = MassFlow / (Density * VelocityLimit * SingleArea) =
〔24,519.42〕 `

¢??` OutletCountThreshold = MassFlow / (OutletDensity * VelocityLimit *
SingleArea) = 〔24,862.46〕 `

Count thresholds are real-valued hydraulic comparisons; round upward for whole
tubes. They are not an adopted geometry change and include no maldistribution
allowance. The average velocity is just below 3 m/s; outlet velocity is
slightly above it with exact count/bore.

## Limits and reproduction

No entrance contour, tube-to-reflector step, blockage, bypass, nonuniform
power/flow, roughness growth, downcomer, plenum, nozzle or external-piping loss
has been resolved. Mean-temperature properties are sufficient for this
preliminary estimate; an independently calculated axial property integration is
recorded in the results JSON as a check, not as a Hurmet result.

The earlier 50%-above-SG pump allowance cannot be assessed by subtracting this
loss alone: that estimate uses a different flow and temperature case. No SG
failure, relief sizing, pump selection or geometry change is included.

Sources: UM/NRDSL-25/02, _Core Design Evolution of Wielenga Innovation Salt Tank
Reactor_, November 15, 2025, Tables 25, 42, 43 and 58; owner corrections 14
October 2026; current `wistr_reactor.py`; inherited SG roughness assumption.
Source hashes and explicit inputs are in `core-coolant-loss-results.json`.

Method reference: [NASA KSC-STD-Z-0017 Rev A, §§7.4–7.5][1], Colebrook and Darcy
loss equations. This is a general calculation method, not nuclear-system
qualification.

Run `python calculations/reactor/core_coolant_loss.py`, followed by `node
calculations/reactor/check_core_coolant_loss.cjs` with HURMET_ENGINE and
TEMML_ENGINE pointing to the project Hurmet bundles. Python uses an independent
bracketed Colebrook solve; Hurmet uses fixed-point iteration, recalculates all
cells and checks save/reopen and sensitivities. The publisher restores the
documented baseline; direct Hurmet input edits require updating the
verification baseline before comparison.

[1]: https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017\\\_RevA\\\_Final.pdf

[2]: https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017\_RevA\_Final.pdf
