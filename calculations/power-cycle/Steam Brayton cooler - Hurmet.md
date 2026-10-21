---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Steam Brayton auxiliary cooler — preliminary screen

¢` format = "h3" `

12 October 2026. Exploratory calculation requested by the project owner, not an
adopted cooling-system design. The purpose is to determine whether a
non-condensing steam loop can power its compressor and reject substantial heat
to air.

The [current generator worksheet][1] uses **560 K (286.85°C) inlet and 830 K
(556.85°C) outlet**, rather than the approximately 260°C recalled in
discussion. Those temperature endpoints are retained. Normal steam-plant
pressure is **not** retained: the auxiliary trial compresses steam from **5 to
10 bar absolute**. At the normal 24 MPa and 560 K, water is liquid-like, not
the vapor required by this trial. Using the existing generator in this mode
would require an isolated, lower-pressure operating arrangement; it cannot be
connected directly to live 24 MPa headers.

Steam enthalpies, temperatures, density and sensitivity results below are
imported from [brayton\_cooler.py][2], using CoolProp 7.2.0 HEOS water /
IAPWS-95. Hurmet recalculates duty scaling and the fan allowance; it does not
solve the steam properties. Changing cycle temperatures, pressures or component
efficiencies requires rerunning Python and this publisher, then the Hurmet
checker.

## Trial assumptions

*   Compressor pressure ratio: 2.0.
*   Compressor/turbine isentropic efficiencies: 85% / 88%; assumptions requiring
    equipment confirmation.
*   Shaft power transfer efficiency: 98%.
*   Steam-side pressure loss: 2% across each exchanger, including its associated
    piping allowance.
*   Heat input: 10 MW for convenient scaling, not a selected decay-heat duty.
*   No recuperator, condensation or feedwater pump.

## Calculated cycle states

+-------------------------------------+----------------+-----------------------+
| Point                               | Temperature °C | Pressure bar absolute |
+=====================================+================+=======================+
| Air-cooler outlet / compressor      | 192.1          | 5.000                 |
| inlet                               |                |                       |
+-------------------------------------+----------------+-----------------------+
| Compressor outlet / generator inlet | 286.8          | 10.000                |
+-------------------------------------+----------------+-----------------------+
| Generator outlet / turbine inlet    | 556.9          | 9.800                 |
+-------------------------------------+----------------+-----------------------+
| Turbine outlet / air-cooler inlet   | 460.2          | 5.102                 |
+-------------------------------------+----------------+-----------------------+
{.grid colWidths="240 120 120"}

The compressor inlet is about 40 K above saturation at 5 bar. Sampled
heat-exchanger and actual/isentropic machine paths remain dry. This is a
steady-state check; shutdown condensation and restart inventory are not
analyzed.

## Editable duty scaling

¢` HeatInput = 10 MW `

¢` hA = 2838.825708006 'kJ/kg' `

¢` hB = 3023.389688285 'kJ/kg' `

¢` hC = 3603.358132588 'kJ/kg' `

¢` hD = 3399.235313214 'kJ/kg' `

¢` ShaftEfficiency = 0.98 `

¢%%` SteamFlow = HeatInput / (hC - hB) = 〔17.2〕 'kg/s' `

¢%%` TurbinePower = SteamFlow * (hC - hD) = 〔3.52〕 MW `

¢%%` CompressorPower = SteamFlow * (hB - hA) = 〔3.18〕 MW `

¢%%` ShaftLoss = TurbinePower * (1 - ShaftEfficiency) = 〔0.0704〕 MW `

¢%%` AvailablePower = TurbinePower - CompressorPower - ShaftLoss = 〔267〕 kW `

¢%%` AirCoolerDuty = SteamFlow * (hD - hA) = 〔9.66〕 MW `

¢%%` EnergyResidual = HeatInput - AirCoolerDuty - TurbinePower + CompressorPower
= 〔0〕 MW `

¢` InletDensity = 2.39786042219 'kg/m3' `

