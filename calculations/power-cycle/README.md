# Preliminary Rankine-cycle design

11 October 2026. This is the first heat-balance case for the Fast Salt steam power
plant, following Thomas Wielenga's supplied [system diagram](</Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Steam Generator/graphics/Diagram.pdf>).
The owner confirmed main-steam reheat as drawn and a provisional water-cooled
condenser at 5 kPa absolute. The fuel-preparation building is outside this scope.

Start with the [Hurmet worksheet](Rankine%20cycle%20-%20Hurmet.md), the
[state table](rankine-states.csv) and [full calculation results](rankine-results.json).
No Blender equipment has been resized from this preliminary calculation.

## Auxiliary Brayton cooler overview

The four-case comparison is preserved as **[RS-008, Revision A - 19 October 2026](../../research/auxiliary-brayton-cooling/README.md)**, with a PDF report and an archived source package.

Start with the **[four-case overview](brayton-overview.md)** for steam, nitrogen, open air and supercritical CO₂ at 30 MW per train. It consolidates the saved results, power margins, flow-volume comparisons and historical pump-loss basis. [Local browser view](preview/brayton-overview.html) (generated; not included in Git).

## Auxiliary steam Brayton cooler — exploratory screen

12 October 2026. [Steam Brayton cooler — Hurmet](Steam%20Brayton%20cooler%20-%20Hurmet.md) tests a separate non-condensing auxiliary mode using the current generator temperature endpoints, 560/830 K. The provisional 5-to-10 bar absolute trial with 85% compressor / 88% turbine efficiencies, 98% shaft transfer and 2% pressure loss per exchanger yields about 267 kW available shaft power per 10 MW heat input. An illustrative 63 kW air-fan allowance leaves 203 kW before salt pumps and other auxiliaries. Lower machine efficiencies or larger pressure losses can remove the margin.

The requested **8:1** comparison retains those temperature endpoints only after lowering pressure enough to keep the compressor inlet dry. A 5 kPa suction / 40 kPa discharge trial gives 1.36 MW surplus per 10 MW heat input, but approximately 521 m³/s inlet volume flow versus 7.19 m³/s for 2:1. Throttling a continuous 24 MPa supply is analyzed separately: it lowers temperature and does not eliminate recompression to the generator pressure.

This is an exploratory calculation, not an adopted cooling system or a revision to the main Rankine cycle. Existing-generator operation at lower pressure, local salt freezing, actual duties, machinery maps and startup remain unverified. Salt-circulation power now has the preliminary estimate below. [Python and full results](brayton-cooler-results.json) include pressure-ratio and loss sensitivities, dry-path checks and an IF97 property comparison. Reproduce with `python brayton_cooler.py`, `python publish_brayton_cooler.py`, then `node check_brayton_hurmet.cjs` using the same Hurmet engine environment below.

## Brayton-powered salt circulation — preliminary estimate

[Brayton-driven salt pump — Hurmet](Brayton-driven%20salt%20pump%20-%20Hurmet.md) applies the original generator friction correlation at reduced flow, with 50% additional loop loss. Using the surplus from a 10 MW cooler gives 2.084 m³/s at 71.23 kPa for 2:1, or 4.099 m³/s at 231.87 kPa for the vacuum 8:1 trial, per leg. Provisional alternator/motor/pump efficiencies are 95%/96%/80%. The worksheet distinguishes transport at a 65 K salt drop from actual cooler duty, includes heat returned by pumping, and compares sharing a single 10 MW trial across three legs. It is not a machinery selection or an adopted cooling design.

Run `python brayton_salt_pump.py`, then `node check_brayton_salt_pump.cjs` with the Hurmet engine environment below. Python imports the preceding cycle results and solves flow roots; Hurmet independently verifies hydraulics and energy/power balances. Thirty-two numerical comparisons, save/reopen, and two input sensitivities are checked. Recompute roots in Python after physical input changes.

## Balanced auxiliary fan and salt-pump demand — 13 October 2026

