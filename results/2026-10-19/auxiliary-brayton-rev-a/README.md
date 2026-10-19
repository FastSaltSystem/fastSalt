# RS-008: Auxiliary Brayton Cooling Options

**Revision A - 19 October 2026 - Preliminary Comparative Study**

[Read the PDF](report.pdf) · [Browser report](report.html) · [Editable Markdown](report.md) · [File manifest](manifest.json)

A preserved comparison of closed steam, closed nitrogen, open air and a simple supercritical CO₂ loop, using the existing 30 MW-per-train cases. No new thermodynamic calculations or equipment selection were made for this issue. This is a local study snapshot; GitHub publication is a separate step.

## Contents and provenance

- `sources/calculations/power-cycle/`: worksheets, Python generators, JavaScript Hurmet checkers, saved results, existing check records and overview.
- `sources/calculations/steam-generator/`: original generator-sizing worksheet referenced by the studies.
- `manifest.json`: actual snapshot hashes, base commit, working-copy status and packaging dependencies. The base commit does not contain all the archived working files.
- `source-hash-audit.json`: comparison of historical result provenance hashes with the archived source copies. Mismatches are retained openly, not repaired by changing original evidence.
- `render_report.py`: report renderer. Set `STUDY_FONT_DIR` to a directory containing DejaVuSans.ttf and DejaVuSans-Bold.ttf, then run with Python and ReportLab installed. This renders the report only.

## Recalculation in a disposable copy

Install the versions in `sources/calculations/power-cycle/requirements.txt`. Set `HURMET_ENGINE` and `TEMML_ENGINE` to the externally installed engine files. Work in the copied `sources/calculations/power-cycle` directory, preserving its sibling `steam-generator` directory.

1. `python brayton_cooler.py`, `python publish_brayton_cooler.py`, `node check_brayton_hurmet.cjs`.
2. `python brayton_salt_pump.py`, `node check_brayton_salt_pump.cjs`.
3. `python brayton_fan_pump_balance.py`, `node check_brayton_fan_pump.cjs`.
4. `python nitrogen_brayton.py`, `python publish_nitrogen_brayton.py`, `node check_nitrogen_brayton.cjs`.
5. `python open_air_brayton.py`, `node check_open_air_brayton.cjs`.
6. `python brayton_size_screen.py`, `node check_brayton_size.cjs`.
7. `python co2_brayton.py`, `node check_co2_brayton.cjs`.

Scripts overwrite their outputs. The overview and report are editorial summaries and must be reconciled manually after any numerical change. Historical check records describe their original runs; packaging does not assert they were rerun. Preserve Revision A and issue a new revision for changed assumptions or results.
