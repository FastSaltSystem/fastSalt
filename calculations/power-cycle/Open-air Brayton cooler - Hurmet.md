---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: undefined
saveDate: 2026-10-13
---------------

# Open-air Brayton auxiliary cooler — preliminary comparison

13 October 2026. Compare an externally heated open cycle with the preserved
[closed steam][1] and [closed nitrogen][2] trials. Flow is **outside air →
intake/filter → compressor → salt-to-air heater → turbine → exhaust duct →
atmosphere**. The turbine drives the compressor and an alternator serving the
salt pump. There is no combustion, recuperator, separate air cooler or separate
cooler fan in this trial.

Real dry-air properties use CoolProp 7.2.0 HEOS::Air and its [Lemmon et al.
equation of state][3]. Humidity and weather-related intake-system behavior are
not modeled. Outside air is 30°C at 101.325 kPa. Intake/filter loss is
provisionally 500 Pa; turbine exhaust backpressure is 1,000 Pa above
atmosphere. Heater pressure loss is 2% of compressor discharge. These are
assumed total-pressure budgets, not verified duct/filter/exchanger losses. Gas
kinetic and elevation terms are neglected in the station energy balances.
Intake and final exhaust pressure losses are treated as adiabatic throttles.

Compressor/turbine isentropic efficiencies remain 85%/88%; turbine
shaft-transfer efficiency is 98% and alternator efficiency 95%. Turbine inlet
stays at 830 K (556.85°C). Unlike the closed trials, compressor inlet
temperature is set by outside air, so heater inlet temperature follows from
compression ratio. The compressor supplies the pressure needed for the complete
air path; adding another fan deduction would double-count that duty unless
additional hardware/losses are introduced.

## Pressure-ratio comparison, each at 10 MW salt-to-air heat input

| Quantity | 2:1 | 4:1 | Matched heater inlet | 8:1 |
| --- | --- | --- | --- | --- |
| Compressor pressure ratio | 2 | 4 | 6.832 | 8 |
| Heater inlet, °C | 107.9 | 201.9 | 286.9 | 314.1 |
| Turbine exhaust, °C | 440.8 | 336.2 | 266.6 | 247.8 |
| Air mass flow, kg/s | 21.12 | 26.45 | 34.45 | 38.2 |
| Compressor-inlet volume, m³/s | 18.22 | 22.82 | 29.72 | 32.96 |
| Atmospheric exhaust volume, m³/s | 42.72 | 45.68 | 52.69 | 56.39 |
| Compressor shaft demand, MW | 1.657 | 4.605 | 9.023 | 11.09 |
| Surplus shaft power, MW | 0.9673 | 1.575 | 1.484 | 1.286 |
| Available electricity, MW | 0.9189 | 1.496 | 1.41 | 1.222 |

The approximately 6.8:1 case reproduces the existing 560/830 K heater endpoints
and is the principal comparison. The 4:1 case has slightly more surplus per
unit heat in this limited sweep but admits air to the heater at about 202°C.
Its larger cold-end temperature difference requires a new local
wall-temperature and salt-freezing assessment. Neither case establishes the
optimal ratio.

## Comparison at the same 287/557°C heater endpoints

| Per 10 MW heat input | Closed steam 2:1 | Closed nitrogen 4:1 | Open air matched |
| --- | --- | --- | --- |
| Compressor pressure range, bar absolute | 5→10 | 10→40 | 1.008→6.888 |
| Compressor inlet, °C | 192.1 | 84.23 | 30 |
| Electricity after air-cooler fan, before salt pump, MW | 0.1875 | 0.8363 | 1.41 |
| Compressor inlet volume, m³/s | 7.191 | 3.557 | 29.72 |

This compares complete candidate operating points; it does not attribute the
gain solely to replacing nitrogen with air. The open cycle draws colder ambient
air directly, changes the pressure ratio and removes the closed-loop cooler
pressure loss and fan. A closed loop cannot cool exactly to ambient with a
finite dry exchanger. Open-air inlet volume is about 8.4 times the pressurized
nitrogen candidate's volume, although total installed footprints cannot be
inferred from volume alone. The nitrogen alternative still has its separate
large air cooler and fan.

## 30 MW-per-leg illustration

Scaling the matched-temperature open cycle to 30 MW gives **103.3 kg/s** of air,
**89.2 m³/s** compressor inlet volume and **158.1 m³/s** atmospheric hot
exhaust. Available electricity is **4.230 MW**. Subtract the prior **130 kW**
salt-pump demand for a 10 K salt drop and retain **4.100 MW**. The closed
nitrogen 4:1 case retained 2.379 MW, and closed steam 2:1 retained 0.432 MW
under their respective assumptions.

The exhaust carries approximately **24.90 MW** above inlet-air enthalpy. The
balance leaves as work and machinery losses. This is not an additional
heat-removal duty to add to the 30 MW taken from salt. Net reactor cooling
remains about 29.88–29.90 MW after heat returned by the same salt pump, before
other heat gains.

