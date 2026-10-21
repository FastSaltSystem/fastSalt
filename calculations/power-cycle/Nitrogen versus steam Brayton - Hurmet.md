---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Nitrogen versus steam — closed Brayton cooler

¢` format = "h3" `

13 October 2026. Exploratory comparison with the preserved [steam cycle][1] and
[fan/pump balance][2]. No working fluid or cooling architecture has been
adopted.

Nitrogen properties are calculated with CoolProp 7.2.0 HEOS using the [Span et
al. nitrogen equation of state][3]. Water results are imported from the earlier
HEOS water calculation. All quoted power figures are calculations, not
manufacturer performance. The same compressor/turbine efficiencies of 85%/88%,
98% shaft transfer and 2% pressure loss across each exchanger are assumed. No
recuperator or compressor intercooling is included.

## Like-for-like temperature comparison

Retain 560 K (286.85°C) heater inlet and 830 K (556.85°C) turbine inlet. Solve
compressor-inlet temperature for each pressure ratio. Each case takes 10 MW
heat from the salt. The first two cases also use identical 5→10 bar absolute
compression pressures; the 4:1 nitrogen candidate uses 10→40 bar. Actual heater
outlet/turbine inlet pressure is 2% below compressor discharge.

Air enters at 30°C and leaves at 130°C, with 500 Pa total air-system loss, 65%
fan efficiency, 96% motor efficiency and 95% alternator efficiency. These are
the same provisional electric-fan assumptions as the preceding balanced
calculation.

+---------------------------+------------+---------------+---------------+
| Per 10 MW heat input      | Steam, 2:1 | Nitrogen, 2:1 | Nitrogen, 4:1 |
+===========================+============+===============+===============+
| Compressor pressures, bar | 5→10       | 5→10          | 10→40         |
| absolute                  |            |               |               |
+---------------------------+------------+---------------+---------------+
| Compressor inlet / cooler | 192.1      | 173.7         | 84.23         |
| outlet, °C                |            |               |               |
+---------------------------+------------+---------------+---------------+
| Turbine outlet / cooler   | 460.2      | 440.3         | 334.5         |
| inlet, °C                 |            |               |               |
+---------------------------+------------+---------------+---------------+
| Working-fluid mass flow,  | 17.24      | 33.69         | 33.48         |
| kg/s                      |            |               |               |
+---------------------------+------------+---------------+---------------+
| Compressor inlet volume,  | 7.191      | 8.951         | 3.557         |
| m³/s                      |            |               |               |
+---------------------------+------------+---------------+---------------+
| Surplus shaft power after | 266.8      | 265.8         | 944.3         |
| compressor, kW            |            |               |               |
+---------------------------+------------+---------------+---------------+
| Air-cooler heat           | 9.663      | 9.646         | 8.89          |
| rejection, MW             |            |               |               |
+---------------------------+------------+---------------+---------------+
| Electricity after air     | 187.5      | 186.6         | 836.3         |
| fan, before salt pump, kW |            |               |               |
+---------------------------+------------+---------------+---------------+
| Required                  | 40.91      | 44.36         | 78.19         |
| ideal-counterflow UA,     |            |               |               |
| kW/K                      |            |               |               |
+---------------------------+------------+---------------+---------------+
{.grid colWidths="250 125 125 125"}

At 2:1 the power balances are almost identical. Nitrogen needs about twice the
mass flow and about 25% more compressor-inlet volume at the same pressures.
Thus simply substituting nitrogen does not inherently make the machinery
smaller or increase the surplus.

Nitrogen's advantage is freedom to choose loop pressure and compressor-inlet
temperature without steam condensation. Nitrogen's critical temperature is
about 126 K, far below these cycle temperatures; no liquid-vapor transition
occurs along these operating paths. At 4:1 the dry pressurized nitrogen trial
gives more power with a readily air-coolable 84°C compressor inlet. The
improvement combines a different pressure ratio and cold-end temperature; it is
not an intrinsic factor-of-3.5 gain at identical cycle states.

## Absolute-pressure effect for 4:1 nitrogen

| Compressor pressures, bar absolute | Inlet volume per 10 MW, m³/s | Surplus shaft power, kW |
|------------------------------------|------------------------------|-------------------------|
| 5→20                               | 7.144                        | 940.2                   |
| 10→40                              | 3.557                        | 944.3                   |
| 20→80                              | 1.766                        | 949.6                   |
{.grid colWidths="250 125 125"}

Raising charge pressure approximately reduces gas volume in inverse proportion
while changing the calculated surplus only slightly. This is a way to reduce
flow-passage sizes, with pressure containment and sealing tradeoffs; volume
alone does not determine a compressor or turbine envelope.

## Why 8:1 needs a different comparison

At 10→80 bar and the same 287°C heater inlet, nitrogen would have to enter the
compressor at **13.5°C**. This is below 30°C ambient and cannot be achieved by
the proposed air cooler. Its formal positive shaft balance is rejected as an
air-cooled operating case.

If compressor inlet is instead fixed at **45°C**, the 8:1 nitrogen compressor
discharges at **346.1°C**. It can then absorb heat up to 556.85°C, but requires
42.39 kg/s per 10 MW and gives about **750 kW shaft surplus**, less than the
4:1 candidate's 944 kW. Its compressor inlet volume is about 4.00 m³/s and
required ideal-counterflow cooler UA about 182 kW/K. This warmer-inlet case
changes the generator temperature range and does not establish an optimum
ratio. The preserved steam 8:1 trial at 5 kPa suction needs about 521 m³/s per
10 MW and has its own close cold-end approach to ambient.

## Air cooler and heat-exchanger consequences

