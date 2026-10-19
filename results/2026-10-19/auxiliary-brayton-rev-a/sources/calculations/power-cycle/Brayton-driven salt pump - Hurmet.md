---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: undefined
saveDate: 2026-10-12
---------------

# Brayton-driven salt pony pump — preliminary estimate

12 October 2026. Use the [steam-generator hydraulic worksheet][1], with the
owner's **50% additional pressure-drop allowance for the entire salt loop**, to
estimate circulation powered by the [Brayton trial][2]. This is a power-balance
estimate; it does not select a pump or demonstrate a reactor cooling system.

The principal comparison is **one salt leg through one generator, with 10 MW
transferred from salt into its auxiliary Brayton loop**. The heat input is a
normalization, not a specified decay-heat requirement. Three such independent
sets would transfer 30 MW gross in total. A separate shared-power case below
instead keeps the entire installation at 10 MW.

## Assumptions and calculation method

The current generator basis uses salt at 875/810 K, a 65 K drop, and properties
at 842.5 K. It contains 12,090 parallel salt tubes, 14 mm bore, 19.879 m
hydraulic length and 0.001 mm roughness. The later 17 m visual casing height
has not revised that hydraulic length. At 500 MW per leg this reproduces 4.6195
m³/s and 190.873 kPa across the generator, or 286.309 kPa including the
additional loop allowance.

Pressure loss is recalculated at the reduced flow with the **original
worksheet's friction correlation**, including its Reynolds-number dependence.
Holding the full-flow head constant would substantially underpredict
circulation. A closed circulation loop has no net geometric lift; this estimate
neglects buoyancy assistance. The 50% allowance remains a lumped assumption for
reactor, piping, valves and the installed pump path. See the [DOE
pumping-system sourcebook][3] for the distinction between friction and static head.

The Brayton turbine already powers its compressor and includes its
shaft-transfer loss. Retain the preceding illustrative air fan as a
**shaft-power deduction**, then convert the remaining power to electricity at
an assumed 95% alternator efficiency. The pony-pump motor is 96% efficient and
the pump is 80% efficient. These are provisional efficiencies for appropriately
selected machinery; no actual pump, motor or drive curve has been applied. An
electric fan, variable-frequency drive, controls, heat tracing or other
consumers would require extra deductions.

Python solves `flow × loop_pressure_drop(flow) = remaining_shaft_power ×
generator_efficiency × motor_efficiency × pump_efficiency`. The flow roots and
Brayton power fractions are imported below. Hurmet independently recalculates
friction, power closure, heat transport and temperature change. **After
changing a physical input, rerun `brayton_salt_pump.py` and the checker to
solve new roots**; changing the inputs in Hurmet alone does not update the
imported flow roots. Real-steam cycle state changes require rerunning
`brayton_cooler.py` first.

## Common inputs

¢` Density = 1637.93125 kg/m3 `

¢` HeatCapacity = 1016.63 J.kg-1.K-1 `

¢` Viscosity = 0.0029496778537971 kg.m-1.s-1 `

¢` TubeCount = 12090 `

¢` TubeDiameter = 0.014 m `

¢` TubeLength = 19.8790057 m `

¢` Roughness = 1e-06 m `

¢` LoopFactor = 1.5 `

¢` GeneratorEfficiency = 0.95 `

¢` MotorEfficiency = 0.96 `

¢` PumpEfficiency = 0.8 `

¢` HeatDuty = 10 MW `

¢` ReferenceSaltDrop = 65 K `

¢??` FlowArea = TubeCount * π * TubeDiameter^2 / 4 = 〔1.86111090391313〕 m2 `

¢??` ReferenceFlow = 500 'MW' / (Density * HeatCapacity * ReferenceSaltDrop) =
〔4.61953282645811〕 m3/s `

## Main comparison: all available surplus used for circulation

+------------------------------------+-----------------+-----------------+
| Quantity, per 10 MW trial          | 2:1 steam cycle | 8:1 steam cycle |
+====================================+=================+=================+
| Shaft surplus after fan, kW        | 203.5           | 1,303           |
+------------------------------------+-----------------+-----------------+
| Pony-pump electricity, kW          | 193.3           | 1,237           |
+------------------------------------+-----------------+-----------------+
| Salt flow, m³/s                    | 2.084           | 4.099           |
+------------------------------------+-----------------+-----------------+
| Salt mass flow, kg/s               | 3,413           | 6,713           |
+------------------------------------+-----------------+-----------------+
| Whole-loop pressure drop, kPa      | 71.23           | 231.9           |
+------------------------------------+-----------------+-----------------+
| Salt tube Reynolds number          | 8,705           | 1.712e+04       |
+------------------------------------+-----------------+-----------------+
| Heat transport if salt drops 65 K, | 225.5           | 443.6           |
| MW                                 |                 |                 |
+------------------------------------+-----------------+-----------------+
| Actual gross heat into the trial,  | 10              | 10              |
| MW                                 |                 |                 |
+------------------------------------+-----------------+-----------------+
| Salt drop for that 10 MW, K        | 2.882           | 1.465           |
+------------------------------------+-----------------+-----------------+
{.grid colWidths="250 135 135"}

