### A Pluto.jl notebook ###
# v1.0.4

using Markdown
using InteractiveUtils

# ╔═╡ f9eb52c7-07f7-5cc2-a13d-4baba5842eb9
using Unitful

# ╔═╡ 00a78451-4c48-5aa8-9f95-fdec96399299
md"""
# Generator sizing
**Fast Salt System · Calca → Pluto trial**

**Try it:** change `NGen = 3` below to `NGen = 4`, then press **Shift+Enter**. Change it back to 3 to restore the original case.

`1500u"MW"` means 1500 megawatts. Use the eye control beside a result to see its formulas.
"""

# ╔═╡ 69a304e7-9f04-5d51-b38a-524132937de2
begin
    NGen = 3
    ReactorPower = 1500u"MW"
    nothing
end

# ╔═╡ cca41702-8d2a-5f88-8058-c0bf8e82029c
md"""
## Plant duty
Calculations for a combined steam generator and emergency air cooler. Number of steam generators / emergency air coolers.
"""

# ╔═╡ a24d768b-14d0-5e8b-b6b5-e891e1b984e4
md"""
## Temperature distribution
Assume  a temperature distribution: Molten salt  enters the top and exits the bottom. Supercritical water enters the bottom and exits the top. Temperature  differences at top and bottom. Average temperature difference. The log mean temperature difference.
"""

# ╔═╡ 36d40005-730c-5105-98a9-21ff0eb116d5
begin
    TSaltHot = 875u"K"
    TSaltCool = 810u"K"
    TStmCool = 560u"K"
    TStmHot = 830u"K"
    nothing
end

# ╔═╡ 5d342740-3e91-5e76-9e8c-7300a7eb9107
md"""
## Coolant properties (MgCl2-KCL-NCl at w/o 45.9, 38.9, 15.1)
Coolant density at average temperature. Assumed molten salt tube's geometry.
"""

# ╔═╡ 9bd15ee4-82a0-5b28-af99-e6a6eb725998
begin
    CoolantLiquidusT = 674u"K"
    TubeID = 1.4u"cm"
    TubeThickness = 1u"mm"
    nothing
end

# ╔═╡ db57c62f-18c6-503f-a916-39a0f3c9f393
md"""
## Number of coolant tubes needed
Calculate the minimum number of tubes needed based on the heat capacity of the molten salt coolant.  This is based on limiting the coolant velocity through the tubes .
"""

# ╔═╡ ddef0ae1-1a9a-5bdd-9447-2e287ac7f5a6
begin
    VelocityLimit = 3u"m/s"
    nothing
end

# ╔═╡ 4fd3fd39-7607-5ce5-a22d-935bbdd0c1f3
md"""
## Tubes Used
Set the number of tubes to use.  Setting higher than the needed amount can reduce the height of the generator. The tubes can be arranged in different configurations, depending on how many tubes are put in each row. This sets the generator to a square profile.
"""

# ╔═╡ 4003560d-b297-5e13-b9f4-db72a6555ca8
md"""
## Generator profile
Assuming same size tubes for steam:
"""

# ╔═╡ 34b9b2db-a78c-59f7-8aab-181efac79b4f
md"""
## Heat transfer per side of tube
Heat transfer in this generator is from both sides of each row of tubes. The amount of heat to transfer on each side of a tube is:
"""

# ╔═╡ 40057253-fcb1-55e5-a654-7dcc6547053d
begin
    Sides = 3
    nothing
end

# ╔═╡ 88d28ce8-2294-5f76-8660-bfacf4cd07dd
md"""
## Radiative heat transfer
Check to see how well heat is transferred by radiated heat due to temperature. The Stefan-Boltzman constant: Basic emissivity of stainless steel. Assuming two infinite flat planes facing each other: Radiation heat transfer is larger at the bottom than the top. Use the average transfer rate for the height of generator needed: This is impractically large so we need conduction and / or convection to bring the size down. We can also bring the height down by increasing the number of tubes.
"""

# ╔═╡ 6291ae03-ba6a-5e81-8141-844ccb229ca7
begin
    eSS = 0.54
    nothing
end

# ╔═╡ c449fcf7-9fe5-591e-861c-9f65dd3c329c
md"""
## Air conductivity
The air  gap has a diamond shape between two sets of circular tubes.  It ranges from zero to TubeOD.  Assume the gap is the average. This is significantly smaller (< 1/10) than the radiation heat transfer.
"""

