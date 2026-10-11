---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Rigid insulation cassette — preliminary screening

11 October 2026. Companion to the [separate rigid-block model][1]. The original
wool draft is retained. Values are provisional; no allowable stress or load
rating is assigned. Steel modulus is an assumed screening input, not a
qualified value for a chosen alloy at temperature.

## Weight and compression

The insulation density allowance uses [Thermo-1200 data][2]. Published
compression above 690 kPa is at 5% compression and must not be treated as a
working allowable. No bending or joint shear capacity is credited to blocks.

¢` format = "h7" `

¢` Density = 240 kg/m3 `

¢` InsulationDepth = 500 mm `

¢` Gravity = 9.80665 m/s2 `

¢` CassetteMass = 1839.156713100 kg `

¢` WoolCassetteMass = 1459.683582204 kg `

¢??` AddedMass = CassetteMass - WoolCassetteMass = 〔379.4731〕 kg `

¢??` MeanBlockPressure = Density * InsulationDepth * Gravity = 〔1.176798〕 kPa `

## Upper-frame results imported from Python

These four values are **externally calculated inputs**, not a Hurmet solution of
the grillage. Source: `outputs/reactor-rigid-cover/rigid-cover-report.json` in
fastSaltModels; report SHA-256
`ff014121a85bc2acd8e440fbdbad3923ea2c2dc1bf81538dd0ec9d184f5d5b56`. The report
also records the generating model and solver hashes. The model uses 160 × 60 ×
3 mm gross RHS sections, rigid joints and plan-area-distributed total mass; no
credit for the insulation stiffening the frame. Four equal-elevation supports
represent either hooks or seats. Actual crane compliance, contact settlement,
slot weakening, local buckling, weld flexibility and thermal strains are
absent. See the model guide for the method and verification.

¢` E = 140 GPa `

¢` LiftedApex = 5.649020521 mm `

¢` SeatedApex = 4.722054137 mm `

¢` LiftedStress = 48.855595850 MPa `

¢` SeatedStress = 32.270474153 MPa `

¢` LoadMultiplier = 2 `

¢??` LiftedDeflectionSensitivity = LoadMultiplier * LiftedApex = 〔11.29804〕 mm `

¢??` LiftedStressSensitivity = LoadMultiplier * LiftedStress = 〔97.71119〕 MPa `

The multiplier illustrates linear load sensitivity. It is not a code load factor
and does not check any allowable. Changing E here does not rerun the grillage;
rerun Python if frame geometry or its property assumptions change.

## Bottom channel and hanger screening

A channel spans between its centre and edge rods. Treat each half as simply
supported, with full column weight of insulation and liner plus channel
self-weight. This neglects beneficial continuity. I is calculated from one 100
× 2 mm top and two 60 × 2 mm downward webs, ignoring corner radii and liner
composite action. The imported maximum half-span follows the authored hanger
positions.

¢` ChannelWidth = 100 mm `

¢` ChannelWall = 2 mm `

¢` WebDepth = 60 mm `

¢` Pitch = 300 mm `

¢` LinerThickness = 1.5 mm `

¢` SteelDensity = 8000 kg/m3 `

¢` Span = 1.800669241384 m `

¢` RodDiameter = 6 mm `

¢` RodLength = 590 mm `

¢??` TopArea = ChannelWidth * ChannelWall = 〔200〕 mm2 `

¢??` WebArea = ChannelWall * WebDepth = 〔120〕 mm2 `

¢??` CentroidDepth = (TopArea * ChannelWall / 2 + 2 * WebArea * (ChannelWall +
WebDepth / 2)) / (TopArea + 2 * WebArea) = 〔17.90909〕 mm `

¢??` ChannelI = ChannelWidth * ChannelWall^3 / 12 + TopArea * (ChannelWall / 2 -
CentroidDepth)^2 + 2 * (ChannelWall * WebDepth^3 / 12 + WebArea *
(ChannelWall + WebDepth / 2 - CentroidDepth)^2) = 〔176,903〕 mm4 `

¢??` ChannelLoad = (MeanBlockPressure + SteelDensity * Gravity *
LinerThickness) * Pitch + (TopArea + 2 * WebArea) * SteelDensity * Gravity =
〔422.8627〕 N/m `

¢??` ChannelSag = 5 * ChannelLoad * Span^4 / (384 * E * ChannelI) = 〔2.33728〕 mm `

¢??` ChannelStress = ChannelLoad * Span^2 / 8 * (ChannelWall + WebDepth -
CentroidDepth) / ChannelI = 〔42.71605〕 MPa `

¢??` CentreRodLoad = ChannelLoad * Span = 〔761.4359〕 N `

¢??` RodArea = pi * RodDiameter^2 / 4 = 〔28.27433〕 mm2 `

¢??` RodGrossStress = CentreRodLoad / RodArea = 〔26.93029〕 MPa `

¢??` RodExtension = CentreRodLoad * RodLength / (E * RodArea) = 〔0.1134919〕 mm `

Thread-root area, local washer/flange bending, adjustment and fatigue require
separate checks. The rods are tension members; their small nominal stress is
not a rating for threaded connections or hot-service material.

## Liner strip between channel tops

Use a one-metre-wide strip, simply supported across the 200 mm clear gap,
carrying the insulation column. The liner's own small weight is omitted here.
No beneficial block bending is assumed.

¢` StripWidth = 1 m `

¢??` ClearGap = Pitch - ChannelWidth = 〔200〕 mm `

¢??` StripI = StripWidth * LinerThickness^3 / 12 = 〔281.25〕 mm4 `

¢??` LinerSag = 5 * MeanBlockPressure * StripWidth * ClearGap^4 / (384 * E *
StripI) = 〔0.6226444〕 mm `

The upper-frame, channel, rod and liner displacements are separate estimates at
different positions; their maxima are not a solved total apex displacement.
This sheet does not assess the four compression posts, zirconia contacts, full
thermal paths, block durability or reactor service clearances.

[1]: ../../../fastSaltModels/docs/rigid-insulation-cover.md

[2]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\_IND\_Thermo-1200\_DS.pdf
