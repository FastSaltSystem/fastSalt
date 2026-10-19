# Fast Salt System

An open research and design project investigating conversion of spent nuclear fuel into salt fuel, its use in the **Wielenga Innovation Salt Tank Reactor (WISTR)**, and the associated fuel processing and steam power plant.

**[View drawings and results](results/README.md)** · **[Explore the 3D models](https://github.com/FastSaltSystem/fastSaltModels/blob/aebdd36c7e7e6599c538882262847f7253aa5afb/results/README.md)** · **[Contribute](CONTRIBUTING.md)**

![Provisional Fast Salt plant layout: turbine hall, reactor building and control annex](https://raw.githubusercontent.com/FastSaltSystem/fastSaltModels/aebdd36c7e7e6599c538882262847f7253aa5afb/results/2026-10-15/control-annex/site.png)

*14 October 2026 site draft, published in the 15 October review collection. Selected roofs and walls are hidden to show equipment. The image is pinned to its model revision.*

## Start here

| I want to… | Start with |
| --- | --- |
| Understand the system | [System overview](design/system-overview.md) and [design basis](design/design-basis.md) |
| Read the coolant, absorber or fuel-maintenance P&IDs | [Viewable PDFs and individual SVG sheets](results/README.md#pid-review-snapshot--15-october-2026) |
| See the power cycle | [Motor-driven feed-pump cycle diagram](results/README.md#steam-power-cycle--11-october-2026) |
| See or rotate the mechanical models | [Dated model gallery](https://github.com/FastSaltSystem/fastSaltModels/blob/aebdd36c7e7e6599c538882262847f7253aa5afb/results/README.md) and [Blender downloads](https://github.com/FastSaltSystem/fastSaltModels/blob/aebdd36c7e7e6599c538882262847f7253aa5afb/README.md#open-a-model) |
| Inspect calculation assumptions | [Calculation conventions](calculations/README.md) and [selected Hurmet worksheets](results/README.md#read-the-calculations) |
| Find research and project history | [Research studies](research/studies.md), [publication index](publications/index.md), [decision record](decisions/index.md) |
| Join the work | [Contributing](CONTRIBUTING.md), [responsibilities](collaboration/contributors.md), [MSU steam-generator project](collaboration/steam-generator-project.md) |

The publication index identifies research and source documents; many original-file links refer to the project owner's local collection. It is a bibliography, not a public document-download library. The selected PDFs and images under **Viewable results** are included in these repositories.

## Current review material

The 15 October collection preserves six coolant P&ID sheets, four absorber sheets, and the three-sheet B3 fuel-maintenance P&ID. The model gallery includes the 14 October control-annex site views and dated reactor, turbine and insulation checkpoints. Each item retains its own revision and limitations; this is not a synchronized engineering release.

The University of Michigan team provides neutronics and related reactor analyses; accident-scenario work is ongoing as reported by the project owner. Michigan State University students are developing the steam-generator concept. See [project status](STATUS.md) for the detailed work record and [shared interfaces](design/interfaces.md) for component relationships.

## Two repositories, one project

| Repository | Owns |
| --- | --- |
| **[fastSalt](https://github.com/FastSaltSystem/fastSalt)** — this repository | Project documentation, calculation sources, P&IDs, research references, shared interfaces and decisions |
| **[fastSaltModels](https://github.com/FastSaltSystem/fastSaltModels)** | Python geometry, Blender generation, model guides and preserved visual checkpoints |

University solver repositories and the student team's repository remain separate workstreams whose sharing arrangements are to be recorded. PMS remains a separate mechanical-simulation tool.

For local development, clone both repositories into the same parent directory:

```sh
git clone https://github.com/FastSaltSystem/fastSalt.git
git clone https://github.com/FastSaltSystem/fastSaltModels.git
```

## Formats and contributions

Markdown is the editable source for project prose. Hurmet Markdown is the preferred format for calculation results wherever practical; GitHub displays the source but does not evaluate it. P&IDs use TOML definitions and Python builders. The [shared coolant model](design/engineering/README.md) supplies selected identities and inputs to the P&ID and 3D views; it is not yet a general export to university solvers.

`results/` contains selected, dated documents with provenance. Ordinary generated `outputs/` remain local and ignored. Public readers can browse without an invitation; contributors propose changes on branches through pull requests to protected `main`.

Code and document licensing choices remain pending. Referenced publications and university contributions retain their original terms and credits. See [contribution guidance](CONTRIBUTING.md) and [publication curation notes](publications/curation-notes.md).