# ╔═╡ 497d3ea4-f898-51cb-80f0-9cfd472bd072
md"""
## Air convection
If we assume, like molten salt, that convection improves heat transfer by a factor of 6 we get: This is still lower (~ 1/2) than radiation heat transfer.
"""

# ╔═╡ dcd3197b-f084-5eb1-a3ce-faf1068c6727
md"""
## Steel conduction
Q/A = (k/dx) DT.  A = contact width * length.  Solving for length gets you: L = (dx/w)(Q/k DT) .  For conduction  we can calculate a nominal length which is Q/kDT.  The actual length needed is just the nominal length times the aspect ratio: (dx/width). Heat per degree K per side.
"""

# ╔═╡ 44440db9-fef1-55f2-ba4f-d1a1ef8a1fe5
md"""
## Tubes touching
Let's say the width of contact width between tubes can be 1/10 the diameter.
"""

# ╔═╡ 9913a360-ba86-53e6-910b-a4fae73d6eb9
md"""
## Tubes with saddle pads
Assume saddle pads that are: 3/4 the diameter in width and half of thickest: Now this is getting more reasonable.
"""

# ╔═╡ bab7e287-0e83-5206-9af8-cd669dfeb999
md"""
## Indented round tubes (somewhat square)
Best height to width ratio. Effective resistance is contact thickness divided by conductivity.
"""

# ╔═╡ 32ef2d2d-3245-503d-bd6f-0cd6e5d6a867
begin
    sqContactW = 8u"mm"
    sqContactTh = 2u"mm"
    nothing
end

# ╔═╡ 126eef74-5488-5eae-97a7-cef016090444
md"""
## Fluid heat transfer

"""

# ╔═╡ 670d5c32-abf7-5325-bd11-005a3b92b89e
md"""
## Salt side
Function calculates heat transfer coefficient from coolant bulk flow to chamber wall. The resistance is just the inverse of the heat transfer coefficient. The length needed can be calculated as the heat per side divided by the temperature difference and the number of sides it is distributed over, divided by the heat transfer coefficient times the wall width.
"""

# ╔═╡ f9a096d2-7fb6-5d06-bc5a-dae94a3387b8
md"""
## Steam side
Values from https://www.ski-gmbh.com/swa/tools/steam, and  https://www.thermopedia.com/de/content/1150/ . Pressure is 24 MPa for both inlet and exit. Steam exit side. Values for inlet side : Add resistances in series: salt, contact, steam.
"""

# ╔═╡ f556c42f-84aa-5232-8a75-3ac2873455eb
begin
    ExitEnthalpy = 3372493u"J/kg"
    InletEnthalpy = 1264452u"J/kg"
    InletDensity = 764.494u"kg/m^3"
    nothing
end

# ╔═╡ 262a7364-4cb9-5616-8523-d97d0b325a23
md"""
## Salt pressure drop
The pressure drop over the generator because of flow resistance in the generator: Since the pressure head is near or over 50 feet we will require some kind of centrifugal pump.
"""

# ╔═╡ 51912ae6-f8ea-524c-ac83-dbd936239c47
begin
    SSRoughness = 0.001u"mm"
    nothing
end

# ╔═╡ 915db99c-0aef-5573-8efe-e0ee19db974c
md"""
## Generator pump power
The power required to push the coolant through each generator.
"""

# ╔═╡ 7580a378-f972-52e0-be0f-49b9c7494def
md"""
## Buoyancy
Pressure across generator due to height and density change in salt.
"""

# ╔═╡ 9995d31b-9cb5-51c4-a5f6-8519340867d2
md"""
## Conversion notes
- All 103 calculation lines and eight functions from the Calca worksheet are represented. Original variable spellings are retained for comparison.
- Unitful checks unit compatibility. `uconvert` changes display units; `ustrip(NoUnits, ...)` obtains a dimensionless number for correlations and tube counts.
- The source's radiative-flux display request `kW/m^-2` was corrected to `kW/m²`, matching its formula and displayed result.
- The source composition label “MgCl2-KCL-NCl” and property/correlation coefficients are retained as supplied. The steam properties remain the original fixed inputs at 24 MPa; changing temperatures does **not** obtain new steam properties automatically.
- Feet of water use 2989 Pa/ftH₂O, the same convention as the Hurmet conversion. Mechanical horsepower uses 745.6998715822702 W/hp. These display conversions do not feed back into the calculations.
- Hydraulic pumping power is pressure drop × volume flow; no efficiency allowance has been added.
- The original “Churchill factor good to 2%” description is retained as a source claim, not established by this conversion. Reproducing the worksheet is not a validation of its engineering assumptions.

**Source:** `Generator sizing.calca`. The original Calca and Hurmet files are unchanged.
"""

