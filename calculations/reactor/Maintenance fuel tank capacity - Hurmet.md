---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Maintenance fuel tank capacity — preliminary volume check

¢` format = "h3" `

12 October 2026. Check one maintenance fuel tank against one core sector,
allowing 50% of the tank volume for cooling pipes, as requested by the owner.
These are the six rectangular maintenance fuel tanks, not the absorber-module
tanks.

## Inputs and provenance

Core dimensions are from `fastSaltModels/models/wistr_reactor.py`, `CORE`: 3.8 m
diameter, 3.4 m active height and six sectors. The active height excludes
reflectors and plenums. Tank dimensions are from
`fastSaltModels/models/wistr_installation.py`, `FUEL_STORAGE`. The tanks are
visual external envelopes, without resolved walls or internal cavities. Use
their dimensions provisionally here; replace with clear internal dimensions
when the tank construction is specified.

¢` CoreDiameter = 3.8 m `

¢` CoreHeight = 3.4 m `

¢` SectorCount = 6 `

¢` TankLength = 3.5 m `

¢` TankWidth = 1.25 m `

¢` TankHeight = 5.4 m `

¢` CoolingFraction = 0.5 `

## Calculation

Treat the entire gross core-sector envelope as fuel for this comparison. This is
an upper bound on fuel contained inside that envelope, not an estimate of
actual fuel inventory: coolant passages, structure and absorber separations
reduce the volume occupied by fuel. Fuel in connected tubing is outside this
bound.

¢%%` SectorEnvelope = pi * CoreDiameter^2 * CoreHeight / (4 * SectorCount) =
〔6.43〕 m3 `

¢%%` TankGross = TankLength * TankWidth * TankHeight = 〔23.6〕 m3 `

¢%%` TankAvailable = TankGross * (1 - CoolingFraction) = 〔11.8〕 m3 `

¢%%` SpareVolume = TankAvailable - SectorEnvelope = 〔5.39〕 m3 `

¢%%` CapacityRatio = TankAvailable / SectorEnvelope = 〔1.84〕 `

¢%%` AvailableSpaceUsed = 100 * SectorEnvelope / TankAvailable = 〔54.4〕 `

`AvailableSpaceUsed` is expressed as a percentage.

## Interpretation and limits

The modeled dimensions provide 11.8125 m³ after the assumed cooling-pipe
occupancy, versus 6.426651 m³ for the entire gross sector envelope: about 1.84
times that envelope, with 5.385849 m³ remaining. There is no indication that a
tank enlargement is needed from this preliminary geometric comparison.

This does not establish final usable tank capacity. Wall thickness, heads or
rounded corners, other internals, required freeboard, fuel-temperature volume
changes and connected-pipe inventory still need to be included. Do not count
the remaining space simultaneously as freeboard and as additional stored
inventory. This worksheet addresses volume only, not cooling performance or
storage qualification.

## Recalculation

Recalculated with Hurmet 0.1.1 using its official `utils/hurmet.cjs` and
matching `utils/temml.cjs` bundles. Saved results were recalculated a second
time and compared with an independent arithmetic calculation. Open this
Markdown file in Hurmet to edit inputs and recalculate; generic Markdown
viewers show saved results.
