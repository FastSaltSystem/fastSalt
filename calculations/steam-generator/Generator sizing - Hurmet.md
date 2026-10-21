---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Generator sizing

¢` format = "h3" `

_Fast Salt System — preliminary steam-generator calculations, converted from
Calca._

Open this Markdown file in **Hurmet → File → Open**. Click a calculation to edit
it, then press **Enter** to apply the change. For a simple trial, change `NGen`
from 3 to 4 and observe the heat load and flow per generator; change it back to
3 afterward. All equations below are live calculations.

The inputs, assumptions, correlations, and explanatory reasoning are retained
from the supplied worksheet. This is a format conversion, not a revision of the
design calculations. Conversion notes are at the end.

Calculations for a combined steam generator and emergency air cooler.

Number of steam generators / emergency air coolers.

¢` NGen = 3 `

¢` ReactorPower = 1500 MW `

¢%%` Q_Gen = ReactorPower / NGen = 〔500〕 MW `

### Temperature distribution

Assume  a temperature distribution: Molten salt  enters the top and exits the
bottom.

¢` TSaltHot = 875 K `

¢` TSaltCool = 810 K `

¢%%` SaltAveT = (TSaltHot +TSaltCool)/2 = 〔843〕 K `

Supercritical water enters the bottom and exits the top.

¢` TStmCool = 560 K `

¢` TStmHot = 830 K `

Temperature  differences at top and bottom.

¢%%` DTtop = TSaltHot - TStmHot = 〔45〕 K `

¢%%` DTbot = TSaltCool - TStmCool = 〔250〕 K `

Average temperature difference.

¢%%` DTAve = (DTtop + DTbot)/2 = 〔148〕 K `

The log mean temperature difference.

¢` function LMTD(Th1, Th2, Tc1, Tc2)
    return ((Th2-Tc2)-(Th1-Tc1))/ln((Th2-Tc2)/(Th1-Tc1))
end `

¢%%` DT_lmdt = LMTD(TSaltHot, TSaltCool, TStmHot, TStmCool) = 〔120〕 K `

### Coolant properties (MgCl2-KCL-NCl at w/o 45.9, 38.9, 15.1).

¢` function CoolantDensityF(temp)
    return 2112.68 'kg/m3' - 0.5635 'kg.m-3.K-1' * temp
end `

¢` function CoolantHeatCapacityF(temp)
    return 1.43788 'J.g-1.K-1' - 0.0005 'J.g-1.K-2' * temp
end `

¢` function CoolantViscosityF(temp)
    return 0.00070645 'kg.m-1.s-1' * exp(1204.1 'K' / temp)
end `

¢` function CoolantHeatCondF(temp)
    return (0.65318 - 2.6e-4 * temp/(1 'K')) * 1 'W.m-1.K-1'
end `

¢` CoolantLiquidusT = 674 K `

Coolant density at average temperature.

¢%%` CoolantDensity = CoolantDensityF(SaltAveT) = 〔1,638〕 kg/m3 `

¢%%` CoolantHeatCapacity = CoolantHeatCapacityF(SaltAveT) = 〔1.02〕 J.g-1.K-1 `

¢%%` CoolantViscosity = CoolantViscosityF(SaltAveT) = 〔0.00295〕 kg.m-1.s-1 `

¢%%` CoolantHeatCond = CoolantHeatCondF(SaltAveT) = 〔0.434〕 W.m-1.K-1 `

¢%%` SaltMassFlow = Q_Gen/(CoolantHeatCapacity*(TSaltHot-TSaltCool)) = 〔7,566〕
kg/s `

Assumed molten salt tube's geometry.

¢` TubeID = 1.4 cm `

¢` TubeThickness = 1 mm `

¢%%` TubeOD = TubeID + 2 * TubeThickness = 〔1.6〕 cm `

¢%%` TubeArea = (pi/4)*TubeID^2 = 〔1.54〕 cm2 `

### Number of coolant tubes needed.

Calculate the minimum number of tubes needed based on the heat capacity of the
molten salt coolant.  This is based on limiting the coolant velocity through
the tubes .

¢` VelocityLimit = 3 'm/s' `

¢%%` AreaNeeded =SaltMassFlow/CoolantDensity/VelocityLimit = 〔1.54〕 m2 `

¢%%` TubesNeeded = ceil(AreaNeeded/TubeArea) = 〔10,004〕 `

## Tubes Used

Set the number of tubes to use.  Setting higher than the needed amount can
reduce the height of the generator.