# ╔═╡ 13a54167-dae9-564c-9044-f74597601328
begin
    # Display rounding only: calculations retain their full precision.
    pretty(x::Unitful.AbstractQuantity) = string(round(ustrip(x); sigdigits=7), " ", unit(x))
    pretty(x::Integer) = string(x)
    pretty(x::Number) = string(round(x; sigdigits=7))
    result_table(rows) = Markdown.parse("| Quantity | Value |\n|:--|--:|\n" *
        join(("| `" * string(label) * "` | " * pretty(value) * " |" for (label, value) in rows), "\n"))
    nothing
end

# ╔═╡ dbfec583-3acd-5001-a2a9-09a8495d2190
begin
    Q_Gen = uconvert(u"MW", ReactorPower / NGen)
    result_table([
        ("Q_Gen", Q_Gen)
    ])
end

# ╔═╡ 55720fee-603f-51bf-af6a-f04bc7d62465
begin
    LMTD(Th1, Th2, Tc1, Tc2) = ((Th2-Tc2)-(Th1-Tc1)) / log((Th2-Tc2)/(Th1-Tc1))
    CoolantDensityF(temp) = 2112.68u"kg/m^3" - 0.5635u"kg/(m^3*K)" * temp
    CoolantHeatCapacityF(temp) = 1.43788u"J/(g*K)" - 0.0005u"J/(g*K^2)" * temp
    CoolantViscosityF(temp) = 0.00070645u"kg/(m*s)" * exp(1204.1u"K" / temp)
    CoolantHeatCondF(temp) = (0.65318 - 2.6e-4 * temp/(1u"K")) * 1u"W/(m*K)"
    ReynoldsNumber(density, velocity, diameter, viscosity) = ustrip(NoUnits, density*velocity*diameter/viscosity)
    function BulkToWallDeltaH(heatCap, viscosity, heatCond, reyNum, diameter)
        prantdlNum = ustrip(NoUnits, heatCap*viscosity/heatCond)
        nusseltNum = 0.0266 * reyNum^0.805 * prantdlNum^(1/3)
        return uconvert(u"kW/(K*m^2)", nusseltNum*heatCond/diameter)
    end
    function PressureDrop(length, diameter, velocity, roughness, density, viscosity)
        reyNum = ReynoldsNumber(density, velocity, diameter, viscosity)
        # Original worksheet correlation, retained without changing its coefficients.
        frictionFactor = (8/6.0516) * log(roughness/diameter + (7/reyNum)^0.9)^(-2)
        kineticP = 0.5 * density * velocity^2
        return frictionFactor * (length/diameter) * kineticP
    end
    nothing
end

# ╔═╡ 669cfbc3-a463-554d-b700-f9fb11cbd6b4
begin
    SaltAveT = uconvert(u"K", (TSaltHot +TSaltCool)/2)
    DTtop = uconvert(u"K", TSaltHot - TStmHot)
    DTbot = uconvert(u"K", TSaltCool - TStmCool)
    DTAve = uconvert(u"K", (DTtop + DTbot)/2)
    DT_lmdt = uconvert(u"K", LMTD(TSaltHot, TSaltCool, TStmHot, TStmCool))
    result_table([
        ("SaltAveT", SaltAveT),
        ("DTtop", DTtop),
        ("DTbot", DTbot),
        ("DTAve", DTAve),
        ("DT_lmdt", DT_lmdt)
    ])
end

