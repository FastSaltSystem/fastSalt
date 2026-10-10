# Component and analysis interfaces

Interface definitions are initial coordination records. No cross-solver exporter or coupled simulation is implemented here.

## IF-001: Reactor and steam generator

Participants: project owner, UM analysis team, and MSU steam-generator team. Named reviewers remain to be recorded.

Inputs to agree: system operating cases; heat duty and allocation among coolant legs; coolant and steam-side conditions; material-property sources and temperature ranges; allowed pressure losses; transient cases relevant to the component; connection sizes and coordinate convention.

Outputs expected from the component study: calculation basis, performance estimates and limits, equipment envelope, connection positions and directions, mass estimates where available, access requirements, and uncertainties.

The current three-leg visual arrangement is a starting interface assumption. It does not by itself establish a steam-generator design or equal-load operating conditions.

## IF-002: Shared design and analysis models

Each model should identify the design revision, component names, geometry scope, units, materials, operating state, simplifications, software version, and its source repository or input-file location.

| Representation | Information to exchange |
| --- | --- |
| Neutronics models | Geometric/material-region definitions and documented simplifications; study outputs with their provenance |
| SAM/system analysis | Component topology, agreed parameters, boundary conditions, cases, and relevant result summaries |
| Local CFD | Modeled domain, boundary conditions, heat-source basis, property sources, mesh/case versions, and scope of any derived quantities |
| Mechanical models | Physical parts and assemblies, material assignments, operating state, and eventual mass-property results |
| Blender graphics | Component geometry, reference frames, display detail, and deliberate presentation changes |

First establish traceable inputs and outputs. Automated coupling is a separate development decision with an identified use case.

## IF-003: Components and installation layout

The graphics project currently uses metres and Z-up. A shared project coordinate system is to be agreed rather than assumed for university inputs.

Each placed component should supply an envelope, connection coordinates and directions, orientation, support interfaces, and access/removal envelopes. Every exported geometry must declare units and its origin.

The installation baseline should identify the exact revisions of the reactor, steam generator, and system assumptions used.
