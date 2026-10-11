---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Molten-salt coolant pipe wall estimate

Preliminary concept estimate — 11 October 2026. The base assumptions produce
**25 mm nominal wall for both hot and cold coolant pipes**, with a 1.425 m
clear bore and 1.475 m bare outside diameter. These are conditional dimensional
estimates, not a verified construction thickness, selected pipe schedule or
approved material specification. This sheet records the discussion and makes
the assumptions and sensitivities editable. No graphics dimensions are changed.

Open in Hurmet and recalculate after editing inputs. Numerical results are live
calculation cells. Inputs copied from other worksheets do not update
automatically.

## 1. Flow and bore

The [coolant pump worksheet][1] gives 4.619533 m³/s per coolant circuit and a
286.3092 kPa running pump pressure-rise allowance. There are three circuits,
each with one hot route and one cool-return route. The bore calculation uses
per-circuit flow, not the combined flow through all three circuits. Round the
minimum bore upward in 25 mm increments to obtain the provisional 1.425 m bore.
This is a dimensional envelope, not a standard pipe size.

The [generator worksheet][2] specifies 875 K (601.85°C) hot coolant and 810 K
(536.85°C) cool return. Its inherited coolant basis is a
magnesium/potassium/sodium chloride mixture. Material compatibility must be
established for the actual salt chemistry and impurities; fluoride-salt alloy
experience alone is not qualification.

¢` format = "h7" `

¢` VolumeFlow = 4.619533 m3/s `

¢` VelocityLimit = 3 m/s `

¢` BoreStep = 25 mm `

¢` HotTemperature = 875 K `

¢` ColdTemperature = 810 K `

¢` RunningPumpRise = 286.3092 kPa `

¢??` MinimumBore = sqrt(4 * VolumeFlow / (pi * VelocityLimit)) = 〔1.400211〕 m `

¢??` Bore = ceil(MinimumBore / BoreStep) * BoreStep = 〔1.425〕 m `

¢??` Velocity = 4 * VolumeFlow / (pi * Bore^2) = 〔2.896533〕 m/s `

## 2. Provisional pressure, stress and allowances

Use **1.0 MPa gauge (10 bar)** solely as a pressure-design screening case. It
has not been derived as the maximum system pressure. Running pump rise is a
pressure difference, not the maximum pipe pressure. Establish local maximum
pressure from cover-gas pressure, hydrostatic elevation, pump shutoff, normal
and upset conditions, and steam-generator tube-failure pressurization. The
secondary water/steam operating basis is 24 MPa absolute; any low-pressure
coolant design needs a substantiated response to that pressure source,
including relief/isolation arrangements. Do not infer that the 1 MPa case is
sufficient. A pressure profile is required; summing unrelated worst-case heads
is not a substitute for locating the critical section and operating condition.

Use **50 MPa effective allowable stress**, meaning S × E × W combined, including
any weld-joint and high-temperature weld-strength factors. This is a numerical
assumption for an unselected material, not a room-temperature yield strength or
a code-table value for a named alloy. The same value screens both hot and cold
legs. Temperature inputs above provide context only: changing temperature does
not automatically update allowable stress, weld factors or corrosion allowance.
Confirm these values at the selected design temperature, service life and code.

Use a **3 mm corrosion/erosion allowance** and **12.5% negative wall
tolerance**. Neither is established from a corrosion-life assessment or a
selected product. For fabricated plate pipe, use the actual
procurement/fabrication tolerances. The dimensionless pressure coefficient y =
0.40 is a provisional screening choice; confirm its applicability for the
material, temperature and governing code. Nominal wall is rounded upward in 5
mm increments for concept layout.

¢` DesignPressure = 1 MPa `

¢` EffectiveStress = 50 MPa `

¢` PressureCoefficient = 0.40 `

¢` Allowance = 3 mm `

¢` NegativeTolerance = 0.125 `

¢` WallStep = 5 mm `

## 3. Straight-pipe pressure relation

Use the same ASME B31.1-type straight circular-pipe internal-pressure relation
as the [steam/feedwater pipe worksheet][3]. An accessible historical ASME text
is hosted by [LANL][4]; [ASME][5] is the official source for current editions.
The applicable code, edition, jurisdiction and nuclear classification remain
unselected. This screening use does not certify code compliance.

For outside diameter Do, pressure P, effective stress Se and coefficient y,
required delivered wall is P Do / \[2(Se + P y)] + A. Since Do = Di + 2 tn and
available delivered wall is (1 − m)tn, solve simultaneously for nominal wall
tn: alpha = P / \[2(Se + P y)], then tn = (alpha Di + A)/(1 − m − 2 alpha). A
is allowance and m is the fractional negative tolerance. After rounding tn,
recalculate required wall at the resulting larger outside diameter. This is a
straight-pipe pressure calculation; it does not size bends, branches or nozzles.

¢` function Wall(D, P, Se, y, A, m)
  if D <= 0 'm' throw "Bore must be positive"
  if P <= 0 'Pa' or Se <= 0 'Pa' throw "Pressure and effective stress must be positive"
  if y < 0 or y > 1 throw "Screening coefficient must be between zero and one"
  if A < 0 'm' throw "Allowance cannot be negative"
  if m < 0 or m >= 1 throw "Tolerance must be between zero and one, excluding one"
  alpha = P / (2 * (Se + P * y))
  denominator = 1 - m - 2 * alpha
  if denominator <= 0 throw "Invalid pressure and effective-stress combination"
  return (alpha * D + A) / denominator
end `

¢??` RequiredNominal = Wall(Bore, DesignPressure, EffectiveStress,
PressureCoefficient, Allowance, NegativeTolerance) = 〔20.03944〕 mm `

