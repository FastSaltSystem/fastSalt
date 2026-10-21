---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Steam Brayton cooler — balanced fan and salt-pump demand

¢` format = "h3" `

[**Overview of steam, nitrogen, open-air and supercritical CO₂
alternatives**][1] — common 30 MW comparison and links to all studies.

13 October 2026. Preliminary follow-up to the [cycle trial][2] and [salt-pump
estimate][3]. Estimate heat duties whose compressor, air-cooler fan and salt
pump can be powered together. No machinery or heat-exchanger rating is
established by this power balance.

The prior salt-pump estimate already reserved fan shaft power. Here both fan and
salt pump are electric: convert the cycle's **surplus before fan deduction**
through a 95% alternator, then supply both motors at 96% efficiency. Pump
hydraulic efficiency is 80%; fan efficiency is 65%. This avoids subtracting the
fan twice. The compressor and cycle shaft losses remain included upstream.

## Trial choices

Use one existing salt leg and one generator. Retain the current generator
hydraulic geometry, salt properties and original turbulent friction
correlation, with total loop drop equal to 1.5 times generator drop. Choose a
**10 K salt temperature drop** for the 30 and 50 MW trial duties. This is an
editable circulation target, not a revised reactor operating temperature or a
necessary optimum. At a nominal 875 K salt inlet it implies about 865 K outlet;
properties are frozen at the earlier 842.5 K reference for comparability and
should be updated in detailed work.

Ambient air is 30°C and leaves the cooler at 130°C; use 500 Pa total air-system
loss, 1,007 J/(kg K) heat capacity and inlet density at 1 atmosphere. Assume a
forced-draft fan at the cool inlet. Pressure drop includes the cooler and
ductwork allowance. A fan after the hot exchanger would need a density
correction. These air-side parameters are assumptions, not a vendor selection.
The [DOE fan-system sourcebook][4] describes the importance of pressure losses
and matching fans to the complete system.

Each heat-duty case scales steam flow and Brayton machinery to that duty while
retaining the prior cycle states and efficiencies. A 30 MW case produces three
times the 10 MW trial's surplus; it is **not the same 10 MW machine producing
30 MW cooling**. Similarly, holding 500 Pa air loss as duty increases assumes a
correspondingly larger cooler/airflow area, not simply speeding up the same fan
and exchanger. Steam-side 2% exchanger losses remain assumed and require
verification against the existing generator's passages, especially for the
vacuum 8:1 trial.

## Results per leg

+------------------------+------------+------------+------------+
| Quantity               | 2:1, 30 MW | 2:1, 50 MW | 8:1, 30 MW |
+========================+============+============+============+
| Available electricity  | 760.5      | 1,268      | 3,870      |
| after compressor, kW   |            |            |            |
+------------------------+------------+------------+------------+
| Salt flow, m³/s        | 1.802      | 3.003      | 1.802      |
+------------------------+------------+------------+------------+
| Salt loop drop, kPa    | 55.41      | 134.4      | 55.41      |
+------------------------+------------+------------+------------+
| Pump electricity, kW   | 130        | 525.4      | 130        |
+------------------------+------------+------------+------------+
| Fan electricity, kW    | 198.1      | 330.2      | 173.1      |
+------------------------+------------+------------+------------+
| Electrical margin, kW  | 432.4      | 411.9      | 3,567      |
+------------------------+------------+------------+------------+
| Air-cooler heat        | 28.99      | 48.31      | 25.34      |
| rejection, MW          |            |            |            |
+------------------------+------------+------------+------------+
| Airflow at cool inlet, | 247.2      | 412        | 216.1      |
| m³/s                   |            |            |            |
+------------------------+------------+------------+------------+
| Minimum net reactor    | 29.88      | 49.5       | 29.88      |
| cooling with pump      |            |            |            |
| losses, MW             |            |            |            |
+------------------------+------------+------------+------------+
| Compressor-inlet steam | 21.57      | 35.95      | 1,564      |
| volume, m³/s           |            |            |            |
+------------------------+------------+------------+------------+
{.grid colWidths="250 125 125 125"}

At 30 MW and 2:1, the actual fan/pump demand splits approximately **60% to the
fan and 40% to the salt pump**, using only about 43% of available electricity.
The remaining 57% is unallocated margin for other consumers or export; no
allowance has yet been assigned to controls, heat tracing, drive electronics or
other station services.