¢%%` TubesUsed = max(TubesNeeded, 12000) = 〔12,000〕 `

The tubes can be arranged in different configurations, depending on how many
tubes are put in each row. This sets the generator to a square profile.

¢%%` TubesPerRowSq = ceil(sqrt(2* TubesUsed) ) = 〔155〕 `

¢%%` TubesPerRow = TubesPerRowSq = 〔155〕 `

¢%%` NRows = ceil(TubesUsed/TubesPerRow) = 〔78〕 `

¢%%` NTubes = TubesPerRow * NRows = 〔12,090〕 `

¢%%` SaltWidth = NRows * TubeOD = 〔1.25〕 m `

## Generator profile

¢%%` GenDepth = TubesPerRow * TubeOD = 〔2.48〕 m `

¢%%` GenDepth = 〔8.14〕 ft `

Assuming same size tubes for steam:

¢%%` GenWidth = 2 * SaltWidth = 〔2.5〕 m `

¢%%` GenWidth = 〔8.19〕 ft `

### Heat transfer per side of tube

Heat transfer in this generator is from both sides of each row of tubes.

¢` Sides = 2 `

The amount of heat to transfer on each side of a tube is:

¢%%` Q_Side = Q_Gen/NTubes/Sides = 〔20.7〕 kW `

### Radiative heat transfer.

Check to see how well heat is transferred by radiated heat due to temperature.
The Stefan-Boltzman constant:

¢%%` sigma = 5.669e-8 'W.m-2.K-4' = 〔5.67e-8〕 W.m-2.K-4 `

Basic emissivity of stainless steel.

¢` eSS = 0.54 `

Assuming two infinite flat planes facing each other:

¢%%` qTop_A = (sigma * (TSaltHot^4 - TStmHot^4)) / ((2/eSS) -1) = 〔2.34〕 kW/m2 `

¢%%` qBot_A = (sigma * (TSaltCool^4 - TStmCool^4)) / ((2/eSS) -1) = 〔6.96〕 kW/m2 `

Radiation heat transfer is larger at the bottom than the top.

Use the average transfer rate for the height of generator needed:

¢%%` qRadAve_A =((qTop_A + qBot_A)/2) = 〔4.65〕 kW/m2 `

¢%%` QRadPerL = qRadAve_A * GenDepth * NRows * Sides = 〔1.8〕 MW/m `

¢%%` RadLength = Q_Gen / QRadPerL = 〔278〕 m `

This is impractically large so we need conduction and / or convection to bring
the size down. We can also bring the height down by increasing the number of
tubes.

### Air conductivity

The air  gap has a diamond shape between two sets of circular tubes.  It ranges
from zero to TubeOD.  Assume the gap is the average.

¢%%` AirK = 0.024 'W.m-1.K-1' = 〔0.024〕 W.m-1.K-1 `

¢%%` AirGap = TubeOD/2 = 〔0.8〕 cm `

¢%%` qAirK_A = AirK * (DT_lmdt)/AirGap = 〔0.359〕 kW/m2 `

This is significantly smaller (\< 1/10) than the radiation heat transfer.

### Air convection

If we assume, like molten salt, that convection improves heat transfer by a
factor of 6 we get:

¢%%` qAirConv_A = 6 * qAirK_A = 〔2.15〕 kW/m2 `

This is still lower (\~ 1/2) than radiation heat transfer.

## Steel conduction

Q/A = (k/dx) DT.  A = contact width \* length.  Solving for length gets you: L =
(dx/w)(Q/k DT) .  For conduction  we can calculate a nominal length which is
Q/kDT.  The actual length needed is just the nominal length times the aspect
ratio: (dx/width).

¢%%` SteelCond = 19 'W.m-1.K-1' = 〔19〕 W.m-1.K-1 `

¢%%` NSurfaces = NTubes * 2 = 〔24,180〕 `

Heat per degree K per side.

¢%%` Q_K_S = Q_Side / DT_lmdt = 〔0.173〕 kW/K `

¢%%` NominalLength = Q_K_S / SteelCond = 〔9.1〕 m `

### Tubes touching

Let's say the width of contact width between tubes can be 1/10 the diameter.

¢%%` touchW = TubeOD/10 = 〔0.16〕 cm `

¢%%` touchTh = 2 * TubeThickness = 〔2〕 mm `

¢%%` touchAspect = touchTh/touchW = 〔1.25〕 `

¢%%` touchLength = NominalLength*touchAspect = 〔11.4〕 m `

### Tubes with saddle pads:

