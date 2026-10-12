# Design basis and current assumptions

Initial register: 10 October 2026. This is a sourced starting point, not a harmonized or approved engineering specification.

## Status vocabulary

- **Reported study:** a source documents an analysis for a particular configuration.
- **Design target:** an intended system characteristic.
- **Current visual definition:** a value used in the graphics baseline; acceptance for visualization does not qualify it for analysis or manufacture.
- **Provisional:** a working assumption requiring review.
- **To agree:** an input that has not yet been established for the shared interface.

## Initial register

| Item | Value | Status and source |
| --- | --- | --- |
| Core diameter | 3.8 m | Current visual definition; owner corrected the earlier 3.6 m value to match slide 6 of Fast Salt System revision 5 |
| Active core height | 3.4 m | Current visual definition; excludes reflectors and plenums |
| Core sectors | 6 | Current visual definition |
| Thermal output | 1500 MWt | System design target in Fast Salt System revision 5; identify the exact analyzed configuration before applying to a study |
| Electrical output | 600 MWe | System design target in that presentation; not a demonstrated net plant output |
| Coolant legs | 3 | Owner-confirmed arrangement; one hot and one cold vessel connection per leg |
| Coolant pipe bare outside diameter | 1.475 m installation; 1.4 m preserved isolated baseline | Installation updated 11 October to conditional 1.425 m bore / 25 mm wall; not approved for manufacture |
| Maximum average coolant-pipe velocity | 3 m/s | Owner criterion; provisional 1.425 m bore gives 2.8965 m/s at the inherited flow |
| Peripheral reflector radial thickness | 0.30 m | Current visual definition |
| Bottom / top reflector thickness | 0.30 / 0.25 m | Current visual definition |
| Downcomer radial width | 1.00 m | Current visual definition |
| Bottom / hot plenum height | 0.75 / 1.60 m | Current visual definition; hot plenum enlarged to accommodate pipe connections |

## Sources