¢%%` InletVolumeFlow = SteamFlow / InletDensity = 〔7.19〕 'm3/s' `

Available power is after compressor and shaft losses, before air fans, salt
pumps and other auxiliaries. If remaining shaft power is ultimately dissipated
within the cooling installation, the total environmental heat release
approaches the full heat input. The air-cooler duty shown is only the
steam-to-air exchanger duty. The turbine transfers approximately 3.52 MW
internally to remove 10 MW of reactor heat; this is a multi-megawatt machine
despite its small net output.

## Illustrative air-fan allowance

Use 30°C incoming air, a 100 K rise, 500 Pa air-path loss and 65% fan
efficiency. These are placeholders, not a designed air cooler. Fan power uses
inlet-air volume and assumes direct shaft drive; gearing or electrical
conversion would add losses.

¢` AirCp = 1007 'J.kg-1.K-1' `

¢` AirRise = 100 K `

¢` AirDensity = 1.164398101419 'kg/m3' `

¢` AirPressureDrop = 500 Pa `

¢` FanEfficiency = 0.65 `

¢%%` AirFlow = AirCoolerDuty / (AirCp * AirRise) = 〔96〕 'kg/s' `

¢%%` FanPower = AirFlow / AirDensity * AirPressureDrop / FanEfficiency = 〔63.4〕 kW `

¢%%` RemainingPower = AvailablePower - FanPower = 〔203〕 kW `

The remaining approximately 203 kW per 10 MW heat input is an allowance for
unspecified loads, not proof that the whole cooling system is self-powered. In
particular, the existing salt-circulation pumps are not included.

## Sensitivity — external real-steam calculations

+---------------------------------+----------------+-----------------------------------+
| Compressor / turbine efficiency | Pressure ratio | Available shaft kW per 10 MW heat |
|                                 |                | input                             |
+=================================+================+===================================+
| 80% / 85%                       | 1.5            | \-143                             |
+---------------------------------+----------------+-----------------------------------+
| 80% / 85%                       | 2.0            | \-14                              |
+---------------------------------+----------------+-----------------------------------+
| 80% / 85%                       | 2.5            | 120                               |
+---------------------------------+----------------+-----------------------------------+
| 80% / 85%                       | 3.0            | Wet inlet required — rejected     |
+---------------------------------+----------------+-----------------------------------+
| 85% / 88%                       | 1.5            | 35                                |
+---------------------------------+----------------+-----------------------------------+
| 85% / 88%                       | 2.0            | 267                               |
+---------------------------------+----------------+-----------------------------------+
| 85% / 88%                       | 2.5            | 466                               |
+---------------------------------+----------------+-----------------------------------+
| 85% / 88%                       | 3.0            | Wet inlet required — rejected     |
+---------------------------------+----------------+-----------------------------------+
| 85% / 90%                       | 1.5            | 81                                |
+---------------------------------+----------------+-----------------------------------+
| 85% / 90%                       | 2.0            | 345                               |
+---------------------------------+----------------+-----------------------------------+
| 85% / 90%                       | 2.5            | 568                               |
+---------------------------------+----------------+-----------------------------------+
| 85% / 90%                       | 3.0            | Wet inlet required — rejected     |
+---------------------------------+----------------+-----------------------------------+
{.grid colWidths="240 120 120"}

Available shaft power is before fan and salt-pump loads. These are different
fixed-temperature trial designs, not performance along one machine map. At
ratio 2.5 and the base efficiencies, positive margin increases but
compressor-inlet superheat decreases. Ratio 3 at 5 bar suction requires a wet
inlet for the specified generator inlet temperature and is rejected.

| Pressure loss in each exchanger | Available shaft kW per 10 MW |
|---------------------------------|------------------------------|
| 0%                              | 464                          |
| 2%                              | 267                          |
| 5%                              | \-40                         |
{.grid colWidths="240 120"}

At 5% loss in each exchanger, the base 2:1 trial cannot drive its own
compressor. Low pressure loss is a key feasibility condition.

## Requested 8:1 comparison

