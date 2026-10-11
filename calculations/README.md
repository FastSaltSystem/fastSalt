# Calculations

**Hurmet Markdown (`.md`) is the preferred official format for Fast Salt System calculation results wherever practical.** This convention is recorded in [D-003](../decisions/index.md#d-003--prefer-hurmet-for-official-calculation-results).

## Working and publishing

Develop estimates in the tool that suits the work: Calca, Hurmet, Python, Julia, or a specialist solver. For a calculation that fits Hurmet, maintain the published worksheet as editable Hurmet Markdown with its inputs, equations, explanations, units, and calculated results together.

When converting a working calculation, compare the results with the source and document discrepancies, changed assumptions, and unit conventions. Recalculate in Hurmet before saving a result revision. Preserve the original calculation's provenance without requiring every exploratory version to remain synchronized.

If Hurmet cannot reasonably represent an analysis, keep the actual calculation in its appropriate tool and repository. Publish a readable result summary with links to the source revision, input data, software environment, and checks. A Hurmet summary may reference those results, but should identify externally calculated values explicitly rather than implying that Hurmet reproduced them.

## What a published worksheet should contain

- Purpose, scope, and preliminary or reviewed status.
- Inputs with units, assumptions, and source references.
- Equations or a traceable reference to the external calculation.
- Recalculated results, relevant software/package versions, and instructions for reproduction.
- Checks, limitations, unresolved questions, and the source revision used for any imported results.

The preferred file format does not establish engineering approval or validation.

## Markdown and display

Hurmet files are text and can be versioned in Git. Their prose is Markdown, with Hurmet extensions for calculation cells and saved results. A generic Markdown viewer does not execute those cells or reproduce all of Hurmet's mathematical typesetting. Open the worksheet in Hurmet for editing and recalculation; generate HTML or PDF snapshots when a broadly viewable presentation is needed. Treat snapshots as outputs of the versioned worksheet, not independently edited sources.

## Current worksheets

| Worksheet | Role and status | Checks |
| --- | --- | --- |
| [Generator sizing — Hurmet](steam-generator/Generator%20sizing%20-%20Hurmet.md) | Preferred published-format worksheet; preliminary source assumptions retained | [Conversion comparison](steam-generator/conversion-check.md) |
| [Generator sizing — Pluto](steam-generator/Generator%20sizing%20-%20Pluto.jl) | Comparison experiment; not a parallel official worksheet to maintain | [Experiment notes](steam-generator/Pluto%20-%20getting%20started.md) |

The source Calca file remains in the project owner's original calculation collection. Its location is recorded in the conversion comparison.

## Installation pump allowance

The [coolant pump estimate](steam-generator/Coolant%20pump%20estimate%20-%20Hurmet.md)
uses the generator worksheet's three-leg case plus the owner's 50% allowance.
It reserves three 2 MW motors and provisional centrifugal-pump envelopes.
[Verification and assumptions](steam-generator/pump-estimate-check.md).

## Steam and feedwater piping

[Steam and feedwater pipe sizing — Hurmet](steam-generator/Steam%20and%20feedwater%20pipe%20sizing%20-%20Hurmet.md)
sizes branches and common headers by velocity and pressure loss, then calculates
pressure-only nominal walls with allowances and tolerance. Material stresses,
design pressure and routing budgets are provisional; no standard schedules are
selected. [Results, checks and reproduction](steam-generator/steam-water-pipe-check.md).

## Steam and feedwater insulation

[Steam and feedwater insulation — Hurmet](steam-generator/Steam%20and%20feedwater%20insulation%20-%20Hurmet.md)
estimates straight-pipe thermal loss and radial thickness. Conditional layout
allowances are 350 mm steam and 175 mm feedwater, with explicit environmental
assumptions and sensitivity cases. [Verification and reproduction](steam-generator/steam-water-insulation-check.md).

## Molten-salt coolant insulation

[Molten-salt coolant insulation — Hurmet](steam-generator/Molten-salt%20coolant%20insulation%20-%20Hurmet.md)
extends the thermal estimate to the three coolant loops: provisional 400 mm hot
and 350 mm return insulation, with 400 mm on both as a common-thickness option.
The 1.5 m bare OD remains a thermal envelope pending wall sizing.
[Verification and sensitivities](steam-generator/molten-salt-insulation-check.md).

## Molten-salt coolant pipe wall

[Molten-salt coolant pipe wall — Hurmet](steam-generator/Molten-salt%20coolant%20pipe%20wall%20-%20Hurmet.md)
records the conditional 25 mm wall estimate at 1 MPa gauge and 50 MPa effective
stress, including allowances, pressure/stress sensitivities and unresolved design
checks. The calculated 1.475 m bare OD fits inside the earlier 1.5 m thermal envelope.
[Verification and reproduction](steam-generator/molten-salt-wall-check.md).

## Reactor top insulation without hood cooling

[Reactor top insulation — Hurmet](reactor/Reactor%20top%20insulation%20-%20Hurmet.md)
estimates a conditional 500 mm calcium-silicate top cover at a 602°C hot face
and 40°C room: about 57°C exposed surface and 5 kW top heat leakage. It includes
removable mass and environmental sensitivities, but does not establish vessel,
well or decay-heat cooling. [Verification](reactor/reactor-top-insulation-check.md).

- [Zirconia cover supports — Hurmet](reactor/Zirconia%20cover%20supports%20-%20Hurmet.md):
  provisional support contact stress and ceramic-only axial conduction; no material
  allowable, whole-cover heat leak or load rating is established.

- [Rigid cover cassette — Hurmet](reactor/Rigid%20cover%20cassette%20-%20Hurmet.md):
  block pressure, bottom channel/liner and rod screening, plus explicitly imported
  Python upper-frame deflections for the rigid-block alternative.

- [T-grid cover — Hurmet](reactor/T-grid%20cover%20-%20Hurmet.md): current five-level recessed-grid
  per-layer runner/collar and accumulated hanger/ceramic-bearing screening, direct-seating average pressure,
  and explicitly imported lifted-only upper-frame result. Supersedes the tray/post
  assumptions of the previous rigid-cover sheet for this revision.
