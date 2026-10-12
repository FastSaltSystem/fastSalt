---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-11
---------------

# Power-plant equipment sizing — preliminary

11 October 2026. Sizes supported by the selected 1,500 MWt cycle: exchanger
surface, flow passages, storage inventory, pump duties and generator capacity.
This is a preliminary equipment study for the layout, not selected manufactured
equipment or a pressure-boundary design.

**Basis:** D-026 / `reheat-selection.json`, exactly 5 kPa reference; 24 MPa /
556.85°C main steam, 510°C reheat. Pressures are absolute. Existing
performance, piping walls and Blender geometry are not overwritten. The higher
pump discharge pressures proposed below require a new coupled heat balance
before updating the 679 MW gross result or extraction flows.

**Imported boundary:** CoolProp 7.2.0 water densities and pump enthalpy
increments, turbine work, flow fractions and integrated exchanger UA are
external Python results. Hurmet executes the equations for volumes, bores,
areas, inventory, capacity and power from those imports. A
pressure/temperature/cycle change requires rerunning Python. The source hashes
and detailed checks are in `equipment-sizing.json`; [method and limitations][1].

¢` format = "h7" `

¢` Gravity = 9.80665 'm/s2' `

¢` Pi = 3.14159265359 `

## 1. Reheater surface and module count

Assume U = 1,000 W/(m² K) and a 20% surface allowance. U is an editable
sensitivity input, not a demonstrated coefficient. The integrated UA retains
the nonlinear supercritical heating-stream profile and 20.3 K minimum local
approach. Four modules are a provisional layout division, all operating, not
standby capacity.

¢` ReheatUA = 6816224.95637 'W/K' `

¢` ReheatU = 1000 'W.m-2.K-1' `

¢` SurfaceFactor = 1.2 `

¢` ReheatModules = 4 `

¢` ReheatDuty = 252.510110742 MW `

¢??` ReheatArea = SurfaceFactor * ReheatUA / ReheatU = 〔8,179.47〕 'm2' `

¢??` ReheatModuleArea = ReheatArea / ReheatModules = 〔2,044.867〕 'm2' `

¢??` ReheatModuleDuty = ReheatDuty / ReheatModules = 〔63.12753〕 MW `

At U = 500 / 1,000 / 1,500 W/(m² K), required areas including the allowance are
**16,359 / 8,179 / 5,453 m²**. At the middle case each of four modules contains
approximately 2,136 tubes, 25.4 mm OD × 12 m effective length. The equivalent
packed bundle diameter is 1.84 m at 1.25D triangular pitch and 70% bundle
utilization. Reserve **16 × 3 × 3 m per module**, plus 13 m withdrawal space.
These dimensions are packing-based placeholders; tube wall, manifolds, 24 MPa
pressure boundary, shell-side velocity, vibration and pressure drop are not yet
designed.

## 2. Condenser

Keep the surface used in the accepted cooling cases; do not silently change its
pressure/performance map. It rejects 804 MW at the exact 5 kPa reference, 826
MW at 30°C water inlet and 838 MW at 35°C. Three equal condenser modules are a
layout option. U = 2,500 W/(m² K) remains an unverified effective assumption
with no separately established fouling allowance. A 20% extra-area option would
be 46,216 m² and needs a revised cooling/control check.

¢` CondenserAreaRequired = 38513.3661192 'm2' `

¢` CondenserModules = 3 `

¢` CondenserTubeOD = 0.0254 m `

¢` CondenserTubeID = 0.0234 m `

¢` CondenserTubeLength = 12 m `

¢` CondenserPasses = 2 `

¢` CondenserTubeCount = 13408 `

¢` CoolingFlow = 23.7633756548 'm3/s' `

¢??` CondenserAreaProvided = CondenserModules * CondenserTubeCount * Pi *
CondenserTubeOD * CondenserTubeLength = 〔38,516.79〕 'm2' `

¢??` CondenserTubeVelocity = (CoolingFlow / CondenserModules) /
((CondenserTubeCount / CondenserPasses) * Pi * CondenserTubeID^2 / 4) =
〔2.747459〕 'm/s' `

Each module has **13,408 tubes**, two passes, 12 m effective length; total
40,224 tubes. The 23.4 mm ID is a provisional hydraulic geometry, not a
verified material/wall choice. Calculated water velocity is 2.75 m/s. A
smooth-tube Darcy estimate (1.5 µm roughness, K=4, 24 m flow length) gives 9.2
m head before external piping and final water-box losses. A packed tube section
is 15.6 m² per module, equivalent to 4.46 m circular diameter. Reserve **16 × 7
× 9 m per module** including provisional water-box, steam-space and hotwell
allowance, plus **13 m tube withdrawal**. This reserve is not a final shell
dimension; vacuum buckling, inlet-neck area, air removal and lifting are
unresolved.

¢` CoolingMainCount = 2 `

¢` CoolingMainBore = 2.25 m `

¢` CoolingBranchBore = 2 m `

¢??` CoolingMainVelocity = CoolingFlow / (CoolingMainCount * Pi *
CoolingMainBore^2 / 4) = 〔2.988293〕 'm/s' `

¢??` CoolingBranchVelocity = (CoolingFlow / CondenserModules) / (Pi *
CoolingBranchBore^2 / 4) = 〔2.521372〕 'm/s' `

Use two 2.25 m bore parallel mains **for each of supply and return**, and one
2.0 m bore supply/return pair per condenser module. These are internal bores;
wall, burial/support and water-hammer design are separate. The final heat
sink/tower size cannot be established without an ambient/water-source basis;
838 MW is the largest rejection load among the accepted full-load cases.

## 3. Turbines and generators

The source diagram has HP/IP and LP generator groups. These capacity estimates
retain that grouping. Mechanical turbine dimensions cannot be selected from MW
alone.

¢` HPIPelectric = 398.246713921 MW `

¢` LPelectric = 280.476419132 MW `

¢` PowerFactor = 0.9 `

¢` GeneratorMargin = 1.1 `

¢` HPIP_MW_number = 398.246713921 `

¢` LP_MW_number = 280.476419132 `

¢??` HPIP_MVA_number = HPIP_MW_number * GeneratorMargin / PowerFactor =
〔486.746〕 `

¢??` LP_MVA_number = LP_MW_number * GeneratorMargin / PowerFactor = 〔342.8045〕 `

The last two numeric results are MVA. Reserve **500 MVA HP/IP and 350 MVA LP
generators**, using 0.90 power factor and 10% capacity margin. The respective
calculated outputs are 398.25 and 280.48 MWe. Generator cooling, fault
capability, excitation and grid requirements remain unresolved.

¢` ExhaustMass = 361.044394886 'kg/s' `

¢` ExhaustDensity = 0.0389960716495 'kg/m3' `

¢` AxialVelocity = 180 'm/s' `

¢` ExhaustFlows = 6 `

¢` HubTipRatio = 0.5 `

¢??` ExhaustVolume = ExhaustMass / ExhaustDensity = 〔9,258.481〕 'm3/s' `

¢??` TotalAnnulus = ExhaustVolume / AxialVelocity = 〔51.43601〕 'm2' `

¢??` TipDiameter = sqrt(4 * TotalAnnulus / (ExhaustFlows * Pi * (1 -
HubTipRatio^2))) = 〔3.814894〕 m `

¢??` BladeLength = TipDiameter * (1 - HubTipRatio) / 2 = 〔0.9537234〕 m `

At 180 m/s assumed axial speed and hub/tip ratio 0.5, four / six / eight exhaust
flows imply tip diameters **4.67 / 3.81 / 3.30 m** and blade lengths **1.17 /
0.95 / 0.83 m**. Six flows, provisionally three double-flow LP casings, are a
useful layout candidate. This is a continuity screen using homogeneous
wet-steam density, not a blade/rotor design or supplier choice; axial velocity,
speed, stress, blockage, exhaust losses, wetness and annulus geometry must be
determined together. Do not interpret 3.81 m as casing OD or an exhaust-pipe size.

## 4. Closed feedwater heaters

Hot and cold duties close for each heater including cascading drains. The area
model ideally pre-mixes incoming bleed and throttled drains at shell pressure,
then integrates a countercurrent temperature profile. This is an area proxy,
not a three-zone design. U = 2,000 W/(m² K), with 20% surface allowance, is
assumed for every heater; no correlation or fouling allowance has been
verified. Final desuperheating/condensing/drain zones, feed-side velocity,
number of shells, pressure walls and extraction nozzles may change these
estimates.

| Heater | Duty MW | Bleed kg/s | Shell MPa | Area m² at assumed U | | ---
| ---: | ---: | ---: | ---: |

| HP4 | 207.4 | 40.58 | 7.644 | 5,337 | | HP3 | 90.4 | 10.58 | 2.800 | 3,623 | |
HP2 | 66.3 | 17.89 | 1.600 | 3,091 | | HP1 | 37.5 | 6.55 | 1.000 | 2,271 | |
LP3 | 22.4 | 9.57 | 0.155 | 1,238 | | LP2 | 53.2 | 22.72 | 0.100 | 2,051 | |
LP1 | 54.1 | 21.99 | 0.030 | 2,062 |

Editable area calculations (UA imported from the detailed thermal profiles):

¢` HeaterU = 2000 'W.m-2.K-1' `

¢` HP4UA = 8895504.9272 'W/K' `