At a purely illustrative 15 m/s exhaust-duct velocity, the matched 30 MW case
needs about 10.5 m² flow area, equivalent to a 3.66 m round duct. This is a
flow-area allowance, not a stack design; duct length, bends, discharge
velocity, noise treatment, weather and recirculation must fit within a verified
backpressure budget. Cooler removal does not eliminate hot-air discharge
routing.

## Implications for the reactor installation

The component arrangement is simpler: no secondary air cooler, its fan or closed
working-gas inventory system. The open process air passes through the heater on
the other side of a metal boundary from salt; it is not direct air contact with
salt or reactor-room ventilation. The heater boundary must keep process
contaminants out of the discharged stream. Leak detection, isolation and the
response to a failed boundary therefore matter to deciding whether open
discharge is acceptable. This calculation assumes an intact separating heat
exchanger and does not characterize exhaust releases.

Open operation gives up adjustable high suction pressure as a way to shrink
turbomachinery. It also introduces outside-air moisture and oxygen into the
gas-side equipment, so materials and the shared-generator drying/isolation
arrangement need checking. Salt-to-air heat-transfer performance and pressure
loss must be verified; the existing steam-generator pressure rating alone does
not establish this service. A dedicated exchanger remains an option rather than
an adopted design.

Startup still needs an initial drive source, and cooler outlet/salt freeze
controls remain required. Ambient-temperature changes alter compressor
discharge and power margin; these are fixed-state capacity comparisons, not
validated startup, cooldown or off-design maps. Residual electricity needs a
useful load or a defined control strategy. A recuperator would be an additional
component and is not assumed for this heat-removal objective.

## Sensitivities at the matched pressure ratio

These trials keep turbine inlet at 557°C, compressor ratio fixed and heat input
at 10 MW; the heater inlet temperature is allowed to change.

| Separate sensitivity | Heater inlet, °C | Surplus shaft power, MW |
| --- | --- | --- |
| 45°C outside air | 313.5 | 1.154 |
| 80% compressor / 85% turbine efficiency | 302.5 | 0.596 |
| 5% heater loss / 5 kPa exhaust backpressure | 286.9 | 1.186 |

## Hurmet verification of the matched-temperature 10 MW case

¢` HeatDuty = 10 MW `

¢` ShaftEfficiency = 0.98 `

¢` GeneratorEfficiency = 0.95 `

¢` PumpAtThirtyMW = 129.99027717071 kW `

¢` InletDensity = 1.1589887238942 kg/m3 `

¢` ExhaustDensity = 0.65380567936662 kg/m3 `

¢` HOne = 429468.03640126 J/kg `

¢` HTwo = 691397.22763044 J/kg `

¢` HThree = 981683.82872752 J/kg `

¢` HFour = 670444.10082073 J/kg `

¢??` MassFlow = HeatDuty / (HThree - HTwo) = 〔34.4487136581813〕 kg/s `

¢??` CompressorPower = MassFlow * (HTwo - HOne) = 〔9.02312370737303〕 MW `

¢??` TurbinePower = MassFlow * (HThree - HFour) = 〔10.7218082657113〕 MW `

¢??` AvailableShaft = ShaftEfficiency * TurbinePower - CompressorPower =
〔1.48424839302401〕 MW `

¢??` AvailableElectricity = GeneratorEfficiency * AvailableShaft =
〔1.41003597337281〕 MW `

¢??` ExhaustHeat = MassFlow * (HFour - HOne) = 〔8.30131544166177〕 MW `

¢??` EnergyResidual = HeatDuty - ExhaustHeat - TurbinePower + CompressorPower =
〔0〕 MW `

¢??` InletFlow = MassFlow / InletDensity = 〔29.7230792224049〕 m3/s `

¢??` ExhaustFlow = MassFlow / ExhaustDensity = 〔52.6895295427133〕 m3/s `

¢??` ThirtyMWMargin = 3 * AvailableElectricity - PumpAtThirtyMW =
〔4.10011764294771〕 MW `

Real-air state enthalpies are imported from Python; Hurmet recalculates energy
and flow at those fixed states. The last formula specifically assumes the 10 MW
normalization and uses the prior 30 MW salt-pump demand. Summary tables are
imported snapshots. Change temperatures, efficiencies or pressure losses in
Python and rerun rather than treating imported states as live property calls.

## Reproduction and status

Run `open_air_brayton.py` in the project's CoolProp environment, then
`check_open_air_brayton.cjs` with the existing Hurmet/Temml engine paths.
Python checks energy, entropy, matching the heater inlet and duty scaling. JSON
preserves all states, source hashes and sensitivities. Hurmet checks ten
numerical results, save/reopen and alternator-efficiency sensitivity. No
cooling architecture, exchanger or turbine rating is selected by this
preliminary screen.

[1]: Steam%20Brayton%20cooler%20-%20Hurmet.md

[2]: Nitrogen%20versus%20steam%20Brayton%20-%20Hurmet.md

[3]: https://coolprop.sourceforge.net/fluid\\\_properties/fluids/Air.html

[4]: https://coolprop.sourceforge.net/fluid\_properties/fluids/Air.html
