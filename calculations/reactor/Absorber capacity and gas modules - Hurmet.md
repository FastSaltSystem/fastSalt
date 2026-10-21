---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Absorber capacity and gas module screen

¢` format = "h3" `

Preliminary review, 15 October 2026. Twelve circuits: primary A and secondary B
at each of six radial assemblies. Source chamber volumes are 0.1589 and 0.1938
m³; their neutronic sufficiency is not reassessed. Current 3D elevations
override the older sketch. The absorber bottom is raised 0.30 m to the
active-core bottom; other equipment envelopes are retained.

The editable equations use explicit, unit-aware quantities. Pressures are in kPa
absolute; volumes are displayed in m³ or litres. Hurmet performs the unit
conversions. These balance pressures are not adopted settings.

## Geometry and assumptions

The original measured absorber tank was 2.10 × 0.08 × 3.95 m, Z = -7.57 to
-3.62 m. The owner excludes the bottom reflector: the adopted bottom is Z =
-7.27 m and the remaining envelope is 3.65 m tall. The active core spans Z =
-7.27 to -3.87 m, 3.4 m high. Reservoir bottoms are Z = -0.05 m. No salt volume
below the active core is included. The second case estimates the 0.25 m upper
region as retained gas space, using the source chamber cross-sections; it is
not additional salt fill. Partition geometry remains unresolved.

Density is inferred from document Eq 1, not independently specified. Reservoirs
are provisionally treated as gross cylinders, with salt charge equal to chamber
volume, zero heel, unchanged prefilled line inventory, and the remaining gas
space initially at 100 kPa absolute. Pressure-vessel volume equals chamber
volume as in the source. Gas is isothermal at equal temperature; real hot/cold
gas differences and line volumes need review.

¢` Gravity = 9.81 m/s2 `

¢` SourcePressure = 337.79 kPa `

¢` SurgeInitial = 100 kPa `

¢` SourceHead = 7.2 m `

¢` PrimaryCharge = 0.1589 m3 `

¢` SecondaryCharge = 0.1938 m3 `

¢` ActiveHeight = 3.4 m `

¢` AbsorberTankLength = 2.1 m `

¢` AbsorberTankWidth = 0.08 m `

¢` AbsorberTankHeight = 3.65 m `

¢` WallTrial = 0.003 m `

¢` TankDiameter = 0.806349471933 m `

¢` TankHeight = 1.25992104989 m `

¢` ReservoirBottom = -0.05 m `

¢` CoreBottom = -7.27 m `

¢` CoreTop = -3.87 m `

¢` AbsorberTankBottom = -7.27 m `

¢` AbsorberTankTop = -3.62 m `

¢` UpperGasHeight = 0.25 m `

¢%%` Density = (SourcePressure - SurgeInitial) / (Gravity SourceHead) = 〔3,367〕
kg/m3 `

¢%%` Gradient = Density Gravity = 〔33〕 kPa/m `

¢%%` TankArea = π TankDiameter^2 / 4 = 〔0.511〕 m2 `

¢%%` TankVolume = TankArea TankHeight = 〔0.643〕 m3 `

¢%%` TankLitres = TankVolume = 〔643〕 L `

¢%%` AbsorberTankGrossL = AbsorberTankLength AbsorberTankWidth
AbsorberTankHeight = 〔613〕 L `

¢%%` AbsorberTankActiveL = AbsorberTankLength AbsorberTankWidth ActiveHeight =
〔571〕 L `

¢%%` TrialNetL = (AbsorberTankLength - 3 WallTrial) (AbsorberTankWidth - 2
WallTrial) ActiveHeight = 〔526〕 L `

¢%%` ChargeTotalL = (PrimaryCharge + SecondaryCharge) = 〔353〕 L `

¢%%` ReservoirTrialL = 0.8 TankLitres = 〔515〕 L `

The 3 mm wall/partition trial and 80% reservoir allowance are capacity
sensitivities only. No metal thickness, usable fill fraction or chamber
division is adopted. The physical fit must also accommodate the separate
bottom-fed external salt tubes.

## Corrected source balance

Eq 5 must include the hydrostatic term in its denominator. For the original 3 m
gap and a zero-headspace full reservoir:

¢%%` SourcePrimarySurgeL = SourcePressure PrimaryCharge / (SourcePressure / 2 +
Gradient * (3 'm') - SurgeInitial) = 〔320〕 L `

¢%%` SourceSecondarySurgeL = SourcePressure SecondaryCharge / (SourcePressure /
2 + Gradient * (3 'm') - SurgeInitial) = 〔390〕 L `