¢??` HP4Area = SurfaceFactor * HP4UA / HeaterU = 〔5,337.303〕 'm2' `

¢` HP3UA = 6038433.24148 'W/K' `

¢??` HP3Area = SurfaceFactor * HP3UA / HeaterU = 〔3,623.06〕 'm2' `

¢` HP2UA = 5151654.9872 'W/K' `

¢??` HP2Area = SurfaceFactor * HP2UA / HeaterU = 〔3,090.993〕 'm2' `

¢` HP1UA = 3784966.4652 'W/K' `

¢??` HP1Area = SurfaceFactor * HP1UA / HeaterU = 〔2,270.98〕 'm2' `

¢` LP3UA = 2063976.69926 'W/K' `

¢??` LP3Area = SurfaceFactor * LP3UA / HeaterU = 〔1,238.386〕 'm2' `

¢` LP2UA = 3419061.80544 'W/K' `

¢??` LP2Area = SurfaceFactor * LP2UA / HeaterU = 〔2,051.437〕 'm2' `

¢` LP1UA = 3436187.99733 'W/K' `

¢??` LP1Area = SurfaceFactor * LP1UA / HeaterU = 〔2,061.713〕 'm2' `

At U = 1,000 the areas double; at 3,000 they are two-thirds of the listed
values. Large LP extraction volumes favor short, direct connections near the
turbine. These heater thermal areas do not yet define shell dimensions.

## 5. Pumps and elevation

Provisionally use three 50% pumps per service: two operating, one standby. This
is an analyst-selected availability/layout assumption. Driver margins do not
guarantee pump curves or startup capability. Pressure losses below are budgets,
not measured losses. Existing cycle fractions and gross output are frozen until
reclosure.

¢` MainMass = 711.670246356 'kg/s' `

¢` DADensity = 908.593781654 'kg/m3' `

¢??` FeedPumpFlow = MainMass / DADensity = 〔0.7832656〕 'm3/s' `

¢` BFPspecificWork = 33315.9524878 'J/kg' `

¢??` BFPshaft = MainMass * BFPspecificWork = 〔23.70997〕 MW `

¢??` BFPshaftEach = BFPshaft / 2 = 〔11.85499〕 MW `

**Feedwater:** 26.5 MPa discharge, 0.6 MPa suction, about 2,907 m pressure head;
85% hydraulic efficiency. The 2.5 MPa above main-turbine inlet pressure budgets
0.4 MPa main-steam piping, 1.5 MPa generator, 0.4 MPa heaters and 0.2 MPa
feedwater piping. This also implies SG steam pressure above the earlier 24 MPa
value. Each duty pump carries 0.392 m³/s and about 11.85 MW shaft; reserve a
**15 MW driver per pump**. Steam drive remains the working preference, with
electric startup/backup unresolved. Total shaft duty rises by **2.28 MW**
relative to the frozen cycle; the feed-pump turbine and its heater bleeds must
be rebalanced before adopting the new pressures.

¢` BFP_NPSHr = 8 m `

¢` BFP_NPSHmargin = 3 m `

¢` BFP_suction_loss = 2 m `

¢??` BFP_min_level = BFP_NPSHr + BFP_NPSHmargin + BFP_suction_loss = 〔13〕 m `

Saturated deaerator water has no pressure-above-vapor-pressure cushion. With
assumed NPSHr=8 m, 3 m margin and 2 m suction loss, the minimum water level
must be 13 m above the pump datum; reserve **14 m** for layout. All three
quantities require pump/suction-line verification. A booster pump is an
alternative to the elevated storage arrangement.

¢` DApressure = 0.6 MPa `

¢` DAlevel = 14 m `

¢` CondensateDensity = 995.0002 'kg/m3' `

¢` LPHeaterLoss = 0.1 MPa `

¢` CondensateLineLoss = 0.05 MPa `

¢??` CondensatePressureRequired = DApressure + CondensateDensity * Gravity *
DAlevel + LPHeaterLoss + CondensateLineLoss = 〔0.8866067〕 MPa `

**Condensate:** 1.0 MPa discharge is a provisional replacement for 0.72 MPa. The
elevation and loss budget alone require 0.887 MPa. Total flow 0.418 m³/s; total
electrical load 0.541 MW at 80% hydraulic / 96% motor efficiency; reserve **355
kW per motor**. A vertical-can arrangement with hotwell level 4 m above the
first-stage datum allows 2 m assumed NPSHr + 1 m suction loss + 1 m margin.
Actual NPSHr, hotwell levels and transients are unresolved.

¢` CoolingDensity = 998 'kg/m3' `

¢` CoolingHead = 20 m `

¢` CoolingPumpEfficiency = 0.88 `

¢` MotorEfficiency = 0.96 `

¢??` CoolingPumpElectric = CoolingDensity * Gravity * CoolingFlow * CoolingHead
/ (CoolingPumpEfficiency * MotorEfficiency) = 〔5.50599〕 MW `

¢??` CoolingPumpEach = CoolingPumpElectric / 2 = 〔2.752995〕 MW `

**Cooling water:** at an assumed 20 m total head, total operating electrical
load is 5.51 MW. Each duty pump carries 11.88 m³/s; reserve **3.5 MW per
motor**. At 15 / 20 / 30 m head, total load is 4.13 / 5.51 / 8.26 MW; the
proposed motors do not cover the 30 m case. The condenser tube estimate
consumes about 9.2 m of the 20 m budget. Source/tower elevation, piping and
intake losses must complete the budget. These are service loads, not a complete
net-power estimate; do not subtract steam-driven BFP work twice.

## 6. Deaerator storage

Assume ten minutes usable inventory at full feedwater flow. This is a project
planning choice, not a code requirement. Usable volume is the operating
drawdown range, not the volume to the top of the tank.

¢` StorageTime = 600 s `

¢` StorageVessels = 2 `

¢` StorageDiameter = 4.5 m `

¢` StorageLength = 22 m `

¢` UsableFraction = 0.7 `

¢??` StorageRequired = FeedPumpFlow * StorageTime = 〔469.9594〕 'm3' `

¢??` StorageGross = StorageVessels * Pi * StorageDiameter^2 * StorageLength / 4
= 〔699.7898〕 'm3' `

¢??` StorageUsable = StorageGross * UsableFraction = 〔489.8528〕 'm3' `

¢??` StorageDuration = StorageUsable / FeedPumpFlow = 〔625.3981〕 s `

A candidate is **two 4.5 m diameter × 22 m straight-length vessels**, excluding
heads and the deaerating sections. Together their 70% usable range provides 490
m³, about 10.4 minutes. That drawdown inventory alone weighs about 445 tonnes;
actual operating water and structural loads include the minimum heel. Reserve
the minimum water level 14 m above feed-pump datum under the NPSH assumptions
above. Five minutes would require about 235 m³ usable; the final reserve time
should be selected with the operating philosophy. Storage and support
elevations are major building-layout constraints.

## 7. Pipe flow passages

All dimensions here are **internal bores**, before pressure wall, insulation and
supports. Velocity screens: main steam 25 m/s; HP admission/heating steam 30;
reheat/crossover 40; extraction lines 35; hot liquid return/feedwater 3; DA
suction 2; condensate 2.5. These are provisional analyst choices. Existing SG
branch/header bores are retained for comparison; their earlier custom walls are
not redesigned here. New line walls require selected materials, design
pressures, code and transients.

| Service | Parallel paths | Flow total kg/s | Bore each mm | Velocity m/s |
| --- | ---: | ---: | ---: | ---: |

| Main steam header (existing bore) | 1 | 711.67 | 725 | 23.41 | | Main steam
branch (each of 3) | 1 | 237.22 | 425 | 22.71 | | HP admission after reheat
split | 1 | 524.66 | 550 | 29.99 | | Reheater heating supply | 1 | 187.01 | 350
| 26.40 | | Reheater heating return | 1 | 187.01 | 475 | 2.74 | | Cold reheat |
2 | 415.33 | 750 | 38.22 | | Hot reheat | 2 | 415.33 | 950 | 39.04 | | IP-to-LP
crossover | 3 | 415.33 | 1400 | 39.64 | | Feedwater header (existing bore) | 1
| 711.67 | 650 | 2.81 | | Feedwater branch (each of 3) | 1 | 237.22 | 375 |
2.81 | | Deaerator to feed pumps | 2 | 711.67 | 500 | 1.99 | | Condensate
through LP heater bank | 1 | 415.33 | 475 | 2.36 | | HP4 extraction | 1 | 40.58
| 225 | 34.95 | | HP3 extraction | 1 | 10.58 | 175 | 33.98 | | HP2 extraction |
1 | 17.89 | 300 | 31.74 | | HP1 extraction | 1 | 6.55 | 225 | 31.33 | | LP3
extraction | 1 | 9.57 | 675 | 34.69 | | LP2 extraction | 1 | 22.72 | 1250 |
34.00 | | LP1 extraction | 1 | 21.99 | 2025 | 34.73 | | Feed-pump turbine
supply | 1 | 58.18 | 275 | 33.55 | | Feed-pump turbine exhaust to DA | 1 |
33.73 | 625 | 33.05 |

Detailed pipe formulas use imported densities at each named state. Bores are
rounded upward in Python in 25 mm steps; existing main/feedwater pipes keep
their prior bores. A generic 40 m route, K=5, Darcy factor 0.015 screens loss
magnitude; this is not the actual route budget and must not be added
indiscriminately to the existing piping losses.

