# Limitations

This section describes the limitations of the thermal-hydraulic sizing of the WISTR dual-tube steam generator. The analysis covers one of three 500 MWt units, with salt 890 → 810 K and water 560 → 830 K at 24 MPa. Each limitation is classified by the direction in which it biases the result:

- **Optimistic:** the analysis underestimates the required tube length, or overestimates thermal performance or margin.
- **Conservative:** the analysis overestimates the required length.
- **Uncertain:** the direction is unknown, or the item lies outside the validated range of the methods used.

Where possible, the effect is stated as a change in the required heated tube length \(L\) for the baseline geometry: 6,536 steam tubes and 4,902 salt tubes, 20 mm ID, 2 mm wall.

Three numbers frame the discussion:

- The sponsor spreadsheet model (`counterSG.xlsx`) gives **11.9 m**.
- The team's independent best-estimate model gives **15.4 m**.
- The plausible range, based on the limitations below, is **about 12.4 m to more than 18 m**.

The required overall conductance, UA = 3.034 MW/K, is fixed by the energy balance and terminal temperatures, so it is not affected by any of the limitations below. They affect only how much tube is needed to deliver that UA, and the pressure drop, wall temperatures and margins that follow from it.

---

## 1. Summary of Limitations

| # | Limitation | Direction | Estimated effect on L (baseline geometry) |
|---|---|---|---|
| 1 | Bulk-property steam-side correlation in the spreadsheet | Optimistic | +31% when corrected (11.85 → 15.48 m) |
| 2 | Spreadsheet correlation coefficient runs above standard forms even away from the pseudo-critical point | Optimistic | Included in item 1 (h is 22–25% above Dittus–Boelter) |
| 3 | Tube-to-tube interface (contact) resistance omitted in the spreadsheet; uncertain in the independent model | Optimistic | +9% to +45% (12.40 → 13.48–17.96 m) |
| 4 | Possible heat-transfer deterioration (HTD) at low mass flux | Optimistic | +5% to +12% beyond best estimate (15.36 → 16.14–17.17 m), possibly more |
| 5 | Correlations used outside their validated range (buoyancy-dominated mixed convection) | Uncertain, risk on the unsafe side | Not quantifiable with available correlations |
| 6 | Jackson correlation accuracy (about ±20%) | Uncertain | About −8% / +12% |
| 7 | Contact-strip heat flux concentration | Optimistic (for HTD and wall temperature) | Local q″/G is 1.5–1.9 kJ/kg vs 0.90–1.14 kJ/kg average |
| 8 | Deformed salt tubes modeled as round 20 mm bores | Optimistic for ΔP and velocity | Salt ΔP and velocity understated; small effect on L |
| 9 | Uniform flow distribution; no flow instability analysis | Optimistic | Not quantified |
| 10 | No fouling, oxide or corrosion layers | Optimistic | Not quantified |
| 11 | Film area taken as contact width only (spreadsheet) | Conservative | −20% combined with item 12 |
| 12 | Fixed wall conductivity k = 19 W/m·K (spreadsheet) | Conservative | Included in item 11 |
| 13 | 1-D circumferential fin model (independent model) | Uncertain | Needs 2-D conduction check |
| 14 | Radiation and heat transfer through air-pass tubes neglected | Slightly conservative (normal operation) | Small |
| 15 | Single-LMTD and ε–NTU methods invalid for sizing | Method limitation (not used) | Would oversize UA by 23.8% here; sign can reverse |
| 16 | Discretization and numerical method | Negligible | < 1% |
| 17 | Salt property correlations and freezing point | Uncertain | Salt film is about 18% of resistance; freezing margin 84–103 K |
| 18 | Constant 24 MPa property evaluation | Negligible | 39 kPa steam-side ΔP |
| 19 | Steady full-power operation only | Optimistic for margins | Part load, startup and transients not analyzed |
| 20 | Terminal temperature basis not finalized | Uncertain | 860 K steam outlet would add more than 4 m |
| 21 | Assumed roughness and minor-loss coefficients; headers excluded | Optimistic for ΔP | ΔP is a lower bound |
| 22 | Structural, materials and mechanical design not assessed | Outside scope | Hoop stress 120 MPa flagged |

