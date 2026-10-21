---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Steam and feedwater pipe sizing

¢` format = "h3" `

Preliminary estimate — 11 October 2026. Four sizes: one-generator steam and
feedwater branches, and their three-generator common headers. The owner
approved provisional design-pressure and material-stress assumptions. This
sheet calculates hydraulic bores and pressure-only straight-pipe walls; it is
not a purchase specification or a completed code design. No graphics are
changed.

Open this file in Hurmet and recalculate after changing inputs. All displayed
results below are live calculations. Bore sizes are rounded to 25 mm increments
and nominal walls to 5 mm increments, representing custom dimensional
envelopes, not standard pipe schedules. Both bore and wall must be reconciled
with available products and their actual dimensional tolerances.

## 1. Duty and properties

The source is [Generator sizing — Hurmet][1]. Properties are copied at 24 MPa
absolute, 830 K steam outlet and 560 K feedwater inlet. They do not update with
pressure or temperature: when operating conditions change, update enthalpies,
densities and viscosities from IAPWS as well.

¢` ReactorDuty = 1500 MW `

¢` GeneratorCount = 3 `

¢` OperatingPressure = 24 'MPa' `

¢` SteamTemperature = 830 K `

¢` WaterTemperature = 560 K `

¢` SteamEnthalpy = 3372.493 kJ/kg `

¢` WaterEnthalpy = 1264.452 kJ/kg `

¢` SteamDensity = 73.6086493 kg/m3 `

¢` WaterDensity = 764.494 kg/m3 `

¢` SteamViscosity = 0.00003392 Pa*s `

¢` WaterViscosity = 0.00009635 Pa*s `

¢%%` GeneratorDuty = ReactorDuty / GeneratorCount = 〔500〕 MW `

¢%%` BranchMass = GeneratorDuty / (SteamEnthalpy - WaterEnthalpy) = 〔237〕 kg/s `

¢%%` HeaderMass = GeneratorCount * BranchMass = 〔712〕 kg/s `

¢%%` SteamBranchFlow = BranchMass / SteamDensity = 〔3.22〕 m3/s `

¢%%` SteamHeaderFlow = HeaderMass / SteamDensity = 〔9.67〕 m3/s `

¢%%` WaterBranchFlow = BranchMass / WaterDensity = 〔0.31〕 m3/s `

¢%%` WaterHeaderFlow = HeaderMass / WaterDensity = 〔0.931〕 m3/s `

## 2. Editable hydraulic assumptions

Velocity limits are screening choices, not code limits. The 3 m/s feedwater
limit is a new assumption, independent of the earlier molten-salt limit.
Lengths and fitting-loss sums below are provisional external-piping budgets,
not measured routes. Each full header is conservatively evaluated at all three
generators' flow; actual segment flow reduces after each water takeoff or
before each steam junction. Internal generator/collector losses and turbine
equipment are excluded. Valve K values must eventually come from the selected
valves.

¢` SteamVelocityLimit = 25 m/s `

¢` WaterVelocityLimit = 3 m/s `

¢` BranchLength = 15 'm' `

¢` HeaderLength = 90 'm' `

¢` BranchK = 6 `

¢` HeaderK = 10 `

¢` BranchLossLimit = 150 kPa `

¢` HeaderLossLimit = 250 kPa `

¢` Roughness = 0.045 'mm' `

¢` BoreStep = 25 'mm' `

## 3. Hydraulic equations

Darcy-Weisbach with local losses; the friction factor is the Darcy factor,
computed by iterating the Colebrook equation. The laminar branch is included,
but results in the transitional Reynolds-number range require review. A bounded
bisection solves for the bore meeting the pressure-loss budget. The larger of
the velocity bore and pressure-loss bore is rounded upward.

¢` function Speed(Q, D)
    return 4 * Q / (pi * D^2)
end `

¢` function Darcy(Q, D, rho, mu, rough)
    rey = rho * (4 * Q / (pi * D^2)) * D / mu
    if rey <= 0 throw "Flow must be positive"
    if rey < 2300 return 64 / rey
    if rey < 4000 throw "Transitional flow: review friction model"
    x = 8
    for i in 1:30
        x = -2 * ln(rough / (3.7 * D) + 2.51 * x / rey) / ln(10)
    end
    return 1 / x^2
end `

