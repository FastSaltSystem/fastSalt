---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Brayton cooler size comparison — 30 MW per train

¢` format = "h3" `

13 October 2026. Preliminary scale check for the three candidate auxiliary
cycles. **One train removes 30 MW gross from salt; three such trains provide 90
MW gross, not 30 MW total.** No duty or redundancy requirement has been
selected. These trains are substantial industrial machinery, not small fans or
pony-pump packages.

The estimates have two different evidence levels: flow areas, equivalent bores,
shaft powers and counterflow cooler UA follow from the existing thermodynamic
calculations; equipment boxes and overall plots below are **judgment-based
reservations for a future layout**, not calculated or vendor-confirmed
dimensions. Do not treat the reservations as selected equipment. No graphics or
accepted site layout is changed.

## Calculated quantities

+---------------------------+------------------+---------------------+-----------------+
| At 30 MW per train        | Closed steam 2:1 | Closed nitrogen 4:1 | Open air 6.83:1 |
+===========================+==================+=====================+=================+
| Compressor shaft demand,  | 9.55             | 21.5                | 27.1            |
| MW                        |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
| Turbine shaft output, MW  | 10.6             | 24.8                | 32.2            |
+---------------------------+------------------+---------------------+-----------------+
| Compressor inlet volume,  | 21.6             | 10.7                | 89.2            |
| m³/s                      |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
| Hot low-pressure return / | 34.2             | 17.8                | 158             |
| exhaust volume, m³/s      |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
| Compressor inlet          | 0.957            | 0.673               | 2.75            |
| equivalent bore, m        |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
| Hot return / exhaust      | 1.2              | 0.87                | 3.66            |
| equivalent bore, m        |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
| Outdoor cooler air        | 247              | 227                 | 0               |
| volume, m³/s              |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
| Minimum cooler airflow    | 82.4             | 75.8                | 0               |
| face at 3 m/s, m²         |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
| Ideal-counterflow cooler  | 123              | 235                 | 0               |
| UA, kW/K                  |                  |                     |                 |
+---------------------------+------------------+---------------------+-----------------+
{.grid colWidths="250 125 125 125"}

Closed-loop working-fluid bores use 30 m/s; open-air intake and atmospheric
exhaust use 15 m/s. They are equivalent circular **clear flow diameters**,
excluding wall, insulation, casing, silencers and headers. They are not
compressor rotor diameters. Velocity choices are provisional; losses, noise and
available space must be checked together. The 3 m/s cooler face velocity is
superficial velocity based on cold inlet air, not free-gap velocity between
fins. Zero cooler area for open air means that the separate heat-rejection
exchanger is absent, not that no intake/exhaust equipment is required.

For the closed cycles, the earlier 30→130°C cooling-air assumption and 500 Pa
total air-system loss remain provisional. The 82 m² steam and 76 m² nitrogen
values are airflow-based minimum face areas, not complete exchanger sizes.
Nitrogen requires about 1.9 times the ideal-counterflow UA because of its
closer approach to ambient. Fin area, gas-side coefficient, fin efficiency,
depth and headers are not yet specified; particularly for nitrogen, a deeper
core or more face area may be necessary without exceeding the pressure budget.

## Initial boxes for a space study — not equipment dimensions

All dimensions are metres. Machine reservations include compressor, turbine,
alternator, coupling/gearing allowance and immediate mechanical auxiliaries.
They do not define stage arrangement. Cooler reservations allow for a
horizontal outdoor fin-fan bank, structure, plenums and fan depth; heights are
guesses pending design. Overall plots allow additional local aisles and piping;
they do not establish rotor withdrawal or lifting clearances.

+--------------------------+-------------+--------------+-----------------+
| Provisional reservation  | Steam 2:1   | Nitrogen 4:1 | Open air 6.83:1 |
+==========================+=============+==============+=================+
| Machinery box, L × W × H | 15 × 6 × 5  | 15 × 6 × 5   | 22 × 7 × 5.5    |
+--------------------------+-------------+--------------+-----------------+
| Separate outdoor cooler  | 12 × 10 × 6 | 16 × 10 × 7  | None            |
| box, L × W × H           |             |              |                 |
+--------------------------+-------------+--------------+-----------------+
| Local plot including     | 28 × 18     | 30 × 20      | 32 × 16         |
| access and connections,  |             |              |                 |
| L × W                    |             |              |                 |
+--------------------------+-------------+--------------+-----------------+
| Local plot area          | 504 m²      | 600 m²       | 512 m²          |
+--------------------------+-------------+--------------+-----------------+
{.grid colWidths="250 125 125 125"}

The closed-machine boxes are held equal because smaller nitrogen passages do not
establish a shorter or smaller complete train: its compressor is doing more
than twice the steam compressor's shaft work, and stage count, speed, seals and
gearbox choices are unresolved. The larger nitrogen cooler reservation reflects
the greater required UA, but is not a thermal design. The open-air plot
includes an allowance for intake filters and local hot-exhaust routing. Intake
orientation, silencing, exhaust separation and stack height are unselected and
can increase its site requirement.

These plots intentionally put all three concepts in roughly the same
**several-hundred-square-metre class**. Small differences between the figures
cannot rank the options. A reasonable uncertainty is at least ±50% in reserved
area until actual machinery and exchanger layouts exist. Larger changes are
possible if separate heaters, long remote ducts or redundant trains are needed.

## Industrial size benchmark

