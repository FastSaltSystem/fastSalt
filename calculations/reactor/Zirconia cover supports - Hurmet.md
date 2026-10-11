---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Zirconia cover supports — preliminary screening

11 October 2026. Four fixed ceramic compression blocks support each removable
insulation cassette. This worksheet screens average contact stress and axial
heat conduction; it does not select an allowable load or predict hook
temperature. Geometry is provisional: 50 mm diameter, 75 mm height. No metal
through-bolt or continuous sleeve connects the two bearing faces. The upper
foot lifts away; the ceramic stays in its shallow lower seat.

## Inputs

Mass is a rounded 1,500 kg screening allowance, not the measured or rated lift
mass. Load factor 2 is an illustrative unequal-load sensitivity, not a code
factor. Real four-point reactions, contact flatness and eccentricity are
unresolved. The temperature difference of 500 K is a sensitivity input, not a
calculated ceramic temperature distribution. Use k = 3 W/(m K) as a provisional
effective conductivity. [CeramTec's material guide][1] lists 2.7 W/(m K) at
25°C for grade 848 TZP; this does not establish conductivity or allowable
compression at reactor operating temperature.

¢` format = "h7" `

¢` CassetteMass = 1500 kg `

¢` Gravity = 9.80665 m/s2 `

¢` Supports = 4 `

¢` Cassettes = 6 `

¢` Diameter = 50 mm `

¢` Height = 75 mm `

¢` LoadFactor = 2 `

¢` Conductivity = 3 W/m/K `

¢` DeltaTemperature = 500 K `

## Average stress, not a strength assessment

¢??` Area = pi * Diameter^2 / 4 = 〔1,963.495〕 mm2 `

¢??` MeanForce = CassetteMass * Gravity / Supports = 〔3.677494〕 kN `

¢??` MeanStress = MeanForce / Area = 〔1.872932〕 MPa `

¢??` ScreeningStress = LoadFactor * MeanStress = 〔3.745864〕 MPa `

No allowable stress is assigned. Do not compare this average with flexural
strength and call it a compression safety factor. Check ceramic grade, edge
loading, bearing-face finish, thermal shock, cycling, environmental
compatibility, fracture retention, differential expansion and the complete
support structure.

## Ceramic-only axial heat path

¢??` HeatPerBlock = Conductivity * Area * DeltaTemperature / Height = 〔39.26991〕 W `

¢??` HeatPerCassette = Supports * HeatPerBlock = 〔157.0796〕 W `

¢??` HeatAllCassettes = Cassettes * HeatPerCassette = 〔942.4778〕 W `

¢??` HeatAtHigherK = HeatPerCassette * 5 / 3 = 〔261.7994〕 W `

The final expression is a k = 5 W/(m K) sensitivity. The calculation neglects
contact resistance and steel resistance in series, but also omits heat arriving
at the posts by radiation, gas and insulation-side conduction. It is neither a
whole-cover heat leak nor a bound on it. Insulating the post sides and closing
the liner clearances need further detailing. Existing outer-skin ties remain
thermal paths. The frame is within the wool and should not be assumed cold.

## Mechanical arrangement

A 10 mm-deep lower cup has 1 mm nominal radial clearance around the ceramic. Its
rim stops 65 mm below the upper bearing plate, so no retaining metal spans the
break. These cold dimensions do not establish hot clearances. The resting load
path is upper frame → hollow steel post → upper bearing foot → zirconia → lower
seat. Attachment of the lower seat to the reactor is still reserved. When
lifting, the cassette leaves the ceramic behind; its load goes from the upper
frame into the sliding shoulders and crane hooks.

See the [cover brief][2] and [model guide][3].

[1]: https://www.ceramtec-group.com/fileadmin/user\_upload/Corporate/11\_Downloads/05\_Ceramaseal/CeramTec\_ctna\_materials.pdf

[2]: ../../design/reactor-insulation-cover.md

[3]: ../../../fastSaltModels/docs/insulation-cover.md