# ╔═╡ c43a8199-ae02-5029-b2b7-32d59a550afe
begin
    CoolantDensity = uconvert(u"kg/m^3", CoolantDensityF(SaltAveT))
    CoolantHeatCapacity = uconvert(u"J*g^-1*K^-1", CoolantHeatCapacityF(SaltAveT))
    CoolantViscosity = uconvert(u"kg*m^-1*s^-1", CoolantViscosityF(SaltAveT))
    CoolantHeatCond = uconvert(u"W*m^-1*K^-1", CoolantHeatCondF(SaltAveT))
    SaltMassFlow = uconvert(u"kg/s", Q_Gen/(CoolantHeatCapacity*(TSaltHot-TSaltCool)))
    TubeOD = uconvert(u"cm", TubeID + 2 * TubeThickness)
    TubeArea = uconvert(u"cm^2", (pi/4)*TubeID^2)
    result_table([
        ("CoolantDensity", CoolantDensity),
        ("CoolantHeatCapacity", CoolantHeatCapacity),
        ("CoolantViscosity", CoolantViscosity),
        ("CoolantHeatCond", CoolantHeatCond),
        ("SaltMassFlow", SaltMassFlow),
        ("TubeOD", TubeOD),
        ("TubeArea", TubeArea)
    ])
end

# ╔═╡ 447fd609-8aa2-5cee-b0d6-e8757ac7060f
begin
    AreaNeeded = uconvert(u"m^2", SaltMassFlow/CoolantDensity/VelocityLimit)
    TubesNeeded = ceil(Int, ustrip(NoUnits, AreaNeeded/TubeArea))
    result_table([
        ("AreaNeeded", AreaNeeded),
        ("TubesNeeded", TubesNeeded)
    ])
end

# ╔═╡ f16d50ea-795d-585a-b46b-3a74a048f49c
begin
    TubesUsed = max(TubesNeeded, 12000)
    TubesPerRowSq = ceil(Int, sqrt(2 * TubesUsed))
    TubesPerRow = TubesPerRowSq
    NRows = ceil(Int, TubesUsed/TubesPerRow)
    NTubes = TubesPerRow * NRows
    SaltWidth = uconvert(u"m", NRows * TubeOD)
    result_table([
        ("TubesUsed", TubesUsed),
        ("TubesPerRowSq", TubesPerRowSq),
        ("TubesPerRow", TubesPerRow),
        ("NRows", NRows),
        ("NTubes", NTubes),
        ("SaltWidth", SaltWidth)
    ])
end

# ╔═╡ 05b05827-58f9-5edb-9f14-21468f63ce0f
begin
    Q_Side = uconvert(u"kW", Q_Gen/NTubes/Sides)
    result_table([
        ("Q_Side", Q_Side)
    ])
end

# ╔═╡ aa657fec-21c3-530e-90bf-ac4909ade182
begin
    SteelCond = uconvert(u"W*m^-1*K^-1", 19u"W*m^-1*K^-1")
    NSurfaces = NTubes * 2
    Q_K_S = uconvert(u"kW/K", Q_Side / DT_lmdt)
    NominalLength = uconvert(u"m", Q_K_S / SteelCond)
    result_table([
        ("SteelCond", SteelCond),
        ("NSurfaces", NSurfaces),
        ("Q_K_S", Q_K_S),
        ("NominalLength", NominalLength)
    ])
end

# ╔═╡ 8d4584ec-d048-50cf-8786-5d575f4ddc36
begin
    sqAspect = ustrip(NoUnits, sqContactTh / sqContactW)
    sqLength = uconvert(u"m", NominalLength * sqAspect)
    sqContactR = uconvert(u"m^2*K/kW", sqContactTh / SteelCond)
    result_table([
        ("sqAspect", sqAspect),
        ("sqLength", sqLength),
        ("sqContactR", sqContactR)
    ])
end

# ╔═╡ b4f3ca28-03dd-59ba-a466-97b1006611ed
begin
    GenDepth = uconvert(u"m", TubesPerRow * TubeOD)
    GenDepth_ft = uconvert(u"ft", GenDepth)
    GenWidth = uconvert(u"m", 2 * SaltWidth)
    GenWidth_ft = uconvert(u"ft", GenWidth)
    result_table([
        ("GenDepth", GenDepth),
        ("GenDepth (ft)", GenDepth_ft),
        ("GenWidth", GenWidth),
        ("GenWidth (ft)", GenWidth_ft)
    ])
end

