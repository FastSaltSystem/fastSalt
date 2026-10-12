# Component and analysis interfaces

Interface definitions are initial coordination records. No cross-solver exporter or coupled simulation is implemented here.

## IF-001: Reactor and steam generator

Participants: project owner, UM analysis team, and MSU steam-generator team. Named reviewers remain to be recorded.

Inputs to agree: system operating cases; heat duty and allocation among coolant legs; coolant and steam-side conditions; material-property sources and temperature ranges; allowed pressure losses; transient cases relevant to the component; connection sizes and coordinate convention.

Outputs expected from the component study: calculation basis, performance estimates and limits, equipment envelope, connection positions and directions, mass estimates where available, access requirements, and uncertainties.

The current three-leg visual arrangement is a starting interface assumption. It does not by itself establish a steam-generator design or equal-load operating conditions.

For the current 10 October single-floor draft, generator casings are rotated
90°: hot/cold salt manifolds face the reactor; water/steam manifolds face the
building wall. Generator bottoms now rest on the sub-floor at Z=−9.1 m.
Cold manifolds and level suction runs are at Z=−7.9 m; two bends lead to the
pump bottom inlet at Z=−6.7 m. Pump side outlets remain at Z=−5.8 m and return
salt to the reactor. This supersedes the earlier manifold/discharge alignment.
Pumps retain the [preliminary allowance](../calculations/steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md).
The 17 m casing, nozzle positions, internal distribution and pressure losses
still need agreement with the generator team.

## IF-002: Shared design and analysis models

Each model should identify the design revision, component names, geometry scope, units, materials, operating state, simplifications, software version, and its source repository or input-file location.

| Representation | Information to exchange |
| --- | --- |
| Neutronics models | Geometric/material-region definitions and documented simplifications; study outputs with their provenance |
| SAM/system analysis | Component topology, agreed parameters, boundary conditions, cases, and relevant result summaries |
| Local CFD | Modeled domain, boundary conditions, heat-source basis, property sources, mesh/case versions, and scope of any derived quantities |
| Mechanical models | Physical parts and assemblies, material assignments, operating state, and eventual mass-property results |
| Blender graphics | Component geometry, reference frames, display detail, and deliberate presentation changes |

First establish traceable inputs and outputs. Automated coupling is a separate development decision with an identified use case.

## IF-003: Components and installation layout

The graphics project currently uses metres and Z-up. A shared project coordinate system is to be agreed rather than assumed for university inputs.

Each placed component should supply an envelope, connection coordinates and directions, orientation, support interfaces, and access/removal envelopes. Every exported geometry must declare units and its origin.

The installation baseline should identify the exact revisions of the reactor, steam generator, and system assumptions used.

