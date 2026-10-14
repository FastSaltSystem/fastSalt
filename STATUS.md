# Project status and next work

## Attached control annex — draft, 14 October 2026

D-069 adds a 20 × 25 m, 5.5 m-high control annex at the turbine hall's southeast corner, with 4 m of shared reactor-facing boundary. It reserves 180 m² for operators, separate control-equipment/UPS/ventilation rooms, an outside entrance and second exit, and a two-door vestibule to the turbine hall. The separate slab and 0.60 m control-side barrier are visual allowances; the single/double-wall and structural details are unresolved.

The draft clears modeled piping and turbine maintenance reservations. The nearest reactor-shell gap is approximately 1.63 m, not a vehicle-access route. [Complete model, exterior/interior/site views and checks](../fastSaltModels/docs/control-annex.md). Existing coolant/nitrogen tag associations and main circulation are retained. This is a spatial study; habitability, protection, ventilation, cable routes, foundations and egress remain to design. Accepted for versioning on 14 October 2026. Model sources: fastSaltModels `8bcc2e8`.

## Exterior nitrogen supply to three service areas — draft, 14 October 2026

D-068 retains the existing outdoor nitrogen skid and adds a common exterior wall header, with separate branches to off-gas treatment, fuel refining/recycling and coolant preparation. Branch isolation and control/protection functions are reserved outside each room. The revised N-600 feed rises at the skid, crosses to the off-gas west wall, then follows the wall around to the front; its freestanding service-area run is removed. Clean nitrogen enters a separate makeup port at the coolant pressure-control station; G-400/H-401 process-gas returns remain separate.

The coolant P&ID now includes sheet 6 for this shared utility and a cross-reference on sheet 3. The 3D coverage expands to 90 tagged items. [Draft model, views and checks](../fastSaltModels/docs/coolant-pid-3d.md). Pipe dimensions are visual reservations; demand, pressure, regulation/backflow hardware, supports and penetration seals remain unresolved. Main hydraulics and existing operating-state definitions are unchanged. Accepted for versioning on 14 October 2026.

## Coolant P&ID in 3D and lowered transfer piping — draft, 14 October 2026

D-067 adds the missing coolant-only gas vessels, header, SG/tank gas branches and valve reservations to the current layout. All 79 tagged P&ID items are accounted for, including proposed valve/instrument locations and explicitly unresolved relief interfaces. The three relief destinations remain local marked stubs, not selected discharge facilities. [Current scene, detailed views and coverage audit](../fastSaltModels/docs/coolant-pid-3d.md).

The unused fresh-air arc between the door and SG-102 inlet is removed and capped; all ten equipment branches and three inlets are retained. The raised L-401 crossing is lowered to the 0.40 m under-vessel/pump level. J-401 sits 0.20 m above the floor, with L-402/L-403 falling toward it. L-401 remains level, so complete gravity drainage is not established. Engineering dimensions/pressure-control hardware remain unresolved where previously unresolved. Main circulation geometry, adopted hydraulics and operating states are unchanged. Accepted as a visual draft for versioning on 14 October 2026.

## Compact shared-wall tank enclosure — draft, 14 October 2026

D-066 moves TK-401 2.83 m toward the reactor and uses the reactor wall as the enclosure's inner boundary. The owner confirms a radial straight wall parallel to a tank tangent; a curved outer wall completes the enclosure. Coolant preparation shares approximately 9.53 m of the fuel-recycling room's east wall. Its equipment and receiving opening shift with the room. P-401 and insulated low-level transfer routes move to fit; the existing raised internal-header crossing remains.

Fresh-air intake 2 moves to 125°, near the main hot-air stack and nitrogen skid. [Current scene, views and geometric checks](../fastSaltModels/docs/compact-services-draft.md). Main coolant circulation and calculations, off-gas/fuel process placeholders and the three-item laydown are retained. Structural, heat-loss, access and intake/exhaust recirculation assessments remain open. This supersedes D-065's freestanding cylindrical silo for current layout review. The owner accepted the layout for versioning on 14 October 2026; model sources are committed in fastSaltModels `bb1b5f4`.

