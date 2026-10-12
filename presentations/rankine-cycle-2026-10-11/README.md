# Rankine-cycle presentation diagram — 11 October 2026

## Motor-driven BFP alternative

The current requested alternative uses the [motor-driven BFP PowerPoint](Fast-Salt-Rankine-cycle-motor-BFP-2026-10-11.pptx)
and [3840 × 2160 PNG](Fast-Salt-Rankine-cycle-motor-BFP-2026-10-11.png).
It retains the previous visual arrangement and the complete heater connections,
replacing the auxiliary steam turbine with an electric motor. Main-IP extractions
supply HP2, HP1 and the deaerator. The earlier steam-drive snapshots remain below.

Values come from `proposed_pressure_comparison.electric` in the
[BFP comparison](../../calculations/power-cycle/bfp-drive-comparison.json):
697.1 MW gross, 25.0 MW BFP electrical consumption, 23.7 MW BFP shaft duty,
671.6 MW after BFP and condensate-pump loads, 282 MW reheat and 809 MW condenser
duty. Other station loads are excluded; 671.6 MW is not final net export.
The drawing now uses 26.5 MPa BFP discharge, 1.0 MPa condensate discharge and
0.12186 MPa LP3 extraction. SG feedwater stays at 24 MPa / 286.85°C.

The motor/pump symbols represent the aggregate duty of two operating trains,
within a candidate three-pump 50% arrangement. The cooling-water temperatures
19.7 → 27.9°C match exactly 5 kPa and the retained condenser envelope; do not mix
them with the separate coupled 20°C inlet case. Full source and modeling details
are in the speaker notes, [source/hash record](sources-motor-bfp.json), and
[Hurmet comparison](../../calculations/power-cycle/BFP%20drive%20comparison%20-%20Hurmet.md).
The [authoring source](build-diagram-motor.mjs) accepts the same two arguments as
below and reads its motor-drive values directly from the calculation files.
Publishing this alternative does not adopt a supplier design or change Blender.

## Preserved steam-driven BFP reference


A single 16:9 diagram following Thomas J. Wielenga’s supplied steam-cycle schematic, annotated with the **selected 5 kPa reference case**. All pressures are absolute. This is a preliminary cycle estimate, not a supplier-qualified equipment design.

- [Editable PowerPoint](Fast-Salt-Rankine-cycle-2026-10-11-v2.pptx): all symbols, lines and labels are native slide objects. Source and modeling notes are in the speaker notes.
- [3840 × 2160 PNG](Fast-Salt-Rankine-cycle-2026-10-11-v2.png): insert directly into a presentation.
- [Sources and exact artifact hashes](sources.json).
- [Authoring source](build-diagram.mjs).

The slide shows 1,500 MWt, 679 MW gross electrical output, 45.2% gross efficiency, 253 MW reheat and 804 MW condenser duty. Values are rounded from `selected_at_5kPa` in [reheat-selection.json](../../calculations/power-cycle/reheat-selection.json); do not mix these with the coupled 20°C cooling case. Official calculation commentary remains in the [Hurmet worksheet](../../calculations/power-cycle/Selected%20reheat%20and%20wetness%20-%20Hurmet.md).

Four HP heaters, three LP heaters, the deaerator and the steam-driven feed pump are retained. Revision 2 draws the complete extraction paths from the HP turbine, feed-pump turbine and LP turbine to all seven heaters, plus the reheater heating return to HP4 and the feed-pump-turbine supply and exhaust. Dots indicate junctions; bridges distinguish crossings. Drain cascades remain described in the footnote. Numerical values are unchanged. The first revision is preserved alongside this version. The reheater heating return is at 24 MPa / 380°C before throttling into HP4. HP exhaust is labeled before the modeled pressure loss into the reheater (2.8 MPa / 253°C becomes 2.66 MPa / 251°C). Gross electrical output includes the modeled extraction effects; net auxiliary loads remain to be resolved. Shaft symbols preserve the original conceptual grouping and do not select a turbine arrangement.

## Rebuilding

Use the bundled Node runtime with `@oai/artifact-tool`. Copy `build-diagram.mjs` into an ignored private build folder, link that folder’s `node_modules` to the runtime’s package directory, and run it with the repository root and build workspace as its two positional arguments. It writes `build/candidate.pptx` and `build/preview.png` inside that workspace. Major steam-state values are read from the JSON; the layout, rounded heater/cooling values and captions are a deliberate snapshot and must be reviewed when the cycle changes. Run the presentation finalizer and inspect the final rendered slide before publishing a new dated snapshot. Keep routine drafts and validation receipts under `outputs/`.
