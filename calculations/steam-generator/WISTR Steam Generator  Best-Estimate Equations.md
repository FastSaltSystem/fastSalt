# WISTR Steam Generator: Best-Estimate Equations

Numerical results use the workbook's existing 500 MW thermal case at 24 MPa, with 6,536 steam tubes, 20 mm inside diameter, and 2 mm walls. These are the thermal-workbook inputs, not the later thicker-wall design.

For equations that vary along the tube, results refer to **segment 1**: bulk water heats from 560 to 560.5 K, with mean 560.25 K. Final-pass values are used unless a pass is labeled; whole-generator equations show totals or extrema, and chart equations show their specified coordinates.

An arrow beside an equation gives its numerical evaluation with units; values are rounded, so substituting the printed numbers may differ slightly from the workbook's full precision. “Change from sponsor” remains blank when the relationship is unchanged.

## Plant duty, energy balance, and geometry

### Plant thermal-to-electric efficiency (E01)

\[
\eta_{\mathrm{plant}}=\frac{P_e}{P_{\mathrm{th}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
\eta_{\mathrm{plant}}\approx 0.4\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(P_e\) is plant electric output (600 MW); \(P_{\mathrm{th}}\) is plant thermal output (1,500 MW); \(\eta_{\mathrm{plant}}\) is their dimensionless ratio (0.40 = 40%).

- **Change from sponsor:**

### Thermal duty and electric allocation per SG (E02)

\[
Q_{\mathrm{SG}}=\frac{P_{\mathrm{th}}}{N_{\mathrm{gen}}},
\qquad P_{e,\mathrm{share}}=\eta_{\mathrm{plant}}Q_{\mathrm{SG}}
\qquad\Longrightarrow\qquad
\begin{gathered}
Q_{\mathrm{SG}}\approx 500\;\mathrm{MW}\\
P_{e,\mathrm{share}}\approx 200\;\mathrm{MW}
\end{gathered}
\]

- **Variables:** \(N_{\mathrm{gen}}\) is the number of generators (3); \(Q_{\mathrm{SG}}\) is thermal duty per generator (MW); \(P_{e,\mathrm{share}}\) is its allocated electric output (MW); \(\eta_{\mathrm{plant}}\) is plant efficiency.

- **Change from sponsor:**

### End temperature approaches and march step (E03)

\[
\Delta T_c=T_{s,\mathrm{out}}-T_{b,\mathrm{in}},\qquad
\Delta T_h=T_{s,\mathrm{in}}-T_{b,\mathrm{out}},\qquad
\delta T_b=\frac{T_{b,\mathrm{out}}-T_{b,\mathrm{in}}}{N_{\mathrm{seg}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta T_c\approx 250\;\mathrm{K}\\
\Delta T_h\approx 60\;\mathrm{K}\\
\delta T_b\approx 0.5\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(T_{s,\mathrm{in}},T_{s,\mathrm{out}}\) are salt inlet/outlet temperatures (890 and 810 K); \(T_{b,\mathrm{in}},T_{b,\mathrm{out}}\) are bulk-water inlet/outlet temperatures (560 and 830 K); \(\Delta T_c,\Delta T_h\) are cold-/hot-end approaches (K); \(N_{\mathrm{seg}}=540\); \(\delta T_b\) is the temperature increment (K).

- **Change from sponsor:**

### Water/steam mass flow (E05)

\[
\dot m_w=\frac{Q}{H_{\mathrm{out}}-H_{\mathrm{in}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
\dot m_w\approx 237.223\;\mathrm{kg/s}
\end{gathered}
\]

- **Variables:** \(\dot m_w\) is total water mass flow (kg/s); \(Q\) is SG duty; \(H_{\mathrm{in}},H_{\mathrm{out}}\) are specific enthalpies (1,264.677 and 3,372.395 kJ/kg). Convert MW to kW when using kJ/kg enthalpies.

- **Change from sponsor:**

### Salt enthalpy change and salt flow (E06)

\[
\Delta H_s=\int_{T_{s,\mathrm{out}}}^{T_{s,\mathrm{in}}}(a_c+b_cT)\,dT
=a_c(T_{s,\mathrm{in}}-T_{s,\mathrm{out}})
+\frac{b_c}{2}(T_{s,\mathrm{in}}^2-T_{s,\mathrm{out}}^2),
\qquad \dot m_s=\frac{Q}{\Delta H_s}
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta H_s\approx 81030.4\;\mathrm{J/kg}\\
\dot m_s\approx 6170.52\;\mathrm{kg/s}
\end{gathered}
\]

- **Variables:** \(a_c=1437.88\) J/(kg·K) and \(b_c=-0.5\) J/(kg·K²) define the supplied salt heat capacity; \(T\) is salt temperature (K); \(\Delta H_s\) is the salt enthalpy change (J/kg); \(\dot m_s\) is total salt flow (kg/s); \(Q\) must be in W when \(\Delta H_s\) is in J/kg.

- **Change from sponsor:** Uses the integrated salt energy balance with the supplied temperature-dependent heat capacity.

### Average heat-capacity rates (E07)

\[
C_{s,\mathrm{avg}}=\frac{Q}{T_{s,\mathrm{in}}-T_{s,\mathrm{out}}},
\qquad
C_{w,\mathrm{avg}}=\frac{Q}{T_{b,\mathrm{out}}-T_{b,\mathrm{in}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
C_{s,\mathrm{avg}}\approx 6.25\;\mathrm{MW/K}\\
C_{w,\mathrm{avg}}\approx 1.85185\;\mathrm{MW/K}
\end{gathered}
\]

- **Variables:** \(C_{s,\mathrm{avg}},C_{w,\mathrm{avg}}\) are average salt/water heat-capacity rates (MW/K); \(Q\) is duty (MW); the denominator is each fluid's terminal-temperature change (K). These are averages, not the strongly varying local water capacity rate.

- **Change from sponsor:** Adds average capacity-rate reporting for the effectiveness and NTU comparisons.

### Reference cycle work per kilogram (E08)

\[
w_{\mathrm{net,ref}}=\eta_R(H_{\mathrm{out}}-H_{\mathrm{in}})
\qquad\Longrightarrow\qquad
\begin{gathered}
w_{\mathrm{net,ref}}\approx 927.396\;\mathrm{kJ/kg}
\end{gathered}
\]

- **Variables:** \(w_{\mathrm{net,ref}}\) is assumed net cycle work per kilogram (kJ/kg); \(\eta_R=0.44\) is the reference cycle efficiency, distinct from the 0.40 plant efficiency; \(H_{\mathrm{out}}-H_{\mathrm{in}}\) is the water enthalpy rise (kJ/kg).

- **Change from sponsor:** Adds a reference cycle-work estimate; it is not part of the heat-transfer sizing.

### Tube counts (E09)

\[
N_s=\operatorname{ROUND}(r_sN_w,0),\qquad N_a=N_w-N_s
\qquad\Longrightarrow\qquad
\begin{gathered}
N_s\approx 4902\;\text{tubes}\\
N_a\approx 1634\;\text{tubes}
\end{gathered}
\]

- **Variables:** \(N_w,N_s,N_a\) are steam-, salt-, and air-tube counts; \(N_w=6536\); \(r_s=0.75\) is the salt/steam tube ratio; ROUND selects the nearest integer.

- **Change from sponsor:**

### Tube dimensions and flow area (E10)

\[
D_o=D_i+2t,\quad A_f=\frac{\pi D_i^2}{4},\quad
r_i=\frac{D_i}{2},\quad r_m=\frac{D_i+t}{2}
\qquad\Longrightarrow\qquad
\begin{gathered}
D_o\approx 0.024\;\mathrm{m}\\
A_f\approx 3.14159\times10^{-4}\;\mathrm{m^2}\\
r_i\approx 0.01\;\mathrm{m}\\
r_m\approx 0.011\;\mathrm{m}
\end{gathered}
\]

- **Variables:** \(D_i=0.020\) m and \(t=0.002\) m are inside diameter and wall thickness; \(D_o\) is outside diameter (m); \(A_f\) is bore flow area (m²); \(r_i,r_m\) are inner and mid-wall radii (m).

- **Change from sponsor:**

### Assumed contact width (E11)

\[
w=\frac{\pi D_o}{2}
\qquad\Longrightarrow\qquad
\begin{gathered}
w\approx 0.0376991\;\mathrm{m}
\end{gathered}
\]

- **Variables:** \(w\) is assumed contact width, equivalent to interface area per metre of tube (m); \(D_o\) is outside diameter (m). This assumes a total half-circumference contact arc, not undeformed round tubes touching along a line.

- **Change from sponsor:**

### Flow per tube and steam mass flux (E12)

\[
\dot m_{w,t}=\frac{\dot m_w}{N_w},\qquad
\dot m_{s,t}=\frac{\dot m_s}{N_s},\qquad
G_w=\frac{\dot m_{w,t}}{A_f}
\qquad\Longrightarrow\qquad
\begin{gathered}
\dot m_{w,t}\approx 0.0362949\;\mathrm{kg/s}\\
\dot m_{s,t}\approx 1.25878\;\mathrm{kg/s}\\
G_w\approx 115.53\;\mathrm{kg/(m^2\,s)}
\end{gathered}
\]

- **Variables:** \(\dot m_{w,t},\dot m_{s,t}\) are water/salt mass flows per tube (kg/s); \(\dot m_w,\dot m_s\) are total flows; \(N_w,N_s\) are counts; \(A_f\) is flow area (m²); \(G_w\) is water mass flux (kg/(m²·s)).

- **Change from sponsor:**

### Directly backed salt-perimeter fraction (E13)

\[
f_{\mathrm{backed}}=\frac23
\qquad\Longrightarrow\qquad
\begin{gathered}
f_{\mathrm{backed}}\approx 0.666667\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(f_{\mathrm{backed}}\) is the dimensionless fraction of the salt-tube perimeter directly backed by tube contacts.

- **Change from sponsor:** Adds the directly backed perimeter fraction used by the salt-side fin model.

## Temperature and energy march

### Segment index and water-temperature boundaries (E16)

\[
i_1=1,\quad i_{r}=i_{r-1}+1;\qquad
T_{b,0}=T_{b,\mathrm{in}},\quad T_{b,i}=T_{b,i-1}+\delta T_b,\quad
T_{b,m,i}=\frac{T_{b,i-1}+T_{b,i}}2
\qquad\Longrightarrow\qquad
\begin{gathered}
i\approx 1\;\text{(segment index)}\\
T_{b,0}\approx 560\;\mathrm{K}\\
T_{b,1}\approx 560.5\;\mathrm{K}\\
T_{b,m,1}\approx 560.25\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(i\) is segment number; \(r\) labels the row in the recurrence; \(T_{b,i-1},T_{b,i}\) are segment inlet/outlet water temperatures (K); \(T_{b,m,i}\) is their mean; \(\delta T_b=0.5\) K. The numerical result is segment 1.

- **Change from sponsor:**

### Segment enthalpies and segment heat (E17)

\[
H_{i-1}=\mathcal I_H(T_{b,i-1}),\quad H_i=\mathcal I_H(T_{b,i}),\qquad
\Delta Q_i=\dot m_w(H_i-H_{i-1})
\qquad\Longrightarrow\qquad
\begin{gathered}
H_0\approx 1264.68\;\mathrm{kJ/kg}\\
H_1\approx 1267.19\;\mathrm{kJ/kg}\\
\Delta Q_1\approx 0.595067\;\mathrm{MW}
\end{gathered}
\]

- **Variables:** \(H_{i-1},H_i\) are endpoint enthalpies; \(\mathcal I_H(T)\) means the supplied enthalpy at temperature \(T\); \(\dot m_w\) is total water flow (kg/s); \(\Delta Q_i\) is the whole-generator heat-transfer rate in the segment. Enthalpy in kJ/kg gives kW before conversion to MW.

- **Change from sponsor:**

### Cumulative heat and duty fraction (E18)

\[
Q_{\mathrm{cum},0}=0,\quad
Q_{\mathrm{cum},i}=Q_{\mathrm{cum},i-1}+\Delta Q_i,\qquad
F_i=\frac{Q_{\mathrm{cum},i}}{Q}
\qquad\Longrightarrow\qquad
\begin{gathered}
Q_{\mathrm{cum},0}\approx 0\;\mathrm{MW}\\
Q_{\mathrm{cum},1}\approx 0.595067\;\mathrm{MW}\\
F_1\approx 0.00119013\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(Q_{\mathrm{cum},i}\) is cumulative heat-transfer rate from the cold end through segment \(i\) (MW); \(\Delta Q_i\) is segment duty; \(Q=500\) MW; \(F_i\) is the dimensionless cumulative-duty fraction. For the first segment, cumulative and segment duty are equal.

- **Change from sponsor:**

### Salt temperature from cumulative energy (E19)

\[
e_i=\frac{Q_{\mathrm{cum},i}}{\dot m_s},
\qquad T_{s,0}=T_{s,\mathrm{out}}
\qquad\Longrightarrow\qquad
\begin{gathered}
e_1\approx 96.4371\;\mathrm{J/kg}\\
T_{s,0}\approx 810\;\mathrm{K}
\end{gathered}
\]

\[
X_i=a_cT_{s,0}+\frac{b_c}{2}T_{s,0}^2+e_i,\qquad
T_{s,i}=\frac{-a_c+\sqrt{a_c^2+2b_cX_i}}{b_c},
\qquad T_{s,m,i}=\frac{T_{s,i-1}+T_{s,i}}2
\qquad\Longrightarrow\qquad
\begin{gathered}
X_1\approx 1.00075\times10^{6}\;\mathrm{J/kg}\\
T_{s,1}\approx 810.093\;\mathrm{K}\\
T_{s,m,1}\approx 810.047\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(e_i\) is cumulative heat per unit salt mass (J/kg); \(T_{s,0}\) is the cold-end salt temperature (K); \(X_i\) is the enthalpy-polynomial intermediate (J/kg); \(a_c,b_c\) are E06's coefficients; \(T_{s,i}\) and \(T_{s,m,i}\) are salt segment-end and mean temperatures (K).

- **Change from sponsor:** Solves the integrated salt energy balance rather than the legacy incremental salt-temperature update.

### Segment driving-temperature differences and local LMTD (E20)

\[
\Delta T_{i,a}=T_{s,i-1}-T_{b,i-1},\qquad
\Delta T_{i,b}=T_{s,i}-T_{b,i},
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta T_{1,a}\approx 250\;\mathrm{K}\\
\Delta T_{1,b}\approx 249.593\;\mathrm{K}
\end{gathered}
\]

\[
\Delta T_{\mathrm{lm},i}=
\begin{cases}
\Delta T_{i,a},&|\Delta T_{i,a}-\Delta T_{i,b}|<10^{-9}\ {\rm K},\\
\dfrac{\Delta T_{i,a}-\Delta T_{i,b}}
{\ln(\Delta T_{i,a}/\Delta T_{i,b})},&\text{otherwise}.
\end{cases}
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta T_{\mathrm{lm},1}\approx 249.797\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(\Delta T_{i,a},\Delta T_{i,b}\) are salt-minus-water differences at the two segment ends (K); \(\Delta T_{\mathrm{lm},i}\) is their logarithmic mean (K); \(\ln\) is natural logarithm. The near-equal branch avoids dividing zero by zero.

- **Change from sponsor:**

### Required segment conductance (E21)

\[
(UA)_i=\frac{\Delta Q_i}{\Delta T_{\mathrm{lm},i}}
\qquad\Longrightarrow\qquad
\begin{gathered}
(UA)_1\approx 0.00238221\;\mathrm{MW/K}
\end{gathered}
\]

- **Variables:** \((UA)_i\) is required segment thermal conductance (MW/K); \(\Delta Q_i\) is segment duty (MW); \(\Delta T_{\mathrm{lm},i}\) is segment LMTD (K).

- **Change from sponsor:**

### Constant-capacity comparison line (E22)

\[
\Delta T_{\mathrm{linear},i}=\Delta T_c+(\Delta T_h-\Delta T_c)F_i
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta T_{\mathrm{linear},1}\approx 249.774\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(\Delta T_{\mathrm{linear},i}\) is the constant-capacity comparison temperature difference (K); \(\Delta T_c,\Delta T_h\) are terminal approaches; \(F_i\) is cumulative-duty fraction. This comparison does not determine segment length.

- **Change from sponsor:** Adds a constant-capacity comparison curve; it is not used for sizing.

### Segment effective heat capacity, capacity rate, and comparison flag (E23)

\[
c_{p,\mathrm{seg},i}=\frac{H_i-H_{i-1}}{T_{b,i}-T_{b,i-1}},\qquad
C_{w,i}=\dot m_w c_{p,\mathrm{seg},i}
\qquad\Longrightarrow\qquad
\begin{gathered}
c_{p,\mathrm{seg},1}\approx 5.01694\;\mathrm{kJ/(kg\,K)}\\
C_{w,1}\approx 1.19013\;\mathrm{MW/K}
\end{gathered}
\]

\[
\mathrm{flag}_i=
\begin{cases}
\text{“Water”},&C_{w,i}>C_{s,\mathrm{avg}},\\
\text{“Salt”},&\text{otherwise}.
\end{cases}
\qquad\Longrightarrow\qquad
\begin{gathered}
\mathrm{flag}_1=\text{Salt (text; no units)}
\end{gathered}
\]

- **Variables:** \(c_{p,\mathrm{seg},i}\) is the secant heat capacity over one water-temperature interval (kJ/(kg·K)); \(C_{w,i}\) is local water capacity rate (MW/K); \(C_{s,\mathrm{avg}}\) is the average salt capacity rate. The text flag names the larger-capacity stream, not the minimum-capacity stream.

- **Change from sponsor:** Adds explicit local capacity-rate and stream-comparison diagnostics.

## Shared flow and heat-transfer relationships

### Data transfer and per-tube duty (E25)

\[
(i,T_b,T_s,\Delta T_{\mathrm{lm}})_{\mathrm{model}}
=(i,T_{b,m},T_{s,m},\Delta T_{\mathrm{lm}})_{\mathrm{TM}},
\qquad \Delta Q_{t,i}=\frac{\Delta Q_i}{N_w}
\qquad\Longrightarrow\qquad
\begin{gathered}
i\approx 1\;\text{(segment index)}\\
T_b\approx 560.25\;\mathrm{K}\\
T_s\approx 810.047\;\mathrm{K}\\
\Delta T_{\mathrm{lm}}\approx 249.797\;\mathrm{K}\\
\Delta Q_{t,1}\approx 91.0446\;\mathrm{W}
\end{gathered}
\]

- **Variables:** \(i\) is segment index; \(T_b,T_s\) are mean bulk temperatures (K); \(\Delta T_{\mathrm{lm}}\) is local driving difference; \(\Delta Q_{t,i}\) is heat-transfer rate in one steam tube's segment (W); \(\Delta Q_i\) is total segment duty; \(N_w\) is steam-tube count. Subscripts model and TM denote linked calculation stages, not different physical states.

- **Change from sponsor:**

### Velocity and Reynolds number (E26)

\[
v=\frac{\dot m_t}{\rho A_f}=\frac{G}{\rho},\qquad
Re=\frac{\rho vD_i}{\mu}=\frac{GD_i}{\mu}
\qquad\Longrightarrow\qquad
\begin{gathered}
v_b\approx 0.1512\;\mathrm{m/s}\\
Re_b\approx 24004.8\;\text{(dimensionless)}\\
v_s\approx 2.41925\;\mathrm{m/s}\\
Re_s\approx 25655.9\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(v\) is speed (m/s); \(\dot m_t\) is per-tube flow (kg/s); \(\rho\) is density (kg/m³); \(A_f\) is flow area (m²); \(G\) is mass flux; \(D_i\) is inside diameter (m); \(\mu\) is dynamic viscosity (Pa·s); \(Re\) is dimensionless. Results are shown for both water (\(b\)) and salt (\(s\)).

- **Change from sponsor:**

### Prandtl number (E27)

\[
Pr=\frac{c_p\mu}{k}
\qquad\Longrightarrow\qquad
\begin{gathered}
Pr_b\approx 0.812084\;\text{(dimensionless)}\\
Pr_s\approx 7.28957\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(Pr\) is the dimensionless Prandtl number; \(c_p\) is specific heat (J/(kg·K)); \(\mu\) is viscosity (Pa·s); \(k\) is fluid conductivity (W/(m·K)). Use point bulk \(c_p\) for Jackson's water-side value.

- **Change from sponsor:**

### Nusselt number to heat-transfer coefficient (E28)

\[
h=\frac{Nu\,k}{D_i}
\qquad\Longrightarrow\qquad
\begin{gathered}
h_w\approx 1838.05\;\mathrm{W/(m^2\,K)}\\
h_s\approx 4150.84\;\mathrm{W/(m^2\,K)}
\end{gathered}
\]

- **Variables:** \(Nu\) is dimensionless Nusselt number; \(k\) is fluid conductivity (W/(m·K)); \(D_i\) is inside diameter (m); \(h\) is convection coefficient (W/(m²·K)). The water result uses the final pass; the salt result uses Gnielinski.

- **Change from sponsor:**

## Best-estimate salt convection

### Petukhov-type factor used inside Gnielinski (E33)

\[
f_P=(0.79\ln Re_s-1.64)^{-2}
\qquad\Longrightarrow\qquad
\begin{gathered}
f_P\approx 0.0245635\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(f_P\) is the dimensionless Petukhov-type factor used inside Gnielinski; \(Re_s\) is salt Reynolds number; \(\ln\) is natural logarithm. This is distinct from the hydraulic Darcy factor used later.

- **Change from sponsor:** Introduces the friction-factor term used within the Gnielinski salt-convection correlation.

### Gnielinski salt correlation (E34)

\[
Nu_s=
\frac{(f_P/8)(Re_s-1000)Pr_s}
{1+12.7\sqrt{f_P/8}(Pr_s^{2/3}-1)},\qquad
h_s=\frac{Nu_sk_s}{D_i}
\qquad\Longrightarrow\qquad
\begin{gathered}
Nu_s\approx 187.58\;\text{(dimensionless)}\\
h_s\approx 4150.84\;\mathrm{W/(m^2\,K)}
\end{gathered}
\]

- **Variables:** \(Nu_s,Re_s,Pr_s,f_P\) are dimensionless; \(k_s\) is salt conductivity (W/(m·K)); \(D_i\) is inside diameter; \(h_s\) is salt-side convection coefficient (W/(m²·K)).

- **Change from sponsor:** Replaces the sponsor salt-convection correlation with Gnielinski.

## Best-estimate water convection and wall-temperature passes

### First-pass wall-temperature assumption (E35)

\[
T_{w,1,1}=T_{b,1}+\Delta T_{\mathrm{guess}},
\qquad
T_{w,1,i}=T_{w,\mathrm{final},i-1}+(T_{b,i}-T_{b,i-1})\quad(i>1)
\qquad\Longrightarrow\qquad
\begin{gathered}
T_{w,1,1}\approx 656.25\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(T_{w,1,i}\) is the first-pass assumed wall temperature in segment \(i\) (K); \(T_{w,\mathrm{final},i-1}\) is the preceding segment's final wall temperature; \(\Delta T_{\mathrm{guess}}=96\) K is the initial offset. The shown result is the first-segment initialization.

- **Change from sponsor:** Adds a wall-temperature starting estimate because Jackson depends on wall conditions.

### Wall-fluid density, enthalpy, and secant heat capacity (E36)

\[
\rho_{w,p}=\mathcal I_\rho(T_{w,p}),\qquad H_{w,p}=\mathcal I_H(T_{w,p}),
\qquad
\bar c_{p,p}=\frac{H_{w,p}-H_b}{T_{w,p}-T_b}
\qquad\Longrightarrow\qquad
\begin{gathered}
\rho_{w,2}\approx 238.872\;\mathrm{kg/m^3}\\
H_{w,2}\approx 2304.54\;\mathrm{kJ/kg}\\
\bar c_{p,2}\approx 10.8078\;\mathrm{kJ/(kg\,K)}
\end{gathered}
\]

\[
\bar c_p=\frac{1}{T_w-T_b}\int_{T_b}^{T_w}c_p(T)\,dT
\qquad\Longrightarrow\qquad
\begin{gathered}
\bar c_{p,2}\approx 10.8078\;\mathrm{kJ/(kg\,K)}
\end{gathered}
\]

- **Variables:** \(p=1,2\) identifies the wall-temperature pass; \(\rho_{w,p}\) is fluid density evaluated at that pass's wall temperature (kg/m³); \(H_{w,p},H_b\) are specific enthalpies (kJ/kg); \(\bar c_{p,p}\) is their secant heat capacity over the wall-to-bulk temperature interval. \(\mathcal I\) denotes a supplied-property lookup. Results below use pass 2; the integral is an equivalent definition at fixed pressure.

- **Change from sponsor:** Adds wall-temperature fluid properties and a wall-to-bulk secant heat capacity for Jackson.

### Jackson exponent (E37)

\[
n=
\begin{cases}
0.4,&T_b<T_w\le T_{\mathrm{pc}}\ \text{or}\ T_b\ge1.2T_{\mathrm{pc}},\\
0.4+0.2(T_w/T_{\mathrm{pc}}-1),&T_b\le T_{\mathrm{pc}}<T_w,\\
0.4+0.2(T_w/T_{\mathrm{pc}}-1)[1-5(T_b/T_{\mathrm{pc}}-1)],
&\text{otherwise}.
\end{cases}
\qquad\Longrightarrow\qquad
\begin{gathered}
n_2\approx 0.400601\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(n\) is Jackson's dimensionless heat-capacity exponent; \(T_b,T_w\) are bulk and assumed wall temperatures (K); \(T_{\mathrm{pc}}=654.38\) K is the workbook's pseudo-critical temperature. The result uses the pass-2 wall assumption.

- **Change from sponsor:** Adds Jackson’s temperature-regime-dependent heat-capacity exponent.

### Jackson Nusselt number and water-side coefficient (E38)

\[
Nu_J=J_CRe_b^{J_{Re}}Pr_b^{J_{Pr}}
\left(\frac{\rho_w}{\rho_b}\right)^{J_\rho}
\left(\frac{\bar c_p}{c_{p,b}}\right)^n,\qquad
h_J=\frac{Nu_Jk_b}{D_i}
\qquad\Longrightarrow\qquad
\begin{gathered}
Nu_{J,2}\approx 61.819\;\text{(dimensionless)}\\
h_{J,2}\approx 1838.05\;\mathrm{W/(m^2\,K)}
\end{gathered}
\]

\[
J_C=0.0183,\qquad J_{Re}=0.82,\qquad
J_{Pr}=0.5,\qquad J_\rho=0.3
\qquad\Longrightarrow\qquad
\begin{gathered}
J_C,J_{Re},J_{Pr},J_\rho=\text{dimensionless constants}
\end{gathered}
\]

- **Variables:** \(Nu_J\) is dimensionless; \(Re_b,Pr_b\) use bulk properties; \(\rho_w/\rho_b\) is the wall-to-bulk density ratio; \(\bar c_p/c_{p,b}\) is the secant-to-bulk heat-capacity ratio; \(n\) is E37's exponent. \(J_C,J_{Re},J_{Pr},J_\rho\) are fitted dimensionless constants; \(k_b\) is bulk conductivity; \(h_J\) is water-side convection coefficient. Results use pass 2 before the optional multiplier, which equals 1 in this case.

- **Change from sponsor:** Replaces the sponsor water-side correlation with Jackson, including wall-to-bulk density and heat-capacity corrections.

### Optional deterioration sensitivity multiplier (E39)

\[
M_i=
\begin{cases}
M_{\mathrm{HTD}},&T_b<T_{\mathrm{pc}}<T_{w,2},\\
1,&\text{otherwise},
\end{cases}
\qquad h_{w,2}=M_i h_{J,2}
\qquad\Longrightarrow\qquad
\begin{gathered}
M_1\approx 1\;\text{(dimensionless)}\\
h_{w,2}\approx 1838.05\;\mathrm{W/(m^2\,K)}
\end{gathered}
\]

- **Variables:** \(M_{\mathrm{HTD}}=1\) is the selected deterioration multiplier; \(M_i\) is the applied segment multiplier; \(T_{w,2}\) is the assumed pass-2 wall temperature; \(h_{J,2}\) is Jackson's coefficient before the multiplier; \(h_{w,2}\) is the resulting coefficient (W/(m²·K)).

- **Change from sponsor:** Adds an optional deterioration sensitivity multiplier; it is not a predictive deterioration correlation.

### Temperature-dependent metal conductivity (E40)

\[
T_{m,p}^{*}=\frac{T_{w,p}+T_s}{2},\qquad k_{m,p}=\mathcal I_{k_m}(T_{m,p}^{*})
\qquad\Longrightarrow\qquad
\begin{gathered}
T_{m,2}^{*}\approx 733.197\;\mathrm{K}\\
k_{m,2}\approx 20.298\;\mathrm{W/(m\,K)}
\end{gathered}
\]

- **Variables:** \(T_{m,p}^{*}\) is the representative metal temperature (K), formed from the pass-\(p\) assumed steam-wall temperature and bulk salt temperature; \(k_{m,p}\) is interpolated steel conductivity (W/(m·K)). \(\mathcal I_{k_m}\) denotes the metal-conductivity lookup; results use pass 2.

- **Change from sponsor:** Replaces the fixed 19 W/(m·K) steel conductivity with temperature-dependent conductivity.

## Fin efficiency, contact resistance, and the full resistance network

### Fin parameter, half-arc length, and efficiency (E41)

\[
m_f=\sqrt{\frac{h}{k_mt}},\qquad
\ell_f=\frac{r_m\theta}{2},\qquad
\eta_f=\frac{\tanh(m_f\ell_f)}{m_f\ell_f},\qquad
\theta=\theta_{\deg}\frac{\pi}{180}
\qquad\Longrightarrow\qquad
\begin{gathered}
m_{f,w}\approx 212.783\;\mathrm{m^{-1}}\\
m_{f,s}\approx 319.762\;\mathrm{m^{-1}}\\
\theta_{60}\approx 1.0472\;\mathrm{rad}\\
\theta_{120}\approx 2.0944\;\mathrm{rad}\\
\ell_{60}\approx 0.00575959\;\mathrm{m}\\
\ell_{120}\approx 0.0115192\;\mathrm{m}\\
\eta_{w,60}\approx 0.686456\;\text{(dimensionless)}\\
\eta_{w,120}\approx 0.401964\;\text{(dimensionless)}\\
\eta_{s,60}\approx 0.516349\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(m_f\) is the fin parameter (1/m); \(h\) is the relevant fluid coefficient; \(k_m\) is steel conductivity; \(t\) is wall thickness; \(r_m\) is mid-wall radius; \(\theta\) is arc angle (rad); \(\ell_f\) is half the arc length (m); \(\eta_f\) is dimensionless efficiency. Water has 60° and 120° arcs; salt has a 60° arc. All results use final-pass values.

- **Change from sponsor:** Adds fin efficiency for circumferential wall regions away from direct tube contact.

### Effective water-side perimeter (E42)

\[
P_{w,\mathrm{eff}}=r_i\left[\pi+\eta_1\theta_1+\eta_2\theta_2\right]
\qquad\Longrightarrow\qquad
\begin{gathered}
P_{w,\mathrm{eff}}\approx 0.0470232\;\mathrm{m}
\end{gathered}
\]

- **Variables:** \(P_{w,\mathrm{eff}}\) is effective water-side perimeter (m); \(r_i\) is inner radius; \(\eta_1,\eta_2\) are the 60° and 120° fin efficiencies; \(\theta_1,\theta_2\) are those arc angles in radians; \(\pi r_i\) is directly backed perimeter.

- **Change from sponsor:** Replaces the contact-width-only water-film area with a direct-contact plus fin-weighted effective perimeter.

### Effective salt perimeter allocated to one steam tube (E43)

\[
P_{s,\mathrm{eff}}=
\frac{N_s}{N_w}\,2\pi r_i
\left[f_{\mathrm{backed}}+(1-f_{\mathrm{backed}})\eta_s\right]
\qquad\Longrightarrow\qquad
\begin{gathered}
P_{s,\mathrm{eff}}\approx 0.0395267\;\mathrm{m}
\end{gathered}
\]

- **Variables:** \(P_{s,\mathrm{eff}}\) is effective salt perimeter allocated to one steam tube (m); \(N_s/N_w\) is the count ratio; \(r_i\) is inner radius; \(f_{\mathrm{backed}}=2/3\); \(\eta_s\) is salt fin efficiency.

- **Change from sponsor:** Adds a fin-weighted salt perimeter allocated by the salt-to-steam tube-count ratio.

### Water and salt film resistance factors (E44)

\[
R'_w=\frac1{h_wP_{w,\mathrm{eff}}},\qquad
R'_s=\frac1{h_sP_{s,\mathrm{eff}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
R'_w\approx 0.0115699\;\mathrm{K\,m/W}\\
R'_s\approx 0.00609499\;\mathrm{K\,m/W}
\end{gathered}
\]

- **Variables:** \(R'_w,R'_s\) are water/salt film resistance factors (K·m/W); \(h_w,h_s\) are convection coefficients; \(P_{w,\mathrm{eff}},P_{s,\mathrm{eff}}\) are effective perimeters (m). A prime denotes the resistance factor used with heat per unit tube length, not a derivative.

- **Change from sponsor:** Uses separate effective water and salt perimeters rather than the common contact-width film-area approximation.

### Two metal walls in series (E45)

\[
R'_m=\frac{2t}{k_mw}
\qquad\Longrightarrow\qquad
\begin{gathered}
R'_m\approx 0.00522729\;\mathrm{K\,m/W}
\end{gathered}
\]

- **Variables:** \(R'_m\) is the resistance factor of both metal walls in series (K·m/W); \(t\) is each wall's thickness (m); \(k_m\) is steel conductivity; \(w\) is contact width (m).

- **Change from sponsor:** Uses temperature-dependent steel conductivity and expresses the two-wall resistance per axial length.

### Tube-to-tube contact resistance (E46)

\[
R'_c=
\begin{cases}
0,&\text{Excel input }h_c=0\text{ (perfect-contact switch)},\\
1/(h_cw),&h_c>0.
\end{cases}
\qquad\Longrightarrow\qquad
\begin{gathered}
R'_c\approx 0.00716914\;\mathrm{K\,m/W}
\end{gathered}
\]

- **Variables:** \(R'_c\) is contact resistance factor (K·m/W); \(h_c=3700\) W/(m²·K) is assumed contact conductance; \(w\) is contact width. The zero-input branch is the workbook's perfect-contact switch, not physical zero conductance. The result uses the finite-conductance branch.

- **Change from sponsor:** Adds finite tube-to-tube contact resistance instead of assuming perfect contact.

### Total resistance and updated wall temperature in each pass (E47)

\[
R'_{\mathrm{tot},p}=R'_{w,p}+R'_{s,p}+R'_{m,p}+R'_{c,p},
\qquad
T_{w,\mathrm{updated},p}
=T_b+\frac{\Delta T_{\mathrm{lm}}}{R'_{\mathrm{tot},p}}R'_{w,p}
\qquad\Longrightarrow\qquad
\begin{gathered}
R'_{\mathrm{tot},1}\approx 0.0300532\;\mathrm{K\,m/W}\\
T_{w,\mathrm{updated},1}\approx 656.348\;\mathrm{K}\\
R'_{\mathrm{tot},2}\approx 0.0300613\;\mathrm{K\,m/W}\\
T_{w,\mathrm{updated},2}\approx 656.391\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(R'_{\mathrm{tot},p}\) is the sum of fluid-film, metal, and contact resistance factors for pass \(p\) (K·m/W); \(T_{w,\mathrm{updated},p}\) is the wall temperature implied by that pass (K); \(T_b\) is bulk water temperature; \(\Delta T_{\mathrm{lm}}\) is the driving difference. Both passes are shown.

- **Change from sponsor:** Adds contact resistance and fin-adjusted film resistances, with wall-temperature feedback.

### Transfer from pass 1 to pass 2 (E48)

\[
T_{w,2}=T_{w,\mathrm{updated},1}
\qquad\Longrightarrow\qquad
\begin{gathered}
T_{w,2}\approx 656.348\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(T_{w,2}\) is the wall temperature assumed in pass 2 (K); \(T_{w,\mathrm{updated},1}\) is the result from pass 1. The final updated wall temperature is slightly different because Excel uses two explicit passes.

- **Change from sponsor:** Adds a second wall-temperature pass to evaluate Jackson without circular references.

## Final local outputs and hydraulic equations

### Heat transfer per metre and required segment length (E49)

\[
q'_i=\frac{\Delta T_{\mathrm{lm},i}}{R'_{\mathrm{tot},i}},\qquad
\Delta L_i=\frac{\Delta Q_{t,i}}{q'_i},\qquad
z_i=\sum_{j=1}^{i}\Delta L_j
\qquad\Longrightarrow\qquad
\begin{gathered}
q'_1\approx 8309.57\;\mathrm{W/m}\\
\Delta L_1\approx 0.0109566\;\mathrm{m}\\
z_1\approx 0.0109566\;\mathrm{m}
\end{gathered}
\]

- **Variables:** \(q'_i\) is heat-transfer rate per metre of one steam tube (W/m); \(R'_{\mathrm{tot},i}\) is its resistance factor; \(\Delta Q_{t,i}\) is per-tube segment duty (W); \(\Delta L_i\) is segment length (m); \(z_i\) is cumulative height. The first segment's height equals its length.

- **Change from sponsor:**

### Local overall \(U\), contact-area basis (E50)

\[
U_{c,i}=\frac1{R'_{\mathrm{tot},i}w}
\qquad\Longrightarrow\qquad
\begin{gathered}
U_{c,1}\approx 882.39\;\mathrm{W/(m^2\,K)}
\end{gathered}
\]

- **Variables:** \(U_{c,i}\) is local overall coefficient on the assumed contact-area basis (W/(m²·K)); \(R'_{\mathrm{tot},i}\) is total resistance factor; \(w\) is contact width. This local value is not the whole-generator average coefficient.

- **Change from sponsor:**

### Final inner-wall temperatures (E51)

\[
T_{w,\mathrm{steam}}=T_b+q'R'_w,\qquad
T_{w,\mathrm{salt}}=T_s-q'R'_s
\qquad\Longrightarrow\qquad
\begin{gathered}
T_{w,\mathrm{steam}}\approx 656.391\;\mathrm{K}\\
T_{w,\mathrm{salt}}\approx 759.4\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(T_{w,\mathrm{steam}},T_{w,\mathrm{salt}}\) are the steam- and salt-side inner-wall temperatures (K); \(T_b,T_s\) are bulk-fluid temperatures; \(q'\) is heat per metre; \(R'_w,R'_s\) are the corresponding film resistance factors.

- **Change from sponsor:**

### Bore-average heat flux and heat-flux-to-mass-flux ratio (E52)

\[
q''_{\mathrm{bore}}=\frac{q'}{\pi D_i}
=\frac{\Delta Q_{t,i}}{\Delta L_i\pi D_i},\qquad
\Psi=\frac{q''_{\mathrm{bore}}}{G_w}
\qquad\Longrightarrow\qquad
\begin{gathered}
q''_{\mathrm{bore}}\approx 132.251\;\mathrm{kW/m^2}\\
\Psi\approx 1.14473\;\mathrm{kJ/kg}
\end{gathered}
\]

- **Variables:** \(q''_{\mathrm{bore}}\) is heat flux averaged over the steam-bore circumference; \(q'\) is heat per metre; \(D_i\) is bore diameter; \(\Psi=q''_{\mathrm{bore}}/G_w\) is heat flux divided by mass flux. Results are kW/m² and kJ/kg; double prime means per unit area.

- **Change from sponsor:** Adds bore-average heat-flux and heat-flux-to-mass-flux outputs for deterioration screening.

### Implemented turbulent Darcy factor (E53)

\[
f_D=\frac8{6.0516}
\left[\ln\left(\frac{\epsilon_r}{D_i}+
\left(\frac7{Re}\right)^{0.9}\right)\right]^{-2}
\qquad\Longrightarrow\qquad
\begin{gathered}
f_{D,w}\approx 0.0253726\;\text{(dimensionless)}\\
f_{D,s}\approx 0.0250001\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(f_D\) is the dimensionless Darcy factor; \(\epsilon_r=1.5\times10^{-6}\) m is absolute roughness; \(D_i\) is diameter; \(Re\) is the stream's Reynolds number. Both water and salt values are shown.

- **Change from sponsor:**

### Segment friction and water hydrostatic pressure change (E54)

\[
\Delta P_{f,i}=f_D\frac{\Delta L_i}{D_i}\frac{\rho_i v_i^2}{2},
\qquad
\Delta P_{g,w,i}=\rho_{b,i}g\Delta L_i
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta P_{f,w,1}\approx 0.121403\;\mathrm{Pa}\\
\Delta P_{f,s,1}\approx 66.3801\;\mathrm{Pa}\\
\Delta P_{g,w,1}\approx 82.1276\;\mathrm{Pa}
\end{gathered}
\]

- **Variables:** \(\Delta P_{f,i}\) is friction loss across one segment (Pa); \(f_D\) is the Darcy factor; \(\rho_i,v_i\) are local density and speed; \(\Delta L_i\) is segment length; \(\Delta P_{g,w,i}\) is the upward water hydrostatic contribution; \(g=9.81\) m/s². These are segment values, not whole-generator losses.

- **Change from sponsor:**

## Deterioration and nonuniform-property screening

### Wall/bulk straddling flag (E55)

\[
I_i=\begin{cases}1,&T_b<T_{\mathrm{pc}}<T_{w,\mathrm{steam}},\\0,&\text{otherwise}.\end{cases}
\qquad\Longrightarrow\qquad
\begin{gathered}
I_1\approx 1\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(I_i\) is a dimensionless indicator: 1 means bulk water is below \(T_{\mathrm{pc}}\) while the steam-side wall is above it; 0 means that condition is not met. It identifies a screening region, not proven deterioration.

- **Change from sponsor:** Adds a flag for bulk and wall temperatures straddling the pseudo-critical temperature.

### Buoyancy parameter (E56)

\[
\nu_b=\frac{\mu_b}{\rho_b},\qquad
Gr_q=\frac{g\beta_bD_i^4q''_{\mathrm{bore}}}{k_b\nu_b^2},
\qquad
Bo^*=\frac{Gr_q}{Re_b^{3.425}Pr_b^{0.8}}
\qquad\Longrightarrow\qquad
\begin{gathered}
\nu_b\approx 1.25975\times10^{-7}\;\mathrm{m^2/s}\\
Gr_q\approx 4.83556\times10^{10}\;\text{(dimensionless)}\\
Bo^*\approx 5.67868\times10^{-5}\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(\nu_b\) is kinematic viscosity (m²/s); \(\mu_b,\rho_b\) are bulk viscosity and density; \(Gr_q,Bo^*\) are dimensionless; \(\beta_b\) is expansion coefficient (1/K); \(q''_{\mathrm{bore}}\) must be W/m²; \(k_b\) is fluid conductivity; \(Re_b,Pr_b\) are bulk dimensionless groups. The parameter screens buoyancy influence.

- **Change from sponsor:** Adds a buoyancy screening parameter.

### Thermal-acceleration parameter (E57)

\[
K_v=\frac{4q''_{\mathrm{bore}}\beta_b}{G_wc_{p,b}Re_b}
\qquad\Longrightarrow\qquad
\begin{gathered}
K_v\approx 8.35834\times10^{-8}\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(K_v\) is the dimensionless thermal-acceleration parameter; \(q''_{\mathrm{bore}}\) must be W/m²; \(\beta_b\) is expansion coefficient; \(G_w\) is mass flux; \(c_{p,b}\) must be J/(kg·K); \(Re_b\) is bulk Reynolds number.

- **Change from sponsor:** Adds a thermal-acceleration screening parameter.

## Whole-exchanger results

### Direct result links (E58)

\[
(Q,\dot m_w,\dot m_s,G_w)_{\mathrm{Results}}
=(Q,\dot m_w,\dot m_s,G_w)_{\mathrm{Inputs}}
\qquad\Longrightarrow\qquad
\begin{gathered}
Q\approx 500\;\mathrm{MW}\\
\dot m_w\approx 237.223\;\mathrm{kg/s}\\
\dot m_s\approx 6170.52\;\mathrm{kg/s}\\
G_w\approx 115.53\;\mathrm{kg/(m^2\,s)}
\end{gathered}
\]

- **Variables:** \(Q\) is generator duty (MW); \(\dot m_w,\dot m_s\) are total fluid flows (kg/s); \(G_w\) is water mass flux (kg/(m²·s)). The equation indicates shared input/output values rather than a new physical calculation.

- **Change from sponsor:**

### Integrated conductance and effective driving difference (E59)

\[
(UA)_{\mathrm{req}}=\sum_i(UA)_i
=\sum_i\frac{\Delta Q_i}{\Delta T_{\mathrm{lm},i}},\qquad
\Delta T_{\mathrm{eff}}=\frac{Q}{(UA)_{\mathrm{req}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
(UA)_{\mathrm{req}}\approx 3.03379\;\mathrm{MW/K}\\
\Delta T_{\mathrm{eff}}\approx 164.811\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \((UA)_{\mathrm{req}}\) is the sum of segment conductances (MW/K); \(\Delta Q_i\) is segment duty; \(\Delta T_{\mathrm{lm},i}\) is local LMTD; \(\Delta T_{\mathrm{eff}}\) is duty divided by integrated conductance (K), not an arithmetic mean.

- **Change from sponsor:**

### Single-LMTD comparison, implied conductance, and error (E60)

\[
\Delta T_{\mathrm{lm,whole}}
=\frac{\Delta T_c-\Delta T_h}{\ln(\Delta T_c/\Delta T_h)},\qquad
(UA)_{\mathrm{single}}=\frac{Q}{\Delta T_{\mathrm{lm,whole}}},
\qquad
E_{\mathrm{LMTD}}=\frac{(UA)_{\mathrm{single}}}{(UA)_{\mathrm{req}}}-1
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta T_{\mathrm{lm,whole}}\approx 133.136\;\mathrm{K}\\
(UA)_{\mathrm{single}}\approx 3.75557\;\mathrm{MW/K}\\
E_{\mathrm{LMTD}}\approx 0.237915\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(\Delta T_{\mathrm{lm,whole}}\) is the terminal-temperature LMTD (K); \((UA)_{\mathrm{single}}\) is the conductance it would imply (MW/K); \(E_{\mathrm{LMTD}}\) is fractional error relative to segmented conductance. A value 0.237915 means 23.7915% higher required conductance in this comparison.

- **Change from sponsor:** Adds a whole-exchanger LMTD comparison and its implied sizing error.

### Average capacity ratio (E61)

\[
C_r=\frac{C_{w,\mathrm{avg}}}{C_{s,\mathrm{avg}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
C_r\approx 0.296296\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(C_r\) is the dimensionless ratio of average water to salt capacity rates. This formula assumes water has the lower average capacity rate.

- **Change from sponsor:** Adds an average capacity-ratio reporting metric.

### Enthalpy-based effectiveness (E62)

\[
Q_{\max,w}=\dot m_w
\left[H(P,T_{s,\mathrm{in}})-H(P,T_{b,\mathrm{in}})\right],
\qquad
\varepsilon_H=\frac{Q}{Q_{\max,w}}
\qquad\Longrightarrow\qquad
\begin{gathered}
Q_{\max,w}\approx 542.497\;\mathrm{MW}\\
\varepsilon_H\approx 0.921664\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(Q_{\max,w}\) is the enthalpy-limited duty for heating water to the salt inlet temperature (MW); \(H(P,T)\) is specific enthalpy at pressure \(P\) and temperature \(T\); \(\dot m_w\) is total flow; \(\varepsilon_H\) is dimensionless effectiveness against that limit. Use consistent W/J or kW/kJ units.

- **Change from sponsor:** Adds an enthalpy-based effectiveness metric.

### Constant-capacity effectiveness and nominal NTU (E63)

\[
\varepsilon_{\mathrm{avg}}=
\frac{Q}{C_{w,\mathrm{avg}}(T_{s,\mathrm{in}}-T_{b,\mathrm{in}})},\qquad
NTU_{\mathrm{avg}}=\frac{(UA)_{\mathrm{req}}}{C_{w,\mathrm{avg}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
\varepsilon_{\mathrm{avg}}\approx 0.818182\;\text{(dimensionless)}\\
NTU_{\mathrm{avg}}\approx 1.63825\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(\varepsilon_{\mathrm{avg}}\) is effectiveness using the average water capacity rate; \(NTU_{\mathrm{avg}}\) is required conductance divided by that rate. Both are dimensionless reporting quantities, not the governing length-sizing equations.

- **Change from sponsor:** Adds nominal effectiveness and NTU reporting metrics; they are not used to size the exchanger.

### Counterflow effectiveness relation and its inverse (E64)

\[
\varepsilon_{\mathrm{CF}}=
\frac{1-e^{-NTU(1-C_r)}}{1-C_re^{-NTU(1-C_r)}},
\qquad
NTU_{\mathrm{inverse}}=
\frac{\ln[(\varepsilon_{\mathrm{avg}}-1)/
(\varepsilon_{\mathrm{avg}}C_r-1)]}{C_r-1}
\qquad\Longrightarrow\qquad
\begin{gathered}
\varepsilon_{\mathrm{CF}}\approx 0.754882\;\text{(dimensionless)}\\
NTU_{\mathrm{inverse}}\approx 2.02801\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(\varepsilon_{\mathrm{CF}}\) is the constant-capacity counterflow prediction; \(NTU\) and \(C_r\) use the average-capacity values; \(NTU_{\mathrm{inverse}}\) is the inverse result using \(\varepsilon_{\mathrm{avg}}\). All are dimensionless. Their mismatch with the segmented result illustrates a model-applicability limitation.

- **Change from sponsor:** Adds the textbook counterflow effectiveness–NTU relation and inverse as diagnostic comparisons.

### Count of capacity-rate reversals (E65)

\[
n_{\mathrm{water\,larger}}=\sum_i
\mathbf1(C_{w,i}>C_{s,\mathrm{avg}})
\qquad\Longrightarrow\qquad
\begin{gathered}
n_{\mathrm{water\,larger}}\approx 18\;\text{segments}
\end{gathered}
\]

- **Variables:** \(\mathbf1(\cdot)\) equals 1 when its condition is true and 0 otherwise; \(C_{w,i}\) is local water capacity rate; \(C_{s,\mathrm{avg}}\) is average salt capacity rate; \(n_{\mathrm{water\,larger}}\) counts matching segments, not their total length.

- **Change from sponsor:** Adds a count of segments in which the water capacity rate exceeds the average salt capacity rate.

### Heated length and heat-transfer areas (E66)

\[
L=\sum_i\Delta L_i,\qquad
A_c=N_wwL,\qquad A_b=N_w\pi D_iL
\qquad\Longrightarrow\qquad
\begin{gathered}
L\approx 15.3599\;\mathrm{m}\\
A_c\approx 3784.7\;\mathrm{m^2}\\
A_b\approx 6307.84\;\mathrm{m^2}
\end{gathered}
\]

- **Variables:** \(L\) is total heated length (m); \(\Delta L_i\) are segment lengths; \(A_c\) is total contact-basis area; \(A_b\) is total steam-bore area (both m²); \(N_w\) is steam-tube count; \(w\) is contact width; \(D_i\) is bore diameter.

- **Change from sponsor:**

### Overall area-based coefficients and installed heated tube length (E67)

\[
U_c=\frac{(UA)_{\mathrm{req}}}{A_c},\qquad
U_b=\frac{(UA)_{\mathrm{req}}}{A_b},\qquad
L_{\mathrm{installed}}=\frac{(N_w+N_s)L}{1000}\quad[\mathrm{km}]
\qquad\Longrightarrow\qquad
\begin{gathered}
U_c\approx 801.592\;\mathrm{W/(m^2\,K)}\\
U_b\approx 480.955\;\mathrm{W/(m^2\,K)}\\
L_{\mathrm{installed}}\approx 175.687\;\mathrm{km}
\end{gathered}
\]

- **Variables:** \(U_c,U_b\) are whole-generator overall coefficients on contact and bore area bases (W/(m²·K)); convert \(UA\) from MW/K to W/K before dividing by area. \(L_{\mathrm{installed}}\) is heated steam-plus-salt tube length in km; it excludes air tubes, bends, and connections.

- **Change from sponsor:**

### Mean salt velocity and total friction losses (E68)

\[
\bar v_s=\frac1{N_{\mathrm{seg}}}\sum_i v_{s,i},\qquad
\Delta P_{f,s}=\sum_i\Delta P_{f,s,i},\qquad
\Delta P_{f,w}=\sum_i\Delta P_{f,w,i},\qquad
\Delta P_{g,w}=\sum_i\Delta P_{g,w,i}
\qquad\Longrightarrow\qquad
\begin{gathered}
\bar v_s\approx 2.45847\;\mathrm{m/s}\\
\Delta P_{f,s}\approx 92.9248\;\mathrm{kPa}\\
\Delta P_{f,w}\approx 0.751721\;\mathrm{kPa}\\
\Delta P_{g,w}\approx 38.1851\;\mathrm{kPa}
\end{gathered}
\]

- **Variables:** \(\bar v_s\) is the unweighted mean of segment salt velocities (m/s); \(N_{\mathrm{seg}}=540\); \(\Delta P_{f,s},\Delta P_{f,w}\) are total friction losses; \(\Delta P_{g,w}\) is total water elevation pressure change. Summed Pa values are reported in kPa.

- **Change from sponsor:**

### Salt minor losses and reported total (E69)

\[
\rho_{s,\mathrm{ref}}=a_\rho+b_\rho\frac{T_{s,\mathrm{in}}+T_{s,\mathrm{out}}}{2},
\quad
\Delta P_{K,s}=K_s\frac{\rho_{s,\mathrm{ref}}\bar v_s^2}{2},
\quad
\Delta P_{s,\mathrm{reported}}=\Delta P_{f,s}+\Delta P_{K,s}
\qquad\Longrightarrow\qquad
\begin{gathered}
\rho_{s,\mathrm{ref}}\approx 1633.7\;\mathrm{kg/m^3}\\
\Delta P_{K,s}\approx 10.368\;\mathrm{kPa}\\
\Delta P_{s,\mathrm{reported}}\approx 103.293\;\mathrm{kPa}
\end{gathered}
\]

- **Variables:** \(\rho_{s,\mathrm{ref}}\) is salt density at the average terminal temperature (kg/m³); \(a_\rho=2112.68\) kg/m³ and \(b_\rho=-0.5635\) kg/(m³·K); \(K_s=2.1\) is the dimensionless lumped loss coefficient; \(\bar v_s\) is mean salt speed. \(\Delta P_{K,s}\) is minor loss and \(\Delta P_{s,\mathrm{reported}}\) is friction plus minor loss, reported in kPa.

- **Change from sponsor:** Makes the assumed salt minor-loss allowance explicit.

### Salt hydraulic power (E70)

\[
\dot W_{\mathrm{hyd},s}=
\Delta P_{s,\mathrm{reported}}\frac{\dot m_s}{\rho_{s,\mathrm{ref}}}
\qquad\Longrightarrow\qquad
\begin{gathered}
\dot W_{\mathrm{hyd},s}\approx 390.138\;\mathrm{kW}
\end{gathered}
\]

- **Variables:** \(\dot W_{\mathrm{hyd},s}\) is hydraulic power (kW); \(\Delta P_{s,\mathrm{reported}}\) is in kPa; \(\dot m_s/\rho_{s,\mathrm{ref}}\) is salt volume flow (m³/s). Pump and motor efficiencies are not included.

- **Change from sponsor:** Adds a salt hydraulic-power estimate, excluding pump and motor inefficiency.

### Water acceleration pressure change (E71)

\[
\Delta P_{\mathrm{acc},w}
=G_w^2\left(\frac1{\rho_{\mathrm{out}}}-\frac1{\rho_{\mathrm{in}}}\right)
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta P_{\mathrm{acc},w}\approx 0.16382\;\mathrm{kPa}
\end{gathered}
\]

- **Variables:** \(\Delta P_{\mathrm{acc},w}\) is water acceleration pressure change; \(G_w\) is mass flux; \(\rho_{\mathrm{out}},\rho_{\mathrm{in}}\) are endpoint densities (kg/m³). The equation gives Pa, converted here to kPa; these baseline temperatures lie on the property grid.

- **Change from sponsor:** Explicitly includes the water acceleration pressure change.

### Water minor losses and total pressure requirement (E72)

\[
\Delta P_{K,w}=
\frac{K_{\mathrm{in}}G_w^2}{2\rho_{\mathrm{in}}}
+\frac{K_{\mathrm{out}}G_w^2}{2\rho_{\mathrm{out}}},
\qquad
\Delta P_{w,\mathrm{total}}=
\Delta P_{f,w}+\Delta P_{g,w}+\Delta P_{\mathrm{acc},w}+\Delta P_{K,w}
\qquad\Longrightarrow\qquad
\begin{gathered}
\Delta P_{K,w}\approx 0.124814\;\mathrm{kPa}\\
\Delta P_{w,\mathrm{total}}\approx 39.2254\;\mathrm{kPa}
\end{gathered}
\]

- **Variables:** \(K_{\mathrm{in}}=0.8\) and \(K_{\mathrm{out}}=1.3\) are dimensionless loss coefficients; \(\rho_{\mathrm{in}},\rho_{\mathrm{out}}\) are endpoint densities; \(\Delta P_{K,w}\) is inlet/outlet loss. Total water pressure requirement adds friction, gravity, acceleration, and minor losses; results are kPa.

- **Change from sponsor:** Explicitly combines water minor losses, friction, elevation, and acceleration.

### Temperature extrema and salt freezing margin (E73)

\[
T_{w,\max}=\max_i T_{w,\mathrm{steam},i},\quad
T_{s,\mathrm{wall},\min}=\min_i T_{w,\mathrm{salt},i},\quad
M_{\mathrm{freeze}}=T_{s,\mathrm{wall},\min}-T_{\mathrm{freeze}}
\qquad\Longrightarrow\qquad
\begin{gathered}
T_{w,\max}\approx 863.415\;\mathrm{K}\\
T_{s,\mathrm{wall},\min}\approx 759.4\;\mathrm{K}\\
M_{\mathrm{freeze}}\approx 84.4\;\mathrm{K}
\end{gathered}
\]

- **Variables:** \(T_{w,\max}\) is the highest modeled steam-side wall temperature; \(T_{s,\mathrm{wall},\min}\) is the lowest modeled salt-side wall temperature (K); \(T_{\mathrm{freeze}}=675\) K; \(M_{\mathrm{freeze}}\) is the temperature margin (K). These are extrema over all segments.

- **Change from sponsor:** Adds wall-temperature extrema and a salt-wall freezing-margin check.

### Conditional extrema in the flagged region (E74)

\[
z_{\mathrm{zone,top}}=\max_{I_i=1}z_i,\quad
\Psi_{\max,\mathrm{zone}}=\max_{I_i=1}\Psi_i,\quad
\Psi_{\min,\mathrm{zone}}=\min_{I_i=1}\Psi_i,
\qquad\Longrightarrow\qquad
\begin{gathered}
z_{\mathrm{zone,top}}\approx 4.5733\;\mathrm{m}\\
\Psi_{\max,\mathrm{zone}}\approx 1.14473\;\mathrm{kJ/kg}\\
\Psi_{\min,\mathrm{zone}}\approx 0.895928\;\mathrm{kJ/kg}
\end{gathered}
\]

\[
q''_{\max,\mathrm{zone}}=\max_{I_i=1}q''_{\mathrm{bore},i},\qquad
Bo^*_{\max,\mathrm{zone}}=\max_{I_i=1}Bo_i^*,\qquad
K_{v,\max}=\max_iK_{v,i}
\qquad\Longrightarrow\qquad
\begin{gathered}
q''_{\max,\mathrm{zone}}\approx 132.251\;\mathrm{kW/m^2}\\
Bo^*_{\max,\mathrm{zone}}\approx 5.67868\times10^{-5}\;\text{(dimensionless)}\\
K_{v,\max}\approx 1.31672\times10^{-7}\;\text{(dimensionless)}
\end{gathered}
\]

- **Variables:** \(I_i=1\) restricts the extrema to the flagged region; \(z_{\mathrm{zone,top}}\) is its highest segment-end height (m); \(\Psi\) is heat-flux/mass-flux ratio (kJ/kg); \(q''_{\mathrm{bore}}\) is kW/m²; \(Bo^*,K_v\) are dimensionless. The maximum \(K_v\) is taken over all segments, unlike the conditional quantities.

- **Change from sponsor:** Adds conditional extrema for the flagged supercritical-water region.

### Yamagata-style heat-flux screening expression (E75)

\[
q''_{\mathrm{screen}}=0.2\,G_w^{1.2}
\qquad\Longrightarrow\qquad
\begin{gathered}
q''_{\mathrm{screen}}\approx 59.7399\;\mathrm{kW/m^2}
\end{gathered}
\]

- **Variables:** \(q''_{\mathrm{screen}}\) is the empirical screening heat flux (kW/m²); \(G_w\) must be in kg/(m²·s). The numerical coefficient is tied to those units; this is not a guaranteed operating limit.

- **Change from sponsor:** Adds an empirical heat-flux screening comparison, not a safe-operating guarantee.

### Thin-wall hoop-stress screen (E76)

\[
\sigma_{\theta,\mathrm{screen}}=\frac{P_{\mathrm{steam}}D_i}{2t}
\qquad\Longrightarrow\qquad
\begin{gathered}
\sigma_{\theta,\mathrm{screen}}\approx 120\;\mathrm{MPa}
\end{gathered}
\]

- **Variables:** \(\sigma_{\theta,\mathrm{screen}}\) is thin-wall hoop stress (MPa); \(P_{\mathrm{steam}}=24\) MPa is the operating pressure used here; \(D_i\) and \(t\) use the same length units. This is not a code minimum-wall calculation.

- **Change from sponsor:** Adds a preliminary hoop-stress screen, not a pressure-code wall-sizing calculation.

## Chart equations and source mapping

### Temperature-profile chart (E77)

\[
(x,y)_{\mathrm{salt}}=(T_{s,i},z_i),\quad
(x,y)_{\mathrm{water}}=(T_{b,i},z_i),\quad
(x,y)_{\mathrm{wall}}=(T_{w,i},z_i)
\qquad\Longrightarrow\qquad
\begin{gathered}
(x,y)_{\mathrm{salt}}\approx\left(810.093\;\mathrm{K},\;0.0109566\;\mathrm{m}\right)\\
(x,y)_{\mathrm{water}}\approx\left(560.5\;\mathrm{K},\;0.0109566\;\mathrm{m}\right)\\
(x,y)_{\mathrm{wall}}\approx\left(656.391\;\mathrm{K},\;0.0109566\;\mathrm{m}\right)
\end{gathered}
\]

- **Variables:** \(x\) is chart temperature (K), \(y=z_i\) is height (m); \(T_{s,i},T_{b,i}\) are segment-end bulk temperatures; \(T_{w,i}\) is the segment wall result. The coordinates shown are the first plotted point, not the fluid inlet point.

- **Change from sponsor:** Plots the coupled best-estimate wall-temperature solution with the bulk-fluid profiles.

### Reference temperature lines (E78)

\[
(x,y)=(T_{\mathrm{freeze}},0),(T_{\mathrm{freeze}},L);
\qquad
(x,y)=(T_{\mathrm{pc}},0),(T_{\mathrm{pc}},L)
\qquad\Longrightarrow\qquad
\begin{gathered}
(x,y)_{\mathrm{freeze},0}\approx\left(675\;\mathrm{K},\;0\;\mathrm{m}\right)\\
(x,y)_{\mathrm{freeze},L}\approx\left(675\;\mathrm{K},\;15.3599\;\mathrm{m}\right)\\
(x,y)_{\mathrm{pc},0}\approx\left(654.38\;\mathrm{K},\;0\;\mathrm{m}\right)\\
(x,y)_{\mathrm{pc},L}\approx\left(654.38\;\mathrm{K},\;15.3599\;\mathrm{m}\right)
\end{gathered}
\]

- **Variables:** \(T_{\mathrm{freeze}}=675\) K and \(T_{\mathrm{pc}}=654.38\) K are reference temperatures; \(L\) is heated length; \(x\) is K and \(y\) is m. Two endpoints define each vertical reference line.

- **Change from sponsor:** Adds freezing and pseudo-critical reference lines.

### Temperature-difference comparison chart (E79)

\[
(x,y)_{\mathrm{actual}}=(F_i,\Delta T_{i,b}),\qquad
(x,y)_{\mathrm{comparison}}=(F_i,\Delta T_{\mathrm{linear},i})
\qquad\Longrightarrow\qquad
\begin{gathered}
(x,y)_{\mathrm{actual}}\approx\left(0.00119013\;\text{(dimensionless)},\;249.593\;\mathrm{K}\right)\\
(x,y)_{\mathrm{comparison}}\approx\left(0.00119013\;\text{(dimensionless)},\;249.774\;\mathrm{K}\right)
\end{gathered}
\]

- **Variables:** \(F_i\) is the dimensionless cumulative-duty fraction; \(\Delta T_{i,b}\) is the segment-end salt-minus-water difference (K); \(\Delta T_{\mathrm{linear},i}\) is the constant-capacity comparison (K). The listed coordinates are at the first segment end.

- **Change from sponsor:** Adds the variable-property temperature-difference comparison chart.

### Best-estimate water-side coefficient chart curve (E80)

\[
(x,y)_{\mathrm{BE}}=(T_{b,m},h_{w,\mathrm{BE}}/1000)
\qquad\Longrightarrow\qquad
\begin{gathered}
(x,y)_{\mathrm{BE}}\approx\left(560.25\;\mathrm{K},\;1.83805\;\mathrm{kW/(m^2\,K)}\right)
\end{gathered}
\]

- **Variables:** \(T_{b,m}\) is segment-mean water temperature (K); \(h_{w,\mathrm{BE}}\) is the best-estimate water-film coefficient in W/(m²·K). Dividing by 1000 gives the chart's kW/(m²·K); the shown point is segment 1.

- **Change from sponsor:** Plots Jackson’s water-side coefficient instead of the sponsor correlation.
