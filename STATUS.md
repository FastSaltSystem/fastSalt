# Project status and next work

Updated 12 October 2026. This is the working handover for the **Fast Salt System** project. Update it when a workstream changes status; keep technical values in the [design basis](design/design-basis.md) and cross-component decisions in the [decision record](decisions/index.md).

## Current materials

| Area | Current state | Start here |
| --- | --- | --- |
| Project organization | Two local Git repositories: `fastSalt` for the project hub, `fastSaltModels` for graphics; no public remote configured | [Repository map](README.md#repository-organization) |
| Detailed reactor graphics | Checkpoint `a99002f` preserves six fitted insulation cassettes and side supply/return plenums; pressure caps retained; earlier 0d981f2 baseline preserved | [Reactor integration](../fastSaltModels/docs/reactor-study.md#insulation-covers-and-side-air-connections--11-october-2026) |
| Installation graphics | Checkpoint `8ec6833` includes provisional 100 mm hot-air insulation and 1 mm cladding; 42 m insulated-pipe layout: separate metal and insulation meshes use conditional Hurmet sizes; generators/storage spread outward; raised cold-salt suction and feedwater routing; reactor side ducts connected to exterior rings, with fresh air routed directly along the floor; D-034 replaces paired absorber stands with a shared expanded-metal catwalk, six distributed modules and 24 dedicated service tubes; D-036 doubles module tank volumes; D-037 adds 12 separate heated reservoirs and doubles the modules to 12; D-038 lowers the catwalk 1.10 m from that draft, replaces service boxes with insulated bundles below liftable channelled covers, preserves falling salt drains and adds local insulation strips; D-035 adds 36 separate sector-to-maintenance-tank lines through core-service inserts and beneath the catwalk; doorway and 5 m hoist clearance retained; selective interference checks | [Installation guide](../fastSaltModels/docs/installation.md#insulated-process-piping--11-october-2026) |
| Site layout | Motor-BFP working draft: D-031 rotates BFPs side by side, reducing the turbine hall to 60 × 40 × 28 m (240 m² less main-hall floor area), 20 × 10 × 7 m BFP electrical annex, external withdrawal aprons and 30 equipment boxes (HP/IP now shown separately); D-030 groups reheaters at steam entry, shifts LP/condenser train left, puts BFPs between heater banks and aligns generators alongside each other; condensate pumps now along the west wall before the shifted LP heater bank; selected box/service checks pass. Fuel preparation stays 30 × 24 × 14 m. D-032 aligns building centres and perpendicular turbine-wall entry; D-033 replaces the offset with two 45° bends per pipe plus a separate 20° reactor outlet alignment turn. 59 main pipe sections now routed with explicit HP → reheaters → IP → LP connections; east feedwater bay has 4.70 m clearance versus 5 m reservation; long crossovers and crane/rotor access need review. Extraction/drain circuits, structure and auxiliaries remain open | [Site guide](../fastSaltModels/docs/site-study.md) |
| Steam-generator estimate | Calca converted to Hurmet; pump allowance worksheet supports three provisional 2 MW motors; steam/feedwater bore and wall worksheet added with explicit provisional pressure/stress inputs; insulation worksheets add conditional 350 mm steam / 175 mm feedwater and 400 mm hot-salt / 350 mm return-salt radial allowances | [Calculation conventions and worksheet](calculations/README.md) |
| Rankine-cycle plant | Motor-BFP equipment basis D-029: 697.1 MW gross / 671.6 MW after BFP + condensate loads at 5 kPa, other loads excluded; 282 MW reheater, 550/350 MVA generator allowances, revised pipe bores and three 15 MW BFP motor trains. Original steam-drive calculation retained; preliminary equipment and dimensional checks complete | [Current equipment](calculations/power-cycle/Motor-BFP%20equipment%20sizing%20-%20Hurmet.md) |
| Maintenance fuel tank volume | Preliminary geometric check: 11.81 m³ per tank after 50% cooling-pipe occupancy, versus 6.43 m³ gross core-sector envelope (1.84×). No enlargement indicated at this stage; clear internal dimensions, freeboard and connected-pipe inventory remain open | [Hurmet worksheet](calculations/reactor/Maintenance%20fuel%20tank%20capacity%20-%20Hurmet.md) |
| Reactor top insulation | No-hood-flow thermal estimate: conditional 500 mm calcium silicate, about 5 kW through the top; room-condition sensitivity and 6.4 t insulation mass documented; six fitted covers now replace the hood in the graphics; local service wells and thermal bridges need an updated heat balance | [Hurmet worksheet](calculations/reactor/Reactor%20top%20insulation%20-%20Hurmet.md) |
| Removable insulation cover | Five grids, bottom grooves and flat upper bearing retained; six fitted covers with hook pockets and removable service inserts are in the reactor. Earlier source cassette ~2.16 t; earlier fitted estimate 2.10 t excludes separate thermal inserts. D-038 installation copies add open-bottom channels, local insulation strips and extended pickups; revised mass/strength/thermal checks pending | [Cover and integration](../fastSaltModels/docs/tgrid-insulation-cover.md) |
| Research evidence | Fourteen indexed work groups, including historical designs and manuscripts; later UM accident work reported but not yet documented here | [Publication library](publications/index.md), [study register](research/studies.md) |
| MSU collaboration | Initial component brief prepared; current student work, repository, contacts, and agreed inputs still to collect | [Student project brief](collaboration/steam-generator-project.md) |
| Workshop presentation | October 27–29, 2026; working title “Fast Salt System - Progress”; ten-slide outline drafted for 14 minutes plus margin and 5 minutes for questions; working visuals refreshed; annotated Rankine-cycle diagrams delivered as editable PowerPoint and PNG, now including the motor-driven BFP alternative with revised heater paths; research figure and final slide composition pending | [Presentation preparation](presentations/README.md) |

## Next work, in order

Next model task: place a stairway to the reactor catwalk and check it against service piping, equipment and access routes. Absorber tubes retain their accessible spider penetrations.

1. Review the [timed workshop outline](presentations/workshop-outline.md) for “Fast Salt System - Progress” at the October 27–29, 2026 workshop, and select the supporting UM research figure.
2. Review the [provisional site layout](../fastSaltModels/docs/site-study.md), then refine the [motor-BFP equipment arrangement](../fastSaltModels/docs/site-study.md) with supplier outlines, piping corridors, columns, stairs, crane/rotor handling and installation access. Establish the fuel-preparation building brief separately.
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