**The 226 MW and 444 MW figures describe heat carried by the calculated salt
flow at a hypothetical 65 K drop. They are not the heat-removal ratings of the
10 MW Brayton units.** Removing that much heat would require correspondingly
larger steam flow, machinery and air coolers, and another coupled
thermal/hydraulic analysis. The base 10 MW trial instead gives about 2.88 K
salt cooling at maximum surplus-powered flow; the vacuum 8:1 trial gives about
1.47 K. These small drops also mean the salt properties near the hot end differ
somewhat from the inherited mean; frozen mean properties are retained for this
first screen.

For an actual 10 MW requirement, circulation need not consume all surplus. A
smaller pump or suitable speed control can trade salt temperature drop against
flow and preserve power for other loads. Very low flow would require a
laminar/transition correlation and a new heat-transfer analysis; the original
turbulent expression is not used to claim performance there.

## Recalculated checks: 2:1 case

¢` TwoShaftFraction = 0.020345780629393 `

¢` TwoFlow = 2.0838596064202 m3/s `

¢??` TwoElectrical = HeatDuty * TwoShaftFraction * GeneratorEfficiency =
〔193.284915979233〕 kW `

¢??` TwoPumpShaft = TwoElectrical * MotorEfficiency = 〔185.553519340064〕 kW `

¢??` TwoHydraulicAvailable = TwoPumpShaft * PumpEfficiency = 〔148.442815472051〕 kW `

¢??` TwoVelocity = TwoFlow / FlowArea = 〔1.11968588332846〕 m/s `

¢??` TwoReynolds = Density * TwoVelocity * TubeDiameter / Viscosity =
〔8,704.5298678205〕 `

¢??` TwoFriction = (8/6.0516) * ln(Roughness/TubeDiameter +
(7/TwoReynolds)^0.9)^(-2) = 〔0.0325742755741179〕 `

¢??` TwoGeneratorDrop = TwoFriction * TubeLength / TubeDiameter * Density *
TwoVelocity^2 / 2 = 〔47.4897045254283〕 kPa `

¢??` TwoLoopDrop = LoopFactor * TwoGeneratorDrop = 〔71.2345567881424〕 kPa `

¢??` TwoHydraulicRequired = TwoFlow * TwoLoopDrop = 〔148.442815472056〕 kW `

¢??` TwoPowerClosure = TwoHydraulicRequired / TwoHydraulicAvailable =
〔1.00000000000003〕 `

¢??` TwoMassFlow = Density * TwoFlow = 〔3,413.21876996835〕 kg/s `

¢??` TwoTransport65K = TwoMassFlow * HeatCapacity * ReferenceSaltDrop =
〔225.54873887734〕 MW `

¢??` TwoSaltDrop = HeatDuty / (TwoMassFlow * HeatCapacity) = 〔2.88186049381322〕 K `

¢??` TwoNetMinimum = HeatDuty - TwoPumpShaft = 〔9.81444648065994〕 MW `

¢??` TwoNetMaximum = HeatDuty - TwoHydraulicRequired = 〔9.85155718452794〕 MW `

## Recalculated checks: 8:1 case

¢` EightShaftFraction = 0.13025639815148 `

¢` EightFlow = 4.0986270096807 m3/s `

¢??` EightElectrical = HeatDuty * EightShaftFraction * GeneratorEfficiency =
〔1,237.43578243906〕 kW `

¢??` EightPumpShaft = EightElectrical * MotorEfficiency = 〔1,187.9383511415〕 kW `

¢??` EightHydraulicAvailable = EightPumpShaft * PumpEfficiency =
〔950.350680913198〕 kW `

¢??` EightVelocity = EightFlow / FlowArea = 〔2.20224759366195〕 m/s `

¢??` EightReynolds = Density * EightVelocity * TubeDiameter / Viscosity =
〔17,120.4533707092〕 `

¢??` EightFriction = (8/6.0516) * ln(Roughness/TubeDiameter +
(7/EightReynolds)^0.9)^(-2) = 〔0.0274087764971781〕 `

¢??` EightGeneratorDrop = EightFriction * TubeLength / TubeDiameter * Density *
EightVelocity^2 / 2 = 〔154.580331196848〕 kPa `

¢??` EightLoopDrop = LoopFactor * EightGeneratorDrop = 〔231.870496795272〕 kPa `

