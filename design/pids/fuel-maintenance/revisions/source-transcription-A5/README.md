# Fuel maintenance source-transcribed draft

15 October 2026. This first P&ID-style draft reformats the owner's supplied illustration and records the clarified grouping. It preserves the original source paths and adds the owner-specified instrumentation and valve functions on a supplemental sheet. Detailed engineering remains open.

- [Seven-sheet PDF](outputs/current/WISTR-fuel-maintenance-source-draft.pdf)
- [Representative sector SVG](outputs/current/FS-FM-001.svg)
- [Repetition and register SVG](outputs/current/FS-FM-002.svg)
- [Remove fuel state SVG](outputs/current/FS-FM-003.svg)
- [Fill fuel state SVG](outputs/current/FS-FM-004.svg)
- [Small fuel addition to R6 SVG](outputs/current/FS-FM-005.svg)
- [Measured removal from R1/R2 SVG](outputs/current/FS-FM-006.svg)
- [Instrumentation and off-gas position SVG](outputs/current/FS-FM-007.svg)
- [Editable TOML record](fuel-maintenance.toml)
- [Unmodified source SVG](sources/Fuel-Maintenance-original.svg)

## Confirmed grouping

There are six core sectors, each with six fuel regions. Within each sector, R1/R2, R3/R4 and R5/R6 form three pairs. Each pair has one shared core-pressure valve and one shared storage-pressure valve as drawn, and is associated with one of three storage regions in that sector's maintenance tank. The existing six maintenance-tank envelopes remain consistent with this count. Internal region geometry is not yet modeled.

The region numbers are local to a sector. The drawing is a representative sector and maintenance tank, not a depiction of only six regions across the entire reactor. The existing 3D tank F-number assignment is a separate cross-reference and is not reassigned here.

## Transcription scope

The original SVG is copied unchanged and identified by SHA-256 in the TOML. In the derivative sheet, the partial left-hand region label is replaced by R1 through R6 using the owner's clarification. The derivative valve legend now shows four core-valve positions, including Vent to off-gas, and three storage-valve positions. The original path attributes are checked for exact preservation. The compressor, gas vessels, two valve banks, two fuel pumps and air symbols remain as drawn. The reference index is a document index, not approved equipment tagging.

The third sheet records the owner-supplied Remove fuel state: core-pressure valves in Add pressure, maintenance-pressure valves in Reduce pressure, and the corresponding two valves returned to Maintain when gas appears in a bottom line. The original wording is retained in the TOML and on the sheet, including the completion statement. Maintenance-pressure valves refer to the source storage-pressure valve bank. Detection hardware is recorded on sheet 7; automation is not specified.

The fourth sheet records the owner-supplied Fill fuel state: maintenance-pressure valves in Add pressure and core-pressure valves in Reduce pressure. Gas appearing in the bottom line from a maintenance tank indicates that tank is empty; its corresponding core-pressure and maintenance-pressure valves return to Maintain. All valves are in Maintain when filling is complete. This completion description is retained verbatim in the TOML and on sheet 4.

Sheet 5 records a small fuel addition to R6: the add-fuel displacement pump meters fuel into the R5/R6 storage region, then the R5/R6 valves use the previously specified Fill fuel positions until gas is detected and both return to Maintain. The interpretation of "add fuel positions" is explicit. The route selecting R6 within the shared R5/R6 connection remains unspecified.

Sheet 6 records the owner-described measured removal of fuel from R1/R2 using the Remove fuel displacement pump. No valve positions, quantity or additional sequence are specified for this state.

Sheet 7 adds one level and pressure sensor per storage region and one gas sensor per bottom line (18 of each across six tanks); pressure sensing on the depicted pressure and surge tanks; and a pressure regulator between compressor and surge tank to set the pressure difference. The differential-pressure reference points and sensing connections remain unspecified. Core-pressure valves gain a fourth position, Vent to off-gas. Storage valves retain their three positions. These are functional symbols rather than assigned instrument tags. No extra control sequence or setpoints are inferred. Assignment/sharing of the source pressure tank, surge tank, compressor and fuel pumps across sectors remains open. External fuel-line destinations and detailed valve/instrument specifications are not supplied by this draft.

## Reproduction

Run `python design/pids/fuel-maintenance/build.py` from the repository root with Python 3.11+, ReportLab and a Node runtime containing Sharp. `NODE` can select the Node executable; `NODE_PATH` can select its package directory. Working PDF, SVG, PNG, CSV and check outputs are generated under `outputs/current/` and remain ignored.

The checks establish source identity and path preservation only. They are not process or equipment validation. The existing 3D model and all calculations are unchanged.
