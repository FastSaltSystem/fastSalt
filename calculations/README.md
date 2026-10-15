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


## Rankine-cycle power plant

[Rankine cycle - Hurmet](power-cycle/Rankine%20cycle%20-%20Hurmet.md) presents the
first regenerative main-steam-reheat case from the owner's system diagram,
with a 5 kPa condenser. Steam properties and coupled extraction fractions are
explicitly imported from a versioned Python/CoolProp calculation. Hurmet handles
flow/power scaling and the conditional condenser estimate. See the
[design basis, state table and checks](power-cycle/README.md).


[Cooling-water cases - Hurmet](power-cycle/Cooling-water%20cases%20-%20Hurmet.md)
checks the accepted 20/30/35°C inlet-water assumptions against one unchanged
condenser envelope. Coupled pressures and cycle results are explicitly imported;
Hurmet verifies thermal area and water temperature rise.


[Selected reheat and wetness - Hurmet](power-cycle/Selected%20reheat%20and%20wetness%20-%20Hurmet.md)
is the current preliminary power-cycle basis (D-026). It replaces the initial
4 MPa / 470°C trial for equipment studies, retaining its source/results for
comparison. A single main-steam reheater at revised pressures meets the provisional
moisture and thermal-approach screens with a 5 kPa condenser floor.


[Power plant equipment sizing - Hurmet](power-cycle/Power%20plant%20equipment%20sizing%20-%20Hurmet.md)
adds preliminary exchanger areas, turbine exhaust passages, generators, pump duties,
deaerator storage and main/extraction pipe bores. [Sizing notes](power-cycle/equipment-sizing-notes.md)
distinguish calculated requirements from layout allowances. The higher proposed
pump pressures need cycle reclosure before updating performance; no graphics change.


[BFP drive comparison — Hurmet](power-cycle/BFP%20drive%20comparison%20-%20Hurmet.md)
compares matched steam/electric pump drives with rebalanced heater extractions and
proposed pump pressure budgets. Electric drive has a conditional 4 MW penalty,
with increased reheater capacity; a candidate for review, not a replacement of
the selected equipment or diagram. Python and Hurmet checks are recorded with it.


[Motor-BFP equipment sizing — Hurmet](power-cycle/Motor-BFP%20equipment%20sizing%20-%20Hurmet.md)
is the current preliminary equipment revision (D-029): revised reheater, generators,
electric pump supplies and pipe bores, with the first dimensional building draft.
Earlier steam-drive schedules remain historical references. Fifty Hurmet numerical
comparisons, two sensitivities and four-case pipe-velocity checks passed.


[Maintenance fuel tank capacity — Hurmet](reactor/Maintenance%20fuel%20tank%20capacity%20-%20Hurmet.md)
compares one tank with the full gross core-sector envelope. At 50% cooling-pipe
occupancy, the modeled tank provides 11.81 m³ versus a 6.43 m³ sector envelope.
This preliminary check uses exterior tank dimensions; internal construction,
freeboard and connected-pipe fuel inventory remain to be resolved.









[Coolant inventory and storage capacity — Hurmet](reactor/Coolant%20inventory%20and%20storage%20capacity%20-%20Hurmet.md) compares the approximately 452 m³ circuit (D-063) with TK-401's provisional 73 m³ working acceptance. A 450°C fill case gives 18–25 m³ expansion, but full hot drainage requires roughly 479 m³ before uncertainty/freeboard allowances. The 8.2 × 16 m D-058 tank reservation is checked separately; relocation remains pending. [Basis, sensitivities and 67 Hurmet checks](reactor/coolant-inventory-check.md).


[Normal coolant pressure profile — Hurmet](reactor/Normal%20coolant%20pressure%20profile%20-%20Hurmet.md) now combines the 1 bar(g) SG-top reference with the UM flow and allocated itemized losses: approximately 2.25 bar(g) suction, 3.82 discharge and 4.25 at the reactor bottom-plenum midpoint. The earlier broad envelope is archived. [Results, assumptions and 53 Hurmet checks](reactor/coolant-pressure-check.md). Mean-density screening only; no pressure ratings or relief settings are selected. SG failure assessment remains deferred.


[Core coolant pressure loss — Hurmet](reactor/Core%20coolant%20pressure%20loss%20-%20Hurmet.md) uses owner-selected UM flow and corrected 3.4 m height: approximately 44.5 kPa active-core friction or 62.7 kPa including reflector extensions and provisional end losses. It distinguishes 2.993 m/s mean velocity from 3.035 m/s hot-outlet velocity and documents the report's count/area mismatch. [Checks](reactor/core-coolant-loss-check.md).


## Itemized coolant pump power

[Itemized coolant pump estimate — Hurmet](steam-generator/Itemized%20coolant%20pump%20estimate%20-%20Hurmet.md) replaces the blanket allowance for the new UM-flow calculation with SG/core/piping and explicit provisional fitting losses. Working total is 2.504 MW electrical for three pumps, with 2.24–3.07 MW fitting sensitivity. [Checks and limits](steam-generator/coolant-pump-itemized-check.md). D-063 updates the shared graphics/P&ID duty; no motor change is selected.

## Current shared coolant hydraulic case — D-063

Use the core, **Itemized coolant pump estimate**, and **Normal coolant pressure profile** Hurmet sheets for current normal-duty inputs. D-063 retains 18,500 kg/s total and 810–890 K, and adopts 172.162 kPa full-loop loss with counterSG tube geometry into the shared views. The original **Coolant pump estimate** remains historical except for its retained 2 MW motor-envelope reservation. Earlier Brayton studies are separate exploratory cases, not revised automatically by this adoption.

## Newer SG workbook — D-063

[Source and correction record](steam-generator/sources/README.md). Corrected `counterSG.xlsx` labels; independently reproduced 11.920866 m length. Active pump, pressure and inventory Hurmet sheets now use this geometry. Earlier Generator sizing and auxiliary Brayton calculations remain historical.

## Absorber system

[Absorber capacity and gas modules — Hurmet](reactor/Absorber%20capacity%20and%20gas%20modules%20-%20Hurmet.md) compares the source charges with current 3D envelopes and gas-space balances. See the [P&ID and assessment](../design/pids/absorber-system/README.md). Bottom-reflector volume is excluded; updated injection time remains unresolved.
