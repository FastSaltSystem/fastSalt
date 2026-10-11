# MSU steam-generator project

## Current understanding

The MSU student team is developing a steam-generator design as part of its education. Thomas Wielenga has supplied preliminary Calca calculations and asked the team to use ChatGPT, Python, and Blender. The project now includes a [Hurmet conversion of Generator sizing.calca](../calculations/steam-generator/Generator%20sizing%20-%20Hurmet.md) and its [conversion checks](../calculations/steam-generator/conversion-check.md). Current student work and any existing team repository still need to be inventoried.

This is an initial coordination brief for discussion with the team, not a new assignment issued to it.

## Proposed first milestone

Understand, reproduce, and check the preliminary Calca calculations before extending the design. Publish the calculation results in Hurmet Markdown wherever practical. The existing conversion provides a starting point; it is still a preliminary calculation, not a reviewed design baseline. Use Calca, Python, Julia, or other appropriate tools for development as needed. Record units, assumptions, input sources, and any differences found, and preserve the original Calca files as the calculation history.

Agree [IF-001](../design/interfaces.md#if-001-reactor-and-steam-generator) with the project owner and relevant UM contributors. Record inputs that remain undecided rather than substituting unmarked assumptions.

## Proposed deliverable package

- A Hurmet Markdown worksheet explaining the calculation, inputs, results, and limits wherever practical.
- Supporting code or solver inputs, when used, with dependency information and run instructions. For results that cannot reasonably be calculated in Hurmet, provide a readable summary linked to their reproducible source.
- A parameterized component model and a viewable Blender snapshot.
- An interface summary with equipment envelope, connection locations, estimated mass where supported, and access needs.
- A list of unresolved questions and the checks performed.

ChatGPT can assist with development and explanation. The saved calculations and documentation must contain the evidence needed for another person to review the work independently of the chat.

## Repository and integration

Check whether the team already has a repository before creating another. Preserve student authorship and work history. An early equipment envelope can be integrated into the installation model while detailed design continues.