The result reproduces about 319.6 and 389.7 litres. The source intermediate Eq
14 also has a sign inconsistency; its Eq 17 correctly gives head = hp + initial
salt depth - filled height - reservoir level drop. Continuity means equal
volume flow, not equal velocities in unequal areas.

## Current reservoir and elevation screen

For each circuit, p0 is the static pressure needed to hold its chamber empty. On
switching, the pressure vessel mixes with the reservoir headspace. Final
reservoir pressure is (p0 Vp + ps0 Vg0)/(Vp + Vg0 + charge). With retained
chamber gas volume Va, the required surge volume is \[p0 charge + (p0 - final
gas pressure) Va] / (final gas pressure - initial surge pressure). This follows
from final hydrostatic balance and conservation of gas. Equilibrium at exactly
full is a mathematical screen, not a carryover-prevention design. D-071 adds
separate charging and discharge services: both module service isolation valves
are closed for this normal-duty gas balance. Shared headers are excluded;
additional module-side dead-leg volume remains to include.

### Active Band primary

¢%%` ActivePrimaryVolume = PrimaryCharge = 〔0.159〕 m3 `

¢%%` ActivePrimaryGasVolume = 0 'm3' = 〔0〕 m3 `

¢%%` ActivePrimaryDepth = ActivePrimaryVolume / TankArea = 〔0.311〕 m `

¢%%` ActivePrimaryHp = ReservoirBottom - CoreBottom = 〔7.22〕 m `

¢%%` ActivePrimaryHf = ReservoirBottom - CoreTop = 〔3.82〕 m `

¢%%` ActivePrimaryP0 = SurgeInitial + Gradient (ActivePrimaryHp +
ActivePrimaryDepth) = 〔349〕 kPa `

¢%%` ActivePrimaryFinal = (ActivePrimaryP0 ActivePrimaryVolume + SurgeInitial
(TankVolume - ActivePrimaryVolume)) / (ActivePrimaryVolume + TankVolume) =
〔129〕 kPa `

¢%%` ActivePrimarySurge = (ActivePrimaryP0 ActivePrimaryVolume +
(ActivePrimaryP0 - ActivePrimaryFinal - Gradient ActivePrimaryHf)
ActivePrimaryGasVolume) / (ActivePrimaryFinal + Gradient ActivePrimaryHf -
SurgeInitial) = 〔0.356〕 m3 `

¢%%` ActivePrimaryPressureL = ActivePrimaryVolume = 〔159〕 L `

¢%%` ActivePrimarySurgeL = ActivePrimarySurge = 〔356〕 L `

¢%%` ActivePrimaryTotalL = (ActivePrimaryVolume + ActivePrimarySurge) = 〔515〕 L `

¢%%` ActivePrimaryP0kPa = ActivePrimaryP0 = 〔349〕 kPa `

### Active Band secondary

¢%%` ActiveSecondaryVolume = SecondaryCharge = 〔0.194〕 m3 `

¢%%` ActiveSecondaryGasVolume = 0 'm3' = 〔0〕 m3 `

¢%%` ActiveSecondaryDepth = ActiveSecondaryVolume / TankArea = 〔0.38〕 m `

¢%%` ActiveSecondaryHp = ReservoirBottom - CoreBottom = 〔7.22〕 m `

¢%%` ActiveSecondaryHf = ReservoirBottom - CoreTop = 〔3.82〕 m `

¢%%` ActiveSecondaryP0 = SurgeInitial + Gradient (ActiveSecondaryHp +
ActiveSecondaryDepth) = 〔351〕 kPa `

¢%%` ActiveSecondaryFinal = (ActiveSecondaryP0 ActiveSecondaryVolume +
SurgeInitial (TankVolume - ActiveSecondaryVolume)) / (ActiveSecondaryVolume +
TankVolume) = 〔135〕 kPa `

¢%%` ActiveSecondarySurge = (ActiveSecondaryP0 ActiveSecondaryVolume +
(ActiveSecondaryP0 - ActiveSecondaryFinal - Gradient ActiveSecondaryHf)
ActiveSecondaryGasVolume) / (ActiveSecondaryFinal + Gradient
ActiveSecondaryHf - SurgeInitial) = 〔0.422〕 m3 `

¢%%` ActiveSecondaryPressureL = ActiveSecondaryVolume = 〔194〕 L `

¢%%` ActiveSecondarySurgeL = ActiveSecondarySurge = 〔422〕 L `

¢%%` ActiveSecondaryTotalL = (ActiveSecondaryVolume + ActiveSecondarySurge) =
〔616〕 L `

¢%%` ActiveSecondaryP0kPa = ActiveSecondaryP0 = 〔351〕 kPa `

### Upper Gas Space primary

¢%%` UpperPrimaryVolume = PrimaryCharge = 〔0.159〕 m3 `

