# Absorber system draft

**Public drawing:** [15 October review snapshot](../../../results/2026-10-15/README.md#absorber). Links into `outputs/` below refer to local builds and are not hosted on GitHub.

15 October 2026. D-070 starts a functional P&ID and capacity check using the owner's injection-time report and the latest site elevations.

## Review

- [Four-sheet P&ID and capacity review](outputs/current/WISTR-absorber-PID.pdf)
- [Circuit diagram SVG](outputs/current/FS-AS-001.svg), [repetition and states](outputs/current/FS-AS-002.svg), [capacity review](outputs/current/FS-AS-003.svg), [separate charging/discharge headers](outputs/current/FS-AS-004.svg)
- [Hurmet worksheet](../../../calculations/reactor/Absorber%20capacity%20and%20gas%20modules%20-%20Hurmet.md) and [browser preview](../../../calculations/reactor/outputs/absorber-capacity/absorber-capacity.html)
- [Calculation results](../../../calculations/reactor/absorber-capacity-results.json) and [Hurmet checks](../../../calculations/reactor/absorber-capacity-hurmet-checks.json)
- [Expanded register](outputs/current/register.csv) and [topology checks](outputs/current/checks.json)
- [Blender chamber-bottom revision](../../../../fastSaltModels/outputs/absorber-review/fast-salt-absorber-review.blend)

## Confirmed arrangement

Each of six narrow in-core absorber tanks contains independent primary and secondary chambers, with source salt volumes of 0.1589 and 0.1938 m³ respectively. Each chamber has its own external salt reservoir and absorber module. Absorber salt moves into and out of the chambers; the tanks remain stationary. A/B tags identify primary/secondary; mapping to the current centre/outer tube pairs is not yet confirmed.

The owner requires external bottom-fed salt lines, not internal dip tubes. The chamber bottom is at the active-core bottom, Z = -7.27 m, excluding the 0.30 m bottom reflector. Filling therefore does not first fill a liquid pocket below the core. The existing top boundary is retained at Z = -3.62 m; the active-core top is -3.87 m. The upper 0.25 m is screened as gas space, not an additional salt charge. The physical partition and upper gas volumes remain provisional.

The new Blender draft raises all six absorber tank bottoms; the canonical generator uses the same bottom. **External bottom-feed piping has not yet been drawn in 3D**: the saved top terminations are placeholders for rerouting. Absorber supports must be reconciled with the raised bottoms. Original scenes and the Word document remain untouched.

## Capacity findings

The revised absorber tank envelope is 613.2 litres gross, including 571.2 litres over the active height, compared with 352.7 litres total source charge. A trial 3 mm wall and radial partition leaves 526.1 litres over the active height. This shows space for the stated volumes, not an adopted wall, chamber shape or neutron-absorption adequacy.

Each external reservoir is 643.4 litres gross. It exceeds either source charge, also under an illustrative 80% working-volume allowance. Final usable capacity must include tube inventory, residual heel and thermal expansion. Oversized tanks must not simply be charged full: their gas space affects the pressure balance.

Retaining the report's pressure-vessel volume equal to the source charge, current reservoir headspace and current heights give ideal pressure-plus-surge volumes of 515.0/616.0 litres (primary/secondary) without extra chamber gas space, or 522.0/623.9 litres including the provisional upper space. The secondary nearly consumes the module's entire 643.4 litre lower cylinder before walls, heads, nozzles and fittings. Its upper box has 929.5 litres gross, but that is not verified equipment accommodation. Retain the overall reservation while arranging two real gas vessels and a compressor; the current single cylinder does not establish module adequacy.

These are equal-temperature isothermal balances with density inferred from the report's pressure/head, zero heel and initially filled salt piping. Actual hot/cold gas temperatures, additional gas lines and physical gas volumes require review. Equilibrium at exactly full is not a liquid-carryover protection scheme. Calculated pressures are not selected settings.

## Separate gas charging and discharge

D-071, 15 October 2026: the owner chooses a pair of service lines per absorber module. **H-700N** carries clean nitrogen from the gas-treatment-area distribution to twelve **N-701A through N-706B** branches. Each has its own **V-…N** isolation valve and a provisional **NRV-…** nonreturn function. Twelve separate **G-701A through G-706B** branches, each with **V-…R** isolation, collect into **H-700R** and return via **G-700** to **B-700T**, a receiving interface before treatment. Discharge has no direct route into the clean nitrogen header.

The charging supply boundary **B-700N** refers to the existing **B-602** nitrogen distribution in the gas-treatment area, downstream of the clean supply. It reserves pressure/flow conditioning and supply isolation without selecting devices or settings. The dedicated return is not connected to that nitrogen distribution. Treatment capacity, receiving pressure, hold-up and final release arrangements remain unspecified.

The draft provisionally connects both module service ports to the surge vessel. The existing recovery compressor supplies the pressure vessel. This internal choice is for review: it does not establish how every isolated gas space can be depressurized or purged. Module valve types, actuation, fail positions and pressure limits are unresolved. Each charging branch reserves backflow prevention, with hardware and protection design still open.

Both module isolation valves are closed during normal absorber duty in the draft, preserving independent circuit gas volumes. Charging uses the supply connection with return isolated; discharge uses the return with supply isolated. These describe intended connections, not an operating procedure. Module-side dead-leg volumes must be added to the final gas balance; shared headers are excluded while isolated. Service discharge does not replace an overpressure protection system.

The four-sheet P&ID expands to 282 uniquely tagged records: 76 equipment/boundary records, 110 lines, 60 instrument proposals and 36 service valve/function reservations (24 isolations and 12 nonreturn functions). All endpoints, valve-line associations and discharge/clean-supply separation are checked. **These new service lines are not yet routed in Blender.**

## Source discrepancies and timing

In the Word document, Eq 5 omits the hydrostatic term from the printed denominator; its reported results are consistent with including that term. Eq 14 has a sign inconsistency with the physically consistent Eq 17. Equal volume flow does not imply equal velocities through different cross-sections. These are recorded in the worksheet without editing the original.

The reported 18.2/22.2 s times are preserved as historical results. No updated time is claimed: the report lacks numerical pipe bore, hydraulic length, viscosity and roughness, and the final 3D bottom-feed route is incomplete. Gas restrictions, temperature changes, valve performance and required insertion time remain unresolved.

## Sources and generation

[Engineering basis](../../engineering/absorber-system.toml) stores source hashes, measured geometry, owner changes and calculation assumptions. [System TOML](absorber-system.toml) defines a reusable circuit and six-by-two repetition. [Layout TOML](layout.toml) places it independently. The builder reuses the coolant drawing primitives without modifying the coolant system.

Run `python calculations/reactor/absorber_capacity.py` from the hub, then `node calculations/reactor/check_absorber_capacity.cjs` with `HURMET_ENGINE` and `TEMML_ENGINE` set to the project bundles. The pinned Hurmet engine is commit `8e82edefe91f1fff5d79df046880fcb5375ed1c4`, with the hash recorded in the check report. Run `python design/pids/absorber-system/build.py` with ReportLab available to recreate PDF, SVGs and registers. Working outputs remain ignored.

The module routing block shows remove (P-A/R-S), inject (P-R/A-S), and a proposed blocked hold state. Physical valve selection, fail state, command logic, protection, instrumentation technology and compressor duty remain unresolved. Separate absorber discharge is routed to a receiving interface before gas treatment; the specific treatment train and its relationship to fuel off-gas equipment remain unresolved. This is a discussion P&ID, not an operating procedure.
