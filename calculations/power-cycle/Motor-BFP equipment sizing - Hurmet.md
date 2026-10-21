---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Motor-BFP power-plant equipment — revised working draft

¢` format = "h3" `

11 October 2026. D-029 updates the equipment schedule after the owner authorized
resizing for the motor-driven boiler feed pumps. Prior steam-drive calculations
and presentation snapshots remain preserved. This worksheet is the current
preliminary equipment basis; it does not select vendor equipment.

The external Python calculation imports the checked motor cycle at exactly 5
kPa, 1,500 MW heat input and 26.5/1.0 MPa BFP/condensate discharge. Gross
output is 697.1 MW. Output after BFP and condensate pumps is 671.6 MW; other
station loads remain excluded. Heater properties, densities, coupled flows, UA
and cooling cases are external results. Hurmet checks the sizing arithmetic
below. A cycle-state change requires rerunning Python, not just recalculating
this worksheet.

The 26.5 MPa pressure budget is represented as an adiabatic aggregate pressure
loss after the HP heaters to the unchanged 24 MPa SG inlet. Its earlier
allocation among piping, heaters, SG and main-steam piping has not been
physically resolved. It is a pump-duty allowance, not a validated distributed
pressure network.

## Reheater and generators

¢` Pi = 3.14159265359 `

¢` ReheatUA = 7602044.46093 'W/K' `

¢` ReheatU = 1000 'W.m-2.K-1' `

¢` AreaFactor = 1.2 `

¢` ReheatCount = 4 `

¢%%` ReheatArea = ReheatUA / ReheatU * AreaFactor = 〔9,122〕 'm2' `

¢%%` AreaPerModule = ReheatArea / ReheatCount = 〔2,281〕 'm2' `

¢` ReheatDuty = 281.621146747 MW `

¢%%` DutyPerModule = ReheatDuty / ReheatCount = 〔70.4〕 MW `

Four reheaters now reserve **16 × 3.25 × 3.25 m each**, plus 13 m straight tube
withdrawal. About 2,382 assumed 25.4 mm OD / 12 m tubes per module give a 1.94
m equivalent bundle. U and packing remain assumptions; shell wall, tube wall,
pressure loss and vibration are not designed. At U=500, required surface
doubles; at U=1,500 it is two-thirds. The prior 16 × 3 × 3 m boxes are
superseded.

¢` HPIPPower = 416.459477857 MW `

¢` LPPower = 280.625777196 MW `

¢` PowerFactor = 0.9 `

¢` CapacityFactor = 1.1 `

¢%%` HPIPRequired = HPIPPower / PowerFactor * CapacityFactor = 〔509〕 MW `

¢%%` LPRequired = LPPower / PowerFactor * CapacityFactor = 〔343〕 MW `

The last two calculated numerical values express apparent-power requirements in
**MVA** (Hurmet uses MW as the power-dimension unit). Reserve **550 MVA HP/IP
and 350 MVA LP**. Both include the same 0.90 power factor and 10% capacity
allowance; these are not purchased nameplate ratings. The HP/IP allowance
replaces 500 MVA. Turbine outlines and shaft arrangement remain provisional.

## Pumps and electrical supply

¢` BFPshaft = 23.7099721146 MW `

¢` DriveEfficiency = 0.95 `

¢` DutyPumps = 2 `

¢` MotorRating = 15 MW `

¢%%` BFPinput = BFPshaft / DriveEfficiency = 〔25〕 MW `

¢%%` ShaftPerPump = BFPshaft / DutyPumps = 〔11.9〕 MW `

¢%%` ElectricPerPump = BFPinput / DutyPumps = 〔12.5〕 MW `

¢` MotorPowerFactor = 0.95 `

¢` ElectricalMargin = 1.1 `

¢%%` RatedInputPerTrain = MotorRating / DriveEfficiency = 〔15.8〕 MW `

¢%%` TransformerRequirement = RatedInputPerTrain / MotorPowerFactor *
ElectricalMargin = 〔18.3〕 MW `

Reserve **three 15 MW motor/pump trains, two duty and one standby**. Each BFP
supply train has a **20 MVA transformer allowance**, above the calculated MVA
requirement. The allowance uses assumed 0.95 supply power factor and 95%
combined drive efficiency; vendor motor/drive maps, voltage, harmonics, losses
and protection are unresolved. The idle standby train is not counted at full
operating consumption. No full-station N+1 electrical capability is claimed.
Reserve a **20 × 10 × 7 m annex** for BFP electrical equipment; partition, fire
separation, ventilation and transformer placement remain to design.

