# Pump estimate verification

10 October 2026. Source: [original generator worksheet](Generator%20sizing%20-%20Hurmet.md).
Source SHA-256: `c43db3790ba8e3346253e4c9faf00d4ee643b1f348d8aad0e25c39083a359c04`.

[Pump worksheet](Coolant%20pump%20estimate%20-%20Hurmet.md) was recalculated with the
local Hurmet JavaScript `updateAndSave` implementation (`hurmet.version = 0.1.1`).
Unit-aware cells use the double-question-mark calculation mode. SI arithmetic
independently checks all eleven output cells to their saved rounding precision.
The source generator worksheet is unchanged.

Per leg: 4.619533 m³/s, 190.872791 kPa generator pressure loss, 286.309187 kPa
with the 50% allowance, 17.82456 m of coolant head, 1322.61468 kW hydraulic,
1653.26835 kW shaft at 80% pump efficiency, 1722.15453 kW electrical at 96%
motor efficiency. The provisional 2000 kW motor is at 82.6634% output loading.
Three-leg electrical input at this allowance duty is 5.166464 MW.

The dimension envelope is an engineering layout assumption informed by the ABB
catalog, not an equipment selection. The 17 m casing has not been substituted
for the generator's calculated tube length. Header, nozzle and external piping
losses are represented only by the requested allowance, not individually modeled.

Graphics inputs and saved pump results are compared against the worksheet as
part of this publication check. Build-time checks additionally verify three
pump connections, motor rating greater than demand, and storage-opening clearance.
