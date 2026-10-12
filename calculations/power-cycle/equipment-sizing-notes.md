# Preliminary power-plant equipment sizes

**Historical steam-drive equipment revision.** Current layout work uses the
[motor-BFP worksheet](Motor-BFP%20equipment%20sizing%20-%20Hurmet.md) and
[motor equipment register](motor-equipment-sizing.json), D-029. The old values
below are preserved for comparison.

11 October 2026. Requested after review of the annotated Rankine-cycle diagram.
Start with the [editable Hurmet worksheet](Power%20plant%20equipment%20sizing%20-%20Hurmet.md).
The calculations use D-026, exactly 5 kPa, and retain the 20/30/35°C cooling checks.
This is a balance-of-plant equipment study; reactor and fuel preparation are outside scope.

## Requirements and layout candidates

| Item | Calculated requirement | Conditional layout/capacity allowance |
| --- | --- | --- |
| Reheater | 252.5 MW; integrated UA 6.816 MW/K | 8,179 m² at assumed U=1,000 with 20% surface allowance; four 63.1 MW modules, each 16 × 3 × 3 m plus 13 m withdrawal |
| Condenser | 804 / 826 / 838 MW across reference / hot / extreme checks | Preserve ~38,500 m² thermal basis; three modules, each 16 × 7 × 9 m plus 13 m withdrawal |
| Condenser tubing | 40,224 tubes total, 25.4 mm OD / 23.4 mm ID, 12 m effective length, two passes | 2.75 m/s cooling water; tube-side loss screen ~9.2 m head; material and wall unselected |
| LP exhaust | 9,258 m³/s at 5 kPa; ~51.4 m² total annulus at assumed 180 m/s | Six exhaust flows / three double-flow LP casings are a candidate; ~3.81 m tip diameter, 0.95 m blade span under assumed 0.5 hub/tip ratio |
| HP/IP and LP generators | 398.2 and 280.5 MW respectively | 500 and 350 MVA with assumed 0.90 power factor and 10% capacity margin |
| Feedwater pumps | 0.783 m³/s total, provisional 26.5 MPa discharge; 23.71 MW total shaft | Three 50% pumps, two duty; reserve 15 MW driver each; steam drive retained provisionally |
| Condensate pumps | 0.418 m³/s total; proposed 1.0 MPa discharge | Three 50% pumps, two duty; 355 kW motor each |
| Cooling-water pumps | 23.76 m³/s total; assumed 20 m total head | Three 50% pumps, two duty; 3.5 MW motor each; ~5.51 MW operating load |
| Deaerator storage | Ten minutes = 470 m³ usable drawdown inventory | Two 4.5 m ID × 22 m straight-length vessels provide ~490 m³ usable at assumed 70% drawdown fraction; heads and deaerating sections extra |
| Water-level elevation | NPSH estimates depend on vendor pump requirements | Reserve minimum deaerator water level 14 m above BFP datum; hotwell 4 m above condensate first stage; neither is a verified pump requirement |

All box dimensions are explicit analyst allowances, not manufacturer dimensions.
Tube counts/packing constrain the boxes but do not validate shell-side flow,
pressure walls, vacuum buckling, vibration, structural loads or maintenance fit.

The reheater area ranges from **5,453 to 16,359 m²** for assumed U=1,500 to
500 W/(m² K), including the same allowance. Its four-module envelope only
represents the middle U case. Condenser thermal U remains provisional, with no
separate proven fouling margin; an extra 20% area option is 46,216 m² and would
require a revised cooling/control calculation before adoption.

## Heater duties and areas

| Heater | Duty MW | Surface m² at U=2,000 plus 20% |
| --- | ---: | ---: |
| HP4 | 207.4 | 5,337 |
| HP3 | 90.4 | 3,623 |
| HP2 | 66.3 | 3,091 |
| HP1 | 37.5 | 2,271 |
| LP3 | 22.4 | 1,238 |
| LP2 | 53.2 | 2,051 |
| LP1 | 54.1 | 2,062 |

The calculation includes incoming cascading drains and the reheater return to
HP4. It ideally mixes incoming hot streams at shell pressure before integrating
`UA = integral(dQ / (Th - Tc))` for counterflow. The local temperature profiles
remain positive and the hot/cold duties close. This is a composite-stream area
proxy; a proper heater design separates desuperheating, condensing and any drain
cooling. A 20% area allowance is not proof that this idealization is conservative.
U=1,000 doubles the listed areas; U=3,000 gives two-thirds. Final shell diameters,
pass counts, tube walls, velocities, zone lengths and pressure drops are deferred.

## Pipe passages

