# Normal coolant pressure screen

14 October 2026. Preliminary steady-flow calculation; steam-generator failure assessment is explicitly deferred at the owner's request. No new pressure rating, relief destination, hardware or setpoint is adopted.

## Results

The [editable Hurmet worksheet](Normal%20coolant%20pressure%20profile%20-%20Hurmet.md) uses 1 bar(g) at a provisional 17 m SG-top reference, 1637.93 kg/m³ representative density, 190.873 kPa SG friction and 286.309 kPa pump rise. Elevations are extracted from the current three-leg assembly; no Blender regeneration occurs.

| Location | Height above floor, m | Normal pressure screen, bar(g) |
| --- | ---: | ---: |
| SG top reference | 17.00 | 1.00 |
| SG hot-inlet connection | 15.50 | 1.24 |
| SG cold-outlet connection | 1.90 | 1.52 |
| Main pump suction | 3.61 | 0.29–1.24 |
| Main pump discharge | 4.51 | 3.01–3.96 |
| Reactor cold inlet | 4.51 | 3.01–3.96 |
| Reactor bottom-plenum midpoint | 1.155 | 3.55–4.50 |
| Reactor hot outlet | 6.28 | 2.72–3.68 |

The bounds redistribute the unlocated 95.436 kPa loss allowance among suction piping, cold-return piping, reactor downflow, reactor upflow and hot piping. They preserve the aggregate pump/loss balance. Bounds at different locations are correlated; they are not independently selectable pressures or a statistical uncertainty interval. They do not cover losses greater than the inherited budget.

The 13.6 m descent between SG connection centres adds about 2.185 bar hydrostatically, exceeding the inherited 1.909 bar SG friction loss. The resulting net pressure gain is about 0.276 bar. Closed-loop elevation is not an additional pump lift with uniform density.

Reducing the SG-top target to 0.5 bar(g) shifts the suction interval to approximately −0.21 to +0.74 bar(g). This is a comparison only. Cavitation margin is not established by gauge pressure: vapor pressure, local velocities, gas release and required NPSH remain unresolved.

## Checks and scope

- 27 independently calculated outputs agree with real Hurmet recalculation; save/reopen is stable.
- The 0.5 bar reference-pressure shift and two uniform-density sensitivity cases pass.
- Five extreme loss allocations and 100 reproducible mixed allocations close the loop and remain within every station's bounds.
- All three legs have matching imported elevations and assumed equal duty.
- Main-pipe velocity-pressure scale is about 0.069 bar. Velocity changes are neglected, and this does not bound local manifold/tube effects.
- Density is uniform in the base screen. Hot/cold uniform-density checks are not a thermosiphon calculation.
- The gas-vessel salt level is not yet modeled; casing-top height is provisional. A 1 m datum change shifts the profile about 0.16 bar.
- TK-401 is isolated between transfers; it does not automatically share the SG bias pressure. Its transfer pressure is outside this normal-circulation profile.
- Building/tank rearrangement, SG failure, relief sizing and transient pressure remain deferred. The output is not a maximum allowable/design pressure determination.

## Reproduction

Run `python calculations/reactor/coolant_pressure_profile.py` from the hub, followed by `node calculations/reactor/check_coolant_pressure.cjs` with HURMET_ENGINE and TEMML_ENGINE set to the Hurmet bundles. The Python script also accepts explicit `--hub`, `--models` and `--output` paths.

Inputs, source hashes and Python checks: [results](coolant-pressure-results.json). Hurmet checks and engine hash: [verification](coolant-pressure-hurmet-checks.json). HTML preview is generated in ignored `outputs/coolant-pressure/`. Hurmet remains the editable calculation; rerunning the publisher restores imported baseline inputs.

Method reference: [DOE Fluid Flow handbook](https://www.energy.gov/ehss/articles/doe-hdbk-10123-92), extended Bernoulli balance. This general method is not reactor qualification.
