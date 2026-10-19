# RS-008: Auxiliary Brayton Cooling Options for the Fast Salt System

**Preliminary Comparative Study - Revision A - 19 October 2026**

[PDF report](../../results/2026-10-19/auxiliary-brayton-rev-a/report.pdf) · [Browser report](../../results/2026-10-19/auxiliary-brayton-rev-a/report.html) · [Editable report](../../results/2026-10-19/auxiliary-brayton-rev-a/report.md) · [Full study package](../../results/2026-10-19/auxiliary-brayton-rev-a/README.md)

## Question and scope

How do the existing steam, nitrogen, open-air and simple supercritical CO₂ Brayton auxiliary-cooling trials compare in power margin, gas flow and heat-rejection scale? Revision A consolidates the saved 12-13 October calculations at a common illustrative 30 MW-per-train duty. It makes no new equipment selection and adds no thermodynamic or hydraulic model.

## Responsibility and review

Project owner: Thomas Wielenga. Prepared within the Fast Salt System project using AI-assisted calculations and documentation; technical review is pending. This is a project working study, not a university-issued report. The MSU emergency air-passage study remains separate.

## Findings and assumptions

The selected cases show positive nominal power margins after modeled fan and salt-pump demand. Small working-fluid volumes do not eliminate the external heat sink. The historical 130 kW pump allowance uses the original steam-generator pressure-loss model plus 50%, rather than the later itemized estimate. The report retains this distinction, the different operating pressures, and the original sensitivity findings.

## Preserved evidence

Revision A includes 36 source files: Hurmet worksheets, Python generators, JavaScript checks, saved results, existing check records, property-package requirements and the original generator-sizing reference. The [manifest](../../results/2026-10-19/auxiliary-brayton-rev-a/manifest.json) identifies actual file contents and the repository base commit. Some sources were uncommitted when captured. A [historical hash audit](../../results/2026-10-19/auxiliary-brayton-rev-a/source-hash-audit.json) records two differences between earlier result provenance and current generator copies.

The [packaging checks](../../results/2026-10-19/auxiliary-brayton-rev-a/packaging-checks.json) cover source-copy integrity, 24 comparison cells, report links and visual review of five PDF pages. Thermodynamic models were not rerun for packaging. Original check results retain their earlier scope.

## Continuing the work

The [working overview](../../calculations/power-cycle/brayton-overview.md) remains the entry point for ongoing edits. Preserve Revision A unchanged; issue a new revision when results, assumptions or review status change. No physical model or university study is changed by this documentation snapshot.