At the same 5 bar suction pressure, 8:1 compression cannot retain a 287°C
compressor outlet with dry steam at the inlet. A vapor-only trial can retain
the generator temperatures by reducing suction pressure to 0.05 bar absolute (5
kPa), with compressor discharge at 0.40 bar. Both sides of this trial are below
atmospheric pressure; vacuum integrity and air ingress become additional
requirements.

+-------------------------------------+-----------+------------------+
| Quantity, per 10 MW heat input      | 2:1 trial | 8:1 vacuum trial |
+=====================================+===========+==================+
| Compressor inlet pressure (bar      | 5         | 0.05             |
| absolute)                           |           |                  |
+-------------------------------------+-----------+------------------+
| Compressor discharge pressure (bar  | 10        | 0.4              |
| absolute)                           |           |                  |
+-------------------------------------+-----------+------------------+
| Compressor inlet temperature (°C)   | 192       | 44.8             |
+-------------------------------------+-----------+------------------+
| Generator inlet temperature (°C)    | 287       | 287              |
+-------------------------------------+-----------+------------------+
| Generator outlet temperature (°C)   | 557       | 557              |
+-------------------------------------+-----------+------------------+
| Turbine outlet temperature (°C)     | 460       | 291              |
+-------------------------------------+-----------+------------------+
| Steam flow (kg/s)                   | 17.2      | 17.8             |
+-------------------------------------+-----------+------------------+
| Compressor inlet volume flow (m³/s) | 7.19      | 521              |
+-------------------------------------+-----------+------------------+
| Turbine power (MW)                  | 3.52      | 9.85             |
+-------------------------------------+-----------+------------------+
| Compressor power (MW)               | 3.18      | 8.3              |
+-------------------------------------+-----------+------------------+
| Available shaft power (MW)          | 0.267     | 1.36             |
+-------------------------------------+-----------+------------------+
| Steam-to-air cooler duty (MW)       | 9.66      | 8.45             |
+-------------------------------------+-----------+------------------+
{.grid colWidths="240 120 120"}

Efficiencies and fractional pressure-loss assumptions are the same in both
trials. The 8:1 case gives more shaft surplus but about 72 times the
compressor-inlet volume flow. Its air-cooler outlet is only about 45°C, with 12
K superheat above saturation and about 15 K approach to the assumed 30°C
incoming air. Hot-weather performance, vacuum operation and very large passages
are unverified. A 2% cooler pressure allowance is only about 102 Pa in this
vacuum trial; that must not be assumed achievable in the existing equipment.

### Editable scaling for the 8:1 trial

¢` hEightA = 2583.407521083 'kJ/kg' `

¢` hEightB = 3049.692400319 'kJ/kg' `

¢` hEightC = 3611.705900276 'kJ/kg' `

¢` hEightD = 3058.02794104 'kJ/kg' `

¢%%` EightFlow = HeatInput / (hEightC - hEightB) = 〔17.8〕 'kg/s' `

¢%%` EightTurbinePower = EightFlow * (hEightC - hEightD) = 〔9.85〕 MW `

¢%%` EightCompressorPower = EightFlow * (hEightB - hEightA) = 〔8.3〕 MW `

¢%%` EightAvailable = ShaftEfficiency * EightTurbinePower - EightCompressorPower
= 〔1,358〕 kW `

¢%%` EightCoolerDuty = EightFlow * (hEightD - hEightA) = 〔8.45〕 MW `

¢` EightDensity = 0.0341365384984 'kg/m3' `

¢%%` EightVolumeFlow = EightFlow / EightDensity = 〔521〕 'm3/s' `

¢%%` EightFanPower = EightCoolerDuty / (AirCp * AirRise) / AirDensity *
AirPressureDrop / FanEfficiency = 〔55.4〕 kW `

¢%%` EightRemaining = EightAvailable - EightFanPower = 〔1,303〕 kW `

## Normal 24 MPa supply and throttling

