---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Steam and feedwater pipe insulation

¢` format = "h3" `

Preliminary layout estimate — 11 October 2026. Allow **350 mm radial insulation
on steam pipes and 175 mm on feedwater pipes**, conditional on the inputs
below. These thicknesses cover both branch and header sizes at the provisional
design temperatures. This is a steady-state straight-pipe thermal estimate, not
an approved insulation specification or an economic optimum. Pressure
containment is provided by the pipe wall; insulation is sized for heat transfer.

Open in Hurmet to edit and recalculate. Saved results are live calculation
cells. Inputs copied from the [pipe-sizing worksheet][1] are not automatically
linked. Revise outside diameters if pressure-wall assumptions change. The
graphics have not been resized by this calculation.

## Inputs and screening criteria

The bare outside diameters include the provisional pressure walls, not just the
hydraulic bore. Operating temperatures are 830 K steam (556.85°C) and 560 K
feedwater (286.85°C). Check temperatures are the previous worksheet's
provisional 600°C steam and 325°C feedwater design temperatures. A uniform
thickness per service is selected using the larger requirement of its branch
and header, rounded upward to 25 mm. These are planning increments, not
available stock sizes.

¢` SteamOperating = 830 K `

¢` WaterOperating = 560 K `

¢` SteamCheck = 873.15 K `

¢` WaterCheck = 598.15 K `

¢` SBOutside = 655 mm `

¢` SHOutside = 1115 mm `

¢` WBOutside = 525 mm `

¢` WHOutside = 890 mm `

The room air and mean radiant surroundings are both assumed to be 40°C. External
convection is provisionally 4 W/(m² K), representing modest indoor natural
convection; it is an editable coefficient, not a calculated air-flow
correlation. Jacket emissivity is assumed 0.20, with sensitivity at 0.10.
Actual finish, oxidation, orientation, air movement and adjacent equipment must
be checked. The 60°C jacket target is a screening criterion, not assurance of
safe contact: burn risk also depends on surface material and duration of
contact ([NIA][2]).

¢` Ambient = 313.15 K `

¢` SurfaceLimit = 333.15 K `

¢` Convection = 4 W/m2/K `

¢` Emissivity = 0.20 `

¢` Sigma = 0.00000005670374419 W/m2/K4 `

¢` ThicknessStep = 25 mm `

### Candidate insulation

Use dry calcium silicate with a protective metal jacket as the provisional
material. [JM Thermo-1200][3] is one reference product, rated up to 650°C. Its
published pipe-test conductivity is 0.070 W/(m K) at 204°C mean temperature,
0.085 at 316°C and 0.093 at 371°C. Rounded effective conductivities of 0.090
for steam and 0.075 for water are used here. They exceed interpolated
manufacturer values at the base-case mean insulation temperatures
(approximately 328°C and 191°C at the design check). These fixed effective
values are screening assumptions, not a fit valid at all temperatures. Revisit
them when temperatures, material, moisture or aging change. No integration of
apparent pipe-test values as local material conductivity is implied.

¢` SteamConductivity = 0.090 W/m/K `

¢` WaterConductivity = 0.075 W/m/K `

## Heat balance and thickness solver

For bare pipe outside diameter D, insulation thickness t and jacket temperature
Ts, radial conduction per metre is 2πk(Tp − Ts)/ln((D + 2t)/D). External loss
is π(D + 2t)\[h(Ts − Ta) + εσ(Ts⁴ − Ta⁴)]. Absolute temperatures are used in
radiation. Solve these expressions for equal heat flow. For minimum thickness,
hold Ts at the target and solve for t. The 1 mm–1 m thickness bracket is
checked explicitly.

The pipe's outside steel surface is taken at fluid temperature, omitting steel
and internal-film resistances. Jacket resistance is neglected. Insulation is
continuous and dry; joints, valves, flanges, hangers, penetrations and thermal
bridges are excluded. Radiation sees surroundings at room temperature with
unity effective view factor; nearby hot equipment can invalidate that
assumption.

