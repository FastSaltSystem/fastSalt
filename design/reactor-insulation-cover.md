# Removable reactor insulation-cover assembly

Date: 11 October 2026. Owner direction: Thomas Wielenga. Status: independent
mechanical concept for review. [Model and review views](../../fastSaltModels/docs/insulation-cover.md).

## Scope and place in the project

A six-sector thermal cover is a separate subassembly of WISTR's thermal enclosure
and remote-handling equipment. It is developed in the existing fastSaltModels
repository. The vessel, spider and removable pressure caps remain separate
pressure-boundary components. No new repository is needed.

Each cassette spans between adjacent spider-leg centrelines, covering half of
each adjacent leg. Remove one cassette to reach that sector's pressure cap and
connections. Use stainless exterior skins and layered high-temperature stone
wool, with intermediate wire supports. Initial insulation depth: 500 mm; this is
a draft allowance rather than a qualified cassette thermal result.

## Adopted mechanism direction

Use four captive straight sliding lifting hooks per cassette. The user's
pivoting-catch alternative was superseded because it adds coordination between
vertical motion and catch rotation. Each sliding stem has a broad shoulder below
the internal carrying frame. At rest the shoulder is separated from the frame;
during lifting the stem rises, the shoulder contacts the frame and carries the
cassette. A cooler outer guide/collar supports each unloaded stem. The draft
uses 40 mm take-up, square stems to preserve alignment, visible travel bands,
and the existing common two-bar head's hook profile and bar spacing.

Resting gaps reduce a principal metal heat path; they do not eliminate heat
through supports, gas, radiation or surrounding metal. External indication shows
position, not load or successful sharing among all four points.

## Interfaces to resolve before reactor integration

- Seating: connect the internal carrying frame to suitable vessel/spider support
  points without loading pressure-cap fasteners or obstructing their tools.
  Zirconia blocks and shallow seats are shown; the gray pedestals below them
  remain attachment reservations, not completed vessel supports.
- Services: fit removable/split insulation around the actual sector and absorber
  tube connections; define disconnection order and ensure one cassette can be
  removed independently. The present study has no service penetrations.
- Handling: establish the complete cassette centre of mass, lifted weight,
  unequal pickup loads, guide clearances at temperature and recovery from a
  stuck stem. Retain the common tool only after these checks.
- Thermal enclosure: close the perimeter and joint gaps without short metal
  heat paths. Calculate bridges, sleeves, radiation and surface temperatures.
- Cooling air: the existing hot/cold hood circuit still appears in the reactor
  and installation models. Its replacement and vessel/well cooling connections
  need a separate system-interface revision. This cover is not decay-heat cooling.

The [previous flat-wall Hurmet estimate](../calculations/reactor/Reactor%20top%20insulation%20-%20Hurmet.md)
provides environmental assumptions and a calcium-silicate reference case. The
stone-wool comparison suggested comparable depth at less mass. Using 128 kg/m³
and the gross 53.37 m² footprint gives about 3.42 tonnes of wool, or 569 kg per
sector, excluding all steel and hardware. Final cassette mass is not yet known.


## Preliminary modeled balance

The [support/CM review](../../fastSaltModels/docs/insulation-cover.md)
now estimates 1.46 t per cassette, with the CM at radius
2.617 m. The four-hook footprint surrounds it; the common
head axis remains approximately 7 mm outward
of this CM. Additive geometry, provisional densities and unfinished joints limit
accuracy. This supersedes the earlier 1.24 t estimate; it is not a lift rating.
The tool and fixed ceramic seating assembly are excluded.

## Adopted zirconia support concept

Four Ø50 × 75 mm zirconia compression blocks per cassette remain in shallow
fixed lower cups when the cassette lifts away. Steel posts support an upper
carrying frame. Separate tension hangers carry individual wool-grid trays and
the bottom liner; diagonal wires stabilize them laterally. There is no continuous
metal fastener or sleeve through a ceramic block. The 40 mm sliding-hook thermal
gap is retained. Sizes are provisional and lower-seat attachment is unresolved.

[Hurmet screening](../calculations/reactor/Zirconia%20cover%20supports%20-%20Hurmet.md)
records average stress and ceramic-only axial heat conduction. The zirconia
grade, hot strength/conductivity, contact finish, differential expansion, thermal
cycling and environmental suitability still require qualification. Side heating,
post insulation and remaining shell ties must be included in the full heat balance.
See [D-016](../decisions/index.md#d-016--zirconia-seating-with-an-upper-frame-and-tension-hangers).

## Rigid-block alternative — preliminary comparison

The owner requested a separate calcium-silicate cassette study after questioning
the wool frame's apex stiffness. [Model, weight and screening](../../fastSaltModels/docs/rigid-insulation-cover.md)
show stacked rigid layers, one suspended bottom tray and a deep upper frame.
The wool candidate remains available. Neither candidate is yet selected for
reactor integration. The rigid alternative is heavier and 240 mm taller; its
simplified frame deflection estimate is explicitly provisional. See the
[Hurmet worksheet](../calculations/reactor/Rigid%20cover%20cassette%20-%20Hurmet.md).

## Recessed T-grid, direct seating and bonded facing — initial revision

The owner authorized proceeding on the assumption that the protective coating
works. The [new model](../../fastSaltModels/docs/tgrid-insulation-cover.md) removes
posts and the bottom tray. Recessed T-sections support grooved bottom blocks;
ceramic washers and sleeves isolate each upper hanger attachment. The coated
underside rests on a flat sector-cap reference, and broad upper-frame shoes bear
on the insulation. The existing four sliding hooks remain.

Assumed coating adhesion is distinct from qualified performance. No coating or
block composite stiffness is credited. The cap's actual plugs, hooks and other
fittings still need clearance pockets and seating integration. This supersedes
the tray/post arrangement within the rigid-block candidate; the old wool model
remains historical. [D-018](../decisions/index.md#d-018--develop-the-recessed-t-grid-cover-with-assumed-bonded-facing).

## Current revision: one suspended grid for each layer

D-019 implements the owner's bottom-up assembly proposal. Each of five nominal
100 mm layers has a recessed grid supported by individual crimp stops on 37
shared rods. Rod and upper ceramic loads accumulate from all five grids; lower
grooves are no longer assigned the full stack load during lifting. Crimp capacity,
groove strength and actual load sharing remain unqualified. Blocks contact at rest; collar setting, rod stretch and thermal expansion
require checking actual lifting load distribution. The model now opens with actual block layers visible.
[Updated model and estimates](../../fastSaltModels/docs/tgrid-insulation-cover.md).


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