BFP hydraulic sizes stay at 0.783 m³/s total and 26.5 MPa discharge. Retain 355
kW condensate motors (three 50% pumps), 3.5 MW cooling-water motor allowances
(three 50% pumps at assumed 20 m head), and two 4.5 m ID × 22 m straight
deaerator storage shells. Condensate load is 0.537 MW; cooling-water load is
5.51 MW. Even subtracting both water-pump systems and BFP leaves 666.1 MW
**before remaining station loads**, not final net export.

## Heater and condenser schedule

HP2 and HP1 now receive main-IP bleeds at about 435°C and 371°C. Their duties
are similar but their inlet/desuperheating regions require redesign. The
premixed-stream areas below are proxies, not separate-zone designs. LP3
operates at 0.12186 MPa; retain its former larger box pending detailed design.

| Heater | Duty MW | Area m² | Bleed °C |
|--------|---------|---------|----------|
| HP4    | 206.75  | 5363    | 377.6    |
| HP3    | 90.15   | 3612    | 253.0    |
| HP2    | 66.12   | 3084    | 434.5    |
| HP1    | 36.21   | 2225    | 370.8    |
| LP3    | 9.77    | 755     | 146.9    |
| LP2    | 52.81   | 2038    | 129.7    |
| LP1    | 53.70   | 2047    | 69.1     |
{.grid colWidths="100 110 110 110"}

Retain three **16 × 7 × 9 m condenser envelopes**, each with 13 m withdrawal,
38517 m² total surface and the same 23.76 m³/s cooling flow. Duties become
809.4 MW at 5 kPa, 832.1 MW at 30°C inlet and 843.4 MW at 35°C inlet. The
latter two use their recalculated backpressures. Six LP exhaust flows remain a
candidate; total volumetric flow is 9329 m³/s at 5 kPa. The final heat sink and
cooling-water pump location remain outside the hall arrangement.

## Revised pipe-bore register

Bores are internal, with walls, insulation and supports additional. Keep
existing bore allowances where the new flow is lower. Increase bores that fail
the prior velocity limits in the 5 kPa reference or any of the three cooling
cases. The former pump-turbine supply is removed; its exhaust service is
replaced by main-IP outlet steam to the deaerator. No reactor/SG main-header
flow change is introduced.

+---------------------------+-------+---------+--------------+
| Service                   | Count | Bore mm | Velocity m/s |
+===========================+=======+=========+==============+
| Main steam header         | 1     | 725     | 23.41        |
| (existing bore)           |       |         |              |
+---------------------------+-------+---------+--------------+
| Main steam branch (each   | 1     | 425     | 22.71        |
| of 3)                     |       |         |              |
+---------------------------+-------+---------+--------------+
| HP admission after reheat | 1     | 550     | 28.76        |
| split                     |       |         |              |
+---------------------------+-------+---------+--------------+
| Reheater heating supply   | 1     | 350     | 29.44        |
+---------------------------+-------+---------+--------------+
| Reheater heating return   | 1     | 500     | 2.76         |
+---------------------------+-------+---------+--------------+
| Cold reheat               | 2     | 775     | 39.92        |
+---------------------------+-------+---------+--------------+
| Hot reheat                | 2     | 1000    | 39.29        |
+---------------------------+-------+---------+--------------+
| IP-to-LP crossover        | 3     | 1400    | 39.38        |
+---------------------------+-------+---------+--------------+
| Feedwater header          | 1     | 650     | 2.81         |
| (existing bore)           |       |         |              |
+---------------------------+-------+---------+--------------+
| Feedwater branch (each of | 1     | 375     | 2.81         |
| 3)                        |       |         |              |
+---------------------------+-------+---------+--------------+
| Deaerator to feed pumps   | 2     | 500     | 1.99         |
+---------------------------+-------+---------+--------------+
| Condensate through LP     | 1     | 475     | 2.34         |
| heater bank               |       |         |              |
+---------------------------+-------+---------+--------------+
| HP4 extraction            | 1     | 225     | 27.13        |
+---------------------------+-------+---------+--------------+
| HP3 extraction            | 1     | 175     | 26.97        |
+---------------------------+-------+---------+--------------+
| HP2 extraction            | 1     | 325     | 32.60        |
+---------------------------+-------+---------+--------------+
| HP1 extraction            | 1     | 225     | 33.43        |
+---------------------------+-------+---------+--------------+
| LP3 extraction            | 1     | 675     | 18.46        |
+---------------------------+-------+---------+--------------+
| LP2 extraction            | 1     | 1250    | 34.08        |
+---------------------------+-------+---------+--------------+
| LP1 extraction            | 1     | 2025    | 34.93        |
+---------------------------+-------+---------+--------------+
| IP outlet steam to        | 1     | 725     | 34.77        |
| deaerator                 |       |         |              |
+---------------------------+-------+---------+--------------+
{.grid colWidths="280 60 80 120"}

