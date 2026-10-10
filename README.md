# Fast Salt System

The Fast Salt System is an open research and design project investigating conversion of spent nuclear fuel (SNF) into salt fuel, its use in the Wielenga Innovation Salt Tank Reactor (WISTR), and the associated fuel processing and power-generation systems.

This repository organizes the project definition, research evidence, component interfaces, and decisions. It is the local starting point for a future public project hub.

## Start here

- [System overview](design/system-overview.md)
- [Design basis and current assumptions](design/design-basis.md)
- [Component and analysis interfaces](design/interfaces.md)
- [Publication library](publications/index.md)
- [Research studies](research/studies.md)
- [Contributors and responsibilities](collaboration/contributors.md)
- [MSU steam-generator project](collaboration/steam-generator-project.md)
- [Decision record](decisions/index.md)
- [Contributing](CONTRIBUTING.md)

## Current work

The University of Michigan team has documented the evolution of WISSR and WISTR through neutronics, fuel-cycle, and thermal-fluid analyses. Subsequent accident-scenario work is ongoing, as reported by the project owner. Michigan State University students are developing the steam-generator concept. The mechanical and installation graphics are maintained in the separate [TextualGraphics project](../TextualGraphics/README.md).

The current graphics baseline is TextualGraphics commit `0d981f2`, “Preserve WISTR remote handling and removable tube plugs.” It is a geometric concept baseline; it does not establish mass properties, structural capacity, or agreement with every analysis model.

## Repository organization

| Repository | Role | Present status |
| --- | --- | --- |
| `fastSalt` | Project overview, publications, shared interfaces, research record, decisions | This repository |
| `TextualGraphics` | Python-authored WISTR and installation graphics, Blender output, geometry checks | Existing local repository; history retained |
| Steam-generator repository | Student calculations, models, reports, and component interfaces | Establish after checking for an existing MSU repository |
| University analysis repositories | Solver inputs, calculations, and research workflows | Locations and sharing arrangements to be recorded with the teams |
| PMS | General mechanical simulation software | Remains a separate tool; not copied here |

## Document conventions

Markdown is the authoritative source for project prose and the curated publication index. Original research files remain in their existing folders. HTML views may be generated later. Machine-readable engineering parameters should be introduced when an actual consuming workflow is defined, rather than duplicating this prose in another manually edited catalog.

Local document links and the sibling TextualGraphics link work in this workspace. Replace or supplement them with stable public URLs before publishing. No GitHub remote is configured by this initial setup.

Code and document licensing choices are pending. This repository does not change the terms of any referenced publication or university contribution. See [publication curation notes](publications/curation-notes.md).
