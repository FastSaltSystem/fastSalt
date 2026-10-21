---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Cooling-water cases - one condenser envelope

¢` format = "h3" `

11 October 2026. Owner-accepted condenser-water inlet cases: 20°C normal, 30°C
hot design check, 35°C extreme check. These are provisional water conditions,
not outdoor air temperatures or statistical site percentiles.

This sheet screens the **existing** condenser allowance, approximately 38,500
m², with the same U and cooling-water flow at each condition. It does not claim
that this is the final hot-weather condenser size. Thermal input remains 1,500
MW. No reactor-power reduction or additional cooling equipment is assumed.

**Imported result boundary:** condenser pressures, gross power, moisture and
heat rejection are imported from `cooling_cases.py`, which couples the Rankine
cycle to condenser heat transfer. Hurmet independently checks water temperature
rise, LMTD and required area at those imported operating states. Changing an
input here does not update pressure, turbine power or steam properties: rerun
the Python coupling and republish before interpreting changed operating cases.

The cycle retains its extraction pressures and 470°C reheat. Bleed flows are
rebalanced; turbine section efficiencies and U stay fixed. This is a
preliminary thermal screening, not a manufacturer's fixed-machine off-design
performance map.

## Common condenser assumptions

¢` Area = 38513.3661192 'm2' `

¢` OverallU = 2500 'W.m-2.K-1' `

¢` WaterMass = 23715.8489035 'kg/s' `

¢` WaterCp = 4180 'J.kg-1.K-1' `

¢` WaterDensity = 998 'kg/m3' `

¢%%` WaterVolume = WaterMass / WaterDensity = 〔23.8〕 'm3/s' `

¢%%` CapacityRate = WaterMass * WaterCp = 〔99.1〕 'MW/K' `

## Normal reference

¢` Inlet1 = 293.15 K `

¢` CondensingT1 = 306.024255137 K `

¢` Pressure1 = 5.00000001304 kPa `

¢` Gross1 = 689.543968751 MW `

¢` Duty1 = 793.057987427 MW `

¢` Moisture1 = 0.126441068311 `

¢%%` WaterRise1 = Duty1 / CapacityRate = 〔8〕 K `

¢%%` WaterOutlet1 = Inlet1 + WaterRise1 = 〔301〕 K `

¢%%` TerminalApproach1 = CondensingT1 - WaterOutlet1 = 〔4.87〕 K `

¢%%` ColdApproach1 = CondensingT1 - Inlet1 = 〔12.9〕 K `

¢%%` LMTD1 = (ColdApproach1 - TerminalApproach1) / ln(ColdApproach1 /
TerminalApproach1) = 〔8.24〕 K `

¢%%` RequiredArea1 = Duty1 / (OverallU * LMTD1) = 〔38,513〕 'm2' `

¢%%` AreaRatio1 = RequiredArea1 / Area = 〔1〕 `

## Hot design check

¢` Inlet2 = 303.15 K `

¢` CondensingT2 = 316.372916027 K `

¢` Pressure2 = 8.75193946622 kPa `

¢` Gross2 = 668.599526155 MW `

¢` Duty2 = 814.535604326 MW `

¢` Moisture2 = 0.109829191939 `

¢%%` WaterRise2 = Duty2 / CapacityRate = 〔8.22〕 K `

¢%%` WaterOutlet2 = Inlet2 + WaterRise2 = 〔311〕 K `

¢%%` TerminalApproach2 = CondensingT2 - WaterOutlet2 = 〔5.01〕 K `

¢%%` ColdApproach2 = CondensingT2 - Inlet2 = 〔13.2〕 K `

¢%%` LMTD2 = (ColdApproach2 - TerminalApproach2) / ln(ColdApproach2 /
TerminalApproach2) = 〔8.46〕 K `

¢%%` RequiredArea2 = Duty2 / (OverallU * LMTD2) = 〔38,513〕 'm2' `

¢%%` AreaRatio2 = RequiredArea2 / Area = 〔1〕 `

¢%%` GrossReduction2 = Gross1 - Gross2 = 〔20.9〕 MW `

## Extreme check

¢` Inlet3 = 308.15 K `

¢` CondensingT3 = 321.550921364 K `

¢` Pressure3 = 11.4045555014 kPa `

¢` Gross3 = 657.906253169 MW `

¢` Duty3 = 825.500785614 MW `

¢` Moisture3 = 0.101555870124 `

¢%%` WaterRise3 = Duty3 / CapacityRate = 〔8.33〕 K `

¢%%` WaterOutlet3 = Inlet3 + WaterRise3 = 〔316〕 K `

¢%%` TerminalApproach3 = CondensingT3 - WaterOutlet3 = 〔5.07〕 K `

¢%%` ColdApproach3 = CondensingT3 - Inlet3 = 〔13.4〕 K `

¢%%` LMTD3 = (ColdApproach3 - TerminalApproach3) / ln(ColdApproach3 /
TerminalApproach3) = 〔8.57〕 K `

¢%%` RequiredArea3 = Duty3 / (OverallU * LMTD3) = 〔38,513〕 'm2' `

¢%%` AreaRatio3 = RequiredArea3 / Area = 〔1〕 `

¢%%` GrossReduction3 = Gross1 - Gross3 = 〔31.6〕 MW `

## Interpretation and next decision

The same condenser rejects heat at warmer saturation temperature and higher
pressure as inlet water warms. The cooler reference case gives the highest
gross output and highest LP wetness of these three cases. Gross output
reductions here are caused by higher exhaust pressure at fixed thermal input;
they are not modeled reactor deratings. Cooling-system electricity and net
export remain unresolved.

No case establishes acceptable turbine operation. The minimum permitted
condenser pressure, wetness and exhaust-volume limits still need to be set.
Cooler-than-20°C conditions require a later low-pressure limit check. The 30°C
case is the sizing reference to use when choosing a permissible hot-weather
pressure/output; it does not by itself specify that permissible value. The 35°C
case tests the extreme.

The water flow is fixed at the baseline value, so water temperature rise changes
slightly with condenser duty instead of being forced to 8 K in every case. U is
held constant; fouling, cooling-tower performance, pump/fan curves, pressure
drop, site weather, air leakage and turbine maps remain to develop.

## Reproduction

Run `python cooling_cases.py`, then `python publish_cooling_cases.py`, then
`node check_cooling_hurmet.cjs` with HURMET_ENGINE and TEMML_ENGINE set to the
local official Hurmet bundles. The model dependencies and the initial-cycle
reproduction are documented in [the cycle basis][1].

The external solver verifies the condenser relation with an independent LMTD
check, recovers the 5 kPa reference case, retains physical flow fractions and
closes the cycle energy balance. The Hurmet checker independently reproduces
all three required areas and water temperature rises from the imported states.

[1]: README.md
