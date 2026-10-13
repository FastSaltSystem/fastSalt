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

## D-022 — Insulate hot-air ductwork in the working model

Date: 2026-10-11. Source: explicit owner direction after checkpoint `a99002f`.
Status: working visual design; thermal sizing pending.

Apply insulation to the hot-air branches, reactor side collector/crossover and
stub, upper manifold, stack connection and barrel. Use a provisional 100 mm layer
and 1 mm metal cladding for space coordination. These thicknesses are model choices,
not owner-specified or thermally qualified values. Enlarge the upper manifold to
fit the liner and wrapped connection, and adjust affected hot routes for clearance.
Retain the floor-level fresh-air route and preserve the committed checkpoint.

## D-023 — Add provisional turbine and fuel-preparation buildings

Date: 2026-10-11. Source: owner requested both buildings and explicitly chose
“Use provisional sizes and locations.” Status: working visual layout.

Create a separate site scene around the current installation. Use a 45 × 24 m,
20 m high turbine envelope beside the west/southwest secondary outlets and a
30 × 24 m, 14 m high fuel-preparation envelope east/northeast across a service
yard. These dimensions and locations are model assumptions approved for drafting,
not equipment or process sizing. Preserve the reactor door approach, air intake
and stack. Continue the existing steam/feedwater jackets to open interface ends
inside the turbine building. Keep fuel preparation at envelope level.

Use a common visual access pad at the existing −9.1 m equipment-floor datum;
actual site grading remains open. No containment, shielding, transport qualification
or fuel-processing capacity is implied. See the
[site guide](../../fastSaltModels/docs/site-study.md). Earlier checkpoints remain unchanged.

## D-024 — Start the Rankine cycle from the supplied system diagram

Date: 2026-10-11. Source: owner supplied Diagram.pdf and confirmed “Yes—use
main-steam reheat as drawn” and “Use that provisional condenser case” for a
water-cooled condenser at 5 kPa absolute. Status: preliminary calculation basis.

Retain the HP/reheat/LP turbine arrangement, regenerative heater banks and
steam-driven feed pump. Carry forward 1,500 MW thermal, 24 MPa, 830 K main steam
and 560 K return feedwater. Extraction pressures, efficiencies, 470°C reheat,
360°C heating-stream return and 20–28°C cooling water are provisional model
choices, not additional owner-specified values. The 500°C reheat trial was
rejected for temperature crossover under the same return assumption.

Publish results in Hurmet with imported water properties and coupled flows clearly
identified. The Python/CoolProp solver remains authoritative for state properties
and coupled balances. LP moisture, equipment adequacy, net export and building fit
remain open. See [cycle basis](../calculations/power-cycle/README.md).

## D-025 — Provisional cooling-water design cases

Date: 2026-10-11. Source: owner accepted the proposed 20°C normal reference,
30°C hot-weather design case and 35°C extreme check with “That sounds good.”
Status: accepted preliminary environmental assumptions; no site selected.

These are temperatures of water entering the condenser, not outdoor air
conditions or claimed occurrence percentiles. Use the hot case to guide cooling
system sizing and the extreme case to examine potential reduced output. Normal
operation need not remain at the hot-day condenser pressure. Set the minimum
permitted condenser pressure after checking LP wetness and turbine limits,
including later cooler-than-reference conditions.

The first follow-up holds the existing approximately 38,500 m² condenser area,
U = 2,500 W/(m² K) and 23.76 m³/s cooling flow fixed. It is a screening comparison,
not acceptance of that equipment size or permission to operate at the calculated
pressures. The permissible hot-day pressure/output and final heat sink remain to
choose. See [cooling cases](../calculations/power-cycle/Cooling-water%20cases%20-%20Hurmet.md).

## D-026 — Select a preliminary reheat/wetness solution

Date: 2026-10-11. Source: owner directed “OK, let's resolve them” after the
reheat/wetness discussion and acceptance of the cooling-water cases.
Status: analyst-selected working thermal-cycle design, not supplier qualification
or owner-specified numerical inputs.

Use 2.8 MPa HP exhaust, 2.66 MPa hot reheat at 510°C, and a 380°C main-steam
heating return. Shift the feed-pump-turbine heater extractions to 1.6/1.0 MPa to
retain positive heater bleeds. Preserve the single main-steam reheater and the
24 MPa / 830 K steam-generator interface. Use a provisional 5 kPa condenser floor
at these reheat conditions, with cooling control still to design.

The selected case clears the 10% moisture screen for the accepted 20/30/35°C
cooling-water cases and for LP interval efficiencies 0.86–0.90 at 5 kPa. The
minimum reheater approach is about 20.28 K. At exactly 5 kPa it costs approximately
10.82 MW gross relative to the first trial; heating-steam fraction rises from
15.96% to 26.28% and reheater duty from 189.4 to 252.5 MW. This favors thermal and
flow margins over highest calculated output. Old trial results are preserved.

This resolves feasibility within the stated steady-state model. Actual turbine
wetness/exhaust limits, pressure losses, thermal equipment design, cold-weather
controls, startup/transient operation and net station loads remain to establish.
See [selected worksheet](../calculations/power-cycle/Selected%20reheat%20and%20wetness%20-%20Hurmet.md).

