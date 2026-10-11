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
