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
| Coolant pipe outside diameter | 1.4 m | Current visual definition; not a completed sizing result for the requested flow-velocity limit |
| Maximum average coolant-pipe velocity | 3 m/s | Owner-requested sizing criterion; flow calculation and selected clear bore remain to be reconciled |
| Peripheral reflector radial thickness | 0.30 m | Current visual definition |
| Bottom / top reflector thickness | 0.30 / 0.25 m | Current visual definition |
| Downcomer radial width | 1.00 m | Current visual definition |
| Bottom / hot plenum height | 0.75 / 1.60 m | Current visual definition; hot plenum enlarged to accommodate pipe connections |

## Sources

- [Current visual parameters](../../TextualGraphics/models/wistr_reactor.py), pinned initially to TextualGraphics commit `0d981f2`.
- [Graphics baseline documentation](../../TextualGraphics/README.md).
- [Fast Salt System revision 5](</Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Fast Salt/Fast Salt System 5.pptx>), cover dated June 26, 2026.
- [UM research overview, work W10](../publications/index.md#w10).
- Project-owner instructions in the originating project conversation, transcribed into this register; confirm this record during engineering review.

## Reconciliation still needed

- Match each analysis to its geometry, material, and operating-state revision. The November 2025 report covers several historical designs.
- Establish the operating conditions, properties, and calculation reference used for coolant flow and steam-generator sizing.
- Agree drained, filled, and maintenance states before calculating masses and lifting balance.
- Assign stable parameter identifiers and a machine-readable schema only when the first shared calculation or model adapter is implemented.

When a value changes, record its source, date, reason, and affected interfaces. Do not silently replace historical study inputs with current visual dimensions.