**Main steam header (existing bore)** (main; single-phase).

¢` Pipe1Mass = 711.670246356 'kg/s' `

¢` Pipe1Density = 73.6283741527 'kg/m3' `

¢` Pipe1Count = 1 `

¢` Pipe1Limit = 25 'm/s' `

¢` Pipe1Bore = 0.725 m `

¢??` Pipe1MinBore = sqrt(4 * Pipe1Mass / (Pi * Pipe1Density * Pipe1Count *
Pipe1Limit)) = 〔0.7016198〕 m `

¢??` Pipe1Velocity = 4 * Pipe1Mass / (Pi * Pipe1Density * Pipe1Count *
Pipe1Bore^2) = 〔23.41357〕 'm/s' `

**Main steam branch (each of 3)** (main; single-phase).

¢` Pipe2Mass = 237.223415452 'kg/s' `

¢` Pipe2Density = 73.6283741527 'kg/m3' `

¢` Pipe2Count = 1 `

¢` Pipe2Limit = 25 'm/s' `

¢` Pipe2Bore = 0.425 m `

¢??` Pipe2MinBore = sqrt(4 * Pipe2Mass / (Pi * Pipe2Density * Pipe2Count *
Pipe2Limit)) = 〔0.4050804〕 m `

¢??` Pipe2Velocity = 4 * Pipe2Mass / (Pi * Pipe2Density * Pipe2Count *
Pipe2Bore^2) = 〔22.71144〕 'm/s' `

**HP admission after reheat split** (main; single-phase).

¢` Pipe3Mass = 524.663909322 'kg/s' `

¢` Pipe3Density = 73.6283741527 'kg/m3' `

¢` Pipe3Count = 1 `

¢` Pipe3Limit = 30 'm/s' `

¢` Pipe3Bore = 0.55 m `

¢??` Pipe3MinBore = sqrt(4 * Pipe3Mass / (Pi * Pipe3Density * Pipe3Count *
Pipe3Limit)) = 〔0.5499363〕 m `

¢??` Pipe3Velocity = 4 * Pipe3Mass / (Pi * Pipe3Density * Pipe3Count *
Pipe3Bore^2) = 〔29.99306〕 'm/s' `

**Reheater heating supply** (main; single-phase).

¢` Pipe4Mass = 187.006337034 'kg/s' `

¢` Pipe4Density = 73.6283741527 'kg/m3' `

¢` Pipe4Count = 1 `

¢` Pipe4Limit = 30 'm/s' `

¢` Pipe4Bore = 0.35 m `

¢??` Pipe4MinBore = sqrt(4 * Pipe4Mass / (Pi * Pipe4Density * Pipe4Count *
Pipe4Limit)) = 〔0.328322〕 m `

¢??` Pipe4Velocity = 4 * Pipe4Mass / (Pi * Pipe4Density * Pipe4Count *
Pipe4Bore^2) = 〔26.39886〕 'm/s' `

**Reheater heating return** (reheat\_return; single-phase).

¢` Pipe5Mass = 187.006337034 'kg/s' `

¢` Pipe5Density = 385.54842247 'kg/m3' `

¢` Pipe5Count = 1 `

¢` Pipe5Limit = 3 'm/s' `

¢` Pipe5Bore = 0.475 m `

¢??` Pipe5MinBore = sqrt(4 * Pipe5Mass / (Pi * Pipe5Density * Pipe5Count *
Pipe5Limit)) = 〔0.453715〕 m `

¢??` Pipe5Velocity = 4 * Pipe5Mass / (Pi * Pipe5Density * Pipe5Count *
Pipe5Bore^2) = 〔2.737161〕 'm/s' `

**Cold reheat** (reheat\_cold; single-phase).

¢` Pipe6Mass = 415.328627777 'kg/s' `

¢` Pipe6Density = 12.2979105765 'kg/m3' `

¢` Pipe6Count = 2 `

¢` Pipe6Limit = 40 'm/s' `

¢` Pipe6Bore = 0.75 m `

¢??` Pipe6MinBore = sqrt(4 * Pipe6Mass / (Pi * Pipe6Density * Pipe6Count *
Pipe6Limit)) = 〔0.7331458〕 m `

¢??` Pipe6Velocity = 4 * Pipe6Mass / (Pi * Pipe6Density * Pipe6Count *
Pipe6Bore^2) = 〔38.22242〕 'm/s' `

**Hot reheat** (reheat\_hot; single-phase).

¢` Pipe7Mass = 415.328627777 'kg/s' `

¢` Pipe7Density = 7.50502349048 'kg/m3' `

¢` Pipe7Count = 2 `