¢` function Minimum(D, Tp, Ta, Ts, k, h, e, sigma)
  if D <= 0 'm' throw "Diameter must be positive"
  if k <= 0 'W/m/K' throw "Conductivity must be positive"
  if h <= 0 'W/m2/K' throw "Convection must be positive"
  if e < 0 or e > 1 throw "Emissivity must be between zero and one"
  if Ta >= Ts or Ts >= Tp throw "Require ambient below target below pipe temperature"
  low = 0.001 'm'
  high = 1 'm'
  flux = h * (Ts - Ta) + e * sigma * (Ts^4 - Ta^4)
  if 2 * k * (Tp - Ts) / ln((D + 2 * high) / D) > (D + 2 * high) * flux throw "Thickness exceeds one metre"
  if 2 * k * (Tp - Ts) / ln((D + 2 * low) / D) <= (D + 2 * low) * flux return low
  for i in 1:55
    mid = (low + high) / 2
    if 2 * k * (Tp - Ts) / ln((D + 2 * mid) / D) > (D + 2 * mid) * flux
      low = mid
    else
      high = mid
    end
  end
  return high
end `

¢` function Surface(D, t, Tp, Ta, k, h, e, sigma)
  if D <= 0 'm' or t <= 0 'm' throw "Diameters and thickness must be positive"
  if k <= 0 'W/m/K' or h <= 0 'W/m2/K' throw "Thermal coefficients must be positive"
  if e < 0 or e > 1 throw "Emissivity must be between zero and one"
  if Tp <= Ta throw "Hot pipe must exceed ambient temperature"
  low = Ta
  high = Tp
  for i in 1:55
    mid = (low + high) / 2
    inside = 2 * k * (Tp - mid) / ln((D + 2 * t) / D)
    outside = (D + 2 * t) * (h * (mid - Ta) + e * sigma * (mid^4 - Ta^4))
    if inside > outside
      low = mid
    else
      high = mid
    end
  end
  return (low + high) / 2
end `

## Required thickness and layout choice

SB = steam branch, SH = steam header, WB = feedwater branch, WH = feedwater
header. The operating-only minima show how much the higher check temperatures add.

¢%%` SBOperatingMinimum = Minimum(SBOutside, SteamOperating, Ambient,
SurfaceLimit, SteamConductivity, Convection, Emissivity, Sigma) = 〔298〕 mm `

¢%%` SBCheckMinimum = Minimum(SBOutside, SteamCheck, Ambient, SurfaceLimit,
SteamConductivity, Convection, Emissivity, Sigma) = 〔319〕 mm `

¢%%` SHOperatingMinimum = Minimum(SHOutside, SteamOperating, Ambient,
SurfaceLimit, SteamConductivity, Convection, Emissivity, Sigma) = 〔324〕 mm `

¢%%` SHCheckMinimum = Minimum(SHOutside, SteamCheck, Ambient, SurfaceLimit,
SteamConductivity, Convection, Emissivity, Sigma) = 〔348〕 mm `

¢%%` WBOperatingMinimum = Minimum(WBOutside, WaterOperating, Ambient,
SurfaceLimit, WaterConductivity, Convection, Emissivity, Sigma) = 〔127〕 mm `

¢%%` WBCheckMinimum = Minimum(WBOutside, WaterCheck, Ambient, SurfaceLimit,
WaterConductivity, Convection, Emissivity, Sigma) = 〔145〕 mm `

¢%%` WHOperatingMinimum = Minimum(WHOutside, WaterOperating, Ambient,
SurfaceLimit, WaterConductivity, Convection, Emissivity, Sigma) = 〔135〕 mm `

¢%%` WHCheckMinimum = Minimum(WHOutside, WaterCheck, Ambient, SurfaceLimit,
WaterConductivity, Convection, Emissivity, Sigma) = 〔155〕 mm `

¢%%` SteamThickness = ceil(max(SBCheckMinimum, SHCheckMinimum) /
ThicknessStep) * ThicknessStep = 〔350〕 mm `

¢%%` WaterThickness = ceil(max(WBCheckMinimum, WHCheckMinimum) /
ThicknessStep) * ThicknessStep = 〔175〕 mm `

## Performance with the selected insulation

