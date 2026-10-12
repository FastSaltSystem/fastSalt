# Fast Salt System

The Fast Salt System is an open research and design project investigating conversion of spent nuclear fuel (SNF) into salt fuel, its use in the Wielenga Innovation Salt Tank Reactor (WISTR), and the associated fuel processing and power-generation systems.

The local app project is named **Fast Salt System** and brings together this repository and `fastSaltModels`.

This repository organizes the project definition, research evidence, component interfaces, and decisions. It is the local starting point for a future public project hub.

## Start here

- [Project status and next work](STATUS.md)
- [Workshop presentation preparation](presentations/README.md)
- [System overview](design/system-overview.md)
- [Design basis and current assumptions](design/design-basis.md)
- [Component and analysis interfaces](design/interfaces.md)
- [Publication library](publications/index.md)
- [Research studies](research/studies.md)
- [Calculations and result format](calculations/README.md)
- [Contributors and responsibilities](collaboration/contributors.md)
- [MSU steam-generator project](collaboration/steam-generator-project.md)
- [Decision record](decisions/index.md)
- [Contributing](CONTRIBUTING.md)

## Current work

The University of Michigan team has documented the evolution of WISSR and WISTR through neutronics, fuel-cycle, and thermal-fluid analyses. Subsequent accident-scenario work is ongoing, as reported by the project owner. Michigan State University students are developing the steam-generator concept. The mechanical and installation graphics are maintained in the separate [fastSaltModels project](../fastSaltModels/README.md).

The current site graphics checkpoint is fastSaltModels commit `a6bbc77`, “Preserve Fast Salt process buildings, service routing and air-inlet checkpoint.” The [named snapshot](../fastSaltModels/baselines/fast-salt-site-2026-10-12/) contains the complete Blender site, key views, checked reports and file hashes. It includes the converter/refiner/off-gas building reservations, paired heated fuel lines, pressure servers and nitrogen routing, internal fresh-air header, complete columns and generator inlet valve centers lowered to 1.35 m above floor.

Earlier [maintenance](../fastSaltModels/baselines/wistr-maintenance-2026-10-12/) (`06a13ef`) and [service-bundle](../fastSaltModels/baselines/wistr-service-bundles-2026-10-12/) (`8ec6833`) snapshots remain intact. These are visual geometry checkpoints, not structural, thermal, process or complete access qualification.

## Repository organization

| Repository | Role | Present status |
| --- | --- | --- |
| `fastSalt` | Project overview, publications, shared interfaces, research record, decisions | This repository |
| `fastSaltModels` | Python-authored WISTR and installation graphics, Blender output, geometry checks | Existing local repository; history retained |
| Steam-generator repository | Student calculations, models, reports, and component interfaces | Establish after checking for an existing MSU repository |
| University analysis repositories | Solver inputs, calculations, and research workflows | Locations and sharing arrangements to be recorded with the teams |
| PMS | General mechanical simulation software | Remains a separate tool; not copied here |

## Document conventions

Markdown is the authoritative source for project prose and the curated publication index. **Hurmet Markdown is the preferred official format for calculation results wherever practical.** Working calculations may use Calca, Python, Julia, or specialist solvers; see the [calculation conventions](calculations/README.md) for publication and verification. Original research files remain in their existing folders. HTML views may be generated later. Machine-readable engineering parameters should be introduced when an actual consuming workflow is defined, rather than duplicating this prose in another manually edited catalog.

Local document links and the sibling fastSaltModels link work in this workspace. Replace or supplement them with stable public URLs before publishing. No GitHub remote is configured by this initial setup.

Code and document licensing choices are pending. This repository does not change the terms of any referenced publication or university contribution. See [publication curation notes](publications/curation-notes.md).