[Fan and salt-pump balance — Hurmet](Brayton%20fan%20and%20salt%20pump%20balance%20-%20Hurmet.md) sizes both electric loads against the cycle surplus before the fan deduction. At 30 MW per leg, the 2:1 case produces 760.5 kW electrical surplus, needs 130.0 kW for salt circulation and 198.1 kW for air flow, and retains 432.4 kW. A 50 MW case is also positive. These assume a chosen 10 K salt drop, 500 Pa air-system loss, 30→130°C air and machinery/coolers scaled to the heat duty. The air-temperature/pressure sensitivity includes a failed power balance. The 8:1 comparison retains its vacuum-volume limitation.

The 69.6 MW zero-margin result is a conditional mathematical boundary, not a selected or verified cooling capacity. Source hashes and results are in `brayton-fan-pump-results.json`. Reproduce with `python brayton_fan_pump_balance.py` and `node check_brayton_fan_pump.cjs`. Seventeen Hurmet numerical checks, save/reopen, altered heat duty, fan-pressure sensitivity and a deficit case pass.

## Nitrogen alternative — 13 October 2026

[Nitrogen versus steam — Hurmet](Nitrogen%20versus%20steam%20Brayton%20-%20Hurmet.md) compares CoolProp real-nitrogen cases with the preserved steam results. Equal-pressure 2:1 cases give nearly equal surplus. A 4:1, 10→40 bar nitrogen trial gives 944 kW shaft surplus per 10 MW, 3.56 m³/s compressor-inlet volume and 84°C cooler outlet; its ideal-counterflow cooler UA is approximately 78 versus 41 kW/K for steam at 2:1. Fixed-endpoint 8:1 nitrogen cannot reject heat solely to 30°C air; a 45°C compressor-inlet variant raises heater inlet to 346°C. Machinery/pressure sensitivities and the 30 MW fan/pump budget are included.

Reproduce with `nitrogen_brayton.py` in the CoolProp environment, `publish_nitrogen_brayton.py`, and `check_nitrogen_brayton.cjs` with Hurmet/Temml configured. Python checks energy, entropy, scaling, an ideal-gas density limit and the rejected air-cooling case. Hurmet passes eleven numerical comparisons, save/reopen and fan-pressure sensitivity. No working fluid or shared-generator changeover arrangement has been selected.

## Open-air alternative — 13 October 2026

[Open-air Brayton cooler — Hurmet](Open-air%20Brayton%20cooler%20-%20Hurmet.md) compares ratios 2, 4, 8 and a 6.832:1 case matching the preceding heater endpoints. The matched case uses 30°C atmospheric intake, 500 Pa intake loss, 2% heater loss and 1 kPa exhaust backpressure; no cooler fan is deducted. It produces 1.484 MW shaft surplus per 10 MW, with roughly 30 m³/s inlet and 53 m³/s atmospheric exhaust. At 30 MW the salt-pump-adjusted electrical margin is 4.10 MW. These are scalable operating-point estimates, not equipment ratings or an approved discharge arrangement.

Run `open_air_brayton.py` in the CoolProp environment, then `check_open_air_brayton.cjs` with Hurmet/Temml configured. Python checks energy/entropy, matched heater inlet and duty scaling; ten Hurmet numerical comparisons, save/reopen and alternator-efficiency sensitivity pass. JSON includes warmer ambient, poorer machine efficiencies and increased pressure-loss sensitivities.

## Auxiliary cooler size screen — 13 October 2026

[Brayton cooler size comparison — Hurmet](Brayton%20cooler%20size%20comparison%20-%20Hurmet.md) compares the same 30 MW-per-train duty. Calculated powers, bores, airflow face areas and cooler UA are distinct from explicitly provisional machinery/cooler boxes and plots. Initial plots are 504/600/512 m² for steam/nitrogen/open-air respectively; differences are not significant enough to rank footprints. The existing salt heater is excluded and its reuse remains unverified. Manufacturer gas-turbine packages provide only a scale benchmark, not selected equipment.

Run `python brayton_size_screen.py`, then `node check_brayton_size.cjs` with Hurmet/Temml configured. Twelve numerical checks, save/reopen and velocity sensitivity pass. None of these layout reservations modifies the accepted site graphics or selects a cooling architecture.

## Simple CO₂ loop — 13 October 2026

