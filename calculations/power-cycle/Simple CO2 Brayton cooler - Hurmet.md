---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: undefined
saveDate: 2026-10-13
---------------

# Simple supercritical CO₂ loop — compact heat-removal screen

13 October 2026. Investigate compact heat removal, rather than maximizing
electrical efficiency. **The emergency air passages built into the steam
generators are reserved for the student team's educational calculation and are
not analyzed here.** This screen concerns a separate closed CO₂ working-fluid
loop and its own outdoor heat-rejection exchanger.

Flow is **CO₂ compressor → salt-to-CO₂ heater → turbine → separate dry cooler →
compressor**. The turbine drives the compressor and an alternator serving the
salt pump and cooler fan. There is no recuperator, recompressor or intercooler.
Omitting recuperators avoids components used primarily to improve power-cycle
efficiency; it does not remove the requirement to reject heat to the
environment.

Use CoolProp 7.2.0 HEOS::CO₂ and the [Span–Wagner property model][1]. CO₂
critical conditions are about 31°C and 7.38 MPa. All four state points here
remain above both. [DOE describes high working-fluid density as a source of
compact turbomachinery][2]; that does not establish complete-system footprint.

## Common assumptions

Low/high compressor pressure: **10/20 MPa (100/200 bar)**. Turbine inlet: 830 K
(556.85°C). Compressor/turbine efficiencies: 85%/88%; shaft transfer 98%;
alternator 95%. Pressure loss is 2% through each exchanger. Salt heat transfer
is 30 MW per train, a comparison duty rather than a specified emergency load.

The outdoor cooler retains 30→130°C air, 500 Pa total air loss, 65% fan
efficiency and 96% motor efficiency. Salt-pump electricity remains 130 kW from
the earlier 30 MW case with a 10 K salt drop and generator pressure loss plus
50%. There is no credit for heat rejection through the students'
steam-generator air passages. Constant machine efficiencies and exchanger
losses are provisional, not selected equipment performance.

## Compare warm and near-critical compressor inlets

+---------------------------+-----------------------+------------------------+-----------------------+
| Per 30 MW heat input      | Match existing heater | 100°C compressor inlet | 40°C compressor inlet |
|                           | inlet                 |                        |                       |
+===========================+=======================+========================+=======================+
| Compressor inlet, °C      | 204.3                 | 100                    | 40                    |
+---------------------------+-----------------------+------------------------+-----------------------+
| Heater inlet, °C          | 286.9                 | 168.4                  | 62.35                 |
+---------------------------+-----------------------+------------------------+-----------------------+
| Compressor inlet density, | 120.6                 | 188.6                  | 628.6                 |
| kg/m³                     |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
| CO₂ mass flow, kg/s       | 90.12                 | 61                     | 42.05                 |
+---------------------------+-----------------------+------------------------+-----------------------+
| Compressor inlet volume,  | 0.7474                | 0.3235                 | 0.06689               |
| m³/s                      |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
| Hot low-pressure return   | 1.265                 | 0.8563                 | 0.5902                |
| volume, m³/s              |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
| Compressor shaft demand,  | 6.636                 | 2.927                  | 0.7309                |
| MW                        |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
| Turbine shaft power, MW   | 7.826                 | 5.297                  | 3.651                 |
+---------------------------+-----------------------+------------------------+-----------------------+
| Available shaft power, MW | 1.033                 | 2.264                  | 2.847                 |
+---------------------------+-----------------------+------------------------+-----------------------+
| Electrical margin after   | 0.6546                | 1.832                  | 2.39                  |
| fan and salt pump, MW     |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
| Heat to separate air      | 28.81                 | 27.63                  | 27.08                 |
| cooler, MW                |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
| Air cooler face at 3 m/s, | 81.9                  | 78.55                  | 76.98                 |
| m²                        |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
| Ideal-counterflow cooler  | 114.3                 | 164.4                  | 770.2                 |
| UA, kW/K                  |                       |                        |                       |
+---------------------------+-----------------------+------------------------+-----------------------+
{.grid colWidths="250 125 125 125"}

The matched-temperature case holds the prior 287/557°C heater endpoints and
obtains approximately 204°C compressor inlet. It gives 0.75 m³/s inlet volume
and 1.27 m³/s hot return, compared with 10.7/17.8 m³/s for the earlier 10→40
bar nitrogen candidate and 21.6/34.2 m³/s for steam. At an illustrative 30 m/s
velocity, the CO₂ equivalent flow bores are about 0.18 and 0.23 m. These
exclude pressure wall, insulation and fittings; they are not turbine or
compressor diameters and do not validate a pipe design at 20 MPa.

The cold 40°C case makes the compressor exceptionally small in flow terms, but
requires about **770 kW/K of cooler UA**, versus **114 kW/K** in the warm
matched case. The sharp near-critical property variation creates a small
internal temperature approach (about 9 K for this air profile). Chasing maximum
density or efficiency can therefore worsen the external heat-rejection
requirement. The 100°C inlet is an intermediate trial with a 168°C heater
inlet; it changes the salt-side cold-end thermal conditions and requires a
fresh local wall/freezing check. No such check is inferred from low overall duty.

## How much of the compactness comes from pressure?

The original nitrogen comparison used 10–40 **bar**, whereas this CO₂ loop uses
100–200 **bar**. It would be misleading to attribute the entire volume
reduction to the choice of CO₂. A supplementary nitrogen case at the same
100–200 bar and 287/557°C heater endpoints gives approximately **1.35 m³/s**
compressor inlet, **12.46 MW** compressor duty and **0.375 MW** electrical
margin after the same fan/pump allowances. CO₂ gives 0.75 m³/s, 6.64 MW and
0.655 MW respectively. It still has an advantage in this screen, but the
same-pressure comparison is much less dramatic than comparison with
lower-pressure nitrogen.

