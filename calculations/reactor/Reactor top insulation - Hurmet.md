---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Reactor top insulation without hood cooling

¢` format = "h3" `

Preliminary thermal estimate — 11 October 2026. Allow **500 mm of dry calcium
silicate insulation** over the reactor top for the base conditions below. The
calculated minimum is about 416 mm. This is a conditional layout allowance for
removable insulation, not a finalized insulation or cooling-system design.

No heat removal by air flowing through a hood is credited. The room-facing
surface still loses heat by natural convection and radiation. The room and its
surroundings are assumed maintained at 40°C by the building heat balance;
removing hood cooling does not imply a thermally isolated room.

Open in Hurmet to edit and recalculate. Source values are copied, not linked
live to the graphics or other worksheets. No Blender geometry is changed.

## Inputs and provenance

The [generator worksheet][1] gives hot coolant at 875 K (601.85°C).
Conservatively apply that temperature uniformly to the insulation hot face. The
actual top-cap metal temperature has not been established. No credit is taken
for metal-wall, internal-film or trapped-air resistance. This estimate covers
the flat top only, not skirts, sidewalls, open ducts or uncovered penetrations.

The environmental basis follows the [pipe insulation worksheet][2]: 40°C room
and radiant surroundings, assumed external convection of 4 W/(m² K), emissivity
0.20 and a 60°C exposed-surface screening target. The target is not a universal
safe-touch limit. The convection coefficient is an assumption, not an evaluated
horizontal-plate correlation.

[JM Thermo-1200][3] provides a candidate material basis: maximum service 650°C;
flat ASTM C518 conductivity 0.073 W/(m K) at 316°C mean and 0.081 at 371°C. Use
effective k = 0.085 W/(m K), conservatively above interpolation near the base
mean temperature of 329°C. Flat data are used here, unlike pipe-test data in
the cylindrical calculations. A density allowance of 240 kg/m³ uses the
published average dry-density upper value for a preliminary mass budget.
Supplier values are typical, not guarantees. Compatibility, irradiation and
maximum service/transient temperature remain to be confirmed.

¢` HotTemperature = 875 K `

¢` Ambient = 313.15 K `

¢` SurfaceLimit = 333.15 K `

¢` Conductivity = 0.085 W/m/K `

¢` Convection = 4 W/m2/K `

¢` Emissivity = 0.20 `

¢` Sigma = 0.00000005670374419 W/m2/K4 `

¢` ThicknessStep = 50 mm `

¢` ExtraLayer = 50 mm `

¢` Density = 240 kg/m3 `

## Flat-wall method

At steady state, k(Th − Ts)/t = h(Ts − Ta) + εσ(Ts⁴ − Ta⁴). Each side is heat
flux per unit top area. Radiation uses absolute kelvin and unit effective view
factor to surroundings at Ta. Unlike cylindrical pipe insulation, the outside
area does not grow with insulation thickness.

Solve directly for thickness at the target surface temperature; solve for
surface temperature at any chosen thickness using the bisection function below.
Round up to 50 mm layers, then add one provisional 50 mm layer. This added
layer is a layout margin, not a quantified allowance for joints or thermal
bridges.

¢` function Minimum(Th, Ta, Ts, k, h, e, sigma)
  if Ts <= Ta or Ts >= Th throw "Surface target must lie between ambient and hot face"
  if k <= 0 'W/m/K' or h <= 0 'W/m2/K' throw "Thermal coefficients must be positive"
  if e < 0 or e > 1 throw "Emissivity must be between zero and one"
  return k * (Th - Ts) / (h * (Ts - Ta) + e * sigma * (Ts^4 - Ta^4))
end `

¢` function Surface(t, Th, Ta, k, h, e, sigma)
  if t <= 0 'm' throw "Thickness must be positive"
  if Th <= Ta throw "Hot face must exceed ambient temperature"
  if k <= 0 'W/m/K' or h <= 0 'W/m2/K' throw "Thermal coefficients must be positive"
  if e < 0 or e > 1 throw "Emissivity must be between zero and one"
  low = Ta
  high = Th
  for i in 1:55
    mid = (low + high) / 2
    inside = k * (Th - mid) / t
    outside = h * (mid - Ta) + e * sigma * (mid^4 - Ta^4)
    if inside > outside
      low = mid
    else
      high = mid
    end
  end
  return (low + high) / 2
end `

