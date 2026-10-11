---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Five-level T-grid cover — preliminary screening

11 October 2026. Each of five layers has its own grid and provisional crimp
stops. Only the bottom layer is grooved; upper blocks rest on flanges. Local
grid load is separated from accumulated rod load. Coating adhesion remains an
owner-authorized assumption without composite strength credit. No material
allowable or lifting rating is assigned.

## Geometry mass inputs

Evaluated mesh masses include grid intersections additively. Geometry retains a
512 mm stack: five 100 mm block layers plus four 3 mm supporting flanges.
Seated average pressure is only a whole-face reference; local compression
beneath flange strips and actual lifting load redistribution are not
calculated. These inputs supersede the single-grid sheet.

¢` format = "h7" `

¢` Radius = 4.121639668346854 m `

¢` CassetteMass = 2160.92400768 kg `

¢` Gravity = 9.80665 m/s2 `

¢` LayerMass1 = 336.375387888 kg `

¢` LayerMass2 = 301.824115736 kg `

¢` LayerMass3 = 301.896404507 kg `

¢` LayerMass4 = 301.824036774 kg `

¢` LayerMass5 = 299.062968045 kg `

¢` SharedHardwareMass = 12.5578219468 kg `

¢??` GrossArea = pi * Radius^2 / 6 = 〔8.894851〕 m2 `

¢??` AverageSeatedPressure = CassetteMass * Gravity / GrossArea = 〔2.382437〕 kPa `

Layer mass includes its blocks, T-grid, saddles and collars. Level 1 also
includes the underside facing/joint cement. Shared hardware includes rods,
upper spreaders/nuts and ceramics. It excludes the upper frame and exterior
shell, which are carried directly by the hooks/frame rather than by the grid rods.

## Most heavily loaded grid level

The main-runner screen distributes each supported level over gross plan area.
This includes cross-tee and peripheral-grid mass, but does not resolve
individual connection forces. The gross T-section ignores holes/notches and
weld flexibility. E and all connection dimensions remain provisional.

¢` E = 140 GPa `

¢` FlangeWidth = 50 mm `

¢` FlangeThickness = 3 mm `

¢` WebHeight = 45 mm `

¢` WebThickness = 2 mm `

¢` TributaryWidth = 600 mm `

¢` Span = 0.560100677028 m `

¢??` HeaviestLayer = max(LayerMass1, LayerMass2, LayerMass3, LayerMass4,
LayerMass5) = 〔336.3754〕 kg `

¢??` LayerPressure = HeaviestLayer * Gravity / GrossArea = 〔0.3708568〕 kPa `

¢??` FlangeArea = FlangeWidth * FlangeThickness = 〔150〕 mm2 `

¢??` WebArea = WebHeight * WebThickness = 〔90〕 mm2 `

¢??` Centroid = (FlangeArea * FlangeThickness / 2 + WebArea * (FlangeThickness +
WebHeight / 2)) / (FlangeArea + WebArea) = 〔10.5〕 mm `

¢??` RunnerI = FlangeWidth * FlangeThickness^3 / 12 + FlangeArea *
(FlangeThickness / 2 - Centroid)^2 + WebThickness * WebHeight^3 / 12 +
WebArea * (FlangeThickness + WebHeight / 2 - Centroid)^2 = 〔47,700〕 mm4 `

¢??` LineLoad = LayerPressure * TributaryWidth = 〔222.5141〕 N/m `

¢??` RunnerSag = 5 * LineLoad * Span^4 / (384 * E * RunnerI) = 〔0.04269866〕 mm `

¢??` RunnerStress = LineLoad * Span^2 / 8 * (FlangeThickness + WebHeight -
Centroid) / RunnerI = 〔6.859818〕 MPa `

¢??` SingleCollarForce = LineLoad * Span = 〔124.6303〕 N `

## Accumulated upper rod and ceramic load

Use a full span times the 600 mm tributary width for a representative interior
rod. Sum every level plus shared hardware. Actual load sharing, thread roots,
crimp retention, saddle/weld capacity and thermal movement are not established.
The collar force above is for one level, not the force in the upper rod.

¢??` SuspendedMass = LayerMass1 + LayerMass2 + LayerMass3 + LayerMass4 +
LayerMass5 + SharedHardwareMass = 〔1,553.541〕 kg `

¢??` RodForce = SuspendedMass * Gravity / GrossArea * TributaryWidth * Span =
〔575.6016〕 N `

¢` RodDiameter = 6 mm `

¢??` RodStress = RodForce / (pi * RodDiameter^2 / 4) = 〔20.35774〕 MPa `

¢` SpreaderDiameter = 32 mm `

¢` CeramicOpening = 14 mm `

¢??` CeramicArea = pi * (SpreaderDiameter^2 - CeramicOpening^2) / 4 = 〔650.3097〕 mm2 `

¢??` CeramicBearing = RodForce / CeramicArea = 〔0.8851192〕 MPa `

## Imported upper-frame result

This is an external Python grillage calculation, not a Hurmet solver result.
Report SHA-256:
`805f5fb870320830d025fe3ecf29d6dc23a94ff2b9cb7548510cb4a4cd23f770`. Source:
`fastSaltModels/outputs/reactor-tgrid-cover/tgrid-cover-report.json`; source
code hashes are in the report. The lifted-only frame model distributes total
cassette mass by area and uses four equal-height hooks, rigid joints and
provisional steel stiffness. No seated grillage result applies to this revision.

¢` LiftedApex = 6.45737452244 mm `

Local grid sag and global frame movement are separate screens. Neither proves
groove strength, hot material suitability, stability or a lifting rating.

[Model guide][1].

[1]: ../../../fastSaltModels/docs/tgrid-insulation-cover.md