Jacket diameters omit thin metal cladding, bands, supports and installation
clearance.

### Steam branch

¢%%` SBJacket = SBOutside + 2 * SteamThickness = 〔1,355〕 mm `

¢%%` SBOperatingSurface = Surface(SBOutside, SteamThickness, SteamOperating,
Ambient, SteamConductivity, Convection, Emissivity, Sigma) = 〔56.6〕 °C `

¢%%` SBOperatingLoss = 2 * pi * SteamConductivity * (SteamOperating -
SBOperatingSurface) / ln(SBJacket / SBOutside) = 〔389〕 W/m `

¢%%` SBCheckSurface = Surface(SBOutside, SteamThickness, SteamCheck, Ambient,
SteamConductivity, Convection, Emissivity, Sigma) = 〔58〕 °C `

¢%%` SBCheckLoss = 2 * pi * SteamConductivity * (SteamCheck - SBCheckSurface) /
ln(SBJacket / SBOutside) = 〔422〕 W/m `

### Steam common header

¢%%` SHJacket = SHOutside + 2 * SteamThickness = 〔1,815〕 mm `

¢%%` SHOperatingSurface = Surface(SHOutside, SteamThickness, SteamOperating,
Ambient, SteamConductivity, Convection, Emissivity, Sigma) = 〔58.4〕 °C `

¢%%` SHOperatingLoss = 2 * pi * SteamConductivity * (SteamOperating -
SHOperatingSurface) / ln(SHJacket / SHOutside) = 〔579〕 W/m `

¢%%` SHCheckSurface = Surface(SHOutside, SteamThickness, SteamCheck, Ambient,
SteamConductivity, Convection, Emissivity, Sigma) = 〔59.9〕 °C `

¢%%` SHCheckLoss = 2 * pi * SteamConductivity * (SteamCheck - SHCheckSurface) /
ln(SHJacket / SHOutside) = 〔627〕 W/m `

### Feedwater branch

¢%%` WBJacket = WBOutside + 2 * WaterThickness = 〔875〕 mm `

¢%%` WBOperatingSurface = Surface(WBOutside, WaterThickness, WaterOperating,
Ambient, WaterConductivity, Convection, Emissivity, Sigma) = 〔54.2〕 °C `

¢%%` WBOperatingLoss = 2 * pi * WaterConductivity * (WaterOperating -
WBOperatingSurface) / ln(WBJacket / WBOutside) = 〔215〕 W/m `

¢%%` WBCheckSurface = Surface(WBOutside, WaterThickness, WaterCheck, Ambient,
WaterConductivity, Convection, Emissivity, Sigma) = 〔56.4〕 °C `

¢%%` WBCheckLoss = 2 * pi * WaterConductivity * (WaterCheck - WBCheckSurface) /
ln(WBJacket / WBOutside) = 〔248〕 W/m `

### Feedwater common header

¢%%` WHJacket = WHOutside + 2 * WaterThickness = 〔1,240〕 mm `

¢%%` WHOperatingSurface = Surface(WHOutside, WaterThickness, WaterOperating,
Ambient, WaterConductivity, Convection, Emissivity, Sigma) = 〔55.4〕 °C `

¢%%` WHOperatingLoss = 2 * pi * WaterConductivity * (WaterOperating -
WHOperatingSurface) / ln(WHJacket / WHOutside) = 〔329〕 W/m `

¢%%` WHCheckSurface = Surface(WHOutside, WaterThickness, WaterCheck, Ambient,
WaterConductivity, Convection, Emissivity, Sigma) = 〔57.7〕 °C `

¢%%` WHCheckLoss = 2 * pi * WaterConductivity * (WaterCheck - WHCheckSurface) /
ln(WHJacket / WHOutside) = 〔380〕 W/m `

## Sensitivity: keep the selected thicknesses fixed

For each common header, change one condition at a time at the higher check fluid
temperature. These cases can exceed 60°C; the thickness recommendation is
conditional on the base environmental assumptions. The 50°C-room case also
assumes 50°C mean radiant surroundings. Smaller convection can represent
sheltered or stagnant locations. The combined adverse case uses all three
changes.