Siemens Energy's [SGT-750 manufacturer data][1] lists about 118 kg/s exhaust
flow and a power-generation package approximately 20.3 × 4.8 × 4.1 m, excluding
the intake filter housing and exhaust stack. Its mechanical-drive package is
12.8 × 4.3 × 4.1 m and excludes driven equipment. The [SGT-600][2] lists 81.3
kg/s and a generation package 18.8 × 4.6 × 4.0 m, with similar exclusions. The
open-air trial processes about 103 kg/s, between those mass flows.

These combustion-turbine packages provide a scale comparison only. They have
different pressure ratios, turbine temperatures, rotor architecture and
electrical output. They are not selected products, and they cannot be assumed
to operate in our externally heated arrangement. Their dimensions do not
validate the closed steam/nitrogen reservations or the proposed 22 × 7 m
open-air box. They do show why a several-metre industrial package is a more
credible starting point than a small standby generator enclosure, despite our
few-megawatt net output.

## Scope and practicality

This comparison assumes reuse of one existing steam-generator heat-transfer
train as the salt-to-working-fluid heater. **The existing generator, reactor,
main salt piping and generator building are excluded from the additional plot
areas.** Reuse is unverified: gas-side heat transfer, pressure loss and
isolation/changeover must be checked. A dedicated salt-to-gas heater would add
an as-yet-unsized major item; the boxes above would then be incomplete.
Salt-pump equipment, startup electrical facilities, remote switchgear,
redundant safety divisions and site-wide separation are also not sized here;
only ordinary local service space is included.

Three independent 30 MW trains would reserve roughly **1,500–1,800 m² total**
with these example plots, before shared access, separation or redundancy
additions. This suggests an outdoor auxiliary plant or annex, rather than
fitting all equipment into remaining reactor-building space. Whether that is
practical depends on the required heat-removal duty and plot available. The
calculations do not establish a decay-heat requirement.

If only 10 MW per train is required, the same-state flow areas and
ideal-counterflow UA scale to one third; equivalent duct diameters scale by the
square root of one third. Complete package dimensions and site area do not
scale linearly because stage arrangements and service clearances remain.
Reusing one 30 MW train for all three salt legs is a separate hydraulic and
availability arrangement, not a reason to divide the above train duty by three.

The earlier vacuum steam 8:1 option is especially unattractive for compactness:
at 30 MW its compressor-inlet volume is approximately 1,564 m³/s, corresponding
to an 8.15 m equivalent pipe at 30 m/s. This is a flow-area illustration, not a
proposed pipe design. That candidate is omitted from the main layout boxes.

## Hurmet verification

Volumes and UA are imported from the preserved cycle results. Editable
velocities below recalculate areas and equivalent bores; they do not resize the
provisional equipment boxes.

¢` ClosedVelocity = 30 m/s `

¢` OpenVelocity = 15 m/s `

¢` CoolerFaceVelocity = 3 m/s `

¢` SteamInletVolume = 21.572128105671 m3/s `

¢` SteamHotVolume = 34.15016252113 m3/s `

¢%%` SteamInletArea = SteamInletVolume / ClosedVelocity = 〔0.719〕 m2 `

¢%%` SteamInletDiameter = sqrt(4 * SteamInletArea / π) = 〔0.957〕 m `

¢%%` SteamHotDiameter = sqrt(4 * SteamHotVolume / (ClosedVelocity * π)) = 〔1.2〕 m `

¢` SteamCoolerVolume = 247.22449663663 m3/s `

¢%%` SteamCoolerFace = SteamCoolerVolume / CoolerFaceVelocity = 〔82.4〕 m2 `

¢` NitrogenInletVolume = 10.671855418594 m3/s `

¢` NitrogenHotVolume = 17.830170931224 m3/s `

¢%%` NitrogenInletArea = NitrogenInletVolume / ClosedVelocity = 〔0.356〕 m2 `

¢%%` NitrogenInletDiameter = sqrt(4 * NitrogenInletArea / π) = 〔0.673〕 m `

¢%%` NitrogenHotDiameter = sqrt(4 * NitrogenHotVolume / (ClosedVelocity * π)) =
〔0.87〕 m `

¢` NitrogenCoolerVolume = 227.45863274228 m3/s `

¢%%` NitrogenCoolerFace = NitrogenCoolerVolume / CoolerFaceVelocity = 〔75.8〕 m2 `

¢` AirInletVolume = 89.169237667213 m3/s `

¢` AirHotVolume = 158.06858862814 m3/s `

¢%%` AirInletArea = AirInletVolume / OpenVelocity = 〔5.94〕 m2 `

¢%%` AirInletDiameter = sqrt(4 * AirInletArea / π) = 〔2.75〕 m `

¢%%` AirHotDiameter = sqrt(4 * AirHotVolume / (OpenVelocity * π)) = 〔3.66〕 m `

¢%%` NitrogenToSteamUARatio = 234557.50738253 / 122734.53735739 = 〔1.91〕 `

## Reproduction and next step

Run `python brayton_size_screen.py`, then `node check_brayton_size.cjs` using
the existing Hurmet/Temml environment. Twelve numerical checks, save/reopen,
and diameter/velocity sensitivity are verified. Source hashes and the explicit
reservation dimensions are in `brayton-size-results.json`.

Next establish the heat duty per train, obtain compressor/turbine envelopes for
these actual flows and temperatures, and develop a coupled
heat-transfer/pressure-drop cooler design. Only then use a site fit to choose
between the options. No accepted site geometry or design decision is changed by
these reservations.

[1]: https://www.siemensenergy.com/global/en/home/products-services/product/sgt-750.html

[2]: https://www.siemens-energy.com/global/en/home/products-services/product/sgt-600.html