¢` function Loss(friction, Q, D, rho, mu, L, Ksum, rough)
    return (friction(Q, D, rho, mu, rough) * L / D + Ksum) * rho * (4 * Q / (pi * D^2))^2 / 2
end `

¢` function LossBore(loss, friction, Q, rho, mu, L, Ksum, rough, limit)
    if Q <= 0 'm3/s' throw "Flow must be positive"
    if limit <= 0 'Pa' throw "Loss budget must be positive"
    if L < 0 'm' throw "Length must not be negative"
    if Ksum < 0 throw "K must not be negative"
    lo = 0.025 'm'
    hi = 5 'm'
    if loss(friction, Q, hi, rho, mu, L, Ksum, rough) > limit throw "Increase upper bore bound"
    for i in 1:50
        mid = (lo + hi) / 2
        if loss(friction, Q, mid, rho, mu, L, Ksum, rough) > limit
            lo = mid
        else
            hi = mid
        end
    end
    return hi
end `

## 4. Hydraulic sizes

SB = steam branch; SH = steam common header; WB = water branch; WH = water
common header. These are clean, nominal internal bores.

### Steam branch

¢%%` SBVelocityBore = sqrt(4 * SteamBranchFlow / (pi * SteamVelocityLimit)) =
〔405〕 mm `

¢%%` SBLossBore = LossBore(Loss, Darcy, SteamBranchFlow, SteamDensity,
SteamViscosity, BranchLength, BranchK, Roughness, BranchLossLimit) = 〔404〕 mm `

¢%%` SBBore = ceil(max(SBVelocityBore, SBLossBore) / BoreStep) * BoreStep =
〔425〕 mm `

¢%%` SBVelocity = Speed(SteamBranchFlow, SBBore) = 〔22.7〕 m/s `

¢%%` SBReynolds = SteamDensity * SBVelocity * SBBore / SteamViscosity =
〔20,948,662〕 `

¢%%` SBFriction = Darcy(SteamBranchFlow, SBBore, SteamDensity, SteamViscosity,
Roughness) = 〔0.0122〕 `

¢%%` SBLoss = Loss(Darcy, SteamBranchFlow, SBBore, SteamDensity, SteamViscosity,
BranchLength, BranchK, Roughness) = 〔122〕 kPa `

¢%%` SBHydraulicOK = (SBVelocity <= SteamVelocityLimit) and (SBLoss <=
BranchLossLimit) = 〔true〕 `

### Steam header

¢%%` SHVelocityBore = sqrt(4 * SteamHeaderFlow / (pi * SteamVelocityLimit)) =
〔702〕 mm `

¢%%` SHLossBore = LossBore(Loss, Darcy, SteamHeaderFlow, SteamDensity,
SteamViscosity, HeaderLength, HeaderK, Roughness, HeaderLossLimit) = 〔710〕 mm `

¢%%` SHBore = ceil(max(SHVelocityBore, SHLossBore) / BoreStep) * BoreStep =
〔725〕 mm `

¢%%` SHVelocity = Speed(SteamHeaderFlow, SHBore) = 〔23.4〕 m/s `

¢%%` SHReynolds = SteamDensity * SHVelocity * SHBore / SteamViscosity =
〔36,840,751〕 `

¢%%` SHFriction = Darcy(SteamHeaderFlow, SHBore, SteamDensity, SteamViscosity,
Roughness) = 〔0.011〕 `

¢%%` SHLoss = Loss(Darcy, SteamHeaderFlow, SHBore, SteamDensity, SteamViscosity,
HeaderLength, HeaderK, Roughness) = 〔229〕 kPa `

¢%%` SHHydraulicOK = (SHVelocity <= SteamVelocityLimit) and (SHLoss <=
HeaderLossLimit) = 〔true〕 `

### Water branch

¢%%` WBVelocityBore = sqrt(4 * WaterBranchFlow / (pi * WaterVelocityLimit)) =
〔363〕 mm `

¢%%` WBLossBore = LossBore(Loss, Darcy, WaterBranchFlow, WaterDensity,
WaterViscosity, BranchLength, BranchK, Roughness, BranchLossLimit) = 〔229〕 mm `

¢%%` WBBore = ceil(max(WBVelocityBore, WBLossBore) / BoreStep) * BoreStep =
〔375〕 mm `

