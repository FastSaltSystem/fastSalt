# Coolant P&ID revision history

| Revision | Date | Change | Preservation |
| --- | --- | --- | --- |
| A | 2026-10-13 | First two-sheet coolant circulation and storage/transfer draft; proposed instruments and isolation | Original root PDF/SVG/CSV files; original renderer and hashes in `revisions/rev-A/` |
| A-working | 2026-10-13 | Separated engineering YAML and layout YAML from the renderer; added validation, equipment register and reproducible working builds; engineering arrangement unchanged | Source files tracked through Git; ordinary generated output ignored |
| A-working / TOML | 2026-10-13 | Owner prefers explicit table headings and easier cut/paste. Adopted TOML for model and layout; explicit unresolved-field convention; eleven checks pass | YAML source archived; rendered PDF, SVGs and registers unchanged |

A named revision is a review milestone, not a construction release. Future entries should state the design changes and unresolved decisions that matter to reviewers.


## A-working / shared main-coolant source — 13 October 2026

D-053 moves main-circulation equipment, topology and numerical inputs into `design/engineering/coolant-system.toml`. The view imports shared identities and rejects local engineering overrides. Storage/transfer and proposals remain local; layout is unchanged. Source and adapter hashes are recorded. PDF, SVGs and registers compare byte-identically with the preceding TOML draft. Preserved Revision A remains untouched.


## B-working / reversible transfer pump — 13 October 2026

Owner confirms P-401 is a reversible positive-displacement pump (D-054). L-401/L-402 now explicitly permit flow in both directions; pump ports are named reactor_side/storage_side so their identity does not reverse. The working drawing and registers reflect drain/refill; original Revision A is unchanged. Pump duty, full-loop drainage and operating valve/vent states remain open.


## B-working / tank pressure and common low-point tee — 13 October 2026

D-055 adds G-401 from coolant preparation to TK-401 gas space. J-401 joins L-402, reversible L-403 and the single tank-bottom branch L-404. The owner confirms that pressure empties the tank to preparation, followed by gas sweeping L-404/J-401/L-403; reactor/SG drainage through P-401 remains separate. New line sizes and controls are unresolved. Original Revision A stays intact; 3D routing is pending.


## B-working / consolidated coolant gas and states — 14 October 2026

D-056 adds a third sheet for the separate coolant-gas system and agreed transfer states. SG top branches and a valved tank gas-return branch join a bidirectional common header to coolant preparation. G-401 remains separate. Shared SG port declarations gain gas_top; gas routes remain P&ID-only. Unassigned gas-valve states and sizing are explicit. Batch review only; no Blender rebuild or new commit.

## B-working / SG gas vessels and expansion states — 14 October 2026

D-057 removes G-401, adds AC-101–103 upstream of gas isolation with pressure/level indications, and shows common controlled gas makeup/return at preparation. Most expansion is assigned to storage through intermittent reversible P-401 transfers. Gas-valve positions and expansion/contraction states are recorded in TOML. State table moved to sheet 4 to keep the gas schematic readable. Vessel volumes, pressure band, transfer triggers and protection remain unresolved. No Blender rebuild or commit.

### D-057 clarification — P-401 stopped during tank transfer and sweep

14 October 2026. Set P-401 to stopped for tank-to-preparation transfer and gas sweep. The owner notes that tank transfer may occur during reactor operation. V-401 remains unassigned; no other valve states or concurrent-operation controls are changed. The TOML state table, Markdown record and sheet 4 agree.

### D-057 clarification — V-401 closed during tank transfer and sweep

14 October 2026. Set V-401 closed for tank-to-preparation transfer and gas sweep. P-401 remains stopped. The two rows now have all listed valve and pump states assigned; transfer controls and sequencing remain unresolved. Updated TOML, state record and sheet 4.


## B-working / normal pressure and level basis — 14 October 2026

D-059 records the owner-confirmed approximately 1 bar(g) SG-top operating target, normally nearly empty TK-401 and P-401 inventory adjustment for accumulator levels. Correct the leak review note to the intended steam-to-air path. Coolant overpressure return to TK-401 remains a proposal; the closed transfer path is not credited as relief. Updated notes and pressure label; topology and state table unchanged. No Blender rebuild or commit.

## B-working / D-061 normal hydraulic adoption — 14 October 2026

Replace inherited SG-loss × 1.5 duty with checked full-loop losses at UM flow. Sheet 1 labels and equipment/line registers adopt the new duty and 890 K hot temperature; pump envelopes and all connection topology remain unchanged. Shared model advances to schema 2; see the engineering guide and D-061. This is still a preliminary working draft, not a named release.

## B-working / high-level SG relief — D-062

14 October 2026. The owner selects one dedicated high-level coolant-side emergency relief connection on each SG, separate from the normal gas-collection/pressure-control piping. Add shared ports `SG-101/102/103.relief_high`, lines L-101R/102R/103R, and rupture-disc concepts RD-101/102/103. No intervening isolation valves are included. Discs are normally intact and remain open after actuation; they are not operable valves in the normal state table.

The requirement is to preserve reactor coolant inventory and prevent continued gravity drainage or siphoning after relief. A high takeoff alone does not prove retention during pressure-driven two-phase discharge. B-501 is an unresolved receiving-system interface with three separate terminations; it does not select a common header, number of receivers, pit, or vent route. No cold-leg downward dump is adopted.

Exact elevations, burst differential pressure at actual disc temperature, flow area/capacity, expelled salt volume, receiving/venting arrangement, backpressure, freeze protection, burst detection/response and subsequent cooling remain unresolved. Detailed SG-failure/transient assessment remains deferred. P&ID sheet 5 records the concept; sheet 1 cross-references it. Physical 3D nozzles/routing remain pending; no Blender rebuild or pressure-calculation change.

Checks: 15 P&ID workflow tests and eight shared-view tests pass. Updated sheets 1 and 5 visually checked; disc sizing is explicitly TBD in the register. Normal operating states and main-circulation geometry/duty remain unchanged.

## B-working / counterSG hydraulic update — 14 October 2026

D-063 adopts revised SG tube geometry and checked pump/pressure results. Shared equipment duty and circulation-sheet labels update; line topology, operating states and high-level relief concepts are unchanged. Generator casing and 2 MW motor envelopes are retained.