[Simple CO₂ Brayton cooler — Hurmet](Simple%20CO2%20Brayton%20cooler%20-%20Hurmet.md) examines an unrecuperated 10–20 MPa loop for compact heat removal. The matched-temperature 30 MW case has 0.75 m³/s compressor inlet, 6.64 MW compressor duty and 655 kW nominal electrical margin after fan/pump loads, but about 29 MW still goes to a separate outdoor dry cooler. Cases at 100°C and 40°C compressor inlet illustrate machinery/cooler tradeoffs. Nitrogen at the same pressures is included to avoid attributing all compactness to CO₂. Machine-efficiency sensitivity reduces the matched-case margin to about 12 kW. Student work on the generator's emergency air passages is explicitly excluded.

Run `co2_brayton.py` with CoolProp available, then `check_co2_brayton.cjs` with Hurmet/Temml configured. Energy/entropy, matched heater inlet, duty scaling, cooler-integration convergence and twelve Hurmet numerical checks pass. No package dimensions or qualified cooling function are established.

## Current equipment and layout basis — motor BFP

D-029 follows the owner's instruction to proceed with the motor-driven BFP
resizing. Use [Motor-BFP equipment sizing — Hurmet](Motor-BFP%20equipment%20sizing%20-%20Hurmet.md),
[motor equipment JSON](motor-equipment-sizing.json),
[pipe register](motor-equipment-pipes.csv), and
[heater register](motor-equipment-heaters.csv) for new layout work. The earlier
steam-drive sizing below is retained for comparison.

Four reheaters now reserve 16 × 3.25 × 3.25 m and 9,122 m² total surface. Generator
allowances are 550/350 MVA; BFPs are three 50% trains with 15 MW motors, with a
20 MVA BFP-only transformer allowance per train. The accepted working pipe-bore
revision is 775 mm cold reheat, 1,000 mm hot reheat, 500 mm heating return,
325 mm HP2 and 725 mm IP-to-deaerator steam. Counts and unchanged bores are in
the register; walls and insulation are additional and not yet resized.

The [first dimensional arrangement](../../../fastSaltModels/docs/site-study.md)
uses a provisional 66 × 40 × 28 m main hall, 20 × 10 × 7 m electrical annex,
+12 m turbine level and +14 m minimum deaerator water level. North/south tube
withdrawal requires removable wall panels and external aprons. This is a
reservation for one arrangement, not a minimum-building claim; piping, columns,
crane reach, egress and full auxiliary systems remain to fit. It replaces the
previous empty 45 × 24 × 20 m reservation for the working draft.

Reproduce `size_motor_equipment.py`, `publish_motor_equipment.py` and
`check_motor_equipment_hurmet.cjs`. The Python revision screens bores at the exact
5 kPa case and three cooling cases; Hurmet passes 50 numerical comparisons and
two sensitivities. The models repository's `models/turbine_layout.py` regenerates
the box/clearance JSON and SVG. Prior performance/source files are preserved.

## BFP drive alternative — 11 October 2026

The [BFP drive comparison — Hurmet](BFP%20drive%20comparison%20-%20Hurmet.md)
rebalances the cycle for electric feed-pump drive and replacement main-IP heater
extractions. At the proposed 26.5/1.0 MPa pump pressures, equal 5 kPa condenser
pressure and assumed 95% combined electrical-drive efficiency, electric drive
costs **4.03 MW / 0.269 percentage points** relative to the matched steam-drive
case. This is about 0.60% of comparison output. Both cases exclude station loads
other than the condensate pump and electric BFP; these are not final net exports.

The larger steam-driven pump required lowering LP3 heater pressure to 0.12186 MPa
to close the deaerator balance; both drive cases use that same pressure. Motor
drive supplies HP2/HP1 from 1.6/1.0 MPa main-IP extractions and DA steam from the
0.6 MPa IP outlet. Reheater duty rises from 250.1 to 281.6 MW, with about 9,122 m²
area under the existing U/margin assumptions. Carry electric drive as the preferred
candidate for review, not an adopted equipment change. Reheater, extraction-pipe,
heater-zone and electrical equipment updates are needed if it is adopted.