## Base thickness and heat leakage

¢%%` TargetFlux = Convection * (SurfaceLimit - Ambient) + Emissivity * Sigma *
(SurfaceLimit^4 - Ambient^4) = 〔111〕 W/m2 `

¢%%` MinimumThickness = Minimum(HotTemperature, Ambient, SurfaceLimit,
Conductivity, Convection, Emissivity, Sigma) = 〔416〕 mm `

¢%%` RoundedMinimum = ceil(MinimumThickness / ThicknessStep) * ThicknessStep =
〔450〕 mm `

¢%%` SelectedThickness = RoundedMinimum + ExtraLayer = 〔500〕 mm `

¢%%` SelectedSurface = Surface(SelectedThickness, HotTemperature, Ambient,
Conductivity, Convection, Emissivity, Sigma) = 〔56.8〕 °C `

¢%%` SelectedFlux = Conductivity * (HotTemperature - SelectedSurface) /
SelectedThickness = 〔92.7〕 W/m2 `

## Thickness comparisons

The 120 mm case compares the previous hood's visual insulation thickness with a
direct 602°C hot face. It is **not** a prediction of the original ventilated,
double-hood arrangement. Other cases use the same base boundary conditions.

¢%%` Surface120 = Surface(120 'mm', HotTemperature, Ambient, Conductivity,
Convection, Emissivity, Sigma) = 〔101〕 °C `

¢%%` Flux120 = Conductivity * (HotTemperature - Surface120) / (120 'mm') = 〔355〕
W/m2 `

¢%%` Surface300 = Surface(300 'mm', HotTemperature, Ambient, Conductivity,
Convection, Emissivity, Sigma) = 〔67.1〕 °C `

¢%%` Flux300 = Conductivity * (HotTemperature - Surface300) / (300 'mm') = 〔152〕
W/m2 `

¢%%` Surface400 = Surface(400 'mm', HotTemperature, Ambient, Conductivity,
Convection, Emissivity, Sigma) = 〔60.8〕 °C `

¢%%` Flux400 = Conductivity * (HotTemperature - Surface400) / (400 'mm') = 〔115〕
W/m2 `

¢%%` Surface450 = Surface(450 'mm', HotTemperature, Ambient, Conductivity,
Convection, Emissivity, Sigma) = 〔58.6〕 °C `

¢%%` Flux450 = Conductivity * (HotTemperature - Surface450) / (450 'mm') = 〔103〕
W/m2 `

¢%%` Surface600 = Surface(600 'mm', HotTemperature, Ambient, Conductivity,
Convection, Emissivity, Sigma) = 〔54.1〕 °C `

¢%%` Flux600 = Conductivity * (HotTemperature - Surface600) / (600 'mm') =
〔77.6〕 W/m2 `

## Footprint, heat load and removable mass

Use the preserved reactor model's hot-hood roof footprint, radius
4.121639668346854 m, as a provisional gross insulated top area. This comes from
`air_system.dimensions.partition_inner` in the [baseline report][4]. It exceeds
the spider/top-flange radius of 4.02164 m. The no-hood-flow concept assumes
former duct openings are closed and insulated; no openings are subtracted here.
An actual segmented cover may have different coverage and side losses.

¢` CoverRadius = 4.121639668346854 m `

¢%%` CoverDiameter = 2 * CoverRadius = 〔8.24〕 m `

¢%%` CoverArea = pi * CoverRadius^2 = 〔53.4〕 m2 `

¢%%` TopHeat = SelectedFlux * CoverArea = 〔4.94〕 kW `

¢%%` InsulationVolume = CoverArea * SelectedThickness = 〔26.7〕 m3 `

¢%%` InsulationMass = InsulationVolume * Density = 〔6,404〕 kg `

