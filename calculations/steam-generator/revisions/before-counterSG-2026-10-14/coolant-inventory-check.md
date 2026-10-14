# Coolant inventory and TK-401 capacity — preliminary check

14 October 2026. [Live Hurmet worksheet](Coolant%20inventory%20and%20storage%20capacity%20-%20Hurmet.md). These are layout-based estimates, not a selected replacement tank or a qualified drainage design.

**The current tank can accommodate the estimated expansion if initially near its reserved heel, but cannot receive the complete coolant inventory.** The steam-generator tubes alone exceed its gross internal capacity under the existing generator calculation.

## Inventory estimate

| Component | Coolant volume, m³ | Basis |
| --- | ---: | --- |
| Reactor spaces | 179.5 | Gross plenums/downcomer plus provisional UM channel-flow area through core/reflectors |
| Three SG tube banks | 111.0 | 12,090 salt tubes each, 14 mm bore, 19.879 m calculated length |
| External main pipes | 152.8 | All nine rounded route segments, 1.425 m bore |
| Six reactor nozzles | 18.9 | Preserved 1.33 m clear bore; lengths excluded from external pipe routes |
| Six salt collectors | 27.7 | Half-cylinder approximations; wall provisional |
| Pump liquid cavities | 16.6 | Assumed 50% of cylindrical casing envelopes |
| Small lines / gas-vessel salt / valves | 2.0 | Provisional aggregate allowance |
| **Total circuit** | **508.5** | Excludes TK-401 inventory, fuel, absorber salt, water and steam |

The vessel spaces are gross fluid envelopes: no exact displacement calculation for supports/links is claimed. The UM report's 3.86 m² coolant area is a provisional engineering reference; its Appendix B dimensions and 890 K outlet differ from current owner geometry and the 875 K generator case. The graphic hole pattern is not a tube-count basis. Precise core passages, pump cavities, collectors and SG internals remain to reconcile.

## Expansion versus full-drain duty

Use a fixed charge that fills the circuit at **450°C**, based on the existing density correlation. Its mass is approximately **867 t**, excluding the separate tank heel/reserve. The normal temperature distribution places approximately **834 t** in the circulating loop.

| Quantity | Result | Meaning |
| --- | ---: | --- |
| Normal expansion transferred to 450°C storage | 19.6 m³ | Difference between cold-filled charge and normal circulating mass |
| All-hot 602°C circuit: expansion at 450°C storage | 25.5 m³ | Thermal screening case, not a selected maximum design temperature |
| Full charge at 450°C storage | 508.5 m³ | Includes previously transferred expansion salt once |
| Full charge at 602°C | 535.4 m³ | Hot receiving-volume reservation |
| Current tank gross external cylinder | 100.5 m³ | 4 m diameter × 8 m height |
| Provisional internal tank volume | 96.8 m³ | Assumed 25 mm radial wall and 100 mm total height deduction |
| Current working acceptance | 72.6 m³ | 20% freeboard and 5% heel reserved separately |
| Expansion-only remaining acceptance | 47.1 m³ | After all-hot expansion, with tank initially at heel |
| Hot full-drain shortfall | 462.8 m³ | Before adding an inventory uncertainty allowance |

Normal expansion would raise the liquid level about **1.60 m** in the assumed 3.95 m internal diameter. No level setting is selected by this result. Any existing tank contents above the heel reduce the available acceptance volume one-for-one.

A full-drain space reservation with **10% inventory uncertainty**, **20% freeboard** and **5% heel** requires approximately **785 m³ internal geometric storage**. At the same 8 m external height and provisional wall/end allowances, one equivalent cylinder would be approximately **11.3 m bare outside diameter**. This is roughly **8.1 times the working capacity** of the current tank (nine identical tanks would be required if no larger tanks were used). It is a space comparison, not a recommendation for nine tanks or an adopted tank design. A larger receiver, multiple receivers, or a separate bulk storage area needs a layout decision.

## Sensitivity

| Change, applied individually | Circuit volume |
| --- | ---: |
| Existing 19.879 m SG tube basis | 508.5 m³ |
| Use 17 m SG tube length instead | 492.4 m³ |
| No pump-cavity credit | 491.9 m³ |
| Entire pump envelopes counted as liquid | 525.1 m³ |
| Deduct 10% from gross reactor plenums/downcomer | 492.1 m³ |

Even the 17 m SG tube case contains **94.9 m³** of salt in the three generators alone, exceeding the **72.6 m³** current working tank capacity. None of these individual variations changes the full-drain conclusion.

Raising the assumed fill temperature from 450°C to 500°C changes the fixed charge: normal expansion falls to **11.2 m³**, and hot full-drain volume to **526.5 m³**. These are alternative charge definitions, not different temperatures applied to the same unchanged charge. The worksheet separately tests receiving temperature with charge held fixed.

## Checks and reproduction

- Pure-Python assembly resolution checks shared P&ID tags/bores and regenerates the route coordinates without Blender.
- Arc lengths follow the current CAD fillet radius/trim rules. Using corner polylines instead would add approximately 18.9 m³, which is not silently included in the rounded-route inventory.
- Volume grouping and fixed-mass balances close. Full drain is the remaining circuit mass plus expansion mass already transferred; expansion is not counted twice.
- Hurmet 0.1.1 recalculated **64 numerical results**, saved/reopened the worksheet, and passed tank-diameter, fill-temperature and storage-temperature sensitivities. [Check record](coolant-inventory-hurmet-checks.json).
- [Python source](coolant_inventory.py) and [inputs/results/source hashes](coolant-inventory-results.json) retain the calculation basis. The pressure-control draft is not changed by this inventory calculation.

From the repository root:

```sh
python3 calculations/reactor/coolant_inventory.py
HURMET_ENGINE=/path/to/hurmet.cjs TEMML_ENGINE=/path/to/temml.cjs \
  node calculations/reactor/check_coolant_inventory.cjs
```

The Python publisher refreshes geometry inputs and resets the baseline worksheet from documented assumptions. Direct worksheet changes remain possible in Hurmet; a reviewed Python/check baseline update is needed before comparing changed inputs against the old expected results. Preview HTML is generated under ignored `outputs/coolant-inventory/`.

No graphical tank, building, P&ID state or protection setting has been changed. Usable internal capacity, actual charge, receiving temperatures, pressure/gas handling, thermal conditioning and complete drainage remain engineering work. The current volume estimate is sufficient to flag that the modeled TK-401 is not a full-system drain receiver.
