---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Selected reheat and LP wetness - preliminary design

¢` format = "h3" `

11 October 2026. This selects a working thermal-cycle configuration after the
owner requested resolution of reheat feasibility and LP wetness. It supersedes
the 4 MPa / 470°C first trial for future equipment studies. Earlier worksheets
and results remain preserved as comparisons.

**Selected inputs:** 2.8 MPa HP exhaust; 2.66 MPa hot reheat after a 5% pressure
allowance; 510°C reheated steam; 380°C heating-stream return at 24 MPa. Retain
main-steam reheat, 1,500 MW heat input, 830 K main steam and 560 K feedwater.
The two feed-pump-turbine extractions move from 2.0/1.2 MPa to 1.6/1.0 MPa. The
deaerator remains 0.6 MPa. The highest LP heater extraction is solved to close
the deaerator heat balance, then held fixed across cooling and efficiency cases.

Use **5 kPa absolute as a provisional minimum condenser pressure** at these
reheat conditions. It is a modeling constraint, not an equipment operating
limit approved by a supplier. The screening target is at most 10% equilibrium
exhaust moisture. No moisture separator or additional reheater has been added.

**Imported boundary:** steam properties, coupled flow fractions, cycle-specific
work, the reheater temperature profile/integrated UA, and cooling-case
pressures are calculated in Python/CoolProp. Hurmet independently reproduces
mass flow, gross power, reheater duty, exhaust moisture from enthalpies, and
area sensitivity. Changing pressure, reheat temperature, heating-return
temperature or efficiencies requires rerunning the Python model and
republishing. Duty changes here only scale the fixed cycle and do not describe
off-design turbine performance.

## Imported properties and selected-cycle inputs

¢` ReactorDuty = 1500 MW `

¢` MainH = 3372.39468556 'kJ/kg' `

¢` FeedH = 1264.67695016 'kJ/kg' `

¢` HPwork = 337.635944418 'kJ/kg' `

¢` IPwork = 236.218786987 'kJ/kg' `

¢` LPwork = 404.153291265 'kJ/kg' `

¢` ColdReheatH = 2875.33932398 'kJ/kg' `

¢` HotReheatH = 3483.31598114 'kJ/kg' `

¢` HeatingReturnH = 2022.11899572 'kJ/kg' `

¢` LPExhaustH = 2342.21990378 'kJ/kg' `

¢` SatLiquidH = 137.748595597 'kJ/kg' `

¢` SatVaporH = 2560.72549038 'kJ/kg' `

¢` HeatingFraction = 0.262771048799 `

¢` ReheatedFraction = 0.583597009857 `

¢` ShaftEfficiency = 0.99 `

¢` GeneratorEfficiency = 0.985 `

¢` MoistureTarget = 0.1 `

## Flow, power and reheat duty at 5 kPa

¢%%` MainFlow = ReactorDuty / (MainH - FeedH) = 〔712〕 'kg/s' `

¢%%` GrossElectric = MainFlow * (HPwork + IPwork + LPwork) * ShaftEfficiency *
GeneratorEfficiency = 〔679〕 MW `

¢%%` GrossEfficiency = GrossElectric / ReactorDuty = 〔0.452〕 `

¢%%` HeatingSteam = MainFlow * HeatingFraction = 〔187〕 'kg/s' `

¢%%` ReheatedSteam = MainFlow * ReheatedFraction = 〔415〕 'kg/s' `

¢%%` ReheatColdDuty = ReheatedSteam * (HotReheatH - ColdReheatH) = 〔253〕 MW `

¢%%` ReheatHotDuty = HeatingSteam * (MainH - HeatingReturnH) = 〔253〕 MW `

¢%%` ReheatBalance = ReheatHotDuty - ReheatColdDuty = 〔4.00e-9〕 MW `

¢%%` ExhaustQuality = (LPExhaustH - SatLiquidH) / (SatVaporH - SatLiquidH) =
〔0.91〕 `

¢%%` ExhaustMoisture = 1 - ExhaustQuality = 〔0.0902〕 `

¢%%` WetnessPass = ExhaustMoisture <= MoistureTarget = 〔true〕 `

The gross result includes the steam diverted to reheating and the steam-driven
BFP. Do not subtract BFP shaft work again. Net export awaits the station
auxiliary load list. The normal 20°C cooling case settles slightly above 5 kPa,
so its power is slightly below this reference value.

## Reheater thermal margin and area sensitivity