¢%%` WBVelocity = Speed(WaterBranchFlow, WBBore) = 〔2.81〕 m/s `

¢%%` WBReynolds = WaterDensity * WBVelocity * WBBore / WaterViscosity =
〔8,358,302〕 `

¢%%` WBFriction = Darcy(WaterBranchFlow, WBBore, WaterDensity, WaterViscosity,
Roughness) = 〔0.0126〕 `

¢%%` WBLoss = Loss(Darcy, WaterBranchFlow, WBBore, WaterDensity, WaterViscosity,
BranchLength, BranchK, Roughness) = 〔19.6〕 kPa `

¢%%` WBHydraulicOK = (WBVelocity <= WaterVelocityLimit) and (WBLoss <=
BranchLossLimit) = 〔true〕 `

### Water header

¢%%` WHVelocityBore = sqrt(4 * WaterHeaderFlow / (pi * WaterVelocityLimit)) =
〔629〕 mm `

¢%%` WHLossBore = LossBore(Loss, Darcy, WaterHeaderFlow, WaterDensity,
WaterViscosity, HeaderLength, HeaderK, Roughness, HeaderLossLimit) = 〔407〕 mm `

¢%%` WHBore = ceil(max(WHVelocityBore, WHLossBore) / BoreStep) * BoreStep =
〔650〕 mm `

¢%%` WHVelocity = Speed(WaterHeaderFlow, WHBore) = 〔2.8〕 m/s `

¢%%` WHReynolds = WaterDensity * WHVelocity * WHBore / WaterViscosity =
〔14,466,293〕 `

¢%%` WHFriction = Darcy(WaterHeaderFlow, WHBore, WaterDensity, WaterViscosity,
Roughness) = 〔0.0114〕 `

¢%%` WHLoss = Loss(Darcy, WaterHeaderFlow, WHBore, WaterDensity, WaterViscosity,
HeaderLength, HeaderK, Roughness) = 〔34.8〕 kPa `

¢%%` WHHydraulicOK = (WHVelocity <= WaterVelocityLimit) and (WHLoss <=
HeaderLossLimit) = 〔true〕 `

The totals are branch plus a full-flow header bound, not a balanced network
solution. Constant-density steam treatment is an estimate at these small
pressure-loss fractions; larger losses require changing-property analysis.

¢%%` SteamPathLoss = SBLoss + SHLoss = 〔352〕 kPa `

¢%%` WaterPathLoss = WBLoss + WHLoss = 〔54.4〕 kPa `

¢%%` SteamLossFraction = SteamPathLoss / OperatingPressure = 〔0.0146〕 `

## 5. Pressure-wall assumptions

Design pressure is **30 MPa gauge** for both services, provisionally selected
above the 24 MPa absolute property basis. It is not a demonstrated maximum:
confirm pump shutoff, static head, relief settings and transient envelopes.
Design metal temperatures are provisionally 600°C steam and 325°C water.

**No material grade has been selected.** Stress values below are numerical
assumptions, not extracted allowable stresses for a named alloy. Replace them
with the adopted code's values at design temperature, including time-dependent
limits where applicable. Changing temperature alone does not update stress or

 y.  The displayed thicknesses are conditional on these assumptions.


¢` SteamDesignPressure = 30 'MPa' `

¢` WaterDesignPressure = 30 'MPa' `

¢` SteamDesignTemperature = 873.15 K `

¢` WaterDesignTemperature = 598.15 K `

¢` SteamStress = 80 'MPa' `

¢` WaterStress = 120 'MPa' `

Seamless construction is assumed for this preliminary case: E = W = 1.
Feasibility of obtaining large seamless sections is not established. Welded
construction needs its applicable efficiency and elevated-temperature
reduction. Here S excludes E; do not enter an SE table value and apply E a
second time. The y values use a provisional ferritic-steel category; they must
follow the selected material, temperature and governing edition.

¢` SteamE = 1 `

¢` WaterE = 1 `

¢` SteamW = 1 `

¢` WaterW = 1 `

¢` SteamY = 0.7 `

¢` WaterY = 0.4 `

Allowances are provisional: 3 mm total corrosion/erosion/mechanical allowance,
12.5% negative wall tolerance, zero OD tolerance in this dimensional envelope.
Positive wall tolerance can reduce delivered bore and must be checked
separately. Insulation is not part of metal wall thickness or the OD calculated here.

