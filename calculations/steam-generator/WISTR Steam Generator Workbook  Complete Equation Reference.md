# WISTR Steam Generator Workbook: Complete Equation Reference

This document explains the equations actually implemented in `WISTR_SG_Calculation_Workbook.xlsx`: their purpose, variables, units, workbook locations, and engineering significance. It describes the existing thermal workbook, not the later tube-layout study or a pressure-code-qualified design, and it does not change the workbook.

## Scope and how to use this reference

The audited workbook contains **74,631 formula cells**, grouped into **252 column-specific, relative-reference formula families**. A formula repeated down 540 rows is explained once rather than printed 540 times; the exact Excel formula, representative cell, and all covered rows are provided in the formula register at the end. First-row initialization formulas, later-row recurrences, the two wall-temperature passes, summary formulas, and chart links are all included.

The starting design in this workbook is one 500 MW thermal steam generator, 6,536 steam tubes, 20 mm tube inside diameter, and 2 mm walls. Those are thermal-model inputs, not an approved mechanical design; the later thicker-wall layout study is a separate calculation.

- **Equation explanations:** The main sections give mathematical expressions and engineering interpretation. Equation IDs such as `E01` provide stable cross-references.
- **Exact implementation:** The final formula register preserves what Excel actually evaluates, including any implementation caveats. The named-range dictionary identifies the inputs behind names such as `G_w` and `h_contact`.
- **Cell notation:** `Temperature_March!G5:G544` means the equation is repeated in every data row in that range. In sections about a particular march sheet, a column specification means rows 5–544 unless a different range is stated.
- **Sheet abbreviations:** TM = `Temperature_March`; SS = `Model_Spreadsheet`; BE = `Model_BestEstimate`. These abbreviations are used only in this reference.
- **No-formula sheets:** `README`, `Studies`, and `Water_Properties` contain no Excel formulas. The property data and study results are stored values; their generating relationships and limitations are nevertheless explained below.

### Calculation sequence

The workbook first establishes duty, flows, and geometry on `Inputs`. `Temperature_March` calculates the energy transferred and the salt/water temperature differences for 540 small water-temperature intervals; the two model sheets then calculate heat-transfer resistance and the length needed for each interval. `Results` aggregates the calculations, and `Charts` links to their outputs.

The energy calculation is therefore separate from the heat-transfer calculation. Both model sheets must transfer the same duty between the same terminal temperatures, but different predicted resistances produce different tube lengths.

## Notation and unit conventions

This reference uses \(H\) for specific enthalpy and \(h\) for a convection coefficient, avoiding the workbook's occasional use of the letter `h` for both. Subscripts \(b\), \(s\), \(w\), and \(m\) mean bulk water, salt, wall or water as explicitly identified, and metal; “wall water properties” means properties of fluid evaluated at the metal/fluid interface temperature, not properties of steel.