¢%%` ArealMass = SelectedThickness * Density = 〔120〕 kg/m2 `

The mass budget excludes cladding, frames, lifting fittings and supports. At
roughly 6.4 tonnes of insulation alone, removable cassettes and their handling
loads need explicit layout. Staggered multilayer joints and insulated covers
around penetrations are required to approach this continuous-wall estimate.

## Sensitivity at fixed selected thickness

The following cases each change one assumption, except Combined, which changes
room temperature, convection and emissivity together. WarmerSalt is an
illustrative 625°C hot face, not an adopted accident or design temperature.
Both surface temperature at the selected thickness and the thickness needed to
hold 60°C are calculated. Room and radiant temperature always change together.

¢%%` WarmRoomSurface = Surface(SelectedThickness, HotTemperature, 323.15 'K',
Conductivity, Convection, Emissivity, Sigma) = 〔66.1〕 °C `

¢%%` WarmRoomMinimum = Minimum(HotTemperature, 323.15 'K', SurfaceLimit,
Conductivity, Convection, Emissivity, Sigma) = 〔822〕 mm `

¢%%` QuietAirSurface = Surface(SelectedThickness, HotTemperature, Ambient,
Conductivity, 2 'W/m2/K', Emissivity, Sigma) = 〔65.5〕 °C `

¢%%` QuietAirMinimum = Minimum(HotTemperature, Ambient, SurfaceLimit,
Conductivity, 2 'W/m2/K', Emissivity, Sigma) = 〔652〕 mm `

¢%%` ShinyJacketSurface = Surface(SelectedThickness, HotTemperature, Ambient,
Conductivity, Convection, 0.10, Sigma) = 〔59.4〕 °C `

¢%%` ShinyJacketMinimum = Minimum(HotTemperature, Ambient, SurfaceLimit,
Conductivity, Convection, 0.10, Sigma) = 〔483〕 mm `

¢%%` WarmerSaltSurface = Surface(SelectedThickness, 898.15 'K', Ambient,
Conductivity, Convection, Emissivity, Sigma) = 〔57.5〕 °C `

¢%%` WarmerSaltMinimum = Minimum(898.15 'K', Ambient, SurfaceLimit,
Conductivity, Convection, Emissivity, Sigma) = 〔434〕 mm `

¢%%` CombinedSurface = Surface(SelectedThickness, HotTemperature, 323.15 'K',
Conductivity, 2 'W/m2/K', 0.10, Sigma) = 〔80.7〕 °C `

¢%%` CombinedMinimum = Minimum(HotTemperature, 323.15 'K', SurfaceLimit,
Conductivity, 2 'W/m2/K', 0.10, Sigma) = 〔1,644〕 mm `

## Scope and next design checks

This calculation estimates normal steady-state heat leakage through top
insulation. It does not establish temperatures after shutdown or during an
accident, internal nuclear heating, thermal stresses or the adequacy of vessel,
well or decay-heat cooling. Removing the hood's collection function changes the
air-system boundary conditions; retain that distinction before changing the
vessel/well cooling arrangement. Thermal bridges at steel supports, lifting
hardware, joints, tubes and plugs need separate treatment; they can create
local hot spots even if the average surface meets the target.

[Independent verification and reproduction][5].

[1]: ../steam-generator/Generator%20sizing%20-%20Hurmet.md

[2]: ../steam-generator/Steam%20and%20feedwater%20insulation%20-%20Hurmet.md

[3]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\\\\\\\\\\\\\_IND\\\\\\\\\\\\\\\_Thermo-1200\\\\\\\\\\\\\\\_DS.pdf

[4]: ../../../fastSaltModels/baselines/wistr-reactor-handling-2026-10-08/reactor-study-report.json

[5]: reactor-top-insulation-check.md

[6]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\\\\\_IND\\\\\\\_Thermo-1200\\\\\\\_DS.pdf

[7]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\_IND\\\_Thermo-1200\\\_DS.pdf

[8]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\_IND\_Thermo-1200\_DS.pdf

[9]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM_IND_Thermo-1200_DS.pdf