¢` Allowance = 3 'mm' `

¢` MillTolerance = 0.125 `

¢` WallStep = 5 'mm' `

## 6. Pressure-thickness calculation

ASME B31.1-2020 §104.1.2(a), equation (7), is used as the preliminary straight
circular-pipe pressure relation \[2]. Applicable jurisdiction, code edition and
nuclear classification remain to be established; this is not code certification.

For outside diameter Do, minimum delivered wall is P Do / (2 (S E W + P y)) plus
allowance. Nominal wall must cover mill under-tolerance. Since bore D is
selected first, Do = D + 2 tn must be solved simultaneously. Thus, with alpha =
P / (2 (S E W + P y)), tn = (alpha D + A)/(1 - m - 2 alpha). Rounding tn upward
also increases Do, so the final dimensions are rechecked using equation (7),
not just the pre-rounding thickness.

¢` function NominalWall(D, P, S, E, W, y, A, tol)
    if D <= 0 'm' throw "Bore must be positive"
    if P <= 0 'Pa' throw "Pressure must be positive"
    if S <= 0 'Pa' throw "Stress must be positive"
    if E <= 0 or E > 1 throw "E must be in (0,1]"
    if W <= 0 or W > 1 throw "W must be in (0,1]"
    if A < 0 'm' throw "Allowance must not be negative"
    if tol < 0 or tol >= 1 throw "Tolerance must be in [0,1)"
    alpha = P / (2 * (S * E * W + P * y))
    denominator = 1 - tol - 2 * alpha
    if denominator <= 0 throw "Invalid pressure/stress combination"
    return (alpha * D + A) / denominator
end `

### Steam branch wall

¢%%` SBRequiredNominal = NominalWall(SBBore, SteamDesignPressure, SteamStress,
SteamE, SteamW, SteamY, Allowance, MillTolerance) = 〔114〕 mm `

¢%%` SBWall = ceil(SBRequiredNominal / WallStep) * WallStep = 〔115〕 mm `

¢%%` SBOD = SBBore + 2 * SBWall = 〔655〕 mm `

¢%%` SBRequiredMinimum = SteamDesignPressure * SBOD / (2 * (SteamStress *
SteamE * SteamW + SteamDesignPressure * SteamY)) + Allowance = 〔100〕 mm `

¢%%` SBDeliveredMinimum = (1 - MillTolerance) * SBWall = 〔101〕 mm `

¢%%` SBWallMargin = SBDeliveredMinimum - SBRequiredMinimum = 〔0.348〕 mm `

¢%%` SBPressureCapacity = 2 * SteamStress * SteamE * SteamW *
(SBDeliveredMinimum - Allowance) / (SBOD - 2 * SteamY * (SBDeliveredMinimum -
Allowance)) = 〔30.1〕 MPa `

¢%%` SBPressureOK = (SBWallMargin >= 0 'mm') and (SBPressureCapacity >=
SteamDesignPressure) = 〔true〕 `

### Steam header wall

¢%%` SHRequiredNominal = NominalWall(SHBore, SteamDesignPressure, SteamStress,
SteamE, SteamW, SteamY, Allowance, MillTolerance) = 〔191〕 mm `

¢%%` SHWall = ceil(SHRequiredNominal / WallStep) * WallStep = 〔195〕 mm `

¢%%` SHOD = SHBore + 2 * SHWall = 〔1,115〕 mm `

¢%%` SHRequiredMinimum = SteamDesignPressure * SHOD / (2 * (SteamStress *
SteamE * SteamW + SteamDesignPressure * SteamY)) + Allowance = 〔169〕 mm `

¢%%` SHDeliveredMinimum = (1 - MillTolerance) * SHWall = 〔171〕 mm `

¢%%` SHWallMargin = SHDeliveredMinimum - SHRequiredMinimum = 〔2.03〕 mm `

¢%%` SHPressureCapacity = 2 * SteamStress * SteamE * SteamW *
(SHDeliveredMinimum - Allowance) / (SHOD - 2 * SteamY * (SHDeliveredMinimum -
Allowance)) = 〔30.5〕 MPa `

¢%%` SHPressureOK = (SHWallMargin >= 0 'mm') and (SHPressureCapacity >=
SteamDesignPressure) = 〔true〕 `

### Water branch wall

