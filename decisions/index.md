# Decision record

## D-001 — Start with a local project hub

Date: 2026-10-10

Context: The project includes a growing publication history, university analysis, mechanical graphics, and a student steam-generator project.

Decision: Establish `fastSalt` locally as the central documentation and coordination repository. Keep TextualGraphics and its approved baselines intact. Record the university repositories when their locations are available. Establish a steam-generator repository after checking for existing student work.

Source: Project-owner agreement in the project conversation and creation of the local fastSalt folder.

Consequences: This initial repository contains Markdown documentation and links to existing sources. It does not publish files or create a GitHub organization.

## D-002 — Markdown is the editable documentation source

Date: 2026-10-10

Decision: Maintain project prose and the curated publication index in Markdown. Generate HTML views only when useful. Keep machine-generated file inventories separate from the curated bibliography.

Source: Project discussion comparing Markdown with the initial HTML publication index.

Consequences: Avoid independently editing duplicate Markdown, JSON, and HTML versions of the same publication record. The earlier HTML/JSON inventory is a historical first-pass aid in TextualGraphics outputs.

## Proposals not yet adopted

- A common Python engineering definition with adapters for graphics and analysis tools.
- Public GitHub organization and repository names.
- Code, documentation, and design-material licensing choices.
- Final student and university repository arrangements.

## Format for subsequent decisions

Use a stable ID, date, context, decision, responsible participants, source, affected models/interfaces, and consequences. Preserve superseded decisions and link to their replacements.