Gross salt-to-cycle heat is distinguished from net heat removed from the
reactor. Hydraulic work returns to the salt as heat; for the lower net estimate
assume all pump shaft work ultimately enters the salt. Alternator and motor
losses are assumed outside the salt. A 30 MW set then removes about
**29.88–29.90 MW net** from the reactor. Three independent sets give 90 MW
gross and approximately **89.63–89.70 MW net**, contingent on the same per-leg
hydraulic assumption; the common reactor flow network is not modeled.

The dedicated air cooler rejects less than the heat entering the cycle because
some becomes work. Ultimately residual electricity and equipment losses also
need destinations; rejecting them locally adds to site heat rejection, not to
the specified steam-to-air exchanger duty.

## How far can the power balance extend?

For the chosen 10 K salt drop and the base 2:1 cycle, the model's zero-reserve
electrical balance occurs at about **69.6 MW per leg**. Pump demand rises much
faster than heat duty, while fan demand and cycle surplus scale linearly only
because cooler and machinery sizes are being scaled. This is a mathematical
boundary with no auxiliary reserve, not a recommended operating point or a
demonstrated capacity. At 50 MW it still leaves about 412 kW electrical margin.

There is no unique maximum cooling duty from surplus power alone. With the
original 65 K salt drop, even the 500 MW design-duty salt flow remains below
the extrapolated available-power budget. That does not establish 500 MW
auxiliary-cooler feasibility; it means the power balance is no longer the
useful sizing constraint. Exchanger thermal performance, steam passage pressure
loss, compressor/turbine size, air-system size and operating temperatures must
define the equipment limit.

## Air-cooler scale and sensitivity

At 30 MW with the 2:1 cycle, the steam-to-air exchanger rejects 28.99 MW using
about 247 m³/s of inlet air. If a provisional 3 m/s superficial face velocity
is selected, the required frontal area is about **82 m²**. At 50 MW it is about
**137 m²**. These are airflow face areas, not fin surface areas or complete
installed footprints. Multiple fan bays could provide this area. No
heat-transfer coefficient, fin geometry or core depth has been selected; the
assumed 500 Pa loss and the required thermal surface must be achieved together.

The 8:1 case has ample power in this idealized scaling but requires about
**1,564 m³/s compressor-inlet steam volume at 30 MW**. Its cold-end steam
temperature is only about 44.8°C against 30°C inlet air, so the close
temperature approach also makes heat-exchanger performance consequential. This
does not support calling that machinery small.

| 30 MW, 2:1 air-side assumption | Fan electricity, kW | Remaining electricity, kW |
|--------------------------------|---------------------|---------------------------|
| 1,000 Pa, 100 K air rise       | 396.2               | 234.3                     |
| 500 Pa, 50 K air rise          | 396.2               | 234.3                     |
| 1,000 Pa, 50 K air rise        | 792.4               | \-161.9                   |
{.grid colWidths="250 125 125"}

The last case has negative margin: it cannot power the fan and pump at the
specified operating point. The result therefore depends on obtaining low
air-side pressure loss and a suitable air-temperature rise, as well as the
preceding cycle efficiency assumptions.

## Hurmet verification of the 30 MW, 2:1 trial

¢` HeatDuty = 30 MW `

¢` SaltDrop = 10 K `

¢` SaltDensity = 1637.93125 kg/m3 `

¢` SaltHeatCapacity = 1016.63 J.kg-1.K-1 `

¢` SaltViscosity = 0.0029496778537971 kg.m-1.s-1 `

¢` FlowArea = 1.8611109039131 m2 `

¢` TubeDiameter = 0.014 m `

¢` TubeLength = 19.8790057 m `

¢` Roughness = 1e-06 m `

¢` LoopFactor = 1.5 `

¢` GeneratorEfficiency = 0.95 `

¢` MotorEfficiency = 0.96 `

¢` PumpEfficiency = 0.8 `

¢` FanEfficiency = 0.65 `

¢` AirDensity = 1.1643981014192 kg/m3 `

¢` AirHeatCapacity = 1007 J.kg-1.K-1 `

¢` AirRise = 100 K `

¢` AirPressureDrop = 500 Pa `

¢` FaceVelocity = 3 m/s `

¢` SurplusFraction = 0.026684870286743 `

¢` RejectFraction = 0.96627602883187 `

