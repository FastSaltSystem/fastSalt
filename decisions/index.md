# Decision record

## D-001 — Start with a local project hub

Date: 2026-10-10

Context: The project includes a growing publication history, university analysis, mechanical graphics, and a student steam-generator project.

Decision: Establish `fastSalt` locally as the central documentation and coordination repository. Keep TextualGraphics and its approved baselines intact. Record the university repositories when their locations are available. Establish a steam-generator repository after checking for existing student work.

Source: Project-owner agreement in the project conversation and creation of the local fastSalt folder.

Consequences: This initial repository contains Markdown documentation and links to existing sources. It does not publish files or create a GitHub organization.

## D-002 — Markdown is the editable documentation source

Date: 2026-10-10

Decision: Maintain project prose and the curated publication index in Markdown. Generate HTML views only when useful. Keep machine-generated file inventories separate from the curated bibliography.

Source: Project discussion comparing Markdown with the initial HTML publication index.

Consequences: Avoid independently editing duplicate Markdown, JSON, and HTML versions of the same publication record. The earlier HTML/JSON inventory is a historical first-pass aid in TextualGraphics outputs.

## D-003 — Prefer Hurmet for official calculation results

Date: 2026-10-10

Context: The project owner compared Calca, Hurmet, and Pluto using the same generator-sizing worksheet. Hurmet better fits the preferred workflow for developing and communicating estimates, while its Markdown source can be versioned.

Decision: Use Hurmet Markdown (`.md`) as the preferred official format for calculation results wherever practical. Calca, Python, Julia, and specialist analysis tools remain acceptable working tools. Where Hurmet is unsuitable, retain the reproducible source and link a readable summary rather than requiring a duplicate calculation implementation.

Responsible participant: Thomas Wielenga, project owner.

Source: Project-owner instruction: “I think we should officially have results in Hurmet if possible. It can be versioned and displayed as markdown.”

Affected work: Published project calculation worksheets, including the steam-generator calculation and proposed student deliverables. Existing university solver workflows and original research reports retain their own formats.

Consequences: Version the editable Hurmet source and save recalculated results. Generic Markdown viewers can show prose and source text but do not provide Hurmet's live calculations or full mathematical rendering; use Hurmet or generated HTML/PDF snapshots for those views. Record input provenance, checks, software versions, and preliminary/reviewed status. A format choice does not validate a calculation. See [calculation conventions](../calculations/README.md).

The Pluto conversion is a comparison experiment; there is no requirement to keep it or the Calca and Hurmet versions synchronized as parallel official worksheets.

## D-004 — Rename the graphics repository to fastSaltModels

Date: 2026-10-10

Context: The graphics work has developed from a general Python/Blender experiment into models of WISTR and the Fast Salt System installation.

Decision: Rename the existing local `TextualGraphics` repository folder to `fastSaltModels`, preserving its Git history, tags, approved baselines, and working outputs. Keep `fastSalt` as the documentation and coordination hub and PracticalMechanicalSimulation as a separate project. The internal Python package remains `textual_graphics`.

Source: Project-owner approval to change the graphics repository name.

Consequences: Update sibling documentation links and the app's project-folder setting. Earlier references to TextualGraphics describe this same repository under its former name. No new repository or public remote is created by this rename.

## D-005 — Revise the installation layout and pump allowance

Date: 2026-10-10

Decision: Place the reactor concrete well directly on the sub-floor, use three
17 m steam-generator casings with both salt manifolds on the right and water/steam
manifolds on the lower/upper left, add three cold-leg pumps, common secondary
headers exiting the building, and six external absorber supply/control envelopes.
Right/left are viewed from the reactor toward each generator. Remove building
circumference railings and increase building height to accommodate the generators.

Responsible participant: Thomas Wielenga, project owner. Source: explicit layout
instructions and clarification of viewing convention and external absorber modules.

Affected work: installation graphics and interfaces IF-001/IF-003. The isolated
reactor baseline, original generator worksheet, and historical analyses are retained.