- [Current visual parameters](../../fastSaltModels/models/wistr_reactor.py), pinned initially to fastSaltModels commit `0d981f2`.
- [Graphics baseline documentation](../../fastSaltModels/README.md).
- [Fast Salt System revision 5](</Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Fast Salt/Fast Salt System 5.pptx>), cover dated June 26, 2026.
- [UM research overview, work W10](../publications/index.md#w10).
- Project-owner instructions in the originating project conversation, transcribed into this register; confirm this record during engineering review.

## Reconciliation still needed

- Match each analysis to its geometry, material, and operating-state revision. The November 2025 report covers several historical designs.
- Establish the operating conditions, properties, and calculation reference used for coolant flow and steam-generator sizing.
- Agree drained, filled, and maintenance states before calculating masses and lifting balance.
- Assign stable parameter identifiers and a machine-readable schema only when the first shared calculation or model adapter is implemented.

When a value changes, record its source, date, reason, and affected interfaces. Do not silently replace historical study inputs with current visual dimensions.

## Installation update — 10 October 2026

Owner-requested current visual definitions: 17 m steam-generator casings, reactor
well seated on the sub-floor, inward-facing salt manifolds and outward-facing
water/steam manifolds following a 90° generator rotation, three cold-leg pumps and
six external absorber-module envelopes. The initial revision raised building
height to 41.2 m; the later floor-mounted-generator revision below supersedes
that height. These are installation parameters,
not replacements for historical research inputs.

The [pump worksheet](../calculations/steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md)
uses 4.619533 m³/s per leg and the source generator pressure drop plus 50%.
Provisional assumptions of 80% pump and 96% motor efficiency lead to 1.653 MW
shaft demand per leg and a 2 MW motor envelope. Physical equipment dimensions,
secondary header diameters, loop pressure-loss allocation and motor speed remain
provisional. The 17 m casing does not revise the calculated 19.879 m tube length.

The subsequent single-floor draft removes the intermediate deck. All storage
tanks now rest on the sub-floor; generator casings rest on 2.1 m steel frames and
pump casings on 2.4 m open steel frames. Pump discharge and lower salt manifolds
are both at Z=−5.8 m; bottom suction enters upward at Z=−6.7 m. Absorber support
platforms are at vessel-top Z=−2.02 m. Z=0 is retained as the old deck datum.
Frame sizing and routes remain provisional; see [D-006](../decisions/index.md#d-006--use-a-single-floor-equipment-layout).

The latest owner revision places generator casings directly on the floor,
removing their 2.1 m frames. Cold manifolds and level suction runs are at
Z=−7.9 m, with two bends into each raised pump. The crane and roof are lowered
so the hoist body underside is exactly 5 m above generator top covers. The new
building envelope is 31.905 m, including the lower level; stack bases also meet
floor elevation. Pump flow direction remains generator → bottom inlet → side
discharge → reactor. See [D-007](../decisions/index.md#d-007--lower-generators-stacks-and-crane).

The subsequent air-routing draft widens the building to **36 m**, explicitly
approved by the owner. Generators move to radius 12 m, fuel tank pairs to 10.8 m,
and secondary headers to 15 m. One provisional 3.6 m exhaust stack replaces the
three 2 m stacks. A high hot-air ring and low exterior fresh-air C-header connect
the reactor, three generators and six maintenance fuel tanks. Duct/stack sizes
are visual space allowances; flow, natural draft and heat-removal performance
are not calculated. See [D-008](../decisions/index.md#d-008--widen-installation-and-combine-cooling-air-headers).

The exterior-plenum revision replaces the round air headers with full hollow
concrete bands attached to the building shell. Both have provisional 3 × 3 m
gross sections and 0.25 m skins; the lower ring starts at floor level and the
upper ring ends at the roof springline. Stack radius increases to 24 m to clear
the rings. Structural strengthening is a design possibility, not an established
result. A floor supply plenum is proposed for comparison but not implemented;
reactor airflow is unchanged. See [D-009](../decisions/index.md#d-009--draft-exterior-concrete-air-plenums).

The latest routing correction lowers the hot ring to Z=8.5–11.5 m, below the
crane runway underside (Z=11.705 m). All equipment air risers remain inside the
building and penetrate the wall only at their ring connections. Feedwater rises
inside to cross at Z=−5.35 m, giving 0.5 m between pipe underside and the cold
ring roof. See [D-010](../decisions/index.md#d-010--keep-air-risers-inside-and-clear-the-cold-ring-with-feedwater).

Generator detail update: four half-pipe collectors per casing replace the
stand-off manifold pipes and branch stubs. Short end transitions preserve the
existing piping terminals. Each generator has a roof-mounted 1.2 × 1.2 × 0.6 m
butterfly-valve placeholder, with hot air exiting upward. The crane and roof
rise 0.6 m to retain 5 m from valve top to hoist body; building envelope is now
32.505 m. All new equipment dimensions are visual assumptions. See
[D-011](../decisions/index.md#d-011--generator-top-air-valves-and-half-pipe-collectors).

Generator inlet/collector revision: fresh air enters a perpendicular casing
face, 90° from the salt and secondary faces and opposite the pump. Collector
diameters are now 2.1 m salt, 1.2 m steam and 0.75 m water (50% enlargement).
Pipe diameters and connection positions are retained, with smoothly blended
transitions matching pipe axes. These are visual envelopes, not hydraulic
sizing results. See [D-012](../decisions/index.md#d-012--enlarge-generator-collectors-and-separate-fresh-air-inlets).

Equipment access/support update: three absorber pairs share 1.8 × 4.2 m braced
platforms at vessel-top elevation. An open 4.5 m-wide, 6.5 m-high doorway at
18° provides straight access beside sector storage, through a 5.5 m minimum
gap in the fresh-air ring. Its ends are sealed, retaining a connected C-shaped
supply passage. The apron is level with the sub-floor; the existing coolant
tank clears this lane. Dimensions remain provisional visual choices. See
[D-013](../decisions/index.md#d-013--shared-absorber-supports-and-equipment-access-beside-sector-storage).

11 October piping estimate: the [Hurmet secondary-piping worksheet](../calculations/steam-generator/Steam%20and%20feedwater%20pipe%20sizing%20-%20Hurmet.md)
provides conditional bore / nominal wall / bare OD envelopes (mm): steam branch
425 / 115 / 655; steam header 725 / 195 / 1115; feedwater branch 375 / 75 / 525;
feedwater header 650 / 120 / 890. Inputs include 30 MPa gauge design pressure,
unselected-material stress assumptions of 80 MPa steam and 120 MPa water,
and provisional flow/loss criteria. These are calculation cases, not adopted
piping specifications. Existing Blender diameters are unchanged. See the
[verification record](../calculations/steam-generator/steam-water-pipe-check.md).

11 October insulation estimate: the [Hurmet thermal worksheet](../calculations/steam-generator/Steam%20and%20feedwater%20insulation%20-%20Hurmet.md)
provides conditional radial layout allowances of 350 mm steam and 175 mm feedwater,
using dry calcium silicate, 40°C room/radiant surroundings, convection 4 W/(m² K),
jacket emissivity 0.20 and a 60°C surface target at provisional 600°C / 325°C check
temperatures. Insulated branch/header diameters are 1.355 / 1.815 m steam and
0.875 / 1.240 m feedwater, before jacket/installation clearance. These are
preliminary thermal estimates, not adopted specifications; hotter surroundings
or weaker surface cooling can exceed the target. No graphics change. See the
[checks and sensitivity cases](../calculations/steam-generator/steam-water-insulation-check.md).

11 October coolant-insulation estimate: the [Hurmet worksheet](../calculations/steam-generator/Molten-salt%20coolant%20insulation%20-%20Hurmet.md)
provides conditional radial allowances of 400 mm hot coolant (875 K) and 350 mm
return coolant (810 K), optionally 400 mm on both. At a provisional 1.5 m bare OD,
insulated diameters are 2.3 / 2.2 m, before jacketing/tracing/installation clearance.
The 1.5 m OD is not a selected pressure wall; reconcile with the 1.400211 m bore
requirement. Assumptions match the secondary-pipe thermal estimate: 40°C room
and radiant surroundings, convection 4 W/(m² K), emissivity 0.20 and 60°C target,
with calcium-silicate effective conductivity 0.090 W/(m K). These remain estimates,
not adopted specifications or freeze-protection provisions. No graphics change.
[Checks and limitations](../calculations/steam-generator/molten-salt-insulation-check.md).

11 October coolant pipe-wall worksheet: the [Hurmet pressure estimate](../calculations/steam-generator/Molten-salt%20coolant%20pipe%20wall%20-%20Hurmet.md)
records a conditional 25 mm nominal wall on a 1.425 m bore, giving 1.475 m bare OD
and 2.8965 m/s at the inherited flow. Screening assumptions are 1 MPa gauge,
50 MPa effective stress including weld factors, y = 0.40, 3 mm allowance and
12.5% negative wall tolerance. None establishes a selected alloy or final pressure
rating. Cover-gas/static/pump-shutoff/tube-failure conditions and structural checks
remain unresolved. Insulated ODs are 2.275 / 2.175 m for 400 / 350 mm insulation;
the existing 1.5 m bare OD thermal/layout allowance is retained. No graphics change.
[Verification](../calculations/steam-generator/molten-salt-wall-check.md).

11 October installation update: [D-014](../decisions/index.md#d-014--apply-calculated-pipe-and-insulation-envelopes-to-the-installation)
applies the conditional worksheet dimensions to the graphics. The shell expands
to 42 m (48 m across exterior rings); equipment/headers spread outward and low
connections move to accommodate insulation. Both salt nozzle sleeves in each
of three pairs are adapted only in the installation copy. All 19 process routes
have separate metal/insulation meshes. The current draft preserves 5 m hoist-body
clearance and passes selective envelope/connection/access checks; this does not
approve pressure design, structural loads or complete maintenance reach.


## Cooling-water environmental basis — 11 October 2026

Owner-accepted provisional condenser-water inlet temperatures: **20°C normal
reference, 30°C hot design case, 35°C extreme check** (D-025). These are not air
temperatures or weather percentiles. No cooling tower, water source or site has
been selected. The initial 5 kPa condenser condition remains the 20°C reference;
it is not imposed at all inlet temperatures. Permissible hot-day pressure/output
and minimum operating pressure remain to determine. See the
[cooling-case results](../calculations/power-cycle/README.md#accepted-cooling-water-cases--11-october-2026).


## Selected preliminary power cycle — 11 October 2026

D-026 selects 2.8 MPa HP exhaust, 2.66 MPa/510°C hot reheat and 380°C high-pressure
heating return, with 1.6/1.0 MPa feed-pump-turbine heater extractions. Main-steam
conditions and 1,500 MW heat input remain inherited targets. A 5 kPa minimum
condenser pressure is a provisional modeling/control requirement at these reheat
conditions, not a qualified turbine limit. The selected cycle meets the 10% LP
moisture screen for the accepted cooling-water cases; it does not establish
blade-erosion acceptability or a net plant output. See the
[selected cycle basis](../calculations/power-cycle/README.md#selected-working-cycle--11-october-2026).


## Preliminary power-plant equipment allowances — 11 October 2026

[D-027](../decisions/index.md#d-027--develop-preliminary-power-plant-equipment-sizes)
adds [equipment-sizing requirements and candidates](../calculations/power-cycle/equipment-sizing-notes.md):
~38,500 m² condenser surface in three modules, ~8,200 m² conditional reheater
surface in four modules, six candidate LP exhaust flows, seven heater thermal
areas, generator capacities, pump allowances and ten-minute deaerator storage.
The 45 × 24 × 20 m turbine building has not been verified against these items.
Proposed 26.5/1.0 MPa feedwater/condensate discharge pressures and 14 m deaerator
minimum level are sizing allowances requiring coupled-cycle and pump verification;
they do not supersede the D-026 numerical performance case yet.


## Motor-BFP equipment and turbine-hall revision — D-029

The owner authorized resizing for motor-driven BFPs. Use the
[current worksheet](../calculations/power-cycle/Motor-BFP%20equipment%20sizing%20-%20Hurmet.md)
and [equipment JSON](../calculations/power-cycle/motor-equipment-sizing.json).
This supersedes the D-027 equipment allowances for working layout purposes,
while retaining that calculation as a historical reference. The BFP comparison
remains the property/heat-balance source; the revised main/IP heater ports and
higher pump duties are represented there. The pump pressure allowance is still
an aggregate rather than a solved distributed steam/water network.

Reheater area is 9,122 m² in four 16 × 3.25 × 3.25 m reservations; generator
allowances 550 and 350 MVA. Keep three 50% BFPs with 15 MW motor allowances and
reserve one 20 MVA BFP-only supply transformer per train. Main reactor/SG duties
and main header bores are unchanged. Revised internal bores and their checks
are in the worksheet; new pressure-wall and insulation designs are not implied.

A first dimensional arrangement reserves a 66 × 40 × 28 m main hall plus a
20 × 10 × 7 m electrical annex, replacing the unverified 45 × 24 × 20 m box.
Its east wall remains at X=−36 m, preserving the reactor pipe interface; the
building expands westward and transversely. Withdrawal aprons and removable
wall panels are needed. The plan is one candidate, not a minimum: main pipe
routes, columns, decks, full egress, crane/rotor handling and remaining auxiliary
plant are unresolved. Fuel-preparation envelope is unchanged.

D-030 revises the arrangement within that same hall: reheaters grouped at the
east steam entry, LP casings/condensers west, BFPs between the LP and HP heater
banks, and the reversed HP/IP train placing its generator beside the LP
unit's generator. DA storage and the south electrical annex move to the central
pump/generator zone. Equipment sizes and cycle results remain those of D-029;
this geometric arrangement does not establish piping or electrical losses.

D-031 shortens the current working hall to **60 × 40 × 28 m**, centre (−66, −10) m,
with the east wall still X=−36 m. The three BFP trains rotate to 4 × 10 m plan
reservations and sit side by side, with 2 m gaps, 2 m front access and the existing
3 m cross aisle. HP heaters and reheaters move inward. The 20 × 10 × 7 m annex
and equipment sizes/capacities stay unchanged. The 240 m² floor-area reduction
is geometric; complete piping, civil and maintenance fit remains unverified.

D-032 aligns the reactor and turbine-hall centres at world Y=0, moving the turbine
hall centre to (−66, 0) m. Reactor geometry and hall dimensions stay unchanged.
Both secondary pipes bend near X=−28 m onto Y=−4.19484 m and enter the hall's
east wall at X=−36 m at right angles. Internal terminals at X=−39 m and local
Y=15.80516 m have matching straight tangents. This supersedes the former diagonal
site approach; pipe pressure, insulation and flexibility assumptions are unchanged.

D-033 refines the D-032 external approach with two 45° offset bends per pipe.
Parallel westward end runs require a separate 20° alignment turn at the original
reactor-side outlet, just outside the reactor. Only the site copy of each building
connection is extended; upstream routes and the existing reactor wall penetration
are retained. Building positions, turbine interfaces, elevations and pipe dimensions
are unchanged. Bend intersections are approximately (−27.2, −8.89252) and
(−31.89768, −4.19484) m; these are control intersections, rounded by the model.

## Reactor catwalk and absorber services — D-034

The 12 October 2026 installation draft uses a shared expanded-metal annular deck,
radii 4.95–7.15 m, at Z=−1.20 m (7.90 m above the equipment floor). Six modules at
radius 6.60 m align with absorbers 1–6 at 45° + 60° increments. Four external tubes
per absorber retain two 25 mm and two 50 mm ODs, provisionally 2 mm walls, and
connect the actual spider stubs to the module base. The route rises through bored
removable insulation inserts, turns down inside the catwalk and continues beneath
the deck. Visible coupling allowances identify removable spider-side jumpers;
detailed remote disconnects and thermal treatment are unresolved. This revises
the former three paired platforms. Structural load rating, access stairs and
complete lifting clearances remain to establish. Site snapshots still reference
the previous installation until explicitly refreshed.

## Sector-to-maintenance-tank services — D-035

The 12 October 2026 layout connects each sector's three 25/50 mm service pairs
to one dedicated fuel-maintenance tank. Provisional assignment: sectors 1–6 to
tanks 6, 1, 2, 3, 4, 5 respectively. All 36 lines start at the existing plug stubs;
tank roof nozzles are new layout allowances. Bored removable thermal inserts and
cap-side disconnect allowances retain the intended maintenance sequence. Routes
sweep under the catwalk before turning down to tank roof connections. Tube sizes
are inherited from the core model, including provisional 2 mm walls; fuel-transfer
operation, thermal treatment, valves, supports and tank internals are not resolved
by these graphics. The earlier site scene remains unchanged until refreshed.

## Absorber tank volume revision — D-036

All six absorber-module cylindrical tanks increase uniformly by 2^(1/3), retaining
their height/diameter ratio of 1.5625. Current envelope dimensions: diameter
0.806349 m, height 1.259921 m; nominal volume 0.643398 m³ each, twice the previous
0.321699 m³. Bottom connections and module positions remain fixed. Control boxes
retain their dimensions and rise 0.259921 m. Catwalk/seat footprints are unchanged;
usable capacity and revised loads require their own engineering basis.

## Paired absorber reservoirs and gravity-drain routing — D-037

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