The owner notes that normal 24 MPa steam provides ample pressure for a
lower-pressure engine. Throttling can charge or feed a lower-pressure system,
but continuously returning steam to a generator held at 24 MPa still requires
recompression to that pressure, or condensation and liquid pumping. The
isolated low-pressure closed cycles above do not include a continuously
supplied 24 MPa branch. A one-time high-pressure charge also does not supply
continuing shaft work.

An adiabatic throttle approximately conserves enthalpy rather than temperature.
With real steam at 24 MPa and 557°C, throttling to 1 MPa produces about 451°C
steam; throttling to 0.04 MPa produces about 445°C. Thus a continuously
throttled supply cannot be represented by simply retaining 557°C at the lower
pressure without adding heat. These throttle results are separate from the
lower-pressure heated-loop trials. Saturation/phase conditions at 24 MPa and
the current 287°C generator inlet also prevent treating the normal feedwater
state as dry steam.

## Checks, sources and unresolved work

Python verifies energy closure, nonnegative machine entropy production, inverse
compressor closure, dry sampled paths and linear heat-duty scaling. HEOS state
enthalpies agree with an IF97 property cross-check within 0.003%. Hurmet
independently checks the power and fan arithmetic and duty/fan-loss
sensitivities. Detailed inputs and results are in [the JSON report][3].

The UM report _Core Design Evolution of Wielenga Innovation Salt Tank Reactor_,
November 15, 2025, section 3.3.1 and Table 3 (printed pages 21–22; PDF pages
37–38), gives 675 K (approximately 402°C) for the selected NaCl–KCl–MgCl2
coolant melting point. The inherited generator worksheet instead contains 674
K; the one-degree difference is immaterial for this screen. The \[local UM
report](\</Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Papers and
Presentations/UMReport/Evolution_of_WISSR\_design 2.pdf>) remains the reference
for the approximately 402°C value. No cutoff temperature is selected here.

*   [CoolProp water property formulation][4].
*   [NASA compressor/turbine matching][5].
*   Generator heat-transfer area, vapor distribution, salt flow, tube-wall
    temperature and freezing protection are not solved. At this lower duty the
    original full-power salt temperature drop must not simply be reused.
*   The 2% pressure-loss assumptions and component efficiencies require checking
    against generator pressure drop and practical machine maps.
*   Air-cooler area, salt-pump power, startup, restart, steam inventory, turndown
    and shutdown response remain open. A temperature cutoff is a control
    concept, not yet a demonstrated freeze-protection function.
*   No change to the main Rankine cycle, reactor cooling architecture or Blender
    model is adopted by this calculation.

Reproduce with the existing power-cycle requirements: `python
brayton_cooler.py`, then `python publish_brayton_cooler.py`, then
`HURMET_ENGINE=/path/to/hurmet.cjs TEMML_ENGINE=/path/to/temml.cjs node
check_brayton_hurmet.cjs`. Changing only HeatInput or the air-fan assumptions in
Hurmet recalculates the scaling at the imported cycle states.

[1]: ../steam-generator/Generator%20sizing%20-%20Hurmet.md

[2]: brayton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_cooler.py

[3]: brayton-cooler-results.json

[4]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[5]: https://www.grc.nasa.gov/WWW/K-12/BGP/ctmatch.html

[6]: brayton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_cooler.py

[7]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[8]: brayton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_cooler.py

[9]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[10]: brayton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_cooler.py

[11]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[12]: brayton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_cooler.py

[13]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[14]: brayton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_cooler.py

[15]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[16]: brayton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_cooler.py

[17]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[18]: brayton\\\\\\\\\\\\\\\_cooler.py

[19]: https://coolprop.org/fluid\\\\\\\\\\\\\\\_properties/fluids/Water.html

[20]: brayton\\\\\\\_cooler.py

[21]: https://coolprop.org/fluid\\\\\\\_properties/fluids/Water.html

[22]: brayton\\\_cooler.py

[23]: https://coolprop.org/fluid\\\_properties/fluids/Water.html

[24]: brayton\_cooler.py

[25]: https://coolprop.org/fluid\_properties/fluids/Water.html
