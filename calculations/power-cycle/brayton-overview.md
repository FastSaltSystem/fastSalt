# Auxiliary Brayton coolers — overview

**Preserved study:** [RS-008, Revision A - 19 October 2026](../../research/auxiliary-brayton-cooling/README.md), including PDF, browser report and source snapshot.

Updated 19 October 2026. Consolidated summary of the existing 12–13 October exploratory calculations. The steam study now sits alongside closed nitrogen, open air and a simple supercritical CO₂ loop. **These are alternative 30 MW-per-train comparison cases, not selected equipment capacities.** No new cycle or hydraulic calculation is introduced here.

Each turbine drives its compressor and an alternator. The remaining electricity supplies the salt pump and, for closed cycles, the air-cooler fan. The open-air cycle exhausts its working air directly and needs no separate cooler fan.

## Comparison at the same heater temperatures

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

## What the alternatives show

- **Steam:** the 2:1 case has a modest positive electrical margin. At 30 MW it requires about 247 m³/s of cooling air and an approximately 82 m² cooler airflow face at the assumed 3 m/s face velocity. The earlier 8:1 steam case increases surplus but requires vacuum suction and about 1,564 m³/s compressor-inlet flow at this duty, undermining the compactness objective.
- **Nitrogen:** the 4:1, 10–40 bar case reduces working-gas volume and has a larger electrical margin than the selected steam case. Its ideal-counterflow cooler conductance is approximately 235 kW/K at 30 MW, versus 123 kW/K for steam. At equal pressure and ratio, the earlier 2:1 nitrogen and steam results were nearly equal; the table compares complete operating points, not fluid effects alone.
- **Open air:** removing the separate cooler and fan leaves the largest nominal electrical margin in these trials. The tradeoff is large process airflow: about 89 m³/s into the compressor and 158 m³/s discharged at approximately 267°C. The earlier flow-area illustration gives roughly 2.75 m intake and 3.66 m exhaust equivalent bores at 15 m/s; these are not selected duct dimensions.
- **Supercritical CO₂:** the matched-temperature, 100–200 bar case has the smallest compressor-inlet flow, but still rejects about 28.8 MW through a separate cooler with roughly 82 m² airflow face. High pressure accounts for part of the reduction: the saved nitrogen trial at the same 100–200 bar gives about 1.35 m³/s inlet flow versus CO₂'s 0.75 m³/s. A smaller flow passage does not establish the size of the complete equipment package.

The CO₂ study also includes 100°C and 40°C compressor-inlet cases. They give smaller working-fluid volumes and larger nominal power margins, but change the heater inlet temperature. The 40°C case requires about 770 kW/K cooler conductance versus 114 kW/K for the matched-temperature case. Those variants are therefore kept separate from the comparison table.

## Basis and limits of this overview

The comparison retains 85% compressor and 88% turbine isentropic efficiencies, 98% shaft transfer, and 95% alternator efficiency. Closed loops assume 2% pressure loss per exchanger and 30→130°C cooling air with 500 Pa air-system loss. Open air uses 30°C ambient intake, 500 Pa intake loss, 2% heater loss and 1 kPa exhaust backpressure.

**The 130 kW salt-pump allowance is historical:** it assumes a 10 K salt temperature drop and the original steam-generator hydraulic model plus 50% for the loop. It has not been updated to the later itemized coolant-loss calculation. Keeping it unchanged preserves the original comparisons; these margins are not the current plant pump budget.

Existing sensitivities show that lower machine efficiency or greater pressure loss can consume the margin. In the matched CO₂ sensitivity, 80% compressor / 85% turbine efficiencies leave only about 12 kW after the modeled fan and pump. Positive nominal power balance alone does not establish performance across startup or cooldown.

The earlier steam/nitrogen/open-air layout reservations of roughly 500–600 m² per train are provisional allowances, excluding the existing salt heater, and do not rank installed footprints reliably. No CO₂ package envelope has been established. Generator reuse, exchanger performance, actual pressure losses and machinery maps remain unresolved. The students' separate study of emergency air passages in the steam generators is not included in these results.

## Detailed worksheets and saved results

| Study | Hurmet worksheet | Saved numerical results |
| --- | --- | --- |
| Steam fan/pump balance | [Steam balance](Brayton%20fan%20and%20salt%20pump%20balance%20-%20Hurmet.md) | [JSON](brayton-fan-pump-results.json) |
| Nitrogen comparison | [Nitrogen versus steam](Nitrogen%20versus%20steam%20Brayton%20-%20Hurmet.md) | [JSON](nitrogen-brayton-results.json) |
| Open-air comparison | [Open-air Brayton cooler](Open-air%20Brayton%20cooler%20-%20Hurmet.md) | [JSON](open-air-brayton-results.json) |
| Supercritical CO₂ comparison | [Simple CO₂ loop](Simple%20CO2%20Brayton%20cooler%20-%20Hurmet.md) | [JSON](co2-brayton-results.json) |
| Preliminary size comparison | [Size screen](Brayton%20cooler%20size%20comparison%20-%20Hurmet.md) | [JSON](brayton-size-results.json) |

The linked worksheets retain their calculation assumptions and checks. This overview reports their saved results; it does not independently recalculate thermodynamic properties. To refresh the local browser view from this Markdown, run `node publish_brayton_overview.cjs` with `HURMET_ENGINE` and `TEMML_ENGINE` configured as for the worksheet checks. Browser previews remain local generated outputs.
