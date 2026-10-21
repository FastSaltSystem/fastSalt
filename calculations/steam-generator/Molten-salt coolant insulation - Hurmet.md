---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Molten-salt coolant pipe insulation

¢` format = "h3" `

Preliminary estimate — 11 October 2026. Allow **400 mm radial insulation on hot
coolant legs and 350 mm on cooler return legs**. An optional common 400 mm
thickness simplifies layout and adds margin on the return. These are
conditional straight-pipe thermal estimates, not approved specifications. This
sheet covers the three coolant circuits between reactor and steam generators,
not the small fuel or absorber tubes. No graphics are changed.

Open in Hurmet to edit and recalculate. Copied source inputs do not
automatically update. All numeric result cells are live calculations.

## Source inputs and dimensional uncertainty

The [generator worksheet][1] specifies coolant temperatures of 875 K hot and 810
K cool (601.85°C / 536.85°C). The [pump worksheet][2] finds a 1.400211 m
minimum clear bore at the stated flow and 3 m/s velocity limit. Therefore the
1.4 m visible diameter in the graphics cannot also be the final bare outside
diameter. Use **1.5 m bare OD** as a provisional thermal/layout envelope. This
leaves about 50 mm per side beyond that bore, but does not select or verify a
50 mm pressure wall. Recalculate when the pipe wall is established. A 1.4 m OD
comparison below quantifies the effect of this uncertainty.

¢` HotTemperature = 875 K `

¢` ColdTemperature = 810 K `

¢` PipeOutside = 1.5 m `

## Insulation and environmental assumptions

Use dry calcium silicate with metal jacketing, using [JM Thermo-1200][3] as a
reference. Its 650°C maximum service temperature exceeds these operating
conditions, but maximum service/transient temperatures still need confirmation.
Its pipe-test conductivity is 0.085 W/(m K) at 316°C mean temperature and 0.093
at 371°C. Use 0.090 W/(m K) for both legs: slightly above interpolated values
at their approximate operating mean insulation temperatures of 330°C and 298°C.
This is an effective screening value, not a material law for all temperatures.
It is not an assessment of compatibility with leaked molten salt.

The environmental basis matches the [steam/feedwater insulation estimate][4]:
40°C room air and mean radiant surroundings, external convection 4 W/(m² K),
and jacket emissivity 0.20. These are assumptions, not measured conditions. The
60°C surface criterion is a screening target, not a universal safe-touch limit.
Use 50 mm thickness increments for this provisional salt-pipe layout; actual
layers and product availability need supplier detailing.

¢` Conductivity = 0.090 W/m/K `

¢` Ambient = 313.15 K `

¢` SurfaceLimit = 333.15 K `

¢` Convection = 4 W/m2/K `

¢` Emissivity = 0.20 `

¢` Sigma = 0.00000005670374419 W/m2/K4 `

¢` ThicknessStep = 50 mm `

## Calculation method

For bare OD D, radial insulation t and jacket temperature Ts, conduction per
metre is 2πk(Tp − Ts)/ln((D + 2t)/D). External loss is π(D + 2t)\[h(Ts − Ta) +
εσ(Ts⁴ − Ta⁴)]. Equate the two expressions to find Ts; fix Ts at the target to
solve for minimum thickness. Radiation uses kelvin. The functions below are the
same unit-aware bisection solvers as the earlier steam/feedwater sheet.

The pipe surface is taken at the coolant temperature; metal wall, internal-film
and thin-jacket resistances are neglected. Insulation is dry and continuous.
Radiation assumes surroundings at ambient temperature with unity effective view
factor. Adjacent hot surfaces, thermal bridges, wetting, fittings and supports
are excluded.

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

## Thickness and steady-state performance

¢%%` HotMinimum = Minimum(PipeOutside, HotTemperature, Ambient, SurfaceLimit,
Conductivity, Convection, Emissivity, Sigma) = 〔364〕 mm `

