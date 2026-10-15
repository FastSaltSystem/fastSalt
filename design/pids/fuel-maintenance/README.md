# WISTR fuel-maintenance P&ID

Revision B3 draft, 15 October 2026. This replaces the earlier annotated illustration with a connected, tagged P&ID. The original drawing remains a reference; the owner's subsequent descriptions control the additions and clarifications.

- [Three-sheet P&ID PDF](outputs/current/WISTR-fuel-maintenance-PID.pdf)
- [Sheet 1: fuel transfer and pressure valves](outputs/current/FS-FM-001.svg)
- [Sheet 2: gas services and metering pumps](outputs/current/FS-FM-002.svg)
- [Sheet 3: valve positions, operating states and tag schedule](outputs/current/FS-FM-003.svg)
- [Equipment](outputs/current/equipment.csv), [instruments](outputs/current/instruments.csv), [valves](outputs/current/valves.csv), [lines](outputs/current/lines.csv), [signals](outputs/current/signals.csv) and [sector tag schedule](outputs/current/sector-tag-schedule.csv)

## Arrangement shown

Sheet 1 shows one representative sector's R1/R2, R3/R4 and R5/R6 circuits and the corresponding A/B/C storage regions in TK-FM-01. Each storage region has level and pressure sensing, and each bottom transfer line has gas-presence sensing. Core and storage selectors each have four positions, including Vent to off-gas. The storage-side off-gas position is used only when selected by the operator and is excluded from automatic fuel-transfer sequences. The selector circle denotes the complete multiport selection function; it does not show a fixed open path between all ports.

Matching HP, HS and OG markers connect to the pressure vessel, surge vessel and off-gas connection on sheet 2. PCV-FM-01 is removed. Each shared unit uses its two tank pressure measurements to start/stop its compressor and control their pressure difference. Sheet 2 details unit 3 (V-FM-05/06, K-FM-03, PDC-FM-03 and PT-FM-95/96), because sector 1 belongs to that existing 3D tank pair. Both pressure and surge headers branch to TK-FM-01 and TK-FM-06 valve banks. Dashed lines show the control signals. G-FM-94 supplies the surge vessel from the existing supply interface in the off-gas treatment room through the modeled common supply header and unit branch. The separate off-gas header returns to the treatment room through the same shared duct. FA brings measured fuel addition to the R5/R6 storage side. FR takes measured removal from the **R1/R2 core fuel line**, as explicitly clarified on 15 October. The cooling enclosure's fresh-air and exhaust interfaces remain on sheet 2.

The six-sector schedule expands the three circuits to 18 core selectors, 18 storage selectors and 18 each of storage level, storage pressure and bottom-line gas sensing. One pressure vessel, surge vessel and controller/compressor unit serves two maintenance tanks: three units total. The 3D server pairs and existing provisional sector-to-tank mapping are retained:

| Gas unit / 3D server | 3D tanks | P&ID tanks | Core sectors |
| --- | --- | --- | --- |
| 1 / P1 | F1, F2 | TK-FM-02, TK-FM-03 | 2, 3 |
| 2 / P2 | F3, F4 | TK-FM-04, TK-FM-05 | 4, 5 |
| 3 / P3 | F5, F6 | TK-FM-06, TK-FM-01 | 6, 1 |

The [pressure-unit schedule](outputs/current/pressure-unit-schedule.csv) assigns each unit its own vessel, controller, compressor and pressure-sensor tags. The [3D interface register](outputs/current/3d-interface-register.csv) records the existing model objects: `site.fuel_pressure.supply_common`, `site.fuel_pressure.offgas_common`, each server supply/return branch and `equipment.fuel_pressure_server_1..3`. The supply-room enclosure is `site.offgas_gas_supply.enclosure`, separate from the treatment train. References: [D-035 sector/tank mapping](../../interfaces.md#sector-to-maintenance-tank-services--d-035) and [existing 3D pressure servers](../../../../fastSaltModels/docs/site-study.md#fuel-pressure-servers-and-nitrogen-relocation--d-047).

This is a cross-reference to existing modeled interfaces, not a claim that the server interiors or all instrumentation are modeled in detail. Metering-pump sharing remains unspecified.

## Editable sources

| File | Purpose |
| --- | --- |
| `fuel-maintenance.toml` | Owner statements, operating states, instrumentation requirements and provenance |
| `pid.toml` | Document metadata, equipment tags, circuit identities and tag templates |
| `layout.toml` | Page dimensions, circuit-column offsets and header elevations |
| `build.py` | Connected drawing templates, vector PDF/SVG rendering, registers and checks |

Run `python3 design/pids/fuel-maintenance/build.py` from the repository root using Python 3.11+ with ReportLab. The PDF has native vector lines and selectable text, sized for A2 landscape; SVGs are editable. Generated outputs remain ignored by Git. The renderer no longer needs Node or Sharp.

The build checks unique tags, declared route endpoints, orthogonal routes, sector counts, recorded valve-position counts and original-source identity. `outputs/current/pid-checks.json` records input hashes and the resolved routes. Visual review checks the PDF after generation.

## Notation and open details

The sheets use conventional tagged equipment, instrument bubbles, piping, connection markers and a title block. [ISA5.1 public guidance](https://www.isa.org/standards-and-publications/isa-standards/isa5-1) is the notation reference. LT/PT denote level/pressure sensing functions; GD is an explicitly defined project designation for gas-presence detection. SEL is the multiport selector function. This draft does not claim full compliance with the purchased standard.

Solid heavy lines are process piping; solid thin instrument connections identify the measured process location. A dot means a junction. Other crossings do not connect. Dashed signal lines show the owner-specified compressor start/stop function, using the two existing pressure measurements. They do not specify wiring or a controller implementation. Core boxes are functional paired-region boundaries, not detailed internal geometry.

Compressor pressure-difference setpoint and switching band, detailed gas-interface hardware, equipment ratings, pipe specifications, fail positions, detailed controls, external fuel source/destination tie-ins, and distribution specifically to R6 within the R5/R6 pair remain TBD. The existing owner-described state conditions are retained without inventing extra sequences. The 3D model and numerical calculations are unchanged.

## Earlier draft

The previous seven-sheet source-transcription generator, TOML and reference SVG are preserved under [revisions/source-transcription-A5](revisions/source-transcription-A5/). That historical generator can be run separately from this current P&ID. The supplied original SVG is unchanged under `sources/`.