## D-027 — Develop preliminary power-plant equipment sizes

Date: 2026-10-11. Source: owner requested “Now let's size what we can.” Status:
analyst-selected sizing assumptions and layout candidates for review, not
owner-specified dimensions or supplier-qualified equipment.

Use D-026's selected cycle for the first equipment schedule. Preserve its condenser
thermal basis; divide it provisionally into three modules. Estimate reheater surface
using U=1,000 W/(m² K) and a 20% allowance, with four candidate modules. Seven
heater area proxies use U=2,000 with the same allowance. Record sensitivities.
Screen six LP exhaust flows, generator capacities at 0.90 power factor with 10%
margin, ten minutes usable deaerator storage, and three 50% pumps per water service.
Pipe velocities, packing, pump heads, NPSH and service clearances are explicit
assumptions in the [worksheet](../calculations/power-cycle/Power%20plant%20equipment%20sizing%20-%20Hurmet.md).

Propose 26.5 MPa BFP discharge and 1.0 MPa condensate discharge to cover loss and
elevation budgets. Do not promote those values to the coupled operating basis yet:
BFP shaft duty rises 2.28 MW, so pump-turbine extraction flows, heaters, SG states,
reheat approach and performance must be reclosed. Preserve the existing diagram,
performance results and main-pipe wall study. No building or reactor geometry is
changed; check a dimensional plant arrangement before resizing the turbine building.

## D-028 — Evaluate electric boiler-feed-pump drive

Date: 2026-10-11. Source: owner requested examination of electric drive, preferring
simplicity if efficiency loss is not significant. Status: completed preliminary
comparison; analyst recommendation for review, not final drive selection.

Compare both drives at the D-027 proposed 26.5 MPa BFP / 1.0 MPa condensate-pump
pressures. Retain the SG interface and selected reheat conditions. Reclose the
steam-driven reference with LP3 at 0.12186 MPa to use its auxiliary exhaust in the
DA; use the same LP3 pressure for the electric alternative. In the latter, feed
HP2/HP1 from 1.6/1.0 MPa main-IP extractions and the DA from its 0.6 MPa outlet.

With 95% combined electrical-drive efficiency, electric drive costs 4.03 MW or
0.269 percentage points at 5 kPa, about 0.60% of comparison output. The same
condenser in 20/30/35°C water gives 4.12–4.23 MW penalties. This favors electric
drive as a simpler candidate, subject to review of the trade. Its reheater needs
281.6 MW duty versus 250.1 MW in the matched steam case; retain 3 × 50% pumps with
15 MW motor shaft allowances as a candidate only. Reheat/main-IP flow, hot heater
bleeds, pipe sizing, electrical supply and startup steam must be reconciled before
adoption. Full station loads and lifecycle economics are not yet evaluated.

Preserve D-026/D-027 result files, equipment schedule and diagram. The alternative
is isolated in its [Hurmet worksheet](../calculations/power-cycle/BFP%20drive%20comparison%20-%20Hurmet.md)
and reproducible coupled calculation. Hurmet imports property/cycle results and
independently checks power, efficiency and capacity arithmetic.

## D-029 — Carry motor BFPs into equipment sizing and the first hall layout

Date: 2026-10-11. Source: owner said “ok, proceed” to update the equipment
schedule/piping and test the turbine-building layout. Status: working preliminary
motor-drive revision; no vendor, pressure-boundary or civil design qualification.

Use D-028's motor case as the current equipment-sizing source. Adopt for layout
four 16 × 3.25 × 3.25 m reheater envelopes (9,122 m² total), 550/350 MVA generator
allowances, three 50% BFPs with 15 MW motors and 20 MVA per-train BFP-only supply
allowances. Revise the five pipe bores identified in the current worksheet and
remove the auxiliary pump-turbine supply service. Retain unchanged pump hydraulic
requirements, condenser surface and deaerator storage; update their operating
loads/flows from the motor cycle. Preserve original steam-drive outputs.

Use a provisional 66 × 40 × 28 m hall, 20 × 10 × 7 m electrical annex and tube
withdrawal aprons for the first dimensional draft. Turbines are at +12 m, minimum
DA water level +14 m and crane underside +25 m. These are analyst reservations,
not new owner-specified dimensions or proof of complete plant fit. The east wall
and steam/feedwater interface remain fixed; the pad expands to accommodate the
westward hall extension and external maintenance areas. The earlier empty 45 ×
24 × 20 m box remains documented; the larger draft is not attributed solely to
the drive change. Fuel-preparation scope remains unchanged.

Verification: all bores pass the retained velocity screens in four cases; Hurmet
save/reopen passes 50 comparisons and two sensitivities; 29 equipment boxes and
16 service reservations pass selected 3D overlap/containment checks. Source,
model and scope are recorded in the [worksheet](../calculations/power-cycle/Motor-BFP%20equipment%20sizing%20-%20Hurmet.md)
and [site guide](../../fastSaltModels/docs/site-study.md). Full piping, structure,
installation access, egress, rotor handling and crane adequacy remain open.

## D-030 — Arrange turbine equipment around the steam-entry side