¢%%` WBRequiredNominal = NominalWall(WBBore, WaterDesignPressure, WaterStress,
WaterE, WaterW, WaterY, Allowance, MillTolerance) = 〔70.4〕 mm `

¢%%` WBWall = ceil(WBRequiredNominal / WallStep) * WallStep = 〔75〕 mm `

¢%%` WBOD = WBBore + 2 * WBWall = 〔525〕 mm `

¢%%` WBRequiredMinimum = WaterDesignPressure * WBOD / (2 * (WaterStress *
WaterE * WaterW + WaterDesignPressure * WaterY)) + Allowance = 〔62.7〕 mm `

¢%%` WBDeliveredMinimum = (1 - MillTolerance) * WBWall = 〔65.6〕 mm `

¢%%` WBWallMargin = WBDeliveredMinimum - WBRequiredMinimum = 〔2.97〕 mm `

¢%%` WBPressureCapacity = 2 * WaterStress * WaterE * WaterW *
(WBDeliveredMinimum - Allowance) / (WBOD - 2 * WaterY * (WBDeliveredMinimum -
Allowance)) = 〔31.6〕 MPa `

¢%%` WBPressureOK = (WBWallMargin >= 0 'mm') and (WBPressureCapacity >=
WaterDesignPressure) = 〔true〕 `

### Water header wall

¢%%` WHRequiredNominal = NominalWall(WHBore, WaterDesignPressure, WaterStress,
WaterE, WaterW, WaterY, Allowance, MillTolerance) = 〔119〕 mm `

¢%%` WHWall = ceil(WHRequiredNominal / WallStep) * WallStep = 〔120〕 mm `

¢%%` WHOD = WHBore + 2 * WHWall = 〔890〕 mm `

¢%%` WHRequiredMinimum = WaterDesignPressure * WHOD / (2 * (WaterStress *
WaterE * WaterW + WaterDesignPressure * WaterY)) + Allowance = 〔104〕 mm `

¢%%` WHDeliveredMinimum = (1 - MillTolerance) * WHWall = 〔105〕 mm `

¢%%` WHWallMargin = WHDeliveredMinimum - WHRequiredMinimum = 〔0.864〕 mm `

¢%%` WHPressureCapacity = 2 * WaterStress * WaterE * WaterW *
(WHDeliveredMinimum - Allowance) / (WHOD - 2 * WaterY * (WHDeliveredMinimum -
Allowance)) = 〔30.3〕 MPa `

¢%%` WHPressureOK = (WHWallMargin >= 0 'mm') and (WHPressureCapacity >=
WaterDesignPressure) = 〔true〕 `

## 7. Dimension summary

All dimensions below are calculated envelopes. Pressure checks mean only that
the assumed straight-pipe relation is satisfied. The present Blender pipes are
not automatically updated from this worksheet.

+--------------+--------------------------+--------------------------+--------------------------+--------------------------+
| Service      | Bore (mm)                | Nominal wall (mm)        | Bare OD (mm)             | Velocity (m/s)           |
+==============+=========================:+=========================:+=========================:+=========================:+
| Steam branch | ¢%%` SBBore = 〔425〕 mm ` | ¢%%` SBWall = 〔115〕 mm ` | ¢%%` SBOD = 〔655〕 mm `   | ¢%%` SBVelocity = 〔22.7〕 |
|              |                          |                          |                          | m/s `                    |
+--------------+--------------------------+--------------------------+--------------------------+--------------------------+
| Steam header | ¢%%` SHBore = 〔725〕 mm ` | ¢%%` SHWall = 〔195〕 mm ` | ¢%%` SHOD = 〔1,115〕 mm ` | ¢%%` SHVelocity = 〔23.4〕 |
|              |                          |                          |                          | m/s `                    |
+--------------+--------------------------+--------------------------+--------------------------+--------------------------+
| Water branch | ¢%%` WBBore = 〔375〕 mm ` | ¢%%` WBWall = 〔75〕 mm `  | ¢%%` WBOD = 〔525〕 mm `   | ¢%%` WBVelocity = 〔2.81〕 |
|              |                          |                          |                          | m/s `                    |
+--------------+--------------------------+--------------------------+--------------------------+--------------------------+
| Water header | ¢%%` WHBore = 〔650〕 mm ` | ¢%%` WHWall = 〔120〕 mm ` | ¢%%` WHOD = 〔890〕 mm `   | ¢%%` WHVelocity = 〔2.8〕  |
|              |                          |                          |                          | m/s `                    |
+--------------+--------------------------+--------------------------+--------------------------+--------------------------+
{.c2r}