A 75–85% auxiliary-turbine / 93–98% electric-drive efficiency sweep gives 2.3–5.4 MW
penalty. With the same condenser and 20/30/35°C water, the base penalty is 4.12–4.23
MW. The original cycle was reproduced, both energy and mass balances close, seven
heater thermal profiles were checked, and the worksheet passes save/reopen, 12
numerical comparisons and an efficiency edit. See the
[full results](bfp-drive-comparison.json) and D-028. Reproduce with
`python compare_bfp_drives.py`, `python publish_bfp_comparison.py`, then
`node check_bfp_hurmet.cjs` with the Hurmet engine environment variables below.
Earlier performance, equipment schedules and the presentation diagram are preserved.

## Selected working cycle — 11 October 2026

After the owner requested resolution of reheat and LP wetness, a parameter study
selected the following preliminary cycle. This **supersedes the first 4 MPa /
470°C trial below for future equipment studies**, while retaining its calculations
as historical comparisons. Use the [selected Hurmet worksheet](Selected%20reheat%20and%20wetness%20-%20Hurmet.md),
[selected state table](selected-cycle-states.csv), [full results](reheat-selection.json)
and [45-case trial register](reheat-trials.csv).

| Parameter | Selected preliminary value |
| --- | --- |
| Main steam / feedwater | Unchanged: 24 MPa, 830 K steam; 560 K feedwater |
| HP exhaust | 2.8 MPa absolute |
| Hot reheat | 2.66 MPa after 5% pressure allowance; 510°C |
| Reheater heating stream | Main steam, cooled to 380°C at 24 MPa, then throttled to HP heater 4 |
| Pump-turbine heater extractions | 1.6 and 1.0 MPa; previously 2.0 and 1.2 MPa |
| Deaerator | 0.6 MPa, unchanged |
| Minimum condenser pressure | 5 kPa absolute, provisional modeling constraint |
| Reheater duty | 252.51 MW |
| Heating-steam fraction | 26.28% of total main flow; previously 15.96% |
| Minimum reheater temperature approach | 20.28 K, versus the provisional 10 K screen |
| Integrated reheater UA | 6.816 MW/K, without design margin |

The lower reheat pressure improves the expansion's moisture result; the warmer
heating-stream return avoids cooling that stream so far that an internal thermal
pinch forms. More main steam must bypass HP expansion to supply reheating.
The heater extraction pressures also change to keep every bleed positive. No
second reheater, moisture separator or salt connection is introduced.

| Condenser-water inlet | Condenser pressure | Gross power | LP moisture |
| --- | --- | --- | --- |
| 20°C | 5.053 kPa | 678.3 MW | 8.99% |
| 30°C | 8.841 kPa | 657.0 MW | 7.18% |
| 35°C | 11.518 kPa | 646.0 MW | 6.28% |

The same condenser area, U and water flow are retained. At exactly 5 kPa, gross
power is 678.72 MW, about 10.82 MW below the original trial. These are gross cycle
results, not net export guarantees or supplier off-design curves. U, interval
isentropic efficiencies and heat-transfer assumptions remain provisional.

The LP interval-efficiency sensitivity at fixed extraction pressures gives
8.43%, 9.02% and 9.61% moisture for efficiencies 0.86, 0.88 and 0.90 at 5 kPa.
Thus the case passes the 10% project screen within that tested range. It does not
establish a universal acceptable moisture level or blade-erosion performance.

Colder water must not be allowed to drive this provisional cycle below its
5 kPa floor without a new check. An uncontrolled 3 kPa trial fails the wetness
screen at LP efficiency 0.90. At a nominal 15°C fresh-water supply, ideal return
mixing of about 37.3% would maintain roughly 19.82°C effective condenser inlet
at unchanged total flow. This only demonstrates a heat-balance route to the
pressure floor; bypass hardware, fan/pump control, startup and protections remain
to design. A colder reheat outlet also requires a new operating-envelope check.

Selection favors margin over maximum output. Some passing trials make slightly
more power but have smaller thermal or heater-flow margins. The chosen point is
not claimed to be a global optimum. Reheater area depends on actual overall U:
assumed 500/1,000/1,500 W/(m² K) corresponds to approximately
13,632/6,816/4,544 m², with no fouling/design margins. These U values are sensitivity
inputs, not equipment selections.

Verification: the parameterized model reproduces the original baseline;
selected flows are positive and component/whole-cycle balances close; the
1,601/3,201-point reheater profiles and integrated UA converge; the three
condenser cases satisfy both effectiveness and LMTD heat transfer; the LP
efficiency sensitivity and cold-pressure check were completed. Hurmet passed
save/reopen recalculation, eight numerical model comparisons and reheater
hot/cold energy closure.

