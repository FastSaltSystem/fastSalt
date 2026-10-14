# Core coolant pressure-loss check

14 October 2026. Owner-selected UM total flow of 18,500 kg/s, inlet/outlet 810/890 K, and confirmed 3.4 m active height. The appendix's 3.8 m height is an owner-confirmed typo. Current 3.8 m core diameter is retained.

## Results

[Editable Hurmet worksheet](Core%20coolant%20pressure%20loss%20-%20Hurmet.md).

| Quantity | Estimate |
| --- | ---: |
| Tube count / clear bore | 24,576 / 14 mm |
| Active length / length including reflectors | 3.40 / 3.95 m |
| Mean bulk temperature | 850 K (577°C) |
| Mean density / dynamic viscosity | 1633.8 kg/m³ / 2.913 mPa·s |
| Total area from count and bore | 3.783 m² |
| Mean / cold-inlet / hot-outlet velocity | 2.993 / 2.952 / 3.035 m/s |
| Reynolds number / Darcy friction factor | 23,506 / 0.02506 |
| Active-core friction | 44.53 kPa (0.445 bar) |
| Both reflector extensions, assumed same bore | 7.20 kPa |
| Provisional entrance + exit allowance, K = 1.5 | 10.98 kPa |
| Total passage loss with end allowances | 62.71 kPa (0.627 bar), 3.91 m salt head |

This is one parallel-passage pressure difference. Do not multiply it by tube count or by three coolant legs. All core flow divides among the complete tube population.

The mean velocity is narrowly below 3 m/s. This does not meet a strict local maximum of 3 m/s at the outlet. The report's 3.86 m² flow area is 2.03% greater than count × exact 14 mm-bore area; using that reported area gives 2.934 m/s at mean temperature, consistent with its rounded 2.94 m/s. The count/area discrepancy remains unresolved; it is not silently removed by changing tube bore.

## Assumptions and checks

- Colebrook/Darcy calculation, 1 micrometre assumed roughness. At 10 micrometres, passage-plus-end loss is 65.71 kPa; at 45 micrometres it is 75.35 kPa. These are sensitivities, not known surface condition.
- Both reflector passages are assumed continuous 14 mm bore. No internal obstruction or tube-to-reflector step is assigned. K = 0.5 entrance + 1.0 exit is a provisional estimate for the passage ends only.
- Mean-temperature active-core friction is 44.532 kPa; an independent axial integration with linear heating gives 44.546 kPa, only 0.03% different. This verifies the mean-property approximation for that assumed temperature profile.
- Upward elevation contributes approximately 63.29 kPa to bottom-to-top static pressure difference; it is not an irreversible loss or additional closed-loop pump duty. The worksheet separately shows a small approximate acceleration term.
- Thirty-five Hurmet numerical comparisons pass, using an independent bracketed Colebrook root in Python and fixed-point iteration in Hurmet. Save/reopen, length, flow and roughness checks pass.
- Flow maldistribution, blocked tubes, bypass, entry details, plenums, downcomer, nozzles and external piping remain outside this estimate.

The earlier generator/pump/pressure-profile worksheets use 22,699 kg/s total and 810–875 K. They must be reconciled to the selected UM basis before this core result is combined with them. Their earlier results remain historical calculations; no new full-loop duty or pressure rating is established here. SG failure assessment and building rearrangement remain deferred.

## Sources and reproduction

UM/NRDSL-25/02, *Core Design Evolution of Wielenga Innovation Salt Tank Reactor*, November 15, 2025: Tables 25 (p.87), 42 (p.109), 43 (p.110), 58 (p.139). Tables 42/43 and 58 were checked visually in the PDF. Owner clarification on 14 October 2026 selects UM flow and corrects height to 3.4 m. Current model supplies reflector thicknesses; roughness is inherited from the preliminary generator calculation.

Run `python calculations/reactor/core_coolant_loss.py` and `node calculations/reactor/check_core_coolant_loss.cjs`, setting HURMET_ENGINE and TEMML_ENGINE to the Hurmet bundles. [Inputs, source hashes and independent results](core-coolant-loss-results.json); [Hurmet verification](core-coolant-loss-hurmet-checks.json). Generated HTML resides in ignored `outputs/core-coolant-loss/`.

Method: [NASA KSC-STD-Z-0017 Rev A](https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017_RevA_Final.pdf), §§7.4–7.5. General fluid-flow method only; not nuclear-system qualification.
