# Auxiliary Brayton Cooling Options for the Fast Salt System

## Preliminary Comparative Study

**RS-008 | Revision A | 19 October 2026**

Prepared for the Fast Salt System project. This report consolidates the project's exploratory calculations of 12-13 October 2026 and the overview assembled on 19 October. Technical review is pending; no cooling architecture or equipment has been selected. The report is a project working study, not a University of Michigan or Michigan State University research publication.

## Purpose and scope

Compare a non-condensing steam Brayton loop with closed nitrogen, open air and a simple supercritical CO₂ loop as auxiliary heat-removal concepts. The objective is to understand their saved power balances and compactness tradeoffs, rather than maximize electricity production.

Each turbine drives its compressor and an alternator. The alternator supplies a salt-circulation pump and, for closed cycles, a separate air-cooler fan. The open-air arrangement exhausts its working air directly. These concepts are separate from the main Rankine power cycle.

## Arrangements compared

- Closed steam, nitrogen and CO₂: compressor → salt-to-working-fluid heater → turbine → air-cooled heat exchanger → compressor.
- Open air: atmospheric intake → compressor → salt-to-air heater → turbine → atmospheric exhaust.

No recuperator or compressor intercooling is included. The comparison uses one 30 MW train with approximately 287°C heater inlet and 557°C turbine inlet. This is a comparison duty, not an established emergency cooling requirement or equipment rating.

## Retained assumptions

The comparison retains 85% compressor and 88% turbine isentropic efficiencies, 98% shaft transfer, and 95% alternator efficiency. Closed loops assume 2% pressure loss per exchanger and 30→130°C cooling air with 500 Pa air-system loss. Open air uses 30°C ambient intake, 500 Pa intake loss, 2% heater loss and 1 kPa exhaust backpressure.

Salt circulation retains a 10 K temperature drop and approximately 130 kW pump electricity from the earlier hydraulic case. That allowance uses the original generator pressure loss plus 50%; it has not been updated to the later itemized pressure-loss estimate.

## Principal finding

All four selected operating points have positive nominal electrical margins after the modeled fan and pump. Compact working-fluid machinery does not necessarily produce a compact cooling installation: the closed cycles still require a substantial outdoor heat sink, while open air requires large intake and exhaust passages.

<!-- pagebreak -->

## 1. Common-duty comparison

All four selected cases use approximately **287°C heater inlet and 557°C turbine inlet**. The nitrogen and air results saved at 10 MW are scaled by three, as in their existing worksheets. Machinery and exchanger capacity are assumed to scale with duty; this is not an increase in the output of a fixed-size machine.

| Quantity at 30 MW heat input | Closed steam | Closed nitrogen | Open air | Supercritical CO₂ |
| --- | --- | --- | --- | --- |
| Compressor pressures, bar absolute | 5 → 10 | 10 → 40 | 1.008 → 6.888 | 100 → 200 |
| Pressure ratio | 2:1 | 4:1 | 6.832:1 | 2:1 |
| Compressor inlet, °C | 192.1 | 84.2 | 30.0 | 204.3 |
| Compressor-inlet volume, m³/s | 21.572 | 10.672 | 89.169 | 0.747 |
| Electricity after compressor, before fan/pump, MW | 0.761 | 2.691 | 4.230 | 0.981 |
| Cooler-fan electricity, MW | 0.198 | 0.182 | None | 0.197 |
| Salt-pump electricity, MW | 0.130 | 0.130 | 0.130 | 0.130 |
| Remaining electricity, MW | 0.432 | 2.379 | 4.100 | 0.655 |
| Heat to separate air cooler, MW | 28.988 | 26.671 | No separate cooler | 28.810 |

“Remaining electricity” is after the compressor, modeled shaft/alternator losses, cooler fan where applicable, and salt pump. It is before unallocated loads such as controls and heat tracing. Open air discharges approximately **24.90 MW** in its exhaust above intake-air enthalpy; this is part of the 30 MW heat balance, not additional cooling.


## Reading the results

The values are imported from the saved calculations. Small differences between sums of displayed values and the displayed margin arise from rounding. The pressure row gives compressor suction and discharge pressure, not pressure at every station.

The selected pressure levels and ratios differ. The table therefore compares complete candidate operating points; it does not isolate the effect of changing only the working fluid. No allowance for controls, heat tracing or other unallocated station loads has been subtracted from the remaining electricity.

With the same salt-pump allowance, the existing worksheets give approximately 29.88-29.90 MW net heat removal after pump heat return for a 30 MW gross salt-to-cycle duty, before other heat gains. This is a modeled steady operating point, not a startup or cooldown capability claim.

<!-- pagebreak -->

## 2. Interpretation and size tradeoffs

- **Steam:** the 2:1 case has a modest positive electrical margin. At 30 MW it requires about 247 m³/s of cooling air and an approximately 82 m² cooler airflow face at the assumed 3 m/s face velocity. The earlier 8:1 steam case increases surplus but requires vacuum suction and about 1,564 m³/s compressor-inlet flow at this duty, undermining the compactness objective.
- **Nitrogen:** the 4:1, 10-40 bar case reduces working-gas volume and has a larger electrical margin than the selected steam case. Its ideal-counterflow cooler conductance is approximately 235 kW/K at 30 MW, versus 123 kW/K for steam. At equal pressure and ratio, the earlier 2:1 nitrogen and steam results were nearly equal; the table compares complete operating points, not fluid effects alone.
- **Open air:** removing the separate cooler and fan leaves the largest nominal electrical margin in these trials. The tradeoff is large process airflow: about 89 m³/s into the compressor and 158 m³/s discharged at approximately 267°C. The earlier flow-area illustration gives roughly 2.75 m intake and 3.66 m exhaust equivalent bores at 15 m/s; these are not selected duct dimensions.
- **Supercritical CO₂:** the matched-temperature, 100-200 bar case has the smallest compressor-inlet flow, but still rejects about 28.8 MW through a separate cooler with roughly 82 m² airflow face. High pressure accounts for part of the reduction: the saved nitrogen trial at the same 100-200 bar gives about 1.35 m³/s inlet flow versus CO₂'s 0.75 m³/s. A smaller flow passage does not establish the size of the complete equipment package.

