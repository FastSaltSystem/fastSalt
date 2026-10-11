# Reactor top insulation verification

Calculated 11 October 2026. Conditional allowance: **500 mm calcium silicate**
with no hood airflow credited. The graphics and air-system arrangement are
unchanged pending review of this concept.

## Results

| Quantity | Base result |
|---|---:|
| Hot face / room | 601.85°C / 40°C |
| Minimum to meet 60°C surface target | 416.2614 mm |
| Rounded minimum / selected allowance | 450 / 500 mm |
| Selected outer surface | 56.81795°C |
| Heat flux | 92.65545 W/m² |
| Gross top area | 53.36910 m² |
| Top heat loss | 4.944938 kW |
| Dry insulation mass, excluding metal | 6,404.293 kg |

| Sensitivity at 500 mm | Surface | Thickness for 60°C |
|---|---:|---:|
| Room and surroundings at 50°C | 66.12°C | 822 mm |
| External convection 2 W/(m² K) | 65.52°C | 652 mm |
| Emissivity 0.10 | 59.36°C | 483 mm |
| Hot face 625°C | 57.50°C | 434 mm |
| 50°C room, h = 2, emissivity 0.10 | 80.74°C | 1,644 mm |

These sensitivities demonstrate dependence on environmental assumptions, not
alternative qualified designs. See the worksheet for the flat-wall equations,
material source, limitations and distinction from vessel/well cooling.

## Checks and reproduction

All 32 saved numerical cells agree with an independent Python SI calculation
using Newton iteration, rather than the worksheet's bisection surface solver.
Tolerance is 6e-7 relative or 5e-8 absolute in each displayed unit. Residual heat
balances also close. Hurmet 0.1.1 recalculated without rendered error markers;
all values survive save/reload. Editing ambient to 50°C recalculates the selected
thickness to 900 mm and the surface below 60°C. A target below ambient triggers
the intended guard.

From this directory:

```sh
python3 checks/verify_reactor_top.py
node checks/check_reactor_top.cjs /path/to/hurmet.cjs /path/to/temml.cjs
```

The JS check needs the Hurmet CJS engine and Temml renderer; the Python check
uses only the standard library. Open the Hurmet Markdown worksheet to edit.
The generated HTML preview is in `outputs/reactor-top-insulation/` and is not
the maintained source. Current tool runtime: `/private/tmp/hurmet-conversion-source/utils/`.

## Source snapshots

Geometry uses the preserved report's `air_system.dimensions.partition_inner`;
its radius was checked directly against the copied worksheet input. Hot coolant
temperature comes from the generator worksheet. SHA-256 values at calculation:

- `/Users/thomaswielenga/Documents/dev/fastSalt/calculations/steam-generator/Generator sizing - Hurmet.md`: `c43db3790ba8e3346253e4c9faf00d4ee643b1f348d8aad0e25c39083a359c04`
- `/Users/thomaswielenga/Documents/dev/fastSaltModels/baselines/wistr-reactor-handling-2026-10-08/reactor-study-report.json`: `49d8b8a9cdf9996bc3b759d9462c4286e1861f3b22b0e7a7e35b299610e4f953`
- `/private/tmp/hurmet-conversion-source/utils/hurmet.cjs`: `24c325bee542762dad7b1dcd3dd943a5518cb549a44e8e2f1aa4e0abcfc4ebf1`
