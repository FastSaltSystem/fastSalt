# Steam/feedwater pipe sizing — verification

11 October 2026. [Editable Hurmet worksheet](Steam%20and%20feedwater%20pipe%20sizing%20-%20Hurmet.md).

## Results and status

| Service | Bore, mm | Nominal wall, mm | Bare OD, mm | Velocity, m/s | Piping loss, kPa |
| --- | ---: | ---: | ---: | ---: | ---: |
| Steam branch | 425 | 115 | 655 | 22.7140 | 122.105 |
| Steam header | 725 | 195 | 1115 | 23.4163 | 229.461 |
| Feedwater branch | 375 | 75 | 525 | 2.80908 | 19.6178 |
| Feedwater header | 650 | 120 | 890 | 2.80493 | 34.8031 |

These are conditional custom-dimensional envelopes, not selected standard
schedules or certified pressure ratings. The owner approved provisional inputs:
30 MPa gauge design pressure; assumed stress 80 MPa steam / 120 MPa water;
600°C / 325°C design temperatures; seamless E=W=1; ferritic y=0.7 / 0.4;
3 mm allowance; 12.5% negative wall tolerance. No named material is assigned
these stress values. They must be replaced with verified values from the chosen
material/code edition. Hydraulic properties retain the original 24 MPa absolute
basis. Design pressure must be reconciled with pump shutoff and transients.

## Numerical checks

- All 138 Hurmet cells recalculate without errors; the saved Markdown was
  reopened and recalculated, including its live summary table.
- Python independently checks 80 unique saved values, including flow, both
  bore criteria, rounded bore, velocity, Reynolds number, Darcy factor, loss,
  nominal and minimum walls, rounded OD, pressure capacity and Boolean checks.
  The independent Colebrook solution uses bisection, rather than Hurmet's
  fixed-point iteration. Comparison tolerance covers seven-significant-digit
  display rounding (relative 6e-7, absolute 5e-8 in displayed units).
- Pressure-only wall inequalities are rechecked at the final rounded OD and
  minimum delivered wall; all four pass the stated relation and assumptions.
- Steam-header nominal wall changes from 195 to 240 mm at 36 MPa, and to
  275 mm when assumed stress decreases to 60 MPa.
- A 15 m/s steam limit increases header bore from 725 to 925 mm.
- Four generators reduce steam branch bore from 425 to 375 mm at fixed total
  thermal duty; total header mass flow is unchanged.
- An invalid pressure/stress combination is rejected by the worksheet guard.

The full header is treated at full combined flow over an assumed 90 m and K=10;
branches use 15 m and K=6. Steam path bound is 351.566 kPa (1.465% of the
property pressure); feedwater bound is 54.421 kPa. This is not a solved network,
includes no internal generator or collector loss, and does not update properties
as pressure and temperature change. The pressure-wall relation was checked in
ASME B31.1-2020 §104.1.2(a); adoption of that edition is not implied.

## Reproduction

From the project root:

```sh
python3 calculations/steam-generator/checks/verify_pipe_sizing.py
HURMET_ENGINE=/path/to/Hurmet/utils/hurmet.cjs node calculations/steam-generator/checks/check_pipe_hurmet.cjs
```

The Hurmet check also uses `temml.cjs` beside `hurmet.cjs`. The engine is the
official [Hurmet source](https://github.com/ronkok/Hurmet), version 0.1.1,
from the previously prepared local conversion runtime.
Engine bundle SHA-256: `24c325bee542762dad7b1dcd3dd943a5518cb549a44e8e2f1aa4e0abcfc4ebf1`.
Generator source SHA-256: `c43db3790ba8e3346253e4c9faf00d4ee643b1f348d8aad0e25c39083a359c04`.

For editing, open the `.md` in Hurmet, change inputs and recalculate. The HTML
preview is a generated snapshot in ignored `outputs/steam-water-pipe-sizing/`.
It does not edit the worksheet. Existing generator/pump sheets and Blender
geometry are unchanged.