# ╔═╡ e8264ffc-f85d-54c0-a5af-80fc4de0793f
begin
    sigma = uconvert(u"W*m^-2*K^-4", 5.669e-8u"W*m^-2*K^-4")
    qTop_A = uconvert(u"kW/m^2", (sigma * (TSaltHot^4 - TStmHot^4)) / ((2/eSS) -1))
    qBot_A = uconvert(u"kW/m^2", (sigma * (TSaltCool^4 - TStmCool^4)) / ((2/eSS) -1))
    qRadAve_A = uconvert(u"kW/m^2", ((qTop_A + qBot_A)/2))
    QRadPerL = uconvert(u"MW/m", qRadAve_A * GenDepth * NRows * Sides)
    RadLength = uconvert(u"m", Q_Gen / QRadPerL)
    result_table([
        ("sigma", sigma),
        ("qTop_A", qTop_A),
        ("qBot_A", qBot_A),
        ("qRadAve_A", qRadAve_A),
        ("QRadPerL", QRadPerL),
        ("RadLength", RadLength)
    ])
end

# ╔═╡ 06ecaef5-07ef-52f2-bc4c-95ffea628aae
begin
    AirK = uconvert(u"W*m^-1*K^-1", 0.024u"W*m^-1*K^-1")
    AirGap = uconvert(u"cm", TubeOD/2)
    qAirK_A = uconvert(u"kW/m^2", AirK * (DT_lmdt)/AirGap)
    result_table([
        ("AirK", AirK),
        ("AirGap", AirGap),
        ("qAirK_A", qAirK_A)
    ])
end

# ╔═╡ 0c18d8ab-bb5a-58d6-83b5-e301ea861596
begin
    qAirConv_A = uconvert(u"kW/m^2", 6 * qAirK_A)
    result_table([
        ("qAirConv_A", qAirConv_A)
    ])
end

# ╔═╡ 3e056a78-4747-5074-8c25-4d78e298cf8e
begin
    touchW = uconvert(u"cm", TubeOD/10)
    touchTh = uconvert(u"mm", 2 * TubeThickness)
    touchAspect = ustrip(NoUnits, touchTh/touchW)
    touchLength = uconvert(u"m", NominalLength*touchAspect)
    result_table([
        ("touchW", touchW),
        ("touchTh", touchTh),
        ("touchAspect", touchAspect),
        ("touchLength", touchLength)
    ])
end

# ╔═╡ d60af6eb-10d3-5bf2-a2e3-ee2527710245
begin
    saddleW = uconvert(u"cm", 0.75 * TubeOD)
    saddleTh = uconvert(u"mm", 2*TubeThickness + (TubeOD/3)/2)
    saddleAspect = ustrip(NoUnits, saddleTh/saddleW)
    saddleLength = uconvert(u"m", NominalLength * saddleAspect)
    result_table([
        ("saddleW", saddleW),
        ("saddleTh", saddleTh),
        ("saddleAspect", saddleAspect),
        ("saddleLength", saddleLength)
    ])
end

# ╔═╡ eebda667-58b0-5e92-977f-9ecf54aebb7f
begin
    saltVel = uconvert(u"m/s", SaltMassFlow/NTubes/CoolantDensity/TubeArea)
    saltReyn = ReynoldsNumber(CoolantDensity, saltVel,TubeID, CoolantViscosity)
    saltBulkH = uconvert(u"kW*m^-2*K^-1", BulkToWallDeltaH(CoolantHeatCapacity, CoolantViscosity, CoolantHeatCond, saltReyn, TubeID))
    saltR = uconvert(u"m^2*K/kW", 1 / saltBulkH)
    saltLength = uconvert(u"m", Q_K_S * saltR / sqContactW)
    result_table([
        ("saltVel", saltVel),
        ("saltReyn", saltReyn),
        ("saltBulkH", saltBulkH),
        ("saltR", saltR),
        ("saltLength", saltLength)
    ])
end

