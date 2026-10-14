# Itemized coolant pump estimate — counterSG update

14 October 2026. [Live Hurmet sheet](Itemized%20coolant%20pump%20estimate%20-%20Hurmet.md). D-063 supersedes D-061 SG geometry.

D-063 adopts the newer `counterSG.xlsx` geometry: **4,902 salt tubes per SG, 20 mm ID / 24 mm OD and 11.920866 m calculated active length**, provisionally used as straight hydraulic length. The 6,536 steam tubes are a separate bank. The 17 m casing, 18,500 kg/s total flow, 810–890 K temperatures and 3.4 m active core remain unchanged. Salt inlet/outlet labels were corrected to 890/810 K; numeric cells and formulas are unchanged.

At the retained flow, mean SG tube velocity is 2.451 m/s. SG tube friction is **70.491 kPa**, or **87.004 kPa including tube ends and collector allowances**. Full-loop pump rise is **172.162 kPa** (10.599 m cold-salt head). Per pump: **801.2 kW shaft / 834.6 kW electrical**; three-pump total **2.504 MW electrical**. Fitting sensitivity is 2.241–3.065 MW, not a certified range. The prior D-061 total was 3.355 MW.

With 1 bar(g) at SG tops, suction is **2.246 bar(g)**, discharge **3.823 bar(g)**, and reactor bottom-plenum midpoint **4.254 bar(g)**. Lower SG resistance raises suction and reduces required pump rise by matching amounts; downstream pressures stay unchanged in this fixed-flow, mean-density screen.

The revised inventory is approximately **452.3 m³**, including **55.1 m³ in all three SG tube banks**. At 890 K, the fixed cold-fill charge requires 478.7 m³, or 526.5 m³ including 10% inventory allowance. The already-selected 8.2 × 16 m storage reservation provides 622.1 m³ working acceptance under existing allowances, leaving 95.6 m³. Tank placement remains pending; the smaller saved Blender tank remains a historical layout envelope.

The shared TOML, P&ID and resolved graphics duty metadata use the checked revision. Existing 2 MW motor reservations and physical equipment/pipe envelopes are retained. Actual SG contact conductance, hydraulic extensions, local coefficients, roughness and pump curves/NPSH remain provisional. No protection setpoints, relief capacity or SG-failure assessment are established. Older Generator sizing and Brayton worksheets remain explicitly historical cases.

## Loss budget per circulation path

| Term | kPa |
| --- | ---: |
| SG straight-tube friction | 70.491 |
| SG tube ends | 7.361 |
| Core and reflector passages, including ends | 62.714 |
| Straight pipe and nozzle friction | 1.293 |
| Bends | 9.591 |
| Collectors | 9.153 |
| Reactor nozzle local losses | 9.005 |
| Valves | 1.831 |
| Downcomer friction | 0.007 |
| Bulk reactor turn | 0.718 |
| Total | 172.162 |

## Verification and reproduction

Workbook recalculation and 62 independent segment-length comparisons pass. Hurmet save/reopen and sensitivities pass for 62 pump, 53 pressure and 67 inventory results. Source workbook, corrected-label provenance and prior hydraulic snapshots are retained under calculations/steam-generator/.
Run `counter_sg_basis.py`, `coolant_pump_itemized.py`, then `check_coolant_pump_itemized.cjs` with the Hurmet bundles. Re-adopt reviewed worksheet hashes and results before downstream builds. The old worksheets and check reports are preserved in `revisions/before-counterSG-2026-10-14/`.

Final cross-view verification: 15 P&ID tests and 8 shared-view tests pass. The rebuilt circulation sheet was visually inspected. All 11 component placements/envelopes, 18 ports and 9 routes match the prior resolved graphics document; only pump loss/duty metadata changes. No full Blender build or commit.