## Compact machinery does not mean a tiny heat sink

The warm CO₂ case still sends about **28.8 MW** to the air cooler, requiring
about **246 m³/s** of cold air under the retained 100 K air-rise assumption.
The approximately **82 m² airflow face** is almost unchanged from the steam
case. This is a flow-area screen, not a thermal exchanger rating or installed
footprint. A selected gas-side coefficient, fin area, core depth, manifolds and
fan/duct arrangement must satisfy both heat transfer and the pressure-loss
budget.

The smaller process-flow passages and lower compressor shaft power support
investigating a smaller machinery package; they do not justify scaling the
earlier machinery box directly by volume flow or claiming a vendor footprint.
Pressure containment, bearings, seals, rotational speed and stage arrangement
remain unselected. The earlier 500–600 m² layout reservations should not be
copied to CO₂ as established dimensions.

Higher air outlet temperature could reduce required airflow, but that option
also exists for steam and nitrogen. It would change cooler driving temperatures
and discharge constraints; it is not a unique benefit of CO₂. Lower power-cycle
efficiency is acceptable if enough work remains for auxiliaries, but it also
means most salt heat must be rejected through the cooler rather than exported
electrically.

## Integration and operating scope

A simple high-pressure loop is the candidate being screened, not the more
complex recuperated cycles used to maximize generation efficiency. The
salt-to-CO₂ heater may reuse existing generator passages only if heat transfer,
pressure loss, materials and isolation/changeover are verified; otherwise a
dedicated heater is another unsized component. CO₂ suitability and a failed
separating-boundary response require review. A nominal pressure below the
normal steam operating pressure alone does not establish compatibility.

Warm compression avoids making the normal operating point depend on cooling
within a few degrees of the critical temperature. Charge/inventory control,
startup drive and pressure containment remain required. Colder shutdown
conditions can enter other fluid regimes. Maintaining the modeled hot
temperature as reactor temperature falls is not assumed to be an established
operating map. At the same compressor-inlet temperature, reducing
compressor/turbine efficiencies to 80%/85% leaves only about **12 kW** after
the modeled fan and salt pump, before controls or other loads. The nominal
matched case therefore has limited robustness to machine performance; positive
nominal margin is not a reliability demonstration. The student
emergency-air-passage study remains an independent alternative.

## Hurmet verification of the matched-temperature case

¢` HeatDuty = 30 MW `

¢` ShaftEfficiency = 0.98 `

¢` GeneratorEfficiency = 0.95 `

¢` FanEfficiency = 0.65 `

¢` MotorEfficiency = 0.96 `

¢` AirRise = 100 K `

¢` AirHeatCapacity = 1007 J.kg-1.K-1 `

¢` AirDensity = 1.1643981014192 kg/m3 `

¢` AirPressureDrop = 500 Pa `

¢` FaceVelocity = 3 m/s `

¢` PumpPower = 129.99027717071 kW `

¢` InletDensity = 120.57348528401 kg/m3 `

¢` HotDensity = 71.239398069111 kg/m3 `

¢` HOne = 637391.75279781 J/kg `

¢` HTwo = 711026.03037939 J/kg `

¢` HThree = 1043911.7401561 J/kg `

¢` HFour = 957077.43541676 J/kg `

¢??` MassFlow = HeatDuty / (HThree - HTwo) = 〔90.1210208756727〕 kg/s `

¢??` InletFlow = MassFlow / InletDensity = 〔0.747436475468825〕 m3/s `

¢??` HotFlow = MassFlow / HotDensity = 〔1.26504467076272〕 m3/s `

¢??` CompressorPower = MassFlow * (HTwo - HOne) = 〔6.63599626709465〕 MW `

¢??` TurbinePower = MassFlow * (HThree - HFour) = 〔7.82559619013858〕 MW `

¢??` AvailableShaft = ShaftEfficiency * TurbinePower - CompressorPower =
〔1.03308799924116〕 MW `

¢??` CoolerHeat = MassFlow * (HFour - HOne) = 〔28.8104000769561〕 MW `

¢??` EnergyResidual = HeatDuty - CoolerHeat - TurbinePower + CompressorPower =
〔0〕 MW `

¢??` AirFlow = CoolerHeat / (AirHeatCapacity * AirRise * AirDensity) =
〔245.70745295682〕 m3/s `

¢??` FaceArea = AirFlow / FaceVelocity = 〔81.9024843189399〕 m2 `

¢??` FanPower = AirFlow * AirPressureDrop / (FanEfficiency * MotorEfficiency) =
〔196.880971920529〕 kW `

¢??` RemainingElectricity = GeneratorEfficiency * AvailableShaft - FanPower -
PumpPower = 〔654.562350187867〕 kW `

Real-fluid states and integrated counterflow UA are imported from Python; Hurmet
independently checks power, heat and flow. Changing state
temperatures/pressures requires a Python rerun. Changing heat duty alone scales
fixed-state machinery, while the pump input remains the specific 30 MW estimate
and must also be recalculated for a different salt duty. Summary tables are
snapshots.

Run `co2_brayton.py` in the existing CoolProp environment, then
`check_co2_brayton.cjs` with Hurmet/Temml configured. JSON records the
matched-temperature solve, pressure/temperature states, source hashes,
energy/entropy checks, duty scaling and cooler-integration convergence. Twelve
Hurmet numerical checks, save/reopen and air-pressure sensitivity are verified.
These establish numerical consistency, not selected hardware or qualified
emergency cooling.

[1]: https://coolprop.org/fluid\\\_properties/fluids/CarbonDioxide.html

[2]: https://www.energy.gov/sco2-rd-focus-areas

[3]: https://coolprop.org/fluid\_properties/fluids/CarbonDioxide.html