¢%%` UpperPrimaryGasVolume = UpperPrimaryVolume / ActiveHeight * UpperGasHeight
= 〔0.0117〕 m3 `

¢%%` UpperPrimaryDepth = UpperPrimaryVolume / TankArea = 〔0.311〕 m `

¢%%` UpperPrimaryHp = ReservoirBottom - CoreBottom = 〔7.22〕 m `

¢%%` UpperPrimaryHf = ReservoirBottom - CoreTop = 〔3.82〕 m `

¢%%` UpperPrimaryP0 = SurgeInitial + Gradient (UpperPrimaryHp +
UpperPrimaryDepth) = 〔349〕 kPa `

¢%%` UpperPrimaryFinal = (UpperPrimaryP0 UpperPrimaryVolume + SurgeInitial
(TankVolume - UpperPrimaryVolume)) / (UpperPrimaryVolume + TankVolume) = 〔129〕 kPa `

¢%%` UpperPrimarySurge = (UpperPrimaryP0 UpperPrimaryVolume + (UpperPrimaryP0 -
UpperPrimaryFinal - Gradient UpperPrimaryHf) UpperPrimaryGasVolume) /
(UpperPrimaryFinal + Gradient UpperPrimaryHf - SurgeInitial) = 〔0.363〕 m3 `

¢%%` UpperPrimaryPressureL = UpperPrimaryVolume = 〔159〕 L `

¢%%` UpperPrimarySurgeL = UpperPrimarySurge = 〔363〕 L `

¢%%` UpperPrimaryTotalL = (UpperPrimaryVolume + UpperPrimarySurge) = 〔522〕 L `

¢%%` UpperPrimaryP0kPa = UpperPrimaryP0 = 〔349〕 kPa `

### Upper Gas Space secondary

¢%%` UpperSecondaryVolume = SecondaryCharge = 〔0.194〕 m3 `

¢%%` UpperSecondaryGasVolume = UpperSecondaryVolume / ActiveHeight *
UpperGasHeight = 〔0.0143〕 m3 `

¢%%` UpperSecondaryDepth = UpperSecondaryVolume / TankArea = 〔0.38〕 m `

¢%%` UpperSecondaryHp = ReservoirBottom - CoreBottom = 〔7.22〕 m `

¢%%` UpperSecondaryHf = ReservoirBottom - CoreTop = 〔3.82〕 m `

¢%%` UpperSecondaryP0 = SurgeInitial + Gradient (UpperSecondaryHp +
UpperSecondaryDepth) = 〔351〕 kPa `

¢%%` UpperSecondaryFinal = (UpperSecondaryP0 UpperSecondaryVolume + SurgeInitial
(TankVolume - UpperSecondaryVolume)) / (UpperSecondaryVolume + TankVolume) =
〔135〕 kPa `

¢%%` UpperSecondarySurge = (UpperSecondaryP0 UpperSecondaryVolume +
(UpperSecondaryP0 - UpperSecondaryFinal - Gradient UpperSecondaryHf)
UpperSecondaryGasVolume) / (UpperSecondaryFinal + Gradient UpperSecondaryHf -
SurgeInitial) = 〔0.43〕 m3 `

¢%%` UpperSecondaryPressureL = UpperSecondaryVolume = 〔194〕 L `

¢%%` UpperSecondarySurgeL = UpperSecondarySurge = 〔430〕 L `

¢%%` UpperSecondaryTotalL = (UpperSecondaryVolume + UpperSecondarySurge) = 〔624〕 L `

¢%%` UpperSecondaryP0kPa = UpperSecondaryP0 = 〔351〕 kPa `

## Interpretation

The existing 643.4 litre salt reservoirs exceed both source charges, including
an illustrative 80% working-volume screen. Filling them completely is not the
modeled operating charge. The internal absorber tanks have enough gross
geometric space for the source volumes, but their partitions, walls and upper
gas spaces are not defined; no bottom-reflector liquid pocket is included.

The active-band primary module requires about 515 litres of ideal
pressure-plus-surge gas space; the secondary about 616 litres. The latter
nearly consumes the entire 643 litre lower cylinder before walls, heads and
fittings. Including the 0.25 m upper gas space increases these totals; see the
Upper case cells above. This space stays gaseous when the active chamber is
filled. The rejected bottom-reflector fill case is removed. The 0.765 × 0.810 ×
1.50 m upper enclosure is additional gross space, not verified pressure-vessel
accommodation. Retain the overall module reservation pending an internal
arrangement; do not conclude that the single lower cylinder alone is adequate.