Reproduce with `python resolve_reheat.py`, `python publish_reheat_selection.py`,
then `node check_reheat_hurmet.cjs` with HURMET_ENGINE and TEMML_ENGINE set as below.
`reheat_model.py` is a parameterized, cached derivative of the preserved initial
solver; it does not overwrite the initial result or its provenance hashes.

Next: size the reheater, turbines and condenser from this working cycle, including
pressure losses, surface area and service access. Obtain turbine wetness,
exhaust-volume and performance limits before treating it as an equipment operating
specification. The provisional turbine-building footprint still needs verification.

## Preliminary equipment sizing — 11 October 2026

The [equipment-sizing Hurmet worksheet](Power%20plant%20equipment%20sizing%20-%20Hurmet.md)
and [sizing notes](equipment-sizing-notes.md) turn D-026 into flow-passage,
thermal-surface, pump, storage and electrical capacity estimates. Candidate layout
allowances include three condenser modules, four reheater modules and six LP
exhaust flows. Seven heater duties/area proxies and all principal/extraction
pipe bores are calculated. Dimensions, U values, availability counts and service
clearances are provisional; see the [machine-readable results](equipment-sizing.json).

A proposed 26.5 MPa BFP and 1.0 MPa condensate-pump discharge budget accounts
for losses and elevation. These values require a subsequent coupled-cycle
reclosure; **the selected 679 MW gross reference and its drawing are not updated**.
The existing turbine-building envelope remains unverified. Next arrange equipment,
water levels and maintenance access, then revise the building geometry.

## Initial design case

| Quantity | First result | Meaning |
| --- | --- | --- |
| Heat delivered to steam generators | 1,500 MW | Existing target; three 500 MW generators |
| Main steam | 24 MPa absolute, 556.85°C | Inherited 830 K condition |
| Return feedwater | 24 MPa absolute, 286.85°C | Inherited 560 K condition |
| Main flow | 711.67 kg/s total; 237.22 kg/s per generator | Recomputed from current water properties |
| Gross electrical power | 689.54 MW | Includes shaft/generator efficiency assumptions; not net export |
| Gross thermal efficiency | 45.97% | Conditional on selected section efficiencies and omitted losses |
| Steam-driven BFP shaft duty | 21.43 MW | Already supplied by modeled steam extraction, not an extra electrical subtraction |
| Condensate-pump electricity | 0.407 MW | Cooling and other auxiliaries are not included |
| Condenser heat rejection | 793.06 MW | Main condenser duty only |
| Reheat temperature | 470°C at 3.8 MPa | Selected first case; not an optimization |
| Reheater minimum approach | 12.32 K | 401-point counterflow check, provisional 10 K screening criterion |
| LP exhaust moisture | 12.64% by mass | Requires turbine/wetness review before accepting the arrangement |
| Cooling-water requirement | 23.76 m³/s | Assumed 20°C inlet, 28°C outlet, 998 kg/m³, cp = 4,180 J/(kg K) |
| Condenser tube surface | Approximately 38,500 m² | Assumed overall U = 2,500 W/(m² K); no fouling or design margin |

The condenser surface is heat-transfer area, **not building floor area**. Tube
length, pass count, velocity, pressure drop, cleaning access and LP exhaust
arrangement are required before producing an equipment envelope. The provisional
45 × 24 m turbine building has not been validated against this equipment.

## Working interpretation of the diagram

The three generators supply a common main-steam header. Main steam splits between
the HP turbine and the reheater heating side. HP exhaust passes through the cold
side of that reheater, then through the reheat/IP and LP turbines. The HP/IP set
and LP set have separate generators as drawn; the calculation sums their outputs.
Condensate passes through three closed LP heaters, the open deaerator, boiler
feed pump and four closed HP heaters before returning to the generators.

This initial mapping follows the visible bleed and drain paths but assigns
pressures that are absent from the drawing. It is a working interpretation to
review, not a claim that the diagram specifies these values. Numbered heaters
increase from coldest to hottest within each bank.