¢??` EightHydraulicRequired = EightFlow * EightLoopDrop = 〔950.350680913184〕 kW `

¢??` EightPowerClosure = EightHydraulicRequired / EightHydraulicAvailable =
〔0.999999999999985〕 `

¢??` EightMassFlow = Density * EightFlow = 〔6,713.26926125007〕 kg/s `

¢??` EightTransport65K = EightMassFlow * HeatCapacity * ReferenceSaltDrop =
〔443.619210389203〕 MW `

¢??` EightSaltDrop = HeatDuty / (EightMassFlow * HeatCapacity) =
〔1.465220587336〕 K `

¢??` EightNetMinimum = HeatDuty - EightPumpShaft = 〔8.8120616488585〕 MW `

¢??` EightNetMaximum = HeatDuty - EightHydraulicRequired = 〔9.04964931908682〕 MW `

## Heat returned by the salt pump

Hydraulic power ultimately dissipates as heat within the salt loop. Depending on
pump construction, some or all of the remaining pump-shaft loss may also enter
the salt. Assuming motor, alternator and fan losses are outside the salt, a
gross 10 MW transfer into the Brayton unit leaves approximately **9.81–9.85 MW
net reactor heat removal for 2:1**, and **8.81–9.05 MW for 8:1**, if all
available surplus drives the pump. These are pump-loss bounds, not uncertainty
bounds on the complete system. The air cooler's separate duties remain 9.663
and 8.445 MW; the rest of the cycle heat appears as work and equipment losses.
Reducing unnecessary pumping would reduce heat returned to the salt.

## Three legs sharing one 10 MW auxiliary heat duty

For a comparison with only 10 MW total across the plant, divide its surplus
equally among three independently modeled legs/pumps. Each leg receives one
third of the power and transfers one third of the heat. Recompute each flow,
rather than simply dividing the single-leg flow by three. Actual common-reactor
losses and distribution require a network calculation.

| Quantity                 | 2:1 steam cycle | 8:1 steam cycle |
|--------------------------|-----------------|-----------------|
| Flow per leg, m³/s       | 1.391           | 2.749           |
| Total salt flow, m³/s    | 4.174           | 8.248           |
| Salt temperature drop, K | 1.439           | 0.7281          |
{.grid colWidths="250 135 135"}

## Sensitivity and limits

+------------------------------------+---------------------+---------------------+
| Single-leg 10 MW case              | 2:1 salt flow, m³/s | 8:1 salt flow, m³/s |
+====================================+=====================+=====================+
| Pump efficiency 60% instead of 80% | 1.875               | 3.693               |
+------------------------------------+---------------------+---------------------+
| Loop loss 2.0 × generator instead  | 1.875               | 3.693               |
| of 1.5 ×                           |                     |                     |
+------------------------------------+---------------------+---------------------+
{.grid colWidths="250 135 135"}

All reported flow solutions remain above Reynolds number 4,000. The
approximately 50% additional loss is assumed to scale with generator loss; it
is not a separately modeled reactor resistance. No stopped-main-pump
resistance, check-valve cracking head, pony-pump branch sizing, NPSH, thermal
stratification, bypass distribution or natural-circulation credit has been
resolved.

Salt-pumping power appears affordable **if the positive Brayton surplus is
achieved**. The preceding cycle study shows that lower compressor/turbine
efficiencies or greater steam-side pressure losses can eliminate the 2:1
surplus. The 8:1 trial still requires about 521 m³/s compressor-inlet steam
volume per 10 MW, versus 7.19 m³/s for 2:1; its stronger pump margin does not
make that vacuum machinery small. Maintaining the assumed 830 K turbine inlet
at reduced heat duty also requires a generator heat-transfer and control check.
Startup power, actual heat demand, freeze protection and heat-rejection
performance remain unresolved.

## Reproduction and checks

Run `python brayton_salt_pump.py`, then `node check_brayton_salt_pump.cjs` with
`HURMET_ENGINE` and `TEMML_ENGINE` pointing to the existing Hurmet/Temml
bundles. The Python program uses only the standard library; its Brayton inputs
come from `brayton-cooler-results.json`. It verifies the inherited full-flow
pressure drop, positive turbulent flow roots and power balance. The checker
recalculates and saves/reopens the Hurmet document, compares all named results
with Python and verifies that changes to loop allowance and pump efficiency
break the imported-root power balance as expected. This prevents silently
treating the imported flow as a live Hurmet root solve. Source hashes, detailed
results and expected checks are stored in `brayton-salt-pump-results.json`.

[1]: ../steam-generator/Generator%20sizing%20-%20Hurmet.md

[2]: Steam%20Brayton%20cooler%20-%20Hurmet.md

[3]: https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf
