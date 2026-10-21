---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-10-20
---------------

# Rankine cycle - preliminary heat balance

¢` format = "h3" `

11 October 2026. Main-steam reheat and a provisional water-cooled condenser at 5
kPa absolute follow the owner's confirmed instructions. This is a first design
case, not a net plant rating or a turbine purchase specification. See
[basis][1].

**Imported calculation boundary:** water properties, extraction fractions and
specific component duties below come from the companion Python/CoolProp model.
Hurmet recalculates flow scaling, output and condenser estimates from these
imported inputs. Changing steam pressures, temperatures, turbine efficiencies
or heater routing requires rerunning Python and regenerating this sheet.
Changing heat duty here scales the fixed cycle; it does not predict part-load
performance.

The diagram is retained: HP turbine, reheater heated by a main-steam branch,
reheat/IP turbine, LP turbine, three LP heaters, deaerator, four HP heaters and
a steam-driven feed pump. The LP heater pressure is selected to close the
deaerator balance without an extra main-turbine extraction. Pressure
assignments remain provisional. No salt-heated reheater is added.

## Adopted state assumptions

*   **Steam-generator duty:** 1,500 MW total, three generators. Existing project
    target; all delivered to water in this case.
*   **Main steam:** 24 MPa absolute, 830 K (556.85°C). Existing generator worksheet.
*   **Return feedwater:** 24 MPa absolute, 560 K (286.85°C). Existing generator
    worksheet.
*   **Reheat:** 4 MPa HP exhaust; 3.8 MPa after 5% loss; 470°C hot reheat.
    Provisional.
*   **Reheater heating-stream return:** 24 MPa, 360°C, then throttled to highest HP
    heater. Provisional.
*   **Condenser:** 5 kPa absolute; saturated-liquid hotwell. Owner-approved starting case.
*   **Deaerator:** 0.6 MPa, saturated liquid. Provisional.
*   **Section isentropic efficiencies:** HP 0.88; IP 0.90; LP 0.88; pump turbine
    0.80. Per modeled expansion interval, not guaranteed overall casing efficiency.
*   **Pump efficiencies:** BFP 0.85; condensate pump 0.80. Provisional.
*   **Shaft/generator efficiencies:** 0.99 / 0.985. Provisional.
*   **Feedwater-heater terminal difference:** 5 K; saturated drains cascade to next
    heater. No separate drain-cooling zone.

At 24 MPa the heating stream does not undergo constant-pressure two-phase
condensation. The reheater is modeled using its full enthalpy/temperature
curve; its cooled high-pressure return is throttled into the highest HP heater.

## Imported state and cycle inputs

¢` ReactorDuty = 1500 MW `

¢` GeneratorCount = 3 `

¢` MainEnthalpy = 3372.39468556 'kJ/kg' `

¢` FeedEnthalpy = 1264.67695016 'kJ/kg' `

¢` HPwork = 337.252327509 'kJ/kg' `

¢` IPwork = 275.084502777 'kJ/kg' `

¢` LPwork = 381.263506393 'kJ/kg' `

¢` BFPwork = 30.1186769796 'kJ/kg' `

¢` CEPwork = 548.420407042 'J/kg' `

¢` CondenserHeat = 1114.36159007 'kJ/kg' `

¢` ReheatGain = 435.9215363 'kJ/kg' `

¢` ReheatFraction = 0.159567439186 `

¢` ReheatedFraction = 0.610462490126 `

¢` LPExhaustFraction = 0.520007886028 `

¢` PumpTurbineFraction = 0.0892988966435 `

¢` ShaftEfficiency = 0.99 `

¢` GeneratorEfficiency = 0.985 `

¢` CEPMotorEfficiency = 0.96 `

## Heat, flow and power

¢%%` TotalSteam = ReactorDuty / (MainEnthalpy - FeedEnthalpy) = 〔712〕 'kg/s' `

¢%%` PerGeneratorSteam = TotalSteam / GeneratorCount = 〔237〕 'kg/s' `

¢%%` ReheaterSupply = TotalSteam * ReheatFraction = 〔114〕 'kg/s' `

¢%%` ReheatedSteam = TotalSteam * ReheatedFraction = 〔434〕 'kg/s' `

¢%%` ReheatDuty = ReheatedSteam * ReheatGain = 〔189〕 MW `

¢%%` PumpTurbineSteam = TotalSteam * PumpTurbineFraction = 〔63.6〕 'kg/s' `

¢%%` LPExhaustSteam = TotalSteam * LPExhaustFraction = 〔370〕 'kg/s' `