| Consumer | Steam source in this case | Nominal pressure |
| --- | --- | --- |
| Reheater heating side | Main header | 24 MPa |
| HP heater 4 and feed-pump turbine | Intermediate HP extraction | Saturation pressure at 565 K, about 7.6 MPa |
| HP heater 3 | HP exhaust | 4 MPa |
| HP heater 2 | Feed-pump-turbine extraction | 2 MPa |
| HP heater 1 | Feed-pump-turbine extraction | 1.2 MPa |
| Deaerator | Feed-pump-turbine exhaust plus HP heater drains | 0.6 MPa |
| LP heater 3 | LP turbine extraction | 0.19438 MPa, solved to close the deaerator balance |
| LP heater 2 | LP turbine extraction | 0.10 MPa |
| LP heater 1 | LP turbine extraction | 0.03 MPa |
| Main condenser | LP exhaust and LP heater drains | 0.005 MPa |

HP drains cascade 4 → 3 → 2 → 1 → deaerator; LP drains cascade 3 → 2 → 1 →
condenser. The reheater's cooled heating stream is throttled into HP heater 4.
The model includes the resulting flash enthalpy in that heater's balance. At
24 MPa, the heating stream crosses no liquid-vapor saturation boundary while
cooling; it is not treated as an isothermal condensing-steam source.

An extra deaerator extraction is **not** added. A temporary mathematical variable
measures its heat imbalance; LP heater 3 pressure is adjusted until that variable
is zero. Other feasible pressure selections can be studied later.

## Calculation method and assumptions

