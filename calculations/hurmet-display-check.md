# Hurmet units and display check — 20 October 2026

Updated all 29 working Hurmet worksheets in `reactor`, `steam-generator`
and `power-cycle`. Archived `revisions` and published research snapshots are
unchanged. This is a presentation and unit-notation update.

## Changes

- One `format = "h3"` cell immediately after each title.
- `%%` unit-aware result selectors suppress substituted-value repetition.
- Explicit units throughout the absorber capacity sheet, replacing scalar SI
  arithmetic and manual litre/kPa conversion factors with Hurmet conversions.
- Large pressure literals converted to kPa or bar, and enthalpy literals to
  kJ/kg, without rounding inputs. Generator ratings now carry MW/MVA units.
- Shared publication helpers keep regenerated sheets in the same format.
  Numerical tests use `h15` internally and publish `h3` only after checking.
- Invalid table-width metadata from Hurmet serialization is removed; the
  existing open-air Brayton pipe-table conversion is preserved for VS Code.

## Verification

All **928 saved results across 29 sheets** were compared before and after
conversion using the same official Hurmet engine at high precision. Dimensional
conversions were accounted for; Boolean results and result counts were also
compared. Numeric differences were within `max(1e-9, abs(original) × 1e-10)`.
All sheets recalculated, reopened and rendered without Hurmet calculation errors.

The existing **23 worksheet checkers** also passed their numerical comparisons,
round-trip checks, sensitivities and invalid-input guards where provided. Their
numerical tolerances were not relaxed. The absorber checker now compares its
kPa results to the original Pa reference values after conversion.

The official Hurmet bundle used for these checks was downloaded from
[Hurmet's repository](https://github.com/ronkok/Hurmet/tree/master/utils).
Its SHA-256 is
`97bbc0c4107d05f817e2ff6f2212d448355603c57d9171edcc541f01e560c96a`.
The matched Temml bundle SHA-256 is
`21cddf155e94f5848186379b4c1dbc14f3a3492a223c20ccf4cb28261e47cfe3`.
These identify the actual engine used here; this check does not claim to use
an earlier pinned engine or revalidate imported specialist-solver results.

For example, run an existing checker with these bundles:

```sh
HURMET_ENGINE=/path/to/hurmet.cjs TEMML_ENGINE=/path/to/temml.cjs \
  node calculations/reactor/check_absorber_capacity.cjs
```

The helpers also need Python 3 from `PATH` (or the `PYTHON` environment variable).

## Working sheets checked

| Worksheet | Saved results compared |
| --- | ---: |
| [Absorber capacity and gas modules - Hurmet.md](reactor/Absorber%20capacity%20and%20gas%20modules%20-%20Hurmet.md) | 60 |
| [Coolant inventory and storage capacity - Hurmet.md](reactor/Coolant%20inventory%20and%20storage%20capacity%20-%20Hurmet.md) | 67 |
| [Core coolant pressure loss - Hurmet.md](reactor/Core%20coolant%20pressure%20loss%20-%20Hurmet.md) | 35 |
| [Maintenance fuel tank capacity - Hurmet.md](reactor/Maintenance%20fuel%20tank%20capacity%20-%20Hurmet.md) | 6 |
| [Normal coolant pressure profile - Hurmet.md](reactor/Normal%20coolant%20pressure%20profile%20-%20Hurmet.md) | 53 |
| [Reactor top insulation - Hurmet.md](reactor/Reactor%20top%20insulation%20-%20Hurmet.md) | 32 |
| [Rigid cover cassette - Hurmet.md](reactor/Rigid%20cover%20cassette%20-%20Hurmet.md) | 18 |
| [T-grid cover - Hurmet.md](reactor/T-grid%20cover%20-%20Hurmet.md) | 17 |
| [Zirconia cover supports - Hurmet.md](reactor/Zirconia%20cover%20supports%20-%20Hurmet.md) | 8 |
| [Coolant pump estimate - Hurmet.md](steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md) | 11 |
| [Generator sizing - Hurmet.md](steam-generator/Generator%20sizing%20-%20Hurmet.md) | 79 |
| [Itemized coolant pump estimate - Hurmet.md](steam-generator/Itemized%20coolant%20pump%20estimate%20-%20Hurmet.md) | 62 |
| [Molten-salt coolant insulation - Hurmet.md](steam-generator/Molten-salt%20coolant%20insulation%20-%20Hurmet.md) | 30 |
| [Molten-salt coolant pipe wall - Hurmet.md](steam-generator/Molten-salt%20coolant%20pipe%20wall%20-%20Hurmet.md) | 22 |
| [Steam and feedwater insulation - Hurmet.md](steam-generator/Steam%20and%20feedwater%20insulation%20-%20Hurmet.md) | 41 |
| [Steam and feedwater pipe sizing - Hurmet.md](steam-generator/Steam%20and%20feedwater%20pipe%20sizing%20-%20Hurmet.md) | 80 |
| [BFP drive comparison - Hurmet.md](power-cycle/BFP%20drive%20comparison%20-%20Hurmet.md) | 12 |
| [Brayton cooler size comparison - Hurmet.md](power-cycle/Brayton%20cooler%20size%20comparison%20-%20Hurmet.md) | 12 |
| [Brayton fan and salt pump balance - Hurmet.md](power-cycle/Brayton%20fan%20and%20salt%20pump%20balance%20-%20Hurmet.md) | 17 |
| [Brayton-driven salt pump - Hurmet.md](power-cycle/Brayton-driven%20salt%20pump%20-%20Hurmet.md) | 32 |
| [Cooling-water cases - Hurmet.md](power-cycle/Cooling-water%20cases%20-%20Hurmet.md) | 25 |
| [Motor-BFP equipment sizing - Hurmet.md](power-cycle/Motor-BFP%20equipment%20sizing%20-%20Hurmet.md) | 50 |
| [Nitrogen versus steam Brayton - Hurmet.md](power-cycle/Nitrogen%20versus%20steam%20Brayton%20-%20Hurmet.md) | 11 |
| [Open-air Brayton cooler - Hurmet.md](power-cycle/Open-air%20Brayton%20cooler%20-%20Hurmet.md) | 10 |
| [Power plant equipment sizing - Hurmet.md](power-cycle/Power%20plant%20equipment%20sizing%20-%20Hurmet.md) | 73 |
| [Rankine cycle - Hurmet.md](power-cycle/Rankine%20cycle%20-%20Hurmet.md) | 20 |
| [Selected reheat and wetness - Hurmet.md](power-cycle/Selected%20reheat%20and%20wetness%20-%20Hurmet.md) | 14 |
| [Simple CO2 Brayton cooler - Hurmet.md](power-cycle/Simple%20CO2%20Brayton%20cooler%20-%20Hurmet.md) | 12 |
| [Steam Brayton cooler - Hurmet.md](power-cycle/Steam%20Brayton%20cooler%20-%20Hurmet.md) | 19 |
