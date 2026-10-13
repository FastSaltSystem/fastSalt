# WISTR coolant system: preliminary P&ID

Revision A, 13 October 2026. This is a discussion drawing based on the current coolant arrangement, with proposed measurement and isolation locations added for review. It is not an issued piping specification or an operating procedure.

## Preserved Revision A drawing package

- [Two-sheet A3 landscape PDF](WISTR-coolant-PID-rev-A.pdf).
- [FS-CS-001: circulation, editable SVG](FS-CS-001-rev-A.svg).
- [FS-CS-002: storage and transfer, editable SVG](FS-CS-002-rev-A.svg).
- [Instrument register](instruments.csv), [candidate valve register](valves.csv), and [line register](lines.csv).
- [Original Revision A build source](revisions/rev-A/build.py). The original PDF, SVGs and registers above remain unchanged.
- [Current working preview](outputs/current/WISTR-coolant-PID.pdf), regenerated from TOML; this ignored local file exists after a build.

The PDF and SVGs are deliberate review snapshots retained with their source. Temporary render images and font caches are not part of the package. The source manifest records hashes of the local references actually used; the references may include uncommitted working documentation. No research result is inferred from a Blender envelope.

## Working source and draft history

The current P&ID view source is [coolant-system.toml](coolant-system.toml). It imports main circulation equipment, connections and quantities from the [shared engineering model](../../engineering/README.md). Storage/transfer, instrumentation and valve proposals remain local. The independent [layout.toml](layout.toml) holds page coordinates, routes, label positions and explanatory captions. [build.py](build.py) validates both files and generates the PDF, SVGs and CSV registers. Markdown remains the explanation and review record. No engineering arrangement changed during this migration.

| Edit | File |
| --- | --- |
| Main circulation equipment, ports, connections, case inputs and dimensions | `../../engineering/coolant-system.toml` |
| Storage/transfer, measurement intent, proposal status and shared item sheet assignments | `coolant-system.toml` |
| Symbol locations, route points, drawing captions and label placement | `layout.toml` |
| Reasons, assumptions, open decisions and reviewer notes | `README.md` |
| Milestone history | `REVISIONS.md` |
| Rendering or validation behavior | `build.py` |

The TOML uses explicit units in field names. TOML has no `null`, so unresolved values are omitted and listed in that table's `unresolved_fields` array. The loader restores them as unresolved internally; zero must not be used to mean unknown. For example:

```toml
[lines.L-403]
od_mm = 50.0
heated = true
unresolved_fields = ["bore_mm", "wall_mm", "temperature_C"]
```

An assigned field cannot also appear in `unresolved_fields`; the loader rejects that conflict. This convention is specific to our model, not a TOML language feature. An endpoint such as `SG-101.salt_outlet` identifies equipment and its declared port. A line's `via = ["P-101"]` means the route enters the pump suction and leaves its discharge. This is connectivity, not a hydraulic solver. No Hurmet calculation has been translated or replaced.

Instrument `on` fields reference a line or equipment item; their descriptive `location` and `purpose` remain reviewable text. Valve and instrument status is `proposed` or `accepted_for_concept`. Neither means installed or qualified. Proposal symbols are amber; accepted concept symbols use the normal drawing color.

Layout labels can bind to model data, for example `${lines.L-101.temperature_C:.0f}`. Temperatures, SG duties and the displayed numerical basis use those bindings. Explanatory captions remain manually maintained, as does the Revision A numerical table below. Editing a topology requires updating the associated route and port anchors in the layout; this initial renderer does not automatically arrange or route equipment. It checks coolant endpoints, line-mounted instrument taps and valves against the referenced routes. It does not qualify physical geometry or automatically assess the prose.

### Build and check