# ╔═╡ 5c0d7e96-094c-5f88-a2a6-56e869aa0724
begin
    SteamMassFlow = uconvert(u"kg/s", Q_Gen/(ExitEnthalpy-InletEnthalpy))
    ExitDensity = uconvert(u"kg/m^3", 1 / (0.01358536u"m^3/kg"))
    ExitViscosity = uconvert(u"kg*m^-1*s^-1", 3.392e-5u"kg*m^-1*s^-1")
    ExitConduct = uconvert(u"W*m^-1*K^-1", 100u"mW*m^-1*K^-1")
    ExitHeatCapacity = uconvert(u"J*kg^-1*K^-1", 2980.664u"J*kg^-1*K^-1")
    ExitVelocity = uconvert(u"m/s", SteamMassFlow/ExitDensity/(TubeArea*NTubes))
    ExityReyn = ReynoldsNumber(ExitDensity, ExitVelocity, TubeID, ExitViscosity)
    ExitBulkH = uconvert(u"kW*m^-2*K^-1", BulkToWallDeltaH(ExitHeatCapacity, ExitViscosity, ExitConduct, ExityReyn, TubeID))
    ExitR = uconvert(u"m^2*K/kW", 1 / ExitBulkH)
    InletViscocity = uconvert(u"kg*m^-1*s^-1", 9.635e-5u"kg*m^-1*s^-1")
    InletConduct = uconvert(u"W*m^-1*K^-1", 600u"mW*m^-1*K^-1")
    InletHeatCapacity = uconvert(u"J*kg^-1*K^-1", 5012.22u"J*kg^-1*K^-1")
    InletVelocity = uconvert(u"m/s", SteamMassFlow/InletDensity/(TubeArea*NTubes))
    InletReyn = ReynoldsNumber(InletDensity, InletVelocity, TubeID, InletViscocity)
    InletBulkH = uconvert(u"kW*m^-2*K^-1", BulkToWallDeltaH(InletHeatCapacity, InletViscocity, InletConduct, InletReyn, TubeID))
    InletR = uconvert(u"m^2*K/kW", 1 / InletBulkH)
    SteamAveR = uconvert(u"m^2*K/kW", (InletR + ExitR)/2)
    steamlength = uconvert(u"m", Q_K_S * SteamAveR/ sqContactW)
    allThreeR = uconvert(u"m^2*K/kW", saltR + sqContactR + SteamAveR)
    tubeLength = uconvert(u"m", Q_K_S * allThreeR / sqContactW)
    AddedLengths = uconvert(u"m", steamlength + saltLength + sqLength)
    tubeLength_ft = uconvert(u"ft", tubeLength)
    tubeLengthTotal = uconvert(u"km", NGen * 2 * NTubes * tubeLength)
    result_table([
        ("SteamMassFlow", SteamMassFlow),
        ("ExitDensity", ExitDensity),
        ("ExitViscosity", ExitViscosity),
        ("ExitConduct", ExitConduct),
        ("ExitHeatCapacity", ExitHeatCapacity),
        ("ExitVelocity", ExitVelocity),
        ("ExityReyn", ExityReyn),
        ("ExitBulkH", ExitBulkH),
        ("ExitR", ExitR),
        ("InletViscocity", InletViscocity),
        ("InletConduct", InletConduct),
        ("InletHeatCapacity", InletHeatCapacity),
        ("InletVelocity", InletVelocity),
        ("InletReyn", InletReyn),
        ("InletBulkH", InletBulkH),
        ("InletR", InletR),
        ("SteamAveR", SteamAveR),
        ("steamlength", steamlength),
        ("allThreeR", allThreeR),
        ("tubeLength", tubeLength),
        ("AddedLengths", AddedLengths),
        ("tubeLength (ft)", tubeLength_ft),
        ("tubeLengthTotal", tubeLengthTotal)
    ])
end

# ╔═╡ 7742d486-08f8-59a6-a96e-ff3b848bff92
begin
    CoolantPressureDrop = uconvert(u"kPa", PressureDrop(tubeLength, TubeID, saltVel, SSRoughness,CoolantDensity, CoolantViscosity))
    CoolantPressureDrop_psi = uconvert(u"psi", CoolantPressureDrop)
    CoolantPressureDrop_ftH2O = ustrip(u"Pa", CoolantPressureDrop) / 2989.0
    result_table([
        ("CoolantPressureDrop", CoolantPressureDrop),
        ("CoolantPressureDrop (psi)", CoolantPressureDrop_psi),
        ("CoolantPressureDrop (ftH₂O)", CoolantPressureDrop_ftH2O)
    ])
end

# ╔═╡ e6178216-48a5-5592-bcae-d70458174afe
begin
    GenPumpPower = uconvert(u"kW", CoolantPressureDrop* SaltMassFlow/CoolantDensity)
    GenPumpPower_hp = ustrip(u"W", GenPumpPower) / 745.6998715822702
    result_table([
        ("GenPumpPower", GenPumpPower),
        ("GenPumpPower (hp)", GenPumpPower_hp)
    ])
end

