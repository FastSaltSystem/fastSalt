---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Coolant pump estimate

¢` format = "h3" `

Preliminary installation allowance, 10 October 2026. One centrifugal pump per
cold leg, three legs. The owner's requested allowance is **50% above the
steam-generator hydraulic power at the same flow**. Pump efficiency is applied
after that allowance; it is not included in the original generator result.

Inputs below are copied from the three-generator case in [Generator sizing -
Hurmet.md][1]. That worksheet is the numerical basis, retaining its preliminary
correlations and calculated tube length of 19.879 m. The requested 17 m
generator **casing** is a visual layout change; it does not establish a new
tube length or pressure loss. Reconcile the internal generator design with MSU
before selecting equipment.

¢` LegCount = 3 `

¢` SaltMassFlow = 7566.47718 kg/s `

¢` SaltDensity = 1637.93125 kg/m3 `

¢` GeneratorPressureDrop = 190.872791 kPa `

¢` AllowanceFactor = 1.5 `

¢` PumpEfficiency = 0.80 `

¢` MotorEfficiency = 0.96 `

¢` Gravity = 9.80665 m/s2 `

## Per-leg duty

¢%%` VolumeFlow = SaltMassFlow / SaltDensity = 〔4.62〕 m3/s `

¢%%` HourlyFlow = VolumeFlow = 〔16,630〕 m3/h `

¢%%` GeneratorHydraulicPower = GeneratorPressureDrop * VolumeFlow = 〔882〕 kW `

¢%%` DesignPressureRise = AllowanceFactor * GeneratorPressureDrop = 〔286〕 kPa `

¢%%` SaltHead = DesignPressureRise / (SaltDensity * Gravity) = 〔17.8〕 m `

¢%%` HydraulicPower = AllowanceFactor * GeneratorHydraulicPower = 〔1,323〕 kW `

¢%%` ShaftPower = HydraulicPower / PumpEfficiency = 〔1,653〕 kW `

¢%%` ElectricalInput = ShaftPower / MotorEfficiency = 〔1,722〕 kW `

¢` MotorRating = 2000 kW `

¢%%` MotorLoading = ShaftPower / MotorRating = 〔0.827〕 `

¢%%` TotalElectricalInput = LegCount * ElectricalInput = 〔5.17〕 MW `

The 2 MW rating is mechanical motor output capacity, not the predicted
electrical consumption. Estimated consumption applies at the allowance duty
above. A closed circulation loop does not require adding the full generator
elevation as a separate static lift. This estimate does not resolve loop
fittings, manifolds, transients, available suction head, operating speed, or
salt-service construction.

## Pipe bore cross-check

¢` VelocityLimit = 3 m/s `

¢%%` MinimumBore = sqrt(4 * VolumeFlow / (pi * VelocityLimit)) = 〔1.4〕 m `

The existing 1.4 m visible pipe diameter is retained in the graphics. This
result is **clear bore**, so a 1.4 m outside diameter with a finite wall would
not satisfy the stated velocity limit at this flow. Pipe wall and insulation
still need an agreed definition.

## Reserved equipment space

*   Centrifugal pump casing: 2.8 m diameter x 1.8 m high.
*   Vertical motor: 2.8 x 2.4 x 3.2 m, 2 MW output rating.
*   Combined unit: 3.2 x 3.2 m support footprint. The current single-floor
    installation raises the casing on a 2.4 m open steel frame; overall
    installed height is approximately 7.9 m above the floor.

Power fixes a motor rating but does not uniquely fix pump dimensions. The pump
casing envelope is a layout estimate roughly twice the current 1.4 m pipe
diameter; no impeller or certified duty curve is implied. The motor envelope is
rounded up from the order of size of ABB's vertical AMI 560L arrangements
(catalog page 112: L = 2870 mm, HD = 2705 mm, AE = 2155 mm for 6+ poles). This
is an industrial size comparison, not a selected motor or molten-salt pump
assembly. Speed, cooling, bearings, thermal stand-off and maintenance space may
change it. The assumed efficiencies are preliminary; they are not guaranteed
vendor values.

Sources consulted 10 October 2026:

*   [ABB high-voltage engineered induction motor catalog, revision M][2], technical
    ratings and vertical dimension drawings, especially page 112.
*   [ABB modular induction motors][3], general configuration range, including
    vertical mounting.
*   Owner's installation instructions: three cold-leg pumps; generator pressure-loss
    duty plus 50%; 17 m generator casings; 10 October 2026.

The source Calca file and original Hurmet generator calculation are unchanged.
This worksheet is recalculated using Hurmet's `updateAndSave`; numerical
results are also checked independently using SI arithmetic. Graphics parameters
are checked against these inputs when this revision is published; the
installation build checks pump power and rating consistency.

[1]: Generator%20sizing%20-%20Hurmet.md

[2]: https://library.e.abb.com/public/2696e1c5940844b892eb2ada7b2d1313/High%20voltage%20engineered%20induction%20motors%20Technical%20catalog%209AKK103508%5FRevM%5FEN%5Flowres.pdf

[3]: https://www.abb.com/global/en/areas/motion/motors-generators/mv-hv-motors/induction-motors/modular-induction-motors