## Shared-wall service annex and coolant silo — draft, 14 October 2026

D-065 combines off-gas and fuel refining/recycling in a divided 5 m building against the reactor's existing curved wall. The nearby air inlet moves to 33°, clear of the doorway approach. A cylindrical 12.5 m OD enclosure replaces the square tank bay; coolant preparation occupies a separate 5 m building on its +Y side. Existing process placeholders are relocated and their interfaces rerouted. The three-item laydown and main circulation paths remain unchanged.

[Current Blender draft, views and scope](../fastSaltModels/docs/attached-services-draft.md). The shape reduces wall perimeter, but heat-loss performance is not calculated. Room segregation/ventilation, structural/support design and complete operational access remain to develop. This supersedes the square-bay layout below for current visual review; D-066 is the latest layout.


## Attached coolant tank bay and expanded laydown — draft, 14 October 2026

D-064 records the owner-selected attached bay beside coolant preparation. The [layout draft](../fastSaltModels/docs/tank-bay-draft.md) moves the selected 8.2 × 16 m tank and reversible transfer pump out of the reactor building, shortens the preparation route, and uses the agreed shared bottom tee. A local raised crossing clears the existing internal headers; high-point gas handling and drainability remain to review. The bay is provisionally 11 × 11 × 19.5 m. The earlier saved interior tank arrangement remains a source snapshot.

The expanded catwalk-level laydown has room for the insulation cover, cap and top reflector together. The cap and reflector share a larger tray, with the reflector reversed in plan. Current checks address geometric fit only; access, supports and loaded handling remain provisional. Main-loop hydraulic calculations are unchanged. Draft outputs and source are linked in the guide; D-066 is the latest layout.


## Newer SG workbook adopted — D-063, 14 October 2026

D-063 adopts the newer `counterSG.xlsx` geometry: **4,902 salt tubes per SG, 20 mm ID / 24 mm OD and 11.920866 m calculated active length**, provisionally used as straight hydraulic length. The 6,536 steam tubes are a separate bank. The 17 m casing, 18,500 kg/s total flow, 810–890 K temperatures and 3.4 m active core remain unchanged. Salt inlet/outlet labels were corrected to 890/810 K; numeric cells and formulas are unchanged.

At the retained flow, mean SG tube velocity is 2.451 m/s. SG tube friction is **70.491 kPa**, or **87.004 kPa including tube ends and collector allowances**. Full-loop pump rise is **172.162 kPa** (10.599 m cold-salt head). Per pump: **801.2 kW shaft / 834.6 kW electrical**; three-pump total **2.504 MW electrical**. Fitting sensitivity is 2.241–3.065 MW, not a certified range. The prior D-061 total was 3.355 MW.

With 1 bar(g) at SG tops, suction is **2.246 bar(g)**, discharge **3.823 bar(g)**, and reactor bottom-plenum midpoint **4.254 bar(g)**. Lower SG resistance raises suction and reduces required pump rise by matching amounts; downstream pressures stay unchanged in this fixed-flow, mean-density screen.

The revised inventory is approximately **452.3 m³**, including **55.1 m³ in all three SG tube banks**. At 890 K, the fixed cold-fill charge requires 478.7 m³, or 526.5 m³ including 10% inventory allowance. The already-selected 8.2 × 16 m storage reservation provides 622.1 m³ working acceptance under existing allowances, leaving 95.6 m³. Tank placement remains pending; the smaller saved Blender tank remains a historical layout envelope.

The shared TOML, P&ID and resolved graphics duty metadata use the checked revision. Existing 2 MW motor reservations and physical equipment/pipe envelopes are retained. Actual SG contact conductance, hydraulic extensions, local coefficients, roughness and pump curves/NPSH remain provisional. No protection setpoints, relief capacity or SG-failure assessment are established. Older Generator sizing and Brayton worksheets remain explicitly historical cases.


Updated 14 October 2026. This is the working handover for the **Fast Salt System** project. Update it when a workstream changes status; keep technical values in the [design basis](design/design-basis.md) and cross-component decisions in the [decision record](decisions/index.md).