Executable velocity and constant-property pressure-loss screens follow. Each
uses the reference density/volume imported from CoolProp, 40 m route length,
Darcy f=0.015 and K=5. These are not actual routed losses. Wet LP1 uses
homogeneous density. Drain, vent, startup, thermal expansion, nozzle and relief
services remain unsized; pressure walls and insulation are not inferred from
these bores.

¢` RouteLength = 40 m `

¢` DarcyFactor = 0.015 `

¢` LocalK = 5 `

**P1: Main steam header (existing bore)**

¢` Q1 = 9.66570638759 'm3/s' `

¢` D1 = 0.725 m `

¢` N1 = 1 `

¢` Rho1 = 73.6283741527 'kg/m3' `

¢%%` V1 = 4 * Q1 / (N1 * Pi * D1^2) = 〔23.4〕 'm/s' `

¢%%` Drop1 = (DarcyFactor * RouteLength / D1 + LocalK) * Rho1 * V1^2 / 2 = 〔118〕 kPa `

**P2: Main steam branch (each of 3)**

¢` Q2 = 3.2219021292 'm3/s' `

¢` D2 = 0.425 m `

¢` N2 = 1 `

¢` Rho2 = 73.6283741527 'kg/m3' `

¢%%` V2 = 4 * Q2 / (N2 * Pi * D2^2) = 〔22.7〕 'm/s' `

¢%%` Drop2 = (DarcyFactor * RouteLength / D2 + LocalK) * Rho2 * V2^2 / 2 = 〔122〕 kPa `

**P3: HP admission after reheat split**

¢` Q3 = 6.83302582013 'm3/s' `

¢` D3 = 0.55 m `

¢` N3 = 1 `

¢` Rho3 = 73.6283741527 'kg/m3' `

¢%%` V3 = 4 * Q3 / (N3 * Pi * D3^2) = 〔28.8〕 'm/s' `

¢%%` Drop3 = (DarcyFactor * RouteLength / D3 + LocalK) * Rho3 * V3^2 / 2 = 〔185〕 kPa `

**P4: Reheater heating supply**

¢` Q4 = 2.83268056746 'm3/s' `

¢` D4 = 0.35 m `

¢` N4 = 1 `

¢` Rho4 = 73.6283741527 'kg/m3' `

¢%%` V4 = 4 * Q4 / (N4 * Pi * D4^2) = 〔29.4〕 'm/s' `

¢%%` Drop4 = (DarcyFactor * RouteLength / D4 + LocalK) * Rho4 * V4^2 / 2 = 〔214〕 kPa `

**P5: Reheater heating return**

¢` Q5 = 0.540958417986 'm3/s' `

¢` D5 = 0.5 m `

¢` N5 = 1 `

¢` Rho5 = 385.54842247 'kg/m3' `

¢%%` V5 = 4 * Q5 / (N5 * Pi * D5^2) = 〔2.76〕 'm/s' `

¢%%` Drop5 = (DarcyFactor * RouteLength / D5 + LocalK) * Rho5 * V5^2 / 2 =
〔9.07〕 kPa `

**P6: Cold reheat**

¢` Q6 = 37.6657853091 'm3/s' `

¢` D6 = 0.775 m `

¢` N6 = 2 `

¢` Rho6 = 12.2979105765 'kg/m3' `

¢%%` V6 = 4 * Q6 / (N6 * Pi * D6^2) = 〔39.9〕 'm/s' `

¢%%` Drop6 = (DarcyFactor * RouteLength / D6 + LocalK) * Rho6 * V6^2 / 2 =
〔56.6〕 kPa `

**P7: Hot reheat**

¢` Q7 = 61.720054589 'm3/s' `

¢` D7 = 1 m `

¢` N7 = 2 `

¢` Rho7 = 7.50502349048 'kg/m3' `

¢%%` V7 = 4 * Q7 / (N7 * Pi * D7^2) = 〔39.3〕 'm/s' `

¢%%` Drop7 = (DarcyFactor * RouteLength / D7 + LocalK) * Rho7 * V7^2 / 2 =
〔32.4〕 kPa `