Assume saddle pads that are: 3/4 the diameter in width and half of thickest:

¢%%` saddleW = 0.75 * TubeOD = 〔1.2〕 cm `

¢%%` saddleTh = 2*TubeThickness + (TubeOD/3)/2 = 〔4.67〕 mm `

¢%%` saddleAspect = saddleTh/saddleW = 〔0.389〕 `

¢%%` saddleLength = NominalLength * saddleAspect = 〔3.54〕 m `

Now this is getting more reasonable.

### Indented round tubes (somewhat square)

¢` sqContactW = 8 mm `

¢` sqContactTh = 2 mm `

¢%%` sqAspect = sqContactTh / sqContactW = 〔0.25〕 `

Best height to width ratio.

¢%%` sqLength = NominalLength * sqAspect = 〔2.28〕 m `

Effective resistance is contact thickness divided by conductivity.

¢%%` sqContactR = sqContactTh / SteelCond = 〔0.105〕 m2.K/kW `

## Fluid heat transfer

### Salt side

¢%%` saltVel = SaltMassFlow/NTubes/CoolantDensity/TubeArea = 〔2.48〕 m/s `

¢` function ReynoldsNumber(density, velocity, diameter, viscosity)
    return density * velocity * diameter / viscosity
end `

Function calculates heat transfer coefficient from coolant bulk flow to chamber wall.

¢` function BulkToWallDeltaH(heatCap, viscosity, heatCond, reyNum, diameter)
    prantdlNum = heatCap * viscosity / heatCond
    nusseltNum = 0.0266 * reyNum^0.805 * prantdlNum^(1/3)
    return nusseltNum * heatCond / diameter
end `

¢%%` saltReyn = ReynoldsNumber(CoolantDensity, saltVel,TubeID, CoolantViscosity)
= 〔19,296〕 `

¢%%` saltBulkH = BulkToWallDeltaH(CoolantHeatCapacity, CoolantViscosity,
CoolantHeatCond, saltReyn, TubeID) = 〔4.43〕 kW.m-2.K-1 `

The resistance is just the inverse of the heat transfer coefficient.

¢%%` saltR = 1 / saltBulkH = 〔0.226〕 m2.K/kW `

The length needed can be calculated as the heat per side divided by the
temperature difference and the number of sides it is distributed over, divided
by the heat transfer coefficient times the wall width.

¢%%` saltLength = Q_K_S * saltR / sqContactW = 〔4.89〕 m `

### Steam side

Values from https://www.ski-gmbh.com/swa/tools/steam, and
https://www.thermopedia.com/de/content/1150/ . Pressure is 24 MPa for both
inlet and exit.

¢` ExitEnthalpy = 3372.493 'kJ/kg' `

¢` InletEnthalpy = 1264.452 'kJ/kg' `

¢%%` SteamMassFlow = Q_Gen/(ExitEnthalpy-InletEnthalpy) = 〔237〕 kg/s `

Steam exit side.

¢%%` ExitDensity = 1 / (0.01358536 'm3/kg') = 〔73.6〕 kg/m3 `

¢%%` ExitViscosity = 3.392e-5 'kg.m-1.s-1' = 〔0.0000339〕 kg.m-1.s-1 `

¢%%` ExitConduct = 100 'mW.m-1.K-1' = 〔0.1〕 W.m-1.K-1 `

¢%%` ExitHeatCapacity = 2980.664 'J.kg-1.K-1' = 〔2,981〕 J.kg-1.K-1 `

¢%%` ExitVelocity = SteamMassFlow/ExitDensity/(TubeArea*NTubes) = 〔1.73〕 m/s `

¢%%` ExityReyn = ReynoldsNumber(ExitDensity, ExitVelocity, TubeID,
ExitViscosity) = 〔52,601〕 `

¢%%` ExitBulkH = BulkToWallDeltaH(ExitHeatCapacity, ExitViscosity, ExitConduct,
ExityReyn, TubeID) = 〔1.2〕 kW.m-2.K-1 `

¢%%` ExitR = 1 / ExitBulkH = 〔0.83〕 m2.K/kW `

Values for inlet side :

¢` InletDensity = 764.494 'kg/m3' `

¢%%` InletViscocity = 9.635e-5 'kg.m-1.s-1' = 〔0.0000963〕 kg.m-1.s-1 `

¢%%` InletConduct = 600 'mW.m-1.K-1' = 〔0.6〕 W.m-1.K-1 `

¢%%` InletHeatCapacity = 5012.22 'J.kg-1.K-1' = 〔5,012〕 J.kg-1.K-1 `