The CO₂ study also includes 100°C and 40°C compressor-inlet cases. They give smaller working-fluid volumes and larger nominal power margins, but change the heater inlet temperature. The 40°C case requires about 770 kW/K cooler conductance versus 114 kW/K for the matched-temperature case. Those variants are therefore kept separate from the comparison table.


<!-- pagebreak -->

## 3. Limitations and unresolved questions

**The 130 kW salt-pump allowance is historical:** it assumes a 10 K salt temperature drop and the original steam-generator hydraulic model plus 50% for the loop. It has not been updated to the later itemized coolant-loss calculation. Keeping it unchanged preserves the original comparisons; these margins are not the current plant pump budget.

Existing sensitivities show that lower machine efficiency or greater pressure loss can consume the margin. In the matched CO₂ sensitivity, 80% compressor / 85% turbine efficiencies leave only about 12 kW after the modeled fan and pump. Positive nominal power balance alone does not establish performance across startup or cooldown.

The earlier steam/nitrogen/open-air layout reservations of roughly 500-600 m² per train are provisional allowances, excluding the existing salt heater, and do not rank installed footprints reliably. No CO₂ package envelope has been established. Generator reuse, exchanger performance, actual pressure losses and machinery maps remain unresolved. The students' separate study of emergency air passages in the steam generators is not included in these results.


## 4. Source record and review status

This revision preserves the current worksheets, Python generators, JavaScript checks, saved JSON results and original generator-sizing reference under `sources/`. The current repository base commit is recorded in `manifest.json`, but the Brayton studies include uncommitted working files: the base commit alone does not identify their contents. The manifest supplies SHA-256 hashes for the actual archived files.

Existing calculation-check records are retained as historical evidence. Packaging verified source copies, the overview values, document links and report rendering; it did not rerun the thermodynamic solvers or perform independent engineering validation. Some stored result files reference earlier source hashes; any mismatch with the current archived copy is listed in `source-hash-audit.json`, without rewriting the historical results.

The next technical review can update the pump-loss basis and assess actual heat-exchanger and machinery performance before selecting a concept. The students' emergency air-passage work remains a separate study. Later changes should form Revision B, preserving this snapshot.

<!-- pagebreak -->

## 5. Supporting worksheets and results

| Study | Hurmet worksheet | Saved numerical results |
| --- | --- | --- |
| Steam fan/pump balance | [Steam balance](sources/calculations/power-cycle/Brayton%20fan%20and%20salt%20pump%20balance%20-%20Hurmet.md) | [JSON](sources/calculations/power-cycle/brayton-fan-pump-results.json) |
| Nitrogen comparison | [Nitrogen versus steam](sources/calculations/power-cycle/Nitrogen%20versus%20steam%20Brayton%20-%20Hurmet.md) | [JSON](sources/calculations/power-cycle/nitrogen-brayton-results.json) |
| Open-air comparison | [Open-air Brayton cooler](sources/calculations/power-cycle/Open-air%20Brayton%20cooler%20-%20Hurmet.md) | [JSON](sources/calculations/power-cycle/open-air-brayton-results.json) |
| Supercritical CO₂ comparison | [Simple CO₂ loop](sources/calculations/power-cycle/Simple%20CO2%20Brayton%20cooler%20-%20Hurmet.md) | [JSON](sources/calculations/power-cycle/co2-brayton-results.json) |
| Preliminary size comparison | [Size screen](sources/calculations/power-cycle/Brayton%20cooler%20size%20comparison%20-%20Hurmet.md) | [JSON](sources/calculations/power-cycle/brayton-size-results.json) |

The archive also contains the initial steam trial and salt-pump follow-up, their publishers and check scripts, and the original generator-sizing worksheet used for provenance. Hurmet Markdown is the editable calculation record; the PDF and HTML report summarize its saved results.

## Software and reproduction

The sources identify CoolProp 7.2.0 real-fluid properties. `requirements.txt` retains CoolProp 7.2.0 and NumPy 2.3.5. The Hurmet and Temml engines are external dependencies, not bundled into this study. Their local hashes at packaging are recorded in the manifest where available.

Use a disposable copy of `sources/` for any recalculation: the original scripts overwrite their results and worksheets. Preserve the directory structure so the generator-sizing reference remains at the expected relative location. Run the cycle and publisher scripts in dependency order, as documented in `README.md`; do not treat regeneration as approval of an operating design.

`report.md` is the editable prose source. `render_report.py` creates `report.pdf` and `report.html` using ReportLab and a Unicode font. Changing prose and rebuilding a document is separate from recalculating the studies.

## Revision history

| Revision | Date | Change | Status |
| --- | --- | --- | --- |
| A | 19 October 2026 | Preserve the four-case comparative overview and supporting calculation records | Preliminary; technical review pending |
