# Molten-salt coolant pipe wall verification

11 October 2026. [Editable Hurmet worksheet](Molten-salt%20coolant%20pipe%20wall%20-%20Hurmet.md).
Preliminary straight-pipe pressure estimate; no alloy or construction specification selected.

## Base case

Per-circuit flow 4.619533 m³/s and 3 m/s limit give minimum bore 1.400211 m,
rounded to 1.425 m. Gauge design pressure 1 MPa, effective stress including weld
factors 50 MPa, y = 0.40, allowance 3 mm and negative tolerance 12.5% give:

| Result | Value |
| --- | ---: |
| Required nominal wall | 20.03944 mm |
| Nominal wall rounded upward by 5 mm | 25 mm |
| Bare outside diameter | 1.475 m |
| Velocity | 2.896533 m/s |
| Minimum delivered wall at assumed tolerance | 21.875 mm |
| Equation-only pressure capacity at selected OD | 1.292897 MPa |
| OD with 400 mm radial insulation | 2.275 m |
| OD with 350 mm radial insulation | 2.175 m |

The base-case pressure check passes the assumed straight-pipe relation only.
The pressure capacity is not a system MAWP. The 1 MPa pressure case is not an
established design pressure, and the assumed effective stress is not tied to a
selected alloy, code-table allowable or service life. The worksheet includes
all comments about cover-gas pressure, static head, pump shutoff, tube-failure
pressurization, corrosion, creep, welds, support loads, expansion and buckling.

Pressure sensitivities at 0.5 / 1 / 2 MPa give unrounded nominal requirements
11.67185 / 20.03944 / 37.15901 mm. At 1 MPa and effective stress 30 MPa the
requirement becomes 31.39453 mm. Thus 25 mm is a conditional concept choice.
The prior insulation worksheet's 1.5 m bare OD envelope is retained; graphics
are unchanged. Actual dimensions and delivered bore need procurement checks.

## Verification

- Recalculated with official Hurmet 0.1.1; rendered HTML contains no calculation errors.
- All 21 numerical cells and one Boolean agree with independent SI calculations
  to saved seven-significant-digit precision.
- Independent wall calculation uses bisection on the original delivered-wall
  inequality, rather than the worksheet's algebraically rearranged nominal-wall formula.
- The inverse pressure-capacity calculation closes the original wall relation.
- Save/reload leaves all 22 result cells unchanged.
- Changing design pressure to 2 MPa selects 40 mm and passes the rounded-wall recheck.
- Reducing effective stress to 30 MPa selects 35 mm and passes that recheck.
- Zero effective stress is rejected by the Hurmet input guard.

Run from the repository root:

```sh
python3 calculations/steam-generator/checks/verify_salt_wall.py
HURMET_ENGINE=/path/to/hurmet.cjs node calculations/steam-generator/checks/check_salt_wall_hurmet.cjs
```

Place matching `temml.cjs` beside the Hurmet bundle. The generated standalone
preview is `outputs/molten-salt-pipe-wall/molten-salt-pipe-wall.html` (ignored).
Inputs are copied, not linked. Reproduction source SHA-256 values:

- Coolant pump estimate - Hurmet.md: `31445e71b66881cec2823ea5b8068a2bf316ff67227f470c3611ea3d903df8b1`

- Generator sizing - Hurmet.md: `c43db3790ba8e3346253e4c9faf00d4ee643b1f348d8aad0e25c39083a359c04`

- Molten-salt coolant insulation - Hurmet.md: `87ea2baefe4ae9bd28072d43d7c59159187f290d655f8b24182ee1923772258e`

- hurmet.cjs: `24c325bee542762dad7b1dcd3dd943a5518cb549a44e8e2f1aa4e0abcfc4ebf1`
