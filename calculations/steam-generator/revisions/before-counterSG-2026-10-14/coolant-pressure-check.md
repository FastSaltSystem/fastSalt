# Normal coolant pressure profile — itemized revision

14 October 2026. [Editable Hurmet worksheet](Normal%20coolant%20pressure%20profile%20-%20Hurmet.md). Replaces the [earlier unallocated-loss screen](revisions/pressure-before-itemized-2026-10-14/README.md).

## Station pressures

Reference is 1.00 bar(g) at a provisional SG-top liquid elevation of 17 m above floor. Three equal legs share the owner-selected UM total flow, 18,500 kg/s, and 810–890 K temperature case. Use mean density for hydrostatics and the checked itemized hydraulic losses.

| Location | Base, bar(g) | Low fitting-loss case | High fitting-loss case |
| --- | ---: | ---: | ---: |
| SG hot connection | 1.24 | 1.24 | 1.24 |
| SG cold connection | 1.96 | 2.03 | 1.86 |
| Main pump suction | 1.66 | 1.74 | 1.53 |
| Main pump discharge | 3.82 | 3.73 | 4.07 |
| Reactor cold-nozzle outer connection | 3.78 | 3.71 | 3.96 |
| Reactor bottom-plenum midpoint | 4.25 | 4.21 | 4.36 |
| Reactor hot-nozzle outer connection | 2.77 | 2.75 | 2.85 |

Low/high describe the selected coefficient scenarios, not the minimum/maximum pressure at every location. Lower SG resistance raises suction pressure; higher downstream resistance raises required discharge pressure. Each case uses its own required pump head at the same flow. These are not confidence bounds or points on one fixed pump curve.

## Loss allocation

| Segment | Base loss, kPa |
| --- | ---: |
| Across SG, including tube ends and both collectors | 145.52 |
| SG cold connection to pump suction | 2.97 |
| Pump discharge to reactor cold outer connection | 3.90 |
| Cold nozzle and downcomer to bottom plenum | 6.80 |
| Core/reflector passage and hot nozzle | 65.85 |
| Hot outer connection to SG hot connection | 5.64 |

Total 230.681 kPa matches the itemized pump estimate. Pump suction-to-discharge static pressure difference is only about 216.3 kPa because the discharge is 0.90 m higher. Adding that elevation term recovers the 230.7 kPa pump head expressed as pressure; it is not a missing loss.

The current suction estimate is 1.66 bar(g), rather than the old broad 0.29–1.24 interval. The old interval used greater flow and allowed all unspecified extra loop resistance to lie before the pump. It is superseded, not an additional uncertainty band around the new result.

## Checks and limitations

- 53 Hurmet comparisons agree with independent SI balances; save/reopen passes.
- Base/low/high loss totals match their upstream pump worksheet cases; each complete pressure loop closes to numerical precision.
- A 0.5 bar reduction of the reference shifts every station by 0.5 bar. Base suction becomes about 1.16 bar(g); this does not establish NPSH or select a lower operating target.
- Raising the reference elevation by 1 m shifts pressures approximately 0.160 bar. Actual accumulator level and gas tap relationship to the SG inlet collector are not yet designed.
- Hydrostatic sensitivity at uniform hot/cold density is checked while keeping imported losses fixed. It is not a distributed-temperature/thermosiphon solution. The base profile consistently retains the mean-density approximation used in the earlier pressure screen.
- Dynamic pressure in main pipes is roughly 0.045–0.046 bar, and in nozzles about 0.06 bar. Local velocity corrections are omitted; results are preliminary station estimates, not precise tap predictions.
- Both SG collector terms are grouped inside the SG segment. Actual gas-reference location relative to the collector could shift the anchored profile by a collector-scale loss.
- TK-401 remains isolated between transfers; its pressure is not set by this circulation profile. The reported bottom value is a plenum midpoint, not maximum wall pressure.
- No pressure rating, relief setting, SG failure assessment, building rearrangement, motor change, geometry rebuild or commit is included.

## Reproduction

Run `python calculations/reactor/coolant_pressure_profile.py`, then `node calculations/reactor/check_coolant_pressure.cjs` with HURMET_ENGINE and TEMML_ENGINE configured. Source hashes are checked before importing the upstream itemized loss budget. [Results and sources](coolant-pressure-results.json); [Hurmet checks](coolant-pressure-hurmet-checks.json). Preview HTML remains ignored under `outputs/coolant-pressure/`.

The six previous calculation/check/source files are retained under `revisions/pressure-before-itemized-2026-10-14/`. D-061 now adopts this case into shared graphics/P&ID records; the active pressure worksheet imports the itemized loss budget directly. Numerical values are unchanged after the provenance refresh.