The 4:1 nitrogen trial requires about **78.2 kW/K of counterflow UA per 10 MW**,
versus **40.9 kW/K** for steam at 2:1. Although nitrogen rejects slightly less
heat, its lower cooler outlet temperature reduces the temperature driving
force. These values integrate real-fluid temperature against heat transfer,
with linear pressure change and the assumed air heat capacity. All sampled
counterflow temperature differences are positive for accepted cases. They are
ideal-counterflow conductances, not selected surface areas or a verified
pressure-drop design. Real flow arrangement, fouling and gas-side heat-transfer
coefficients may increase the required area.

The existing generator also needs gas-side heat-transfer and pressure-drop
checking for nitrogen; its water/steam service calculation and pressure rating
do not establish nitrogen duty. A permanent nitrogen auxiliary loop would use
its own gas inventory. Sharing the current steam-generator passages would
require a defined water removal, purge, isolation and changeover arrangement; a
separate salt-to-nitrogen exchanger is an alternative to assess, not selected
here. Nitrogen avoids steam condensation management, but startup still needs an
initial drive source and salt freeze protection remains necessary.

## A 30 MW-per-leg nitrogen trial

At 4:1 and 10→40 bar, scaling to 30 MW gives about **2.69 MW electrical surplus
after the compressor**, with **182 kW** for the air fan and the previously
calculated **130 kW** salt-pump demand (10 K salt drop; generator loss plus
50%). Approximately **2.38 MW remains**, versus 0.432 MW in the steam 2:1 case.
Nitrogen circulation is about 100.45 kg/s and compressor-inlet volume 10.67
m³/s. The air cooler rejects 26.67 MW; electricity and machinery losses account
for the balance and need their own destinations. This is machinery scaled to 30
MW, not the same 10 MW machine operated at triple capacity.

Two sensitivity checks at 4:1 retain positive surplus: lowering
compressor/turbine efficiency to 80%/85% gives about 389 kW shaft surplus per
10 MW, and increasing each exchanger pressure loss to 5% gives about 631 kW.
These are separate tests. Actual maps, combined adverse conditions and cooldown
temperatures are not validated.

## Hurmet checks for the nitrogen 4:1 case

Thermodynamic states and the integrated cooler UA are imported from Python.
Hurmet recalculates the cycle power and heat balance, fan demand and the 30 MW
fan/pump margin. Changing pressure, temperature or machine efficiency requires
rerunning the real-fluid solver; changing heat duty here only scales
fixed-state machinery.

¢` HeatDuty = 10 MW `

¢` ShaftEfficiency = 0.98 `

¢` GeneratorEfficiency = 0.95 `

¢` FanEfficiency = 0.65 `

¢` MotorEfficiency = 0.96 `

¢` AirDensity = 1.1643981014192 kg/m3 `

¢` AirHeatCapacity = 1007 J.kg-1.K-1 `

¢` AirRise = 100 K `

¢` AirPressureDrop = 500 Pa `

¢` PumpAtThirtyMW = 129.99027717071 kW `

¢` HOne = 369.68496316802 kJ/kg `

¢` HTwo = 583.66620690323 kJ/kg `

¢` HThree = 882.33377409443 kJ/kg `

¢` HFour = 635.20676904002 kJ/kg `

¢%%` HeatPerMass = HThree - HTwo = 〔298,668〕 J/kg `

¢%%` MassFlow = HeatDuty / HeatPerMass = 〔33.5〕 kg/s `

¢%%` TurbinePower = MassFlow * (HThree - HFour) = 〔8,274〕 kW `

¢%%` CompressorPower = MassFlow * (HTwo - HOne) = 〔7,165〕 kW `

¢%%` SurplusPower = ShaftEfficiency * TurbinePower - CompressorPower = 〔944〕 kW `

¢%%` CoolerHeat = MassFlow * (HFour - HOne) = 〔8.89〕 MW `

¢%%` EnergyResidual = HeatDuty - CoolerHeat - TurbinePower + CompressorPower =
〔0〕 kW `

¢%%` AirFlow = CoolerHeat / (AirHeatCapacity * AirRise * AirDensity) = 〔75.8〕
m3/s `

¢%%` FanPower = AirFlow * AirPressureDrop / (FanEfficiency * MotorEfficiency) =
〔60.8〕 kW `

¢%%` ElectricAfterFan = GeneratorEfficiency * SurplusPower - FanPower = 〔836〕 kW `

¢%%` MarginAtThirtyMW = 3 * ElectricAfterFan - PumpAtThirtyMW = 〔2,379〕 kW `

The last formula is specifically the 30 MW case when the normalization above is
10 MW; the fixed salt-pump input is not a pump scaling law. Summary tables are
imported snapshots and do not update automatically in Hurmet.

## Reproduction

Run `nitrogen_brayton.py` with the project CoolProp environment, then `python
publish_nitrogen_brayton.py`, and `node check_nitrogen_brayton.cjs` with the
existing Hurmet/Temml engine paths. JSON preserves source hashes, all state
points, air approaches, sensitivity cases, energy/entropy and duty-scaling
checks. Hurmet verifies eleven named results after save/reopen and checks
fan-pressure sensitivity. These checks establish numerical consistency, not a
qualified cooling-system design.

[1]: Steam%20Brayton%20cooler%20-%20Hurmet.md

[2]: Brayton%20fan%20and%20salt%20pump%20balance%20-%20Hurmet.md

[3]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[4]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[5]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[6]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[7]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[8]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[9]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[10]: https://coolprop.org/fluid\\\\\\\\\\\\\\\_properties/fluids/Nitrogen.html

[11]: https://coolprop.org/fluid\\\\\\\_properties/fluids/Nitrogen.html

[12]: https://coolprop.org/fluid\\\_properties/fluids/Nitrogen.html

[13]: https://coolprop.org/fluid\_properties/fluids/Nitrogen.html
