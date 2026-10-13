# Coolant P&ID revision history

| Revision | Date | Change | Preservation |
| --- | --- | --- | --- |
| A | 2026-10-13 | First two-sheet coolant circulation and storage/transfer draft; proposed instruments and isolation | Original root PDF/SVG/CSV files; original renderer and hashes in `revisions/rev-A/` |
| A-working | 2026-10-13 | Separated engineering YAML and layout YAML from the renderer; added validation, equipment register and reproducible working builds; engineering arrangement unchanged | Source files tracked through Git; ordinary generated output ignored |
| A-working / TOML | 2026-10-13 | Owner prefers explicit table headings and easier cut/paste. Adopted TOML for model and layout; explicit unresolved-field convention; eleven checks pass | YAML source archived; rendered PDF, SVGs and registers unchanged |

A named revision is a review milestone, not a construction release. Future entries should state the design changes and unresolved decisions that matter to reviewers.


## A-working / shared main-coolant source — 13 October 2026

D-053 moves main-circulation equipment, topology and numerical inputs into `design/engineering/coolant-system.toml`. The view imports shared identities and rejects local engineering overrides. Storage/transfer and proposals remain local; layout is unchanged. Source and adapter hashes are recorded. PDF, SVGs and registers compare byte-identically with the preceding TOML draft. Preserved Revision A remains untouched.