| Symbol | Definition | Units used in mathematical equations |
|---|---|---|
| \(Q,\Delta Q_i\) | Total SG thermal duty; heat-transfer rate in segment \(i\) | W unless an MW conversion is shown |
| \(\dot m,\dot m_t\) | Total mass flow; mass flow per tube | kg/s |
| \(H\) | Specific enthalpy | J/kg; the water table stores kJ/kg |
| \(c_p,c_{p,\mathrm{seg}},\bar c_p\) | Point specific heat; segment secant specific heat; wall-to-bulk secant specific heat | J/(kg·K) |
| \(T_b,T_s,T_w\) | Bulk water, bulk salt, steam-side inner-wall temperature | K |
| \(D_i,D_o,t,r_i,r_m\) | Tube inside diameter, outside diameter, thickness, inner radius, mid-wall radius | m |
| \(A_f,w,P_{\mathrm{eff}}\) | Tube flow area, assumed contact width, effective heated/wetted perimeter | m²; m; m |
| \(G,v,\rho,\mu,\nu,\beta\) | Mass flux, speed, density, dynamic viscosity, kinematic viscosity, expansion coefficient | kg/(m²·s); m/s; kg/m³; Pa·s; m²/s; 1/K |
| \(k,h,h_c\) | Conductivity, convection coefficient, contact conductance | W/(m·K); W/(m²·K); W/(m²·K) |
| \(R'',R'\) | Area-normalized resistance; resistance factor used with heat per axial length | m²·K/W; K·m/W |
| \(q'',q'\) | Heat flux; heat-transfer rate per metre of one steam tube | W/m²; W/m |
| \(U,UA,C\) | Overall coefficient, integrated conductance, heat-capacity rate | W/(m²·K); W/K; W/K |
| \(N_w,N_s,N_a,N_{\mathrm{seg}}\) | Steam-, salt-, air-tube counts; segment count | Dimensionless counts |
| \(f_D,K,\epsilon_r\) | Darcy friction factor, minor-loss coefficient, absolute wall roughness | Dimensionless; dimensionless; m |
| \(\eta_f,\eta_{\mathrm{plant}},\varepsilon\) | Fin efficiency, plant efficiency, heat-exchanger effectiveness | Dimensionless |

The prime on \(R'\) does not mean a derivative. It identifies a quantity with units K·m/W so that \(q'R'\) is a temperature difference; the resistance of an actual segment of length \(\Delta L\) is \(R'/\Delta L\), in K/W. Similarly, the double prime on \(q''\) denotes “per unit area,” not a second derivative.

Conversions used throughout are \(1\text{ MW}=10^6\text{ W}=10^3\text{ kW}\), \(1\text{ kJ}=10^3\text{ J}\), and \(1\text{ kPa}=10^3\text{ Pa}\). These factors explain many otherwise unexplained `1000` and `1000000` terms in Excel.

## Plant duty, energy balance, and geometry

### Plant thermal-to-electric efficiency (E01)

\[
\eta_{\mathrm{plant}}=\frac{P_e}{P_{\mathrm{th}}}
\]

- **Location:** `Inputs!C10`.
- **Variables:** \(P_e\) is plant electric output (`C8`, MW); \(P_{\mathrm{th}}\) is reactor thermal output (`C7`, MW).
- **Purpose and significance:** Establishes the 600/1500 = 0.40 plant efficiency. It is not a heat-transfer efficiency to be applied again inside the SG.

### Thermal duty and electric allocation per SG (E02)

\[
Q_{\mathrm{SG}}=\frac{P_{\mathrm{th}}}{N_{\mathrm{gen}}},
\qquad P_{e,\mathrm{share}}=\eta_{\mathrm{plant}}Q_{\mathrm{SG}}
\]

- **Location:** `Inputs!C11:C12`.
- **Variables:** \(N_{\mathrm{gen}}\) is the SG count (`C9`); both outputs use MW.
- **Purpose and significance:** Assigns 500 MW thermal to each of three SGs and a 200 MW electric share for bookkeeping. The exchanger is sized for 500 MW, not 200 MW.

### End temperature approaches and march step (E03)

\[
\Delta T_c=T_{s,\mathrm{out}}-T_{b,\mathrm{in}},\qquad
\Delta T_h=T_{s,\mathrm{in}}-T_{b,\mathrm{out}},\qquad
\delta T_b=\frac{T_{b,\mathrm{out}}-T_{b,\mathrm{in}}}{N_{\mathrm{seg}}}
\]

- **Location:** `Inputs!C21:C22`, `C24`.
- **Variables:** Terminal temperatures are `C16:C19`; segment count is `C23`.
- **Purpose and significance:** Defines the cold/hot approaches and temperature discretization. The base values are 250 K, 60 K, and 0.5 K; the 540 intervals have unequal axial lengths.

### Inlet/outlet water enthalpy (E04)

\[
H_{\mathrm{in}}=\mathcal I_H(T_{b,\mathrm{in}}),\qquad
H_{\mathrm{out}}=\mathcal I_H(T_{b,\mathrm{out}})
\]

- **Location:** `Inputs!C27:C28`.
- **Variables:** \(\mathcal I_H\) is the linear table-interpolation operation in E14; Excel stores these outputs in kJ/kg.
- **Purpose and significance:** Uses real-fluid enthalpy rather than assuming one constant specific heat over the entire heating range.

### Water/steam mass flow (E05)

\[
\dot m_w=\frac{Q}{H_{\mathrm{out}}-H_{\mathrm{in}}}
\]

- **Location:** `Inputs!C29`; Excel form `=Q_SG*1000/(h_w_out-h_w_in)`.
- **Variables:** \(Q_{\mathrm{SG}}\) is in MW in Excel and enthalpies are in kJ/kg, requiring the factor 1000.
- **Purpose and significance:** Determines the total water flow required to absorb the prescribed duty. This flow sets tube mass flux and therefore both heat transfer and pressure loss.

### Salt enthalpy change and salt flow (E06)

\[
\Delta H_s=\int_{T_{s,\mathrm{out}}}^{T_{s,\mathrm{in}}}(a_c+b_cT)\,dT
=a_c(T_{s,\mathrm{in}}-T_{s,\mathrm{out}})
+\frac{b_c}{2}(T_{s,\mathrm{in}}^2-T_{s,\mathrm{out}}^2),
\qquad \dot m_s=\frac{Q}{\Delta H_s}
\]

- **Location:** `Inputs!C30:C31`; \(a_c=\texttt{cp_a}\) and \(b_c=\texttt{cp_b}\) are `C55:C56`.
- **Variables:** \(\Delta H_s\) is J/kg; `C31` converts MW to W using \(10^6\).
- **Purpose and significance:** Integrates the specified temperature-dependent salt heat capacity exactly for its linear form. It avoids treating the inlet heat capacity as representative of the entire salt temperature change.

### Average heat-capacity rates (E07)

\[
C_{s,\mathrm{avg}}=\frac{Q}{T_{s,\mathrm{in}}-T_{s,\mathrm{out}}},
\qquad
C_{w,\mathrm{avg}}=\frac{Q}{T_{b,\mathrm{out}}-T_{b,\mathrm{in}}}
\]

- **Location:** `Inputs!C32:C33`, named `C_salt` and `C_w_avg`.
- **Variables:** With \(Q\) in MW, \(C\) is MW/K.
- **Purpose and significance:** Supplies average capacity rates for summary comparisons. The workbook uses \(C_{w,\mathrm{avg}}\) as its average \(C_{\min}\); it is not the local water capacity rate near the pseudo-critical peak.

### Reference cycle work per kilogram (E08)

\[
w_{\mathrm{net,ref}}=\eta_R(H_{\mathrm{out}}-H_{\mathrm{in}})
\]

- **Location:** `Inputs!C34`; \(\eta_R\) is `C13`, distinct from the plant efficiency.
- **Variables:** With table enthalpy in kJ/kg, work is kJ/kg.
- **Purpose and significance:** Estimates cycle work using an assumed reference efficiency. It does not model a turbine, condenser, pump, or complete Rankine cycle and does not determine the SG length.

### Tube counts (E09)

\[
N_s=\operatorname{ROUND}(r_sN_w,0),\qquad N_a=N_w-N_s
\]

- **Location:** `Inputs!C39:C40`; \(N_w\) and \(r_s\) are `C37:C38`.
- **Variables:** \(r_s\) is salt tubes per steam tube, nominally 0.75.
- **Purpose and significance:** Preserves the intended 4:3:1 steam:salt:air count relationship, subject to integer rounding. Counts determine flow splitting; they do not by themselves verify a manufacturable contact pattern.

### Tube dimensions and flow area (E10)

\[
D_o=D_i+2t,\quad A_f=\frac{\pi D_i^2}{4},\quad
r_i=\frac{D_i}{2},\quad r_m=\frac{D_i+t}{2}
\]

- **Location:** `Inputs!C43:C44`, `C46:C47`; \(D_i,t\) are `C41:C42`.
- **Purpose and significance:** Establishes the flow area and radii used for velocity, mass flux, heat-transfer area, and fin conduction. Both fluid tube sets have the same dimensions in this workbook.

### Assumed contact width (E11)

\[
w=\frac{\pi D_o}{2}
\]

- **Location:** `Inputs!C45`, named `w_contact`.
- **Variables:** \(w\) is contact area per unit axial length, in m.
- **Purpose and significance:** Represents a total contact arc of 180° per steam tube in the model. It assumes broad formed contacts; it is not the actual contact width of undeformed circular tubes merely touching along a line, and it needs geometric verification.

### Flow per tube and steam mass flux (E12)

\[
\dot m_{w,t}=\frac{\dot m_w}{N_w},\qquad
\dot m_{s,t}=\frac{\dot m_s}{N_s},\qquad
G_w=\frac{\dot m_{w,t}}{A_f}
\]

- **Location:** `Inputs!C48:C50`.
- **Purpose and significance:** Assumes equal flow through every parallel tube. Mass flux, unlike velocity, does not change with local density when mass flow and cross-section remain fixed.

### Explicit fractional constants (E13)

\[
b_{\mathrm{Nu}}=\frac13,\qquad f_{\mathrm{backed}}=\frac23
\]

- **Location:** `Inputs!C66`, `C81`.
- **Variables:** \(b_{\mathrm{Nu}}\) is the sponsor Prandtl exponent; \(f_{\mathrm{backed}}\) is the salt-tube perimeter fraction directly backed by contacts.
- **Purpose and significance:** These are formula cells even though they evaluate fixed fractions. The latter controls the division between direct heating and fin-assisted heat transfer.

## Property data and interpolation

### Linear interpolation used throughout Excel (E14)

\[
x=\frac{T-T_0}{\delta T_{\mathrm{tab}}},\qquad j=\lfloor x\rfloor,\qquad
\theta=x-j,\qquad
\mathcal I_y(T)=y_j+\theta(y_{j+1}-y_j)
\]

- **Locations:** `Inputs!C27:C28`; TM `E:F`, `U:Z`; BE `O:P`, `AG:AH`; `Results!C15:D15` and the density lookups in `C36:D37`. The same operation is used for metal conductivity in BE `T` and `AL`.
- **Variables:** \(T_0\) is the first table temperature; \(\delta T_{\mathrm{tab}}\) is table spacing; \(y_j\) and \(y_{j+1}\) are neighboring tabulated values. Excel uses `INT` for \(j\) and `INDEX(...,j+1)` for the zero-based \(j\)-th entry.
- **Purpose and significance:** Makes property values available at arbitrary model temperatures without embedding the full fluid equation of state in Excel. It is a numerical lookup, not a heat-transfer correlation.

For water, \(T_0=555\) K and spacing is 0.25 K (`Water_Properties!C3`, `E3`); the arrays occupy rows 5–1385. Even when \(\theta=0\), the formula references the next row, so exactly the upper table endpoint of 900 K can cause an out-of-range reference; use temperatures below it unless the formula or table is extended.

### Property columns and what is not an Excel equation

The workbook stores water properties at 24 MPa as constants in `Water_Properties!B5:H1385`. These were generated by the companion model; the sponsor cites the [NIST thermophysical-properties database](https://webbook.nist.gov/chemistry/fluid/) for its fluid-property inputs.

| Column / named array | Stored quantity | Where used |
|---|---|---|
| B / `WP_T` | Temperature, K | Lookup grid |
| C / `WP_h` | Enthalpy, kJ/kg | Energy balance, segment heat, Jackson secant \(c_p\) |
| D / `WP_rho` | Density, kg/m³ | Velocities, Jackson density ratio, pressure drop |
| E / `WP_cp` | Point \(c_p\), kJ/(kg·K) | Jackson bulk Prandtl number and acceleration check |
| F / `WP_mu` | Dynamic viscosity, Pa·s | Reynolds/Prandtl numbers and hydraulic calculations |
| G / `WP_k` | Water conductivity, W/(m·K) | Nusselt-to-\(h\) conversion, Prandtl and buoyancy checks |
| H / `WP_beta` | Isobaric expansion coefficient, 1/K | Buoyancy and acceleration screening |

The thermodynamic meaning of the final column is \(\beta=-(1/\rho)(\partial\rho/\partial T)_P\). This definition explains the stored input; Excel does not evaluate that derivative, nor does it evaluate the underlying IAPWS equation of state.

Changing `Inputs!C20` does not regenerate these data or the fixed pseudo-critical temperature. The pressure cell is informational for property generation and is also used in the hoop-stress estimate, so changing it alone would create an inconsistent thermal model.

### Salt property correlations (E15)

\[
\rho_s=a_\rho+b_\rho T_s,\quad
c_{p,s}=a_c+b_cT_s,\quad
\mu_s=a_\mu\exp(b_\mu/T_s),\quad
k_s=a_k+b_kT_s
\]

- **Location:** TM `AA:AD`, evaluated at the segment mean salt temperature `L`.
- **Variables:** Coefficients are `Inputs!C53:C60`; outputs are kg/m³, J/(kg·K), Pa·s, and W/(m·K).
- **Purpose and significance:** Supplies local salt properties for flow and convection calculations. These are accepted sponsor-input correlations; the workbook does not establish their validity for a different salt composition.

## Temperature and energy march

### Segment index and water-temperature boundaries (E16)

\[
i_1=1,\quad i_{r}=i_{r-1}+1;\qquad
T_{b,0}=T_{b,\mathrm{in}},\quad T_{b,i}=T_{b,i-1}+\delta T_b,\quad
T_{b,m,i}=\frac{T_{b,i-1}+T_{b,i}}2
\]

- **Location:** TM `A:D`; initialization in `A5`, `B5`; recurrences in `A6:A544`, `B6:B544`.
- **Purpose and significance:** Defines the marching coordinate as water temperature. Height is an output calculated later, so uniform temperature steps do not imply uniform length steps.

### Segment enthalpies and segment heat (E17)

\[
H_{i-1}=\mathcal I_H(T_{b,i-1}),\quad H_i=\mathcal I_H(T_{b,i}),\qquad
\Delta Q_i=\dot m_w(H_i-H_{i-1})
\]

- **Location:** TM `E:G`; Excel divides the kW enthalpy-flow product by 1000 to report MW.
- **Purpose and significance:** Enforces energy conservation in each interval. Near the pseudo-critical region, a small temperature rise may require a relatively large enthalpy increase.

### Cumulative heat and duty fraction (E18)

\[
Q_{\mathrm{cum},0}=0,\quad
Q_{\mathrm{cum},i}=Q_{\mathrm{cum},i-1}+\Delta Q_i,\qquad
F_i=\frac{Q_{\mathrm{cum},i}}{Q}
\]

- **Location:** TM `H:I`; first-row `H5=G5`, later rows add to the preceding cumulative value.
- **Purpose and significance:** Tracks how much duty has been transferred from the cold end. \(F_i\) is the horizontal coordinate of the temperature-difference comparison chart.

### Salt temperature from cumulative energy (E19)

Define \(e_i=Q_{\mathrm{cum},i}/\dot m_s\) in J/kg and \(T_{s,0}=T_{s,\mathrm{out}}\). Then

\[
X_i=a_cT_{s,0}+\frac{b_c}{2}T_{s,0}^2+e_i,\qquad
T_{s,i}=\frac{-a_c+\sqrt{a_c^2+2b_cX_i}}{b_c},
\qquad T_{s,m,i}=\frac{T_{s,i-1}+T_{s,i}}2
\]

- **Location:** TM `J:L`; `J` uses the cumulative heat before the segment, `K` after it, and `L` their temperature average.
- **Variables:** \(a_c,b_c\) are E06's salt heat-capacity coefficients. MW in column `H` is multiplied by \(10^6\) before division by salt flow.
- **Purpose and significance:** Inverts the salt enthalpy integral so the salt and water energy balances agree. The march proceeds upward from the salt outlet, opposite to salt flow; an increasing salt temperature along the plotted upward coordinate is therefore expected.

This implementation assumes \(b_c\ne0\). If a constant salt heat capacity is substituted by setting \(b_c=0\), the inverse must instead be written \(T_{s,i}=T_{s,0}+e_i/a_c\); the current quadratic expression would divide by zero.

### Segment driving-temperature differences and local LMTD (E20)

\[
\Delta T_{i,a}=T_{s,i-1}-T_{b,i-1},\qquad
\Delta T_{i,b}=T_{s,i}-T_{b,i},
\]
\[
\Delta T_{\mathrm{lm},i}=
\begin{cases}
\Delta T_{i,a},&|\Delta T_{i,a}-\Delta T_{i,b}|<10^{-9}\ {\rm K},\\
\dfrac{\Delta T_{i,a}-\Delta T_{i,b}}
{\ln(\Delta T_{i,a}/\Delta T_{i,b})},&\text{otherwise}.
\end{cases}
\]

- **Location:** TM `M:O`.
- **Purpose and significance:** Supplies the local temperature driving force while avoiding a 0/0 calculation for equal end differences. Small segments permit a local LMTD approximation even though a single constant-property LMTD treatment is unsuitable for the full exchanger.

Both end differences must remain positive for the intended hot-to-cold configuration. A pinch, sign change, or impossible terminal-temperature choice requires separate handling rather than blindly evaluating the logarithm.

### Required segment conductance (E21)

\[
(UA)_i=\frac{\Delta Q_i}{\Delta T_{\mathrm{lm},i}}
\]

- **Location:** TM `P`; output is MW/K.
- **Purpose and significance:** Separates the conductance demanded by the temperature/energy path from the geometry required to supply it. Both model sheets use this same thermal requirement.

### Constant-capacity comparison line (E22)

\[
\Delta T_{\mathrm{linear},i}=\Delta T_c+(\Delta T_h-\Delta T_c)F_i
\]

- **Location:** TM `Q`.
- **Purpose and significance:** Generates the comparison curve for the single-LMTD chart. It is linear with cumulative duty fraction, not necessarily with physical height; it is not used to size the tube.

### Segment effective heat capacity, capacity rate, and comparison flag (E23)

\[
c_{p,\mathrm{seg},i}=\frac{H_i-H_{i-1}}{T_{b,i}-T_{b,i-1}},\qquad
C_{w,i}=\dot m_w c_{p,\mathrm{seg},i}
\]
\[
\mathrm{flag}_i=
\begin{cases}
\text{“Water”},&C_{w,i}>C_{s,\mathrm{avg}},\\
\text{“Salt”},&\text{otherwise}.
\end{cases}
\]

- **Location:** TM `R:T`; outputs are kJ/(kg·K), MW/K, and text.
- **Purpose and significance:** Shows the large variation of water capacity rate and the reversal of which stream has the larger capacity rate. The comparison uses the average salt capacity rate, not the slightly varying local \(\dot m_sc_{p,s}(T)\).

The segment secant \(c_{p,\mathrm{seg}}\) differs from both point \(c_p(T_b)\) and Jackson's wall-to-bulk \(\bar c_p\). The sponsor-model Prandtl calculation uses the segment secant, whereas Jackson uses point bulk \(c_p\).

### Properties evaluated at segment means (E24)

\[
(\rho_b,\mu_b,k_b,c_{p,b},H_b,\beta_b)
=\mathcal I(T_{b,m,i})
\]

- **Location:** TM `U:Z`; salt properties follow E15 in `AA:AD`.
- **Purpose and significance:** Gives a representative local property set for each small interval. \(H_b\) is interpolated at the midpoint temperature rather than assumed equal to the average of endpoint enthalpies.

## Shared flow and heat-transfer relationships

### Data transfer and per-tube duty (E25)

\[
(i,T_b,T_s,\Delta T_{\mathrm{lm}})_{\mathrm{model}}
=(i,T_{b,m},T_{s,m},\Delta T_{\mathrm{lm}})_{\mathrm{TM}},
\qquad \Delta Q_{t,i}=\frac{\Delta Q_i}{N_w}
\]

- **Location:** SS and BE `A:E`; column `E` multiplies TM's MW by \(10^6\) before dividing by \(N_w\).
- **Purpose and significance:** Ensures both models solve the same segment energy balance. Direct links in columns `A:D` are bookkeeping, not independent physical assumptions.

### Velocity and Reynolds number (E26)

\[
v=\frac{\dot m_t}{\rho A_f}=\frac{G}{\rho},\qquad
Re=\frac{\rho vD_i}{\mu}=\frac{GD_i}{\mu}
\]

- **Location:** SS water `F:G`, salt `K:L`; BE salt `F:G`, water `L` and `BI`.
- **Variables:** Use the relevant fluid's density and viscosity; \(Re\) is dimensionless.
- **Purpose and significance:** Relates geometry and flow to the convection and friction correlations. Water velocity increases as density falls, even when mass flux remains constant.

### Prandtl number (E27)

\[
Pr=\frac{c_p\mu}{k}
\]

- **Location:** SS water `H` uses TM `R`; SS salt `M` and BE salt `H` use TM `AB`; BE water `M` uses TM `X`.
- **Variables:** \(c_p\) must be J/(kg·K), requiring a factor 1000 for the water table's kJ units.
- **Purpose and significance:** Characterizes momentum diffusion relative to thermal diffusion in the selected correlation. The choice of point versus secant \(c_p\) matters near the pseudo-critical region.

### Nusselt number to heat-transfer coefficient (E28)

\[
h=\frac{Nu\,k}{D_i}
\]

- **Location:** SS water `J`, salt `O`; BE salt `K`; incorporated directly in BE Jackson formulas `S` and `AK`.
- **Purpose and significance:** Converts the dimensionless correlation result into W/(m²·K), which can be used in convection resistances. A Nusselt correlation does not itself calculate exchanger length.

## Sponsor-physics model

### Sponsor Nusselt correlation (E29)

\[
Nu=C_{\mathrm{Nu}}Re^{a_{\mathrm{Nu}}}Pr^{b_{\mathrm{Nu}}}
=0.0266Re^{0.805}Pr^{1/3}
\]

- **Location:** SS water `I`, salt `N`; coefficients are `Inputs!C64:C66`.
- **Purpose and significance:** Reproduces the sponsor's selected relation for both streams. It is not the standard Dittus–Boelter equation, and the workbook does not identify a traceable original publication for these particular coefficients.

`Model_Spreadsheet` reproduces the sponsor's heat-transfer assumptions using the new workbook's fine march and common energy balance. It is not a literal cell-for-cell recreation of the uploaded coarse spreadsheet.

### Area-normalized resistances and local overall coefficient (E30)

\[
R''_w=\frac1{h_w},\quad R''_s=\frac1{h_s},\quad
R''_m=\frac{2t}{k_{m,\mathrm{fixed}}},\quad
R''_{\mathrm{tot}}=R''_w+R''_s+R''_m,\quad U=\frac1{R''_{\mathrm{tot}}}
\]

- **Location:** SS `P:T`; the resistances are stored in m²·K/kW, so Excel multiplies SI resistance by 1000 and uses `U=1000/S`.
- **Variables:** \(k_{m,\mathrm{fixed}}\) is `Inputs!C67`; two equal-thickness metal walls are in series.
- **Purpose and significance:** Treats both convection films and both walls on the assumed contact-area basis. There is no contact resistance or circumferential fin correction in this model.

### Segment length and cumulative height (E31)

\[
\Delta L_i=\frac{\Delta Q_{t,i}R''_{\mathrm{tot},i}}
{w\Delta T_{\mathrm{lm},i}},\qquad
z_i=\sum_{j=1}^{i}\Delta L_j
\]

- **Location:** SS `U:V`; first height equals the first segment length, subsequent heights accumulate it.
- **Purpose and significance:** Converts the heat-transfer requirement into physical tube length. With SS's stored resistance units, Excel includes a division by 1000.

### Contact-area heat flux and both wall temperatures (E32)

\[
q''_c=\frac{\Delta T_{\mathrm{lm}}}{R''_{\mathrm{tot}}},
\qquad T_{w,\mathrm{steam}}=T_b+\frac{q''_c}{h_w},\qquad
T_{w,\mathrm{salt}}=T_s-\frac{q''_c}{h_s}
\]

- **Location:** SS `W:Y`; `W` stores kW/m² and the wall formulas multiply it by 1000.
- **Purpose and significance:** Calculates the temperature drops across the fluid films. These are model wall temperatures on the contact-strip approximation, not a resolved circumferential metal-temperature field.

## Best-estimate salt convection

### Petukhov-type factor used inside Gnielinski (E33)

\[
f_P=(0.79\ln Re_s-1.64)^{-2}
\]

- **Location:** BE `I`.
- **Purpose and significance:** Supplies the friction-factor term inside the salt heat-transfer correlation. The hydraulic pressure-drop calculation elsewhere uses a different, sponsor-derived factor; do not substitute this cell without recognizing that distinction.

### Gnielinski salt correlation (E34)

\[
Nu_s=
\frac{(f_P/8)(Re_s-1000)Pr_s}
{1+12.7\sqrt{f_P/8}(Pr_s^{2/3}-1)},\qquad
h_s=\frac{Nu_sk_s}{D_i}
\]

- **Location:** BE `J:K`; inputs are BE `G:I` and TM `AD`.
- **Purpose and significance:** Provides a separate turbulent internal-flow estimate for salt convection. It assumes the modeled round passage and does not validate heat transfer in a deformed contact tube or account for local salt maldistribution.

## Best-estimate water convection and wall-temperature passes

Jackson is an empirical forced-convection correlation with wall-to-bulk property corrections, not an equation of state or a full CFD model. Its role and its limitations for buoyancy-affected/deteriorated supercritical heat transfer are discussed in the [ICTP supercritical-fluid heat-transfer notes](https://indico.ictp.it/event/a10196/session/19/contribution/14/material/0/0.pdf).

### First-pass wall-temperature assumption (E35)

\[
T_{w,1,1}=T_{b,1}+\Delta T_{\mathrm{guess}},
\qquad
T_{w,1,i}=T_{w,\mathrm{final},i-1}+(T_{b,i}-T_{b,i-1})\quad(i>1)
\]

- **Location:** BE `N5` and `N6:N544`; guess offset is `Inputs!C77`.
- **Purpose and significance:** Seeds the wall-temperature-dependent correlation without circular Excel references. The first-row 96 K offset is a numerical starting value, not a material property.

### Wall-fluid density, enthalpy, and secant heat capacity (E36)

\[
\rho_{w,p}=\mathcal I_\rho(T_{w,p}),\qquad H_{w,p}=\mathcal I_H(T_{w,p}),
\qquad
\bar c_{p,p}=\frac{H_{w,p}-H_b}{T_{w,p}-T_b}
\]

- **Location:** BE pass 1 `O:Q`; pass 2 `AG:AI`.
- **Variables:** \(p=1,2\) denotes the pass. The workbook multiplies its kJ/kg enthalpy difference by 1000.
- **Purpose and significance:** Samples fluid properties at the wall temperature and calculates the enthalpy-based average \(c_p\) over the wall-to-bulk temperature interval. This is a temperature-interval average, not a measured spatial average across the boundary layer.

At fixed pressure, \(\bar c_p=(T_w-T_b)^{-1}\int_{T_b}^{T_w}c_p(T)\,dT\). The current Excel expression has no equal-temperature limit branch, so \(T_w=T_b\) would require special handling.

### Jackson exponent (E37)

\[
n=
\begin{cases}
0.4,&T_b<T_w\le T_{\mathrm{pc}}\ \text{or}\ T_b\ge1.2T_{\mathrm{pc}},\\
0.4+0.2(T_w/T_{\mathrm{pc}}-1),&T_b\le T_{\mathrm{pc}}<T_w,\\
0.4+0.2(T_w/T_{\mathrm{pc}}-1)[1-5(T_b/T_{\mathrm{pc}}-1)],
&\text{otherwise}.
\end{cases}
\]

- **Location:** BE pass 1 `R`; pass 2 `AJ`; \(T_{\mathrm{pc}}\) is `Inputs!C76`.
- **Purpose and significance:** Adjusts the heat-capacity correction according to the temperature regime. “Otherwise” reproduces the workbook logic; its intended application is heated water with \(T_w>T_b\), not arbitrary cooling conditions.

### Jackson Nusselt number and water-side coefficient (E38)

\[
Nu_J=J_CRe_b^{J_{Re}}Pr_b^{J_{Pr}}
\left(\frac{\rho_w}{\rho_b}\right)^{J_\rho}
\left(\frac{\bar c_p}{c_{p,b}}\right)^n,\qquad
h_J=\frac{Nu_Jk_b}{D_i}
\]

The default constants are \(J_C=0.0183\), \(J_{Re}=0.82\), \(J_{Pr}=0.5\), and \(J_\rho=0.3\). They are input cells `C72:C75`, not automatically refitted coefficients.

- **Location:** BE pass 1 `S`; pass 2 `AK`, before the deterioration multiplier.
- **Variables:** Bulk \(Re,Pr\) are BE `L:M`; bulk properties are TM `U:X`; wall-property quantities are E36.
- **Purpose and significance:** Corrects the coefficient for large density and heat-capacity differences between the bulk and wall-temperature fluid. The correction factors can increase or decrease the base expression; Jackson does not simply replace bulk \(c_p\) with \(\bar c_p\).

### Optional deterioration sensitivity multiplier (E39)

\[
M_i=
\begin{cases}
M_{\mathrm{HTD}},&T_b<T_{\mathrm{pc}}<T_{w,2},\\
1,&\text{otherwise},
\end{cases}
\qquad h_{w,2}=M_i h_{J,2}
\]

- **Location:** BE `AK`; multiplier is `Inputs!C71`.
- **Purpose and significance:** Allows a user-selected reduction in the predicted coefficient as a sensitivity study. It is not a predictive deterioration correlation; the base value 1 applies no penalty.

Only pass 2 applies the multiplier in Excel. The final zone flag uses the final wall temperature (E55), whereas this branch uses the pass-2 assumed temperature, so the two classifications need not match exactly for all edited inputs.

### Temperature-dependent metal conductivity (E40)

\[
T_{m,p}^{*}=\frac{T_{w,p}+T_s}{2},\qquad k_{m,p}=\mathcal I_{k_m}(T_{m,p}^{*})
\]

- **Location:** BE pass 1 `T`; pass 2 `AL`; table is `Inputs!B94:C101`, with grid definitions `C91:C92`.
- **Variables:** \(T_m^*\) is a representative metal temperature, not a solved average through both walls.
- **Purpose and significance:** Lets steel conductivity vary with temperature and changes both wall and fin resistances. The choice of representative temperature is a model approximation.

## Fin efficiency, contact resistance, and the full resistance network

### Fin parameter, half-arc length, and efficiency (E41)

\[
m_f=\sqrt{\frac{h}{k_mt}},\qquad
\ell_f=\frac{r_m\theta}{2},\qquad
\eta_f=\frac{\tanh(m_f\ell_f)}{m_f\ell_f},\qquad
\theta=\theta_{\deg}\frac{\pi}{180}
\]

- **Location:** BE water pass 1 `U:V`, pass 2 `AM:AN`; salt pass 1 `X`, pass 2 `AP`.
- **Variables:** Water fins use \(h=h_w\), salt fins use \(h=h_s\). Arc inputs are `Inputs!C78:C80`, nominally 60°, 120°, and 60°.
- **Purpose and significance:** Represents circumferential conduction from direct contact regions into the otherwise unbacked wall. Dividing the arc length by two models heat conduction from both bounding contacts to a symmetry point.

The “fins” are portions of the tube wall, not added external fin hardware. The formula is a one-dimensional thin-wall fin approximation; a two-dimensional conduction solution is needed to resolve actual contact-strip temperature peaks.

### Effective water-side perimeter (E42)

\[
P_{w,\mathrm{eff}}=r_i\left[\pi+\eta_1\theta_1+\eta_2\theta_2\right]
\]

- **Location:** BE pass 1 `W`; pass 2 `AO`.
- **Variables:** \(\pi r_i\) is the directly backed half of the bore perimeter; the two remaining arcs are weighted by their fin efficiencies.
- **Purpose and significance:** Adds the useful heat-transfer contribution of the remaining tube wall without treating it as perfectly effective. It converts water \(h\) into a per-length conductance \(h_wP_{w,\mathrm{eff}}\).

### Effective salt perimeter allocated to one steam tube (E43)

\[
P_{s,\mathrm{eff}}=
\frac{N_s}{N_w}\,2\pi r_i
\left[f_{\mathrm{backed}}+(1-f_{\mathrm{backed}})\eta_s\right]
\]

- **Location:** BE pass 1 `Y`; pass 2 `AQ`.
- **Variables:** The count ratio allocates salt-tube perimeter to the per-steam-tube resistance network.
- **Purpose and significance:** Keeps area accounting consistent when there are fewer salt tubes than steam tubes. Omitting the count ratio would overstate salt-side conductance per steam tube.

### Water and salt film resistance factors (E44)

\[
R'_w=\frac1{h_wP_{w,\mathrm{eff}}},\qquad
R'_s=\frac1{h_sP_{s,\mathrm{eff}}}
\]

- **Location:** BE pass 1 `Z:AA`; pass 2 `AR:AS`.
- **Variables:** Outputs are K·m/W, unlike SS's area-normalized m²·K/kW resistances.
- **Purpose and significance:** Quantifies the temperature drop needed per W/m transferred through each fluid film. These values cannot be directly added to SS resistances without unit and area-basis conversion.

### Two metal walls in series (E45)

\[
R'_m=\frac{2t}{k_mw}
\]

- **Location:** BE pass 1 `AB`; pass 2 `AT`.
- **Purpose and significance:** Represents conduction across two equal-thickness walls over the assumed contact width. It is a planar-wall approximation, not the exact cylindrical logarithmic resistance or a resolved deformed-contact conduction model.

### Tube-to-tube contact resistance (E46)

\[
R'_c=
\begin{cases}
0,&\text{Excel input }h_c=0\text{ (perfect-contact switch)},\\
1/(h_cw),&h_c>0.
\end{cases}
\]

- **Location:** BE pass 1 `AC`; pass 2 `AU`; conductance input is `Inputs!C70`.
- **Variables:** \(h_c\) is W/(m²·K); \(w\) is assumed interface area per metre.
- **Purpose and significance:** Adds the resistance of imperfect solid-to-solid contact. The zero-input convention is a software switch, not physical zero conductance; physical \(h_c\to0\) would make resistance very large.

The 3,700 W/(m²·K) input is an assumed conductance, not an intrinsic property of 316 stainless steel or a measurement of this bundle. Contact depends on pressure, surfaces, and the gap medium, as described in the [thermal-contact-resistance reference](https://help.solidworks.com/2025/english/solidworks/cworks/c_Thermal_Contact_Resistance.htm).

### Total resistance and updated wall temperature in each pass (E47)

\[
R'_{\mathrm{tot},p}=R'_{w,p}+R'_{s,p}+R'_{m,p}+R'_{c,p},
\qquad
T_{w,\mathrm{updated},p}
=T_b+\frac{\Delta T_{\mathrm{lm}}}{R'_{\mathrm{tot},p}}R'_{w,p}
\]

- **Location:** BE pass 1 `AD:AE`; pass 2 `AV:AW`.
- **Purpose and significance:** Solves the series thermal-resistance network for the wall temperature implied by each assumed property state. It couples Jackson to the geometry, salt convection, and contact assumptions.

### Transfer from pass 1 to pass 2 (E48)

\[
T_{w,2}=T_{w,\mathrm{updated},1}
\]

- **Location:** BE `AF=AE` in each row.
- **Purpose and significance:** Re-evaluates the entire network using a better wall-temperature estimate. Excel makes two explicit passes only; it does not iterate until a specified residual is reached, so the final \(T_w\) can differ from the temperature used to evaluate the final \(h_w\).

The companion Python calculation iterates the wall temperature to a tolerance. Agreement with it is a numerical check, not experimental validation of Jackson or the contact model.

## Final local outputs and hydraulic equations

### Heat transfer per metre and required segment length (E49)

\[
q'_i=\frac{\Delta T_{\mathrm{lm},i}}{R'_{\mathrm{tot},i}},\qquad
\Delta L_i=\frac{\Delta Q_{t,i}}{q'_i},\qquad
z_i=\sum_{j=1}^{i}\Delta L_j
\]

- **Location:** BE `AX:AZ`; `AZ5=AY5`, subsequent heights add to the preceding height.
- **Purpose and significance:** Converts the resistance solution into length. \(q'\) is not a user-imposed constant: it changes along the tube as temperatures and resistances change.

### Local overall \(U\), contact-area basis (E50)

\[
U_{c,i}=\frac1{R'_{\mathrm{tot},i}w}
\]

- **Location:** BE `BA`; corresponding SS result is E30 in `T`.
- **Purpose and significance:** Expresses the per-length conductance as an area-based coefficient. The value of \(U\) changes if a different reference area is chosen, even though the heat-transfer prediction is unchanged.

### Final inner-wall temperatures (E51)

\[
T_{w,\mathrm{steam}}=T_b+q'R'_w,\qquad
T_{w,\mathrm{salt}}=T_s-q'R'_s
\]

- **Location:** BE `BB:BC`; `BB` is algebraically equivalent to the pass-2 update `AW`.
- **Purpose and significance:** Determines the plotted steam-side wall temperature and the salt-side freezing-margin temperature. These are effective local temperatures in the simplified network, not a detailed circumferential maximum/minimum.

A wall-temperature dip is possible if \(q'R'_w\) decreases faster than \(T_b\) rises. This mathematical behavior explains the dip near the pseudo-critical region but does not establish its experimental magnitude.

### Bore-average heat flux and heat-flux-to-mass-flux ratio (E52)

\[
q''_{\mathrm{bore}}=\frac{q'}{\pi D_i}
=\frac{\Delta Q_{t,i}}{\Delta L_i\pi D_i},\qquad
\Psi=\frac{q''_{\mathrm{bore}}}{G_w}
\]

- **Location:** SS `Z:AA`; BE `BD:BE`.
- **Units:** Heat flux is stored in kW/m², making \(\Psi\) kJ/kg.
- **Purpose and significance:** Provides common-area quantities for deterioration screening. The bore-average flux is not the higher local flux at a contact strip, and \(\Psi\) is not dimensionless.

### Implemented turbulent Darcy factor (E53)

\[
f_D=\frac8{6.0516}
\left[\ln\left(\frac{\epsilon_r}{D_i}+
\left(\frac7{Re}\right)^{0.9}\right)\right]^{-2}
\]

- **Location:** SS water `AB`, salt `AE`; BE water `BJ`, salt `BM`.
- **Variables:** \(\epsilon_r=\texttt{rough}\), `Inputs!C84`; \(Re\) is the appropriate stream's value.
- **Purpose and significance:** Supplies the hydraulic factor used by the existing workbook. This reference preserves the implemented sponsor-derived approximation rather than labeling it as a verified full Churchill correlation; the workbook has no laminar/transition branch.

### Segment friction and water hydrostatic pressure change (E54)

\[
\Delta P_{f,i}=f_D\frac{\Delta L_i}{D_i}\frac{\rho_i v_i^2}{2},
\qquad
\Delta P_{g,w,i}=\rho_{b,i}g\Delta L_i
\]

- **Location:** SS water friction `AC`, gravity `AD`, salt friction `AF`; BE water friction `BK`, gravity `BL`, salt friction `BN`.
- **Variables:** \(g=\texttt{g_acc}\), `Inputs!C85`; results are Pa.
- **Purpose and significance:** Integrates friction along the computed length and adds elevation head for water upflow. Salt gravity is not added to the reported salt loss total; gravity is a driving/recovery term rather than an irreversible friction loss.

## Deterioration and nonuniform-property screening

These diagnostics are flags, not acceptance criteria or predictions of how much heat transfer deteriorates. The workbook labels use thresholds, but the governing phenomena depend on flow direction, geometry, pressure, and heating conditions; the [ICTP notes](https://indico.ictp.it/event/a10196/session/19/contribution/14/material/0/0.pdf) distinguish normal, improved, and deteriorated heat transfer and discuss the limits of forced-convection correlations.

### Wall/bulk straddling flag (E55)

\[
I_i=\begin{cases}1,&T_b<T_{\mathrm{pc}}<T_{w,\mathrm{steam}},\\0,&\text{otherwise}.\end{cases}
\]

- **Location:** BE `BF`.
- **Purpose and significance:** Identifies segments in which the bulk and wall-temperature fluid lie on opposite sides of the pseudo-critical temperature. This is a screening zone, not proof that every flagged segment is deteriorated.

### Buoyancy parameter (E56)

\[
\nu_b=\frac{\mu_b}{\rho_b},\qquad
Gr_q=\frac{g\beta_bD_i^4q''_{\mathrm{bore}}}{k_b\nu_b^2},
\qquad
Bo^*=\frac{Gr_q}{Re_b^{3.425}Pr_b^{0.8}}
\]

- **Location:** BE `BG`; \(\nu_b\) and \(Gr_q\) are inline subexpressions, not separate columns.
- **Variables:** Uses point bulk properties and bore-average heat flux in W/m², so BE `BD` is multiplied by 1000.
- **Purpose and significance:** Screens the potential influence of buoyancy relative to forced flow. The worksheet annotation \(Bo^*>8\times10^{-6}\) should be read as a screening warning, not a sharp universal boundary.

### Thermal-acceleration parameter (E57)

\[
K_v=\frac{4q''_{\mathrm{bore}}\beta_b}{G_wc_{p,b}Re_b}
\]

- **Location:** BE `BH`; \(c_{p,b}\) comes from TM `X` and is converted to J/(kg·K).
- **Purpose and significance:** Screens acceleration caused by density change during heating. The annotation \(K_v>3\times10^{-6}\) is a screening guide; the workbook does not solve the resulting turbulence changes.

## Whole-exchanger results

Unless stated otherwise, each equation below appears in both `Results` columns C and D, with C referring to SS and D to BE. Identical thermodynamic quantities appear twice for comparison; repeating them does not mean the models have different energy balances.

### Direct result links (E58)

\[
(Q,\dot m_w,\dot m_s,G_w)_{\mathrm{Results}}
=(Q,\dot m_w,\dot m_s,G_w)_{\mathrm{Inputs}}
\]

- **Location:** `Results!C6:D8`, `C43:D43`.
- **Purpose and significance:** Shows common inputs next to model-dependent outputs. These cells add no new physical equation.

### Integrated conductance and effective driving difference (E59)

\[
(UA)_{\mathrm{req}}=\sum_i(UA)_i
=\sum_i\frac{\Delta Q_i}{\Delta T_{\mathrm{lm},i}},\qquad
\Delta T_{\mathrm{eff}}=\frac{Q}{(UA)_{\mathrm{req}}}
\]

- **Location:** `Results!C9:D9`, `C11:D11`.
- **Purpose and significance:** Summarizes the segmented energy/temperature calculation. The “true mean” label in the workbook means this model's effective mean, not an arithmetic average of salt–water temperature differences or an exact solution independent of discretization.

### Single-LMTD comparison, implied conductance, and error (E60)

\[
\Delta T_{\mathrm{lm,whole}}
=\frac{\Delta T_c-\Delta T_h}{\ln(\Delta T_c/\Delta T_h)},\qquad
(UA)_{\mathrm{single}}=\frac{Q}{\Delta T_{\mathrm{lm,whole}}},
\qquad
E_{\mathrm{LMTD}}=\frac{(UA)_{\mathrm{single}}}{(UA)_{\mathrm{req}}}-1
\]

- **Location:** `Results!C10:D10`, `C12:D13`.
- **Purpose and significance:** Quantifies the error of using the two terminal approaches as if the constant-capacity textbook construction applied globally. It does not imply that LMTD is invalid locally; E20 uses it in small segments.

The whole-exchanger Excel expression lacks the equal-end-difference safeguard in E20. Equal terminal approaches would require the limiting value rather than direct evaluation of 0/0.

### Average capacity ratio (E61)

\[
C_r=\frac{C_{w,\mathrm{avg}}}{C_{s,\mathrm{avg}}}
\]

- **Location:** `Results!C14:D14`.
- **Purpose and significance:** Supplies the nominal \(C_{\min}/C_{\max}\) for the comparison formulas. Excel does not apply `MIN` and `MAX`; this expression assumes water has the smaller average capacity rate and must be revisited if the operating case changes.

### Enthalpy-based effectiveness (E62)

\[
Q_{\max,w}=\dot m_w
\left[H(P,T_{s,\mathrm{in}})-H(P,T_{b,\mathrm{in}})\right],
\qquad
\varepsilon_H=\frac{Q}{Q_{\max,w}}
\]

- **Location:** `Results!C15:D15`; the hotter-limit water enthalpy is interpolated directly inside the formula.
- **Purpose and significance:** Measures actual duty relative to heating the water to the hot inlet temperature. The formula called “exact” in the workbook is exact only relative to this chosen enthalpy limit, property interpolation, and the stated assumptions.

The workbook does not independently compute the salt-side limiting duty or check for every possible internal pinch in a variable-property limiting exchanger. It should not be described as an unrestricted exact effectiveness formula for arbitrary edited conditions.

### Constant-capacity effectiveness and nominal NTU (E63)

\[
\varepsilon_{\mathrm{avg}}=
\frac{Q}{C_{w,\mathrm{avg}}(T_{s,\mathrm{in}}-T_{b,\mathrm{in}})},\qquad
NTU_{\mathrm{avg}}=\frac{(UA)_{\mathrm{req}}}{C_{w,\mathrm{avg}}}
\]

- **Location:** `Results!C16:D17`.
- **Purpose and significance:** Provides textbook-style reporting metrics using average capacity rates. They are not the equations used to determine length.

### Counterflow effectiveness relation and its inverse (E64)

\[
\varepsilon_{\mathrm{CF}}=
\frac{1-e^{-NTU(1-C_r)}}{1-C_re^{-NTU(1-C_r)}},
\qquad
NTU_{\mathrm{inverse}}=
\frac{\ln[(\varepsilon_{\mathrm{avg}}-1)/
(\varepsilon_{\mathrm{avg}}C_r-1)]}{C_r-1}
\]

- **Location:** `Results!C18:D19`.
- **Purpose and significance:** Demonstrates the inconsistency introduced by forcing a constant-capacity relation onto this variable-property exchanger. The mismatch is an applicability issue, not a reason to adjust the energy balance to make the numbers agree.

The displayed expressions assume \(C_r\ne1\). At \(C_r=1\), the appropriate limits are \(\varepsilon=NTU/(1+NTU)\) and \(NTU=\varepsilon/(1-\varepsilon)\); Excel does not implement those branches here.

### Count of capacity-rate reversals (E65)

\[
n_{\mathrm{water\,larger}}=\sum_i
\mathbf1(C_{w,i}>C_{s,\mathrm{avg}})
\]

- **Location:** `Results!C20:D20`, implemented using `COUNTIF(TM!T5:T544,"Water")`.
- **Purpose and significance:** Counts segments in which water is the higher-capacity stream. This is a diagnostic count, not a length fraction; the segments have unequal lengths.

### Heated length and heat-transfer areas (E66)

\[
L=\sum_i\Delta L_i,\qquad
A_c=N_wwL,\qquad A_b=N_w\pi D_iL
\]

- **Location:** `Results!C22:D22`, `C25:D26`.
- **Purpose and significance:** Reports the common heated length for the modeled parallel tubes and two alternative area bases. Neither area is the tube flow area \(A_f\).

### Overall area-based coefficients and installed heated tube length (E67)

\[
U_c=\frac{(UA)_{\mathrm{req}}}{A_c},\qquad
U_b=\frac{(UA)_{\mathrm{req}}}{A_b},\qquad
L_{\mathrm{installed}}=\frac{(N_w+N_s)L}{1000}\quad[\mathrm{km}]
\]

- **Location:** `Results!C23:D24`, `C27:D27`.
- **Purpose and significance:** Summarizes conductance per chosen area and total heated steam-plus-salt tube length. Installed length excludes air tubes, bends, and header connections; overall \(U\) is an aggregate, not a simple arithmetic mean of local \(U_i\).

### Mean salt velocity and total friction losses (E68)

\[
\bar v_s=\frac1{N_{\mathrm{seg}}}\sum_i v_{s,i},\qquad
\Delta P_{f,s}=\sum_i\Delta P_{f,s,i},\qquad
\Delta P_{f,w}=\sum_i\Delta P_{f,w,i},\qquad
\Delta P_{g,w}=\sum_i\Delta P_{g,w,i}
\]

- **Location:** `Results!C29:D30`, `C34:D35`.
- **Units:** Segment pressure outputs are divided by 1000 to give kPa.
- **Purpose and significance:** Aggregates local hydraulic results. The salt velocity is an unweighted average over equal water-temperature intervals, not a length-weighted average.

### Salt minor losses and reported total (E69)

\[
\rho_{s,\mathrm{ref}}=a_\rho+b_\rho\frac{T_{s,\mathrm{in}}+T_{s,\mathrm{out}}}{2},
\quad
\Delta P_{K,s}=K_s\frac{\rho_{s,\mathrm{ref}}\bar v_s^2}{2},
\quad
\Delta P_{s,\mathrm{reported}}=\Delta P_{f,s}+\Delta P_{K,s}
\]

- **Location:** `Results!C31:D32`; \(K_s\) is `Inputs!C86`.
- **Purpose and significance:** Adds the assumed entrance/exit/bend losses to straight-tube friction. It is not a complete salt-loop pressure balance and does not include an emergency natural-circulation solution.

### Salt hydraulic power (E70)

\[
\dot W_{\mathrm{hyd},s}=
\Delta P_{s,\mathrm{reported}}\frac{\dot m_s}{\rho_{s,\mathrm{ref}}}
\]

- **Location:** `Results!C33:D33`.
- **Units:** kPa multiplied by m³/s gives kW.
- **Purpose and significance:** Estimates fluid hydraulic power. It is not pump electrical power; the workbook applies no pump/motor efficiency.

### Water acceleration pressure change (E71)

\[
\Delta P_{\mathrm{acc},w}
=G_w^2\left(\frac1{\rho_{\mathrm{out}}}-\frac1{\rho_{\mathrm{in}}}\right)
\]

- **Location:** `Results!C36:D36`, reporting kPa.
- **Variables:** End densities should be the fully interpolated values at the water inlet and outlet temperatures.
- **Purpose and significance:** Accounts for acceleration as the water density falls. The current Excel expansion has a parenthesis defect for off-grid endpoint temperatures; see the implementation findings below and the exact formula register.

### Water minor losses and total pressure requirement (E72)

\[
\Delta P_{K,w}=
\frac{K_{\mathrm{in}}G_w^2}{2\rho_{\mathrm{in}}}
+\frac{K_{\mathrm{out}}G_w^2}{2\rho_{\mathrm{out}}},
\qquad
\Delta P_{w,\mathrm{total}}=
\Delta P_{f,w}+\Delta P_{g,w}+\Delta P_{\mathrm{acc},w}+\Delta P_{K,w}
\]

- **Location:** `Results!C37:D38`; minor coefficients are `Inputs!C87:C88`.
- **Purpose and significance:** Adds terminal losses to friction, elevation, and acceleration. The minor-loss Excel expansion has the same off-grid interpolation issue as E71; headers, flow-distribution orifices, and external steam piping are not explicitly modeled.

### Temperature extrema and salt freezing margin (E73)

\[
T_{w,\max}=\max_i T_{w,\mathrm{steam},i},\quad
T_{s,\mathrm{wall},\min}=\min_i T_{w,\mathrm{salt},i},\quad
M_{\mathrm{freeze}}=T_{s,\mathrm{wall},\min}-T_{\mathrm{freeze}}
\]

- **Location:** `Results!C40:D42`; freezing input is `Inputs!C61`.
- **Purpose and significance:** Screens steady-state metal temperature and salt-wall freezing margin. Comparing the steam-side wall curve against a salt freezing line does not establish salt safety; the salt-side wall result is the relevant quantity.

### Conditional extrema in the flagged region (E74)

\[
z_{\mathrm{zone,top}}=\max_{I_i=1}z_i,\quad
\Psi_{\max,\mathrm{zone}}=\max_{I_i=1}\Psi_i,\quad
\Psi_{\min,\mathrm{zone}}=\min_{I_i=1}\Psi_i,
\]
\[
q''_{\max,\mathrm{zone}}=\max_{I_i=1}q''_{\mathrm{bore},i},\qquad
Bo^*_{\max,\mathrm{zone}}=\max_{I_i=1}Bo_i^*,\qquad
K_{v,\max}=\max_iK_{v,i}
\]

- **Location:** `Results!D44:D47`, `D49:D50`; implemented with `MAXIFS`, `MINIFS`, and `MAX`.
- **Purpose and significance:** Summarizes screening quantities where the wall/bulk straddling condition holds. “Zone top” is the highest flagged segment end, not necessarily the length of one continuous deteriorated region.

For no matching rows, conditional aggregate functions may return zero rather than a meaningful physical minimum. The `_xlfn.` prefix present in the stored formulas also means spreadsheet-software compatibility should be checked when opening the file.

### Yamagata-style heat-flux screening expression (E75)

\[
q''_{\mathrm{screen}}=0.2\,G_w^{1.2}
\]

- **Location:** `Results!D48`.
- **Variables and units:** \(G_w\) must be in kg/(m²·s); the resulting empirical estimate is kW/m².
- **Purpose and significance:** Provides a comparison level for the modeled heat flux. It is a unit-dependent empirical screening relation, not a universal safe operating boundary or a replacement for matching validation data.

### Thin-wall hoop-stress screen (E76)

\[
\sigma_{\theta,\mathrm{screen}}=\frac{P_{\mathrm{steam}}D_i}{2t}
\]

- **Location:** `Results!C51:D51`.
- **Units:** \(P_{\mathrm{steam}}\) is entered in MPa, so the output is MPa when \(D_i,t\) use the same length units.
- **Purpose and significance:** Flags whether the starting wall thickness warrants mechanical review. This is not an ASME minimum-wall calculation and includes neither creep life, corrosion allowance, fabrication tolerance, nor detailed contact/bending stresses.

## Chart equations and source mapping

### Temperature-profile chart (E77)

\[
(x,y)_{\mathrm{salt}}=(T_{s,i},z_i),\quad
(x,y)_{\mathrm{water}}=(T_{b,i},z_i),\quad
(x,y)_{\mathrm{wall}}=(T_{w,i},z_i)
\]

- **Location:** `Charts!R6:U545`; `R` links to BE `AZ`, `S` to TM `K`, `T` to TM `C`, and `U` to BE `BB`.
- **Purpose and significance:** Plots temperature horizontally and height vertically. Chart row \(r\) links to march row \(r-1\).

The bulk curves use segment-end temperatures, whereas the wall temperature represents the segment's mean-temperature calculation plotted at its end height. This small coordinate approximation is important when interpreting the precise location of a narrow wall-temperature dip.

### Reference temperature lines (E78)

\[
(x,y)=(T_{\mathrm{freeze}},0),(T_{\mathrm{freeze}},L);
\qquad
(x,y)=(T_{\mathrm{pc}},0),(T_{\mathrm{pc}},L)
\]

- **Location:** `Charts!C6:D9`; `D6` and `D8` are hard-coded zero, while `D7` and `D9` link to `Results!D22`.
- **Purpose and significance:** Adds visual reference lines, not additional calculated temperature profiles.

### Temperature-difference comparison chart (E79)

\[
(x,y)_{\mathrm{actual}}=(F_i,\Delta T_{i,b}),\qquad
(x,y)_{\mathrm{comparison}}=(F_i,\Delta T_{\mathrm{linear},i})
\]

- **Location:** `Charts!V6:X545`, linked to TM `I`, `N`, and `Q`.
- **Purpose and significance:** Displays why the actual variable-property temperature-difference path differs from the constant-capacity comparison. “Actual” in the chart means calculated using the property data, not experimentally measured.

### Water-side coefficient comparison chart (E80)

\[
(x,y)_{\mathrm{SS}}=(T_{b,m},h_{w,\mathrm{SS}}/1000),\qquad
(x,y)_{\mathrm{BE}}=(T_{b,m},h_{w,\mathrm{BE}}/1000)
\]

- **Location:** `Charts!Y6:AA545`; `Y` links to TM `D`, `Z` to SS `J`, and `AA` to BE `AK`.
- **Purpose and significance:** Compares convection predictions in kW/(m²·K). These curves are water-film coefficients, not whole-exchanger \(U\).

## Static studies and their generating equations

`Studies` has no live Excel formulas; changing `Inputs` does not update its results. The companion script reruns the same governing equations with different inputs, except for the explicitly described legacy-replica calculation.

### Model decomposition and parameter substitutions (E81)

\[
L=L(\text{model},h_c,M_{\mathrm{HTD}},N_w,D_i,T_{\mathrm{ends}})
\]

- **Locations:** `Studies!B6:C10` compares model variants; `B15:F18` changes \(h_c\); `B23:D25` changes the deterioration multiplier.
- **Purpose and significance:** Isolates sensitivity to selected assumptions. The “Jackson-only” case retains the sponsor model's resistance-area assumptions and replaces its water-side coefficient; the full best-estimate case changes additional terms, so length changes must not be added as if independent.

The perfect-contact and finite-contact cases use E46's software convention. The Python model uses a converged wall-temperature loop rather than Excel's two passes.

### Tube count required for a target length (E82)

\[
F(N_w)=L(N_w)-L_{\mathrm{target}}=0,\qquad
N_{\mathrm{mid}}=\frac{N_{\mathrm{lo}}+N_{\mathrm{hi}}}{2}
\]

- **Location:** Static results in `Studies!B30:G33`; implemented in the script's `n_for_length`.
- **Variables:** \(L_{\mathrm{target}}=11.92\) m; the search brackets counts from 4,000 to 20,000, makes 11 bisection steps, and reruns a 270-segment model with integer tube counts.
- **Purpose and significance:** Finds a numerical tube count satisfying the thermal-length target while maintaining the salt-count rule. It does not optimize pressure drop, cost, flow stability, or mechanical design.

### Geometry sweep and alternate-temperature case (E83)

\[
(L,v_s,G,\Delta P_s,\dot W_{\mathrm{hyd},s},\Delta P_w)
=\mathcal M(D_i,N_w;\text{other fixed inputs})
\]

- **Location:** `Studies!B38:I45` uses 16 and 20 mm inside diameters with 5,000, 6,536, 8,000, and 10,000 steam tubes; it uses 270 segments.
- **Alternate case:** `Studies!C50:C53` reruns the sponsor-physics model with salt inlet 875 K and water outlet 860 K, using 600 segments; salt outlet and water inlet remain 810 and 560 K.
- **Purpose and significance:** Exposes trade-offs by recalculating all linked quantities. The alternate-temperature case changes two terminal temperatures, so its length change must not be attributed to the steam outlet temperature alone.

### Legacy replica used for the first static study (E84)

The script's separate `spreadsheet_replica()` uses a nominal 5 K water-temperature sequence and endpoint-evaluated properties. With enthalpy in kJ/kg, its per-steam-tube duty is

\[
\Delta Q_{t,i}^{[\mathrm{kW}]}=\dot m_{w,t}(H_i-H_{i-1}),
\qquad
T_{s,i}=T_{s,i-1}
+\frac{1000\,\Delta Q_{t,i}^{[\mathrm{kW}]}\,(4/3)}
{\dot m_{s,t}c_{p,s}(T_{s,i-1})}.
\]

Its incremental length is

\[
\Delta L_i=
\frac{\Delta Q_{t,i}^{[\mathrm{kW}]}
\left(1000/h_w+1000/h_s+2000t/k_m\right)}
{w\Delta T_{\mathrm{lm},i}}.
\]

- **Location:** Stored result `Studies!C6`; formulas are in the companion script, not Excel.
- **Purpose and significance:** Provides a historical coarse-step reproduction check. It does not use the exact quadratic salt inversion of TM, and the live `Model_Spreadsheet` result should not be expected to match it exactly.

## Implementation findings and interpretation limits

The formula register below records the workbook as it currently exists. The following findings distinguish intended engineering relationships from the actual implementation; no corrections have been silently applied to the workbook.

### Off-grid density interpolation in pressure-drop formulas

The intended reciprocal of an interpolated density is

\[
\frac1{\rho(T)}=\frac1{\rho_j+\theta(\rho_{j+1}-\rho_j)}.
\]

In `Results!C36:D36`, the expanded formula instead places the interpolation correction outside the reciprocal; for the inlet term the sign is also inconsistent with subtracting the whole interpolated reciprocal. In `C37:D37`, the density correction likewise appears outside the reciprocal and its associated loss prefactor.

At the current 560 K and 830 K endpoints, both temperatures fall exactly on the 0.25 K grid, so the interpolation correction is zero and this defect does not change those base-case results. Off-grid endpoint edits can produce incorrect acceleration and minor losses; the intended E71–E72 expressions should use parentheses around the complete interpolated density.

### Other limits important when using the equations

- **Pressure dependence:** Water data and \(T_{\mathrm{pc}}\) are fixed at 24 MPa; a pressure edit does not regenerate them.
- **Temperature/table boundaries:** Lookups require the next table entry, even at a zero interpolation fraction. The upper water and metal-table endpoints need special handling.
- **No live structural sizing:** The workbook has only a thin-wall hoop screen, not code wall-thickness, corrosion-life, tubesheet, header, creep-fatigue, or differential-expansion calculations.
- **No automatic study refresh:** `Studies` values are static and may cease to represent the live `Inputs` after edits.
- **Finite-pass approximation:** Excel's two wall-temperature passes are not a general convergence guarantee. Sensitivity changes, particularly strong deterioration penalties, warrant checking against a converged solver.
- **Area and contact assumptions:** Contact width, fin geometry, and the contact conductance must correspond to the actual formed tube layout. Formula consistency does not validate those physical inputs.
- **Thermal limits:** The model is steady-state, uses a one-dimensional segmented energy path and simplified circumferential fins, and does not resolve startup, freezing transients, leaks, emergency air cooling, or parallel-channel flow stability.
- **Hydraulic limits:** Flow is uniformly split among tubes; the turbulent friction approximation, lumped minor coefficients, and incomplete header/loop representation require validation.
- **Screening versus proof:** Deterioration flags, wall-temperature dips, freezing margins, and hoop stress are calculated model outputs. None alone establishes component acceptability.

## Excel functions and bookkeeping operations

These operations explain every nonphysical formula mechanism in the register. They change how the physical equations are evaluated or reported, not the underlying energy balance.

| Excel operation | Meaning in this workbook | Significance |
|---|---|---|
| `INDEX`, `INT` | Locate neighboring property rows; construct interpolation fraction | Implements E14; `INT` is floor for the nonnegative in-range lookup index |
| `IF`, `AND`, `OR`, `ABS` | Choose regimes, perfect-contact switch, flags, equal-LMTD safeguard | Branch selection is part of the model and must be preserved |
| `ROUND(...,0)` | Convert salt count to an integer | Small count-ratio discrepancies are possible |
| `SUM` and previous-row addition | Accumulate heat, length, conductance, pressure loss | Sum rates over spatial segments, not over time |
| `AVERAGE` | Unweighted mean salt velocity | Not a spatially weighted mean |
| `MAX`, `MIN` | Extreme modeled values | Do not recover unmodeled local contact hot spots |
| `MAXIFS`, `MINIFS`, `COUNTIF` | Conditional extrema or segment count | Depend on zone flags and spreadsheet-software support |
| `LN`, `EXP`, `SQRT`, powers | Correlations, salt-energy inversion, logarithmic means | `LN` is natural logarithm; inputs must remain in each expression's domain |
| `TANH`, `RADIANS`, `PI` | Fin efficiency and circular geometry | Degree-based input angles are converted before use |
| Direct `=Sheet!Cell` or named-range links | Bring common inputs/results into a sheet or chart | Included in the audit even though they add no new equation |

The following generated appendices complete the cell-level coverage. Their formulas are transcribed from the workbook, not reconstructed from the narrative above.

<!-- GENERATED AUDIT APPENDICES -->

## Named-range dictionary

The names below are the literal identifiers used in Excel formulas. A cached value is a snapshot of the audited workbook, not a new input or a recommendation; array entries point to the actual table rather than repeating all stored property values.

| Excel name | Workbook location | Meaning / units | Cached value |
|---|---|---|---|
| `A_flow` | `Inputs!$C$44` | Flow area per tube (m²) | 0.0003141592654 |
| `cp_a` | `Inputs!$C$55` | Specific heat c_p = a + bT : a (J/kg·K) | 1437.88 |
| `cp_b` | `Inputs!$C$56` | Specific heat : b (J/kg·K²) | -0.5 |
| `C_salt` | `Inputs!$C$32` | Salt capacity rate C_salt (MW/K) | 6.25 |
| `C_w_avg` | `Inputs!$C$33` | Water average capacity rate C_water (MW/K) | 1.851851852 |
| `dh_salt` | `Inputs!$C$30` | Salt Δh = ∫c_p dT from outlet to inlet (J/kg) | 81030.4 |
| `dT_cold` | `Inputs!$C$21` | Cold-end ΔT (salt out − water in) (K) | 250 |
| `dT_hot` | `Inputs!$C$22` | Hot-end ΔT (salt in − steam out) (K) | 60 |
| `dT_step` | `Inputs!$C$24` | Water temperature step per segment (K) | 0.5 |
| `D_i` | `Inputs!$C$41` | Tube inner diameter (both tube sets) (m) | 0.02 |
| `D_o` | `Inputs!$C$43` | Tube outer diameter (m) | 0.024 |
| `eta_plant` | `Inputs!$C$10` | Plant efficiency (-) | 0.4 |
| `eta_R` | `Inputs!$C$13` | Reference Rankine-cycle efficiency (-) | 0.44 |
| `_gap1` | `Inputs!$C$78` | Steam-tube fin arc 1 (non-salt contact) (deg) | 60 |
| `_gap2` | `Inputs!$C$79` | Steam-tube fin arc 2 (non-salt contact) (deg) | 120 |
| `g_acc` | `Inputs!$C$85` | Gravity (m/s²) | 9.81 |
| `G_w` | `Inputs!$C$50` | Steam-side mass flux G (kg/m²·s) | 115.5302301 |
| `HTD_mult` | `Inputs!$C$71` | Multiplier on water h in deterioration zone (-) | 1 |
| `h_contact` | `Inputs!$C$70` | Tube-to-tube contact conductance h_c (W/m²·K) | 3700 |
| `h_w_in` | `Inputs!$C$27` | Water enthalpy at inlet (kJ/kg) | 1264.67695 |
| `h_w_out` | `Inputs!$C$28` | Steam enthalpy at outlet (kJ/kg) | 3372.394686 |
| `J_C` | `Inputs!$C$72` | Jackson: coefficient (-) | 0.0183 |
| `J_Pr` | `Inputs!$C$74` | Jackson: Pr exponent (-) | 0.5 |
| `J_Re` | `Inputs!$C$73` | Jackson: Re exponent (-) | 0.82 |
| `J_rho` | `Inputs!$C$75` | Jackson: density-ratio exponent (-) | 0.3 |
| `K316_dT` | `Inputs!$C$92` | Table step (K) | 100 |
| `K316_k` | `Inputs!$C$94:$C$101` | 316 conductivity values, W/(m·K) | Stored array |
| `K316_T0` | `Inputs!$C$91` | Table start T (K) | 300 |
| `k_a` | `Inputs!$C$59` | Conductivity k = a + bT : a (W/m·K) | 0.65318 |
| `k_b` | `Inputs!$C$60` | Conductivity : b (W/m·K²) | -0.00026 |
| `K_salt` | `Inputs!$C$86` | Salt minor-loss coefficient (total) (-) | 2.1 |
| `k_wall_ss` | `Inputs!$C$67` | Wall conductivity (fixed) (W/m·K) | 19 |
| `K_w_in` | `Inputs!$C$87` | Water minor loss at inlet (-) | 0.8 |
| `K_w_out` | `Inputs!$C$88` | Water minor loss at outlet (-) | 1.3 |
| `mu_a` | `Inputs!$C$57` | Viscosity μ = a·exp(b/T) : a (Pa·s) | 0.00070645 |
| `mu_b` | `Inputs!$C$58` | Viscosity : b (K) | 1204.1 |
| `m_s` | `Inputs!$C$31` | Salt mass flow (kg/s) | 6170.523655 |
| `m_s_tube` | `Inputs!$C$49` | Salt flow per salt tube (kg/s) | 1.258776755 |
| `m_w` | `Inputs!$C$29` | Water/steam mass flow (kg/s) | 237.2234155 |
| `m_w_tube` | `Inputs!$C$48` | Water flow per steam tube (kg/s) | 0.03629489221 |
| `Nu_a` | `Inputs!$C$65` | Nu correlation : a (-) | 0.805 |
| `Nu_b` | `Inputs!$C$66` | Nu correlation : b (-) | 0.3333333333 |
| `Nu_C` | `Inputs!$C$64` | Nu = C·Re^a·Pr^b : C (-) | 0.0266 |
| `N_air` | `Inputs!$C$40` | Air-pass tubes (-) | 1634 |
| `N_gen` | `Inputs!$C$9` | Number of steam generators (-) | 3 |
| `N_salt` | `Inputs!$C$39` | Salt tubes (-) | 4902 |
| `N_seg` | `Inputs!$C$23` | Number of march segments (-) | 540 |
| `N_steam` | `Inputs!$C$37` | Steam tubes per steam generator (-) | 6536 |
| `P_e` | `Inputs!$C$8` | Plant electric output (MW) | 600 |
| `P_steam` | `Inputs!$C$20` | Steam pressure (MPa) | 24 |
| `P_th` | `Inputs!$C$7` | Reactor thermal power (MW) | 1500 |
| `Q_SG` | `Inputs!$C$11` | Heat duty per steam generator, Q (MW) | 500 |
| `rho_a` | `Inputs!$C$53` | Density ρ = a + bT : a (kg/m³) | 2112.68 |
| `rho_b` | `Inputs!$C$54` | Density : b (kg/m³·K) | -0.5635 |
| `rough` | `Inputs!$C$84` | Wall roughness (m) | 0.0000015 |
| `r_i` | `Inputs!$C$46` | Inner radius (m) | 0.01 |
| `r_m` | `Inputs!$C$47` | Mid-wall radius (m) | 0.011 |
| `salt_backed` | `Inputs!$C$81` | Fraction of salt-tube bore backed by contacts (-) | 0.6666666667 |
| `salt_gap` | `Inputs!$C$80` | Salt-tube fin arc (deg) | 60 |
| `salt_ratio` | `Inputs!$C$38` | Salt tubes per steam tube (-) | 0.75 |
| `T_freeze` | `Inputs!$C$61` | Salt freezing temperature (K) | 675 |
| `T_pc` | `Inputs!$C$76` | Pseudo-critical temperature at 24 MPa (K) | 654.38 |
| `T_salt_in` | `Inputs!$C$16` | Salt inlet temperature (top) (K) | 890 |
| `T_salt_out` | `Inputs!$C$17` | Salt outlet temperature (bottom) (K) | 810 |
| `t_wall` | `Inputs!$C$42` | Tube wall thickness (m) | 0.002 |
| `T_w_in` | `Inputs!$C$18` | Water inlet temperature (bottom) (K) | 560 |
| `T_w_out` | `Inputs!$C$19` | Steam outlet temperature (top) (K) | 830 |
| `wall_guess` | `Inputs!$C$77` | First-segment wall-temperature guess (wall − bulk) (K) | 96 |
| `We_SG` | `Inputs!$C$12` | Electric share per steam generator (MWe) | 200 |
| `WP_beta` | `Water_Properties!$H$5:$H$1385` | Isobaric expansion coefficient, 1/K | Stored array |
| `WP_cp` | `Water_Properties!$E$5:$E$1385` | Point specific heat, kJ/(kg·K) | Stored array |
| `WP_dT` | `Water_Properties!$E$3` | Water table spacing, K | 0.25 |
| `WP_h` | `Water_Properties!$C$5:$C$1385` | Enthalpy, kJ/kg | Stored array |
| `WP_k` | `Water_Properties!$G$5:$G$1385` | Water conductivity, W/(m·K) | Stored array |
| `WP_mu` | `Water_Properties!$F$5:$F$1385` | Dynamic viscosity, Pa·s | Stored array |
| `WP_rho` | `Water_Properties!$D$5:$D$1385` | Density, kg/m³ | Stored array |
| `WP_T` | `Water_Properties!$B$5:$B$1385` | Water temperature grid, K | Stored array |
| `WP_T0` | `Water_Properties!$C$3` | Water table starting temperature, K | 555 |
| `w_contact` | `Inputs!$C$45` | Salt-contact width per steam tube (m) | 0.03769911184 |
| `w_net` | `Inputs!$C$34` | Cycle work per kg steam (kJ/kg) | 927.3958036 |

## Complete formula register

Each entry identifies the full range covered by one relative-reference formula family and transcribes its first formula exactly. Filling that representative formula down the listed range with normal Excel relative-reference behavior reproduces every formula in the family; absolute references and named ranges remain unchanged.

Rows with different initialization or recurrence logic are separate entries. The reference IDs point to the explanations above; a family may include more than one adjacent result row when its relative formula is identical, in which case all applicable IDs are listed.

### Inputs

This sheet contains 26 formula cells in 26 audited families. The following entries cover all of them.

- **Plant efficiency:** `Inputs!C10` (1 cell). Explanation: E01. Representative cell: `C10`.

```excel
=P_e/P_th
```

- **Heat duty per steam generator, Q:** `Inputs!C11` (1 cell). Explanation: E02. Representative cell: `C11`.

```excel
=P_th/N_gen
```

- **Electric share per steam generator:** `Inputs!C12` (1 cell). Explanation: E02. Representative cell: `C12`.

```excel
=eta_plant*Q_SG
```

- **Cold-end ΔT (salt out − water in):** `Inputs!C21` (1 cell). Explanation: E03. Representative cell: `C21`.

```excel
=T_salt_out-T_w_in
```

- **Hot-end ΔT (salt in − steam out):** `Inputs!C22` (1 cell). Explanation: E03. Representative cell: `C22`.

```excel
=T_salt_in-T_w_out
```

- **Water temperature step per segment:** `Inputs!C24` (1 cell). Explanation: E03. Representative cell: `C24`.

```excel
=(T_w_out-T_w_in)/N_seg
```

- **Water enthalpy at inlet:** `Inputs!C27` (1 cell). Explanation: E04, E14. Representative cell: `C27`.

```excel
=INDEX(WP_h,INT(((T_w_in)-WP_T0)/WP_dT)+1)+(((T_w_in)-WP_T0)/WP_dT-INT(((T_w_in)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((T_w_in)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((T_w_in)-WP_T0)/WP_dT)+1))
```

- **Steam enthalpy at outlet:** `Inputs!C28` (1 cell). Explanation: E04, E14. Representative cell: `C28`.

```excel
=INDEX(WP_h,INT(((T_w_out)-WP_T0)/WP_dT)+1)+(((T_w_out)-WP_T0)/WP_dT-INT(((T_w_out)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((T_w_out)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((T_w_out)-WP_T0)/WP_dT)+1))
```

- **Water/steam mass flow:** `Inputs!C29` (1 cell). Explanation: E05. Representative cell: `C29`.

```excel
=Q_SG*1000/(h_w_out-h_w_in)
```

- **Salt Δh = ∫c_p dT from outlet to inlet:** `Inputs!C30` (1 cell). Explanation: E06. Representative cell: `C30`.

```excel
=cp_a*(T_salt_in-T_salt_out)+cp_b/2*(T_salt_in^2-T_salt_out^2)
```

- **Salt mass flow:** `Inputs!C31` (1 cell). Explanation: E06. Representative cell: `C31`.

```excel
=Q_SG*1000000/dh_salt
```

- **Salt capacity rate C_salt:** `Inputs!C32` (1 cell). Explanation: E07. Representative cell: `C32`.

```excel
=Q_SG/(T_salt_in-T_salt_out)
```

- **Water average capacity rate C_water:** `Inputs!C33` (1 cell). Explanation: E07. Representative cell: `C33`.

```excel
=Q_SG/(T_w_out-T_w_in)
```

- **Cycle work per kg steam:** `Inputs!C34` (1 cell). Explanation: E08. Representative cell: `C34`.

```excel
=eta_R*(h_w_out-h_w_in)
```

- **Salt tubes:** `Inputs!C39` (1 cell). Explanation: E09. Representative cell: `C39`.

```excel
=ROUND(N_steam*salt_ratio,0)
```

- **Air-pass tubes:** `Inputs!C40` (1 cell). Explanation: E09. Representative cell: `C40`.

```excel
=N_steam-N_salt
```

- **Tube outer diameter:** `Inputs!C43` (1 cell). Explanation: E10. Representative cell: `C43`.

```excel
=D_i+2*t_wall
```

- **Flow area per tube:** `Inputs!C44` (1 cell). Explanation: E10. Representative cell: `C44`.

```excel
=PI()*D_i^2/4
```

- **Salt-contact width per steam tube:** `Inputs!C45` (1 cell). Explanation: E11. Representative cell: `C45`.

```excel
=0.5*PI()*D_o
```

- **Inner radius:** `Inputs!C46` (1 cell). Explanation: E10. Representative cell: `C46`.

```excel
=D_i/2
```

- **Mid-wall radius:** `Inputs!C47` (1 cell). Explanation: E10. Representative cell: `C47`.

```excel
=(D_i+t_wall)/2
```

- **Water flow per steam tube:** `Inputs!C48` (1 cell). Explanation: E12. Representative cell: `C48`.

```excel
=m_w/N_steam
```

- **Salt flow per salt tube:** `Inputs!C49` (1 cell). Explanation: E12. Representative cell: `C49`.

```excel
=m_s/N_salt
```

- **Steam-side mass flux G:** `Inputs!C50` (1 cell). Explanation: E12. Representative cell: `C50`.

```excel
=m_w_tube/A_flow
```

- **Nu correlation : b:** `Inputs!C66` (1 cell). Explanation: E13. Representative cell: `C66`.

```excel
=1/3
```

- **Fraction of salt-tube bore backed by contacts:** `Inputs!C81` (1 cell). Explanation: E13. Representative cell: `C81`.

```excel
=2/3
```

### Temperature_March

This sheet contains 16,200 formula cells in 34 audited families. The following entries cover all of them.

- **Segment number:** `Temperature_March!A5` (1 cell). Explanation: E16. Representative cell: `A5`.

```excel
=1
```

- **Segment number:** `Temperature_March!A6:A544` (539 cells). Explanation: E16. Representative cell: `A6`.

```excel
=A5+1
```

- **Water temperature at segment start (K):** `Temperature_March!B5` (1 cell). Explanation: E16. Representative cell: `B5`.

```excel
=T_w_in
```

- **Water temperature at segment start (K):** `Temperature_March!B6:B544` (539 cells). Explanation: E16. Representative cell: `B6`.

```excel
=C5
```

- **Water temperature at segment end (K):** `Temperature_March!C5:C544` (540 cells). Explanation: E16. Representative cell: `C5`.

```excel
=B5+dT_step
```

- **Water mean temperature in segment (K):** `Temperature_March!D5:D544` (540 cells). Explanation: E16. Representative cell: `D5`.

```excel
=(B5+C5)/2
```

- **Water enthalpy at segment start (kJ/kg):** `Temperature_March!E5:E544` (540 cells). Explanation: E17, E14. Representative cell: `E5`.

```excel
=INDEX(WP_h,INT(((B5)-WP_T0)/WP_dT)+1)+(((B5)-WP_T0)/WP_dT-INT(((B5)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((B5)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((B5)-WP_T0)/WP_dT)+1))
```

- **Water enthalpy at segment end (kJ/kg):** `Temperature_March!F5:F544` (540 cells). Explanation: E17, E14. Representative cell: `F5`.

```excel
=INDEX(WP_h,INT(((C5)-WP_T0)/WP_dT)+1)+(((C5)-WP_T0)/WP_dT-INT(((C5)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((C5)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((C5)-WP_T0)/WP_dT)+1))
```

- **Heat transferred in segment, whole SG (MW):** `Temperature_March!G5:G544` (540 cells). Explanation: E17. Representative cell: `G5`.

```excel
=m_w*(F5-E5)/1000
```

- **Cumulative heat at segment end (MW):** `Temperature_March!H5` (1 cell). Explanation: E18. Representative cell: `H5`.

```excel
=G5
```

- **Cumulative heat at segment end (MW):** `Temperature_March!H6:H544` (539 cells). Explanation: E18. Representative cell: `H6`.

```excel
=H5+G6
```

- **Fraction of total duty at segment end (-):** `Temperature_March!I5:I544` (540 cells). Explanation: E18. Representative cell: `I5`.

```excel
=H5/Q_SG
```

- **Salt temperature at segment start (K):** `Temperature_March!J5` (1 cell). Explanation: E19. Representative cell: `J5`.

```excel
=(-cp_a+SQRT(cp_a^2+2*cp_b*(cp_a*T_salt_out+cp_b/2*T_salt_out^2)))/cp_b
```

- **Salt temperature at segment start (K):** `Temperature_March!J6:J544` (539 cells). Explanation: E19. Representative cell: `J6`.

```excel
=(-cp_a+SQRT(cp_a^2+2*cp_b*(cp_a*T_salt_out+cp_b/2*T_salt_out^2+H5*1000000/m_s)))/cp_b
```

- **Salt temperature at segment end (K):** `Temperature_March!K5:K544` (540 cells). Explanation: E19. Representative cell: `K5`.

```excel
=(-cp_a+SQRT(cp_a^2+2*cp_b*(cp_a*T_salt_out+cp_b/2*T_salt_out^2+H5*1000000/m_s)))/cp_b
```

- **Salt mean temperature in segment (K):** `Temperature_March!L5:L544` (540 cells). Explanation: E19. Representative cell: `L5`.

```excel
=(J5+K5)/2
```

- **Salt − water ΔT at segment start (K):** `Temperature_March!M5:M544` (540 cells). Explanation: E20. Representative cell: `M5`.

```excel
=J5-B5
```

- **Salt − water ΔT at segment end (K):** `Temperature_March!N5:N544` (540 cells). Explanation: E20. Representative cell: `N5`.

```excel
=K5-C5
```

- **Segment log-mean temperature difference (K):** `Temperature_March!O5:O544` (540 cells). Explanation: E20. Representative cell: `O5`.

```excel
=IF(ABS(M5-N5)<0.000000001,M5,(M5-N5)/LN(M5/N5))
```

- **UA required for segment (MW/K):** `Temperature_March!P5:P544` (540 cells). Explanation: E21. Representative cell: `P5`.

```excel
=G5/O5
```

- **ΔT a single LMTD assumes at segment end (K):** `Temperature_March!Q5:Q544` (540 cells). Explanation: E22. Representative cell: `Q5`.

```excel
=dT_cold+(dT_hot-dT_cold)*I5
```

- **Water effective c_p in segment (kJ/kg·K):** `Temperature_March!R5:R544` (540 cells). Explanation: E23. Representative cell: `R5`.

```excel
=(F5-E5)/(C5-B5)
```

- **Local water capacity rate ṁ_w·c_p (MW/K):** `Temperature_March!S5:S544` (540 cells). Explanation: E23. Representative cell: `S5`.

```excel
=m_w*R5/1000
```

- **Stream with larger capacity rate:** `Temperature_March!T5:T544` (540 cells). Explanation: E23. Representative cell: `T5`.

```excel
=IF(S5>C_salt,"Water","Salt")
```

- **Water density at mean T (kg/m³):** `Temperature_March!U5:U544` (540 cells). Explanation: E24, E14. Representative cell: `U5`.

```excel
=INDEX(WP_rho,INT(((D5)-WP_T0)/WP_dT)+1)+(((D5)-WP_T0)/WP_dT-INT(((D5)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((D5)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((D5)-WP_T0)/WP_dT)+1))
```

- **Water viscosity at mean T (Pa·s):** `Temperature_March!V5:V544` (540 cells). Explanation: E24, E14. Representative cell: `V5`.

```excel
=INDEX(WP_mu,INT(((D5)-WP_T0)/WP_dT)+1)+(((D5)-WP_T0)/WP_dT-INT(((D5)-WP_T0)/WP_dT))*(INDEX(WP_mu,INT(((D5)-WP_T0)/WP_dT)+2)-INDEX(WP_mu,INT(((D5)-WP_T0)/WP_dT)+1))
```

- **Water conductivity at mean T (W/m·K):** `Temperature_March!W5:W544` (540 cells). Explanation: E24, E14. Representative cell: `W5`.

```excel
=INDEX(WP_k,INT(((D5)-WP_T0)/WP_dT)+1)+(((D5)-WP_T0)/WP_dT-INT(((D5)-WP_T0)/WP_dT))*(INDEX(WP_k,INT(((D5)-WP_T0)/WP_dT)+2)-INDEX(WP_k,INT(((D5)-WP_T0)/WP_dT)+1))
```

- **Water true c_p at mean T (kJ/kg·K):** `Temperature_March!X5:X544` (540 cells). Explanation: E24, E14. Representative cell: `X5`.

```excel
=INDEX(WP_cp,INT(((D5)-WP_T0)/WP_dT)+1)+(((D5)-WP_T0)/WP_dT-INT(((D5)-WP_T0)/WP_dT))*(INDEX(WP_cp,INT(((D5)-WP_T0)/WP_dT)+2)-INDEX(WP_cp,INT(((D5)-WP_T0)/WP_dT)+1))
```

- **Water enthalpy at mean T (kJ/kg):** `Temperature_March!Y5:Y544` (540 cells). Explanation: E24, E14. Representative cell: `Y5`.

```excel
=INDEX(WP_h,INT(((D5)-WP_T0)/WP_dT)+1)+(((D5)-WP_T0)/WP_dT-INT(((D5)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((D5)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((D5)-WP_T0)/WP_dT)+1))
```

- **Water expansion coefficient β at mean T (1/K):** `Temperature_March!Z5:Z544` (540 cells). Explanation: E24, E14. Representative cell: `Z5`.

```excel
=INDEX(WP_beta,INT(((D5)-WP_T0)/WP_dT)+1)+(((D5)-WP_T0)/WP_dT-INT(((D5)-WP_T0)/WP_dT))*(INDEX(WP_beta,INT(((D5)-WP_T0)/WP_dT)+2)-INDEX(WP_beta,INT(((D5)-WP_T0)/WP_dT)+1))
```

- **Salt density at mean T (kg/m³):** `Temperature_March!AA5:AA544` (540 cells). Explanation: E15. Representative cell: `AA5`.

```excel
=rho_a+rho_b*L5
```

- **Salt specific heat at mean T (J/kg·K):** `Temperature_March!AB5:AB544` (540 cells). Explanation: E15. Representative cell: `AB5`.

```excel
=cp_a+cp_b*L5
```

- **Salt viscosity at mean T (Pa·s):** `Temperature_March!AC5:AC544` (540 cells). Explanation: E15. Representative cell: `AC5`.

```excel
=mu_a*EXP(mu_b/L5)
```

- **Salt conductivity at mean T (W/m·K):** `Temperature_March!AD5:AD544` (540 cells). Explanation: E15. Representative cell: `AD5`.

```excel
=k_a+k_b*L5
```

### Model_Spreadsheet

This sheet contains 17,280 formula cells in 33 audited families. The following entries cover all of them.

- **Segment number:** `Model_Spreadsheet!A5:A544` (540 cells). Explanation: E25. Representative cell: `A5`.

```excel
=Temperature_March!A5
```

- **Water mean temperature (K):** `Model_Spreadsheet!B5:B544` (540 cells). Explanation: E25. Representative cell: `B5`.

```excel
=Temperature_March!D5
```

- **Salt mean temperature (K):** `Model_Spreadsheet!C5:C544` (540 cells). Explanation: E25. Representative cell: `C5`.

```excel
=Temperature_March!L5
```

- **Segment LMTD (K):** `Model_Spreadsheet!D5:D544` (540 cells). Explanation: E25. Representative cell: `D5`.

```excel
=Temperature_March!O5
```

- **Heat per steam tube in segment (W):** `Model_Spreadsheet!E5:E544` (540 cells). Explanation: E25. Representative cell: `E5`.

```excel
=Temperature_March!G5*1000000/N_steam
```

- **Water velocity (m/s):** `Model_Spreadsheet!F5:F544` (540 cells). Explanation: E26. Representative cell: `F5`.

```excel
=m_w_tube/(Temperature_March!U5*A_flow)
```

- **Water Reynolds number (-):** `Model_Spreadsheet!G5:G544` (540 cells). Explanation: E26. Representative cell: `G5`.

```excel
=Temperature_March!U5*F5*D_i/Temperature_March!V5
```

- **Water Prandtl number (-):** `Model_Spreadsheet!H5:H544` (540 cells). Explanation: E27. Representative cell: `H5`.

```excel
=Temperature_March!R5*1000*Temperature_March!V5/Temperature_March!W5
```

- **Water Nusselt number (-):** `Model_Spreadsheet!I5:I544` (540 cells). Explanation: E29. Representative cell: `I5`.

```excel
=Nu_C*G5^Nu_a*H5^Nu_b
```

- **Water-side h (W/m²·K):** `Model_Spreadsheet!J5:J544` (540 cells). Explanation: E28. Representative cell: `J5`.

```excel
=I5*Temperature_March!W5/D_i
```

- **Salt velocity (m/s):** `Model_Spreadsheet!K5:K544` (540 cells). Explanation: E26. Representative cell: `K5`.

```excel
=m_s_tube/(Temperature_March!AA5*A_flow)
```

- **Salt Reynolds number (-):** `Model_Spreadsheet!L5:L544` (540 cells). Explanation: E26. Representative cell: `L5`.

```excel
=Temperature_March!AA5*K5*D_i/Temperature_March!AC5
```

- **Salt Prandtl number (-):** `Model_Spreadsheet!M5:M544` (540 cells). Explanation: E27. Representative cell: `M5`.

```excel
=Temperature_March!AB5*Temperature_March!AC5/Temperature_March!AD5
```

- **Salt Nusselt number (-):** `Model_Spreadsheet!N5:N544` (540 cells). Explanation: E29. Representative cell: `N5`.

```excel
=Nu_C*L5^Nu_a*M5^Nu_b
```

- **Salt-side h (W/m²·K):** `Model_Spreadsheet!O5:O544` (540 cells). Explanation: E28. Representative cell: `O5`.

```excel
=N5*Temperature_March!AD5/D_i
```

- **Water film resistance (m²·K/kW):** `Model_Spreadsheet!P5:P544` (540 cells). Explanation: E30. Representative cell: `P5`.

```excel
=1000/J5
```

- **Salt film resistance (m²·K/kW):** `Model_Spreadsheet!Q5:Q544` (540 cells). Explanation: E30. Representative cell: `Q5`.

```excel
=1000/O5
```

- **Two tube walls (m²·K/kW):** `Model_Spreadsheet!R5:R544` (540 cells). Explanation: E30. Representative cell: `R5`.

```excel
=1000*2*t_wall/k_wall_ss
```

- **Total resistance (m²·K/kW):** `Model_Spreadsheet!S5:S544` (540 cells). Explanation: E30. Representative cell: `S5`.

```excel
=P5+Q5+R5
```

- **Local U, contact-area basis (W/m²·K):** `Model_Spreadsheet!T5:T544` (540 cells). Explanation: E30. Representative cell: `T5`.

```excel
=1000/S5
```

- **Tube length for segment (m):** `Model_Spreadsheet!U5:U544` (540 cells). Explanation: E31. Representative cell: `U5`.

```excel
=E5*S5/1000/(D5*w_contact)
```

- **Height at segment end (m):** `Model_Spreadsheet!V5` (1 cell). Explanation: E31. Representative cell: `V5`.

```excel
=U5
```

- **Height at segment end (m):** `Model_Spreadsheet!V6:V544` (539 cells). Explanation: E31. Representative cell: `V6`.

```excel
=V5+U6
```

- **Heat flux at contact strip (kW/m²):** `Model_Spreadsheet!W5:W544` (540 cells). Explanation: E32. Representative cell: `W5`.

```excel
=D5/S5
```

- **Steam-side wall temperature (K):** `Model_Spreadsheet!X5:X544` (540 cells). Explanation: E32. Representative cell: `X5`.

```excel
=B5+W5*1000/J5
```

- **Salt-side wall temperature (K):** `Model_Spreadsheet!Y5:Y544` (540 cells). Explanation: E32. Representative cell: `Y5`.

```excel
=C5-W5*1000/O5
```

- **Heat flux, steam-bore average (kW/m²):** `Model_Spreadsheet!Z5:Z544` (540 cells). Explanation: E52. Representative cell: `Z5`.

```excel
=E5/U5/(PI()*D_i)/1000
```

- **Heat flux / mass flux q″/G (kJ/kg):** `Model_Spreadsheet!AA5:AA544` (540 cells). Explanation: E52. Representative cell: `AA5`.

```excel
=Z5/G_w
```

- **Water Darcy friction factor (-):** `Model_Spreadsheet!AB5:AB544` (540 cells). Explanation: E53. Representative cell: `AB5`.

```excel
=(8/6.0516)*LN(rough/D_i+(7/G5)^0.9)^(-2)
```

- **Water friction ΔP (Pa):** `Model_Spreadsheet!AC5:AC544` (540 cells). Explanation: E54. Representative cell: `AC5`.

```excel
=AB5*U5/D_i*0.5*Temperature_March!U5*F5^2
```

- **Water gravity ΔP (Pa):** `Model_Spreadsheet!AD5:AD544` (540 cells). Explanation: E54. Representative cell: `AD5`.

```excel
=Temperature_March!U5*g_acc*U5
```

- **Salt Darcy friction factor (-):** `Model_Spreadsheet!AE5:AE544` (540 cells). Explanation: E53. Representative cell: `AE5`.

```excel
=(8/6.0516)*LN(rough/D_i+(7/L5)^0.9)^(-2)
```

- **Salt friction ΔP (Pa):** `Model_Spreadsheet!AF5:AF544` (540 cells). Explanation: E54. Representative cell: `AF5`.

```excel
=AE5*U5/D_i*0.5*Temperature_March!AA5*K5^2
```

### Model_BestEstimate

This sheet contains 35,640 formula cells in 68 audited families. The following entries cover all of them.

- **Segment number:** `Model_BestEstimate!A5:A544` (540 cells). Explanation: E25. Representative cell: `A5`.

```excel
=Temperature_March!A5
```

- **Water mean temperature (K):** `Model_BestEstimate!B5:B544` (540 cells). Explanation: E25. Representative cell: `B5`.

```excel
=Temperature_March!D5
```

- **Salt mean temperature (K):** `Model_BestEstimate!C5:C544` (540 cells). Explanation: E25. Representative cell: `C5`.

```excel
=Temperature_March!L5
```

- **Segment LMTD (K):** `Model_BestEstimate!D5:D544` (540 cells). Explanation: E25. Representative cell: `D5`.

```excel
=Temperature_March!O5
```

- **Heat per steam tube in segment (W):** `Model_BestEstimate!E5:E544` (540 cells). Explanation: E25. Representative cell: `E5`.

```excel
=Temperature_March!G5*1000000/N_steam
```

- **Salt velocity (m/s):** `Model_BestEstimate!F5:F544` (540 cells). Explanation: E26. Representative cell: `F5`.

```excel
=m_s_tube/(Temperature_March!AA5*A_flow)
```

- **Salt Reynolds number (-):** `Model_BestEstimate!G5:G544` (540 cells). Explanation: E26. Representative cell: `G5`.

```excel
=Temperature_March!AA5*F5*D_i/Temperature_March!AC5
```

- **Salt Prandtl number (-):** `Model_BestEstimate!H5:H544` (540 cells). Explanation: E27. Representative cell: `H5`.

```excel
=Temperature_March!AB5*Temperature_March!AC5/Temperature_March!AD5
```

- **Petukhov friction factor (-):** `Model_BestEstimate!I5:I544` (540 cells). Explanation: E33. Representative cell: `I5`.

```excel
=(0.79*LN(G5)-1.64)^(-2)
```

- **Salt Nusselt, Gnielinski (-):** `Model_BestEstimate!J5:J544` (540 cells). Explanation: E34. Representative cell: `J5`.

```excel
=(I5/8)*(G5-1000)*H5/(1+12.7*SQRT(I5/8)*(H5^(2/3)-1))
```

- **Salt-side h (W/m²·K):** `Model_BestEstimate!K5:K544` (540 cells). Explanation: E34, E28. Representative cell: `K5`.

```excel
=J5*Temperature_March!AD5/D_i
```

- **Water bulk Reynolds number (-):** `Model_BestEstimate!L5:L544` (540 cells). Explanation: E26. Representative cell: `L5`.

```excel
=G_w*D_i/Temperature_March!V5
```

- **Water bulk Prandtl number (-):** `Model_BestEstimate!M5:M544` (540 cells). Explanation: E27. Representative cell: `M5`.

```excel
=Temperature_March!X5*1000*Temperature_March!V5/Temperature_March!W5
```

- **Pass 1: assumed steam-side wall T (K):** `Model_BestEstimate!N5` (1 cell). Explanation: E35. Representative cell: `N5`.

```excel
=B5+wall_guess
```

- **Pass 1: assumed steam-side wall T (K):** `Model_BestEstimate!N6:N544` (539 cells). Explanation: E35. Representative cell: `N6`.

```excel
=BB5+(B6-B5)
```

- **Pass 1: water density at wall T (kg/m³):** `Model_BestEstimate!O5:O544` (540 cells). Explanation: E36, E14. Representative cell: `O5`.

```excel
=INDEX(WP_rho,INT(((N5)-WP_T0)/WP_dT)+1)+(((N5)-WP_T0)/WP_dT-INT(((N5)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((N5)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((N5)-WP_T0)/WP_dT)+1))
```

- **Pass 1: water enthalpy at wall T (kJ/kg):** `Model_BestEstimate!P5:P544` (540 cells). Explanation: E36, E14. Representative cell: `P5`.

```excel
=INDEX(WP_h,INT(((N5)-WP_T0)/WP_dT)+1)+(((N5)-WP_T0)/WP_dT-INT(((N5)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((N5)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((N5)-WP_T0)/WP_dT)+1))
```

- **Pass 1: integrated c̄_p wall–bulk (J/kg·K):** `Model_BestEstimate!Q5:Q544` (540 cells). Explanation: E36. Representative cell: `Q5`.

```excel
=(P5-Temperature_March!Y5)*1000/(N5-B5)
```

- **Pass 1: Jackson exponent n (-):** `Model_BestEstimate!R5:R544` (540 cells). Explanation: E37. Representative cell: `R5`.

```excel
=IF(OR(AND(B5<N5,N5<=T_pc),B5>=1.2*T_pc),0.4,IF(AND(B5<=T_pc,T_pc<N5),0.4+0.2*(N5/T_pc-1),0.4+0.2*(N5/T_pc-1)*(1-5*(B5/T_pc-1))))
```

- **Pass 1: water-side h, Jackson (W/m²·K):** `Model_BestEstimate!S5:S544` (540 cells). Explanation: E38. Representative cell: `S5`.

```excel
=J_C*L5^J_Re*M5^J_Pr*(O5/Temperature_March!U5)^J_rho*(Q5/(Temperature_March!X5*1000))^R5*Temperature_March!W5/D_i
```

- **Pass 1: wall conductivity, 316 SS (W/m·K):** `Model_BestEstimate!T5:T544` (540 cells). Explanation: E40, E14. Representative cell: `T5`.

```excel
=(INDEX(K316_k,INT((((N5+C5)/2)-K316_T0)/K316_dT)+1)+((((N5+C5)/2)-K316_T0)/K316_dT-INT((((N5+C5)/2)-K316_T0)/K316_dT))*(INDEX(K316_k,INT((((N5+C5)/2)-K316_T0)/K316_dT)+2)-INDEX(K316_k,INT((((N5+C5)/2)-K316_T0)/K316_dT)+1)))
```

- **Pass 1: fin efficiency, 60° arc (-):** `Model_BestEstimate!U5:U544` (540 cells). Explanation: E41. Representative cell: `U5`.

```excel
=TANH(SQRT(S5/(T5*t_wall))*r_m*RADIANS(_gap1)/2)/(SQRT(S5/(T5*t_wall))*r_m*RADIANS(_gap1)/2)
```

- **Pass 1: fin efficiency, 120° arc (-):** `Model_BestEstimate!V5:V544` (540 cells). Explanation: E41. Representative cell: `V5`.

```excel
=TANH(SQRT(S5/(T5*t_wall))*r_m*RADIANS(_gap2)/2)/(SQRT(S5/(T5*t_wall))*r_m*RADIANS(_gap2)/2)
```

- **Pass 1: effective water-wetted perimeter (m):** `Model_BestEstimate!W5:W544` (540 cells). Explanation: E42. Representative cell: `W5`.

```excel
=r_i*(PI()+U5*RADIANS(_gap1)+V5*RADIANS(_gap2))
```

- **Pass 1: salt-tube fin efficiency (-):** `Model_BestEstimate!X5:X544` (540 cells). Explanation: E41. Representative cell: `X5`.

```excel
=TANH(SQRT(K5/(T5*t_wall))*r_m*RADIANS(salt_gap)/2)/(SQRT(K5/(T5*t_wall))*r_m*RADIANS(salt_gap)/2)
```

- **Pass 1: effective salt-wetted perimeter per steam tube (m):** `Model_BestEstimate!Y5:Y544` (540 cells). Explanation: E43. Representative cell: `Y5`.

```excel
=N_salt/N_steam*2*PI()*r_i*(salt_backed+(1-salt_backed)*X5)
```

- **Pass 1: water film resistance (K·m/W):** `Model_BestEstimate!Z5:Z544` (540 cells). Explanation: E44. Representative cell: `Z5`.

```excel
=1/(S5*W5)
```

- **Pass 1: salt film resistance (K·m/W):** `Model_BestEstimate!AA5:AA544` (540 cells). Explanation: E44. Representative cell: `AA5`.

```excel
=1/(K5*Y5)
```

- **Pass 1: two walls (K·m/W):** `Model_BestEstimate!AB5:AB544` (540 cells). Explanation: E45. Representative cell: `AB5`.

```excel
=2*t_wall/(T5*w_contact)
```

- **Pass 1: tube-to-tube interface (K·m/W):** `Model_BestEstimate!AC5:AC544` (540 cells). Explanation: E46. Representative cell: `AC5`.

```excel
=IF(h_contact=0,0,1/(h_contact*w_contact))
```

- **Pass 1: total resistance per steam tube (K·m/W):** `Model_BestEstimate!AD5:AD544` (540 cells). Explanation: E47. Representative cell: `AD5`.

```excel
=Z5+AA5+AB5+AC5
```

- **Pass 1: updated steam-side wall T (K):** `Model_BestEstimate!AE5:AE544` (540 cells). Explanation: E47. Representative cell: `AE5`.

```excel
=B5+D5/AD5*Z5
```

- **Pass 2: assumed steam-side wall T (K):** `Model_BestEstimate!AF5:AF544` (540 cells). Explanation: E48. Representative cell: `AF5`.

```excel
=AE5
```

- **Pass 2: water density at wall T (kg/m³):** `Model_BestEstimate!AG5:AG544` (540 cells). Explanation: E36, E14. Representative cell: `AG5`.

```excel
=INDEX(WP_rho,INT(((AF5)-WP_T0)/WP_dT)+1)+(((AF5)-WP_T0)/WP_dT-INT(((AF5)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((AF5)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((AF5)-WP_T0)/WP_dT)+1))
```

- **Pass 2: water enthalpy at wall T (kJ/kg):** `Model_BestEstimate!AH5:AH544` (540 cells). Explanation: E36, E14. Representative cell: `AH5`.

```excel
=INDEX(WP_h,INT(((AF5)-WP_T0)/WP_dT)+1)+(((AF5)-WP_T0)/WP_dT-INT(((AF5)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((AF5)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((AF5)-WP_T0)/WP_dT)+1))
```

- **Pass 2: integrated c̄_p wall–bulk (J/kg·K):** `Model_BestEstimate!AI5:AI544` (540 cells). Explanation: E36. Representative cell: `AI5`.

```excel
=(AH5-Temperature_March!Y5)*1000/(AF5-B5)
```

- **Pass 2: Jackson exponent n (-):** `Model_BestEstimate!AJ5:AJ544` (540 cells). Explanation: E37. Representative cell: `AJ5`.

```excel
=IF(OR(AND(B5<AF5,AF5<=T_pc),B5>=1.2*T_pc),0.4,IF(AND(B5<=T_pc,T_pc<AF5),0.4+0.2*(AF5/T_pc-1),0.4+0.2*(AF5/T_pc-1)*(1-5*(B5/T_pc-1))))
```

- **Pass 2: water-side h, Jackson (W/m²·K):** `Model_BestEstimate!AK5:AK544` (540 cells). Explanation: E38, E39. Representative cell: `AK5`.

```excel
=J_C*L5^J_Re*M5^J_Pr*(AG5/Temperature_March!U5)^J_rho*(AI5/(Temperature_March!X5*1000))^AJ5*Temperature_March!W5/D_i*IF(AND(B5<T_pc,T_pc<AF5),HTD_mult,1)
```

- **Pass 2: wall conductivity, 316 SS (W/m·K):** `Model_BestEstimate!AL5:AL544` (540 cells). Explanation: E40, E14. Representative cell: `AL5`.

```excel
=(INDEX(K316_k,INT((((AF5+C5)/2)-K316_T0)/K316_dT)+1)+((((AF5+C5)/2)-K316_T0)/K316_dT-INT((((AF5+C5)/2)-K316_T0)/K316_dT))*(INDEX(K316_k,INT((((AF5+C5)/2)-K316_T0)/K316_dT)+2)-INDEX(K316_k,INT((((AF5+C5)/2)-K316_T0)/K316_dT)+1)))
```

- **Pass 2: fin efficiency, 60° arc (-):** `Model_BestEstimate!AM5:AM544` (540 cells). Explanation: E41. Representative cell: `AM5`.

```excel
=TANH(SQRT(AK5/(AL5*t_wall))*r_m*RADIANS(_gap1)/2)/(SQRT(AK5/(AL5*t_wall))*r_m*RADIANS(_gap1)/2)
```

- **Pass 2: fin efficiency, 120° arc (-):** `Model_BestEstimate!AN5:AN544` (540 cells). Explanation: E41. Representative cell: `AN5`.

```excel
=TANH(SQRT(AK5/(AL5*t_wall))*r_m*RADIANS(_gap2)/2)/(SQRT(AK5/(AL5*t_wall))*r_m*RADIANS(_gap2)/2)
```

- **Pass 2: effective water-wetted perimeter (m):** `Model_BestEstimate!AO5:AO544` (540 cells). Explanation: E42. Representative cell: `AO5`.

```excel
=r_i*(PI()+AM5*RADIANS(_gap1)+AN5*RADIANS(_gap2))
```

- **Pass 2: salt-tube fin efficiency (-):** `Model_BestEstimate!AP5:AP544` (540 cells). Explanation: E41. Representative cell: `AP5`.

```excel
=TANH(SQRT(K5/(AL5*t_wall))*r_m*RADIANS(salt_gap)/2)/(SQRT(K5/(AL5*t_wall))*r_m*RADIANS(salt_gap)/2)
```

- **Pass 2: effective salt-wetted perimeter per steam tube (m):** `Model_BestEstimate!AQ5:AQ544` (540 cells). Explanation: E43. Representative cell: `AQ5`.

```excel
=N_salt/N_steam*2*PI()*r_i*(salt_backed+(1-salt_backed)*AP5)
```

- **Pass 2: water film resistance (K·m/W):** `Model_BestEstimate!AR5:AR544` (540 cells). Explanation: E44. Representative cell: `AR5`.

```excel
=1/(AK5*AO5)
```

- **Pass 2: salt film resistance (K·m/W):** `Model_BestEstimate!AS5:AS544` (540 cells). Explanation: E44. Representative cell: `AS5`.

```excel
=1/(K5*AQ5)
```

- **Pass 2: two walls (K·m/W):** `Model_BestEstimate!AT5:AT544` (540 cells). Explanation: E45. Representative cell: `AT5`.

```excel
=2*t_wall/(AL5*w_contact)
```

- **Pass 2: tube-to-tube interface (K·m/W):** `Model_BestEstimate!AU5:AU544` (540 cells). Explanation: E46. Representative cell: `AU5`.

```excel
=IF(h_contact=0,0,1/(h_contact*w_contact))
```

- **Pass 2: total resistance per steam tube (K·m/W):** `Model_BestEstimate!AV5:AV544` (540 cells). Explanation: E47. Representative cell: `AV5`.

```excel
=AR5+AS5+AT5+AU5
```

- **Pass 2: updated steam-side wall T (K):** `Model_BestEstimate!AW5:AW544` (540 cells). Explanation: E47. Representative cell: `AW5`.

```excel
=B5+D5/AV5*AR5
```

- **Heat per unit length per steam tube (W/m):** `Model_BestEstimate!AX5:AX544` (540 cells). Explanation: E49. Representative cell: `AX5`.

```excel
=D5/AV5
```

- **Tube length for segment (m):** `Model_BestEstimate!AY5:AY544` (540 cells). Explanation: E49. Representative cell: `AY5`.

```excel
=E5/AX5
```

- **Height at segment end (m):** `Model_BestEstimate!AZ5` (1 cell). Explanation: E49. Representative cell: `AZ5`.

```excel
=AY5
```

- **Height at segment end (m):** `Model_BestEstimate!AZ6:AZ544` (539 cells). Explanation: E49. Representative cell: `AZ6`.

```excel
=AZ5+AY6
```

- **Local U, contact-area basis (W/m²·K):** `Model_BestEstimate!BA5:BA544` (540 cells). Explanation: E50. Representative cell: `BA5`.

```excel
=1/(AV5*w_contact)
```

- **Final steam-side wall temperature (K):** `Model_BestEstimate!BB5:BB544` (540 cells). Explanation: E51. Representative cell: `BB5`.

```excel
=B5+AX5*AR5
```

- **Salt-side wall temperature (K):** `Model_BestEstimate!BC5:BC544` (540 cells). Explanation: E51. Representative cell: `BC5`.

```excel
=C5-AX5*AS5
```

- **Heat flux, steam-bore average (kW/m²):** `Model_BestEstimate!BD5:BD544` (540 cells). Explanation: E52. Representative cell: `BD5`.

```excel
=AX5/(PI()*D_i)/1000
```

- **Heat flux / mass flux q″/G (kJ/kg):** `Model_BestEstimate!BE5:BE544` (540 cells). Explanation: E52. Representative cell: `BE5`.

```excel
=BD5/G_w
```

- **In deterioration-prone zone? (1 = yes):** `Model_BestEstimate!BF5:BF544` (540 cells). Explanation: E55. Representative cell: `BF5`.

```excel
=IF(AND(B5<T_pc,BB5>T_pc),1,0)
```

- **Buoyancy parameter Bo* (-):** `Model_BestEstimate!BG5:BG544` (540 cells). Explanation: E56. Representative cell: `BG5`.

```excel
=(g_acc*Temperature_March!Z5*D_i^4*BD5*1000/(Temperature_March!W5*(Temperature_March!V5/Temperature_March!U5)^2))/(L5^3.425*M5^0.8)
```

- **Acceleration parameter K_v (-):** `Model_BestEstimate!BH5:BH544` (540 cells). Explanation: E57. Representative cell: `BH5`.

```excel
=4*BD5*1000*Temperature_March!Z5/(G_w*Temperature_March!X5*1000*L5)
```

- **Water velocity (m/s):** `Model_BestEstimate!BI5:BI544` (540 cells). Explanation: E26. Representative cell: `BI5`.

```excel
=G_w/Temperature_March!U5
```

- **Water Darcy friction factor (-):** `Model_BestEstimate!BJ5:BJ544` (540 cells). Explanation: E53. Representative cell: `BJ5`.

```excel
=(8/6.0516)*LN(rough/D_i+(7/L5)^0.9)^(-2)
```

- **Water friction ΔP (Pa):** `Model_BestEstimate!BK5:BK544` (540 cells). Explanation: E54. Representative cell: `BK5`.

```excel
=BJ5*AY5/D_i*0.5*Temperature_March!U5*BI5^2
```

- **Water gravity ΔP (Pa):** `Model_BestEstimate!BL5:BL544` (540 cells). Explanation: E54. Representative cell: `BL5`.

```excel
=Temperature_March!U5*g_acc*AY5
```

- **Salt Darcy friction factor (-):** `Model_BestEstimate!BM5:BM544` (540 cells). Explanation: E53. Representative cell: `BM5`.

```excel
=(8/6.0516)*LN(rough/D_i+(7/G5)^0.9)^(-2)
```

- **Salt friction ΔP (Pa):** `Model_BestEstimate!BN5:BN544` (540 cells). Explanation: E54. Representative cell: `BN5`.

```excel
=BM5*AY5/D_i*0.5*Temperature_March!AA5*F5^2
```

### Results

This sheet contains 79 formula cells in 77 audited families. The following entries cover all of them.

- **Heat duty Q:** `Results!C6` (1 cell). Explanation: E58. Representative cell: `C6`.

```excel
=Q_SG
```

- **Heat duty Q:** `Results!D6` (1 cell). Explanation: E58. Representative cell: `D6`.

```excel
=Q_SG
```

- **Water / steam mass flow:** `Results!C7` (1 cell). Explanation: E58. Representative cell: `C7`.

```excel
=m_w
```

- **Water / steam mass flow:** `Results!D7` (1 cell). Explanation: E58. Representative cell: `D7`.

```excel
=m_w
```

- **Salt mass flow:** `Results!C8` (1 cell). Explanation: E58. Representative cell: `C8`.

```excel
=m_s
```

- **Salt mass flow:** `Results!D8` (1 cell). Explanation: E58. Representative cell: `D8`.

```excel
=m_s
```

- **Required UA (sum over segments):** `Results!C9` (1 cell). Explanation: E59. Representative cell: `C9`.

```excel
=SUM(Temperature_March!$P$5:$P$544)
```

- **Required UA (sum over segments):** `Results!D9` (1 cell). Explanation: E59. Representative cell: `D9`.

```excel
=SUM(Temperature_March!$P$5:$P$544)
```

- **Single LMTD (reference only):** `Results!C10` (1 cell). Explanation: E60. Representative cell: `C10`.

```excel
=(dT_cold-dT_hot)/LN(dT_cold/dT_hot)
```

- **Single LMTD (reference only):** `Results!D10` (1 cell). Explanation: E60. Representative cell: `D10`.

```excel
=(dT_cold-dT_hot)/LN(dT_cold/dT_hot)
```

- **True mean ΔT (use for sizing):** `Results!C11:C12` (2 cells). Explanation: E59, E60. Representative cell: `C11`.

```excel
=Q_SG/C9
```

- **True mean ΔT (use for sizing):** `Results!D11:D12` (2 cells). Explanation: E59, E60. Representative cell: `D11`.

```excel
=Q_SG/D9
```

- **Single-LMTD sizing error:** `Results!C13` (1 cell). Explanation: E60. Representative cell: `C13`.

```excel
=C12/C9-1
```

- **Single-LMTD sizing error:** `Results!D13` (1 cell). Explanation: E60. Representative cell: `D13`.

```excel
=D12/D9-1
```

- **Capacity ratio C_r (average):** `Results!C14` (1 cell). Explanation: E61. Representative cell: `C14`.

```excel
=C_w_avg/C_salt
```

- **Capacity ratio C_r (average):** `Results!D14` (1 cell). Explanation: E61. Representative cell: `D14`.

```excel
=C_w_avg/C_salt
```

- **Effectiveness ε (exact, enthalpy basis):** `Results!C15` (1 cell). Explanation: E62, E14. Representative cell: `C15`.

```excel
=Q_SG/(m_w*(INDEX(WP_h,INT(((T_salt_in)-WP_T0)/WP_dT)+1)+(((T_salt_in)-WP_T0)/WP_dT-INT(((T_salt_in)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((T_salt_in)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((T_salt_in)-WP_T0)/WP_dT)+1))-h_w_in)/1000)
```

- **Effectiveness ε (exact, enthalpy basis):** `Results!D15` (1 cell). Explanation: E62, E14. Representative cell: `D15`.

```excel
=Q_SG/(m_w*(INDEX(WP_h,INT(((T_salt_in)-WP_T0)/WP_dT)+1)+(((T_salt_in)-WP_T0)/WP_dT-INT(((T_salt_in)-WP_T0)/WP_dT))*(INDEX(WP_h,INT(((T_salt_in)-WP_T0)/WP_dT)+2)-INDEX(WP_h,INT(((T_salt_in)-WP_T0)/WP_dT)+1))-h_w_in)/1000)
```

- **Effectiveness ε (constant-c_p form):** `Results!C16` (1 cell). Explanation: E63. Representative cell: `C16`.

```excel
=Q_SG/(C_w_avg*(T_salt_in-T_w_in))
```

- **Effectiveness ε (constant-c_p form):** `Results!D16` (1 cell). Explanation: E63. Representative cell: `D16`.

```excel
=Q_SG/(C_w_avg*(T_salt_in-T_w_in))
```

- **NTU:** `Results!C17` (1 cell). Explanation: E63. Representative cell: `C17`.

```excel
=C9/C_w_avg
```

- **NTU:** `Results!D17` (1 cell). Explanation: E63. Representative cell: `D17`.

```excel
=D9/C_w_avg
```

- **ε predicted by counterflow ε–NTU formula:** `Results!C18` (1 cell). Explanation: E64. Representative cell: `C18`.

```excel
=(1-EXP(-C17*(1-C14)))/(1-C14*EXP(-C17*(1-C14)))
```

- **ε predicted by counterflow ε–NTU formula:** `Results!D18` (1 cell). Explanation: E64. Representative cell: `D18`.

```excel
=(1-EXP(-D17*(1-D14)))/(1-D14*EXP(-D17*(1-D14)))
```

- **NTU the formula says is needed:** `Results!C19` (1 cell). Explanation: E64. Representative cell: `C19`.

```excel
=LN((C16-1)/(C16*C14-1))/(C14-1)
```

- **NTU the formula says is needed:** `Results!D19` (1 cell). Explanation: E64. Representative cell: `D19`.

```excel
=LN((D16-1)/(D16*D14-1))/(D14-1)
```

- **Segments where water is the larger stream:** `Results!C20` (1 cell). Explanation: E65. Representative cell: `C20`.

```excel
=COUNTIF(Temperature_March!$T$5:$T$544,"Water")
```

- **Segments where water is the larger stream:** `Results!D20` (1 cell). Explanation: E65. Representative cell: `D20`.

```excel
=COUNTIF(Temperature_March!$T$5:$T$544,"Water")
```

- **Heated tube length L:** `Results!C22` (1 cell). Explanation: E66. Representative cell: `C22`.

```excel
=SUM(Model_Spreadsheet!$U$5:$U$544)
```

- **Heated tube length L:** `Results!D22` (1 cell). Explanation: E66. Representative cell: `D22`.

```excel
=SUM(Model_BestEstimate!$AY$5:$AY$544)
```

- **Overall U, contact-area basis:** `Results!C23` (1 cell). Explanation: E67. Representative cell: `C23`.

```excel
=C9*1000000/(N_steam*w_contact*C22)
```

- **Overall U, contact-area basis:** `Results!D23` (1 cell). Explanation: E67. Representative cell: `D23`.

```excel
=D9*1000000/(N_steam*w_contact*D22)
```

- **Overall U, steam-bore basis:** `Results!C24` (1 cell). Explanation: E67. Representative cell: `C24`.

```excel
=C9*1000000/(N_steam*PI()*D_i*C22)
```

- **Overall U, steam-bore basis:** `Results!D24` (1 cell). Explanation: E67. Representative cell: `D24`.

```excel
=D9*1000000/(N_steam*PI()*D_i*D22)
```

- **Contact heat-transfer area:** `Results!C25` (1 cell). Explanation: E66. Representative cell: `C25`.

```excel
=N_steam*w_contact*C22
```

- **Contact heat-transfer area:** `Results!D25` (1 cell). Explanation: E66. Representative cell: `D25`.

```excel
=N_steam*w_contact*D22
```

- **Steam-bore area:** `Results!C26` (1 cell). Explanation: E66. Representative cell: `C26`.

```excel
=N_steam*PI()*D_i*C22
```

- **Steam-bore area:** `Results!D26` (1 cell). Explanation: E66. Representative cell: `D26`.

```excel
=N_steam*PI()*D_i*D22
```

- **Total tube length (steam + salt tubes):** `Results!C27` (1 cell). Explanation: E67. Representative cell: `C27`.

```excel
=(N_steam+N_salt)*C22/1000
```

- **Total tube length (steam + salt tubes):** `Results!D27` (1 cell). Explanation: E67. Representative cell: `D27`.

```excel
=(N_steam+N_salt)*D22/1000
```

- **Mean salt velocity:** `Results!C29` (1 cell). Explanation: E68. Representative cell: `C29`.

```excel
=AVERAGE(Model_Spreadsheet!$K$5:$K$544)
```

- **Mean salt velocity:** `Results!D29` (1 cell). Explanation: E68. Representative cell: `D29`.

```excel
=AVERAGE(Model_BestEstimate!$F$5:$F$544)
```

- **Salt friction ΔP:** `Results!C30` (1 cell). Explanation: E68. Representative cell: `C30`.

```excel
=SUM(Model_Spreadsheet!$AF$5:$AF$544)/1000
```

- **Salt friction ΔP:** `Results!D30` (1 cell). Explanation: E68. Representative cell: `D30`.

```excel
=SUM(Model_BestEstimate!$BN$5:$BN$544)/1000
```

- **Salt minor losses:** `Results!C31` (1 cell). Explanation: E69. Representative cell: `C31`.

```excel
=K_salt*0.5*(rho_a+rho_b*(T_salt_in+T_salt_out)/2)*C29^2/1000
```

- **Salt minor losses:** `Results!D31` (1 cell). Explanation: E69. Representative cell: `D31`.

```excel
=K_salt*0.5*(rho_a+rho_b*(T_salt_in+T_salt_out)/2)*D29^2/1000
```

- **Salt total ΔP:** `Results!C32` (1 cell). Explanation: E69. Representative cell: `C32`.

```excel
=C30+C31
```

- **Salt total ΔP:** `Results!D32` (1 cell). Explanation: E69. Representative cell: `D32`.

```excel
=D30+D31
```

- **Salt hydraulic pump power:** `Results!C33` (1 cell). Explanation: E70. Representative cell: `C33`.

```excel
=C32*m_s/(rho_a+rho_b*(T_salt_in+T_salt_out)/2)
```

- **Salt hydraulic pump power:** `Results!D33` (1 cell). Explanation: E70. Representative cell: `D33`.

```excel
=D32*m_s/(rho_a+rho_b*(T_salt_in+T_salt_out)/2)
```

- **Water friction ΔP:** `Results!C34` (1 cell). Explanation: E68. Representative cell: `C34`.

```excel
=SUM(Model_Spreadsheet!$AC$5:$AC$544)/1000
```

- **Water friction ΔP:** `Results!D34` (1 cell). Explanation: E68. Representative cell: `D34`.

```excel
=SUM(Model_BestEstimate!$BK$5:$BK$544)/1000
```

- **Water gravity ΔP:** `Results!C35` (1 cell). Explanation: E68. Representative cell: `C35`.

```excel
=SUM(Model_Spreadsheet!$AD$5:$AD$544)/1000
```

- **Water gravity ΔP:** `Results!D35` (1 cell). Explanation: E68. Representative cell: `D35`.

```excel
=SUM(Model_BestEstimate!$BL$5:$BL$544)/1000
```

- **Water acceleration ΔP:** `Results!C36` (1 cell). Explanation: E71. Representative cell: `C36`.

```excel
=G_w^2*(1/INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1)+(((T_w_out)-WP_T0)/WP_dT-INT(((T_w_out)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1))-1/INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1)+(((T_w_in)-WP_T0)/WP_dT-INT(((T_w_in)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1)))/1000
```

- **Water acceleration ΔP:** `Results!D36` (1 cell). Explanation: E71. Representative cell: `D36`.

```excel
=G_w^2*(1/INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1)+(((T_w_out)-WP_T0)/WP_dT-INT(((T_w_out)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1))-1/INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1)+(((T_w_in)-WP_T0)/WP_dT-INT(((T_w_in)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1)))/1000
```

- **Water minor losses:** `Results!C37` (1 cell). Explanation: E72. Representative cell: `C37`.

```excel
=(K_w_in*0.5*G_w^2/INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1)+(((T_w_in)-WP_T0)/WP_dT-INT(((T_w_in)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1))+K_w_out*0.5*G_w^2/INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1)+(((T_w_out)-WP_T0)/WP_dT-INT(((T_w_out)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1)))/1000
```

- **Water minor losses:** `Results!D37` (1 cell). Explanation: E72. Representative cell: `D37`.

```excel
=(K_w_in*0.5*G_w^2/INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1)+(((T_w_in)-WP_T0)/WP_dT-INT(((T_w_in)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_in)-WP_T0)/WP_dT)+1))+K_w_out*0.5*G_w^2/INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1)+(((T_w_out)-WP_T0)/WP_dT-INT(((T_w_out)-WP_T0)/WP_dT))*(INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+2)-INDEX(WP_rho,INT(((T_w_out)-WP_T0)/WP_dT)+1)))/1000
```

- **Water total ΔP:** `Results!C38` (1 cell). Explanation: E72. Representative cell: `C38`.

```excel
=C34+C35+C36+C37
```

- **Water total ΔP:** `Results!D38` (1 cell). Explanation: E72. Representative cell: `D38`.

```excel
=D34+D35+D36+D37
```

- **Maximum steam-side wall temperature:** `Results!C40` (1 cell). Explanation: E73. Representative cell: `C40`.

```excel
=MAX(Model_Spreadsheet!$X$5:$X$544)
```

- **Maximum steam-side wall temperature:** `Results!D40` (1 cell). Explanation: E73. Representative cell: `D40`.

```excel
=MAX(Model_BestEstimate!$BB$5:$BB$544)
```

- **Minimum salt-side wall temperature:** `Results!C41` (1 cell). Explanation: E73. Representative cell: `C41`.

```excel
=MIN(Model_Spreadsheet!$Y$5:$Y$544)
```

- **Minimum salt-side wall temperature:** `Results!D41` (1 cell). Explanation: E73. Representative cell: `D41`.

```excel
=MIN(Model_BestEstimate!$BC$5:$BC$544)
```

- **Margin above salt freezing:** `Results!C42` (1 cell). Explanation: E73. Representative cell: `C42`.

```excel
=C41-T_freeze
```

- **Margin above salt freezing:** `Results!D42` (1 cell). Explanation: E73. Representative cell: `D42`.

```excel
=D41-T_freeze
```

- **Steam mass flux G:** `Results!C43` (1 cell). Explanation: E58. Representative cell: `C43`.

```excel
=G_w
```

- **Steam mass flux G:** `Results!D43` (1 cell). Explanation: E58. Representative cell: `D43`.

```excel
=G_w
```

- **Top of deterioration-prone zone:** `Results!D44` (1 cell). Explanation: E74. Representative cell: `D44`.

```excel
=_xlfn.MAXIFS(Model_BestEstimate!$AZ$5:$AZ$544,Model_BestEstimate!$BF$5:$BF$544,1)
```

- **q″/G in that zone (max):** `Results!D45` (1 cell). Explanation: E74. Representative cell: `D45`.

```excel
=_xlfn.MAXIFS(Model_BestEstimate!$BE$5:$BE$544,Model_BestEstimate!$BF$5:$BF$544,1)
```

- **q″/G in that zone (min):** `Results!D46` (1 cell). Explanation: E74. Representative cell: `D46`.

```excel
=_xlfn.MINIFS(Model_BestEstimate!$BE$5:$BE$544,Model_BestEstimate!$BF$5:$BF$544,1)
```

- **Bore heat flux in that zone (max):** `Results!D47` (1 cell). Explanation: E74. Representative cell: `D47`.

```excel
=_xlfn.MAXIFS(Model_BestEstimate!$BD$5:$BD$544,Model_BestEstimate!$BF$5:$BF$544,1)
```

- **Yamagata limiting heat flux 0.2 G^1.2:** `Results!D48` (1 cell). Explanation: E75. Representative cell: `D48`.

```excel
=0.2*G_w^1.2
```

- **Buoyancy parameter Bo* in zone (max):** `Results!D49` (1 cell). Explanation: E74. Representative cell: `D49`.

```excel
=_xlfn.MAXIFS(Model_BestEstimate!$BG$5:$BG$544,Model_BestEstimate!$BF$5:$BF$544,1)
```

- **Acceleration parameter K_v (max):** `Results!D50` (1 cell). Explanation: E74. Representative cell: `D50`.

```excel
=MAX(Model_BestEstimate!$BH$5:$BH$544)
```

- **Steam-tube hoop stress P D/(2t):** `Results!C51` (1 cell). Explanation: E76. Representative cell: `C51`.

```excel
=P_steam*D_i/(2*t_wall)
```

- **Steam-tube hoop stress P D/(2t):** `Results!D51` (1 cell). Explanation: E76. Representative cell: `D51`.

```excel
=P_steam*D_i/(2*t_wall)
```

### Charts

This sheet contains 5,406 formula cells in 14 audited families. The following entries cover all of them.

- **Reference-line coordinate:** `Charts!C6:C7` (2 cells). Explanation: E78. Representative cell: `C6`.

```excel
=T_freeze
```

- **Reference-line coordinate:** `Charts!C8:C9` (2 cells). Explanation: E78. Representative cell: `C8`.

```excel
=T_pc
```

- **Reference-line coordinate:** `Charts!D7` (1 cell). Explanation: E78. Representative cell: `D7`.

```excel
=Results!D22
```

- **Reference-line coordinate:** `Charts!D9` (1 cell). Explanation: E78. Representative cell: `D9`.

```excel
=Results!D22
```

- **Height, best estimate (m):** `Charts!R6:R545` (540 cells). Explanation: E77. Representative cell: `R6`.

```excel
=Model_BestEstimate!AZ5
```

- **Salt T at segment end (K):** `Charts!S6:S545` (540 cells). Explanation: E77. Representative cell: `S6`.

```excel
=Temperature_March!K5
```

- **Water T at segment end (K):** `Charts!T6:T545` (540 cells). Explanation: E77. Representative cell: `T6`.

```excel
=Temperature_March!C5
```

- **Steam-side wall T, best (K):** `Charts!U6:U545` (540 cells). Explanation: E77. Representative cell: `U6`.

```excel
=Model_BestEstimate!BB5
```

- **Duty fraction (-):** `Charts!V6:V545` (540 cells). Explanation: E79. Representative cell: `V6`.

```excel
=Temperature_March!I5
```

- **Actual ΔT at segment end (K):** `Charts!W6:W545` (540 cells). Explanation: E79. Representative cell: `W6`.

```excel
=Temperature_March!N5
```

- **ΔT single LMTD assumes (K):** `Charts!X6:X545` (540 cells). Explanation: E79. Representative cell: `X6`.

```excel
=Temperature_March!Q5
```

- **Water mean T (K):** `Charts!Y6:Y545` (540 cells). Explanation: E80. Representative cell: `Y6`.

```excel
=Temperature_March!D5
```

- **h_water spreadsheet (kW/m²K):** `Charts!Z6:Z545` (540 cells). Explanation: E80. Representative cell: `Z6`.

```excel
=Model_Spreadsheet!J5/1000
```

- **h_water Jackson (kW/m²K):** `Charts!AA6:AA545` (540 cells). Explanation: E80. Representative cell: `AA6`.

```excel
=Model_BestEstimate!AK5/1000
```

## Coverage verification

The register was checked against every formula cell in the workbook snapshot. Repeated calculations have been condensed only by exact relative-reference equivalence within each column, not by assuming that similar-looking formulas are interchangeable.

| Sheet | Formula cells | Audited families |
|---|---:|---:|
| README | 0 | 0 |
| Inputs | 26 | 26 |
| Results | 79 | 77 |
| Charts | 5,406 | 14 |
| Temperature_March | 16,200 | 34 |
| Model_Spreadsheet | 17,280 | 33 |
| Model_BestEstimate | 35,640 | 68 |
| Studies | 0 | 0 |
| Water_Properties | 0 | 0 |
| Total | 74,631 | 252 |

The narrative contains E01–E84, including the static-study generating relationships. All 252 formula families have equation cross-references; the no-formula sheets are explicitly accounted for, and the workbook itself was not modified.

Workbook snapshot SHA-256:

```text
ca8a8b58b00096eea48a900628a55213c1a83ee9337ceed96d1cbd9f02a8daa3
```