# ╔═╡ 36268a3f-65b4-5a97-96a7-519233d7a306
md"""
### Results at a glance
| Per-generator result | Current value |
|:--|--:|
| Heat duty | $(pretty(Q_Gen)) |
| Salt mass flow | $(pretty(SaltMassFlow)) |
| Steam mass flow | $(pretty(SteamMassFlow)) |
| Salt tubes | $(NTubes) |
| Tube length | $(pretty(tubeLength)) |
| Salt pressure drop | $(pretty(CoolantPressureDrop)) |
| Hydraulic pumping power | $(pretty(GenPumpPower)) |

**Calculation trail** — expand a result cell to see or edit the equations that produce it.
"""

# ╔═╡ 21c47b13-7ff9-5e8d-8d7f-31b0c86ae588
begin
    Buoncy = uconvert(u"kPa", tubeLength*(CoolantDensityF(TSaltCool) - CoolantDensityF(TSaltHot) ) * 9.8u"N/kg")
    result_table([
        ("Buoncy", Buoncy)
    ])
end

# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
Unitful = "1986cc42-f94f-5a68-af5c-568840ba703d"

[compat]
Unitful = "~1.29.0"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

julia_version = "1.12.6"
manifest_format = "2.0"
project_hash = "0af3c9f6f928c23eeec1a4a6b52a94b21714c110"

[[deps.Artifacts]]
uuid = "56f22d72-fd6d-98f1-02f0-08ddc0907c33"
version = "1.11.0"