Use Python 3.11 or newer, which includes the TOML parser. The dependencies are recorded in [requirements.txt](requirements.txt).

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py --check
.venv/bin/python build.py
.venv/bin/python -m unittest -v test_build.py
```

Run these commands from this directory. Builds default to `outputs/current/`, already excluded by the repository's `outputs/` ignore rule. Each build includes a manifest with hashes of its model, layout, renderer, shared engineering model/adapter and referenced worksheets. Use `--model`, `--layout` and `--output` for a separate experiment; `--check` validates without writing anything. The root output directory is rejected to protect the existing Revision A files.

Validation rejects duplicate TOML tables/keys, unknown equipment ports, missing required line fields, inconsistent bore/wall/OD values, omitted instruments or valves, and coolant routes or taps that disagree with the model. Eleven regression checks exercise those editing risks and confirm that an edited temperature reaches both the SVG and CSV.

### Review milestones

1. Edit TOML and Markdown, rebuild, and visually inspect both PDF pages. Review the Git diff to see exactly what changed.
2. Keep ordinary working builds in `outputs/current/`. Git tracks the source; there is no need to keep every exported PDF.
3. When a draft is ready to preserve, set its revision/date in the model and create a new `revisions/rev-B/` (or subsequent revision) directory. Keep copies of the view and shared model TOML, shared loader, layout TOML, renderer, requirements, review notes, calculation revisions/recoverable references, reference manifest and generated drawings/registers together. Never overwrite an earlier named revision.
4. Record the revision and change summary in `REVISIONS.md`, then commit the reviewed source and deliberate snapshot together when requested.

The existing Revision A deliverables remain at the package root for stable links. Their original renderer and a hash manifest are retained in `revisions/rev-A/`. The current source is labeled **A-working** to distinguish a regenerable working draft from that preserved package. The earlier YAML model, layout, renderer and dependencies are archived in [the YAML source snapshot](revisions/yaml-source-2026-10-13/README.md). The working renderer now uses TOML only. No engineering values or drawing contents changed, and no commit was made by this format migration.

## How to read the drawing

Solid lines are established process connections. Red identifies hot circulating coolant, blue the cool return, and dark lines storage/service salt. Arrows show the intended flow direction. Amber symbols identify proposed valves and measurements, rather than installed equipment. Dashed amber lines identify the measurement association; they do not prescribe impulse tubing, electrical wiring or a control signal.

Instrument letters are defined in the sheet legend. The public [ISA5.1 scope and purpose](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa5-1) provides background on consistent instrument identification. This drawing uses simplified project notation and does not claim compliance with the full standard. It assigns no control loops, interlocks, alarm/trip settings, safety classification, actuator selection or valve fail positions.

The reactor rectangle is a functional boundary. Alternating hot and cold ports down its right edge do not represent nozzle elevations. H1-H3 connect to the shared internal hot plenum; C1-C3 connect to the shared downcomer. There is no external common salt header. The internal route is downcomer, bottom plenum, bottom reflector/core coolant tubes/top reflector, hot plenum. Fuel is separate from this coolant.

Each cold leg runs from the steam generator into the bottom of its main pump and from the pump discharge to the reactor. L-201/202/203 each cover the complete cold route, on both sides of a pump; a later line-class/pressure-boundary issue should split these into segments. SG secondary connections identify the power-cycle boundary only. Secondary instrumentation, air passages and emergency cooling circuits are outside this first sheet's scope.

Sheet 2 retains the established reactor-bottom-to-storage transfer direction and a separate preparation-to-storage bottom connection. Its vertical arrangement is schematic, not proof of slope, drainage or suction head. No reverse pumping, refill line, check valve, vent destination or relief device has been invented.

## Equipment identification

These stable shared IDs leave Blender object names intact. SG/P-101, 102 and 103 map to graphics pairs 1, 2 and 3 at 180°, 60° and 300°. Main circulation data now feeds both views (D-053); changes appear after rebuilding. Other systems remain outside this migration.

| Drawing tags | Established equipment / source correspondence |
| --- | --- |
| R-101 | WISTR reactor assembly, imported through `models/wistr_installation.py` REACTOR configuration |
| SG-101, SG-102, SG-103 | Three steam generators; one per coolant leg, 500 MWth target each |
| P-101, P-102, P-103 | Three main cold-leg circulation pumps; configuration in `models/wistr_installation.py` |
| TK-401 | `equipment.coolant_storage`, built in `src/textual_graphics/installation_utilities.py` |
| P-401 | `equipment.coolant_transfer_pump`, same source module |
| L-401 / L-402 | `connections.coolant_transfer`, routes `reactor_to_pump` / `pump_to_storage` |
| L-403 | Preparation interface plus `site.salt_distribution.duct_to_coolant_storage` |

## Numerical basis

| Item | Carried into this drawing | Status / reference |
| --- | --- | --- |
| Three-leg duty | 1500 MWth total; 500 MWth per generator | Existing design target |
| Salt temperature | 875 / 810 K, rounded to 602 / 537 C | Existing generator and pipe-wall worksheets |
| Circulation | 4.619533 m3/s per leg | Existing pump worksheet |
| Pump rise | 286.3092 kPa | 1.5 times preliminary generator loss; not system design pressure |
| Main pump | 1.653 MW shaft, provisional 2 MW motor | Existing pump worksheet; no supplier selection |
| Main pipe | 1425 mm bore / 25 mm nominal wall / 1475 mm bare OD | Conditional pipe-wall screening case |
| Main insulation | 400 mm radial hot / 350 mm radial return | Existing insulation estimate and installation interface |
| Transfer/supply tube | 50 mm OD, heated, 50 mm radial insulation | Visual allowances; transfer line has provisional 3 mm wall; preparation line wall unselected |
| Storage insulation | 350 mm | Current visual allowance; no revised tank heat balance |

The 1.0 MPa(g) case in the wall worksheet is a screening input, not an established design pressure. The 24 MPa(a) secondary operating basis makes SG tube-failure pressurization an unresolved interface. The pump estimate retains the generator calculation's 19.879 m tube length; the 17 m visual casing does not establish that internal design or validate pressure drop. The installation main pipe bore also needs harmonizing with the isolated reactor's older 1.4 m nozzle envelope.

## Review questions for the next revision

1. **Fill and drain states:** how does salt return from storage to the reactor; what empties each generator and low point; what salt remains trapped? The existing transfer pump is not assumed reversible.
2. **Pressure and expansion:** establish operating/transient pressure profiles, coolant expansion accommodation, storage gas/vent arrangements, relief destinations, and response to secondary tube failure. Include thermal expansion of salt trapped by any proposed isolation.
3. **Isolation strategy:** decide whether the proposed hot/cold branch valves are practical and sufficient, whether pumps need separate maintenance isolation, and what remote actuation and position indication are needed. No valve technology or credited safety function is selected.
4. **Measurement feasibility:** choose high-temperature salt-compatible methods and maintainable locations for flow, pressure, temperature and storage level. Point symbols do not imply wetted probes or conventional impulse lines. Determine additional reactor level/pressure and heat-trace temperature coverage after the pressure/operating concept is established.
5. **Thermal and hydraulic states:** define preheat, transfer rate, heat-trace coverage and power, freezing/recovery, available suction head, reverse flow through idle legs, and shared-plenum flow distribution.
6. **Equipment interfaces:** reconcile SG internals with MSU, nozzle bores with the reactor model, and coolant inventory with usable storage capacity and freeboard.

For the next discussion, walk through normal circulation, filling, draining, loss of one pump, and a steam-generator leak on these sheets. Record desired behavior before assigning automatic actions or setpoints.

## Sources

- [Coolant pump estimate](../../../calculations/steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md).
- [Coolant pipe-wall estimate](../../../calculations/steam-generator/Molten-salt%20coolant%20pipe%20wall%20-%20Hurmet.md).
- [Coolant insulation estimate](../../../calculations/steam-generator/Molten-salt%20coolant%20insulation%20-%20Hurmet.md).
- [Current interface history](../../interfaces.md), including D-014 main piping, D-041 transfer/storage and D-046 preparation supply.
- [Model configuration](../../../../fastSaltModels/models/wistr_installation.py), [utility piping](../../../../fastSaltModels/src/textual_graphics/installation_utilities.py), and [preparation supply](../../../../fastSaltModels/src/textual_graphics/site_salt_distribution.py).

Verification: both PDF pages rendered and visually inspected; flow traced from reactor through each SG and pump back to reactor, and independently from reactor/preparation to the two storage ports. Registers checked against drawing tags. These checks establish document consistency, not component performance or system qualification.