Current draft: 5 m vertical clearance from generator top covers to the underside
of the hoist body; the displayed hook is raised. Stack base bottoms share floor
elevation. See [D-007](../decisions/index.md#d-007--lower-generators-stacks-and-crane).

## IF-004: Equipment cooling air and installation headers

The 36 m installation draft connects ten air-cooled equipment envelopes to
separate hot and fresh headers: reactor, three generators and six fuel
maintenance tanks. Reactor endpoints come from the preserved hood-stub geometry.
Other equipment air ports represent provisional cooling spaces, not process
fluid connections. Generator/fuel cooling passages remain undefined.

Current visual route: hot ring at Z=10 m inside the wall to one rear stack;
fresh C-header at Z=−8 m outside the wall, with an exterior intake. Reactor
crossovers are removable and must be disconnected for hood/sector maintenance.
Confirm heat loads, air temperatures, pressure losses, flow sharing, operating
and maintenance states, supports and extraction clearances before adopting
these routing envelopes as engineered interfaces. No airflow calculation has
been added in this visual revision. See [D-008](../decisions/index.md#d-008--widen-installation-and-combine-cooling-air-headers).

IF-004 update: [D-009](../decisions/index.md#d-009--draft-exterior-concrete-air-plenums)
supersedes the round-duct header geometry above with exterior hollow concrete
rings. Fresh ring Z=−9.1 to −6.1 m; hot ring Z=11.705 to 14.705 m. The hot
reactor crossover remains at Z=10 m and rises into the ring outside the wall.
All ten equipment interfaces and the existing reactor hood flow remain. A floor
plenum would be a separate interface revision requiring new bottom connections
and reconsideration of the current outer cold hood's cooling function.

IF-003/IF-004 routing correction: the hot ring now spans Z=8.5–11.5 m. All twenty
equipment air routes stay inside the wall until a horizontal crossing directly
into the corresponding ring. Equipment exhaust risers use radius 16.5 m; the
2 m reactor supply riser uses radius 16.3 m. Wall entries are at Z=10 m (hot)
and Z=−7.6 m (fresh). The feedwater external connection rises at radius 16 m to
Z=−5.35 m and crosses above the lower ring; the low distribution header remains
unchanged. See [D-010](../decisions/index.md#d-010--keep-air-risers-inside-and-clear-the-cold-ring-with-feedwater).

IF-001/IF-004 generator detail update: the four process-side manifolds are now
half-pipe collectors directly against the casing, with short D-to-round end
transitions at the unchanged external pipe terminals. The former branch stubs
are removed. Hot-air outlets start vertically at the top of a provisional
roof butterfly-valve box, Z=8.63 m. IF-003 clearance now uses this equipment top:
hoist underside Z=13.63 m, giving 5 m. This is geometry only; valve internals and
collector hydraulic behavior are undefined. See [D-011](../decisions/index.md#d-011--generator-top-air-valves-and-half-pipe-collectors).

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

## 11 October insulated installation interface revision

[D-014](../decisions/index.md#d-014--apply-calculated-pipe-and-insulation-envelopes-to-the-installation)
supersedes the earlier uninsulated connection envelopes for the current graphics.
Salt bore/wall/insulation are 1.425 m / 25 mm / 400 mm hot or 350 mm return;
steam branch/header insulated OD is 1.355 / 1.815 m; feedwater is 0.875 / 1.240 m.
These are conditional worksheet cases, not approved material/pressure specifications.
Generator centres are now radius 14 m in a provisional 42 m shell. Cold salt
collector/suction centreline is Z=−7.2 m, pump suction Z=−5.49 m and discharge
Z=−4.59 m. Feedwater collector/header is Z=−5.6 m; hot salt and steam remain
Z=+6.4 m. Reactor terminals retain positions/orientation with installed sleeves
adapted to the salt bore/wall. The isolated baseline remains unchanged. Collectors,
supports and full lifting/extraction paths require separate design review.


## Reactor removable insulation-cover interface — 11 October 2026

The [six-sector cover concept](reactor-insulation-cover.md) is a distinct thermal
and handling subassembly above the pressure caps. Its straight sliding pickups
reuse the common head's 750 mm bar pitch and external hook profile. Cassette
seams align with spider-leg centrelines. The independent model has an 8.24 m
nominal footprint and 500 mm wool allowance; 40 mm hook take-up interrupts the
main frame contact at rest. Final vessel/spider supports, service penetrations,
thermal bridges and complete extraction routes are unresolved. The existing
reactor and installation hood/air interfaces remain in place until that system
revision is developed. See [D-015](../decisions/index.md#d-015--develop-a-separate-six-sector-insulation-cover-with-sliding-pickups).

The revised cassette transfers its resting load through four Ø50 × 75 mm
zirconia blocks in fixed shallow seats. No metal fastener spans the break.
An upper frame carries individually framed wool grids on tension hangers.
Lower seat attachments, post-side insulation and operational clearances remain
open; the separate cover does not yet replace the installed hood. See
[D-016](../decisions/index.md#d-016--zirconia-seating-with-an-upper-frame-and-tension-hangers).

A separate rigid-block comparison keeps the footprint, 500 mm insulation and
common lifting interface but raises the enclosure top by 240 mm. Its guide/hook
heights and support-post positions differ from the wool cassette. This envelope
has not been installed in the reactor/building model. Retain both candidates
until a selection is made. [Comparison](../../fastSaltModels/docs/rigid-insulation-cover.md).

Current cover revision: the recessed T-grid has no tray or floor-standing posts.
Its 2 mm assumed bonded facing rests directly on the sector cap reference; the
upper frame bears through shoes on top of the blocks. Ceramic breaks move to the
hanger attachments. Top enclosure elevation is 0.699 m above the block underside.
The old point-supported seated calculation is withdrawn for this revision.
Actual cap hardware and service reliefs remain to integrate.
[Current draft](../../fastSaltModels/docs/tgrid-insulation-cover.md).


Five-level update (D-019): footprint, upper frame, cap reference and hook interface
are retained. Five recessed grids now slide on common rods, with one provisional
crimp stop at each level. The five nominal 100 mm layers contact at rest, retaining the 500 mm envelope.
Five embedded grids and aligned main joints require thermal review; collar
setting and suspended-layer load sharing require mechanical review. Actual cap seating
and hardware reliefs remain unintegrated. See the current cover guide above.


### Upper layers on flat T-bar flanges — D-020

Retain all five grids. Only the bottom block layer has recessed grooves; upper
blocks sit directly on their T-bar flanges with webs between blocks. Retaining
five full 100 mm block layers and four 3 mm flanges makes a 512 mm stack. Frame,
ceramic attachments, shell and hooks rise 12 mm; exterior top is now 0.711 m.
At rest the flange strips transfer load into blocks below, so local strip-bearing
compression needs checking. Collar adjustment and cumulative rod loads still
apply. The previous all-grooved study is preserved; installed reactor geometry
is unchanged. [Current guide](../../fastSaltModels/docs/tgrid-insulation-cover.md).


## Reactor hood replaced by fitted insulation covers — D-021

Six cassettes now cover the pressure caps, with blind hook pockets, service wells,
removable thermal inserts and local hollow frame collars. Existing short service
terminals remain disconnected beneath the inserts; operating extensions remain
to route. Standalone cassette mass/grillage results do not qualify the fitted
cover. Separate side plenums connect to the existing well/baffle and vessel/baffle
annular passages. The hot connection has a sealed crossover through the cold
passage; neither air connection penetrates the reactor pressure vessel.

The installation uses the revised working reactor and side ducts. Absorber pairs
move outward while keeping vessel-top platform elevation. Historical baselines
are preserved. Airflow, well-opening structure, fitted cover strength and thermal
bridges remain unqualified. [Geometry and checks](../../fastSaltModels/docs/reactor-study.md#insulation-covers-and-side-air-connections--11-october-2026).


The 11 October floor-routing refinement keeps the reactor cold-air interface at
its side manifold but feeds it directly from the lower ring along the floor,
with one rise at the reactor. The provisional 2 m duct centreline is 1.5 m above
the slab (0.5 m beneath its envelope). It replaces the elevated crossover; the
hot-air interface is unchanged. See the installation guide for geometry checks.


## Hot-air insulation — provisional visual allowance

Following the owner's request to insulate all hot-air ducts, the working graphics
use 100 mm generic insulation and 1 mm cladding on the reactor collector and
crossover, ten hot branches, stack connector and barrel. The upper concrete ring
has an internal liner; its outer radius grows by 202 mm and height by 404 mm to
accommodate the liner and wrapped connection. Cold-air routing remains at floor
level. These values are visual coordination allowances, not calculated material
or insulation selections. Temperature cases, heat loss, surface temperature and
natural-draft performance remain to evaluate. See the
[model guide](../../fastSaltModels/docs/installation.md#hot-air-insulation-allowance--11-october-2026).


## Site building interfaces — provisional layout, 11 October 2026

The [site model](../../fastSaltModels/docs/site-study.md) retains the current reactor
installation and places the turbine building beside its 200° secondary outlets.
Straight coaxial extensions retain the report's steam jacket OD of 1.815 m and
feedwater jacket OD of 1.240 m. They terminate inside a provisional turbine pipe
bay; turbine inlet, feedwater plant, condenser and heat rejection are not connected
or sized. Source terminal coordinates and input hashes are in the generated site
report. Pipe supports shown are placement envelopes, not a stress/support design.

Fuel preparation is a separate envelope across the east/northeast service yard,
with its receiving opening facing the existing reactor access approach. Its
process, throughput, inventories and material-handling interfaces remain to agree.
No fuel process or transfer pipe is invented in this draft. The common pad datum
is illustrative; future civil grading must reconcile the reactor sub-floor with
site access. Both footprints and heights are provisional under D-023.


## Preliminary Rankine-cycle interface — 11 October 2026

The [first cycle case](../calculations/power-cycle/README.md) retains 24 MPa,
830 K steam and 560 K feedwater at the generator interface. Current water properties
give 711.67 kg/s total versus the older 711.56 kg/s worksheet value; no pipe
geometry changes have been made. The main-steam-reheat branch is inside the power
plant boundary, so its flow is part of the existing steam-header duty. No extra
salt connection is introduced. The 5 kPa condenser rejects about 793 MW in this
conditional case. Turbine wetness, pressure-loss budgets, station auxiliaries,
heat sink and equipment dimensions must be resolved before validating the
provisional turbine-building envelope. About 690 MW is gross generation, not net
export and not a replacement for the project's 600 MWe design target.


## Selected reheat interfaces — 11 October 2026

The selected cycle (D-026) preserves the steam-generator main-steam/feedwater
interfaces but changes the internal power-plant arrangement: HP exhaust at
2.8 MPa, hot reheat at 2.66 MPa and 510°C, and about 26.28% of main flow diverted
to the reheater heating side. Its 24 MPa heating return is 380°C before throttling
to HP heater 4. Reheater duty is about 252.5 MW. No new salt route is required.

The 20/30/35°C cooling cases give condenser duties about 804.5/826.5/837.6 MW.
These supersede the first-cycle thermal loads for subsequent equipment sizing;
the original results remain historical comparisons. Cooling control must support
the provisional 5 kPa pressure floor. Reheater/LP exhaust ducts, heater shells,
condenser geometry, cooling control and maintenance envelopes remain to size
before validating the turbine building. See [selected cycle](../calculations/power-cycle/README.md#selected-working-cycle--11-october-2026).


## IF-007: Power-cycle equipment and building layout

11 October 2026. [D-027 equipment sizing](../calculations/power-cycle/equipment-sizing-notes.md)
provides conditional equipment envelopes, pipe bores and storage elevations for
the next turbine-building arrangement. Keep bores distinct from metal/insulated
ODs, heat-transfer area distinct from footprint, and blade-tip diameter distinct
from casing size. No geometry has been changed from these results.

The proposed BFP pressure budget requires a generator steam outlet above the
previous 24 MPa interface to preserve 24 MPa at the turbine after piping loss.
Reclose the cycle and reconcile the MSU steam-generator pressure-drop allocation
before changing IF-001 or the displayed performance. A 14 m deaerator level also
requires more condensate-pump pressure than the former 0.72 MPa discharge.

## Turbine-hall internal routing — 11 October 2026

The [first routing draft](../../fastSaltModels/docs/turbine-piping.md) keeps the
existing steam/feedwater terminal coordinates and conditional jacket dimensions.
Internal nozzles, collector sizes, walls and insulation are geometric allowances.
The below-floor condensate collector requires civil/NPSH review. Existing east
feedwater piping leaves 4.70 m underside clearance against a 5 m aisle reservation;
this is an open interface constraint. IP–LP routes of 71.6/56.3/41.3 m require
revisiting the earlier 40 m pressure-loss screen, and overhead turbine-maintenance
paths need review. This routing does not update the thermodynamic calculation.

HP/IP graphics correction: the combined train reservation is now divided into
labeled HP and IP sections. Main admission and cold-reheat outlets connect to HP;
hot-reheat returns and LP crossover outlets connect to IP. This fixes ambiguous
stage-port placement in the first piping graphic without changing the cycle basis.

D-032 supersedes the retained diagonal site-terminal coordinates above. The reactor
outlet positions/tangents stay fixed; external bends turn both lines onto the same
wall-normal approach. Turbine centre is (−66, 0) m; both internal-interface world
positions are X=−39 m, Y=−4.19484 m, at the existing elevations (steam Z=6.4 m,
feedwater Z=−3.78 m). Position and tangent matching is asserted during site build.
The wall bay is shifted within the turbine east wall to suit the aligned approach.

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

D-036 doubles absorber tank envelope volumes to 0.643398 m³ each (0.806349 m
diameter × 1.259921 m cylinder height). Tank bottom connections, module positions
and catwalk footprints stay fixed; control boxes rise 0.259921 m. Account for the
increased eventual tank/salt loads when sizing module supports; usable capacity
is not established by this geometric revision.

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
