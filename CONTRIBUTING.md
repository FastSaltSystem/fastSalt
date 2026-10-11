# Contributing

This is the initial local organization of the Fast Salt System project. Public contribution and licensing arrangements are still to be established.

## Propose a change

1. Identify the document, component, or interface affected.
2. Explain the reason and cite the supporting source or calculation.
3. Label assumptions and distinguish reported results from proposed changes.
4. Update the related interface or decision record when the change affects another workstream.

When a shared remote is established, use branches and reviewed pull requests for changes to the shared baseline. Named reviewers will be recorded with the teams.

## Research and publication records

Preserve author names, document dates, design revisions, and original publication terms. Link to authoritative documents. Do not infer publication or acceptance from a filename such as “final” or “R2.” Keep editorial correspondence separate from public reading lists.

The [publication index](publications/index.md) is the editable source for the curated bibliography. The [curation notes](publications/curation-notes.md) record uncertain versions and duplicate files.

## Calculations and models

Use **Hurmet Markdown (`.md`) for official calculation results wherever practical**, following the [calculation conventions](calculations/README.md). Calca, Python, Julia, and specialist solvers remain acceptable development tools. When a calculation cannot reasonably be represented in Hurmet, retain its reproducible source and link a clear result summary; do not maintain a second implementation merely to satisfy a format preference.

Record units, input sources, software versions, model scope, run instructions, and meaningful checks. Recalculate a Hurmet worksheet before saving its results, and compare converted results with their source. State whether results are preliminary or reviewed; use of the preferred format does not itself establish review status. Keep component identities and reference frames explicit when exchanging data. A visual fit or closed mesh is not a substitute for a physics or engineering validation.

Do not add routine generated renders or caches to this repository. Retain original files in their owning repository or source collection and reference a named revision.