The 1,601-point counterflow enthalpy-temperature check was repeated at 3,201
points. The hot and cold streams remain separated by more than 20 K. This
exceeds the provisional 10 K screen. Unlike an endpoint-only LMTD estimate, the
imported UA integrates Q \* integral\[1/(Th - Tc)] over the actual nonlinear
temperature profiles. No tube material, heat-transfer correlation or
pressure-boundary design is selected here. The following U values are explicit
sensitivity assumptions, not claimed representative performance; resulting
areas exclude design margins.

¢` MinimumApproach = 20.2759558515 K `

¢` ImportedUA = 6816224.95637 'W/K' `

¢` AssumedU1 = 500 'W.m-2.K-1' `

¢%%` ReheaterArea1 = ImportedUA / AssumedU1 = 〔13,632〕 'm2' `

¢` AssumedU2 = 1000 'W.m-2.K-1' `

¢%%` ReheaterArea2 = ImportedUA / AssumedU2 = 〔6,816〕 'm2' `

¢` AssumedU3 = 1500 'W.m-2.K-1' `

¢%%` ReheaterArea3 = ImportedUA / AssumedU3 = 〔4,544〕 'm2' `

## Coupled cooling-water cases, unchanged condenser

*   **20°C inlet water:** 5.053 kPa condenser; 678.34 MW gross; 8.985% LP moisture;
    804.53 MW condenser duty.

*   **30°C inlet water:** 8.841 kPa condenser; 656.95 MW gross; 7.178% LP moisture;
    826.46 MW condenser duty.

*   **35°C inlet water:** 11.518 kPa condenser; 646.05 MW gross; 6.277% LP moisture;
    837.64 MW condenser duty.

The existing 38,513 m² condenser and 23.76 m³/s cooling-water flow are retained
with constant U. These thermal cases rebalance extraction flows at fixed
pressures and assumed interval efficiencies; they are not supplier off-design maps.

## Sensitivity and cold-weather control requirement

*   LP interval efficiency 0.86 at 5 kPa: 8.427% moisture; 673.30 MW gross.

*   LP interval efficiency 0.88 at 5 kPa: 9.018% moisture; 678.72 MW gross.

*   LP interval efficiency 0.90 at 5 kPa: 9.607% moisture; 684.12 MW gross.

At 3 kPa with LP interval efficiency 0.90, calculated moisture rises to 11.19%,
above the screen. Thus the minimum-pressure condition is part of the selected
preliminary cycle, not optional.

For an illustrative 15°C supply, ideal mixing of approximately 37.3% warm return
with fresh supply would give a 19.82°C effective inlet and maintain 5 kPa at
the nominal case, with the same total condenser flow. This is only a
heat/mass-balance example. Actual bypass, tower/fan controls, pump head,
fouling and operating protections are not designed. Lower reheat temperature or
other turbine efficiencies also require rechecking the pressure floor; this
worksheet does not define a startup envelope.

## Selection and remaining work

Relative to the original 5 kPa case, the selected case loses about 10.82 MW
gross. Reheater heating flow rises from 15.96% to 26.28% of total main flow,
and reheater duty rises from 189.4 MW to 252.5 MW. This is the price of meeting
the wetness screen with more thermal margin while retaining the requested
single main-steam reheater.

The study compared 45 combinations at fixed provisional heater pressures;
selection favors thermal and flow margin, not the highest calculated output.
[Trial results][1] retain rejected cases. All selected bleeds are positive,
including the previously problematic intermediate HP heater.

This resolves the two issues **within the preliminary thermal model**. Turbine
supplier wetness/erosion and exhaust-volume limits, performance maps, reheater
construction and pressure drop, control design and transient operation remain
engineering tasks. The 10% criterion is a project screen, not an industry-wide
acceptance limit. Original reactor/steam-generator conditions and Blender
geometry are not changed by this worksheet.

Reproduce with `python resolve_reheat.py`, `python publish_reheat_selection.py`,
then `node check_reheat_hurmet.cjs` with the official Hurmet engine environment
variables described in [the basis][2]. Dependencies use CoolProp 7.2.0 HEOS
water ([IAPWS-95][3]). The source hashes, checks, selected state table and full
results are saved alongside.

[1]: reheat-trials.csv

[2]: README.md

[3]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[4]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[5]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[6]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[7]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[8]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[9]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[10]: https://coolprop.org/fluid\\\\\\\\\\\\\\\_properties/fluids/Water.html

[11]: https://coolprop.org/fluid\\\\\\\_properties/fluids/Water.html

[12]: https://coolprop.org/fluid\\\_properties/fluids/Water.html

[13]: https://coolprop.org/fluid\_properties/fluids/Water.html