There is no updated injection-time prediction. The document reports 18.2 and
22.2 s, but numerical bore, hydraulic length, viscosity, roughness, gas
temperatures and valve/gas-line resistance are not supplied. The current 50 mm
OD and 2 mm visual wall imply 46 mm bore only as a visualization assumption.
External bottom routing must be completed before its hydraulic length is
available. Required shutdown time and gas recovery time are also unresolved. No
calibration to the reported times is used.

## Michigan team input and results record

Status: awaiting team input and review. This section records externally supplied
analysis; it contains no injection-time calculation. Blank entries mean not
provided, not zero. The historical times quoted above are not current results.

### Original dimensioned reference drawing

Historical geometry from page 1 of AbsorberSaltInjectionTime.docx. The drawing
is reproduced unchanged from the supplied document. Its dimensions and routing
have not been updated to the current 3D model. Use the geometry/model revision
field below to identify the drawing used by the Michigan team.

![1][]

The original drawing is a reference for the document's notation, not a new
dimensioned drawing of the current installation.

### Analysis identification

| Field                                 | Team entry     |
|---------------------------------------|----------------|
| Analysis title and case identifier    | To be supplied |
| Author and organization               | To be supplied |
| Analysis date and revision            | To be supplied |
| Report or calculation file reference  | To be supplied |
| Geometry/model file and revision used | To be supplied |
| Reviewer, review date and status      | Not reviewed   |
{.grid colWidths="null null"}

### Inputs and assumptions supplied by the team

Record the values actually used in the referenced analysis, including their
units and sources. Identify each entry as measured, reported, assumed or
reviewed. Reference the geometry section above where applicable and record any
differences; its values are not automatically adopted by this record. Duplicate
rows as needed.

| Input or assumption | Value or description | Units          | Source/revision | Status  |
|---------------------|----------------------|----------------|-----------------|---------|
| To be supplied      | To be supplied       | To be supplied | To be supplied  | Pending |
{.grid colWidths="null null null null null"}

### Team-reported results

Define the meaning of each reported time in the team report, and identify the
case and applicable limitations. Values below are entered from that report;
they are not calculated or validated by this worksheet.

+-------------------------+-----------------+-------------------+----------------+-----------------------+
| Result                  | Primary chamber | Secondary chamber | Units          | Report/case reference |
+=========================+=================+===================+================+=======================+
| Reported filling time   | Pending         | Pending           | s              | Pending               |
+-------------------------+-----------------+-------------------+----------------+-----------------------+
| Definition of reported  | Pending         | Pending           | Not applicable | Pending               |
| time                    |                 |                   |                |                       |
+-------------------------+-----------------+-------------------+----------------+-----------------------+
| Reported uncertainty or | Pending         | Pending           | As reported    | Pending               |
| range                   |                 |                   |                |                       |
+-------------------------+-----------------+-------------------+----------------+-----------------------+
{.grid colWidths="null null null null null"}

### Review notes and revision record

+--------------------------------------------------+----------------+
| Field                                            | Team entry     |
+==================================================+================+
| Applicability and limitations                    | To be supplied |
+--------------------------------------------------+----------------+
| Differences from the Word document or current    | To be supplied |
| geometry                                         |                |
+--------------------------------------------------+----------------+
| Open questions and responsible person            | To be supplied |
+--------------------------------------------------+----------------+
| Review disposition and supporting reference      | Pending        |
+--------------------------------------------------+----------------+
| Revision, date, author and description of change | To be supplied |
+--------------------------------------------------+----------------+
{.grid colWidths="null null"}

This section is maintained in this Hurmet Markdown file and preserved by the
worksheet generator. Keep its heading and the following Sources and
reproduction heading when editing.

## Sources and reproduction

Source: AbsorberSaltInjectionTime.docx, pages 1-6; immutable source hash in
design/engineering/absorber-system.toml. Current scene measurements:
absorber-geometry-audit.json. Owner confirmed two separate chambers per
assembly, external bottom-feed routing, and exclusion of the bottom-reflector
region on 15 October 2026.

General gas-law reference: [DOE Fundamentals Handbook, Thermodynamics volume
1][2]. Absolute pressures and temperatures are required. This does not validate
the source isothermal assumption.

Run absorber_capacity.py and then check_absorber_capacity.cjs with HURMET_ENGINE
and TEMML\_ENGINE set to the pinned project bundles. Python independently
checks measured elevations, counts, original source rounding and final balance
closure; Hurmet checks evaluation, reopening and parameter sensitivity.
Generated HTML remains ignored.

[1]: assets/absorber-injection-original-dimensioned.png
{.inline}

[2]: https://www.energy.gov/documents/doe-hdbk-1012-92vol1

[3]: assets/absorber-injection-original-dimensioned.png
{.inline alt="Original dimensioned absorber-system schematic from the Word document"}