---

## 2. Limitations That Make the Results Optimistic

### 2.1 Bulk-property correlation on the steam side

The sponsor spreadsheet applies one turbulent-pipe correlation, \(Nu = 0.0266\,Re^{0.805}Pr^{1/3}\), to both fluids, with properties evaluated at the bulk (mixed-mean) temperature. This works for the molten salt, whose properties vary smoothly; it agrees with the Gnielinski correlation within 3%. It does not work for supercritical water near its pseudo-critical temperature (654.4 K at 24 MPa).

At the pseudo-critical point:

- the bulk specific heat peaks at about 122 kJ/kg·K, compared with about 5 kJ/kg·K at the inlet;
- the bulk Prandtl number rises above 10;
- because \(Nu \propto Pr^{1/3}\), the correlation predicts a sharp spike in \(h\).

In reality, most of the thermal resistance lies in the thin fluid layer next to the wall. That layer is hotter than the bulk and has already passed the pseudo-critical point, so its specific heat, density and conductivity are much lower. The actual enhancement is far smaller than the bulk-property calculation suggests.

The Jackson (2002) correlation corrects for this. It adds wall-to-bulk density and integrated-specific-heat ratios, \((\rho_w/\rho_b)^{0.3}(\bar c_p/c_{p,b})^n\) ([IntechOpen review](https://www.intechopen.com/chapters/69345); [ICTP lecture notes](https://indico.ictp.it/event/a10196/session/19/contribution/14/material/0/0.pdf)). Compared with Jackson, the spreadsheet correlation overpredicts the steam-side coefficient:

- by 21% at the steam outlet;
- by about 50% at the inlet;
- by a factor of 2.4 at the pseudo-critical point.

The steam-side film is the largest thermal resistance in the exchanger (about 47% of the total in the best-estimate model), so this error carries directly into the length. Replacing only the steam-side correlation, with every other spreadsheet assumption unchanged, increases the required length from 11.85 m to 15.48 m (+31%).

### 2.2 Correlation coefficient above standard forms

Even well away from the pseudo-critical region, the spreadsheet correlation gives coefficients about 22–25% higher than the standard Dittus–Boelter form, \(Nu = 0.023\,Re^{0.8}Pr^{0.4}\). For example, at the inlet it gives 2,477 vs 2,009 W/m²·K, and at the outlet 1,066 vs 874 W/m²·K.

The team could not trace the specific form \(0.0266\,Re^{0.805}Pr^{1/3}\) to a standard reference. Its use on the water side is therefore unverified. On the salt side it agrees closely with Gnielinski, so there the concern is limited to the steam side.

### 2.3 Omitted tube-to-tube interface resistance

The spreadsheet cell labeled "tube contact resistance" contains only conduction through the two tube walls, \(2t/k = 2.1\times10^{-4}\) m²·K/W. It includes no thermal resistance at the interface where the salt tube presses against the steam tube.

Two separately manufactured tubes touch only at microscopic high points of their surfaces. Heat crossing the interface must pass through those small contacts or through the air in the gaps, which adds resistance. Published contact conductance for stainless steel on stainless steel with air in the gaps, at 1–10 atm contact pressure, is about 2,000–3,700 W/m²·K ([SOLIDWORKS thermal contact reference](https://help.solidworks.com/2025/english/solidworks/cworks/c_Thermal_Contact_Resistance.htm); [ANSYS Innovation Space](https://innovationspace.ansys.com/courses/wp-content/uploads/sites/5/2020/03/Lesson-3-Thermal-contact.pdf)). That corresponds to \(2.7\)–\(5.0\times10^{-4}\) m²·K/W, as large as or larger than both tube walls combined.

The independent model adopts 3,700 W/m²·K as the best estimate, because the roughly 1 MPa salt pressure is near the top of the tabulated pressure range. This value remains the largest single unknown in the analysis. It depends on:

- the joining method (pressed, expanded, brazed or diffusion-bonded);
- the contact pressure during operation, including differential thermal expansion between the hotter salt tubes and the cooler steam tubes;
- surface finish and oxide growth over time;
- gas conduction and radiation across the gaps at 750–890 K.

| Interface conductance (W/m²·K) | Required length (m) | Change vs perfect contact |
|---|---|---|
| Perfect contact | 12.40 | — |
| 10,000 | 13.48 | +9% |
| 3,700 (best estimate) | 15.36 | +24% |
| 2,000 | 17.96 | +45% |

Because the spreadsheet assumes perfect contact, its length is optimistic by at least the amount shown. Interface resistance may also grow over the plant's life if contact pressure relaxes through creep or oxide layers form, which would reduce performance over time.

### 2.4 Heat-transfer deterioration at low mass flux

The steam tubes operate at a very low mass flux, \(G\) = 115.5 kg/m²·s (0.0363 kg/s per tube in a 20 mm bore). The water enters the generator well below the pseudo-critical temperature, and in the bottom 4.6 m of the tubes the steam-side wall is hotter than 654 K while the bulk water is cooler. That is the condition under which supercritical water can show heat-transfer deterioration.

The physical mechanism:

1. The fluid next to the wall becomes light and gas-like. Its density is about one-third of the bulk density at the inlet, and its conductivity is low.
2. In upward heated flow, buoyancy accelerates this light layer relative to the dense core.
3. The velocity profile flattens, shear stress falls, and turbulence production is suppressed. The flow partly "laminarizes".
4. The heat transfer coefficient drops and the wall temperature rises locally.

Deterioration typically occurs in vertical upward flow near the tube inlet, before the bulk reaches the pseudo-critical temperature, and at high heat-flux-to-mass-flux ratios ([Int. J. Heat Fluid Flow review, 2024](https://www.sciencedirect.com/science/article/abs/pii/S0142727X24002595)). This describes the lower section of this design.

The ratio of wall heat flux to mass flux, \(q''/G\) (units of J/kg), indicates how strongly the wall is heated relative to the flow's ability to carry the heat away. Two relations show why:

\[
\frac{dh_b}{dx}=\frac{4}{D}\frac{q''}{G}
\qquad\text{and}\qquad
T_w-T_b\ \propto\ \frac{q''}{G^{0.8}}
\]

- The first is the energy balance on a slice of tube: the bulk enthalpy rises along the tube at a rate proportional to \(q''/G\).
- The second follows from \(T_w - T_b = q''/h\) with \(h \propto G^{0.8}\) for turbulent flow: a high ratio drives the wall far above the bulk temperature.

| Indicator | Threshold for concern | Best-estimate design value |
|---|---|---|
| \(T_b < T_{pc} < T_w\) | Present → deterioration-prone | Present for x = 0 to 4.6 m |
| \(q''/G\) ([ICTP](https://indico.ictp.it/event/a10196/session/19/contribution/14/material/0/0.pdf)) | > 0.4 kJ/kg | 0.90–1.14 kJ/kg (tube average); about 1.5–1.9 kJ/kg on contact strips; above 0.4 up to x ≈ 11.7 m |
| Yamagata limit \(q_c = 0.2G^{1.2}\) kW/m² ([Yamagata et al. 1972](https://www.sciencedirect.com/science/article/pii/0017931072901482)) | \(q'' > q_c\) | \(q_c\) ≈ 60 kW/m² vs \(q''\) = 104–132 kW/m² |
| Acceleration parameter \(K_v\) ([Energies 2020](https://www.mdpi.com/1996-1073/13/4/989)) | > 3×10⁻⁶ | ≤ 1.3×10⁻⁷ (not a concern) |

By both flux-based criteria, the design operates in the regime where deterioration is observed experimentally. The best-estimate model uses the Jackson correlation, which describes normal (non-deteriorated) forced convection. It therefore does not include any deterioration penalty. A sensitivity study, reducing the steam-side coefficient in the deterioration-prone zone, gives:

| Reduction of steam-side h in bottom zone | Required length (m) |
|---|---|
| None (best estimate) | 15.36 |
| 30% | 16.14 (+5%) |
| 50% | 17.17 (+12%) |

These reductions are illustrative and not predictions. Experiments with severe deterioration report larger local drops in \(h\) and sharp wall-temperature peaks, so the true penalty could exceed this range.

### 2.5 Operation outside the validated range of the correlations

The Jackson–Hall buoyancy parameter, \(Bo^* = Gr^*/(Re^{3.425}Pr^{0.8})\), measures how strongly buoyancy affects the flow. Its regimes are ([Frontiers in Energy Research, 2023](https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1129469/full)):

- below 6×10⁻⁷: buoyancy is negligible;
- 6×10⁻⁷ to 8×10⁻⁶: heat transfer is impaired;
- above 8×10⁻⁶: buoyancy dominates and heat transfer partially recovers.

In the lower section of this design, \(Bo^*\) = 4.2–5.7×10⁻⁵, well into the buoyancy-dominated regime. The bottom of the steam tubes is therefore in mixed convection, not the forced convection that both the spreadsheet correlation and the Jackson correlation were developed for.

Most supercritical-water heat-transfer data come from mass fluxes of order 10³ kg/m²·s; Yamagata's tests, for example, were at about 1,100–1,240 kg/m²·s ([ICTP](https://indico.ictp.it/event/a10196/session/19/contribution/14/material/0/0.pdf)). This design is roughly ten times lower. The buoyancy map suggests partial recovery of heat transfer in this regime, but the steam-side coefficient in the lower 4–5 m cannot be predicted with confidence by any correlation used here. This is listed as uncertain rather than optimistic, but it should be treated as a risk on the unsafe side until supported by data or CFD.

### 2.6 Heat flux concentration at the contact strips

Heat enters each steam tube only through three contact strips covering half its circumference, then spreads around the wall to the rest of the bore. The analysis uses perimeter-averaged heat flux for the deterioration criteria and a mean steam-side wall temperature.

The local heat flux on the inner surface behind the contact strips is about 1.7 times the perimeter average. So the local \(q''/G\) (about 1.5–1.9 kJ/kg) and the local wall temperature are both higher than the reported averages. The deterioration criteria and peak wall temperatures in this report are therefore optimistic locally.

### 2.7 Salt tube shape and flow area

The salt tubes are deformed into a non-circular shape to improve contact, but the analysis models them as round tubes with a 20 mm bore. For a fixed perimeter, a non-circular cross-section encloses less area than a circle. The real salt tubes will therefore have a smaller flow area and hydraulic diameter. As a result:

- the salt velocity (2.46 m/s) and pressure drop (103 kPa) are understated;
- the salt-side coefficient is slightly understated as well. This partly offsets the effect on length, because the salt film is only about 18% of the total resistance.

Corner regions of a deformed tube may also have locally low velocity and heat transfer. These quantities should be recalculated once the deformed cross-section is defined.

### 2.8 Uniform flow distribution and flow stability

The analysis assumes every tube carries the same flow. In practice:

- header design, tube-to-tube differences in resistance, and uneven heating cause maldistribution;
- the tubes that receive less flow heat up more, and in supercritical water this can be self-reinforcing because the density falls about tenfold along the heated length;
- low-mass-flux, upward-flow supercritical channels with large density change can be susceptible to density-wave flow oscillations, which this analysis does not assess.

Inlet orificing of the steam tubes is a common way to stabilize flow, but it adds pressure drop that is not included here.

### 2.9 Fouling, oxide and corrosion layers

No fouling or surface-film resistances are included on either side. Over the plant's life, oxide grows on the steam-side surface of stainless steel at 800–870 K, and corrosion products or deposits may form on the salt side. These layers add resistance and would increase the required length or reduce performance over time. No allowance is made; the team should apply one once the materials and water chemistry are defined.

### 2.10 Pressure drop is a lower bound

The pressure-drop calculation uses:

- an assumed wall roughness of 1.5 µm (smooth drawn tubing);
- placeholder minor-loss coefficients (K = 2.1 total: entrance, exit and two bends);
- tube friction, acceleration and gravity only.

It does not include inlet and outlet headers, tube-sheet penetrations, flow orificing, the deformed salt-tube geometry, or roughness growth from corrosion. The reported 103 kPa (salt) and 39 kPa (steam) should be treated as lower bounds, and the 390 kW salt pumping power per generator as a minimum.

---

## 3. Limitations That Make the Results Conservative

### 3.1 Film area limited to the contact width (spreadsheet)

The spreadsheet applies both convective films over the contact width only (37.7 mm per steam tube). In reality, heat also conducts around the tube wall into the half of the steam-tube bore not directly behind a salt contact, and that surface also transfers heat to the water.

The independent model accounts for this with a circumferential fin-efficiency treatment. At the inlet, this raises the effective steam-side perimeter from 37.7 mm to about 47 mm. The spreadsheet's film-area assumption is therefore conservative.

### 3.2 Fixed wall conductivity (spreadsheet)

The spreadsheet uses \(k\) = 19 W/m·K for the tube walls. Type 316 stainless steel has a conductivity of 19.8–22.8 W/m·K at 700–900 K ([316 SS property data](https://qedfusion.org/LIB/PROPS/PANOS/ss.html)), so the spreadsheet slightly overstates the wall resistance.

Together, the fin-area correction and the temperature-dependent conductivity shorten the required length by about 20% (15.48 m → 12.40 m at perfect contact). This conservatism partly hides the optimistic items in Section 2: the spreadsheet's 11.9 m result is the net of errors that point in opposite directions, not a result that happens to be accurate.

### 3.3 Radiation and air-pass tubes neglected

Radiation across the small air gaps between tubes is neglected, and the air-pass tubes are assumed to carry no heat during normal operation. Both would add a small parallel heat path, so neglecting them is slightly conservative. In emergency air cooling these paths become the primary heat-removal route, and they are not analyzed here (Section 5).

---

## 4. Method Limitations and Uncertain Effects

### 4.1 Single-LMTD and ε–NTU methods cannot be used for sizing

The log-mean temperature difference (LMTD) and effectiveness–NTU methods both come from integrating the counterflow energy balance:

\[
d(\Delta T) = d\dot Q\left(\frac{1}{C_s}-\frac{1}{C_w}\right)
\]

This assumes constant heat capacity rates \(C = \dot m c_p\) and a constant overall coefficient \(U\). Neither holds here:

- **Capacity rate:** the water's specific heat varies by a factor of about 40 through the pseudo-critical region, so its capacity rate ranges from 0.74 to 28.1 MW/K, against 6.25 MW/K for the salt. The water is the smaller stream over most of the exchanger but the larger one between 651 and 659.5 K, which carries 23.7% of the duty. No single "C_min" or capacity ratio exists.
- **Shape of ΔT:** because of this, the salt-to-water temperature difference is S-shaped rather than linear in heat duty.
- **U:** the local overall coefficient also varies by a factor of about 1.6 along the tube.

The analysis therefore uses a 540-segment march, applying the LMTD only within each 0.5 K step, where the assumptions hold. For reference, the lumped methods would give:

| Method | Required UA | Error |
|---|---|---|
| Single LMTD (133.1 K) | 3.756 MW/K | +23.8% |
| ε–NTU chart (NTU 2.03 required vs 1.64 actual) | 3.756 MW/K | +23.8% |
| Three-zone LMTD | 3.210 MW/K | +5.8% |
| 540-segment march (used) | 3.034 MW/K | reference |

The single-LMTD error happens to be conservative for these temperatures, but it is not reliably so:

- Near the water inlet, the actual temperature difference is smaller than the linear assumption, so a lumped method undersizes that region.
- With different terminal temperatures or flow ratios, the net error can change sign.
- A lumped method cannot detect an internal pinch, where the minimum temperature difference occurs inside the exchanger rather than at an end.

The values of ε (0.922) and NTU (1.64) are reported only as performance metrics, not as a basis for sizing.

### 4.2 Accuracy of the Jackson correlation

The Jackson correlation is reported to predict supercritical-water heat transfer within about ±20% for simple geometries in forced convection ([ICTP](https://indico.ictp.it/event/a10196/session/19/contribution/14/material/0/0.pdf)). Its data come from round tubes heated uniformly around the circumference, not from tubes heated on three contact strips. With the steam-side film at about 47% of the total resistance, a ±20% change in \(h\) changes the required length by roughly −8% to +12%. This is in addition to the deterioration concerns in Sections 2.4–2.5.

### 4.3 Circumferential conduction model

The independent model treats conduction around the steam-tube wall as two independent 1-D fins (60° and 120° arcs). It assumes:

- the outer surface of those arcs is adiabatic;
- the heat path through the two walls is a flat slab across the contact width.

The real problem is two-dimensional: curved walls, deformed salt tubes, non-uniform contact pressure, and heat flowing both radially and around the circumference. The fin model sits between the spreadsheet's contact-width-only assumption and a full-perimeter assumption, but its accuracy has not been verified. A 2-D finite-element conduction model of one steam tube with its surrounding salt and air tubes is recommended to calibrate it.

### 4.4 Salt properties and freezing point

The salt properties come from sponsor-supplied correlations and are taken as given. No uncertainty band was available. The salt film is about 18% of the total resistance, so moderate errors in salt conductivity or viscosity have a secondary but real effect on length. They have a larger effect on salt pressure drop and pumping power through viscosity.

The freezing point depends on composition. Published NaCl–KCl–MgCl₂ eutectic melting points range from about 656 to 675 K ([MDPI Energies 2025](https://www.mdpi.com/1996-1073/18/14/3616); [ASME J. Solar Energy Eng.](https://asmedigitalcollection.asme.org/solarenergyengineering/article/143/4/041005/1091929/Thermophysical-Properties-Experimentally-Tested)). The analysis uses the conservative 675 K, giving an 84 K margin to the coldest salt-side wall (759 K) at full power. Both the margin and the freezing point must be confirmed once the WISTR coolant composition is fixed.

### 4.5 Constant-pressure water properties

Water properties are evaluated at a constant 24 MPa. The calculated steam-side pressure drop is only 39 kPa, about 0.16% of the system pressure, so the error is negligible at full power. It would matter more if orificing or header losses add significant pressure drop, or at part-load pressures closer to the critical point (22.06 MPa), where properties are more sensitive.

### 4.6 Discretization and numerical method

The march uses 0.5 K water-temperature steps, with properties evaluated at the mean of each step. Halving the step changes the length by less than 0.01%. The spreadsheet's coarser 5 K steps with end-node properties give 11.92 m against 11.85 m for the refined method, a 0.6% difference. Its explicit salt-temperature update closes the energy balance within 0.04 K. Numerical error is negligible compared with the physical uncertainties above.

---

## 5. Scope Limitations

### 5.1 Steady, full-power operation only

All results are for steady operation at the full 500 MWt per generator. The following were not analyzed:

- part-load operation;
- startup and shutdown;
- load-following transients;
- loss-of-feedwater or loss-of-flow events.

These conditions matter for the following reasons:

- **Freezing margin:** at reduced salt flow or with cold feedwater, the salt-side wall at the bottom of the generator moves closer to the salt freezing point. The 84 K full-power margin may shrink substantially.
- **Deterioration zone:** at part load, the relationship between mass flux and heat flux changes, and the deterioration-prone zone may move or grow.
- **Thermal stress:** temperature differences between the salt tubes and steam tubes during transients create thermal stresses and could change interface contact pressure.

### 5.2 Terminal temperature basis

The analysis uses the spreadsheet terminal temperatures, with a steam outlet of 830 K. The kickoff deliverables list a steam outlet of 860 K. At 860 K with 875 K salt inlet, the hot-end temperature difference narrows to 15 K. With spreadsheet-basis physics, the required length rises to about 16.9 m. With the independent model's corrections the increase would be larger. The design-point temperatures must be confirmed with the sponsor before the geometry is finalized.

### 5.3 Structural, materials and mechanical design

The thermal-hydraulic analysis does not assess:

- **Pressure containment:** a thin-wall estimate of the steam-tube hoop stress gives \(\sigma = P D_i/(2t)\) = 24 × 20/(2 × 2) = 120 MPa at metal temperatures up to about 865 K. This must be checked against ASME allowable stresses at temperature, including creep, and may govern wall thickness. A thicker wall would in turn add conduction resistance and length.
- **Thermal and differential-expansion stresses** between tube sets.
- **Flow-induced vibration** and tube support design.
- **Materials compatibility:** salt-side corrosion, steam-side oxidation and creep.
- **Manufacturability** of the deformed-tube contact geometry.

### 5.4 Emergency air cooling and natural circulation

The dual-tube design is intended to serve as an emergency cooler: air flows through the air-pass tubes, and salt circulates naturally. This analysis does not evaluate:

- air-side heat transfer or radiation;
- the decay-heat removal capacity;
- the natural-circulation flow the loop can sustain.

The buoyancy head calculated over the heated length alone is small compared with the full-flow friction loss. A dedicated loop analysis is needed.

---

## 6. Combined Effect and Recommendations

The spreadsheet's 11.9 m heated length results from several optimistic simplifications that are partly offset by conservative ones:

- **Optimistic:** the bulk-property steam-side correlation and the omitted interface resistance.
- **Conservative:** contact-width film areas and fixed wall conductivity.

Correcting each of these gives a best estimate of **15.4 m** for the baseline geometry. The range is about **12.4 m (perfect contact) to 18 m (low contact conductance)**, and more if heat-transfer deterioration is significant.

The largest remaining uncertainties are, in order:

1. the tube-to-tube interface conductance;
2. steam-side heat transfer in the low-mass-flux, buoyancy-dominated lower section;
3. accuracy of the circumferential conduction model.

Recommended actions to reduce these limitations:

1. **Define the tube-joining method** with the sponsor, then bound the interface conductance with literature data or a simple bench test.
2. **Raise the steam-side mass flux** with fewer or smaller-bore steam tubes. For example, 16 mm bores at the same tube count raise G from 115 to 181 kg/m²·s. This moves the design toward the validated range of the correlations and reduces deterioration risk.
3. **Evaluate the lower 5 m of the steam tubes** with CFD, or check it against low-mass-flux supercritical-water data.
4. **Build a 2-D conduction model** of one steam tube and its neighbors to replace the 1-D fin approximation.
5. **Carry the length range,** not a single value, into the layout, height and cost estimates until items 1–4 are resolved. Size the vessel for the upper end of the range.
6. **Extend the analysis** to part load, startup, emergency air cooling and natural circulation, with salt freezing margin as a governing criterion.
7. **Confirm the design-point steam outlet temperature** (830 K vs 860 K) and the WISTR coolant composition with the sponsor.