## High-level SG relief connections — 14 October 2026

14 October 2026. The owner selects one dedicated high-level coolant-side emergency relief connection on each SG, separate from the normal gas-collection/pressure-control piping. Add shared ports `SG-101/102/103.relief_high`, lines L-101R/102R/103R, and rupture-disc concepts RD-101/102/103. No intervening isolation valves are included. Discs are normally intact and remain open after actuation; they are not operable valves in the normal state table.

The requirement is to preserve reactor coolant inventory and prevent continued gravity drainage or siphoning after relief. A high takeoff alone does not prove retention during pressure-driven two-phase discharge. B-501 is an unresolved receiving-system interface with three separate terminations; it does not select a common header, number of receivers, pit, or vent route. No cold-leg downward dump is adopted.

Exact elevations, burst differential pressure at actual disc temperature, flow area/capacity, expelled salt volume, receiving/venting arrangement, backpressure, freeze protection, burst detection/response and subsequent cooling remain unresolved. Detailed SG-failure/transient assessment remains deferred. P&ID sheet 5 records the concept; sheet 1 cross-references it. Physical 3D nozzles/routing remain pending; no Blender rebuild or pressure-calculation change.

## Shared coolant basis adopted — 14 October 2026

**Historical D-061 values below; D-063 supersedes the SG geometry, pump duty and suction pressure.**

D-061 adopts the UM hydraulic case into the shared engineering model, P&ID equipment register and graphics duty metadata: **18,500 kg/s total**, three equal 6,166.67 kg/s legs, **810–890 K**, and **3.4 m active core height**. At 810 K, pump-inlet density is 1,656.3245 kg/m³ and volume flow is **3.7231 m³/s per pump**. Full itemized loop loss is **230.681 kPa** (14.202 m cold-salt head), with **1.074 MW shaft / 1.118 MW electrical per pump**, **3.355 MW electrical total**. No SG-loss multiplier remains in the active adapter.

Normal station pressures retain the checked mean-density screen: SG tops 1 bar(g), pump suction/discharge 1.660/3.823 bar(g), reactor bottom-plenum midpoint 4.254 bar(g). Pump differential head is distinct from the static-pressure difference between ports at different heights. These values are not design pressures or relief settings.

The **2 MW motor reservations**, casing dimensions, pipe dimensions/insulation and building layout remain unchanged. Existing saved Blender scenes remain snapshots; the resolved coolant document is updated without a full Blender rebuild. SG tube geometry is retained and its 500 MW per-generator duty remains a target; SG thermal rerating, fitting losses, roughness, supplier pump curves/efficiency and NPSH remain provisional. Insulation/wall worksheets retain their earlier screening cases and need review against 890 K; adoption does not requalify them. Tank relocation and SG-failure/relief assessment remain deferred.

## Updated normal coolant pressure profile — 14 October 2026

The [active Hurmet pressure worksheet](calculations/reactor/Normal%20coolant%20pressure%20profile%20-%20Hurmet.md) now uses the UM flow and allocated itemized losses: at 1 bar(g) SG-top reference, base suction/discharge are 1.66/3.82 bar(g), reactor cold inlet 3.78, bottom-plenum midpoint 4.25 and hot outlet 2.77. Base pump head remains equivalent to 230.7 kPa; the 0.90 m rise between pump ports explains its smaller static-pressure difference. Fifty-three Hurmet outputs, all three case loop closures and datum/hydrostatic sensitivities pass. Mean-density screening only; no relief/SG-failure work. [Checks and preserved earlier revision](calculations/reactor/coolant-pressure-check.md). Shared P&ID/graphics duty is now adopted under D-061 above.

## Itemized coolant pump power — 14 October 2026