¢` Pipe7Limit = 40 'm/s' `

¢` Pipe7Bore = 0.95 m `

¢??` Pipe7MinBore = sqrt(4 * Pipe7Mass / (Pi * Pipe7Density * Pipe7Count *
Pipe7Limit)) = 〔0.9384907〕 m `

¢??` Pipe7Velocity = 4 * Pipe7Mass / (Pi * Pipe7Density * Pipe7Count *
Pipe7Bore^2) = 〔39.03667〕 'm/s' `

**IP-to-LP crossover** (IPex; single-phase).

¢` Pipe8Mass = 415.328627793 'kg/s' `

¢` Pipe8Density = 2.26865916018 'kg/m3' `

¢` Pipe8Count = 3 `

¢` Pipe8Limit = 40 'm/s' `

¢` Pipe8Bore = 1.4 m `

¢??` Pipe8MinBore = sqrt(4 * Pipe8Mass / (Pi * Pipe8Density * Pipe8Count *
Pipe8Limit)) = 〔1.393721〕 m `

¢??` Pipe8Velocity = 4 * Pipe8Mass / (Pi * Pipe8Density * Pipe8Count *
Pipe8Bore^2) = 〔39.64199〕 'm/s' `

**Feedwater header (existing bore)** (feedwater; single-phase).

¢` Pipe9Mass = 711.670246356 'kg/s' `

¢` Pipe9Density = 764.509244639 'kg/m3' `

¢` Pipe9Count = 1 `

¢` Pipe9Limit = 3 'm/s' `

¢` Pipe9Bore = 0.65 m `

¢??` Pipe9MinBore = sqrt(4 * Pipe9Mass / (Pi * Pipe9Density * Pipe9Count *
Pipe9Limit)) = 〔0.6285538〕 m `

¢??` Pipe9Velocity = 4 * Pipe9Mass / (Pi * Pipe9Density * Pipe9Count *
Pipe9Bore^2) = 〔2.805301〕 'm/s' `

**Feedwater branch (each of 3)** (feedwater; single-phase).

¢` Pipe10Mass = 237.223415452 'kg/s' `

¢` Pipe10Density = 764.509244639 'kg/m3' `

¢` Pipe10Count = 1 `

¢` Pipe10Limit = 3 'm/s' `

¢` Pipe10Bore = 0.375 m `

¢??` Pipe10MinBore = sqrt(4 * Pipe10Mass / (Pi * Pipe10Density * Pipe10Count *
Pipe10Limit)) = 〔0.3628957〕 m `

¢??` Pipe10Velocity = 4 * Pipe10Mass / (Pi * Pipe10Density * Pipe10Count *
Pipe10Bore^2) = 〔2.809457〕 'm/s' `

**Deaerator to feed pumps** (deaerator; single-phase).

¢` Pipe11Mass = 711.670246356 'kg/s' `

¢` Pipe11Density = 908.593781654 'kg/m3' `

¢` Pipe11Count = 2 `

¢` Pipe11Limit = 2 'm/s' `

¢` Pipe11Bore = 0.5 m `

¢??` Pipe11MinBore = sqrt(4 * Pipe11Mass / (Pi * Pipe11Density * Pipe11Count *
Pipe11Limit)) = 〔0.4993207〕 m `

¢??` Pipe11Velocity = 4 * Pipe11Mass / (Pi * Pipe11Density * Pipe11Count *
Pipe11Bore^2) = 〔1.994569〕 'm/s' `

**Condensate through LP heater bank** (condensate\_pump; single-phase).

¢` Pipe12Mass = 415.328627793 'kg/s' `

¢` Pipe12Density = 995.000215804 'kg/m3' `

¢` Pipe12Count = 1 `

¢` Pipe12Limit = 2.5 'm/s' `

¢` Pipe12Bore = 0.475 m `

¢??` Pipe12MinBore = sqrt(4 * Pipe12Mass / (Pi * Pipe12Density * Pipe12Count *
Pipe12Limit)) = 〔0.4610727〕 m `

¢??` Pipe12Velocity = 4 * Pipe12Mass / (Pi * Pipe12Density * Pipe12Count *
Pipe12Bore^2) = 〔2.355546〕 'm/s' `

**HP4 extraction** (HP4; single-phase).

¢` Pipe13Mass = 40.5751345293 'kg/s' `

¢` Pipe13Density = 29.1948309528 'kg/m3' `

¢` Pipe13Count = 1 `

¢` Pipe13Limit = 35 'm/s' `

¢` Pipe13Bore = 0.225 m `

¢??` Pipe13MinBore = sqrt(4 * Pipe13Mass / (Pi * Pipe13Density * Pipe13Count *
Pipe13Limit)) = 〔0.2248527〕 m `