¢%%` HotThickness = ceil(HotMinimum / ThicknessStep) * ThicknessStep = 〔400〕 mm `

¢%%` HotJacket = PipeOutside + 2 * HotThickness = 〔2.3〕 m `

¢%%` HotSurface = Surface(PipeOutside, HotThickness, HotTemperature, Ambient,
Conductivity, Convection, Emissivity, Sigma) = 〔58〕 °C `

¢%%` HotLoss = 2 * pi * Conductivity * (HotTemperature - HotSurface) /
ln(HotJacket / PipeOutside) = 〔719〕 W/m `

¢%%` ColdMinimum = Minimum(PipeOutside, ColdTemperature, Ambient, SurfaceLimit,
Conductivity, Convection, Emissivity, Sigma) = 〔326〕 mm `

¢%%` ColdThickness = ceil(ColdMinimum / ThicknessStep) * ThicknessStep = 〔350〕 mm `

¢%%` ColdJacket = PipeOutside + 2 * ColdThickness = 〔2.2〕 m `

¢%%` ColdSurface = Surface(PipeOutside, ColdThickness, ColdTemperature, Ambient,
Conductivity, Convection, Emissivity, Sigma) = 〔58.5〕 °C `

¢%%` ColdLoss = 2 * pi * Conductivity * (ColdTemperature - ColdSurface) /
ln(ColdJacket / PipeOutside) = 〔706〕 W/m `

¢%%` CommonThickness = max(HotThickness, ColdThickness) = 〔400〕 mm `

¢%%` CommonJacket = PipeOutside + 2 * CommonThickness = 〔2.3〕 m `

¢%%` CommonColdSurface = Surface(PipeOutside, CommonThickness, ColdTemperature,
Ambient, Conductivity, Convection, Emissivity, Sigma) = 〔56〕 °C `

¢%%` CommonColdLoss = 2 * pi * Conductivity * (ColdTemperature -
CommonColdSurface) / ln(CommonJacket / PipeOutside) = 〔636〕 W/m `

## Sensitivity at fixed selected thicknesses

Change one condition at a time: room/radiant temperature to 50°C, convection to
2 W/(m² K), emissivity to 0.10, or coolant temperature upward by 25 K. The last
is only an illustrative temperature sensitivity, not an adopted design
temperature or a predicted transient. The combined case changes room,
convection and emissivity together, keeping nominal coolant temperatures.
Exceeding 60°C in these cases means the base selection does not meet the target
in those conditions.

¢%%` HotWarmRoomSurface = Surface(PipeOutside, HotThickness, HotTemperature,
323.15 'K', Conductivity, Convection, Emissivity, Sigma) = 〔67.3〕 °C `

¢%%` HotQuietAirSurface = Surface(PipeOutside, HotThickness, HotTemperature,
Ambient, Conductivity, 2 'W/m2/K', Emissivity, Sigma) = 〔67.3〕 °C `

¢%%` HotShinyJacketSurface = Surface(PipeOutside, HotThickness, HotTemperature,
Ambient, Conductivity, Convection, 0.10, Sigma) = 〔60.8〕 °C `

¢%%` HotWarmerSaltSurface = Surface(PipeOutside, HotThickness, HotTemperature +
25 'K', Ambient, Conductivity, Convection, Emissivity, Sigma) = 〔58.8〕 °C `

¢%%` HotCombinedSurface = Surface(PipeOutside, HotThickness, HotTemperature,
323.15 'K', Conductivity, 2 'W/m2/K', 0.10, Sigma) = 〔82.9〕 °C `

¢%%` ColdWarmRoomSurface = Surface(PipeOutside, ColdThickness, ColdTemperature,
323.15 'K', Conductivity, Convection, Emissivity, Sigma) = 〔67.7〕 °C `

¢%%` ColdQuietAirSurface = Surface(PipeOutside, ColdThickness, ColdTemperature,
Ambient, Conductivity, 2 'W/m2/K', Emissivity, Sigma) = 〔67.9〕 °C `