¢%%` InletVelocity = SteamMassFlow/InletDensity/(TubeArea*NTubes) = 〔0.167〕 m/s `

¢%%` InletReyn = ReynoldsNumber(InletDensity, InletVelocity, TubeID,
InletViscocity) = 〔18,518〕 `

¢%%` InletBulkH = BulkToWallDeltaH(InletHeatCapacity, InletViscocity,
InletConduct, InletReyn, TubeID) = 〔2.89〕 kW.m-2.K-1 `

¢%%` InletR = 1 / InletBulkH = 〔0.346〕 m2.K/kW `

¢%%` SteamAveR = (InletR + ExitR)/2 = 〔0.588〕 m2.K/kW `

¢%%` steamlength = Q_K_S * SteamAveR/ sqContactW = 〔12.7〕 m `

Add resistances in series: salt, contact, steam.

¢%%` allThreeR = saltR + sqContactR + SteamAveR = 〔0.919〕 m2.K/kW `

¢%%` tubeLength = Q_K_S * allThreeR / sqContactW = 〔19.9〕 m `

¢%%` AddedLengths = steamlength + saltLength + sqLength = 〔19.9〕 m `

¢%%` tubeLength = 〔65.2〕 ft `

¢%%` tubeLengthTotal = NGen * 2 * NTubes * tubeLength = 〔1,442〕 km `

## Salt pressure Drop

¢` function PressureDrop(length, diameter, velocity, roughness, density, viscosity)
    reyNum = density * velocity * diameter / viscosity
    frictionFactor = (8/6.0516) * ln(roughness/diameter + (7/reyNum)^0.9)^(-2)
    kineticP = 0.5 * density * velocity^2
    return frictionFactor * (length/diameter) * kineticP
end `

¢` SSRoughness = 0.001 mm `

The pressure drop over the generator because of flow resistance in the
generator:

¢%%` CoolantPressureDrop = PressureDrop(tubeLength, TubeID, saltVel,
SSRoughness,CoolantDensity, CoolantViscosity) = 〔191〕 kPa `

¢%%` CoolantPressureDrop = 〔27.7〕 psi `

¢%%` CoolantPressureDrop = 〔63.9〕 ftH₂O `

Since the pressure head is near or over 50 feet we will require some kind of
centrifugal pump.

### Generator pump power

The power required to push the coolant through each generator.

¢%%` GenPumpPower=CoolantPressureDrop* SaltMassFlow/CoolantDensity = 〔882〕 kW `

¢%%` GenPumpPower = 〔1,182〕 hp `

### Buoyancy

Pressure across generator due to height and density change in salt.

¢%%` Buoncy = tubeLength*(CoolantDensityF(TSaltCool) - CoolantDensityF(TSaltHot)
) * 9.8 'N/kg' = 〔7.14〕 kPa `

## Conversion notes

*   Calca functions were translated into Hurmet `function … return … end` cells.
    Inside `PressureDrop`, the Reynolds-number expression is written directly
    because separately defined functions are not visible within that function’s
    local scope. Unit-aware evaluation is used for derived quantities;
    displayed results are rounded while subsequent equations use the full
    calculated values.
*   The two radiative-flux expressions requested `kW/m^-2` in the source but
    displayed `kW/m²`. Their output unit is `kW/m²` here, matching the
    expressions and the original results.
*   Compound units are written as products with negative exponents where needed: for
    example, `W.m-1.K-1` means W/(m·K). The density coefficient is explicitly
    per kelvin, and the thermal-conductivity function explicitly divides
    temperature by 1 K.
*   The coolant composition label and correlation coefficients are retained as
    supplied, including the source label “MgCl2-KCL-NCl.” The sixfold
    air-convection multiplier, heat-transfer correlation, and pressure-drop
    correlation are also retained. The source describes its pressure-drop
    expression as a Churchill factor “good to 2%”; this conversion does not
    establish that claim.
*   Original variable spellings such as `ExityReyn`, `InletViscocity`, and `Buoncy`
    are retained so the two files can be compared easily. Minor heading spacing
    was cleaned up.
*   Hurmet’s built-in `ftH₂O` unit uses 2,989 Pa per foot of water. This gives
    63.8584111 ftH₂O instead of the source’s 63.8588 ftH2O, a difference of
    about 0.0006%. The pressure result in kPa agrees.
*   Pump power is calculated by the original pressure-drop × volume-flow expression;
    no pump-efficiency allowance has been introduced.
