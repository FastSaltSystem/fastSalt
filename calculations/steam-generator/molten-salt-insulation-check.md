# Molten-salt coolant insulation verification

11 October 2026. Preliminary straight-pipe thermal estimate.

[Editable Hurmet worksheet](Molten-salt%20coolant%20insulation%20-%20Hurmet.md).
No graphics changes or pressure-wall selection are included.

## Basis and results

Three coolant loops, with hot coolant 875 K (601.85°C) and return coolant
810 K (536.85°C), from the generator worksheet. A provisional 1.5 m bare outside
diameter accommodates the approximately 1.4002 m required bore plus an unresolved
wall allowance. This does not establish a 50 mm pressure-wall thickness.

Same environmental basis as the steam/feedwater estimate: 40°C air and radiant
surroundings, convection 4 W/(m² K), metal-jacket emissivity 0.20, and 60°C target
surface temperature. Dry calcium-silicate effective conductivity 0.090 W/(m K)
for both legs is a rounded screening assumption. Temperature-dependent property
changes and environmental conditions must be reviewed before final selection.

| Case | Minimum thickness, mm | Selected thickness, mm | Insulated OD, m | Jacket temperature, °C | Heat loss, W/m |
| --- | ---: | ---: | ---: | ---: | ---: |
| Hot leg | 364.00 | 400 | 2.30 | 58.04 | 719.43 |
| Cool return | 325.64 | 350 | 2.20 | 58.51 | 706.27 |
| Optional common thickness on return | 325.64 | 400 | 2.30 | 56.00 | 636.14 |

Radial thicknesses are rounded upward in 50 mm layout increments. The optional
400 mm common thickness matches the hot-leg allowance. Thin jacketing, tracing
space, bands and installation clearance are additional. On a 1.4 m bare OD,
minimum thicknesses would be 360.64 / 322.81 mm: the selected layout thicknesses
are unchanged, but 1.4 m bare OD does not meet the prior bore requirement.

Assuming three 15 m hot routes and three 15 m complete cool-return routes,
straight-pipe loss is **64.16 kW**, or **61.00 kW** with 400 mm on both services.
Each return length includes generator-to-pump plus pump-to-reactor; it is counted
once. No external common headers are included. These are illustrative route
budgets, not measured lengths or a whole-building ventilation calculation.

## Sensitivity at fixed 400 / 350 mm thickness

| Changed condition | Hot jacket, °C | Return jacket, °C |
| --- | ---: | ---: |
| Base | 58.04 | 58.51 |
| Air and radiant surroundings 50°C | 67.30 | 67.70 |
| Convection 2 W/(m² K) | 67.29 | 67.90 |
| Jacket emissivity 0.10 | 60.77 | 61.29 |
| Coolant temperatures increased 25 K | 58.83 | 59.42 |
| First three adverse changes combined | 82.88 | 83.48 |

The 25 K increase is an illustrative sensitivity, not an adopted design
condition or accident calculation. A 60°C screening target does not certify
safe contact. Insulation bridges, pumps, valves, flanges, supports, moisture,
aging and nearby hot radiant surfaces are excluded. Insulation alone does not
prevent stagnant-salt freezing: preheat, tracing, draining and freeze protection
require separate analysis. No liquidus, tracing duty or cooldown time is inferred.

## Checks and reproduction

- Official Hurmet runtime recalculated all 30 saved numeric result cells without errors.
- Independent SI Newton solves agree with Hurmet's bisection to saved seven-digit precision.
- Independent conductive/external heat balances close within 0.0000001 W/m.
- All 30 results survive a Hurmet save/reload unchanged.
- Higher ambient temperature, higher conductivity and lower emissivity increase
  required hot-leg thickness. Invalid ambient/target ordering is rejected.

```sh
python3 calculations/steam-generator/checks/verify_salt_insulation.py
HURMET_ENGINE=/path/to/hurmet.cjs node calculations/steam-generator/checks/check_salt_insulation_hurmet.cjs
```

Use the matching `temml.cjs` alongside `hurmet.cjs`. Runtime version is 0.1.1.
The generated offline preview is
`outputs/molten-salt-insulation/molten-salt-insulation.html` (ignored by Git).

The candidate insulation reference is [JM Thermo-1200 data sheet, 8 April 2025](https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM_IND_Thermo-1200_DS.pdf):
650°C maximum service temperature; pipe-test conductivity 0.085 W/(m K) at 316°C
mean and 0.093 at 371°C. This establishes a thermal reference, not qualification
for molten-salt leakage or plant transient conditions.

Inputs are copied, not linked. Source snapshot SHA-256 values:

- Generator sizing - Hurmet.md: `c43db3790ba8e3346253e4c9faf00d4ee643b1f348d8aad0e25c39083a359c04`

- Coolant pump estimate - Hurmet.md: `31445e71b66881cec2823ea5b8068a2bf316ff67227f470c3611ea3d903df8b1`

- Steam and feedwater insulation - Hurmet.md: `bcb8cc9cc4066b8f0a87fd958100497086d185ede18b562ef338c68ab655baf1`

- hurmet.cjs: `24c325bee542762dad7b1dcd3dd943a5518cb549a44e8e2f1aa4e0abcfc4ebf1`