Date: 2026-10-11. Source: owner requested grouped reheaters near steam entry,
LP turbine/condensers to the left, BFPs between HP/LP equipment, and reversal of
the HP/IP train to place both generators together. Status: preliminary layout
implemented; HP/LP equipment interpreted as the feedwater-heater banks.

Keep D-029 equipment sizes and the 66 × 40 × 28 m hall. Group all four reheaters
on the east/right; put three condensers and LP casings on the west/left. Place
BFPs between the LP and HP heater banks, with DA storage above. Reverse HP/IP so
the turbine is near the east steam entry and its generator aligns alongside
the LP generator. Move the electrical annex to the central south frontage,
leaving separate heater withdrawal aprons on either side.

The revised 29 equipment boxes and 16 service volumes pass selected 3D overlap,
wall/vertical clearance, external pull-apron coverage and arrangement checks.
No cycle, equipment capacity or piping size changes. Shorter steam/electrical
connections are a layout intent, not a calculated pressure-loss or cabling result.
Internal piping, structural support, full access and crane coverage remain open.
See the [current plan and model](../../fastSaltModels/docs/site-study.md).

D-030 follow-up: the owner requested checking space for condensate pumps along
the west wall, before the LP heaters. Move the three existing pump envelopes
there and shift the LP heater bank 2.25 m east. Reserve a 1.2 m pump-side access
strip; retain the 3 m cross aisle, condenser locations and hall size. The revised
29 equipment boxes and 17 service volumes pass the selected checks. Outlet
positions, suction head, piping length and pump removal paths remain unresolved.

## D-031 — Rotate BFPs and shorten the turbine hall

Date: 2026-10-11. Source: owner proposed turning the BFPs 90° to reduce building
size. Status: preliminary dimensional draft; full installation fit unresolved.

Rotate each existing 10 × 4 m BFP/motor envelope to 4 × 10 m and arrange the
three side by side with 2 m gaps. Retain a 4 × 10 m laydown area and reserve a
2 m front-access strip leading to the 3 m cross aisle. Move HP heaters and
reheaters inward and shorten the main hall from 66 to 60 m, retaining its 40 m
width and 28 m height. The east steam/feedwater interface remains at X=−36 m;
the hall centre moves to (−66, −10) m. The annex remains 20 × 10 × 7 m.

Main-hall area reduces 240 m², from 2,640 to 2,400 m² (9.1%). Equipment capacities,
envelope dimensions apart from orientation, and cycle results are retained.
Twenty-nine equipment boxes and 18 service reservations pass selected overlap,
containment, apron and vertical-clearance checks. Detailed piping, structure,
transport/rotor handling and crane access remain unresolved. The present turbine
trains limit further shortening without rearrangement; this is not a minimum.
Earlier 66 m drafts remain preserved in outputs/site-study-motor through -v3.

## D-032 — Align the buildings and enter the turbine wall squarely

Date: 2026-10-11. Source: owner requested bends near the reactor and improved
building alignment so steam/feedwater enter the power-plant wall at right angles.
Status: provisional geometry implemented and checked.

Keep the reactor at its established origin and translate the turbine hall, annex,
equipment and maintenance aprons 10 m north, placing the hall centre at (−66, 0) m.
Retain the 60 × 40 × 28 m hall and the east wall at X=−36 m. Bend both pipes near
X=−28 m onto a shared westward approach at Y=−4.19484 m. Shift the wall bay and
pipe-rack frames to suit; update internal terminal tangents to the wall-normal run.
Preserve reactor nozzle tangents and all existing pipe dimensions and elevations.

Check building/air-ring separation, pipe envelopes around the reactor, bend radii,
wall opening, exact internal/site endpoint and tangent continuity, plus existing
internal route/stage checks. The 4.70 m feedwater clearance issue and pressure-loss,
thermal-expansion, support and maintenance-review limitations remain open. Earlier
site/piping outputs are preserved. See the [site guide](../../fastSaltModels/docs/site-study.md).

## D-033 — Gentler interbuilding pipe offsets

Date: 2026-10-11. Source: owner requested two 45° bends between buildings.
Status: provisional geometry; subject to routing review.

Use two opposite 45° bends on both steam and feedwater offsets. The existing
reactor outlet points 20° away from the turbine-wall normal, so the site copy
adds a separate shallow 20° alignment turn just outside the reactor before the
two-bend offset. This is three horizontal direction changes overall, not two.
The original reactor wall penetration, building locations, turbine interfaces,
pipe sizes and elevations remain unchanged. Move the illustrative support frames
under the final straight section. The source installation and prior site drafts
remain preserved. Geometry checks cover bend angles, endpoints/tangents and
selected clearances; pressure loss, flexibility and support design remain open.
See the [site guide](../../fastSaltModels/docs/site-study.md).

## D-034 — Shared reactor catwalk and distributed absorber modules

Date: 2026-10-12. Source: owner requested an expanded-metal catwalk near the
vessel top, replacement of the absorber stands and service connections; owner
selected one module opposite each absorber rather than three pairs.
Status: provisional model generated; connection and selected clearance checks passed.

