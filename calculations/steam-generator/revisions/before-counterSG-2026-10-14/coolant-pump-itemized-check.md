# Itemized coolant pump-power check

14 October 2026. [Editable Hurmet worksheet](Itemized%20coolant%20pump%20estimate%20-%20Hurmet.md). A preliminary normal-duty power budget at the owner-selected UM case, with explicit loss terms replacing the previous 50% multiplier. This is not a final pump or motor selection.

## Results

Total mass flow is 18,500 kg/s, or 6,166.7 kg/s in each of three parallel SG/pump legs. Pump cold-leg volume flow is 3.723 m³/s per leg at 810 K; SG mean-temperature properties use 850 K. The reactor core carries the combined flow, but its pressure loss is common to each loop path and is counted once per pump head.

| Pressure-loss contribution | kPa per circulation path |
| --- | ---: |
| SG tube friction, recalculated at UM flow | 131.33 |
| SG tube entrance/exit allowance | 5.04 |
| Core + reflector passages + their end allowances | 62.71 |
| Main pipe and reactor-nozzle straight friction | 1.29 |
| Seven modeled bends, provisional K values | 9.59 |
| Two SG collectors/transitions, provisional | 9.15 |
| Reactor nozzle entry/exit, provisional | 9.00 |
| Two proposed fully open main isolation valves | 1.83 |
| Downcomer straight friction | 0.01 |
| Reactor bulk-turn allowance | 0.72 |
| **Total** | **230.68** |

Equivalent differential head is 14.20 m of cold salt. No blanket percentage is added. Full building height is not an extra closed-loop static lift; no favorable thermosiphon credit is taken.

| Power | Per pump | All three pumps |
| --- | ---: | ---: |
| Hydraulic | 859 kW | 2.577 MW |
| Shaft, 80% pump efficiency | 1,074 kW | 3.221 MW |
| Electrical input, 96% motor efficiency | 1,118 kW | **3.355 MW** |

## Uncertainty

- The documented low/high fitting-coefficient cases give **3.103–3.905 MW electrical total**, holding core resistance, tube roughness and efficiencies fixed. This is a sensitivity range, not a statistical confidence interval or guaranteed design envelope.
- Raising both core/SG tube roughness from 1 to 10 micrometres gives 3.482 MW, and to 45 micrometres gives 3.906 MW with baseline fittings. These separate sensitivities do not bound combined adverse changes.
- Varying pump efficiency from 85% to 75%, with motor efficiency fixed at 96%, gives 3.158–3.579 MW for baseline hydraulic losses.
- SG tube length remains the earlier 19.879 m hydraulic estimate, not the 17 m visible casing. Thermal performance at the new temperature range is not verified here.
- Actual collectors, bends, nozzles, valve selection, internal restrictions, flow distribution and deposit growth are not resolved. Core resistance is explicitly imported from the checked core worksheet; changing flow requires recalculating it.
- Detailed variable-density network energy balance, pump curve/NPSH and off-normal duty are still needed. Existing 2 MW motor reservations are not changed.

The earlier 5.166 MW result used the larger 22,699 kg/s flow as well as the blanket SG × 1.5 rule. At the **same new flow**, that old method gives 2.865 MW, below the 3.355 MW itemized estimate. Thus the reduction from the original 5.166 MW is primarily due to the changed flow basis; replacing the blanket factor does not necessarily reduce duty.

## Verification and reproducibility

Sixty-two Hurmet comparisons against independent SI arithmetic and bracketed Colebrook solutions pass. Save/reopen, efficiency sensitivity, SG length scaling, bend coefficient response and itemized addition pass. The three modeled legs have equal route lengths; the representative leg contains 15.751 m hot pipe, 16.184 m cold suction/return pipe and seven bends. Reactor nozzle lengths are included separately.

Run `python calculations/steam-generator/coolant_pump_itemized.py`, then `node calculations/steam-generator/check_coolant_pump_itemized.cjs` with HURMET_ENGINE and TEMML_ENGINE set to the existing bundles. [Inputs, routes, source hashes and independent results](coolant-pump-itemized-results.json); [Hurmet verification](coolant-pump-itemized-hurmet-checks.json). HTML is generated under ignored `outputs/coolant-pump-itemized/`.

Sources: current core worksheet, original generator sizing, current resolved coolant assembly and verified reactor-interface report. Method reference: [NASA KSC-STD-Z-0017 Rev A](https://standards.nasa.gov/sites/default/files/standards/KSC/A/0/KSC-STD-Z-0017_RevA_Final.pdf), §§7.4–8.1. Local K coefficients are provisional choices, not certified values for this geometry.

D-061 now adopts this checked duty into the shared P&ID/graphics records; all numerical results are unchanged after source-provenance refresh. No Blender regeneration, motor downsizing, commit, SG failure assessment or relief sizing is performed.