¢??` NominalWall = ceil(RequiredNominal / WallStep) * WallStep = 〔25〕 mm `

¢??` Outside = Bore + 2 * NominalWall = 〔1.475〕 m `

¢??` DeliveredMinimum = (1 - NegativeTolerance) * NominalWall = 〔21.875〕 mm `

¢??` RequiredMinimum = DesignPressure * Outside / (2 * (EffectiveStress +
DesignPressure * PressureCoefficient)) + Allowance = 〔17.63294〕 mm `

¢??` WallMargin = DeliveredMinimum - RequiredMinimum = 〔4.242063〕 mm `

¢??` NetPressureWall = DeliveredMinimum - Allowance = 〔18.875〕 mm `

¢??` PressureCapacity = 2 * EffectiveStress * NetPressureWall / (Outside - 2 *
PressureCoefficient * NetPressureWall) = 〔1.292897〕 MPa `

¢??` PressureCheck = (WallMargin >= 0 'mm') and (PressureCapacity >=
DesignPressure) = 〔true〕 `

The calculated pressure capacity applies only to this equation and these
assumptions. It is not an assigned maximum allowable working pressure for the
assembled system. The pressure-check flag addresses only the straight-pipe
internal-pressure wall requirement. No mechanical adequacy is implied by
rounding 20.04 mm to 25 mm. Pipe tolerances must also preserve the required
clear bore.

## 4. Sensitivities

Hold the calculated bore and other assumptions fixed. Pressure cases are gauge
pressures. Values below are nominal wall requirements before 5 mm rounding;
compare these with the base-case 25 mm wall. A higher pressure or lower
effective stress may require a thicker wall.

¢??` WallAtHalfMPa = Wall(Bore, 0.5 'MPa', EffectiveStress, PressureCoefficient,
Allowance, NegativeTolerance) = 〔11.67185〕 mm `

¢??` WallAtOneMPa = Wall(Bore, 1 'MPa', EffectiveStress, PressureCoefficient,
Allowance, NegativeTolerance) = 〔20.03944〕 mm `

¢??` WallAtTwoMPa = Wall(Bore, 2 'MPa', EffectiveStress, PressureCoefficient,
Allowance, NegativeTolerance) = 〔37.15901〕 mm `

¢??` WallAtStress30 = Wall(Bore, DesignPressure, 30 'MPa', PressureCoefficient,
Allowance, NegativeTolerance) = 〔31.39453〕 mm `

¢??` WallAtStress50 = Wall(Bore, DesignPressure, 50 'MPa', PressureCoefficient,
Allowance, NegativeTolerance) = 〔20.03944〕 mm `

¢??` WallAtStress80 = Wall(Bore, DesignPressure, 80 'MPa', PressureCoefficient,
Allowance, NegativeTolerance) = 〔13.75198〕 mm `

## 5. Insulated layout envelope

The [coolant insulation worksheet][6] estimates 400 mm radial insulation hot and
350 mm on the return, with 400 mm on both as an option. That worksheet used a
provisional 1.5 m bare OD. The base wall estimate here gives 1.475 m bare OD,
which fits within that thermal envelope. Retain the previously reserved 2.3 m
hot / 2.2 m return layout space until dimensions and installation details
settle. Values below show metal plus insulation only: cladding, tracing, bands,
supports and installation clearance are additional. Thermal performance is not
recomputed here; revisit the thermal worksheet if material or dimensions change
appreciably.

¢` HotInsulation = 400 mm `

¢` ColdInsulation = 350 mm `

¢??` HotInsulatedOutside = Outside + 2 * HotInsulation = 〔2.275〕 m `

¢??` ColdInsulatedOutside = Outside + 2 * ColdInsulation = 〔2.175〕 m `

¢??` CommonInsulation = max(HotInsulation, ColdInsulation) = 〔400〕 mm `

¢??` CommonInsulatedOutside = Outside + 2 * CommonInsulation = 〔2.275〕 m `

## 6. What remains before construction sizing

*   Establish design pressure and temperature, including cover-gas pressure, local
    static head, pump shutoff, relief/isolation and steam-generator
    tube-failure conditions.
*   Select a salt-compatible alloy, product form and weld procedure. Confirm
    applicable allowable stress, high-temperature weld factors, creep life and
    corrosion/erosion allowance against the actual chloride salt chemistry.
*   Check weight of pipe, contained salt and insulation, support spans, local
    support loads, seismic and other imposed loads, and load transfer to equipment.
*   Check restrained thermal expansion, flexibility, fatigue and creep interaction;
    thicker walls do not automatically resolve those loads.
*   Check external pressure/vacuum buckling, ovality, handling and fabrication;
    pressure-only thickness does not establish stability of a large-diameter pipe.
*   Size elbows, branches, reducers, flanges, nozzles and weld details, and
    establish examination, testing, procurement tolerances and minimum
    delivered bore.

Thus **25 mm is a conditional concept-model wall**, not a verified construction
thickness. The worksheet does not change the graphics or approve a pressure
rating. See the [verification record][7] for independent checks and
reproduction.

[1]: Coolant%20pump%20estimate%20-%20Hurmet.md

[2]: Generator%20sizing%20-%20Hurmet.md

[3]: Steam%20and%20feedwater%20pipe%20sizing%20-%20Hurmet.md

[4]: https://engstandards.lanl.gov/esm/pressure\_safety/Chapter17-entire.pdf

[5]: https://www.asme.org/codes-standards/find-codes-standards/b31-1-power-piping

[6]: Molten-salt%20coolant%20insulation%20-%20Hurmet.md

[7]: molten-salt-wall-check.md

[8]: https://engstandards.lanl.gov/esm/pressure_safety/Chapter17-entire.pdf