¢%%` HPIPGross = TotalSteam * (HPwork + IPwork) * ShaftEfficiency *
GeneratorEfficiency = 〔425〕 MW `

¢%%` LPGross = TotalSteam * LPwork * ShaftEfficiency * GeneratorEfficiency =
〔265〕 MW `

¢%%` GrossElectric = HPIPGross + LPGross = 〔690〕 MW `

¢%%` GrossEfficiency = GrossElectric / ReactorDuty = 〔0.46〕 `

¢%%` BFPShaft = TotalSteam * BFPwork = 〔21.4〕 MW `

¢%%` CEPElectric = TotalSteam * CEPwork / CEPMotorEfficiency = 〔0.407〕 MW `

¢%%` CondenserDuty = TotalSteam * CondenserHeat = 〔793〕 MW `

The feed-pump turbine extraction already pays for BFP shaft power in the turbine
flow balance. Do **not** subtract BFP shaft power again from electrical
generation. Net export remains uncalculated: salt pumps, cooling-water pumps,
cooling-system fans, services, transformer losses and other station loads still
need a load list. No 600 MWe net-output claim is established by this gross
result.

## Conditional condenser estimate

Cooling water at 20°C inlet and 28°C outlet is a provisional design case, not
site weather data. The total heat-transfer coefficient is an assumed 2.5 kW/(m²
K), not a selected condenser performance guarantee. The area below excludes
design margin and explicit fouling/air-removal allowances. Cooling-system head,
pump power, water supply and final heat sink remain open.

¢` CondensingT = 306.024255091 K `

¢` CoolingIn = 293.15 K `

¢` CoolingOut = 301.15 K `

¢` WaterHeatCapacity = 4180 'J.kg-1.K-1' `

¢` WaterDensity = 998 'kg/m3' `

¢` CondenserU = 2500 'W.m-2.K-1' `

¢%%` CoolingMass = CondenserDuty / (WaterHeatCapacity * (CoolingOut -
CoolingIn)) = 〔23,716〕 'kg/s' `

¢%%` CoolingVolume = CoolingMass / WaterDensity = 〔23.8〕 'm3/s' `

¢%%` ColdApproach = CondensingT - CoolingIn = 〔12.9〕 K `

¢%%` HotApproach = CondensingT - CoolingOut = 〔4.87〕 K `

¢%%` CondenserLMTD = (ColdApproach - HotApproach) / ln(ColdApproach /
HotApproach) = 〔8.24〕 K `

¢%%` CondenserArea = CondenserDuty / (CondenserU * CondenserLMTD) = 〔38,513〕
'm2' `

## Feasibility checks and open decisions

*   The linear heater/reheater/pump balances close to 5.82e-11 J per kg of main
    flow; whole-cycle first-law residual is 7.47e-09 J/kg.
*   The reheater's 401-point counterflow check gives **12.32 K** minimum approach at
    470°C reheat. A 500°C trial gives **-5.59 K** and is rejected for
    temperature crossover. This is thermodynamic screening, not heat-exchanger
    sizing.
*   LP exhaust moisture is **12.64% by mass** under the equilibrium-property model.
    Acceptable wetness, blade erosion, moisture separation and actual turbine
    performance require review; no universal allowable is assumed.
*   The supercritical generator main-flow result differs slightly from the older
    property table: 711.670 kg/s versus 711.561 kg/s. Existing pipe geometry
    has not been revised for this small property-source difference.
*   Condensate-pump discharge is 1.2 times deaerator pressure. All other feedwater
    and main-steam line losses, except the 5% cold-reheat allowance, are
    omitted. BFP and turbine work must be revised when pressure budgets are
    assigned.

## Condenser-pressure sensitivity

Each case recloses the deaerator heater balance; reheat temperature is held
fixed.

*   5.0 kPa: gross 689.5 MW, condenser 793.1 MW, LP moisture 12.64%.
*   7.5 kPa: gross 674.6 MW, condenser 808.4 MW, LP moisture 11.45%.
*   10.0 kPa: gross 663.3 MW, condenser 820.0 MW, LP moisture 10.57%.

## References

The imported steam properties use [CoolProp water / IAPWS-95][2], version 7.2.0.
The [state table][3], solver, extraction fractions, provenance hash and
reproduction steps are kept alongside this worksheet.

[1]: README.md

[2]: https://coolprop.org/fluid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_properties/fluids/Water.html

[3]: rankine-states.csv

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

[14]: https://coolprop.org/fluid_properties/fluids/Water.html