**P8: IP-to-LP crossover**

¢` Q8 = 181.877480368 'm3/s' `

¢` D8 = 1.4 m `

¢` N8 = 3 `

¢` Rho8 = 2.26865916018 'kg/m3' `

¢%%` V8 = 4 * Q8 / (N8 * Pi * D8^2) = 〔39.4〕 'm/s' `

¢%%` Drop8 = (DarcyFactor * RouteLength / D8 + LocalK) * Rho8 * V8^2 / 2 =
〔9.55〕 kPa `

**P9: Feedwater header (existing bore)**

¢` Q9 = 0.930885076075 'm3/s' `

¢` D9 = 0.65 m `

¢` N9 = 1 `

¢` Rho9 = 764.509244639 'kg/m3' `

¢%%` V9 = 4 * Q9 / (N9 * Pi * D9^2) = 〔2.81〕 'm/s' `

¢%%` Drop9 = (DarcyFactor * RouteLength / D9 + LocalK) * Rho9 * V9^2 / 2 =
〔17.8〕 kPa `

**P10: Feedwater branch (each of 3)**

¢` Q10 = 0.310295025358 'm3/s' `

¢` D10 = 0.375 m `

¢` N10 = 1 `

¢` Rho10 = 764.509244639 'kg/m3' `

¢%%` V10 = 4 * Q10 / (N10 * Pi * D10^2) = 〔2.81〕 'm/s' `

¢%%` Drop10 = (DarcyFactor * RouteLength / D10 + LocalK) * Rho10 * V10^2 / 2 =
〔19.9〕 kPa `

**P11: Deaerator to feed pumps**

¢` Q11 = 0.783265592089 'm3/s' `

¢` D11 = 0.5 m `

¢` N11 = 2 `

¢` Rho11 = 908.593781654 'kg/m3' `

¢%%` V11 = 4 * Q11 / (N11 * Pi * D11^2) = 〔1.99〕 'm/s' `

¢%%` Drop11 = (DarcyFactor * RouteLength / D11 + LocalK) * Rho11 * V11^2 / 2 =
〔11.2〕 kPa `

**P12: Condensate through LP heater bank**

¢` Q12 = 0.414642972211 'm3/s' `

¢` D12 = 0.475 m `

¢` N12 = 1 `

¢` Rho12 = 995.116376062 'kg/m3' `

¢%%` V12 = 4 * Q12 / (N12 * Pi * D12^2) = 〔2.34〕 'm/s' `

¢%%` Drop12 = (DarcyFactor * RouteLength / D12 + LocalK) * Rho12 * V12^2 / 2 =
〔17.1〕 kPa `

**P13: HP4 extraction**

¢` Q13 = 1.07880931284 'm3/s' `

¢` D13 = 0.225 m `

¢` N13 = 1 `

¢` Rho13 = 29.1948309528 'kg/m3' `

¢%%` V13 = 4 * Q13 / (N13 * Pi * D13^2) = 〔27.1〕 'm/s' `

¢%%` Drop13 = (DarcyFactor * RouteLength / D13 + LocalK) * Rho13 * V13^2 / 2 =
〔82.4〕 kPa `

**P14: HP3 extraction**

¢` Q14 = 0.64859276424 'm3/s' `

¢` D14 = 0.175 m `

¢` N14 = 1 `

¢` Rho14 = 12.9487516673 'kg/m3' `

¢%%` V14 = 4 * Q14 / (N14 * Pi * D14^2) = 〔27〕 'm/s' `

¢%%` Drop14 = (DarcyFactor * RouteLength / D14 + LocalK) * Rho14 * V14^2 / 2 =
〔39.7〕 kPa `

**P15: HP2 extraction**

¢` Q15 = 2.70443924361 'm3/s' `

¢` D15 = 0.325 m `

¢` N15 = 1 `

¢` Rho15 = 4.98531509919 'kg/m3' `

¢%%` V15 = 4 * Q15 / (N15 * Pi * D15^2) = 〔32.6〕 'm/s' `

¢%%` Drop15 = (DarcyFactor * RouteLength / D15 + LocalK) * Rho15 * V15^2 / 2 =
〔18.1〕 kPa `

**P16: HP1 extraction**

¢` Q16 = 1.32911486864 'm3/s' `

¢` D16 = 0.225 m `

¢` N16 = 1 `

¢` Rho16 = 3.41775618903 'kg/m3' `