The [new Hurmet pump estimate](calculations/steam-generator/Itemized%20coolant%20pump%20estimate%20-%20Hurmet.md) combines the UM flow/temperature case, recalculated SG friction, checked core loss and modeled piping with explicit provisional fitting terms. Working duty is 230.7 kPa / 14.2 m cold-salt head, 1.074 MW shaft and 1.118 MW electrical per pump: **3.355 MW electrical for three pumps**. Fitting-only sensitivity is 3.10–3.91 MW; not a certified operating envelope. Sixty-two Hurmet comparisons and sensitivities pass. D-061 now adopts the shared graphics/P&ID duty while retaining 2 MW motor reservations; no failure/relief work. [Checks and itemization](calculations/steam-generator/coolant-pump-itemized-check.md).

## Core coolant pressure loss — 14 October 2026

D-060 records owner selection of UM's 18,500 kg/s core flow and correction of the report's 3.8 m height typo to 3.4 m. The [Hurmet core worksheet](calculations/reactor/Core%20coolant%20pressure%20loss%20-%20Hurmet.md) estimates 44.5 kPa active-core friction, or 62.7 kPa including same-bore reflector passages and provisional entrance/exit losses. Exact 24,576 × 14 mm bores give 2.993 m/s mean velocity and 3.035 m/s at the hot outlet; the report's 3.86 m² area differs by 2%. Thirty-five Hurmet comparisons and sensitivities pass. The itemized pump and active pressure profile reconcile this case; D-061 adopts it across the shared views. [Checks and scope](calculations/reactor/core-coolant-loss-check.md). No geometry, relief or SG-failure work.

## Earlier normal pressure screen — superseded 14 October 2026

The original higher-flow, unallocated-loss envelope is [preserved here](calculations/reactor/revisions/pressure-before-itemized-2026-10-14/README.md). It is superseded by the itemized pressure revision above; its broad suction and reactor-pressure ranges should no longer be used as the current normal case. SG failure assessment and tank relocation remain deferred.

## Coolant pressure and level basis — 14 October 2026

D-059 records approximately 1 bar(g) at the SG tops, TK-401 normally nearly empty, and P-401 inventory transfers setting accumulator levels independently of gas-pressure control. Steam-side leaks are intended to enter the SG air side, not coolant. Relief return to TK-401 is a proposal requiring an available path and tank gas/backpressure review; no relief hardware or setpoints are adopted. P&ID notes and source metadata updated; building rearrangement remains deferred.

## Coolant storage size selected; placement pending — 14 October 2026

D-058 adopts an 8.2 m diameter × 16 m high bare tank as a provisional planning envelope (8.902 m insulated diameter; approximately 622 m³ working capacity with current allowances). The saved 42 m building has sufficient gross height/diameter, but the existing bay conflicts with the laydown platform, internal fresh-air duct/branch and hot coolant pipe. The [fit study](../fastSaltModels/docs/coolant-storage-fit.md) records the conflicts. The saved 3D tank remains 4 × 8 m pending coordinated relocation/rerouting; no building enlargement is selected.

## Coolant inventory and storage capacity — 14 October 2026

The [new Hurmet inventory worksheet](calculations/reactor/Coolant%20inventory%20and%20storage%20capacity%20-%20Hurmet.md) estimates 508.5 m³ in the current reactor/SG/piping circuit, versus 72.6 m³ provisional working acceptance in the modeled 4 × 8 m TK-401. A 450°C cold-fill case yields 19.6–25.5 m³ expansion: expansion-only storage appears feasible with an initially low tank level, but full drainage does not fit. Hot full-drain inventory is about 535 m³; a 10% inventory allowance plus 20% freeboard/5% heel gives approximately 785 m³ internal geometric storage. The equivalent 11.3 m diameter × 8 m external-height cylinder is a space comparison, not a selected replacement. Gross reactor spaces, SG tube length, collector/pump cavities and storage internals remain provisional. Sixty-four Hurmet comparisons and temperature/diameter sensitivities pass. No Blender or P&ID changes. Next: choose the storage arrangement and reconcile the detailed inventory before transfer controls. [Calculation notes](calculations/reactor/coolant-inventory-check.md).

## Consolidated coolant-gas draft — 14 October 2026