¢%%` ColdShinyJacketSurface = Surface(PipeOutside, ColdThickness,
ColdTemperature, Ambient, Conductivity, Convection, 0.10, Sigma) = 〔61.3〕 °C `

¢%%` ColdWarmerSaltSurface = Surface(PipeOutside, ColdThickness,
ColdTemperature + 25 'K', Ambient, Conductivity, Convection, Emissivity, Sigma)
= 〔59.4〕 °C `

¢%%` ColdCombinedSurface = Surface(PipeOutside, ColdThickness, ColdTemperature,
323.15 'K', Conductivity, 2 'W/m2/K', 0.10, Sigma) = 〔83.5〕 °C `

¢%%` HotSmallODMinimum = Minimum(1.4 'm', HotTemperature, Ambient, SurfaceLimit,
Conductivity, Convection, Emissivity, Sigma) = 〔361〕 mm `

¢%%` ColdSmallODMinimum = Minimum(1.4 'm', ColdTemperature, Ambient,
SurfaceLimit, Conductivity, Convection, Emissivity, Sigma) = 〔323〕 mm `

## Illustrative external-pipe heat load

Assume three hot routes and three complete cool-return routes, each 15 m long. A
cool-return route includes generator-to-pump plus pump-to-reactor piping; it is
counted once, not twice. Lengths are placeholders, not measured geometry. There
are no external common coolant headers in this configuration. This budget
excludes generators, pumps, reactor, manifolds, valves and supports.

¢` LoopCount = 3 `

¢` HotRouteLength = 15 m `

¢` ColdRouteLength = 15 m `

¢%%` HotRoomHeat = LoopCount * HotRouteLength * HotLoss = 〔32.4〕 kW `

¢%%` ColdRoomHeat = LoopCount * ColdRouteLength * ColdLoss = 〔31.8〕 kW `

¢%%` TotalRoomHeat = HotRoomHeat + ColdRoomHeat = 〔64.2〕 kW `

¢%%` CommonRoomHeat = LoopCount * (HotRouteLength * HotLoss + ColdRouteLength *
CommonColdLoss) = 〔61〕 kW `

## Installation and operating limits

Use multiple layers with staggered joints and protective jacketing; thickness is
radial. Final cladding, bands, heat-tracing space and installation clearance
add to the calculated diameter. Pumps, valves and flanges need separately
detailed removable insulation. Confirm maximum service temperature and material
suitability before specifying a product; 650°C is a product limit, not an
allowed plant transient.

Insulation slows cooling but does not prevent eventual freezing in stagnant
salt. Startup, shutdown and drainability need a separate heat-tracing/preheat
and freeze-protection analysis using the selected salt's liquidus and operating
procedures. No tracing power or time-to-freeze is established here.

These thermal results do not establish pipe wall strength, pressure design, leak
containment or insulation resistance to a salt leak. Actual route lengths,
room/radiant conditions and conductivity must be confirmed. See
[verification][5].

[1]: Generator%20sizing%20-%20Hurmet.md

[2]: Coolant%20pump%20estimate%20-%20Hurmet.md

[3]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\\\\\\\\\\\\\_IND\\\\\\\\\\\\\\\_Thermo-1200\\\\\\\\\\\\\\\_DS.pdf

[4]: Steam%20and%20feedwater%20insulation%20-%20Hurmet.md

[5]: molten-salt-insulation-check.md

[6]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\\\\\_IND\\\\\\\_Thermo-1200\\\\\\\_DS.pdf

[7]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\\\_IND\\\_Thermo-1200\\\_DS.pdf

[8]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM\_IND\_Thermo-1200\_DS.pdf

[9]: https://www.jm.com/content/dam/jm/global/en/industrial-insulation/calcium-silicate/thermo-1200/JM_IND_Thermo-1200_DS.pdf