¢%%` V16 = 4 * Q16 / (N16 * Pi * D16^2) = 〔33.4〕 'm/s' `

¢%%` Drop16 = (DarcyFactor * RouteLength / D16 + LocalK) * Rho16 * V16^2 / 2 =
〔14.6〕 kPa `

**P17: LP3 extraction**

¢` Q17 = 6.60461748362 'm3/s' `

¢` D17 = 0.675 m `

¢` N17 = 1 `

¢` Rho17 = 0.635284755851 'kg/m3' `

¢%%` V17 = 4 * Q17 / (N17 * Pi * D17^2) = 〔18.5〕 'm/s' `

¢%%` Drop17 = (DarcyFactor * RouteLength / D17 + LocalK) * Rho17 * V17^2 / 2 =
〔0.637〕 kPa `

**P18: LP2 extraction**

¢` Q18 = 41.8276129554 'm3/s' `

¢` D18 = 1.25 m `

¢` N18 = 1 `

¢` Rho18 = 0.543510637661 'kg/m3' `

¢%%` V18 = 4 * Q18 / (N18 * Pi * D18^2) = 〔34.1〕 'm/s' `

¢%%` Drop18 = (DarcyFactor * RouteLength / D18 + LocalK) * Rho18 * V18^2 / 2 =
〔1.73〕 kPa `

**P19: LP1 extraction**

¢` Q19 = 112.491720811 'm3/s' `

¢` D19 = 2.025 m `

¢` N19 = 1 `

¢` Rho19 = 0.196485292687 'kg/m3' `

¢%%` V19 = 4 * Q19 / (N19 * Pi * D19^2) = 〔34.9〕 'm/s' `

¢%%` Drop19 = (DarcyFactor * RouteLength / D19 + LocalK) * Rho19 * V19^2 / 2 =
〔0.635〕 kPa `

**P20: IP outlet steam to deaerator**

¢` Q20 = 14.3553407515 'm3/s' `

¢` D20 = 0.725 m `

¢` N20 = 1 `

¢` Rho20 = 2.26865916018 'kg/m3' `

¢%%` V20 = 4 * Q20 / (N20 * Pi * D20^2) = 〔34.8〕 'm/s' `

¢%%` Drop20 = (DarcyFactor * RouteLength / D20 + LocalK) * Rho20 * V20^2 / 2 =
〔7.99〕 kPa `

## First dimensional building check

The layout reserves a **66 × 40 × 28 m main hall** and a **20 × 10 × 7 m BFP
electrical annex**. Turbines/generators are at +12 m above the common equipment
floor; condenser tops are +9.5 m. The lowest deaerator water level remains +14

 m.  Storage boxes include 3 m beyond the 22 m straight shells for heads. A
    provisional crane underside at +25 m gives at least 6 m above the turbine
    boxes, with roof at +28 m. Crane, floors, supports and lifting loads are
    not designed.


Tube withdrawal uses 13 m volumes beyond the north ends of condenser/reheater
boxes, extending through removable wall panels onto a 7 m external apron.
Heater withdrawal is directed south onto a 12 m apron. The first old 45 × 24 ×
20 m reservation does not contain this arrangement. The new dimensions are a
workable reservation for this particular placement, not a proven minimum. Most
of the increase is the first inclusion of actual equipment/access volumes, not
a consequence of changing the BFP drive alone.

The companion `turbine_layout.py` / `turbine-layout.json` checks 29 equipment
boxes and 16 service volumes for selected intersections, wall containment and
vertical separation. A dimensioned plan accompanies the Blender draft. Pipe
corridors have not been routed; structural columns, deck openings, stairs,
egress, crane reach, rotor handling and full installation transport remain
open. Thus passing box checks does not establish that a complete plant fits.

## Reproduction and sources

Use pinned `requirements.txt` and run `python size_motor_equipment.py`, `python
publish_motor_equipment.py`, then `node check_motor_equipment_hurmet.cjs` with
HURMET_ENGINE and TEMML_ENGINE set as in the cycle README. The JSON records
input hashes; Python screens all four operating cases. Hurmet checks
power/capacity/area and every pipe velocity/loss after save/reopen, plus
reheater-U and drive-efficiency sensitivities.

Sources: [motor-drive heat balance][1], [historical sizing assumptions][2], and
their linked CoolProp/property references. No new vendor outlines or verified
material allowables are introduced by this revision.

[1]: BFP%20drive%20comparison%20-%20Hurmet.md

[2]: Power%20plant%20equipment%20sizing%20-%20Hurmet.md
