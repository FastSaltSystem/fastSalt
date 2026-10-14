# Coolant inventory and TK-401 capacity — counterSG update

14 October 2026. [Live Hurmet sheet](Coolant%20inventory%20and%20storage%20capacity%20-%20Hurmet.md).

D-063 adopts the newer `counterSG.xlsx` geometry: **4,902 salt tubes per SG, 20 mm ID / 24 mm OD and 11.920866 m calculated active length**, provisionally used as straight hydraulic length. The 6,536 steam tubes are a separate bank. The 17 m casing, 18,500 kg/s total flow, 810–890 K temperatures and 3.4 m active core remain unchanged. Salt inlet/outlet labels were corrected to 890/810 K; numeric cells and formulas are unchanged.

At the retained flow, mean SG tube velocity is 2.451 m/s. SG tube friction is **70.491 kPa**, or **87.004 kPa including tube ends and collector allowances**. Full-loop pump rise is **172.162 kPa** (10.599 m cold-salt head). Per pump: **801.2 kW shaft / 834.6 kW electrical**; three-pump total **2.504 MW electrical**. Fitting sensitivity is 2.241–3.065 MW, not a certified range. The prior D-061 total was 3.355 MW.

With 1 bar(g) at SG tops, suction is **2.246 bar(g)**, discharge **3.823 bar(g)**, and reactor bottom-plenum midpoint **4.254 bar(g)**. Lower SG resistance raises suction and reduces required pump rise by matching amounts; downstream pressures stay unchanged in this fixed-flow, mean-density screen.

The revised inventory is approximately **452.3 m³**, including **55.1 m³ in all three SG tube banks**. At 890 K, the fixed cold-fill charge requires 478.7 m³, or 526.5 m³ including 10% inventory allowance. The already-selected 8.2 × 16 m storage reservation provides 622.1 m³ working acceptance under existing allowances, leaving 95.6 m³. Tank placement remains pending; the smaller saved Blender tank remains a historical layout envelope.

The shared TOML, P&ID and resolved graphics duty metadata use the checked revision. Existing 2 MW motor reservations and physical equipment/pipe envelopes are retained. Actual SG contact conductance, hydraulic extensions, local coefficients, roughness and pump curves/NPSH remain provisional. No protection setpoints, relief capacity or SG-failure assessment are established. Older Generator sizing and Brayton worksheets remain explicitly historical cases.

## Volume and capacity basis

| Quantity | m³ |
| --- | ---: |
| Reactor gross spaces and channels | 179.20 |
| Three SG tube banks | 55.07 |
| Hot main pipes | 75.36 |
| Cold main pipes | 77.43 |
| Collectors | 27.73 |
| Pump liquid allowance | 16.63 |
| Whole loop | 452.28 |
| Normal expansion at 450°C storage | 18.41 |
| All-hot expansion at 450°C storage | 24.94 |
| Required hot working capacity with 10% allowance | 526.54 |
| Selected tank working capacity | 622.10 |
| Selected tank remaining margin | 95.56 |

Core coolant area now consistently uses 24,576 × 14 mm bores (3.78318 m²), rather than the report’s rounded 3.86 m². The 17 m SG full-casing-length alternative is sensitivity only, not the active tube basis. Gross plenums, collector/pump cavities, internal tank allowances and service volumes remain provisional. The original 4 × 8 m tank still in Blender provides only 72.6 m³ working capacity; the selected larger tank is a separate planning reservation. No relocation or geometry change is made.

Workbook recalculation and 62 independent segment-length comparisons pass. Hurmet save/reopen and sensitivities pass for 62 pump, 53 pressure and 67 inventory results. Source workbook, corrected-label provenance and prior hydraulic snapshots are retained under calculations/steam-generator/.
Run `coolant_inventory.py`, then `check_coolant_inventory.cjs`. Mass-balance checks avoid double-counting expansion salt. Prior inputs/results are preserved with the hydraulic snapshot.
