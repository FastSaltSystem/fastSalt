# Generator sizing — conversion check

Converted 2026-10-10 from `Generator sizing.calca` to native Hurmet Markdown.

## Using the worksheet

Open [Hurmet](https://hurmet.org), choose **File → Open**, and select `Generator sizing - Hurmet.md`. Click a calculation to edit it and press Enter to accept it. If needed, use **Recalculate all** in the toolbar. Keep this `.md` extension when saving: this is Hurmet's editable document format.

The saved worksheet in this folder is the versioned source. Open it in a fresh Hurmet session when continuing work, then save recalculated changes back to the file.

## Verification

- All 103 source calculation lines and all 8 functions were converted. Including the added number-format setting, the saved document contains 112 calculation cells.
- Evaluated with the official Hurmet calculation engine, then saved, reopened through its Markdown parser, and recalculated without errors.
- Checked all 84 numeric results recorded in the source. 83 agree within the two files' displayed rounding precision. The remaining result is the feet-of-water conversion described below.
- Loaded all 112 cells into the live editor at hurmet.org, where they calculated without errors.
- Recalculated with `NGen = 4` in the browser: generator duty 375 MW, salt mass flow 5,674.85788 kg/s, tube length 18.3497129 m, and pump hydraulic power 368.025388 kW. Restored `NGen = 3`; duty returned to 500 MW and tube length to 19.8790057 m.
- No change was made to the original Calca file. Correlations and engineering assumptions were preserved; these checks establish conversion fidelity, not the adequacy of the design assumptions.

Hurmet uses 2,989 Pa per `ftH₂O`. Its answer is 63.8584111 ftH₂O versus 63.8588 in Calca, approximately 0.0006% lower. The calculated pressure drop in kPa agrees. This difference is confined to that display conversion.

The source's two `kW/m^-2` radiation display requests were changed to `kW/m2`, matching their equations and original displayed results. Other syntax adaptations are listed in the worksheet's conversion notes.

## Provenance

- Source path: `/Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Steam Generator/Calculations/Generator sizing.calca`
- Source SHA-256: `0b64fac45e4e272bb46c3cdb198e1a1eacd35de9465e362521c786f34b34e0f1`
- Engine: [official Hurmet source](https://github.com/ronkok/Hurmet/tree/8e82edefe91f1fff5d79df046880fcb5375ed1c4), commit `8e82edefe91f1fff5d79df046880fcb5375ed1c4`.

## Result comparison

Hurmet values below use nine significant digits for non-integers. Original Calca display precision varies. Units with negative exponents are equivalent to denominator notation.

| Quantity | Original Calca display | Hurmet display | Check |
|---|---|---|---|
| `Q_Gen` | 500 MW | 500 MW | Matches rounding |
| `SaltAveT` | 842.5 K | 842.5 K | Matches rounding |
| `DTtop` | 45 K | 45 K | Matches rounding |
| `DTbot` | 250 K | 250 K | Matches rounding |
| `DTAve` | 147.5 K | 147.5 K | Matches rounding |
| `DT_lmdt` | 119.5476 K | 119.547579 K | Matches rounding |
| `CoolantDensity` | 1,637.9313 kg/m^3 | 1,637.93125 kg/m3 | Matches rounding |
| `CoolantHeatCapacity` | 1.0166 J/(g*K) | 1.01663 J.g-1.K-1 | Matches rounding |
| `CoolantViscosity` | 0.0029 kg/(m*s) | 0.00294967785 kg.m-1.s-1 | Matches rounding |
| `CoolantHeatCond` | 0.4341 W/(K*m) | 0.43413 W.m-1.K-1 | Matches rounding |
| `SaltMassFlow` | 7,566.4772 kg/s | 7,566.47718 kg/s | Matches rounding |
| `TubeOD` | 1.6 cm | 1.6 cm | Matches rounding |
| `TubeArea` | 1.5394 cm^2 | 1.5393804 cm2 | Matches rounding |
| `AreaNeeded` | 1.5398 m^2 | 1.53984428 m2 | Matches rounding |
| `TubesNeeded` | 10,004 | 10,004 | Matches rounding |
| `TubesUsed` | 12,000 | 12,000 | Matches rounding |
| `TubesPerRowSq` | 155 | 155 | Matches rounding |
| `NRows` | 78 | 78 | Matches rounding |
| `NTubes` | 12,090 | 12,090 | Matches rounding |
| `SaltWidth` | 1.248 m | 1.248 m | Matches rounding |
| `GenDepth` | 2.48 m | 2.48 m | Matches rounding |
| `GenDepth` | 8.1365 ft | 8.13648294 ft | Matches rounding |
| `GenWidth` | 2.496 m | 2.496 m | Matches rounding |
| `GenWidth` | 8.189 ft | 8.18897638 ft | Matches rounding |
| `Q_Side` | 20.6782 kW | 20.6782465 kW | Matches rounding |
| `sigma` | 5.669e-8 W/(m^2*K^4) | 5.66900000e-8 W.m-2.K-4 | Matches rounding |
| `qTop_A` | 2.3399 kW/m^2 | 2.33994392 kW/m2 | Matches rounding |
| `qBot_A` | 6.9638 kW/m^2 | 6.96378465 kW/m2 | Matches rounding |
| `qRadAve_A` | 4.6519 kW/m^2 | 4.65186428 kW/m2 | Matches rounding |
| `QRadPerL` | 1.7997 MW/m | 1.79971325 MW/m | Matches rounding |
| `RadLength` | 277.822 m | 277.822036 m | Matches rounding |
| `AirK` | 0.024 W/(K*m) | 0.024 W.m-1.K-1 | Matches rounding |
| `AirGap` | 0.8 cm | 0.8 cm | Matches rounding |
| `qAirK_A` | 0.3586 kW/m^2 | 0.358642736 kW/m2 | Matches rounding |
| `qAirConv_A` | 2.1519 kW/m^2 | 2.15185642 kW/m2 | Matches rounding |
| `SteelCond` | 19 W/(K*m) | 19 W.m-1.K-1 | Matches rounding |
| `NSurfaces` | 24,180 | 24,180 | Matches rounding |
| `Q_K_S` | 0.173 kW/K | 0.172970852 kW/K | Matches rounding |
| `NominalLength` | 9.1037 m | 9.10372903 m | Matches rounding |
| `touchW` | 0.16 cm | 0.16 cm | Matches rounding |
| `touchTh` | 2 mm | 2 mm | Matches rounding |
| `touchAspect` | 1.25 | 1.25 | Matches rounding |
| `touchLength` | 11.3797 m | 11.3796613 m | Matches rounding |
| `saddleW` | 1.2 cm | 1.2 cm | Matches rounding |
| `saddleTh` | 4.6667 mm | 4.66666667 mm | Matches rounding |
| `saddleAspect` | 0.3889 | 0.388888889 | Matches rounding |
| `saddleLength` | 3.5403 m | 3.54033907 m | Matches rounding |
| `sqAspect` | 0.25 | 0.25 | Matches rounding |
| `sqLength` | 2.2759 m | 2.27593226 m | Matches rounding |
| `sqContactR` | 0.1053 m^2*K/kW | 0.105263158 m2.K/kW | Matches rounding |
| `saltVel` | 2.4821 m/s | 2.48213732 m/s | Matches rounding |
| `saltReyn` | 19,296.339 | 19,296.339 | Matches rounding |
| `saltBulkH` | 4.4254 kW/(K*m^2) | 4.42540763 kW.m-2.K-1 | Matches rounding |
| `saltR` | 0.226 K*m^2/kW | 0.225967884 m2.K/kW | Matches rounding |
| `saltLength` | 4.8857 m | 4.88573217 m | Matches rounding |
| `SteamMassFlow` | 237.187 kg/s | 237.187038 kg/s | Matches rounding |
| `ExitDensity` | 73.6086 kg/m^3 | 73.6086493 kg/m3 | Matches rounding |
| `ExitViscosity` | 3.392e-5 kg/(m*s) | 0.00003392 kg.m-1.s-1 | Matches rounding |
| `ExitConduct` | 0.1 W/(m*K) | 0.1 W.m-1.K-1 | Matches rounding |
| `ExitHeatCapacity` | 2,980.664 W*s/(kg*K) | 2,980.664 J.kg-1.K-1 | Matches rounding |
| `ExitVelocity` | 1.7314 m/s | 1.73136984 m/s | Matches rounding |
| `ExityReyn` | 52,600.6232 | 52,600.6232 | Matches rounding |
| `ExitBulkH` | 1.2043 kW/(K*m^2) | 1.2043172 kW.m-2.K-1 | Matches rounding |
| `ExitR` | 0.8303 K*m^2/kW | 0.830346025 m2.K/kW | Matches rounding |
| `InletViscocity` | 9.635e-5 kg/(m*s) | 0.00009635 kg.m-1.s-1 | Matches rounding |
| `InletConduct` | 0.6 W/(m*K) | 0.6 W.m-1.K-1 | Matches rounding |
| `InletHeatCapacity` | 5,012.22 W*s/(kg*K) | 5,012.22 J.kg-1.K-1 | Matches rounding |
| `InletVelocity` | 0.1667 m/s | 0.166703461 m/s | Matches rounding |
| `InletReyn` | 18,518.0398 | 18,518.0398 | Matches rounding |
| `InletBulkH` | 2.89 kW/(K*m^2) | 2.88998576 kW.m-2.K-1 | Matches rounding |
| `InletR` | 0.346 K*m^2/kW | 0.346022467 m2.K/kW | Matches rounding |
| `SteamAveR` | 0.5882 K*m^2/kW | 0.588184246 m2.K/kW | Matches rounding |
| `steamlength` | 12.7173 m | 12.7173412 m | Matches rounding |
| `allThreeR` | 0.9194 K*m^2/kW | 0.919415288 m2.K/kW | Matches rounding |
| `tubeLength` | 19.879 m | 19.8790057 m | Matches rounding |
| `AddedLengths` | 19.879 m | 19.8790057 m | Matches rounding |
| `tubeLength` | 65.2198 ft | 65.2198349 ft | Matches rounding |
| `tubeLengthTotal` | 1,442.0231 km | 1,442.02307 km | Matches rounding |
| `CoolantPressureDrop` | 190.8728 kPa | 190.872791 kPa | Matches rounding |
| `CoolantPressureDrop` | 27.6838 psi | 27.6837578 psi | Matches rounding |
| `CoolantPressureDrop` | 63.8588 ftH2O | 63.8584111 ftH₂O | Unit-constant difference |
| `GenPumpPower` | 881.7431 kW | 881.743122 kW | Matches rounding |
| `GenPumpPower` | 1,182.437 hp | 1,182.437 hp | Matches rounding |
| `Buoncy` | 7.1356 kPa | 7.13555914 kPa | Matches rounding |