Use a 4.95–7.15 m annular deck at installation Z=−1.20 m with six modules at
radius 6.60 m. Dedicated steel bearing pads share the catwalk frame. Route each
absorber's four existing 25/50 mm stubs to its own module through removable
spider-side jumpers and under-deck tubing. Add passages to the absorber insulation
inserts in the installation copy. Original reactor source and prior site snapshots
remain preserved. Deck/frame sizing, tube thermal treatment, remote connectors,
access stairs and maintenance qualification remain open. See the
[installation guide](../../fastSaltModels/docs/installation.md).

## D-035 — Connect sector service plugs to maintenance tanks

Date: 2026-10-12. Source: owner requested piping from the fuel-maintenance tanks
to the ports on the sector tops. Status: provisional routing generated; connection and
selected static clearance checks passed.

Retain the three independent 25/50 mm tube pairs per sector and use one dedicated
tank per sector. The layout assignment is S1→T6, S2→T1, S3→T2, S4→T3, S5→T4,
S6→T5, keeping the routes ordered around the building. Route through the existing
removable core-service thermal inserts, outward and beneath the catwalk, then to
six separate roof nozzles on each tank. Show removable cap-side jumpers and tank
connections. The actual sector stub coordinates and diameters are retained;
tank nozzles, wall thickness, unions and routing elevations are provisional.
This adds visual connectivity, not a fuel-transfer sequence, hydraulic/thermal
result, tank-internal design or handling qualification. Tube heating/insulation,
valves, supports and maintenance sweeps remain open. See the
[installation guide](../../fastSaltModels/docs/installation.md).

## D-036 — Double the absorber-module tank volumes

Date: 2026-10-12. Source: owner requested twice the volume with the same or similar
aspect ratio. Scale the six absorber tank envelopes uniformly by 2^(1/3), from
0.640 m diameter × 1.000 m height to 0.80635 × 1.25992 m. Nominal cylinder volume
changes from 0.32170 to 0.64340 m³ each. Preserve tank bottom elevations and existing
connections; raise the unchanged control boxes and panels by 259.9 mm. Existing
module seats accommodate the wider tanks. These are geometric envelope volumes;
usable salt capacity and increased equipment/support loads remain to establish.
Earlier installation snapshots remain preserved. See the
[installation guide](../../fastSaltModels/docs/installation.md).


## D-037 — Add paired absorber reservoirs and raise the catwalk

Owner-approved 12 October 2026: two reservoirs and two independent modules per
absorber (12 of each). Large 50 mm spider lines connect to reservoir bottoms;
reservoir tops and the separate 25 mm spider lines connect to their matching
modules. No shared absorber-salt manifold is introduced. Catwalk Z rises from
−1.20 to +0.50 m; outer radius grows to 7.35 m, inner radius stays 4.95 m.
Reservoir bottom Z=1.05 m provides 2.70 m fall to the existing spider terminals.
External drains have continuously descending rounded paths; internal inherited
paths are checked for no upward step. Pressure/gas displacement and drainage
rates are not established by that geometric check.

Reservoir dimensions reuse 0.80635 m diameter × 1.25992 m height provisionally;
capacity is not sized against required absorber inventory. Existing module tanks
retain D-036 dimensions. New reservoir insulation is a provisional 100 mm with
1 mm cladding and electric heating allowances; individual service insulation
is provisionally 50 mm, with a removable common enclosure around close-pitch
spider tubing. These values reserve space, not thermal performance. Structural
ratings, access stairs, supports, heater duty, controls and handling sweeps remain
open. See the [installation guide](../../fastSaltModels/docs/installation.md).

## D-038 — Compact heated bundles beneath liftable insulation

Owner-approved 12 October 2026: replace bulky service enclosures with compact
insulated tubes and open-bottom channels under the removable insulation covers.
Only the large absorber salt lines are heated; paired gas lines share insulation.
Tank-top gas lines are insulated but unheated. All 36 fuel-maintenance lines are
heated, arranged in six insulated bundles retaining independent tube pairs.
Twelve reservoirs and twelve modules remain. Catwalk Z=−0.60 m is 1.10 m below
D-037; tank bottom Z=−0.05 m retains 1.60 m fall to spider terminals. No external
salt drain has an uphill segment. Fifty-millimetre bundle insulation remains a
visual allowance, not a thermal sizing result.

The intended mechanical access sequence lifts insulation before disconnecting
cap-side services. Installation cassette copies have open-bottom channels,
480 mm local top-up insulation strips, upper headers and channel-edge webs.
Nominal insulation depth above channels remains 512 mm; pickup heads/guides
extend 550 mm upward. New structural, mass and thermal assessment is required.
Pressure parts are unchanged. Selective tube, envelope and sampled cover-lift
checks do not qualify the full maintenance/operating sequence. Isolated reactor,
cover study and site snapshots are not automatically refreshed. D-037 remains
historical; its boxes and elevations are superseded by this decision.
See the [installation guide](../../fastSaltModels/docs/installation.md).

The accepted D-038 checkpoint is fastSaltModels `8ec6833`, with the saved installation under `baselines/wistr-service-bundles-2026-10-12/`. The owner retained spider penetrations after considering the less accessible vessel-side alternative. Stair access will be developed separately.

## D-039 — Add stair access to the reactor catwalk