¢%%` SHWarmRoomSurface = Surface(SHOutside, SteamThickness, SteamCheck, 323.15
'K', SteamConductivity, Convection, Emissivity, Sigma) = 〔69.1〕 °C `

¢%%` SHQuietAirSurface = Surface(SHOutside, SteamThickness, SteamCheck, Ambient,
SteamConductivity, 2 'W/m2/K', Emissivity, Sigma) = 〔69.9〕 °C `

¢%%` SHShinyJacketSurface = Surface(SHOutside, SteamThickness, SteamCheck,
Ambient, SteamConductivity, Convection, 0.10, Sigma) = 〔62.9〕 °C `

¢%%` SHCombinedSurface = Surface(SHOutside, SteamThickness, SteamCheck, 323.15
'K', SteamConductivity, 2 'W/m2/K', 0.10, Sigma) = 〔86〕 °C `

¢%%` WHWarmRoomSurface = Surface(WHOutside, WaterThickness, WaterCheck, 323.15
'K', WaterConductivity, Convection, Emissivity, Sigma) = 〔66.7〕 °C `

¢%%` WHQuietAirSurface = Surface(WHOutside, WaterThickness, WaterCheck, Ambient,
WaterConductivity, 2 'W/m2/K', Emissivity, Sigma) = 〔66.4〕 °C `

¢%%` WHShinyJacketSurface = Surface(WHOutside, WaterThickness, WaterCheck,
Ambient, WaterConductivity, Convection, 0.10, Sigma) = 〔60.3〕 °C `

¢%%` WHCombinedSurface = Surface(WHOutside, WaterThickness, WaterCheck, 323.15
'K', WaterConductivity, 2 'W/m2/K', 0.10, Sigma) = 〔80.9〕 °C `

## Approximate room heat load from these pipes

Reuse the previous worksheet's provisional 15 m per branch and 90 m total
common-header length for each service. There are three branches per service.
Each header length is counted once. This is only straight-pipe heat loss; it
excludes the generators, reactor, salt lines and all insulation
discontinuities. Actual route lengths and fittings must replace these budgets
for ventilation design.

¢` BranchCount = 3 `

¢` BranchLength = 15 m `

¢` HeaderLength = 90 m `

¢%%` SteamRoomHeat = BranchCount * BranchLength * SBOperatingLoss +
HeaderLength * SHOperatingLoss = 〔69.6〕 kW `

¢%%` WaterRoomHeat = BranchCount * BranchLength * WBOperatingLoss +
HeaderLength * WHOperatingLoss = 〔39.3〕 kW `

¢%%` TotalRoomHeat = SteamRoomHeat + WaterRoomHeat = 〔109〕 kW `

## Implementation and remaining choices

Allow for multiple insulation layers with staggered joints and a removable
protective jacket. Final layer sizes, attachment, expansion accommodation,
moisture exclusion and corrosion compatibility need supplier detailing. Valves
and connections need removable insulation covers and separate thermal bridge
checks. Thickness here is radial: 350 mm adds 700 mm to a steam pipe's
diameter, and 175 mm adds 350 mm to a feedwater pipe's diameter.

Before final selection, confirm the room and radiant temperatures, jacket
finish, convection, actual pipe sizes, material conductivity and acceptable
heat load. Accessible surfaces may require guarding or a stricter
contact-temperature criterion. There is no salt-pipe sizing or graphics change
in this estimate. See the [verification record][4] for independent checks and
reproduction.

[1]: Steam%20and%20feedwater%20pipe%20sizing%20-%20Hurmet.md

[2]: https://insulation.org/training-tools/designguide/design-objectives/

[3]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\\\\\\\\\\\\\_IND\\\\\\\\\\\\\\\_Thermo-1200\\\\\\\\\\\\\\\_DS.pdf

[4]: steam-water-insulation-check.md

[5]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\\\\\_IND\\\\\\\_Thermo-1200\\\\\\\_DS.pdf

[6]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\_IND\\\_Thermo-1200\\\_DS.pdf

[7]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\_IND\_Thermo-1200\_DS.pdf

[8]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM_IND_Thermo-1200_DS.pdf