Provisional implementation: raise the building, crane and stacks 7 m; use the
original generator pressure-loss duty plus 50% at unchanged flow, then assume 80%
pump and 96% motor efficiencies. Reserve a 2 MW motor per leg. Physical equipment
envelopes, header diameters and storage relocations remain draft choices for review.
See the [pump estimate](../calculations/steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md)
and [installation guide](../../fastSaltModels/docs/installation.md#earlier-layout-revisions).

## D-006 — Use a single-floor equipment layout

Date: 2026-10-10. This revises the placement/orientation portions of D-005.

Source and responsible participant: Thomas Wielenga's explicit request to rotate
the generators 90°, remove the intermediate floor, give pumps bottom suction and
raised supports, support generators from the floor, align lower manifolds and
pump outlets, put storage on the floor, and raise absorber supports to vessel-top
level. Affects installation graphics and interfaces IF-001/IF-003.

Implementation: salt manifolds face inward; water/steam face outward. Generator
centres are at radius 10 m, 0.7 m outward from the preceding draft. Provisional
steel frames raise generator bottoms 2.1 m and pump casing bottoms 2.4 m above
the sub-floor. Pump outlets align with lower manifolds; generator return still
feeds pump suction, preserving circuit direction. Absorber platform tops match
the vessel-top datum. Storage rests on the floor. The existing building envelope,
2 MW motor allowance and approved reactor baseline are retained.

Consequences: updated draft views supersede the previous intermediate-floor
layout. Support member sizing and piping pressure losses remain to develop.
See the [current installation guide](../../fastSaltModels/docs/installation.md).

## D-007 — Lower generators, stacks and crane

Date: 2026-10-10. Revises the generator supports and building elevations in
D-005/D-006; their records remain as earlier layout decisions.

Source and responsible participant: Thomas Wielenga requested floor-level stack
bases, 5 m generator-to-hoist clearance (clarified as underside of hoist body),
and then floor-mounted generators to simplify pump inlet connections. Affects
installation geometry and interfaces IF-001/IF-003.

Implementation: remove 2.1 m generator frames; casing bottoms meet Z=−9.1 m.
Cold manifolds feed level suction runs at Z=−7.9 m with two bends into the raised
pumps. Side discharge still returns salt to the reactor. Generator top covers
are Z=8.03 m and hoist body underside Z=13.03 m; the crane runway is Z=12.005 m.
Roof and crane are lowered 9.295 m relative to D-005/D-006, giving a 31.905 m
building envelope including the lower level. Stack base bottoms meet the floor;
the 35 m tubes stand on 1 m bases. The hook is depicted raised.

Checks: world-space mesh bounds verify generator/stack floor placement and 5 m
hoist-body clearance; pipe endpoints and two-bend suction topology are checked.
These are visual layout checks; pumping duty and equipment ratings are unchanged.

## D-008 — Widen installation and combine cooling-air headers

Date: 2026-10-10. Source and responsible participant: Thomas Wielenga requested
more space, one large exhaust stack, a high hot-air manifold, and fresh-air
connections to the reactor, fuel maintenance tanks and steam generators. He
explicitly approved a **36 m** building diameter for the draft.

Implementation choices for review: generator radius 12 m; fuel tank pair radius
10.8 m; pumps moved outward 2 m; secondary header radius 15 m. The hot-air ring
is inside the wall at Z=10 m, above generators and below the crane. A fresh-air
C-header sits low outside the wall to free the equipment aisles and leave space
around the single rear stack. Reactor crossovers attach to the actual hood
stubs and are marked removable. All ten items have hot and fresh connections.
Provisional diameters: stack 3.6 m, hot ring 2.4 m, fresh header 2 m. The existing
5 m generator-to-hoist-body clearance and floor-level equipment remain.

Affects IF-001/IF-003 and introduces IF-004. The new generated folder is
`outputs/installation-air-layout`; preceding drafts are preserved. Geometry
checks cover connection topology and selected clearances; no air-flow, thermal,
natural-draft, structural or complete maintenance-path analysis is implied.

## D-009 — Draft exterior concrete air plenums

Date: 2026-10-10. Source: Thomas Wielenga requested exterior concrete rings for
fresh air at the bottom and hot air at the top, with the upper ring connected
to the stack. He also raised an under-floor supply plenum as an alternative.

The draft implements full hollow exterior rings, each with provisional 3 × 3 m
gross section and 0.25 m skins, attached to the 36 m building shell. Their outer
diameter is 42 m. The fresh ring rests at the floor; the hot ring ends at the
roof springline. Stack radius becomes 24 m. Air branches remain connected to
the reactor, three generators and six maintenance tanks. The reactor's current
hood flow and removable connections are retained. Affects IF-003/IF-004.

The rings are architectural envelopes; structural action, reinforcement,
thermal protection and airflow performance remain unverified. Strengthening
is not an adopted calculation result. The floor-plenum alternative remains
unimplemented pending comparison of access, drainage, foundations and revised
reactor/outer-hood airflow. Earlier round-duct drafts are preserved.

## D-010 — Keep air risers inside and clear the cold ring with feedwater

Date: 2026-10-10. Source: Thomas Wielenga requested the hot manifold below the
crane, equipment air connections rising inside the wall and penetrating only at
the ring, and the cold-water inlet crossing above the cold-air manifold.

The hot concrete ring is lowered to Z=8.5–11.5 m, leaving 0.205 m below the crane
runway underside. Both sets of equipment air routes now cross the wall
horizontally through their rings' inner webs: Z=10 m hot and Z=−7.6 m fresh.
The former external risers and ring-floor/roof entries are removed. Feedwater
rises inside before its external connection, placing the pipe underside 0.5 m
above the lower ring roof. Its distribution header and generator ports stay at
the existing low elevation. Affects IF-001/IF-003/IF-004 and supersedes these
placement/routing portions of D-009.

Checks cover twenty connected air routes, inside-wall riser envelopes,
ring-level penetrations, hot-ring crane clearance, and the raised feedwater
crossing. This remains a visual draft with provisional clearances.

## D-011 — Generator top air valves and half-pipe collectors

Date: 2026-10-10. Source: Thomas Wielenga requested hot-air outlets at generator
tops, boxes representing butterfly valves with ducts leaving their tops, and
half-pipe side manifolds replacing the series of right-angle branch pipes.

Implementation: each generator carries one 1.2 × 1.2 × 0.6 m valve-box envelope
on its roof and an upward hot-air outlet. Four D-section half-pipe collectors
attach directly to the casing. Short end transitions join the unchanged round
pipe terminals. The three branch stubs formerly on each collector are removed.
The crane and roof rise 0.6 m to retain the prior 5 m hoist-body clearance above
the new valve-box tops. The hot ring remains at Z=8.5–11.5 m, now 0.805 m below
the runway underside. Affects IF-001/IF-003/IF-004.

Checks verify twelve collectors, casing attachment, absence of old stubs,
terminal continuity, three roof valve boxes, upward air outlets and hoist
clearance. Internal manifolding, valve mechanism, wall thickness and losses
remain outside this visual draft.

## D-012 — Enlarge generator collectors and separate fresh-air inlets

Date: 2026-10-10. Source: Thomas Wielenga requested fresh-air entry on a side
90 degrees from the process manifolds, 50% larger manifold diameters, and
smoother pipe transitions. Affects IF-001/IF-004.

The four collectors per generator now have diameters of 2.1 m (both salt),
1.2 m (steam), and 0.75 m (feedwater). External pipe diameters and terminal
positions are retained. Smooth lofts and short round collars replace abrupt
transitions; secondary connections curve outward to match their radial pipes.
Fresh-air entries move to the perpendicular side opposite the pump, with an
initial approach normal to that casing face, then route to the low supply ring.

Geometry checks cover enlargement, terminal radii and tangents, floor clearance,
and perpendicular air entry. This is a visual revision; pressure losses,
collector internals and fabrication remain to be designed.

## D-013 — Shared absorber supports and equipment access beside sector storage

Date: 2026-10-10. Source: Thomas Wielenga requested larger combined supports
for each absorber pair and a building doorway near sector storage, interrupting
the fresh-air ring for floor-level passage. Affects IF-003/IF-004.

Three provisional 1.8 × 4.2 m braced steel platforms replace six separate
frames, keeping the module/deck elevation at Z=−2.02 m. A provisional open
4.5 × 6.5 m equipment doorway is placed at plan angle 18°. The wall and its
intersecting pilaster are cut. A 5.5 m minimum sealed-end gap in the fresh-air
plenum aligns with the door and a level apron. The fresh passage becomes a
continuous C shape connecting all existing branches; the hot ring is unchanged.

The straight access lane clears the existing coolant tank, so relocation is
unnecessary. Selective geometry checks do not establish vehicle swept paths,
site grading, door containment performance or support capacity.

## D-014 — Apply calculated pipe and insulation envelopes to the installation

Date: 2026-10-11. Source: Thomas Wielenga requested the Blender reactor-building
model be redone using the calculated pipe sizes and insulation, with building
resizing as needed. Affects IF-001, IF-003 and IF-004. Status: implemented draft
for review; the specific 42 m dimension is a provisional fit choice.

Use the four Hurmet wall/insulation worksheets as conditional visual inputs.
Keep distinct bore, nominal wall, bare OD and insulation OD, with separate metal
and insulation meshes. Enlarge the equipment shell from 36 to 42 m and exterior
ring envelope from 42 to 48 m. Move generators/storage outward, raise low salt
and water ports and pump frames, and route reactor fresh air underneath the
raised feedwater header. Retain the floor-mounted generators, exterior plenums,
open doorway and 5 m hoist-body clearance. The detailed source reactor is
preserved; adapt nozzle sleeves only in its installation copy.

The build records worksheet hashes and selective interference/connection/access
checks. It does not establish approved pressures/materials, structural span or
supports, thermal performance, complete lifting paths or pipework fabrication.
[Dimensions and checks](../../fastSaltModels/docs/installation.md#insulated-process-piping--11-october-2026).

## D-015 — Develop a separate six-sector insulation cover with sliding pickups

Date: 2026-10-11. Source: Thomas Wielenga's cover and remote-lifting proposals,
followed by his choice to return from pivoting catches to straight sliding hooks
and authorization to proceed. Status: concept implemented for review.

Develop a removable thermal-cover subassembly in fastSaltModels, with its
requirements and interfaces in fastSalt. Keep the six pressure-retaining caps
separate. Cassette boundaries follow spider-leg centrelines. Reuse the common
two-bar lifting interface, with four captive shoulders that contact an internal
frame only during load take-up. A 40 mm stroke and 500 mm stone-wool allowance
are provisional model choices. Record stem positions visibly; do not treat them
as load confirmation. Reactor service penetrations, final seating and replacement
of the hood cooling circuit remain to be designed. No new repository is created.

[Assembly brief](../design/reactor-insulation-cover.md) and
[model/checks](../../fastSaltModels/docs/insulation-cover.md).

## D-016 — Zirconia seating with an upper frame and tension hangers

Date: 2026-10-11. Owner: Thomas Wielenga. Source: user direction to use tension
rods, lateral wire bracing and zirconia thermal breaks. Status: visual concept
implemented; material grade and dimensions provisional. Extends D-015.

Move the carrying frame near the cassette top. Suspend each grid tray and the
bottom liner independently on tension hangers; use separate compression posts
for the resting load. Put four zirconia blocks under those posts, with shallow
fixed lower cups and removable upper feet. Keep metal retainers from bridging
the ceramic. Preserve straight sliding hooks and their 40 mm resting gap.

The draft uses Ø50 × 75 mm ceramic blocks. This is a layout choice, not a
qualified ceramic specification. Record contact stress and axial conduction in
[Hurmet](../calculations/reactor/Zirconia%20cover%20supports%20-%20Hurmet.md).
Recheck the actual cassette mass, CM and common-tool interface. Lower attachment,
post insulation, hot properties, contact stresses and complete thermal/structural
qualification remain open. [Assembly brief](../design/reactor-insulation-cover.md).

## D-017 — Compare a rigid-block insulation cassette before selecting the cover

Date: 2026-10-11. Owner: Thomas Wielenga. Source: concern about apex sag and
request to explore rigid calcium silicate with tension supports. Status:
preliminary alternative authorized; no material or assembly selection made.

Preserve D-015/D-016 and the wool model. Develop a separate rigid-block cassette
with blocks stacked in compression, one bottom retaining tray, distributed ties
to an upper lifting frame, and the existing common-hook interface. Compare mass,
envelope and approximate seated/lifted deflection. Do not credit block joints
with composite bending strength or treat published compression at 5% strain as
an allowable. [Comparison](../../fastSaltModels/docs/rigid-insulation-cover.md)
and [Hurmet](../calculations/reactor/Rigid%20cover%20cassette%20-%20Hurmet.md).

## D-018 — Develop the recessed T-grid cover with assumed bonded facing

Date: 2026-10-11. Owner: Thomas Wielenga. Source: direct-seating, recessed T-bar,
ceramic-washer and coating proposals, followed by explicit direction to assume
the coating works and design the assembly. Status: current preliminary direction.

Remove compression posts and the full bottom tray from the rigid-block candidate.
Support grooved bottom blocks with a recessed T-grid hung from the upper frame.
Use zirconia washers and sleeves at rod/frame attachments. Rest the coated bottom
on the sector cap; distribute the upper frame's resting load onto the upper blocks.
Preserve independent sector removal and the common four-hook lifting interface.

Use 2 mm refractory facing and joint cement with provisional density and assume
adhesion/handling durability for this study. No specific product is selected and
no block/coating composite structural capacity is credited. Keep prior models
as historical comparisons; their four-post seated solution no longer applies.
Actual cap hardware reliefs, grid connection details and material qualification
remain outside this geometry revision.
[Current model](../../fastSaltModels/docs/tgrid-insulation-cover.md) and
[Hurmet worksheet](../calculations/reactor/T-grid%20cover%20-%20Hurmet.md).

## D-019 — Suspend each rigid insulation layer on its own recessed T-grid

Date: 2026-10-11. Owner: Thomas Wielenga. Source: clarification that assembly
starts with bottom blocks and T-bars, then further grids slide onto the supports
and are crimped at their own levels. Status: current preliminary geometry.
Extends D-018; supersedes its single grid carrying the whole insulation stack.

Provide five grids on shared vertical rods, one for each nominal 100 mm layer.
Model sliding saddles with individual crimp stops beneath them. Each groove and
collar carries its own layer; rod and upper attachment loads accumulate upward.
Retain recessed flanges, ceramic upper connections, assumed underside facing and
the common sliding-hook interface. Preserve the previous model as a comparison.

The Ø12 × 10 mm collars and saddle details are provisional model choices, not
user-selected specifications. Blocks contact at rest; adjust collars to distribute
lifting loads by layer. Recalculate added steel mass and cumulative hanger loads.
Rod stretch and thermal expansion require load-sharing assessment; crimp slip, groove breakout and weld capacities
are unresolved. Open Blender with actual insulation visible to distinguish the
T-grids from the upper frame and gray sector-cap reference.
[Model](../../fastSaltModels/docs/tgrid-insulation-cover.md) and
[Hurmet](../calculations/reactor/T-grid%20cover%20-%20Hurmet.md).

## D-020 — Retain five grids and use plain upper blocks on T-bar flanges

Date: 2026-10-11. Owner: Thomas Wielenga. Source: explicit preference to retain
all five grids for robustness despite added weight, and to use grooves only in
the bottom layer. Status: current preliminary visual arrangement; extends D-019.

Keep the bottom recessed grid and four upper grids on shared rods and individual
crimp stops. Place the upper block undersides on the upper flanges, with the webs
in block joints. Preserve 500 mm total nominal block thickness; four intervening
3 mm flanges increase the stack to 512 mm. Shift frame, shell and hook elevations
by 12 mm. Recalculate mass and load screening. Removal of upper groove lips does
not establish a quantified strength increase: flat-block spanning, strip-bearing
compression, crimp capacity and hot properties remain to check.
[Model](../../fastSaltModels/docs/tgrid-insulation-cover.md).

## D-021 — Replace the reactor hood with six insulation covers and side air plenums

Date: 2026-10-11. Owner: Thomas Wielenga. Source: explicit direction to replace
the hood with the developed insulation and move hot/cold ducts to side manifolds
connected to the vessel's surrounding air space. Status: working visual integration.

Retain pressure caps and the vessel's downflow/underfloor/upflow air circuit.
Fit six five-grid cassettes above the caps. Close the annular passages at the top
and collect/distribute air through separate side plenums; sleeve the hot crossover
through the cold passage. Retain provisional 2 m side stubs. Local azimuths,
plenum envelopes, hook pockets, service inserts, frame collars and outward
absorber-platform positions are model choices for review, not approved engineering
specifications. Connect the revised reactor to the building air rings.

Preserve earlier approved baselines. Operating service extensions, fitted frame
and insulation strength, local bearing, thermal bridges, draft/pressure drop and
structural well openings require further design. Do not carry the standalone
cassette's grillage results or mass into the fitted assembly without recalculation.
[Reactor guide](../../fastSaltModels/docs/reactor-study.md#insulation-covers-and-side-air-connections--11-october-2026).

### D-021 refinement — Direct floor route for reactor fresh air

11 October 2026, explicit owner request: remove the fresh-air high crossover.
Run directly along the floor from the lower building ring, rising only at the
reactor side manifold. Retain the 2 m provisional duct and ring-centre elevation
of 1.5 m above the slab. Support and airflow design remain provisional.

### D-021 checkpoint — Accepted insulated installation

11 October 2026: the owner accepted the direct floor-level reactor fresh-air
route and requested a commit. `fastSaltModels` commit `a99002f` preserves the
current reactor, standalone cover and installation, plus draft images, geometry
reports and a hash manifest in
[the dated checkpoint](../../fastSaltModels/baselines/wistr-insulated-installation-2026-10-11/).
Earlier baselines remain unchanged. This records acceptance of the visual draft,
not engineering qualification. The model checkpoint and this documentation
checkpoint are separate local Git commits.

## Proposals not yet adopted

- A common Python engineering definition with adapters for graphics and analysis tools.
- Public GitHub organization and repository names.
- Code, documentation, and design-material licensing choices.
- Final student and university repository arrangements.

## Format for subsequent decisions

Use a stable ID, date, context, decision, responsible participants, source, affected models/interfaces, and consequences. Preserve superseded decisions and link to their replacements.
