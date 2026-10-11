# Steam and feedwater insulation verification

11 October 2026. Preliminary calculation, not an approved specification.

## Results

The [Hurmet worksheet](Steam%20and%20feedwater%20insulation%20-%20Hurmet.md)
selects a common radial thickness for each service: **350 mm steam and 175 mm
feedwater**, with dry calcium-silicate effective conductivity 0.090 and
0.075 W/(m K), respectively. This is conditional on 40°C air/radiant surroundings,
external convection 4 W/(m² K), emissivity 0.20, and a 60°C surface target.
Selections cover provisional check temperatures 600°C steam and 325°C feedwater.

| Service | Bare OD, mm | Insulation, mm | Insulated OD, mm | Operating surface, °C | Check surface, °C | Operating loss, W/m |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Steam branch | 655 | 350 | 1355 | 56.60 | 57.95 | 389.2 |
| Steam header | 1115 | 350 | 1815 | 58.38 | 59.88 | 578.5 |
| Feedwater branch | 525 | 175 | 875 | 54.22 | 56.37 | 214.6 |
| Feedwater header | 890 | 175 | 1240 | 55.36 | 57.68 | 328.9 |

The unrounded operating-only minima are 297.6 / 324.2 mm steam and
127.0 / 135.1 mm feedwater (branch / header). A 25 mm increment would give
300 / 325 mm steam and 150 / 150 mm feedwater. Higher check temperatures and
a uniform service thickness produce the 350 / 175 mm layout allowance.
At operating temperatures (556.85°C steam, 286.85°C water), three 15 m branches
and one 90 m header per service give **108.84 kW** combined straight-pipe loss.
Lengths remain provisional. Thin metal cladding and fitting clearances are omitted.

## Sensitivities and limitations

At selected thickness and the higher check temperatures, common-header jacket
temperatures are:

| Case | Steam, °C | Feedwater, °C |
| --- | ---: | ---: |
| Base | 59.88 | 57.68 |
| 50°C room and radiant surroundings | 69.05 | 66.67 |
| Convection reduced to 2 W/(m² K) | 69.92 | 66.36 |
| Emissivity reduced to 0.10 | 62.89 | 60.26 |
| All three adverse changes | 86.03 | 80.89 |

A 60°C target is not a universal safe-touch limit. Room and radiant temperatures,
jacketing, air movement, acceptable heat loss and actual pipe sizes need confirmation.
Constant effective conductivities are conservative screening choices over these
cases, not a universal property law. The model excludes wetting, degradation,
bridges, fittings and adjacent hot equipment. No economics, burn-contact-time,
transient, final installation or code-compliance analysis is implied.

## Verification and reproduction

- Recalculated with the official Hurmet 0.1.1 bundle; HTML contained no calculation errors.
- All **41 numeric result cells** agreed with an independent SI calculation using
  Newton solves, versus Hurmet's bisection, within seven-significant-digit rounding.
- Independent checks also enforce conductive/external heat-balance closure.
- Hurmet save/reload preserved all 41 results.
- Higher ambient temperature, higher conductivity and lower emissivity each
  increased selected steam thickness; invalid ambient/target ordering was rejected.
- Conductivity/source data: [JM Thermo-1200 data sheet, 8 April 2025](https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM_IND_Thermo-1200_DS.pdf).
- Surface target context: [NIA Design Objectives](https://insulation.org/training-tools/designguide/design-objectives/).

Run from the repository root:

```sh
python3 calculations/steam-generator/checks/verify_insulation.py
HURMET_ENGINE=/path/to/hurmet.cjs node calculations/steam-generator/checks/check_insulation_hurmet.cjs
```

Place the matching `temml.cjs` beside the Hurmet bundle. Runtime paths are local
tools, not dependencies committed into this repository. The generated standalone
preview is `outputs/steam-water-insulation/steam-water-insulation.html` (ignored).

Source pipe worksheet SHA-256: `50f0f4142050675a98aba2ea65c241c812dc5087839a7055f4bf05b3a0d605fe`.
Hurmet bundle SHA-256: `24c325bee542762dad7b1dcd3dd943a5518cb549a44e8e2f1aa4e0abcfc4ebf1`.
Inputs are copied from that source revision; they do not update automatically.

No Blender dimensions were changed. The estimate does not size molten-salt insulation.