¢%%` AvailableElectricity = HeatDuty * SurplusFraction * GeneratorEfficiency =
〔761〕 kW `

¢%%` SaltFlow = HeatDuty / (SaltDensity * SaltHeatCapacity * SaltDrop) = 〔1.8〕
m3/s `

¢%%` SaltVelocity = SaltFlow / FlowArea = 〔0.968〕 m/s `

¢%%` SaltReynolds = SaltDensity * SaltVelocity * TubeDiameter / SaltViscosity =
〔7,526〕 `

¢%%` Friction = (8/6.0516) * ln(Roughness/TubeDiameter +
(7/SaltReynolds)^0.9)^(-2) = 〔0.0339〕 `

¢%%` LoopDrop = LoopFactor * Friction * TubeLength / TubeDiameter *
SaltDensity * SaltVelocity^2 / 2 = 〔55.4〕 kPa `

¢%%` PumpHydraulic = SaltFlow * LoopDrop = 〔100〕 kW `

¢%%` PumpShaft = PumpHydraulic / PumpEfficiency = 〔125〕 kW `

¢%%` PumpElectricity = PumpShaft / MotorEfficiency = 〔130〕 kW `

¢%%` AirHeat = HeatDuty * RejectFraction = 〔29〕 MW `

¢%%` AirMass = AirHeat / (AirHeatCapacity * AirRise) = 〔288〕 kg/s `

¢%%` AirFlow = AirMass / AirDensity = 〔247〕 m3/s `

¢%%` FanElectricity = AirFlow * AirPressureDrop / (FanEfficiency *
MotorEfficiency) = 〔198〕 kW `

¢%%` RemainingElectricity = AvailableElectricity - PumpElectricity -
FanElectricity = 〔432〕 kW `

¢%%` NetReactorMinimum = HeatDuty - PumpShaft = 〔29.9〕 MW `

¢%%` NetReactorMaximum = HeatDuty - PumpHydraulic = 〔29.9〕 MW `

¢%%` FaceArea = AirFlow / FaceVelocity = 〔82.4〕 m2 `

The heat duty, salt drop and air-system inputs recalculate directly in this
Hurmet block, provided the resulting salt Reynolds number remains above 4,000.
The summary tables and zero-reserve root are Python results and do not change
automatically in Hurmet. Real-steam states and efficiencies are imported
through the two cycle fractions; rerun the original real-steam solver for
altered temperatures, pressures or machine efficiencies.

## Reproduction and limits

Run `python brayton_fan_pump_balance.py`, then `node check_brayton_fan_pump.cjs`
using the existing HURMET_ENGINE and TEMML_ENGINE paths. Results and source
hashes are in `brayton-fan-pump-results.json`. The checker verifies 17 results
after save/reopen and exercises heat duty, air pressure drop and the
power-deficit sensitivity. Python verifies the 500 MW hydraulic reference and
zero-reserve root.

This is an exploratory energy/hydraulic screen. No assumption of a fixed-size
cooler retaining constant pressure loss at arbitrary airflow is made.
Heat-transfer capability of the generator and air cooler, operating maps,
pressure losses, local salt freezing, stopped-main-pump resistance, startup and
decay-heat requirements remain unresolved. The positive 2:1 balance can
disappear with the less favorable machine efficiencies already tested in the
preceding cycle study. No reactor-building geometry or adopted cooling design
is changed.

[1]: brayton-overview.md

[2]: Steam%20Brayton%20cooler%20-%20Hurmet.md

[3]: Brayton-driven%20salt%20pump%20-%20Hurmet.md

[4]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sourcebook.pdf

[5]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sourcebook.pdf

[6]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sourcebook.pdf

[7]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sourcebook.pdf

[8]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sourcebook.pdf

[9]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sourcebook.pdf

[10]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sourcebook.pdf

[11]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\\\\\\\\\_assistance/pdfs/fan\\\\\\\\\\\\\\\_sourcebook.pdf

[12]: https://www1.eere.energy.gov/manufacturing/tech\\\\\\\_assistance/pdfs/fan\\\\\\\_sourcebook.pdf

[13]: https://www1.eere.energy.gov/manufacturing/tech\\\_assistance/pdfs/fan\\\_sourcebook.pdf

[14]: https://www1.eere.energy.gov/manufacturing/tech\_assistance/pdfs/fan\_sourcebook.pdf