¢??` Pipe13Velocity = 4 * Pipe13Mass / (Pi * Pipe13Density * Pipe13Count *
Pipe13Bore^2) = 〔34.95418〕 'm/s' `

**HP3 extraction** (HPex; single-phase).

¢` Pipe14Mass = 10.5826135852 'kg/s' `

¢` Pipe14Density = 12.9487516673 'kg/m3' `

¢` Pipe14Count = 1 `

¢` Pipe14Limit = 35 'm/s' `

¢` Pipe14Bore = 0.175 m `

¢??` Pipe14MinBore = sqrt(4 * Pipe14Mass / (Pi * Pipe14Density * Pipe14Count *
Pipe14Limit)) = 〔0.1724263〕 m `

¢??` Pipe14Velocity = 4 * Pipe14Mass / (Pi * Pipe14Density * Pipe14Count *
Pipe14Bore^2) = 〔33.9781〕 'm/s' `

**HP2 extraction** (pump\_bleed2; single-phase).

¢` Pipe15Mass = 17.8892211221 'kg/s' `

¢` Pipe15Density = 7.97321996903 'kg/m3' `

¢` Pipe15Count = 1 `

¢` Pipe15Limit = 35 'm/s' `

¢` Pipe15Bore = 0.3 m `

¢??` Pipe15MinBore = sqrt(4 * Pipe15Mass / (Pi * Pipe15Density * Pipe15Count *
Pipe15Limit)) = 〔0.2856932〕 m `

¢??` Pipe15Velocity = 4 * Pipe15Mass / (Pi * Pipe15Density * Pipe15Count *
Pipe15Bore^2) = 〔31.74134〕 'm/s' `

**HP1 extraction** (pump\_bleed1; two-phase homogeneous screen).

¢` Pipe16Mass = 6.55429701675 'kg/s' `

¢` Pipe16Density = 5.26205482183 'kg/m3' `

¢` Pipe16Count = 1 `

¢` Pipe16Limit = 35 'm/s' `

¢` Pipe16Bore = 0.225 m `

¢??` Pipe16MinBore = sqrt(4 * Pipe16Mass / (Pi * Pipe16Density * Pipe16Count *
Pipe16Limit)) = 〔0.2128661〕 m `

¢??` Pipe16Velocity = 4 * Pipe16Mass / (Pi * Pipe16Density * Pipe16Count *
Pipe16Bore^2) = 〔31.32679〕 'm/s' `

**LP3 extraction** (LP3; single-phase).

¢` Pipe17Mass = 9.57268457708 'kg/s' `

¢` Pipe17Density = 0.771039909151 'kg/m3' `

¢` Pipe17Count = 1 `

¢` Pipe17Limit = 35 'm/s' `

¢` Pipe17Bore = 0.675 m `

¢??` Pipe17MinBore = sqrt(4 * Pipe17Mass / (Pi * Pipe17Density * Pipe17Count *
Pipe17Limit)) = 〔0.6720467〕 m `

¢??` Pipe17Velocity = 4 * Pipe17Mass / (Pi * Pipe17Density * Pipe17Count *
Pipe17Bore^2) = 〔34.69441〕 'm/s' `

**LP2 extraction** (LP2; single-phase).

¢` Pipe18Mass = 22.7215410217 'kg/s' `

¢` Pipe18Density = 0.544582091613 'kg/m3' `

¢` Pipe18Count = 1 `

¢` Pipe18Limit = 35 'm/s' `

¢` Pipe18Bore = 1.25 m `

¢??` Pipe18MinBore = sqrt(4 * Pipe18Mass / (Pi * Pipe18Density * Pipe18Count *
Pipe18Limit)) = 〔1.231993〕 m `

¢??` Pipe18Velocity = 4 * Pipe18Mass / (Pi * Pipe18Density * Pipe18Count *
Pipe18Bore^2) = 〔33.99887〕 'm/s' `

**LP1 extraction** (LP1; two-phase homogeneous screen).

¢` Pipe19Mass = 21.9900073082 'kg/s' `

¢` Pipe19Density = 0.196598883359 'kg/m3' `

¢` Pipe19Count = 1 `

¢` Pipe19Limit = 35 'm/s' `

¢` Pipe19Bore = 2.025 m `

¢??` Pipe19MinBore = sqrt(4 * Pipe19Mass / (Pi * Pipe19Density * Pipe19Count *
Pipe19Limit)) = 〔2.017173〕 m `

¢??` Pipe19Velocity = 4 * Pipe19Mass / (Pi * Pipe19Density * Pipe19Count *
Pipe19Bore^2) = 〔34.72997〕 'm/s' `

**Feed-pump turbine supply** (HP4; single-phase).

¢` Pipe20Mass = 58.1775334302 'kg/s' `