[Detailed pipe register](equipment-pipes.csv) and live equations are in Hurmet.
Bores are internal; pressure walls, insulation and supports are additional.
Representative proposed passages:

- Cold reheat: two 750 mm bores; hot reheat: two 950 mm bores.
- IP-to-LP crossover: three 1,400 mm bores, one candidate per double-flow LP casing.
- Reheater heating supply: 350 mm bore; high-pressure return before throttle: 475 mm.
- Existing steam header/branch: 725/425 mm; feedwater header/branch: 650/375 mm.
- LP heater extractions: 675 / 1,250 / 2,025 mm bores for LP3 / LP2 / LP1.
- Cooling mains: two 2,250 mm supply mains and two 2,250 mm return mains;
  2,000 mm supply/return branches per condenser module.

The large LP1 extraction follows from ~22 kg/s at 0.03 MPa: low density gives a
large actual volume. Place low-pressure heaters near their turbine connections.
Do not use an ordinary small steam-pipe symbol as an equipment envelope.

The generic pressure-loss screen uses 40 m, K=5 and Darcy f=0.015 for each
steam/feedwater route. This is an order-of-magnitude comparison, not a solved
network or actual route loss, and does not replace the earlier main piping
worksheet. Wet lines use a homogeneous density approximation; flashing return
and cascade-drain/control/vent lines still need two-phase analysis and sizing.
All proposed bores remain within their selected velocity limits over the accepted
20/30/35°C cooling cases. The minimum 5 kPa case bounds LP exhaust volume in those
checks; startup, part load and pressure below 5 kPa are excluded.

## Pump pressures require a subsequent heat-balance revision

The existing 0.72 MPa condensate discharge has only 0.12 MPa above the deaerator.
Raising water 14 m consumes about 0.137 MPa before heater/piping losses, so that
old pressure cannot serve the proposed arrangement. A provisional 1.0 MPa discharge
covers the 0.887 MPa combined pressure/elevation/loss estimate.

The 26.5 MPa BFP discharge budget includes 0.4 MPa main-steam piping, 1.5 MPa SG,
0.4 MPa heaters and 0.2 MPa feedwater piping above the 24 MPa turbine inlet.
The pump shaft duty becomes 23.71 MW, **2.28 MW above the frozen cycle value**.
This is a proposed pressure budget, not a new 679 MW performance result. Reclose
extraction flows, pump-turbine output, heater balances, SG pressure states and
reheater approach before promoting these pressures to the operating basis.
The diagram's one feed-pump-turbine symbol is aggregate; the three 50% pump
arrangement and startup/standby drivers need a detailed equipment schematic.

The cooling-water 3.5 MW motor allowance assumes 20 m head and two duty pumps.
It does not cover the 30 m sensitivity case. The final heat sink, external lift
and route lengths are still unknown. Net export remains open; do not subtract
steam-driven BFP shaft work again from gross electrical output.

## Building implications

Three condenser envelopes occupy 336 m²; four reheaters occupy 192 m², both
before access. Two storage cylinders need ~198 m² of projected plan area before
heads and access, potentially elevated. About 445 tonnes is only the usable
water inventory, not the full storage operating/support load.

These areas cannot establish a building size by summing them: turbines may sit
over condensers, while tube withdrawal, crane laydown, generators, heaters and
safe maintenance routes need clear space. The existing **45 × 24 × 20 m** building
is still an unverified concept envelope. Next make a dimensional arrangement
with elevations and access, then decide its footprint and height. No Blender
geometry is changed in this calculation pass.

## Reproduction and checks

Use the pinned cycle Python dependencies. From this directory:

```sh
python size_equipment.py
python check_equipment_envelope.py . .
python publish_equipment.py
HURMET_ENGINE=/path/to/hurmet.cjs TEMML_ENGINE=/path/to/temml.cjs node check_equipment_hurmet.cjs
```

Python checks heater energy closure, positive local approaches and UA integration
convergence (1,601 versus 3,201 points, within 0.1%), condenser tube geometry and
water velocity, pump/driver margins, inventory, and cooling-case passage velocities.
Hurmet save/reopen recalculation passes **73 numerical comparisons** and four
sensitivities (reheater U, heater U, storage time and cooling head). Those checks
verify the formulas and stated assumptions, not equipment qualification.

Sources are linked in the worksheet. CoolProp 7.2.0 supplies IAPWS-95 properties;
Spirax Sarco supplies general storage context; Graham and Siemens material gives
configuration context only. No published vendor drawing or catalog size is being
represented as the selected plant equipment. The first schematic, original cycle,
previous piping worksheets and current graphics remain preserved.