Properties use CoolProp 7.2.0, HEOS water with the
[IAPWS-95 equation of state](https://coolprop.org/fluid_properties/fluids/Water.html).
The retained package/version and source-diagram SHA-256 are in the result file.
The old generator worksheet's properties are preserved in that historical file;
this model does not silently replace them.

All mass fractions refer to one kilogram leaving the steam generators. Ten linear
balances solve reheater supply, heater bleeds, feed-pump-turbine admission and a
diagnostic deaerator imbalance. The outer pressure solve makes the last variable
zero. Expansion proceeds sequentially between extraction points with assumed
isentropic efficiency at each interval: HP 88%, IP 90%, LP 88%, pump turbine 80%.
These are interval efficiencies, not specified overall turbine-casing efficiencies.
Pump hydraulic efficiencies are 85% for BFP and 80% for condensate pump; shaft
transfer is 99%, generators 98.5%, condensate motor 96%.

For each interval, h_out = h_in − eta × (h_in − h_out,isentrope).
For a pump, h_out = h_in + (h_out,isentrope − h_in)/eta.
A closed heater satisfies:

`bleed × (h_bleed − h_drain,out) + incoming_drains × (h_drain,in − h_drain,out) = feed_flow × (h_feed,out − h_feed,in)`.

The reheater balance equates its two stream duties. The deaerator uses direct
mass/enthalpy mixing at saturated-liquid outlet conditions. Feed-pump-turbine work,
after shaft loss, equals BFP fluid work. Its two heater extractions reduce flow
through subsequent intervals. Heater drains are saturated liquids at shell
pressure; outlet feedwater is 5 K below shell saturation. Separate drain coolers,
vent steam, gland steam, leakage and blowdown are omitted.

HP exhaust is 4 MPa. Reheat pressure loss is 5%; the hot-side return is 360°C at
24 MPa. Other main-steam, feedwater, bleed and heater pressure losses are omitted.
The condensate pump discharges at 0.72 MPa to feed a 0.6 MPa deaerator; the final
0.12 MPa head allowance dissipates isenthalpically. BFP discharge is only 24 MPa
in this first case and must rise once generator/feedwater losses are allocated.
No heat losses or startup/off-design controls are modeled.

## Findings to resolve before equipment layout

1. **Reheat feasibility:** a 500°C outlet with the same 360°C return creates a
   −5.59 K internal approach even though endpoint temperatures alone appear
   possible. Reject that case. The 470°C case clears the provisional 10 K criterion;
   exchanger area and pressure-drop design remain open.
2. **LP wetness:** the first case gives 12.64% equilibrium moisture at exhaust.
   Obtain an acceptable turbine wetness/performance basis and consider the
   pressure split, reheat arrangement or moisture handling as needed. No blanket
   acceptance limit or equipment suitability is claimed here.
3. **Heat sink:** 5 kPa corresponds to about 32.9°C saturation. The selected
   20–28°C cooling-water case fits below it; actual summer water/weather conditions
   may require a higher backpressure. At 7.5/10 kPa the model yields about
   674.6/663.3 MW gross, respectively. These cases reclose the heater balance.
4. **Net export:** assemble station loads and revise pressure losses before
   comparing with the project's 600 MWe target. Do not subtract steam-driven BFP
   work twice. Three 2 MW salt-pump motor envelopes are not a measured auxiliary load.
5. **Equipment sizing:** select turbine exhaust arrangement, condenser geometry,
   feedwater-heater areas, deaerator hold-up and pump pressure budgets; only then
   test the proposed building dimensions and lifting/access arrangements.

## Reproduction and checks

Create a Python environment with `requirements.txt`, then run:

```sh
python rankine_cycle.py
python publish_rankine.py
HURMET_ENGINE=/path/to/hurmet.cjs TEMML_ENGINE=/path/to/temml.cjs \
  node check_rankine_hurmet.cjs
```

Run these commands in this directory. `rankine_cycle.py` performs the coupled
cycle calculation and writes JSON/CSV. `publish_rankine.py` imports that fixed
result into the Hurmet source. The final command recalculates and saves the
worksheet using the official Hurmet engine; a regenerated HTML preview is ignored
by Git. Paths to the engines are environment-specific, not project dependencies.

Verification completed: positive physical flows, feed-pump-turbine remaining
flow, zero supplemental deaerator bleed, component mass/energy consistency,
whole-cycle first-law closure, state-property round trips, condenser-pressure
sensitivity, and rejection of the reheater temperature crossover. Hurmet passed
a save/reopen recalculation, six numerical comparisons to the external model and
a fixed-cycle 50% heat-duty scaling check. These checks verify the implementation
and the stated idealizations, not the physical suitability of a plant design.


## Accepted cooling-water cases — 11 October 2026

The owner accepted 20°C normal-reference, 30°C hot-design and 35°C extreme
condenser-water inlet cases. No site or frequency of occurrence is implied.
The [cooling-water Hurmet worksheet](Cooling-water%20cases%20-%20Hurmet.md)
and [coupled results](cooling-cases.json) screen the same condenser in all cases:
38,513 m², U = 2,500 W/(m² K), water flow 23.76 m³/s, 1,500 MW heat input,
470°C reheat and unchanged extraction pressures. Extraction flows rebalance;
section efficiencies remain constant. This is not a manufacturer's operating map.

| Inlet water | Outlet water | Condenser absolute pressure | Gross power | Exhaust moisture |
| --- | --- | --- | --- | --- |
| 20°C reference | 28.00°C | 5.00 kPa | 689.5 MW | 12.64% |
| 30°C hot check | 38.22°C | 8.75 kPa | 668.6 MW | 10.98% |
| 35°C extreme | 43.33°C | 11.40 kPa | 657.9 MW | 10.16% |

The reductions of approximately 20.9 and 31.6 MW are gross output changes from
higher exhaust pressure at constant heat input, not reactor deratings. Station
loads, turbine operating limits and possible power restrictions are not modeled.
The results do not yet meet the proposed 10% moisture screening target in any
case. Cooler water increases the wetness concern in this trial cycle, so hot-day
sizing cannot substitute for a minimum-pressure operating check.

The condenser solve uses constant U and cooling-water heat capacity rate C:
`Q(P) = C * (1 - exp(-UA/C)) * (Tsat(P) - Tin)`.
Cycle heat rejection Q(P) and saturation temperature determine the pressure.
Water outlet is `Tin + Q/C`; its rise is not fixed at 8 K outside the reference
case. The solution is checked independently with `Q = UA * LMTD`, preserves
physical flow fractions, closes cycle energy and recovers the reference case.
Hurmet independently checks all three areas and outlet temperatures after a
save/reopen recalculation.

Run `python cooling_cases.py`, `python publish_cooling_cases.py`, then
`node check_cooling_hurmet.cjs` with HURMET_ENGINE and TEMML_ENGINE set as above.
The original Rankine worksheet remains the reference case. This follow-up has
not selected a new condenser size: choosing permissible hot-day pressure/output
and the cooling-system arrangement is still required before equipment sizing.