## 8. Sensitivity and comparison

Stress sensitivity keeps the calculated steam-header bore and all other inputs
fixed. Values are unrounded nominal wall requirements. These stress cases do
not imply that a particular grade meets them at 600°C.

¢%%` SHWallAt60 = NominalWall(SHBore, SteamDesignPressure, 60 'MPa', SteamE,
SteamW, SteamY, Allowance, MillTolerance) = 〔272〕 mm `

¢%%` SHWallAt80 = NominalWall(SHBore, SteamDesignPressure, 80 'MPa', SteamE,
SteamW, SteamY, Allowance, MillTolerance) = 〔191〕 mm `

¢%%` SHWallAt100 = NominalWall(SHBore, SteamDesignPressure, 100 'MPa', SteamE,
SteamW, SteamY, Allowance, MillTolerance) = 〔148〕 mm `

¢%%` SHWallAtOperating = NominalWall(SHBore, 24 'MPa', SteamStress, SteamE,
SteamW, SteamY, Allowance, MillTolerance) = 〔148〕 mm `

The 24 MPa case above is a pressure sensitivity using 24 MPa gauge for
comparison; it does not replace design pressure with operating pressure. For
comparison only, treating the original graphical 0.8 m steam and 0.5 m water
diameters as bores gives:

¢%%` OriginalSteamHeaderVelocity = Speed(SteamHeaderFlow, 0.8 'm') = 〔19.2〕 m/s `

¢%%` OriginalWaterHeaderVelocity = Speed(WaterHeaderFlow, 0.5 'm') = 〔4.74〕 m/s `

## 9. Boundaries of this estimate

The nominal bore must be guaranteed after tolerances; final selection starts
from available OD/wall dimensions and repeats these checks. No standard NPS,
schedule, material grade, fitting or valve rating is selected here. Straight
pipe walls do not establish the strength of the D-shaped collectors, casing,
tees, nozzles, bends, closures or flanges. Thermal expansion, deadweight,
supports, seismic loads, fatigue, creep qualification, water hammer, external
pressure and testing remain separate design work. Feedwater design pressure
must ultimately include pump shutoff and other credible operating states.

The original generator worksheet and graphics remain unchanged. The 17 m casing
model does not revise the worksheet's internal generator calculations.

## References and verification

1.  [Generator sizing — Hurmet][1]: enthalpies, density and viscosity retained from
   the preliminary Calca conversion.
2.  ASME B31.1-2020, §104.1.2(a), equations (7) and (9), and Table 104.1.2-1. [ASME
   publication page][2]. The 2020 equation was checked in the [ASME-authored
   text][3]. The governing edition has not been selected; no allowable-stress
   table is reproduced.
3.  [IAPWS industrial formulation][4]: source to use when replacing the inherited
   water/steam property inputs.
4.  [Spirax Sarco pipe sizing][5]: velocity and pressure loss both matter; worksheet
   limits are our assumptions.
5.  [Numerical verification and reproduction][6].


Equations are recalculated using Hurmet and independently checked in SI units.

[1]: Generator%20sizing%20-%20Hurmet.md

[2]: https://www.asme.org/codes-standards/find-codes-standards/b31-1-power-piping

[3]: https://www.ipgmservicios.com/wp-content/uploads/2024/03/ASME-B31.1-2020-Power-Piping.pdf#page=48

[4]: https://www.iapws.org/relguide/IF97-Rev.html

[5]: https://www.spiraxsarco.com/learn-about-steam/steam-distribution/pipes-and-pipe-sizing?sc\\\\\\\\\\\\\\\_lang=en-GB

[6]: steam-water-pipe-check.md

[7]: https://www.spiraxsarco.com/learn-about-steam/steam-distribution/pipes-and-pipe-sizing?sc\\\\\\\_lang=en-GB

[8]: https://www.spiraxsarco.com/learn-about-steam/steam-distribution/pipes-and-pipe-sizing?sc\\\_lang=en-GB

[9]: https://www.spiraxsarco.com/learn-about-steam/steam-distribution/pipes-and-pipe-sizing?sc\_lang=en-GB