[[deps.CompilerSupportLibraries_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "e66e0078-7015-5450-92f7-15fbd957f2ae"
version = "1.3.0+1"

[[deps.Dates]]
deps = ["Printf"]
uuid = "ade2ca70-3891-5945-98fb-dc099432e06a"
version = "1.11.0"

[[deps.Libdl]]
uuid = "8f399da3-3557-5675-b5ff-fb832c97cbdb"
version = "1.11.0"

[[deps.LinearAlgebra]]
deps = ["Libdl", "OpenBLAS_jll", "libblastrampoline_jll"]
uuid = "37e2e46d-f89d-539d-b4ee-838fcccc9c8e"
version = "1.12.0"

[[deps.OpenBLAS_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "Libdl"]
uuid = "4536629a-c528-5b80-bd46-f80d51c5b363"
version = "0.3.29+0"

[[deps.Printf]]
deps = ["Unicode"]
uuid = "de0858da-6303-5e67-8744-51eddeeeb8d7"
version = "1.11.0"

[[deps.Random]]
deps = ["SHA"]
uuid = "9a3f8284-a2c9-5f02-9a11-845980a1fd5c"
version = "1.11.0"

[[deps.SHA]]
uuid = "ea8e919c-243c-51af-8825-aaa63cd721ce"
version = "0.7.0"

[[deps.Unicode]]
uuid = "4ec0a83e-493e-50e2-b9ac-8f72acf5a8f5"
version = "1.11.0"

[[deps.Unitful]]
deps = ["Dates", "LinearAlgebra", "Random"]
git-tree-sha1 = "1f0f9f401753701a7e4113b5056ca38d33875b55"
uuid = "1986cc42-f94f-5a68-af5c-568840ba703d"
version = "1.29.0"

    [deps.Unitful.extensions]
    ConstructionBaseUnitfulExt = "ConstructionBase"
    ForwardDiffExt = "ForwardDiff"
    InverseFunctionsUnitfulExt = "InverseFunctions"
    LatexifyExt = ["Latexify", "LaTeXStrings"]
    NaNMathExt = "NaNMath"
    PrintfExt = "Printf"

    [deps.Unitful.weakdeps]
    ConstructionBase = "187b0558-2788-49d3-abe0-74a17ed4e7c9"
    ForwardDiff = "f6369f11-7733-5829-9624-2563aa707210"
    InverseFunctions = "3587e190-3f89-42d0-90ee-14403ec27112"
    LaTeXStrings = "b964fa9f-0449-5b57-a5c2-d3ea65f4040f"
    Latexify = "23fbe1c1-3f47-55db-b15f-69d7ec21a316"
    NaNMath = "77ba4419-2d1f-58cd-9bb1-8ffee604a2e3"
    Printf = "de0858da-6303-5e67-8744-51eddeeeb8d7"

[[deps.libblastrampoline_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "8e850b90-86db-534c-a0d3-1478176c7d93"
version = "5.15.0+0"
"""

# ╔═╡ Cell order:
# ╟─00a78451-4c48-5aa8-9f95-fdec96399299
# ╠═69a304e7-9f04-5d51-b38a-524132937de2
# ╟─36268a3f-65b4-5a97-96a7-519233d7a306
# ╟─cca41702-8d2a-5f88-8058-c0bf8e82029c
# ╟─dbfec583-3acd-5001-a2a9-09a8495d2190
# ╟─a24d768b-14d0-5e8b-b6b5-e891e1b984e4
# ╠═36d40005-730c-5105-98a9-21ff0eb116d5
# ╟─669cfbc3-a463-554d-b700-f9fb11cbd6b4
# ╟─5d342740-3e91-5e76-9e8c-7300a7eb9107
# ╠═9bd15ee4-82a0-5b28-af99-e6a6eb725998
# ╟─c43a8199-ae02-5029-b2b7-32d59a550afe
# ╟─db57c62f-18c6-503f-a916-39a0f3c9f393
# ╠═ddef0ae1-1a9a-5bdd-9447-2e287ac7f5a6
# ╟─447fd609-8aa2-5cee-b0d6-e8757ac7060f
# ╟─4fd3fd39-7607-5ce5-a22d-935bbdd0c1f3
# ╟─f16d50ea-795d-585a-b46b-3a74a048f49c
# ╟─4003560d-b297-5e13-b9f4-db72a6555ca8
# ╟─b4f3ca28-03dd-59ba-a466-97b1006611ed
# ╟─34b9b2db-a78c-59f7-8aab-181efac79b4f
# ╠═40057253-fcb1-55e5-a654-7dcc6547053d
# ╟─05b05827-58f9-5edb-9f14-21468f63ce0f
# ╟─88d28ce8-2294-5f76-8660-bfacf4cd07dd
# ╠═6291ae03-ba6a-5e81-8141-844ccb229ca7
# ╟─e8264ffc-f85d-54c0-a5af-80fc4de0793f
# ╟─c449fcf7-9fe5-591e-861c-9f65dd3c329c
# ╟─06ecaef5-07ef-52f2-bc4c-95ffea628aae
# ╟─497d3ea4-f898-51cb-80f0-9cfd472bd072
# ╟─0c18d8ab-bb5a-58d6-83b5-e301ea861596
# ╟─dcd3197b-f084-5eb1-a3ce-faf1068c6727
# ╟─aa657fec-21c3-530e-90bf-ac4909ade182
# ╟─44440db9-fef1-55f2-ba4f-d1a1ef8a1fe5
# ╟─3e056a78-4747-5074-8c25-4d78e298cf8e
# ╟─9913a360-ba86-53e6-910b-a4fae73d6eb9
# ╟─d60af6eb-10d3-5bf2-a2e3-ee2527710245
# ╟─bab7e287-0e83-5206-9af8-cd669dfeb999
# ╠═32ef2d2d-3245-503d-bd6f-0cd6e5d6a867
# ╟─8d4584ec-d048-50cf-8786-5d575f4ddc36
# ╟─126eef74-5488-5eae-97a7-cef016090444
# ╟─670d5c32-abf7-5325-bd11-005a3b92b89e
# ╟─eebda667-58b0-5e92-977f-9ecf54aebb7f
# ╟─f9a096d2-7fb6-5d06-bc5a-dae94a3387b8
# ╠═f556c42f-84aa-5232-8a75-3ac2873455eb
# ╟─5c0d7e96-094c-5f88-a2a6-56e869aa0724
# ╟─262a7364-4cb9-5616-8523-d97d0b325a23
# ╠═51912ae6-f8ea-524c-ac83-dbd936239c47
# ╟─7742d486-08f8-59a6-a96e-ff3b848bff92
# ╟─915db99c-0aef-5573-8efe-e0ee19db974c
# ╟─e6178216-48a5-5592-bcae-d70458174afe
# ╟─7580a378-f972-52e0-be0f-49b9c7494def
# ╟─21c47b13-7ff9-5e8d-8d7f-31b0c86ae588
# ╟─9995d31b-9cb5-51c4-a5f6-8519340867d2
# ╟─f9eb52c7-07f7-5cc2-a13d-4baba5842eb9
# ╟─13a54167-dae9-564c-9044-f74597601328
# ╟─55720fee-603f-51bf-af6a-f04bc7d62465
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002