D-057 supersedes the D-056 gas draft with three SG-top gas vessels, pressure/level indication and one common pressure-control station at coolant preparation. G-401 is removed; G-400 / H-401 / G-402 supply and receive TK-401 gas. The four-sheet P&ID separates the gas diagram from agreed operating states, including intermittent expansion/contraction transfers through reversible P-401. P-401 is now explicitly stopped during tank-to-preparation transfer and gas sweep; V-401 is closed in those states. Numeric vessel sizes, pressure band, transfer triggers, storage capacity and protection remain unresolved. Draft consolidation only: no Blender rebuild or commit. See [working states](design/pids/coolant-system/operating-states.md).

## Coolant-system P&ID draft — 13 October 2026

A [two-sheet preliminary coolant P&ID](design/pids/coolant-system/README.md) now records the three circulation legs, bottom-suction main pumps, reactor-to-storage transfer and preparation-to-storage supply. Amber symbols distinguish 20 proposed measurements and nine candidate isolation valves from established process connections. Editable SVGs, a printable PDF, registers and source hashes are retained. Detailed refill/drain states, pressure/expansion/vent arrangements, SG tube-failure response and instrumentation technologies remain open. This is a discussion document; no automatic protection logic or new graphics design is adopted.

The coolant drawing now uses separate engineering and layout TOML sources, a Python renderer and Markdown review notes. The owner selected explicit TOML tables for clearer hierarchy and easier cut/paste. Earlier YAML sources are archived; eleven validation/regression checks pass; model edits drive the drawings and registers. Routine builds go to ignored `outputs/current/`; the original Revision A deliverables and renderer are preserved. See the [editing and revision workflow](design/pids/coolant-system/README.md#working-source-and-draft-history). No engineering arrangement changed in this refactor.

D-054 records the owner's clarification: P-401 is a reversible positive-displacement pump. The B-working P&ID shows L-401/L-402 in both directions, resolving the intended reactor refill connection through the same piping. Complete low-point/SG drainage and valve/vent states remain to define. Original Revision A is preserved.

D-055 adds preparation-to-TK-401 pressure gas, a common low-point tee and one bottom tank branch. The owner confirms tank emptying followed by a gas sweep back to preparation through L-403; reactor/SG drainage remains separate. The [working flow-state table](design/pids/coolant-system/operating-states.md) records the sequence. Gas sizing/controls and 3D routing are pending.

## Python assembly authoring and TOML exchange — 13 October 2026

[D-052](decisions/index.md#d-052--python-authored-assemblies-with-resolved-toml-exchange) implements the PMS-style authoring structure for the three main coolant legs: Python assembly rules → detached resolved document → Blender, with optional TOML export/import. Eight plain-Python checks, Blender direct/TOML geometry checks and a full installation build from TOML pass. P&ID tags, flow paths and dimensions agree for the migrated subset. Existing geometry and baselines are retained; the remaining systems still use their existing builders. See [the working guide](../fastSaltModels/docs/assembly-models.md).

## Shared coolant engineering source — 13 October 2026

[D-053](decisions/index.md#d-053--shared-coolant-engineering-source-for-multiple-views) moves the main coolant identities, ports, topology, pipe dimensions and operating-case inputs into [one shared model](design/engineering/README.md). Both P&ID and graphics consume it, with view layouts retained separately. Worksheet hashes require explicit review when calculation sources change. Six cross-view checks pass, including one edited source updating both views. The P&ID remains byte-identical and resolved graphics geometry is unchanged. Blender direct/TOML checks and the full installation build (4,332 meshes) pass. Hurmet equations remain authoritative in the worksheets; automatic Hurmet exchange and simulation adapters are still future work.

## Current materials

Accepted turbine equipment checkpoint: fastSaltModels `094d4a3`, preserved with the complete Blender site, three inspection views, checked reports and hash manifest in [the turbine equipment baseline](../fastSaltModels/baselines/turbine-equipment-2026-10-12/). It adds D-051 machinery detail to the retained layout.

Earlier site checkpoint: fastSaltModels `a6bbc77`, preserved with its Blender scene, key views, checked reports and hash manifest in [the 12 October site baseline](../fastSaltModels/baselines/fast-salt-site-2026-10-12/). It includes D-043–D-050 and the final 1.35 m generator-inlet elevation. Routine outputs remain ignored.

| Area | Current state | Start here |
| --- | --- | --- |
| Project organization | Two local Git repositories: `fastSalt` for the project hub, `fastSaltModels` for graphics; no public remote configured | [Repository map](README.md#repository-organization) |
| Detailed reactor graphics | Checkpoint `a99002f` preserves six fitted insulation cassettes and side supply/return plenums; pressure caps retained; earlier 0d981f2 baseline preserved | [Reactor integration](../fastSaltModels/docs/reactor-study.md#insulation-covers-and-side-air-connections--11-october-2026) |
| Installation graphics | Accepted maintenance/utility checkpoint `06a13ef`, saved in [the named baseline](../fastSaltModels/baselines/wistr-maintenance-2026-10-12/); earlier service checkpoint `8ec6833` includes provisional 100 mm hot-air insulation and 1 mm cladding; 42 m insulated-pipe layout: separate metal and insulation meshes use conditional Hurmet sizes; generators/storage spread outward; raised cold-salt suction and feedwater routing; reactor side ducts connected to exterior rings, with fresh air routed directly along the floor; D-034 replaces paired absorber stands with a shared expanded-metal catwalk, six distributed modules and 24 dedicated service tubes; D-036 doubles module tank volumes; D-037 adds 12 separate heated reservoirs and doubles the modules to 12; D-038 lowers the catwalk 1.10 m from that draft, replaces service boxes with insulated bundles below liftable channelled covers, preserves falling salt drains and adds local insulation strips; D-035 adds 36 separate sector-to-maintenance-tank lines through core-service inserts and beneath the catwalk; D-039 adds a three-flight catwalk stair; D-040 replaces the exterior hot-air ring with a large internal insulated header and aligns the stack for a separate direct reactor exhaust; D-041 centres/doubles generator exhausts, adds the heated coolant transfer line/pump, insulates coolant storage and adds a provisional outdoor nitrogen supply; D-042 replaces fixed sector storage with a mobile canister/cart and adds cover/cap laydown at catwalk level; doorway and 5 m hoist clearance retained; selective interference checks | [Installation guide](../fastSaltModels/docs/installation.md#insulated-process-piping--11-october-2026) |
| Site layout | Motor-BFP working draft: D-031 rotates BFPs side by side, reducing the turbine hall to 60 × 40 × 28 m (240 m² less main-hall floor area), 20 × 10 × 7 m BFP electrical annex, external withdrawal aprons and 30 equipment boxes (HP/IP now shown separately); D-030 groups reheaters at steam entry, shifts LP/condenser train left, puts BFPs between heater banks and aligns generators alongside each other; condensate pumps now along the west wall before the shifted LP heater bank; selected box/service checks pass. D-043 now uses 15 × 12 × 5 m fuel/coolant preparation at (11.5, 32) m and an adjacent 10 × 11 × 5 m off-gas building at (−1, 31.5) m; both footprints are quartered and share one elevated service duct, with a separate release stack and provisional process equipment/connections. The site now imports the current reactor maintenance/utility arrangement. D-032 aligns building centres and perpendicular turbine-wall entry; D-033 replaces the offset with two 45° bends per pipe plus a separate 20° reactor outlet alignment turn. 59 main pipe sections now routed with explicit HP → reheaters → IP → LP connections; east feedwater bay has 4.70 m clearance versus 5 m reservation; long crossovers and crane/rotor access need review. Extraction/drain circuits, structure and auxiliaries remain open | [Site guide](../fastSaltModels/docs/site-study.md) |
| Fuel handling and recycling layout | Presentation reviewed: separate SNF-conversion and liquid-salt refining/recycling buildings. D-044 horseshoe retained as an observation/access concept only; 28 m / 8 m dimensions and seven bays withdrawn as sizing basis. Current converter/refiner reports reviewed and indexed as W15/W16; no dimensioned facility schedule found. D-045 adopts rectangular layout placeholders (converter 20 × 15 × 8 m; refiner 15 × 12 × 5 m) and adds separate fuel supply/return in the shared duct | [Floor-plan study](../fastSaltModels/docs/fuel-handling-study.md) |
| Steam-generator estimate | Calca converted to Hurmet; pump allowance worksheet supports three provisional 2 MW motors; steam/feedwater bore and wall worksheet added with explicit provisional pressure/stress inputs; insulation worksheets add conditional 350 mm steam / 175 mm feedwater and 400 mm hot-salt / 350 mm return-salt radial allowances | [Calculation conventions and worksheet](calculations/README.md) |
| Rankine-cycle plant | Motor-BFP equipment basis D-029: 697.1 MW gross / 671.6 MW after BFP + condensate loads at 5 kPa, other loads excluded; 282 MW reheater, 550/350 MVA generator allowances, revised pipe bores and three 15 MW BFP motor trains. Original steam-drive calculation retained; preliminary equipment and dimensional checks complete | [Current equipment](calculations/power-cycle/Motor-BFP%20equipment%20sizing%20-%20Hurmet.md) |
| Maintenance fuel tank volume | Preliminary geometric check: 11.81 m³ per tank after 50% cooling-pipe occupancy, versus 6.43 m³ gross core-sector envelope (1.84×). No enlargement indicated at this stage; clear internal dimensions, freeboard and connected-pipe inventory remain open | [Hurmet worksheet](calculations/reactor/Maintenance%20fuel%20tank%20capacity%20-%20Hurmet.md) |
| Reactor top insulation | No-hood-flow thermal estimate: conditional 500 mm calcium silicate, about 5 kW through the top; room-condition sensitivity and 6.4 t insulation mass documented; six fitted covers now replace the hood in the graphics; local service wells and thermal bridges need an updated heat balance | [Hurmet worksheet](calculations/reactor/Reactor%20top%20insulation%20-%20Hurmet.md) |
| Removable insulation cover | Five grids, bottom grooves and flat upper bearing retained; six fitted covers with hook pockets and removable service inserts are in the reactor. Earlier source cassette ~2.16 t; earlier fitted estimate 2.10 t excludes separate thermal inserts. D-038 installation copies add open-bottom channels, local insulation strips and extended pickups; revised mass/strength/thermal checks pending | [Cover and integration](../fastSaltModels/docs/tgrid-insulation-cover.md) |
| Research evidence | Sixteen indexed work groups, including historical designs and manuscripts; later UM accident work reported but not yet documented here | [Publication library](publications/index.md), [study register](research/studies.md) |
| MSU collaboration | Initial component brief prepared; current student work, repository, contacts, and agreed inputs still to collect | [Student project brief](collaboration/steam-generator-project.md) |
| Workshop presentation | October 27–29, 2026; working title “Fast Salt System - Progress”; ten-slide outline drafted for 14 minutes plus margin and 5 minutes for questions; working visuals refreshed; annotated Rankine-cycle diagrams delivered as editable PowerPoint and PNG, now including the motor-driven BFP alternative with revised heater paths; research figure and final slide composition pending | [Presentation preparation](presentations/README.md) |

D-046 adds low insulated salt-storage distribution in the composed site: a fuel valve-box reservation with six supply/return pairs to the maintenance tanks, plus coolant supply to the storage-tank bottom. Long fuel/coolant runs are centred 0.20/0.40 m above floor. [Floor-routing view and limits](../fastSaltModels/docs/site-study.md#low-insulated-salt-distribution--d-046).

D-047 adds three fuel pressure servers, twelve 25 mm tank gas tubes and paired supply/off-gas headers through the shared duct. The nitrogen skid now feeds the off-gas building from beside its west wall. [Current arrangement](../fastSaltModels/docs/site-study.md#fuel-pressure-servers-and-nitrogen-relocation--d-047).

D-050 completes the reactor-building columns and adds three outdoor fresh-air inlets plus horizontally centered generator-side valve boxes, subsequently lowered to 1.35 m above floor with short level duct connections. Inlet bores give 75% of exhaust clear area; selected route/equipment checks cover the enlarged connections. [Current air layout](../fastSaltModels/docs/site-study.md#generator-air-inlets-and-complete-column-layout--d-050).

The accepted turbine-hall visual checkpoint adds [recognizable machinery exteriors and inspection views](../fastSaltModels/docs/turbine-equipment.md) (D-051), retaining the equipment reservations and all main pipe terminals. Upper-level structures and supplier geometry remain to develop.


## Next work, in order

A provisional three-flight stair in the 210° equipment bay and approximately 8.2 m dogleg bridge to the catwalk are now modeled (D-039), with selected solid and walking/headroom clearance checks. D-040 adds the internal hot-air header and straight reactor-to-stack exhaust. D-042 adds cover/cap laydown and mobile sector removal. Next review: platform and receiving-frame loads, canister/cart design (only 0.17 m door-height reserve), crane transfer paths, exhaust sizing and complete access/egress. Absorber tubes retain their accessible spider penetrations.

1. Review the [timed workshop outline](presentations/workshop-outline.md) for “Fast Salt System - Progress” at the October 27–29, 2026 workshop, and select the supporting UM research figure.
2. Review the [provisional site layout](../fastSaltModels/docs/site-study.md), then refine the [motor-BFP equipment arrangement](../fastSaltModels/docs/site-study.md) with supplier outlines, piping corridors, columns, stairs, crane/rotor handling and installation access. Develop the off-gas and fuel/coolant preparation briefs, process duties and reactor-side collection/supply interfaces.
3. Select readable views and any short handling animation, then build and rehearse the 15-minute deck. Preserve the exact model revisions and graphics used.

The [coolant pipe-wall worksheet](calculations/steam-generator/Molten-salt%20coolant%20pipe%20wall%20-%20Hurmet.md)
now records the conditional 25 mm nominal wall case (1.425 m bore, 1.475 m bare OD).
Pressure, alloy, effective allowable stress and structural checks remain provisional.

## Inputs still to collect

These items can be resolved alongside presentation work; they do not prevent drafting its structure.

- UM: latest accident-scenario reports, specific results approved for citation, and associated design revisions. See [RS-006](research/studies.md).
- MSU: point of contact, existing deliverables/repository, and an agreed steam-generator input basis. See [IF-001](design/interfaces.md#if-001-reactor-and-steam-generator).
- Publications: preferred manuscript versions and outstanding citation questions in the [curation notes](publications/curation-notes.md).
- Shared engineering basis: the installation now uses a conditional 1.425 m bore / 25 mm salt wall with 400/350 mm insulation; confirm design pressure, salt-compatible alloy, allowable stress and generator internals before pipe selection.
- Public release: choose hosting and licenses, confirm reuse terms, and replace local-only document links. The local cleanup does not publish the project.

## Continuing in focused chats

Use this chat for project coordination. Start focused chats as needed for reactor modeling, installation layout, steam-generator calculations, and the workshop deck. A chat may touch both repositories. Each handover should identify the objective, relevant files and revisions, decisions made, checks performed, and next action. Save durable information in the repositories rather than relying on a chat transcript.

### Paired fuel insulation — D-048

Fuel in/out now share a continuous heated and insulated jacket from refining to the distributor and on each of its six tank branches. The draft uses two 50 mm OD tubes at 80 mm spacing, 50 mm minimum insulation and 1 mm cladding (236 mm overall). Long fuel runs are centred 0.18 m above floor; coolant remains at 0.40 m. These are visual allowances; heater duty and thermal/pressure/support qualification remain open. See [the current routing and cutaway](../fastSaltModels/docs/site-study.md#common-heated-fuel-bundles--d-048). This supersedes the separate fuel envelopes and 0.20 m fuel elevation recorded in D-046.

### Internal cold-air distribution — D-049

The current site moves fresh-air distribution into a floor-level steel duct inside the reactor wall. Ten equipment branches connect internally; the outdoor intake and a sealed 5.5 m doorway gap remain. Nominal clear area is retained at 6.25 m², with local offsets around columns. Airflow, effective area through offsets, pressure loss and structural/support design remain provisional. See [the current layout](../fastSaltModels/docs/site-study.md#internal-fresh-air-duct--d-049).