¢` Pipe20Density = 29.1948309528 'kg/m3' `

¢` Pipe20Count = 1 `

¢` Pipe20Limit = 35 'm/s' `

¢` Pipe20Bore = 0.275 m `

¢??` Pipe20MinBore = sqrt(4 * Pipe20Mass / (Pi * Pipe20Density * Pipe20Count *
Pipe20Limit)) = 〔0.2692438〕 m `

¢??` Pipe20Velocity = 4 * Pipe20Mass / (Pi * Pipe20Density * Pipe20Count *
Pipe20Bore^2) = 〔33.55012〕 'm/s' `

**Feed-pump turbine exhaust to DA** (pump\_exhaust; two-phase homogeneous
screen).

¢` Pipe21Mass = 33.7340152913 'kg/s' `

¢` Pipe21Density = 3.32673491508 'kg/m3' `

¢` Pipe21Count = 1 `

¢` Pipe21Limit = 35 'm/s' `

¢` Pipe21Bore = 0.625 m `

¢??` Pipe21MinBore = sqrt(4 * Pipe21Mass / (Pi * Pipe21Density * Pipe21Count *
Pipe21Limit)) = 〔0.6073597〕 m `

¢??` Pipe21Velocity = 4 * Pipe21Mass / (Pi * Pipe21Density * Pipe21Count *
Pipe21Bore^2) = 〔33.05217〕 'm/s' `

HP1, LP1 and feed-pump-turbine exhaust are screened with homogeneous wet-steam
properties; real drainage, erosion, slip and flashing losses need separate
analysis. Reheater return must remain pressurized upstream of its throttle; do
not use its dense-liquid bore for the flashed downstream mixture. HP4 incoming
drains include that return, and all drain/vent/control lines are still unsized.
LP1 extraction is approximately **2.03 m bore** under the 35 m/s assumption; it
needs a short, direct heater connection, not a long small pipe.

## 8. Layout and follow-up

The condenser reserves about 336 m² of equipment plan area across three modules,
before operating aisles or withdrawal space. Four reheater reserves add 192 m².
These are not additive building floor requirements if equipment is stacked, and
are not proof that the existing **45 × 24 × 20 m** turbine building fits. The
storage vessels, elevated water levels, three candidate double-flow LP casings,
both generators, heaters, cranes and laydown space must be arranged explicitly
before setting a new building size.

The present work establishes numerical starting points for that arrangement.
Keep turbine casing and generator envelopes supplier-dependent. Final heater
shells, piping walls, exhaust necks, cooling tower, air-removal system, water
treatment, electrical switchgear, foundations and crane capacities remain
unsized. No purchase specification or construction drawing is implied.

## Sources and verification

*   Selected cycle and cooling cases: [reheat-selection.json][2], [selected Hurmet
    basis][3]; exact source hashes are in [equipment-sizing.json][4].
*   Properties: pinned CoolProp 7.2.0 HEOS water; [official water/IAPWS-95
    reference][5]. The current documentation version may differ from the pinned
    calculation version.
*   [Spirax Sarco, pressurised deaerators][6] gives storage context for typical
    boiler installations. Its typical low-pressure conditions are not adopted
    here; our 0.6 MPa cycle and ten-minute usable-inventory assumption are
    explicit project choices.
*   [Graham, surface condensers][7] describes modular large condensers and
    configuration dependence. Our tube count and envelope are
    calculations/allowances, not Graham product dimensions.
*   [Siemens Energy, utility steam turbines][8] illustrates multiple LP casings and
    down-exhaust arrangements. It does not validate our annulus screen, select
    a model or establish a footprint.

Python checks seven heater heat balances, positive local temperature approaches,
numerical UA convergence, condenser tube geometry and velocity, drive margins,
and usable storage. Hurmet is saved, reopened and recalculated, then compared
to the Python values. `size_equipment.py`, `publish_equipment.py` and
`check_equipment_hurmet.cjs` reproduce this worksheet. Sensitivity checks
change U, cooling head and storage time; no turbine manufacturer performance
map is asserted.

[1]: equipment-sizing-notes.md

[2]: reheat-selection.json

[3]: Selected%20reheat%20and%20wetness%20-%20Hurmet.md

[4]: equipment-sizing.json

[5]: https://coolprop.org/fluid\\\_properties/fluids/Water.html

[6]: https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/pressurised-deaerators?sc\\\_lang=en-GB

[7]: https://graham-mfg.com/solutions/products/surface-condensers/

[8]: https://www.siemens-energy.com/global/en/home/products-services/product/utility-steam-turbines.html

[9]: https://coolprop.org/fluid\_properties/fluids/Water.html

[10]: https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/pressurised-deaerators?sc\_lang=en-GB