Owner requested a stairway on 12 October 2026. The draft uses three switchback
flights in the clear bay at radius 14 m and installation angle 210°. An
approximately 8.2 m bridge with two bends avoids the hot-salt riser and joins
the catwalk at 195° through a 1.30 m rail
opening between module stations. Independent columns carry the stair; no support
is attached to the vessel. The 8.50 m rise uses 48 equal 177.1 mm risers, 280 mm
going, at least 1.20 m clear width and two 1.20 m deep intermediate landings.
These dimensions and framing are provisional layout choices. Actual stair solids and 52 walking/headroom volumes reserve 2.10 m clearance
and are screened against existing equipment and services with all collections
evaluated. Side trusses indicate the provisional bridge support arrangement. Complete egress, strength, foundations, handrail
detail and operational access remain unresolved. The earlier D-038 checkpoint
is preserved; the site composition is not automatically refreshed.
See the [installation guide](../../fastSaltModels/docs/installation.md#catwalk-stairway--12-october-2026).

## D-040 — Internal hot-air header and direct reactor-to-stack exhaust

On 12 October 2026 the owner requested replacing the exterior upper concrete
ring with an insulated duct inside the building, aligning the stack with the
reactor exhaust for a direct connection, and retaining a large manifold for the
steam generators because they have the highest maximum heat load. The proposed
smaller manifold is superseded by this final direction.

The working visual header has 2.50 × 2.702 m clear section (6.755 m²), preserving
the previous ring's passage area, at radius 18.75 m and Z=10 m. A provisional
3 mm shell, 100 mm external insulation and 1 mm cladding give 246 mm wall
clearance and 850 mm clearance below the crane runway. The three generator
roof exhausts and six fuel-tank exhausts feed it; it connects independently to
the stack through a 2.4 m duct. The stack moves to angle 135°, radius 27 m.
The reactor's 2 m hot-air duct runs straight at outlet elevation Z=−2.77 m to
the same stack, bypassing the header. The external lower concrete fresh-air
ring remains. Dimensions are provisional geometry, not calculated heat-removal
capacity; maximum duties, airflow, losses, buoyancy, insulation and supports
require assessment. Existing named baselines remain unchanged; site composition
is not automatically refreshed. See the
[installation guide](../../fastSaltModels/docs/installation.md#internal-hot-air-header-and-direct-reactor-exhaust--12-october-2026).

## D-041 — Larger centred generator exhausts and auxiliary supplies

Owner requests of 12 October 2026: centre and double all three generator hot-air
outlets; add a 50 mm line from reactor bottom through a pump near coolant storage
to its bottom; add an outdoor liquid-nitrogen supply; insulate coolant storage.
The owner confirmed 50 mm OD with heating/insulation, and a provisional nitrogen
tank, vaporizer and common header with consumer branches deferred.

The visual draft uses 1.8 m generator exhaust OD (2.002 m insulated), 2.2 m square
valve boxes with unchanged height, a 50 mm OD / provisional 3 mm wall transfer
tube with 50 mm radial insulation, and a small unsized motor-pump envelope.
The coolant tank is raised 0.9 m for bottom entry, with provisional 350 mm
side/top/bottom insulation and 1 mm jacket, borrowing the return-salt allowance.
An outdoor nitrogen vessel envelope of 2.5 m diameter × 6.5 m height is placed
at radius 28.5 m, 330°, with ambient vaporizer, regulator panel and 50 mm gas
header with three capped future takeoffs. Final tank capacity, equipment duties,
thermal performance, pressure boundaries, supports and cryogenic system design
remain open. These are visual layout choices, not selected equipment ratings.
See the [installation guide](../../fastSaltModels/docs/installation.md#generator-exhausts-coolant-transfer-and-nitrogen-supply--12-october-2026).

## D-042 — Catwalk-level laydown and mobile sector removal

**12 October 2026 — owner direction; dimensions provisional.** Remove the fixed
sector-storage facility. Bring a canister on a cart to receive a core sector,
then remove it through the equipment door. Add temporary storage surfaces for
one insulation cover and one sector cap at catwalk level.

The draft uses an independently supported 8.7 × 6.1 m platform at Z=−0.6 m,
above the maintenance fuel tanks, with separate receiving bays and a bridge at
15°. Existing stair access remains at 195°. Receiving supports, deck loading
and demountable framing for future tank access remain to detail. A 3.6 × 3.25 m
cart carries a provisional 2.95 m-ID × 6 m-clear canister. Overall 6.33 m height
leaves 0.17 m beneath the present door; reserve is tight and must be revisited
with shielding, cooling, load capacity and restraints. The envelope accommodates
the modeled core with attached tubes, not an established transport package.
Selected geometry checks and inspection-only cover/cap placement are documented
in the [installation guide](../../fastSaltModels/docs/installation.md#maintenance-laydown-and-mobile-sector-canister--12-october-2026).

The accepted D-039–D-042 checkpoint is fastSaltModels `06a13ef`. The saved scene,
selected review views, geometry report and hash manifest are preserved in
[the maintenance baseline](../../fastSaltModels/baselines/wistr-maintenance-2026-10-12/).
Earlier baselines and the site snapshot remain unchanged.

## D-043 — Attached off-gas and fuel/coolant salt-preparation buildings

**12 October 2026 — owner direction; envelopes provisional.** Add an off-gas
treatment building attached to the reactor building. Reactor gas is treated
before release. The owner selected a **separate release stack** for the draft.
Place fuel and coolant salt preparation adjacent to it and also attached to
the reactor building. Salt arrives in canisters, is purified/melted, and is
supplied to the reactor building as liquid through separate pipes.

The owner then requested halving each building's length and width (one-quarter
area), a shared pipe/tube duct, and **5 m height for both buildings**. The current
north-side envelopes are 10 × 11 × 5 m for off-gas at (−1, 31.5) m, and
15 × 12 × 5 m for salt preparation at (11.5, 32) m. They share a boundary at
X=4 m and one enclosed 4 m-wide, 1 m-high service duct across the fresh-air
ring. Its underside clears the ring by 0.3 m and its roof is 4.66 m above the
building floor. Gas, fuel and coolant retain separate lines inside it.
Canister receiving remains on the north side through a 6 × 4.2 m opening;
the existing reactor equipment door and transfer lane remain available.
The separate 0.8 m × 22 m release-stack envelope moves to (−7.5, 35.5) m.
Equipment placeholders shrink in plan to suit; heights and pipe diameters are
retained. These dimensions do not establish process duties or equipment capacity.

The model shows functional equipment reservations, a provisional reactor gas
collection terminal, and insulated liquid fuel/coolant lines ending at reserved
reactor-side tie-ins. It does not select purification chemistry or qualify gas
treatment performance. Detailed reactor-side collection/distribution, process
duties, supports, confinement and handling remain to design. The turbine hall
and its existing cycle/piping definition are retained. See the
[site guide](../../fastSaltModels/docs/site-study.md#attached-off-gas-and-salt-preparation-buildings--12-october-2026).

## D-044 — Horseshoe fuel handling and radioactive fuel return

**12 October 2026 — owner direction; floor-plan study authorized.** Fuel salt
is both supplied and removed for recycling. Arrange remote fuel-handling
equipment in a horseshoe around a central observation post, with shielded
viewing and manipulation areas outside. Use the EBR-II Fuel Cycle Facility
as an architectural reference. Develop a dimensioned plan before rebuilding
the site model.

The proposed study uses a 28 m outer span, 7 m-clear central room, 4.5 m radial
equipment band, 2.5 m outer gallery, and 1.5 m placeholder shielding bands.
An 8 m fuel-building height allows a 6.5 m clear cell plus 1.5 m overhead
reservation. The separate 12 × 12 × 5 m coolant annex and these dimensions are
**proposals, not approved engineering requirements**. Off-gas remains 10 × 11 ×
5 m with a separate stack. Fuel supply and radioactive return are distinct
interfaces within the shared service-entry concept. Return-line sizing and
process operations are not selected.

The existing D-043 Blender geometry remains current until this plan is
reviewed and integrated. The reference values, drawings, checks and limitations
are in the [fuel-handling study](../../fastSaltModels/docs/fuel-handling-study.md).

### D-044 clarification — conversion separate from liquid-salt refining

After reviewing Fast Salt System revision 5, the owner clarifies that incoming
spent-fuel conversion occupies a separate building. The horseshoe building
under discussion refines crude converter salt and recycles returned WISTR fuel.
It deals with interconnected liquid-processing equipment, so EBR-II's solid-fuel
station arrangement is not its sizing basis. Retain the horseshoe as an
observation/access preference; mark the 28 m span, 8 m height and seven bays as
reference-only. No replacement facility dimensions are established by the deck.
See the [source review](../design/conversion-refining-review.md).

## D-045 — Rectangular process-building reservations and fuel supply/return

12 October 2026. The owner accepts approximate site-layout envelopes: converter
20 × 15 × 8 m; fuel refining/recycling 15 × 12 × 5 m; existing off-gas building
10 × 11 × 5 m. These are revisable visual space reservations, not process sizing.
The horseshoe and leaded-glass observation layout are no longer requirements.
Camera-based observation is a working concept; no viewing/control system is designed.

The owner requests independent fuel-in and fuel-out pipes through the shared
refiner–reactor service duct. Gold indicates refined-fuel supply toward the
reactor; rose indicates used-fuel return toward the refiner. Both terminate at
reserved interfaces. The new return borrows the existing supply line's 150 mm
visible jacket envelope solely for illustration (50 mm tube plus 50 mm radial
insulation); no return-line engineering size or internal extraction circuit is selected.
Existing coolant and off-gas routes remain distinct inside the same duct.

The converter is an empty building envelope at (11.5, 55) m, beyond the refiner
and its receiving apron. No converter/refiner process connection or equipment
train is added. The existing coolant preparation placeholders remain in the
refiner building pending later allocation. The refiner and off-gas retain their
previous footprints. See the [site guide](../../fastSaltModels/docs/site-study.md).

## D-046 — Low insulated storage distribution

12 October 2026. At the owner's request, extend the shared-duct coolant supply to the bottom of the coolant storage tank and take the fuel supply/return to a valve box, then six separate pairs to the six fuel maintenance tanks. Keep all lines insulated and near ground level where possible. This supersedes the reactor-side reserved endpoints in D-045.

The visual draft places the box north of the vessel, with fuel branch centrelines 0.20 m above floor and a coolant floor route 0.40 m above floor. Short raised transitions clear the existing feedwater header; the shared duct stays above the exterior fresh-air ring. Coolant connects to an independent bottom nozzle beside the existing reactor-transfer connection. The fuel pairs connect at low inner tank ends; existing sector service bundles remain.

The 50 mm tube and 50 mm radial insulation (150 mm jacket envelope) are inherited visual allowances, not newly calculated sizes. The insulated 1.6 × 3.0 × 1.14 m valve box reserves space only. Valve internals, transfer sequences, process duty, pressure/shielding requirements and heat-trace design are unspecified. Selected pipe/equipment/support/stair clearance checks and terminal continuity are recorded by the model builder; full access and support qualification remain open.

Affected: composed site model, storage interfaces and [site guide](../../fastSaltModels/docs/site-study.md#low-insulated-salt-distribution--d-046). The isolated installation and named maintenance baseline are preserved.

## D-047 — Fuel pressure servers and nitrogen supply through off-gas building

12 October 2026. The owner requests one pressure server per maintenance-fuel-tank pair, styled like the absorber modules: a control box above a cylindrical tank. Each of the six maintenance tanks receives two 25 mm tubes from its associated server. Supply gas is paired with off-gas through the shared building duct and splits into three server branches.

The draft adopts 25 mm as bare tube OD. New gas tubing has a provisional 25 mm radial insulation allowance and is unheated; the existing 150 mm off-gas trunk envelope is retained. Three absorber-module-sized server envelopes and a separate supply-interface box in the off-gas building are shown. The previous reserved pickup above the reactor is replaced by the three-server collection network. Valve internals, pressure ratings, flow duty, pressure-control logic and operating sequences remain unspecified.

Move the nitrogen tank and its vaporizer together beside the off-gas building, at (−10, 30) m in the site frame. Retain the 50 mm gas-outlet allowance but route it into the off-gas building. Remove the old direct reactor feed, unused capped gas header and its wall sleeve from the composed site. The isolated installation and named baselines are preserved.

The model checks all twelve tank tubes, six common-header tee connections, selected route/equipment clearances and the skid's location. See the [model guide and previews](../../fastSaltModels/docs/site-study.md#fuel-pressure-servers-and-nitrogen-relocation--d-047). These remain visual interfaces rather than a qualified gas-control or radioactive-off-gas system.

## D-048 — Common insulation and heat tracing for each fuel pair

12 October 2026. The owner requests that fuel in/out lines remain together and be heated and insulated from fuel handling to the distributor, and from the distributor to every maintenance fuel tank.

The visual model now uses seven continuous common clad jackets, each containing two 50 mm OD tubes at 80 mm centre spacing with electrical tracing. The existing provisional 50 mm minimum insulation allowance plus 1 mm cladding gives a 236 mm overall envelope. Fuel floor centrelines are lowered 20 mm to 0.18 m for clearance at existing coolant crossings; coolant remains at 0.40 m. The refiner end is a paired reserved interface beside its supply station; internal process connections remain unspecified.

This supersedes the separate colored outer-envelope representation in D-045/D-046. The fourteen fuel members, seven jackets, duct fit and selected clashes are checked by the site builder. Heater duty, thermal sizing, pressure/support design and full access qualification remain open. Gas services from D-047 are unchanged. Affected: composed site geometry, [site guide](../../fastSaltModels/docs/site-study.md#common-heated-fuel-bundles--d-048), and fuel-storage interface records.

## D-049 — Move fresh-air distribution inside the reactor building

12 October 2026. The owner requests moving the outside cold-air duct inside the building. The composed site now uses a closed floor-level steel C-shaped duct with sealed ends around the existing 5.5 m equipment-door gap. Ten existing equipment branches shorten to inside connections; the outdoor intake remains and passes through the wall. The former exterior concrete ring and branch wall holes are removed.

The provisional clear section is 2.45 × 2.551 m (6.25 m² nominal, retained from the previous plenum), with 6 mm steel and a 60 mm support allowance. The duct top is 2.623 m above floor. Its normal outer radius is 20.30 m; the entire section shifts inward at existing wall columns. Local effective area, airflow/pressure loss, steel/support sizing and full access remain unresolved. Equipment and fuel/gas routes retain their positions; the coolant-storage supply drop shifts 0.5 m inward to clear a column recess. This is a visual layout revision, not airflow or structural qualification.

Affected: [site model and guide](../../fastSaltModels/docs/site-study.md#internal-fresh-air-duct--d-049), shared site interface records. The historical source installation remains a retained input, with the revision applied by the site builder.

## D-050 — Complete columns and revise generator fresh-air connections

12 October 2026. The owner requests columns on both sides, three outdoor air intakes near the generators, centered generator-side butterfly-valve boxes, and inlet area equal to 75% of exhaust area. D-050 completes all 18 column positions (20° spacing) while retaining the cutaway wall, and replaces the single south inlet with short inlets at 190°, 70° and 310°. The initial valve centers were 8.5 m above floor. In the subsequent owner-requested revision, lower all three to **1.35 m above floor**, retaining horizontal centering and the bore-area ratio. The boxes have approximately 0.37 m floor clearance; short level branches replace the tall inlet risers.

The area ratio uses clear bores: 1.794 m exhaust bore → 1.55365 m inlet bore (1.55965 m OD with provisional 3 mm wall). Outdoor intakes use the same diameter as a layout allowance. Air paths clear selected piping and stair envelopes; the coolant supply drop shifts to (3.8, 16.5) m. Both headers recess around columns. A local cold-header outer-wall pocket at 340° preserves coolant-tank clearance but reduces local passage below the 6.25 m² nominal section. Airflow, local losses, support/structural design and complete access remain unqualified. See [the current model guide](../../fastSaltModels/docs/site-study.md#generator-air-inlets-and-complete-column-layout--d-050).

## D-051 — Add illustrative turbine-hall machinery detail

12 October 2026. The owner requests more equipment detail in the steam power plant. Replace opaque reservation boxes with recognizable turbine and generator housings, pump/motor sets, condenser shells, reheaters, feedwater heaters and deaerator/storage drums. Retain the existing hall, equipment envelopes, cycle sizing and main pipe terminals. Add local casing connectors, shaft alignment at a provisional 15.2 m above floor, and guarded couplings in the five existing train gaps.

The owner accepted this visual checkpoint and requested commits; fastSaltModels `094d4a3` preserves [the named snapshot](../../fastSaltModels/baselines/turbine-equipment-2026-10-12/). Generic casing profiles, bolt patterns, saddles and coupling dimensions do not qualify supplier equipment or structural/pressure design. The model guide records containment and connection checks, preserved routing limitations and omitted upper structures/auxiliary circuits. Source and affected model: [turbine equipment detail](../../fastSaltModels/docs/turbine-equipment.md). The previously accepted site baseline remains preserved separately.

## D-052 — Python-authored assemblies with resolved TOML exchange

13 October 2026. The owner selects the same authoring pattern used in PMS: Python expresses repeated components, nested frames and geometric connections; a detached resolved document can be passed directly to Blender or exchanged as TOML. TOML is the literal exchange format for complex 3D assemblies, while the small P&ID remains directly authored in TOML. Markdown retains explanations and review decisions.

The first implementation migrates the three main coolant legs in `fastSaltModels`: 11 semantic components, 18 ports and nine pipe segments, including three generator and pump assemblies. It retains current graphics parameters, object names, pipe routes and geometry. The resolved document records source hashes when generated by the command-line authoring workflow. It is a separate static-graphics schema, not a PMS simulation input, and no PMS code or solver is changed.

Shared P&ID aliases now map SG-101/P-101 to graphics generator/pump 1 at 180°, SG-102/P-102 to pair 2 at 60°, and SG-103/P-103 to pair 3 at 300°. Reactor H/C aliases follow those legs; the resolved port metadata records their mapping to native reactor terminal names. The optional cross-check agrees for seven equipment tags and six main line specifications and flow paths. These aliases do not change physical nozzle locations.

Eight plain-Python checks and Blender direct-document/TOML comparisons pass. A comparison against the earlier builder preserves 117 mesh topology counts and all route controls within 0.00001 m. The complete installation build from exported TOML passes its existing equipment, route and selected clearance checks. These are software/geometry checks, not physical qualification.

Scope remains incremental: reactor internals, coolant storage/transfer, fuel/absorber, air and turbine systems retain their existing builders. No new thermal, hydraulic, structural, neutronics or safety conclusions follow from this refactor. See [assembly authoring and exchange](../../fastSaltModels/docs/assembly-models.md) for API, limitations and reproducible commands. Working outputs remain ignored; accepted baseline files are preserved. Responsible: project owner; implementation in `fastSaltModels`, shared interface record here.

## D-053 — Shared coolant engineering source for multiple views

13 October 2026. The owner accepts establishing a common component-and-connection model for graphics, P&ID, calculations and eventual simulation. The first implementation places the three main coolant legs in the hub's [shared engineering model](../design/engineering/README.md). Stable equipment/port/line IDs, adopted dimensions and case inputs now supply both existing views. This supersedes D-052's independently authored main-coolant dimensions and cross-check-only relationship; Python remains the graphics authoring layer and TOML remains the resolved exchange format.

Each quantity carries units, provenance and status. Normal-case data and the conditional wall-pressure screening case remain separate. Existing Hurmet worksheets retain equations/results; their hashes pin the explicitly adopted revision. A changed worksheet requires review before builds proceed. No solver integration or automatic worksheet editing is introduced. P&ID layout/instrumentation and Blender shapes/placements stay in their respective sources; non-migrated systems retain their definitions.

The P&ID import rejects local overrides of shared quantities. Graphics binds equipment identities to placement tags and rejects unsupported topologies. Six cross-view tests cover propagation from one shared edit, source order independence, overrides, units/ports, topology and source freshness. The existing P&ID outputs and resolved coolant geometry are preserved by this migration. No sizing or engineering qualification changes. Responsible: project owner; shared source in `fastSalt`, graphics consumer in `fastSaltModels`.

## Proposals not yet adopted

- Extending the D-052 resolved assembly definition to additional plant systems and qualified analysis adapters.
- Public GitHub organization and repository names.
- Code, documentation, and design-material licensing choices.
- Final student and university repository arrangements.

## Format for subsequent decisions

Use a stable ID, date, context, decision, responsible participants, source, affected models/interfaces, and consequences. Preserve superseded decisions and link to their replacements.
