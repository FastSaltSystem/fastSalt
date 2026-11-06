---------------
decimalFormat: 1,000,000.
fontSize: 12
pageSize: letter
dateFormat: yyyy-mm-dd
saveDate: 2026-11-05
---------------

# WISTR Steam Generator: Full Hurmet Workbook

Native Hurmet conversion of WISTR_SG_Calculation\_Workbook.xlsx. Both models,
all input data, all 540 segments, all result formulas, the three charts, the
static studies and the embedded water-property table are retained.

## Opening and editing

Open this Markdown file in Hurmet using its file-open command; do not paste it
into an ordinary Markdown editor expecting calculations to run. Calculation
cells and user-defined functions use native Hurmet syntax, as described in the
[Hurmet manual][1].

Edit an input calculation in the Inputs section to recalculate the document. The
complete marches are stored in TM (30 columns), SS (32 columns) and BE (66
columns); their columns match Excel A:AD, A:AF and A:BN respectively, and
Hurmet segment i corresponds to Excel row i+4.

**Units:** the solver deliberately uses numeric magnitudes in the workbook's
stated units, not dimensional-unit checking. Units are shown alongside inputs,
results and every column definition; do not insert unit suffixes into the
solver inputs or change their unit system.

**Scope:** this is a format conversion, not a new design validation. The Jackson
model still uses exactly two wall-temperature passes per segment, and the
approximately 4 m wall-temperature dip remains a model prediction rather than
an experimentally validated feature.

### Preserved limitations and conversion details

*   Water properties remain the embedded 24 MPa table. Editing steam pressure
    changes the hoop-stress calculation only; it does not regenerate water
    properties or the pseudo-critical temperature.
*   Keep Nseg = 540 for the faithful workbook configuration. All bulk and wall
    lookup temperatures must lie inside the property-table range and have an
    upper interpolation row; do not extrapolate beyond 555 to less than 900 K.
    Steel-table lookup temperatures must likewise stay below its last row at 1000 K.
*   Entering contact conductance 0 retains the workbook's special meaning: perfect
    contact, not an insulating interface.
*   The pressure-loss expressions at Results C36:D37 retain the workbook's original
    interpolation grouping. They match the baseline, whose inlet/outlet
    temperatures lie on table rows, but have a known reciprocal-density
    grouping defect for off-grid endpoint temperatures. Do not use off-grid
    endpoint pressure-loss outputs for design without correcting and
    revalidating those four cells.
*   TM column T is encoded as 1 = Water, 0 = Salt to keep the march matrix numeric.
    The criterion is unchanged; it labels the larger capacity-rate stream, not
    C\_min.
*   Intermediate cell results are rounded to 15 significant digits to keep Hurmet
    rational arithmetic bounded. Numerical conversion tolerances are reported
    in the verification section.
*   Studies remain static, exactly as in Excel, including their small differences
    from the live two-pass baseline. They do not update when inputs change.
*   Native Hurmet charts replace Excel chart objects. Workbook styles and drawing
    objects are not calculation data; source chart-helper formulas are also
    retained as a live matrix.

¢` format = "h15" `

## Calculation functions

These native functions replace the repeated row formulas, not the engineering
model. Local variable cA means the current segment's Excel column A, pA means
the previous segment's A, and so on; each cell expression remains visible and
editable.

¢` function flagged(values, flags, criterion, maximum)
    found = 0
    ans = 0
    for i in 1:length(values)
        if flags[i] == criterion
            if found == 0
                ans = values[i]
                found = 1
            elseif maximum == 1
                ans = max(ans, values[i])
            else
                ans = min(ans, values[i])
            end
        end
    end
    return ans
end `

¢` function sgMarch(iv, WP, KT, TM)
    WPdT = iv[1]
    WPT0 = iv[2]
    Pth = iv[3]
    Pe = iv[4]
    Ngen = iv[5]
    etaplant = iv[6]
    QSG = iv[7]
    WeSG = iv[8]
    etaR = iv[9]
    Tsaltin = iv[10]
    Tsaltout = iv[11]
    Twin = iv[12]
    Twout = iv[13]
    Psteam = iv[14]
    dTcold = iv[15]
    dThot = iv[16]
    Nseg = iv[17]
    dTstep = iv[18]
    hwin = iv[19]
    hwout = iv[20]
    mw = iv[21]
    dhsalt = iv[22]
    ms = iv[23]
    Csalt = iv[24]
    Cwavg = iv[25]
    wnet = iv[26]
    Nsteam = iv[27]
    saltratio = iv[28]
    Nsalt = iv[29]
    Nair = iv[30]
    Di = iv[31]
    twall = iv[32]
    Do = iv[33]
    Aflow = iv[34]
    wcontact = iv[35]
    ri = iv[36]
    rm = iv[37]
    mwtube = iv[38]
    mstube = iv[39]
    Gw = iv[40]
    rhoa = iv[41]
    rhob = iv[42]
    cpa = iv[43]
    cpb = iv[44]
    mua = iv[45]
    mub = iv[46]
    ka = iv[47]
    kb = iv[48]
    Tfreeze = iv[49]
    NuC = iv[50]
    Nua = iv[51]
    Nub = iv[52]
    kwallss = iv[53]
    hcontact = iv[54]
    HTDmult = iv[55]
    JC = iv[56]
    JRe = iv[57]
    JPr = iv[58]
    Jrho = iv[59]
    Tpc = iv[60]
    wallguess = iv[61]
    gap1 = iv[62]
    gap2 = iv[63]
    saltgap = iv[64]
    saltbacked = iv[65]
    rough = iv[66]
    gacc = iv[67]
    Ksalt = iv[68]
    Kwin = iv[69]
    Kwout = iv[70]
    K316T0 = iv[71]
    K316dT = iv[72]
    for i in 1:Nseg
        if i == 1
            cA = round(1, "r15")
        else
            cA = round((pA + 1), "r15")
        end
        if i == 1
            cB = round(Twin, "r15")
        else
            cB = round(pC, "r15")
        end
        cC = round((cB + dTstep), "r15")
        cD = round(((cB + cC) / 2), "r15")
        cE = round((WP[(floor(((cB - WPT0) / WPdT)) + 1),2] + ((((cB - WPT0) / WPdT) - floor(((cB - WPT0) / WPdT))) * (WP[(floor(((cB - WPT0) / WPdT)) + 2),2] - WP[(floor(((cB - WPT0) / WPdT)) + 1),2]))), "r15")
        cF = round((WP[(floor(((cC - WPT0) / WPdT)) + 1),2] + ((((cC - WPT0) / WPdT) - floor(((cC - WPT0) / WPdT))) * (WP[(floor(((cC - WPT0) / WPdT)) + 2),2] - WP[(floor(((cC - WPT0) / WPdT)) + 1),2]))), "r15")
        cG = round(((mw * (cF - cE)) / 1000), "r15")
        if i == 1
            cH = round(cG, "r15")
        else
            cH = round((pH + cG), "r15")
        end
        cI = round((cH / QSG), "r15")
        if i == 1
            cJ = round((((-cpa) + sqrt(((cpa ^ 2) + ((2 * cpb) * ((cpa * Tsaltout) + ((cpb / 2) * (Tsaltout ^ 2))))))) / cpb), "r15")
        else
            cJ = round((((-cpa) + sqrt(((cpa ^ 2) + ((2 * cpb) * (((cpa * Tsaltout) + ((cpb / 2) * (Tsaltout ^ 2))) + ((pH * 1000000) / ms)))))) / cpb), "r15")
        end
        cK = round((((-cpa) + sqrt(((cpa ^ 2) + ((2 * cpb) * (((cpa * Tsaltout) + ((cpb / 2) * (Tsaltout ^ 2))) + ((cH * 1000000) / ms)))))) / cpb), "r15")
        cL = round(((cJ + cK) / 2), "r15")
        cM = round((cJ - cB), "r15")
        cN = round((cK - cC), "r15")
        if (abs((cM - cN)) < 0.000000001)
            conditional1 = cM
        else
            conditional1 = ((cM - cN) / ln((cM / cN)))
        end
        cO = round(conditional1, "r15")
        cP = round((cG / cO), "r15")
        cQ = round((dTcold + ((dThot - dTcold) * cI)), "r15")
        cR = round(((cF - cE) / (cC - cB)), "r15")
        cS = round(((mw * cR) / 1000), "r15")
        if (cS > Csalt)
            conditional2 = 1
        else
            conditional2 = 0
        end
        cT = round(conditional2, "r15")
        cU = round((WP[(floor(((cD - WPT0) / WPdT)) + 1),3] + ((((cD - WPT0) / WPdT) - floor(((cD - WPT0) / WPdT))) * (WP[(floor(((cD - WPT0) / WPdT)) + 2),3] - WP[(floor(((cD - WPT0) / WPdT)) + 1),3]))), "r15")
        cV = round((WP[(floor(((cD - WPT0) / WPdT)) + 1),5] + ((((cD - WPT0) / WPdT) - floor(((cD - WPT0) / WPdT))) * (WP[(floor(((cD - WPT0) / WPdT)) + 2),5] - WP[(floor(((cD - WPT0) / WPdT)) + 1),5]))), "r15")
        cW = round((WP[(floor(((cD - WPT0) / WPdT)) + 1),6] + ((((cD - WPT0) / WPdT) - floor(((cD - WPT0) / WPdT))) * (WP[(floor(((cD - WPT0) / WPdT)) + 2),6] - WP[(floor(((cD - WPT0) / WPdT)) + 1),6]))), "r15")
        cX = round((WP[(floor(((cD - WPT0) / WPdT)) + 1),4] + ((((cD - WPT0) / WPdT) - floor(((cD - WPT0) / WPdT))) * (WP[(floor(((cD - WPT0) / WPdT)) + 2),4] - WP[(floor(((cD - WPT0) / WPdT)) + 1),4]))), "r15")
        cY = round((WP[(floor(((cD - WPT0) / WPdT)) + 1),2] + ((((cD - WPT0) / WPdT) - floor(((cD - WPT0) / WPdT))) * (WP[(floor(((cD - WPT0) / WPdT)) + 2),2] - WP[(floor(((cD - WPT0) / WPdT)) + 1),2]))), "r15")
        cZ = round((WP[(floor(((cD - WPT0) / WPdT)) + 1),7] + ((((cD - WPT0) / WPdT) - floor(((cD - WPT0) / WPdT))) * (WP[(floor(((cD - WPT0) / WPdT)) + 2),7] - WP[(floor(((cD - WPT0) / WPdT)) + 1),7]))), "r15")
        cAA = round((rhoa + (rhob * cL)), "r15")
        cAB = round((cpa + (cpb * cL)), "r15")
        cAC = round((mua * exp((mub / cL))), "r15")
        cAD = round((ka + (kb * cL)), "r15")
        if i == 1
            mat = [cA, cB, cC, cD, cE, cF, cG, cH, cI, cJ, cK, cL, cM, cN, cO, cP, cQ, cR, cS, cT, cU, cV, cW, cX, cY, cZ, cAA, cAB, cAC, cAD]
        else
            mat = vcat(mat, [cA, cB, cC, cD, cE, cF, cG, cH, cI, cJ, cK, cL, cM, cN, cO, cP, cQ, cR, cS, cT, cU, cV, cW, cX, cY, cZ, cAA, cAB, cAC, cAD])
        end
        pA = cA
        pC = cC
        pH = cH
    end
    return mat
end `

¢` function sgSponsor(iv, WP, KT, TM)
    WPdT = iv[1]
    WPT0 = iv[2]
    Pth = iv[3]
    Pe = iv[4]
    Ngen = iv[5]
    etaplant = iv[6]
    QSG = iv[7]
    WeSG = iv[8]
    etaR = iv[9]
    Tsaltin = iv[10]
    Tsaltout = iv[11]
    Twin = iv[12]
    Twout = iv[13]
    Psteam = iv[14]
    dTcold = iv[15]
    dThot = iv[16]
    Nseg = iv[17]
    dTstep = iv[18]
    hwin = iv[19]
    hwout = iv[20]
    mw = iv[21]
    dhsalt = iv[22]
    ms = iv[23]
    Csalt = iv[24]
    Cwavg = iv[25]
    wnet = iv[26]
    Nsteam = iv[27]
    saltratio = iv[28]
    Nsalt = iv[29]
    Nair = iv[30]
    Di = iv[31]
    twall = iv[32]
    Do = iv[33]
    Aflow = iv[34]
    wcontact = iv[35]
    ri = iv[36]
    rm = iv[37]
    mwtube = iv[38]
    mstube = iv[39]
    Gw = iv[40]
    rhoa = iv[41]
    rhob = iv[42]
    cpa = iv[43]
    cpb = iv[44]
    mua = iv[45]
    mub = iv[46]
    ka = iv[47]
    kb = iv[48]
    Tfreeze = iv[49]
    NuC = iv[50]
    Nua = iv[51]
    Nub = iv[52]
    kwallss = iv[53]
    hcontact = iv[54]
    HTDmult = iv[55]
    JC = iv[56]
    JRe = iv[57]
    JPr = iv[58]
    Jrho = iv[59]
    Tpc = iv[60]
    wallguess = iv[61]
    gap1 = iv[62]
    gap2 = iv[63]
    saltgap = iv[64]
    saltbacked = iv[65]
    rough = iv[66]
    gacc = iv[67]
    Ksalt = iv[68]
    Kwin = iv[69]
    Kwout = iv[70]
    K316T0 = iv[71]
    K316dT = iv[72]
    for i in 1:Nseg
        cA = round(TM[i,1], "r15")
        cB = round(TM[i,4], "r15")
        cC = round(TM[i,12], "r15")
        cD = round(TM[i,15], "r15")
        cE = round(((TM[i,7] * 1000000) / Nsteam), "r15")
        cF = round((mwtube / (TM[i,21] * Aflow)), "r15")
        cG = round((((TM[i,21] * cF) * Di) / TM[i,22]), "r15")
        cH = round((((TM[i,18] * 1000) * TM[i,22]) / TM[i,23]), "r15")
        cI = round(((NuC * (cG ^ Nua)) * (cH ^ Nub)), "r15")
        cJ = round(((cI * TM[i,23]) / Di), "r15")
        cK = round((mstube / (TM[i,27] * Aflow)), "r15")
        cL = round((((TM[i,27] * cK) * Di) / TM[i,29]), "r15")
        cM = round(((TM[i,28] * TM[i,29]) / TM[i,30]), "r15")
        cN = round(((NuC * (cL ^ Nua)) * (cM ^ Nub)), "r15")
        cO = round(((cN * TM[i,30]) / Di), "r15")
        cP = round((1000 / cJ), "r15")
        cQ = round((1000 / cO), "r15")
        cR = round((((1000 * 2) * twall) / kwallss), "r15")
        cS = round(((cP + cQ) + cR), "r15")
        cT = round((1000 / cS), "r15")
        cU = round((((cE * cS) / 1000) / (cD * wcontact)), "r15")
        if i == 1
            cV = round(cU, "r15")
        else
            cV = round((pV + cU), "r15")
        end
        cW = round((cD / cS), "r15")
        cX = round((cB + ((cW * 1000) / cJ)), "r15")
        cY = round((cC - ((cW * 1000) / cO)), "r15")
        cZ = round((((cE / cU) / (π * Di)) / 1000), "r15")
        cAA = round((cZ / Gw), "r15")
        cAB = round(((8 / 6.0516) * (ln(((rough / Di) + ((7 / cG) ^ 0.9))) ^ (-2))), "r15")
        cAC = round((((((cAB * cU) / Di) * 0.5) * TM[i,21]) * (cF ^ 2)), "r15")
        cAD = round(((TM[i,21] * gacc) * cU), "r15")
        cAE = round(((8 / 6.0516) * (ln(((rough / Di) + ((7 / cL) ^ 0.9))) ^ (-2))), "r15")
        cAF = round((((((cAE * cU) / Di) * 0.5) * TM[i,27]) * (cK ^ 2)), "r15")
        if i == 1
            mat = [cA, cB, cC, cD, cE, cF, cG, cH, cI, cJ, cK, cL, cM, cN, cO, cP, cQ, cR, cS, cT, cU, cV, cW, cX, cY, cZ, cAA, cAB, cAC, cAD, cAE, cAF]
        else
            mat = vcat(mat, [cA, cB, cC, cD, cE, cF, cG, cH, cI, cJ, cK, cL, cM, cN, cO, cP, cQ, cR, cS, cT, cU, cV, cW, cX, cY, cZ, cAA, cAB, cAC, cAD, cAE, cAF])
        end
        pV = cV
    end
    return mat
end `

¢` function sgBest(iv, WP, KT, TM)
    WPdT = iv[1]
    WPT0 = iv[2]
    Pth = iv[3]
    Pe = iv[4]
    Ngen = iv[5]
    etaplant = iv[6]
    QSG = iv[7]
    WeSG = iv[8]
    etaR = iv[9]
    Tsaltin = iv[10]
    Tsaltout = iv[11]
    Twin = iv[12]
    Twout = iv[13]
    Psteam = iv[14]
    dTcold = iv[15]
    dThot = iv[16]
    Nseg = iv[17]
    dTstep = iv[18]
    hwin = iv[19]
    hwout = iv[20]
    mw = iv[21]
    dhsalt = iv[22]
    ms = iv[23]
    Csalt = iv[24]
    Cwavg = iv[25]
    wnet = iv[26]
    Nsteam = iv[27]
    saltratio = iv[28]
    Nsalt = iv[29]
    Nair = iv[30]
    Di = iv[31]
    twall = iv[32]
    Do = iv[33]
    Aflow = iv[34]
    wcontact = iv[35]
    ri = iv[36]
    rm = iv[37]
    mwtube = iv[38]
    mstube = iv[39]
    Gw = iv[40]
    rhoa = iv[41]
    rhob = iv[42]
    cpa = iv[43]
    cpb = iv[44]
    mua = iv[45]
    mub = iv[46]
    ka = iv[47]
    kb = iv[48]
    Tfreeze = iv[49]
    NuC = iv[50]
    Nua = iv[51]
    Nub = iv[52]
    kwallss = iv[53]
    hcontact = iv[54]
    HTDmult = iv[55]
    JC = iv[56]
    JRe = iv[57]
    JPr = iv[58]
    Jrho = iv[59]
    Tpc = iv[60]
    wallguess = iv[61]
    gap1 = iv[62]
    gap2 = iv[63]
    saltgap = iv[64]
    saltbacked = iv[65]
    rough = iv[66]
    gacc = iv[67]
    Ksalt = iv[68]
    Kwin = iv[69]
    Kwout = iv[70]
    K316T0 = iv[71]
    K316dT = iv[72]
    for i in 1:Nseg
        cA = round(TM[i,1], "r15")
        cB = round(TM[i,4], "r15")
        cC = round(TM[i,12], "r15")
        cD = round(TM[i,15], "r15")
        cE = round(((TM[i,7] * 1000000) / Nsteam), "r15")
        cF = round((mstube / (TM[i,27] * Aflow)), "r15")
        cG = round((((TM[i,27] * cF) * Di) / TM[i,29]), "r15")
        cH = round(((TM[i,28] * TM[i,29]) / TM[i,30]), "r15")
        cI = round((((0.79 * ln(cG)) - 1.64) ^ (-2)), "r15")
        cJ = round(((((cI / 8) * (cG - 1000)) * cH) / (1 + ((12.7 * sqrt((cI / 8))) * ((cH ^ (2 / 3)) - 1)))), "r15")
        cK = round(((cJ * TM[i,30]) / Di), "r15")
        cL = round(((Gw * Di) / TM[i,22]), "r15")
        cM = round((((TM[i,24] * 1000) * TM[i,22]) / TM[i,23]), "r15")
        if i == 1
            cN = round((cB + wallguess), "r15")
        else
            cN = round((pBB + (cB - pB)), "r15")
        end
        cO = round((WP[(floor(((cN - WPT0) / WPdT)) + 1),3] + ((((cN - WPT0) / WPdT) - floor(((cN - WPT0) / WPdT))) * (WP[(floor(((cN - WPT0) / WPdT)) + 2),3] - WP[(floor(((cN - WPT0) / WPdT)) + 1),3]))), "r15")
        cP = round((WP[(floor(((cN - WPT0) / WPdT)) + 1),2] + ((((cN - WPT0) / WPdT) - floor(((cN - WPT0) / WPdT))) * (WP[(floor(((cN - WPT0) / WPdT)) + 2),2] - WP[(floor(((cN - WPT0) / WPdT)) + 1),2]))), "r15")
        cQ = round((((cP - TM[i,25]) * 1000) / (cN - cB)), "r15")
        if (((cB < cN) and (cN <= Tpc)) or (cB >= (1.2 * Tpc)))
            conditional1 = 0.4
        else
            if ((cB <= Tpc) and (Tpc < cN))
                conditional2 = (0.4 + (0.2 * ((cN / Tpc) - 1)))
            else
                conditional2 = (0.4 + ((0.2 * ((cN / Tpc) - 1)) * (1 - (5 * ((cB / Tpc) - 1)))))
            end
            conditional1 = conditional2
        end
        cR = round(conditional1, "r15")
        cS = round(((((((JC * (cL ^ JRe)) * (cM ^ JPr)) * ((cO / TM[i,21]) ^ Jrho)) * ((cQ / (TM[i,24] * 1000)) ^ cR)) * TM[i,23]) / Di), "r15")
        cT = round((KT[(floor(((((cN + cC) / 2) - K316T0) / K316dT)) + 1),2] + ((((((cN + cC) / 2) - K316T0) / K316dT) - floor(((((cN + cC) / 2) - K316T0) / K316dT))) * (KT[(floor(((((cN + cC) / 2) - K316T0) / K316dT)) + 2),2] - KT[(floor(((((cN + cC) / 2) - K316T0) / K316dT)) + 1),2]))), "r15")
        cU = round((tanh((((sqrt((cS / (cT * twall))) * rm) * (gap1 * π / 180)) / 2)) / (((sqrt((cS / (cT * twall))) * rm) * (gap1 * π / 180)) / 2)), "r15")
        cV = round((tanh((((sqrt((cS / (cT * twall))) * rm) * (gap2 * π / 180)) / 2)) / (((sqrt((cS / (cT * twall))) * rm) * (gap2 * π / 180)) / 2)), "r15")
        cW = round((ri * ((π + (cU * (gap1 * π / 180))) + (cV * (gap2 * π / 180)))), "r15")
        cX = round((tanh((((sqrt((cK / (cT * twall))) * rm) * (saltgap * π / 180)) / 2)) / (((sqrt((cK / (cT * twall))) * rm) * (saltgap * π / 180)) / 2)), "r15")
        cY = round((((((Nsalt / Nsteam) * 2) * π) * ri) * (saltbacked + ((1 - saltbacked) * cX))), "r15")
        cZ = round((1 / (cS * cW)), "r15")
        cAA = round((1 / (cK * cY)), "r15")
        cAB = round(((2 * twall) / (cT * wcontact)), "r15")
        if (hcontact == 0)
            conditional3 = 0
        else
            conditional3 = (1 / (hcontact * wcontact))
        end
        cAC = round(conditional3, "r15")
        cAD = round((((cZ + cAA) + cAB) + cAC), "r15")
        cAE = round((cB + ((cD / cAD) * cZ)), "r15")
        cAF = round(cAE, "r15")
        cAG = round((WP[(floor(((cAF - WPT0) / WPdT)) + 1),3] + ((((cAF - WPT0) / WPdT) - floor(((cAF - WPT0) / WPdT))) * (WP[(floor(((cAF - WPT0) / WPdT)) + 2),3] - WP[(floor(((cAF - WPT0) / WPdT)) + 1),3]))), "r15")
        cAH = round((WP[(floor(((cAF - WPT0) / WPdT)) + 1),2] + ((((cAF - WPT0) / WPdT) - floor(((cAF - WPT0) / WPdT))) * (WP[(floor(((cAF - WPT0) / WPdT)) + 2),2] - WP[(floor(((cAF - WPT0) / WPdT)) + 1),2]))), "r15")
        cAI = round((((cAH - TM[i,25]) * 1000) / (cAF - cB)), "r15")
        if (((cB < cAF) and (cAF <= Tpc)) or (cB >= (1.2 * Tpc)))
            conditional4 = 0.4
        else
            if ((cB <= Tpc) and (Tpc < cAF))
                conditional5 = (0.4 + (0.2 * ((cAF / Tpc) - 1)))
            else
                conditional5 = (0.4 + ((0.2 * ((cAF / Tpc) - 1)) * (1 - (5 * ((cB / Tpc) - 1)))))
            end
            conditional4 = conditional5
        end
        cAJ = round(conditional4, "r15")
        if ((cB < Tpc) and (Tpc < cAF))
            conditional6 = HTDmult
        else
            conditional6 = 1
        end
        cAK = round((((((((JC * (cL ^ JRe)) * (cM ^ JPr)) * ((cAG / TM[i,21]) ^ Jrho)) * ((cAI / (TM[i,24] * 1000)) ^ cAJ)) * TM[i,23]) / Di) * conditional6), "r15")
        cAL = round((KT[(floor(((((cAF + cC) / 2) - K316T0) / K316dT)) + 1),2] + ((((((cAF + cC) / 2) - K316T0) / K316dT) - floor(((((cAF + cC) / 2) - K316T0) / K316dT))) * (KT[(floor(((((cAF + cC) / 2) - K316T0) / K316dT)) + 2),2] - KT[(floor(((((cAF + cC) / 2) - K316T0) / K316dT)) + 1),2]))), "r15")
        cAM = round((tanh((((sqrt((cAK / (cAL * twall))) * rm) * (gap1 * π / 180)) / 2)) / (((sqrt((cAK / (cAL * twall))) * rm) * (gap1 * π / 180)) / 2)), "r15")
        cAN = round((tanh((((sqrt((cAK / (cAL * twall))) * rm) * (gap2 * π / 180)) / 2)) / (((sqrt((cAK / (cAL * twall))) * rm) * (gap2 * π / 180)) / 2)), "r15")
        cAO = round((ri * ((π + (cAM * (gap1 * π / 180))) + (cAN * (gap2 * π / 180)))), "r15")
        cAP = round((tanh((((sqrt((cK / (cAL * twall))) * rm) * (saltgap * π / 180)) / 2)) / (((sqrt((cK / (cAL * twall))) * rm) * (saltgap * π / 180)) / 2)), "r15")
        cAQ = round((((((Nsalt / Nsteam) * 2) * π) * ri) * (saltbacked + ((1 - saltbacked) * cAP))), "r15")
        cAR = round((1 / (cAK * cAO)), "r15")
        cAS = round((1 / (cK * cAQ)), "r15")
        cAT = round(((2 * twall) / (cAL * wcontact)), "r15")
        if (hcontact == 0)
            conditional7 = 0
        else
            conditional7 = (1 / (hcontact * wcontact))
        end
        cAU = round(conditional7, "r15")
        cAV = round((((cAR + cAS) + cAT) + cAU), "r15")
        cAW = round((cB + ((cD / cAV) * cAR)), "r15")
        cAX = round((cD / cAV), "r15")
        cAY = round((cE / cAX), "r15")
        if i == 1
            cAZ = round(cAY, "r15")
        else
            cAZ = round((pAZ + cAY), "r15")
        end
        cBA = round((1 / (cAV * wcontact)), "r15")
        cBB = round((cB + (cAX * cAR)), "r15")
        cBC = round((cC - (cAX * cAS)), "r15")
        cBD = round(((cAX / (π * Di)) / 1000), "r15")
        cBE = round((cBD / Gw), "r15")
        if ((cB < Tpc) and (cBB > Tpc))
            conditional8 = 1
        else
            conditional8 = 0
        end
        cBF = round(conditional8, "r15")
        cBG = round(((((((gacc * TM[i,26]) * (Di ^ 4)) * cBD) * 1000) / (TM[i,23] * ((TM[i,22] / TM[i,21]) ^ 2))) / ((cL ^ 3.425) * (cM ^ 0.8))), "r15")
        cBH = round(((((4 * cBD) * 1000) * TM[i,26]) / (((Gw * TM[i,24]) * 1000) * cL)), "r15")
        cBI = round((Gw / TM[i,21]), "r15")
        cBJ = round(((8 / 6.0516) * (ln(((rough / Di) + ((7 / cL) ^ 0.9))) ^ (-2))), "r15")
        cBK = round((((((cBJ * cAY) / Di) * 0.5) * TM[i,21]) * (cBI ^ 2)), "r15")
        cBL = round(((TM[i,21] * gacc) * cAY), "r15")
        cBM = round(((8 / 6.0516) * (ln(((rough / Di) + ((7 / cG) ^ 0.9))) ^ (-2))), "r15")
        cBN = round((((((cBM * cAY) / Di) * 0.5) * TM[i,27]) * (cF ^ 2)), "r15")
        if i == 1
            mat = [cA, cB, cC, cD, cE, cF, cG, cH, cI, cJ, cK, cL, cM, cN, cO, cP, cQ, cR, cS, cT, cU, cV, cW, cX, cY, cZ, cAA, cAB, cAC, cAD, cAE, cAF, cAG, cAH, cAI, cAJ, cAK, cAL, cAM, cAN, cAO, cAP, cAQ, cAR, cAS, cAT, cAU, cAV, cAW, cAX, cAY, cAZ, cBA, cBB, cBC, cBD, cBE, cBF, cBG, cBH, cBI, cBJ, cBK, cBL, cBM, cBN]
        else
            mat = vcat(mat, [cA, cB, cC, cD, cE, cF, cG, cH, cI, cJ, cK, cL, cM, cN, cO, cP, cQ, cR, cS, cT, cU, cV, cW, cX, cY, cZ, cAA, cAB, cAC, cAD, cAE, cAF, cAG, cAH, cAI, cAJ, cAK, cAL, cAM, cAN, cAO, cAP, cAQ, cAR, cAS, cAT, cAU, cAV, cAW, cAX, cAY, cAZ, cBA, cBB, cBC, cBD, cBE, cBF, cBG, cBH, cBI, cBJ, cBK, cBL, cBM, cBN])
        end
        pBB = cBB
        pB = cB
        pAZ = cAZ
    end
    return mat
end `

## Embedded property data

### Water properties

This is the complete original Water\_Properties table: 1,381 rows, 555 to 900 K
in 0.25 K increments, at fixed 24 MPa. The workbook identifies it as IAPWS-95
data; this conversion copies those values and does not independently regenerate
or certify them.

Columns are T (K), h (kJ/kg), rho (kg/m³), cp (kJ/kg·K), mu (Pa·s), k (W/m·K),
beta (1/K). Display is suppressed for this large dataframe, but its complete
editable data are embedded in the calculation cell.

¢``` WP = ``T	h	rho	cp	mu	k	beta
555	1239.76876818352	772.758725547065	4.95059299086971	0.0000982797896074267	0.601523842983358	0.00210100523223878
555.25	1241.0067935643	772.352512150724	4.95361227830998	0.0000981825680592357	0.601202610973058	0.00210543591225651
555.5	1242.24557543788	771.94565535068	4.95664494829059	0.0000980854366121035	0.600880804168909	0.00210988604666428
555.75	1243.48511716121	771.538152622934	4.95969109144918	0.0000979883945220544	0.600558421704017	0.00211435577610885
556	1244.72542211399	771.130001425688	4.96275079929279	0.0000978914410452444	0.600235462702632	0.00211884524261174
556.25	1245.96649369894	770.72119919919	4.9658241642085	0.0000977945754379386	0.599911926280083	0.00212335458958615
556.5	1247.20833534196	770.311743365548	4.96891127947393	0.0000976977969564844	0.599587811542677	0.00212788396185428
556.75	1248.45095049239	769.901631328554	4.97201223926833	0.0000976011048572859	0.599263117587616	0.00213243350566515
557	1249.69434262323	769.490860473532	4.97512713868322	0.0000975044983967831	0.598937843502937	0.00213700336871189
557.25	1250.93851523136	769.079428167134	4.97825607373376	0.0000974079768314224	0.598611988367401	0.00214159370015019
557.5	1252.1834718378	768.667331757172	4.98139914137	0.0000973115394176325	0.598285551250413	0.0021462046506166
557.75	1253.42921598792	768.254568572445	4.98455643948819	0.000097215185411802	0.597958531211954	0.00215083637224684
558	1254.67575125166	767.841135922534	4.98772806694267	0.0000971189140702488	0.597630927302465	0.00215548901869514
558.25	1255.92308122382	767.427031097633	4.99091412355748	0.0000970227246491974	0.597302738562778	0.00216016274515305
558.5	1257.17120952427	767.012251368353	4.99411471013843	0.0000969266164047522	0.596973964024016	0.00216485770836917
558.75	1258.4201397982	766.596793985539	4.99732992848513	0.0000968305885928729	0.596644602707513	0.00216957406666853
559	1259.66987571638	766.180656180056	5.00055988140355	0.0000967346404693426	0.596314653624702	0.0021743119799732
559.25	1260.92042097543	765.763835162616	5.00380467271842	0.0000966387712897477	0.59598411577704	0.0021790716098223
559.5	1262.17177929801	765.346328123575	5.00706440728578	0.0000965429803094487	0.59565298815591	0.00218385311939253
559.75	1263.42395443316	764.928132232722	5.01033919100617	0.0000964472667835516	0.595321269742522	0.00218865667351955
560	1264.67695015652	764.509244639081	5.01362913083765	0.0000963516299668813	0.594988959507805	0.00219348243871922
560.25	1265.93077027059	764.089662470713	5.01693433480892	0.0000962560691139567	0.594656056412336	0.00219833058320897
560.5	1267.18541860503	763.669382834494	5.020254912033	0.0000961605834789593	0.594322559406215	0.00220320127693005
560.75	1268.44089901689	763.248402815917	5.02359097272085	0.0000960651723157078	0.59398846742898	0.00220809469156971
561	1269.69721539095	762.826719478866	5.0269426281953	0.0000959698348776287	0.593653779409495	0.00221301100058399
561.25	1270.95437163992	762.404329865409	5.03030999090521	0.0000958745704177283	0.593318494265855	0.0022179503792207
561.5	1272.2123717048	761.981230995576	5.03369317443969	0.0000957793781885647	0.592982610905278	0.00222291300454266
561.75	1273.4712195551	761.557419867135	5.0370922935428	0.000095684257442218	0.592646128223997	0.00222789905545167
562	1274.7309191892	761.132893455369	5.04050746412831	0.0000955892074302611	0.592309045107158	0.00223290871271256
562.25	1275.99147463455	760.707648712851	5.0439388032945	0.0000954942274037324	0.591971360428711	0.00223794215897745
562.5	1277.25288994808	760.281682569209	5.04738642933968	0.0000953993166131036	0.591633073051299	0.00224299957881097
562.75	1278.51516921641	759.854991930891	5.05085046177757	0.0000953044743082503	0.591294181826143	0.00224808115871539
563	1279.77831655622	759.427573680938	5.05433102135294	0.0000952096997384243	0.59095468559294	0.00225318708715627
563.25	1281.04233611451	758.99942467873	5.05782823005768	0.0000951149921522194	0.590614583179736	0.00225831755458862
563.5	1282.30723206895	758.570541759755	5.06134221114699	0.0000950203507975436	0.59027387340282	0.0022634727534834
563.75	1283.57300862816	758.140921735362	5.06487308915573	0.0000949257749215875	0.589932555066608	0.00226865287835425
564	1284.83967003208	757.710561392504	5.06842098991532	0.0000948312637707924	0.58959062696352	0.00227385812578514
564.25	1286.10722055227	757.279457493493	5.07198604057065	0.0000947368165908194	0.589248087873861	0.00227908869445799
564.5	1287.37566449223	756.84760677574	5.07556836959736	0.000094642432626517	0.588904936565698	0.00228434478518105
564.75	1288.64500618775	756.415005951499	5.07916810681929	0.0000945481111218897	0.588561171794748	0.00228962660091734
565	1289.91525000725	755.981651707609	5.08278538342632	0.0000944538513200663	0.588216792304245	0.002294934346814
565.25	1291.18640035212	755.547540705208	5.08642033199271	0.000094359652463263	0.587871796824803	0.00230026823023216
565.5	1292.45846165707	755.112669579495	5.090073086495	0.0000942655137927573	0.587526184074318	0.00230562846077644
565.75	1293.73143839048	754.677034939426	5.09374378233118	0.0000941714345488477	0.587179952757809	0.00231101525032626
566	1295.00533505475	754.24063336746	5.0974325563393	0.0000940774139708251	0.586833101567306	0.00231642881306641
566.25	1296.28015618668	753.803461419264	5.10113954681699	0.0000939834512969355	0.586485629181708	0.00232186936551903
566.5	1297.55590635784	753.365515623441	5.10486489354095	0.0000938895457643477	0.586137534266656	0.00232733712657555
566.75	1298.83259017491	752.926792481224	5.10860873778691	0.0000937956966091164	0.585788815474385	0.00233283231752956
567	1300.11021228009	752.487288466214	5.11237122234976	0.0000937019030661513	0.585439471443612	0.00233835516210974
567.25	1301.38877735147	752.04700002405	5.11615249156426	0.0000936081643691757	0.585089500799361	0.0023439058865139
567.5	1302.66829010341	751.605923572132	5.11995269132592	0.0000935144797506957	0.584738902152849	0.00234948471944327
567.75	1303.94875528696	751.164055499306	5.12377196911221	0.0000934208484419611	0.58438767410133	0.00235509189213736
568	1305.23017769022	750.721392165568	5.12761047400408	0.000093327269672931	0.584035815227962	0.00236072763840936
568.25	1306.51256213877	750.277929901739	5.13146835670805	0.0000932337426722355	0.583683324101644	0.00236639219468234
568.5	1307.79591349608	749.833665009153	5.13534576957851	0.0000931402666671381	0.58333019927688	0.00237208580002603
568.75	1309.08023666391	749.388593759338	5.13924286664032	0.0000930468408834988	0.58297643929362	0.00237780869619399
569	1310.36553658272	748.942712393696	5.14315980361186	0.0000929534645457369	0.582622042677121	0.00238356112766148
569.25	1311.65181823215	748.496017123154	5.14709673792873	0.0000928601368767887	0.582267007937767	0.0023893433416645
569.5	1312.9390866314	748.048504127853	5.1510538287672	0.0000927668570980737	0.581911333570941	0.00239515558823837
569.75	1314.22734683966	747.600169556798	5.15503123706878	0.0000926736244294517	0.581555018056852	0.00240099812025827
570	1315.51660395661	747.151009527508	5.15902912556472	0.0000925804380891829	0.581198059860366	0.00240687119347949
570.25	1316.80686312283	746.701020125686	5.16304765880105	0.0000924872972938902	0.580840457430863	0.00241277506657882
570.5	1318.09812952026	746.25019740484	5.16708700316428	0.0000923942012585153	0.580482209202052	0.00241871000119676
570.75	1319.39040837269	745.798537385956	5.17114732690699	0.0000923011491962806	0.580123313591822	0.00242467626197991
571	1320.68370494617	745.346036057104	5.17522880017452	0.0000922081403186446	0.579763769002055	0.00243067411662479
571.25	1321.97802454957	744.892689373088	5.17933159503161	0.0000921151738352618	0.579403573818465	0.00243670383592191
571.5	1323.27337253498	744.438493255072	5.18345588548971	0.0000920222489539396	0.579042726410422	0.00244276569380083
571.75	1324.56975429827	743.983443590193	5.18760184753469	0.0000919293648805948	0.578681225130776	0.00244885996737595
572	1325.86717527954	743.527536231176	5.19176965915527	0.000091836520819209	0.57831906831567	0.00245498693699327
572.25	1327.16564096365	743.070766995958	5.19595950037146	0.0000917437159717875	0.577956254284369	0.00246114688627763
572.5	1328.4651568807	742.61313166728	5.20017155326397	0.0000916509495383119	0.577592781339079	0.00246734010218107
572.75	1329.76572860659	742.154625992283	5.20440600200386	0.0000915582207166944	0.577228647764738	0.00247356687503201
573	1331.06736176354	741.695245682116	5.20866303288273	0.0000914655287027358	0.57686385182886	0.00247982749858509
573.25	1332.37006202057	741.234986411512	5.21294283434365	0.0000913728726900748	0.57649839178132	0.00248612227007229
573.5	1333.67383509414	740.773843818364	5.21724559701241	0.0000912802518701425	0.576132265854159	0.00249245149025473
573.75	1334.97868674858	740.311813503322	5.22157151372926	0.0000911876654321178	0.57576547226141	0.00249881546347506
574	1336.28462279675	739.848891029338	5.22592077958155	0.0000910951125628756	0.575398009198875	0.00250521449771159
574.25	1337.59164910057	739.385071921238	5.23029359193667	0.0000910025924469385	0.57502987484393	0.00251164890463283
574.5	1338.89977157157	738.920351665289	5.23469015047551	0.0000909101042664312	0.574661067355329	0.00251811899965281
574.75	1340.20899617149	738.454725708725	5.23911065722701	0.0000908176472010254	0.574291584872982	0.00252462510198845
575	1341.51932891289	737.988189459315	5.24355531660248	0.0000907252204278936	0.573921425517755	0.0025311675347164
575.25	1342.83077585974	737.520738284881	5.24802433543155	0.0000906328231216556	0.573550587391255	0.00253774662483252
575.5	1344.14334312799	737.052367512839	5.2525179229979	0.0000905404544543275	0.573179068575604	0.00254436270331131
575.75	1345.45703688627	736.583072429717	5.25703629107614	0.0000904481135952698	0.572806867133239	0.00255101610516697
576	1346.77186335643	736.112848280665	5.26157965396927	0.0000903557997111321	0.572433981106666	0.00255770716951554
576.25	1348.08782881422	735.641690268977	5.2661482285466	0.000090263511965802	0.572060408518252	0.00256443623963793
576.5	1349.40493958996	735.169593555573	5.27074223428273	0.0000901712495203482	0.57168614736999	0.00257120366304456
576.75	1350.72320206913	734.69655325851	5.27536189329691	0.0000900790115329671	0.571311195643261	0.00257800979154075
577	1352.04262269311	734.222564452456	5.28000743039335	0.0000899867971589252	0.57093555129861	0.00258485498129366
577.25	1353.36320795979	733.747622168175	5.28467907310218	0.000089894605550504	0.570559212275504	0.00259173959290034
577.5	1354.68496442431	733.271721391986	5.28937705172116	0.0000898024358569403	0.570182176492081	0.00259866399145713
577.75	1356.00789869972	732.794857065239	5.29410159935819	0.0000897102872243704	0.569804441844918	0.00260562854663025
578	1357.33201745773	732.317024083754	5.29885295197472	0.0000896181587957683	0.569426006208768	0.00261263363272802
578.25	1358.65732742936	731.83821729728	5.30363134842976	0.0000895260497108883	0.56904686743632	0.00261967962877409
578.5	1359.98383540573	731.358431508919	5.3084370305248	0.000089433959106203	0.568667023357938	0.00262676691858223
578.75	1361.31154823881	730.877661474562	5.31327024304984	0.0000893418861148414	0.5682864717814	0.00263389589083279
579	1362.64047284211	730.395901902296	5.31813123382989	0.0000892498298665262	0.567905210491628	0.00264106693915026
579.25	1363.97061619148	729.913147451835	5.32302025377243	0.0000891577894875132	0.56752323725044	0.00264828046218231
579.5	1365.30198532592	729.429392733902	5.32793755691617	0.0000890657641005237	0.56714054979626	0.00265553686368094
579.75	1366.6345873483	728.944632309624	5.3328834004803	0.0000889737528246811	0.566757145843849	0.00266283655258457
580	1367.96842942622	728.458860689915	5.33785804491473	0.0000888817547754438	0.566373023084027	0.00267017994310186
580.25	1369.3035187928	727.97207233485	5.34286175395172	0.0000887897690645395	0.565988179183386	0.00267756745479765
580.5	1370.6398627475	727.484261653025	5.34789479465792	0.0000886977947998967	0.565602611784015	0.00268499951267988
580.75	1371.97746865696	726.995423000909	5.35295743748785	0.000088605831085576	0.56521631850319	0.00269247654728872
581	1373.3163439559	726.505550682181	5.35804995633826	0.0000885138770216987	0.564829296933089	0.00269999899478739
581.25	1374.6564961479	726.014638947067	5.36317262860372	0.0000884219317043778	0.564441544640491	0.0027075672970547
581.5	1375.99793280638	725.522681991654	5.36832573523293	0.0000883299942256441	0.564053059166471	0.00271518190177939
581.75	1377.34066157542	725.029673957211	5.37350956078648	0.0000882380636733758	0.563663838026089	0.00272284326255635
582	1378.6846901707	724.535608929463	5.37872439349594	0.0000881461391312198	0.563273878708074	0.00273055183898541
582.25	1380.03002638042	724.040480937906	5.38397052532334	0.0000880542196785222	0.562883178674518	0.00273830809677072
582.5	1381.37667806626	723.544283955064	5.38924825202278	0.0000879623043902471	0.562491735360535	0.00274611250782373
582.75	1382.72465316429	723.047011895755	5.39455787320264	0.0000878703923369014	0.562099546173949	0.0027539655503672
583	1384.07395968601	722.548658616339	5.39989969238943	0.0000877784825844539	0.561706608494945	0.00276186770904189
583.25	1385.42460571927	722.049217913967	5.40527401709255	0.000087686574194258	0.561312919675746	0.00276981947501503
583.5	1386.7765994293	721.548683525799	5.41068115887066	0.0000875946662229697	0.560918477040267	0.00277782134609121
583.75	1388.12994905975	721.047049128215	5.41612143339947	0.000087502757722463	0.560523277883756	0.00278587382682596
584	1389.48466293371	720.54430833602	5.42159516054057	0.0000874108477397487	0.560127319472454	0.00279397742864088
584.25	1390.84074945474	720.040454701628	5.42710266441201	0.0000873189353168882	0.559730599043228	0.00280213266994177
584.5	1392.198217108	719.535481714233	5.43264427346018	0.0000872270194909062	0.559333113803209	0.00281034007623923
584.75	1393.55707446129	719.029382798975	5.43822032053314	0.0000871350992937054	0.558934860929424	0.00281860018027128
585	1394.9173301662	718.522151316078	5.4438311429557	0.0000870431737519748	0.55853583756842	0.00282691352212928
585.25	1396.2789929592	718.013780559984	5.4494770826057	0.000086951241887101	0.558136040835879	0.00283528064938576
585.5	1397.64207166281	717.50426375846	5.45515848599254	0.000086859302715073	0.557735467816232	0.00284370211722599
585.75	1399.00657518676	716.993594071714	5.46087570433634	0.0000867673552463933	0.557334115562272	0.00285217848858097
586	1400.3725125292	716.481764591464	5.46662909364995	0.0000866753984859786	0.556931981094747	0.00286071033426466
586.25	1401.73989277789	715.968768340013	5.47241901482195	0.0000865834314330649	0.556529061401955	0.00286929823311339
586.5	1403.10872511141	715.454598269309	5.47824583370131	0.00008649145308111	0.556125353439343	0.00287794277212809
586.75	1404.47901880044	714.939247259965	5.4841099211848	0.0000863994624176913	0.555720854129069	0.00288664454662058
587	1405.85078320904	714.422708120295	5.49001165330508	0.0000863074584244068	0.555315560359599	0.00289540416036193
587.25	1407.22402779591	713.904973585309	5.49595141132158	0.0000862154400767701	0.55490946898526	0.00290422222573482
587.5	1408.59876211573	713.386036315694	5.5019295818131	0.0000861234063441058	0.554502576825807	0.00291309936388903
587.75	1409.9749958205	712.865888896793	5.50794655677208	0.0000860313561894441	0.554094880665985	0.00292203620490004
588	1411.35273866093	712.344523837534	5.51400273370178	0.000085939288569409	0.553686377255058	0.00293103338793207
588.25	1412.73200048776	711.821933569386	5.52009851571454	0.0000858472024341121	0.553277063306374	0.00294009156140348
588.5	1414.11279125326	711.298110445244	5.52623431163316	0.0000857550967270365	0.552866935496878	0.00294921138315699
588.75	1415.49512101261	710.773046738334	5.53241053609396	0.000085662970384924	0.552455990466645	0.00295839352063314
589	1416.87899992538	710.246734641081	5.53862760965231	0.0000855708223376593	0.552044224818403	0.00296763865104774
589.25	1418.26443825706	709.719166263966	5.54488595889057	0.0000854786515081515	0.551631635117038	0.0029769474615734
589.5	1419.65144638051	709.190333634342	5.55118601652864	0.0000853864568122127	0.551218217889098	0.00298632064952554
589.75	1421.04003477758	708.660228695254	5.5575282215364	0.0000852942371584369	0.550803969622289	0.00299575892255174
590	1422.43021404065	708.12884330422	5.56391301924958	0.0000852019914480734	0.550388886764954	0.00300526299882666
590.25	1423.82199487423	707.596169231994	5.57034086148766	0.0000851097185749018	0.549972965725561	0.00301483360725058
590.5	1425.21538809662	707.062198161319	5.57681220667446	0.0000850174174251024	0.549556202872174	0.00302447148765249
590.75	1426.61040464156	706.526921685625	5.58332751996216	0.0000849250868771231	0.549138594531899	0.00303417739099892
591	1428.00705555993	705.990331307739	5.58988727335733	0.0000848327258015471	0.548720136990347	0.00304395207960643
591.25	1429.40535202148	705.452418438546	5.59649194585063	0.0000847403330609558	0.548300826491079	0.00305379632735992
591.5	1430.8053053166	704.913174395636	5.60314202354922	0.0000846479075097894	0.547880659235029	0.00306371091993589
591.75	1432.20692685811	704.372590401929	5.609837999812	0.0000845554479942076	0.547459631379947	0.00307369665503048
592	1433.6102281831	703.830657584251	5.61658037538899	0.0000844629533519418	0.547037739039788	0.0030837543425943
592.25	1435.01522095475	703.287366971914	5.62336965856291	0.0000843704224121514	0.546614978284138	0.00309388480507131
592.5	1436.42191696432	702.742709495246	5.63020636529496	0.0000842778539952726	0.546191345137601	0.00310408887764459
592.75	1437.83032813299	702.196675984109	5.63709101937345	0.0000841852469128666	0.545766835579184	0.00311436740848719
593	1439.24046651391	701.649257166365	5.64402415256707	0.0000840925999674637	0.54534144554167	0.00312472125902044
593.25	1440.65234429417	701.100443666349	5.65100630478032	0.0000839999119524065	0.544915170910993	0.00313515130417657
593.5	1442.06597379688	700.550226003263	5.65803802421423	0.000083907181651686	0.544488007525572	0.00314565843266986
593.75	1443.48136748324	699.998594589588	5.66511986753037	0.0000838144078397787	0.544059951175668	0.00315624354727326
594	1444.89853795471	699.445539729432	5.67225240001862	0.0000837215892814796	0.543630997602711	0.00316690756510192
594.25	1446.31749795516	698.891051616858	5.67943619576966	0.0000836287247317296	0.543201142498624	0.00317765141790442
594.5	1447.7382603731	698.335120334171	5.68667183785158	0.0000835358129354414	0.542770381505115	0.00318847605236086
594.75	1449.16083824394	697.777735850182	5.69395991849065	0.0000834428526273228	0.542338710212995	0.0031993824303884
595	1450.58524475233	697.218888018426	5.70130103925707	0.0000833498425316941	0.541906124161445	0.003210371529455
595.25	1452.01149323448	696.658566575353	5.70869581125505	0.0000832567813623036	0.541472618837297	0.00322144434290048
595.5	1453.4395971806	696.096761138472	5.71614485531795	0.0000831636678221392	0.541038189674287	0.0032326018802665
595.75	1454.86957023735	695.533461204465	5.72364880220845	0.0000830705006032347	0.540602832052305	0.0032438451676347
596	1456.30142621033	694.968656147263	5.73120829282361	0.0000829772783864743	0.540166541296626	0.00325517524797341
596.25	1457.73517906665	694.402335216077	5.73882397840547	0.0000828839998413925	0.539729312677132	0.00326659318149374
596.5	1459.17084293756	693.834487533382	5.74649652075716	0.0000827906636259669	0.539291141407509	0.00327810004601493
596.75	1460.60843212111	693.265102092883	5.75422659246439	0.0000826972683864122	0.538852022644449	0.00328969693733896
597	1462.04796108484	692.694167757409	5.76201487712305	0.0000826038127569649	0.538411951486821	0.00330138496963553
597.25	1463.48944446862	692.121673256777	5.76986206957278	0.0000825102953596659	0.537970922974835	0.0033131652758371
597.5	1464.93289708744	691.54760718562	5.77776887613647	0.0000824167148041386	0.537528932089191	0.00332503900804418
597.75	1466.37833393434	690.971958001145	5.78573601486654	0.0000823230696873611	0.53708597375021	0.00333700733794197
598	1467.82577018336	690.39471402086	5.79376421579773	0.0000822293585934335	0.536642042816947	0.00334907145722824
598.25	1469.27522119257	689.815863420258	5.80185422120628	0.0000821355800933432	0.536197134086305	0.003361232578052
598.5	1470.7267025072	689.235394230421	5.81000678587721	0.000082041732744719	0.535751242292102	0.00337349193346582
598.75	1472.18022986271	688.653294335611	5.81822267737757	0.0000819478150915871	0.535304362104153	0.00338585077788858
599	1473.63581918814	688.069551470773	5.82650267633835	0.0000818538256641153	0.53485648812731	0.00339831038758267
599.25	1475.0934866093	687.484153219005	5.83484757674346	0.0000817597629783556	0.534407614900507	0.00341087206114347
599.5	1476.55324845222	686.897087008976	5.84325818622679	0.000081665625535982	0.533957736895773	0.00342353712000243
599.75	1478.01512124659	686.308340112244	5.85173532637853	0.0000815714118240137	0.533506848517216	0.0034363069089458
600	1479.47912172926	685.717899640589	5.86027983305821	0.0000814771203145475	0.53305494410003	0.00344918279664512
600.25	1480.94526684784	685.125752543201	5.86889255671873	0.0000813827494644679	0.532602017909427	0.00346216617620606
600.5	1482.41357376444	684.531885603875	5.87757436273789	0.0000812882977151619	0.5321480641396	0.00347525846573031
600.75	1483.88405985941	683.936285438095	5.88632613176052	0.0000811937634922217	0.53169307691263	0.0034884611088953
601	1485.35674273521	683.338938490076	5.89514876004984	0.0000810991452051426	0.531237050277402	0.00350177557554969
601.25	1486.83164022035	682.739831029723	5.90404315984918	0.0000810044412470122	0.530779978208465	0.00351520336232663
601.5	1488.30877037344	682.13894914954	5.91301025975413	0.0000809096499941965	0.530321854604916	0.00352874599327465
601.75	1489.7881514873	681.536278761436	5.92205100509586	0.0000808147698060115	0.529862673289222	0.00354240502050744
602	1491.26980209326	680.931805593485	5.93116635833537	0.0000807197990243943	0.529402428006041	0.00355618202487261
602.25	1492.75374096542	680.325515186591	5.94035729946947	0.0000806247359735614	0.528941112421016	0.00357007861664006
602.5	1494.2399871251	679.717392891086	5.94962482644896	0.0000805295789596616	0.52847872011955	0.00358409643621144
602.75	1495.72855984544	679.107423863228	5.95896995560958	0.0000804343262704175	0.528015244605542	0.00359823715485097
603	1497.21947865597	678.495593061643	5.96839372211507	0.000080338976174763	0.527550679300125	0.00361250247543749
603.25	1498.71276334743	677.881885243652	5.97789718041482	0.0000802435269224662	0.527085017540351	0.00362689413324069
603.5	1500.20843397663	677.266284961524	5.98748140471433	0.0000801479767437478	0.526618252577873	0.00364141389671977
603.75	1501.70651087144	676.648776558645	5.997147489461	0.0000800523238488883	0.526150377577595	0.0036560635683478
604	1503.20701463594	676.029344165556	6.00689654984439	0.0000799565664278219	0.525681385616277	0.00367084498546109
604.25	1504.70996615565	675.407971695947	6.01672972231187	0.0000798607026497285	0.525211269681154	0.00368576002113462
604.5	1506.2153866029	674.784642842502	6.0266481651009	0.000079764730662606	0.524740022668482	0.00370081058508578
604.75	1507.72329744239	674.159341072668	6.03665305878741	0.0000796686485928387	0.524267637382089	0.00371599862460591
605	1509.23372043677	673.532049624304	6.04674560685179	0.0000795724545447503	0.523794106531877	0.00373132612552147
605.25	1510.74667765254	672.902751501224	6.05692703626278	0.0000794761466001479	0.523319422732312	0.00374679511318612
605.5	1512.26219146589	672.271429468627	6.06719859808016	0.0000793797228178527	0.522843578500863	0.00376240765350461
605.75	1513.78028456887	671.638066048408	6.0775615680759	0.0000792831812332204	0.522366566256432	0.00377816585398871
606	1515.30097997564	671.002643514331	6.08801724737717	0.0000791865198576441	0.52188837831773	0.00379407186484968
606.25	1516.82430102887	670.365143887109	6.09856696312806	0.0000790897366780507	0.521409006901638	0.00381012788012354
606.5	1518.35027140634	669.725548929333	6.10921206917436	0.0000789928296563799	0.520928444121538	0.00382633613883536
606.75	1519.8789151277	669.083840140264	6.11995394677023	0.0000788957967290496	0.520446681985589	0.00384269892620103
607	1521.41025656141	668.439998750487	6.13079400530893	0.0000787986358064058	0.519963712394982	0.00385921857487008
607.25	1522.9443204319	667.794005716437	6.14173368307638	0.0000787013447721603	0.519479527142162	0.00387589746620807
607.5	1524.48113182683	667.145841714767	6.15277444803138	0.0000786039214828121	0.518994117909008	0.00389273803162399
607.75	1526.02071620466	666.49548713656	6.16391779861114	0.0000785063637670519	0.518507476264987	0.00390974275394142
608	1527.56309940236	665.842922081363	6.17516526456482	0.0000784086694251465	0.518019593665233	0.00392691416881761
608.25	1529.10830764334	665.188126351119	6.18651840781415	0.0000783108362283166	0.517530461448644	0.00394425486620894
608.5	1530.65636754558	664.531079443867	6.19797882334441	0.0000782128619180871	0.517040070835903	0.00396176749188858
608.75	1532.20730613007	663.871760547279	6.20954814012661	0.0000781147442056199	0.516548412927448	0.00397945474901739
609	1533.76115082937	663.210148532048	6.22122802206967	0.0000780164807710338	0.51605547870143	0.00399731939976673
609.25	1535.31792949648	662.546221945059	6.23302016900736	0.0000779180692627008	0.515561259011624	0.0040153642670007
609.5	1536.87767041398	661.879959002364	6.2449263177191	0.0000778195072965198	0.515065744585262	0.0040335922360167
609.75	1538.44040230336	661.211337581968	6.25694824298692	0.0000777207924551731	0.514568926020864	0.00405200625634806
610	1540.00615433466	660.540335216422	6.26908775868889	0.0000776219222873625	0.514070793786006	0.00407060934362954
610.25	1541.57495613641	659.866929085152	6.28134671893307	0.0000775228943070153	0.513571338215031	0.00408940458153245
610.5	1543.1468378058	659.191096006616	6.29372701923049	0.0000774237059924758	0.51307054950672	0.0041083951237671
610.75	1544.72182991922	658.512812430196	6.30623059771095	0.0000773243547856663	0.512568417721923	0.00412758419615903
611	1546.29996354303	657.832054427877	6.31885943638254	0.0000772248380912268	0.512064932781129	0.0041469750988007
611.25	1547.88127024473	657.148797685636	6.33161556243767	0.0000771251532756247	0.511560084461974	0.00416657120828309
611.5	1549.46578210339	656.463017495989	6.34450104956688	0.0000770252976664531	0.511053862397689	0.0041863759799489
611.75	1551.05353172537	655.774688743579	6.35751801951201	0.000076925268550669	0.510546256070757	0.00420639295052179
612	1552.64455225082	655.083785903502	6.37066864330254	0.0000768250631748139	0.510037254815741	0.00422662574026085
612.25	1554.23887736987	654.390283026615	6.38395514290666	0.0000767246787432354	0.509526847813021	0.00424707805576063
612.5	1555.83654133465	653.694153730807	6.39737979276081	0.0000766241124172469	0.509015024086925	0.0042677536925769
612.75	1557.43757897266	652.99537119069	6.41094492139473	0.0000765233613140568	0.508501772502887	0.00428865653801004
613	1559.04202570044	652.293908127021	6.42465291311598	0.0000764224225056741	0.507987081764593	0.00430979057399217
613.25	1560.64991753779	651.589736795729	6.43850620976048	0.0000763212930177675	0.507470940411015	0.00433115988008842
613.5	1562.26129112232	650.882828976658	6.45250731250772	0.0000762199698284998	0.506953336813425	0.00435276863661097
613.75	1563.87618372458	650.173155961915	6.46665878376696	0.0000761184498673175	0.506434259172316	0.00437462112785635
614	1565.49463326354	649.460688543834	6.48096324913628	0.000076016730013701	0.505913695514266	0.00439672174546924
614.25	1567.1166783227	648.745397002605	6.49542339943683	0.0000759148070958814	0.505391633688745	0.00441907499193773
614.5	1568.74235816666	648.027251093411	6.51004199282778	0.0000758126778895021	0.504868061364809	0.00444168548422878
614.75	1570.37171275815	647.306220033262	6.52482185700193	0.000075710339116253	0.5043429660278	0.00446455795756484
615	1572.00478277581	646.582272487263	6.53976589147137	0.0000756077874424422	0.503816334975877	0.00448769726935726
615.25	1573.64160963234	645.855376554531	6.55487706994033	0.0000755050194775315	0.503288155316552	0.00451110840329263
615.5	1575.28223549342	645.125499753606	6.57015844277445	0.0000754020317726221	0.502758413963119	0.00453479647358743
615.75	1576.92670329716	644.392609007347	6.5856131395689	0.0000752988208188807	0.502227097630988	0.00455876672941597
616	1578.57505677426	643.656670627356	6.60124437181936	0.0000751953830459213	0.501694192833972	0.00458302455951878
616.25	1580.2273404688	642.917650297848	6.61705543570162	0.0000750917148201272	0.501159685880475	0.00460757549700146
616.5	1581.88359975981	642.175513058973	6.63304971496414	0.0000749878124429147	0.50062356286959	0.00463242522433212
616.75	1583.5438808835	641.430223289573	6.64923068393895	0.0000748836721489399	0.500085809687136	0.00465757957854701
617	1585.20823095632	640.681744689313	6.6656019106769	0.0000747792901042378	0.499546412001579	0.0046830445566749
617.25	1586.87669799879	639.930040260237	6.68216706021141	0.0000746746624043045	0.499005355259901	0.0047088263213884
617.5	1588.54933096015	639.17507228761	6.69892989795947	0.0000745697850721008	0.498462624683337	0.00473493120689708
617.75	1590.22617974393	638.416802320129	6.71589429326401	0.0000744646540559933	0.497918205263051	0.00476136572509051
618	1591.90729523435	637.655191149429	6.73306422308446	0.0000743592652276216	0.497372081755719	0.0047881365719437
618.25	1593.59272932373	636.890198788823	6.75044377584435	0.0000742536143796835	0.496824238678995	0.00481525063420043
618.5	1595.28253494084	636.121784451303	6.76803715544165	0.0000741476972236465	0.496274660306909	0.00484271499634523
618.75	1596.97676608031	635.349906526718	6.78584868543065	0.0000740415093873701	0.495723330665133	0.00487053694787997
619	1598.67547783303	634.574522558161	6.80388281338241	0.0000739350464126496	0.495170233526197	0.00489872399091795
619.25	1600.37872641781	633.795589217419	6.82214411543491	0.000073828303752659	0.494615352404548	0.00492728384811558
619.5	1602.086569214	633.013062279587	6.84063730103888	0.00007372127676931	0.494058670551545	0.00495622447095289
619.75	1603.79906479554	632.226896596695	6.85936721791105	0.0000736139607305073	0.493500170950357	0.00498555404838443
620	1605.51627296608	631.437046070336	6.87833885720568	0.0000735063508072983	0.492939836310708	0.00501528101587979
620.25	1607.23825479558	630.64346362331	6.89755735891176	0.0000733984420709263	0.492377649063579	0.00504541406486853
620.5	1608.96507265816	629.84610117014	6.91702801749158	0.0000732902294897604	0.491813591355759	0.00507596215261725
620.75	1610.6967902715	629.044909586498	6.93675628776855	0.000073181707926117	0.491247645044309	0.00510693451255419
621	1612.43347273765	628.239838677441	6.95674779107982	0.0000730728721329578	0.49067979169092	0.0051383406650696
621.25	1614.17518658548	627.430837144415	6.97700832170575	0.0000729637167504578	0.490110012556145	0.00517019042881426
621.5	1615.92199981476	626.617852550995	6.99754385358977	0.0000728542363024472	0.489538288593559	0.0052024939325215
621.75	1617.6739819419	625.800831287253	7.01836054736519	0.0000727444251927073	0.488964600443763	0.00523526162738303
622	1619.43120404759	624.979718532758	7.03946475770225	0.0000726342777011294	0.488388928428331	0.00526850430000392
622.25	1621.19373882625	624.154458218075	7.06086304099486	0.0000725237879797167	0.487811252543613	0.00530223308597193
622.5	1622.96166063741	623.324992984773	7.08256216340124	0.0000724129500484343	0.487231552454462	0.00533645948406902
622.75	1624.73504555927	622.491264143772	7.1045691092605	0.0000723017577908876	0.486649807487832	0.00537119537116498
623	1626.51397144428	621.653211632052	7.12689108990199	0.0000721902049498335	0.48606599662629	0.00540645301782548
623.25	1628.29851797706	620.810773967604	7.14953555286941	0.0000720782851225114	0.485480098501441	0.00544224510467532
623.5	1630.08876673466	619.963888202494	7.17251019158257	0.0000719659917557805	0.484892091387221	0.00547858473955997
623.75	1631.88480124922	619.112489874082	7.19582295545641	0.0000718533181410689	0.484301953193151	0.0055154854755428
624	1633.68670707338	618.256512954112	7.21948206050896	0.0000717402574091049	0.483709661457451	0.00555296132979607
624.25	1635.49457184824	617.39588979578	7.24349600047656	0.0000716268025244422	0.483115193340108	0.00559102680342214
624.5	1637.30848537428	616.530551078546	7.26787355846877	0.0000715129462797552	0.482518525615863	0.00562969690226529
624.75	1639.12853968516	615.660425750615	7.29262381919212	0.0000713986812898975	0.481919634667127	0.00566898715876892
625	1640.95482912479	614.785440968973	7.31775618177359	0.0000712839999857099	0.481318496476819	0.00570891365493677
625.25	1642.78745042751	613.905522036923	7.34328037321463	0.0000711688946075785	0.480715086621209	0.00574949304645787
625.5	1644.62650280191	613.020592338839	7.36920646251711	0.0000710533571987052	0.480109380262647	0.00579074258807154
625.75	1646.47208801806	612.130573272211	7.395544875511	0.0000709373795981097	0.479501352142338	0.00583268016023142
626	1648.32431049876	611.235384176645	7.42230641043114	0.0000708209534333173	0.478890976573048	0.00587532429715717
626.25	1650.18327741458	610.334942259836	7.44950225427933	0.0000707040701127481	0.478278227431862	0.00591869421634417
626.5	1652.04909878324	609.429162520195	7.47714400002384	0.0000705867208177603	0.477663078152908	0.00596280984962895
626.75	1653.92188757332	608.517957666152	7.50524366467629	0.0000704688964943666	0.477045501720188	0.00600769187588959
627	1655.80175981261	607.601238031774	7.53381370830594	0.0000703505878445735	0.476425470660416	0.00605336175549303
627.25	1657.68883470139	606.678911488652	7.56286705403981	0.0000702317853173493	0.475802957035976	0.00609984176658442
627.5	1659.58323473079	605.750883353788	7.59241710911097	0.0000701124790991896	0.475177932437995	0.00614715504333685
627.75	1661.48508580656	604.817056293294	7.622477787016	0.000069992659104262	0.47455036797955	0.00619532561627965
628	1663.39451737851	603.877330221716	7.65306353084816	0.0000698723149641152	0.473920234289081	0.00624437845483269
628.25	1665.31166257599	602.931602196688	7.68418933788018	0.0000697514360169186	0.473287501504013	0.00629433951218886
628.5	1667.23665834964	601.979766308711	7.71587078546985	0.0000696300112962177	0.472652139264638	0.00634523577268702
628.75	1669.16964561978	601.021713565832	7.74812405837238	0.0000695080296939403	0.47201411667547	0.006397095301836
629	1671.11076942975	600.057331775101	7.780965977438	0.0000693854797347524	0.471373402340223	0.00644994729898354
629.25	1673.06017911623	599.086505408003	7.81441403039975	0.0000692623492041458	0.470729964420826	0.00650382215379881
629.5	1675.01802846958	598.1091154791	7.84848640341907	0.0000691386257988559	0.470083770515006	0.00655875150444745
629.75	1676.98447591904	597.125039400332	7.88320201529898	0.0000690142968467493	0.469434787697684	0.00661476830058008
630	1678.95968471883	596.13415083705	7.91858055320521	0.000068889349292328	0.46878298251865	0.00667190686929782
630.25	1680.94382314491	595.136319555443	7.9546425105003	0.0000687637696813341	0.468128321000049	0.00673020298511307
630.5	1682.93706470153	594.131411262406	7.99140922675841	0.0000686375441446081	0.467470768634683	0.00678969394405809
630.75	1684.93958833796	593.119287437597	8.02890293009713	0.0000685106583811863	0.466810290385308	0.00685041864220894
631	1686.95157867623	592.099805157107	8.06714678198911	0.0000683830976405796	0.466146850685006	0.00691241765893858
631.25	1688.97322625032	591.072816908298	8.10616492472297	0.0000682548467041899	0.465480413438775	0.00697573334522788
631.5	1691.0047277576	590.03817039535	8.14598253169417	0.000068125889865825	0.464810942026539	0.00704040991738534
631.75	1693.04628632317	588.995708334872	8.18662586072948	0.0000679962109112466	0.464138399307677	0.00710649355656905
632	1695.09811177804	587.945268241078	8.2281223106568	0.0000678657930967094	0.463462747627342	0.0071740325145217
632.25	1697.16042095172	586.886682199858	8.27050048135712	0.0000677346191264241	0.462783948824732	0.00724307722597669
632.5	1699.23343798047	585.819776631079	8.31379023755204	0.0000676026711288847	0.462101964243569	0.00731368042822493
632.75	1701.31739463183	584.744372038429	8.35802277660321	0.0000674699306319965	0.461416754745074	0.00738589728837715
633	1703.41253064674	583.660282745993	8.40323070062825	0.0000673363785369262	0.460728280723713	0.00745978553890811
633.25	1705.5190941002	582.567316620745	8.4494480932621	0.0000672019950905998	0.460036502126042	0.00753540562211686
633.5	1707.63734178176	581.465274780117	8.49671060142128	0.0000670667598567723	0.459341378473066	0.00761282084419215
633.75	1709.76753959715	580.353951283625	8.54505552247172	0.0000669306516855694	0.458642868886491	0.0076920975396502
634	1711.90996299238	579.233132807536	8.59452189723122	0.0000667936486814115	0.457940932119332	0.00777330524697239
634.25	1714.06489740185	578.102598301534	8.64515060928101	0.0000666557281692208	0.457235526591458	0.00785651689635094
634.5	1716.23263872222	576.9621186261	8.69698449111721	0.0000665168666587939	0.456526610430597	0.00794180901055329
634.75	1718.41349381361	575.811456169351	8.7500684377175	0.0000663770398072206	0.455814141519503	0.00802926192000269
635	1720.60778103035	574.65036444195	8.80444952816626	0.0000662362223792248	0.455098077550018	0.00811895999329462
635.25	1722.81583078306	573.478587648515	8.8601771560518	0.0000660943882052768	0.454378376084865	0.00821099188449925
635.5	1725.0379861347	572.295860233922	8.91730316942208	0.0000659515101373319	0.45365499462813	0.00830545079873522
635.75	1727.27460342886	571.101906406516	8.97588202092135	0.0000658075600025188	0.452927890707525	0.00840243477723987
636	1729.52605297315	569.896439616566	9.03597093042188	0.0000656625085520619	0.452197021959239	0.00850204700599681
636.25	1731.79271973661	568.679162031557	9.09763005829935	0.0000655163254108635	0.451462346239888	0.00860439614505924
636.5	1734.07500411802	567.449763952529	9.16092269418886	0.0000653689790206551	0.450723821738836	0.00870959668686564
636.75	1736.37332275004	566.207923207574	9.22591545999976	0.0000652204365814543	0.449981407113176	0.00881776934177596
637	1738.68810936361	564.953304499203	9.29267853016056	0.0000650706639884378	0.449235061636629	0.00892904145606485
637.25	1741.0198156946	563.68555872462	9.3612858692722	0.0000649196257667657	0.448484745376115	0.00904354746296346
637.5	1743.36891247652	562.404322227126	9.43181549195904	0.0000647672849991592	0.447730419379028	0.00916142937509409
637.75	1745.73589048015	561.109216018633	9.50434974403048	0.0000646136032514448	0.446972045896722	0.00928283731715422
638	1748.12126163586	559.799844939806	9.57897560967523	0.0000644585404919528	0.446209588632764	0.00940793010713889
638.25	1750.52556023447	558.475796763687	9.65578504690643	0.0000643020550056692	0.445443013025434	0.00953687589022878
638.5	1752.94934421596	557.136641235872	9.73487535480182	0.0000641441033024394	0.444672286568367	0.00966985283173153
638.75	1755.3931965543	555.78192904533	9.8163495764726	0.0000639846400186647	0.443897379174767	0.00980704987616252
639	1757.85772674813	554.411190719043	9.90031694232289	0.0000638236178118461	0.443118263591487	0.00994866758065188
639.25	1760.34357242808	553.023935432815	9.98689335887189	0.0000636609872472465	0.44233491587026	0.0100949190321162
639.5	1762.85140108644	551.619649735792	10.0762019487204	0.0000634966966766157	0.44154731590755	0.0102460308582029
639.75	1765.38191196968	550.197796153649	10.16837365095	0.0000633306921049091	0.440755448051111	0.0104022443483789
640	1767.93583809739	548.757811708959	10.2635478860072	0.0000631629170501019	0.439959301808431	0.0105638166926883
640.25	1770.51394848298	547.299106291455	10.3618732994578	0.0000629933123881019	0.439158872645075	0.0107310223633626
640.5	1773.11705053999	545.821060898708	10.4635085930211	0.000062821816185722	0.438354162905783	0.0109041546543946
640.75	1775.74599271047	544.323025718264	10.5686234573434	0.0000626483635185871	0.437545182871753	0.0110835274045951
641	1778.40166734179	542.804318032964	10.6773996222616	0.0000624728862722457	0.436731951977352	0.0112694769319975
641.25	1781.08501383562	541.26421993448	10.7900320425554	0.0000622953129252347	0.435914500216467	0.0114623642114623
641.5	1783.79702213203	539.701975794338	10.906730243795	0.0000621155683085686	0.435092869759683	0.0116625773388735
641.75	1786.53873652515	538.116789505792	11.0277198504241	0.0000619335733440551	0.434267116839555	0.0118705343212817
642	1789.3112599086	536.507821415619	11.1532443319308	0.000061749244752461	0.43343731392953	0.0120866862562345
642.25	1792.11575847875	534.874184932945	11.2835670018612	0.0000615624947310044	0.432603552283421	0.0123115209620004
642.5	1794.95346697765	533.214942753864	11.4189733158255	0.0000613732305939464	0.431765944895169	0.0125455671405094
642.75	1797.82569455045	531.529102649908	11.5597735218044	0.0000611813543714008	0.430924629959295	0.0127893991677688
643	1800.73383132068	529.815612744976	11.7063057283284	0.0000609867623589139	0.430079774922835	0.0130436426284965
643.25	1803.6793557769	528.073356217986	11.8589394665266	0.0000607893446121885	0.429231581248411	0.0133089807307054
643.5	1806.66384315963	526.301145285304	12.0180798459789	0.0000605889843717497	0.428380290004684	0.0135861617788382
643.75	1809.6889749207	524.497714429087	12.1841724090927	0.0000603855574161993	0.427526188478592	0.0138760078938576
644	1812.75654953927	522.661712649345	12.3577088319896	0.0000601789313207666	0.42666961797308	0.0141794252462068
644.25	1815.86849486787	520.791694627103	12.5392336338289	0.0000599689646116447	0.42581098304714	0.0144974160945205
644.5	1819.02688230058	518.886110585893	12.7293521006024	0.0000597555057954933	0.424950762477384	0.0148310930034969
644.75	1822.23394311804	516.943294593356	12.928739675335	0.0000595383922391763	0.424089522277778	0.0151816956992536
645	1825.49208736491	514.961451057087	13.138153113937	0.0000593174488775064	0.423227931204872	0.0155506111092101
645.25	1828.80392580456	512.938639013861	13.3584437867664	0.0000590924867100872	0.422366779226244	0.0159393972831906
645.5	1832.17229549281	510.87275383416	13.5905735779785	0.0000588633010529907	0.421506999560691	0.0163498120289712
645.75	1835.60028971986	508.761505802034	13.8356339493157	0.000058629669494443	0.420649694989448	0.0167838473103581
646	1839.09129318062	506.602394961239	14.0948688598161	0.0000583913494986736	0.419796169284324	0.0172437706930315
646.25	1842.64902344452	504.392681467993	14.3697023970224	0.0000581480755883154	0.418947964744585	0.0177321754355163
646.5	1846.2775800299	502.129350529817	14.6617721759569	0.0000578995560218114	0.418106907002744	0.0182520412068169
646.75	1849.98150268389	499.809070806857	14.9729698122589	0.0000576454688647297	0.417275158435955	0.018806807893674
647	1853.76584081816	497.428144918482	15.3054900830292	0.0000573854573343879	0.416455281695716	0.01940046555572
647.25	1857.636236553	494.982450351623	15.6618907783322	0.0000571191242667777	0.415650315002511	0.020037664345397
647.5	1861.59902427351	492.467368793476	16.0451656961624	0.0000568460255351087	0.414863860943236	0.0207238490978624
647.75	1865.66135041604	489.877701356527	16.458833814359	0.000056565662200623	0.414100190401873	0.0214654244481315
648	1869.83131792328	487.207566741395	16.907048313941	0.0000562774711464786	0.413364362916215	0.022269957631907
648.25	1874.11816061938	484.450278679745	17.3947297639099	0.000055980813887582	0.412662363590116	0.023146427481191
648.5	1878.53245625209	481.598198413834	17.9277295279429	0.000055674963213909	0.412001257380105	0.0241055314351297
648.75	1883.08638003456	478.642557095139	18.5130267024543	0.0000553590872436979	0.411389350325824	0.0251600581615181
649	1887.79401879887	475.573242411762	19.1589692066576	0.0000550322304613739	0.410836358615664	0.0263253462536461
649.25	1892.67174651883	472.378543014485	19.8755606544197	0.0000546932912319019	0.410353557534594	0.0276198347827487
649.5	1897.7386798141	469.044844545558	20.6747997177056	0.0000543409953649383	0.409953885988335	0.0290657205173434
649.75	1903.01722456833	465.556271605128	21.571070968834	0.0000539738653550335	0.409651955508017	0.0306897236693215
650	1908.5337259272	461.894272848715	22.5815788958863	0.0000535901852122686	0.409463890557129	0.0325239509691128
650.25	1914.31923007521	458.037151710155	23.7268036584546	0.0000531879612837302	0.409406900020241	0.0346068203070334
650.5	1920.41035908715	453.959554192421	25.0309414005444	0.0000527648802709579	0.409498464398917	0.036983979360399
650.75	1926.85028897835	449.631938434708	26.5222843980378	0.0000523182668832829	0.409755053403132	0.0397091287978359
651	1933.68981351363	445.020062566513	28.2335319929014	0.0000518450448217267	0.410190436504159	0.0428447091298567
651.25	1940.98848962174	440.084524977594	30.2021830145972	0.0000513417052974819	0.41081403694204	0.0464626741216546
651.5	1948.81594495579	434.780337006258	32.4715969858552	0.000050804284271388	0.41163055282554	0.0506463375022277
651.75	1957.25367701805	429.056336031022	35.0942208592717	0.0000502283377762748	0.412643240825717	0.055495930328107
652	1966.398218173	422.853870440866	38.1399157778526	0.0000496088757988683	0.41386434629075	0.0611432106139888
652.25	1976.36746981667	416.103575275853	41.7138047343092	0.0000489401628666733	0.415335800505085	0.0677834163408799
652.5	1987.31319040497	408.718379140183	45.9883387511303	0.0000482152263028748	0.417159628257315	0.0757336640402564
652.75	1999.44356117395	400.580631676202	51.2518168134988	0.0000474248704280059	0.419529844866298	0.0855223082703423
653	2013.05950071134	391.522284963545	57.967610256993	0.000046556049760757	0.422745905319152	0.0979977945331017
653.25	2028.60410517573	381.301597591731	66.8088790048871	0.0000455897552532353	0.42716276836958	0.114387032020731
653.5	2046.70502334646	369.595369697706	78.527975698674	0.000044499674957139	0.432972595000627	0.136025591180873
653.75	2068.12813061444	356.066601264067	93.2994781897863	0.0000432564039305229	0.439670606350528	0.163048790971531
654	2093.45920675792	340.614310098404	109.184711214939	0.0000418478182937617	0.445266411423301	0.191413387014318
654.25	2122.33909694049	323.828112632585	120.404377588989	0.0000403210559227269	0.445595224905744	0.210041313046353
654.5	2152.70623901871	307.20785187046	120.4747933969	0.000038812027379626	0.436353221359112	0.207740820283011
654.75	2181.75259152667	292.299982001229	110.833281735733	0.0000374736574437759	0.418781020882627	0.188452428897338
655	2207.86393276819	279.69065994605	97.9638597460425	0.0000363677386110409	0.398051791870238	0.164293553453739
655.25	2230.80751527299	269.197702277345	85.8719362894609	0.000035474847609901	0.377816764954329	0.142211973743949
655.5	2250.96584339903	260.407969331733	75.734748760441	0.0000347506297645713	0.35950624649535	0.124013633879958
655.75	2268.83474623184	252.936243053211	67.5080183257326	0.0000341541115619444	0.343358646760676	0.109425786069693
656	2284.84986062509	246.483931073885	60.8422316455369	0.0000336540670891563	0.329185836254083	0.0977188977147072
656.25	2299.35672823707	240.830821507531	55.3893672495413	0.000033227930587971	0.316702457529148	0.0882170038271621
656.5	2312.62221812942	235.81525822482	50.8709173192819	0.0000328594835910152	0.305636334204647	0.080394984676039
656.75	2324.85242579128	231.317189621498	47.0771240251861	0.0000325369287687947	0.29575648738797	0.0738642930961537
657	2336.2080731237	227.24594681269	43.8521524541648	0.0000322515302250945	0.286874271763422	0.0683398621673536
657.25	2346.81614013195	223.531823004852	41.0797794544994	0.0000319966949406274	0.278837229579311	0.0636111447115867
657.5	2356.77832152287	220.120305682951	38.6723912124422	0.0000317673552338713	0.271522036543437	0.0595206820734147
657.75	2366.1771331639	216.968089514267	36.5630693295238	0.0000315595493740959	0.264828354472353	0.0559490188766777
658	2375.08034700719	214.040278706655	34.7000051327663	0.0000313701322101578	0.258673909572338	0.0528042110312321
658.25	2383.54424751709	211.308390725312	33.0425581520622	0.0000311965719468187	0.252990671571652	0.0500145036350652
658.5	2391.61605376118	208.748907562999	31.5584527875478	0.0000310368048688112	0.247721915368646	0.0475231695250483
658.75	2399.33574500245	206.34220720897	30.2217616565444	0.0000308891297093143	0.242819960772216	0.0452848240036929
659	2406.73745462019	204.071763480852	29.0114363120043	0.0000307521296103589	0.23824442529861	0.043262757220061
659.25	2413.85054758892	201.923538327385	27.9102228304454	0.0000306246136090782	0.233960863938034	0.0414269765603983
659.5	2420.70046299209	199.885514277749	26.9038512960038	0.0000305055721613964	0.229939701631783	0.0397527509524334
659.75	2427.3093798976	197.947330396025	25.9804226659336	0.0000303941429077195	0.226155388473011	0.0382195147405171
660	2433.69674887766	196.099995695095	25.1299396560998	0.000030289584014947	0.222585725631971	0.036810032539226
660.25	2439.87972020176	194.335661233294	24.3439439806475	0.0000301912531950452	0.219211323199123	0.0355097558915921
660.5	2445.87349174269	192.647437176302	23.6152330337967	0.0000300985910275277	0.216015160794133	0.0343063225741969
660.75	2451.69159389495	191.029244678329	22.9376365565252	0.0000300111075812625	0.212982228878427	0.0331891631820788
661	2457.3461246326	189.475694990783	22.3058390593006	0.0000299283715915196	0.210099233941584	0.0321491892455278
661.25	2462.84794476532	187.981990056403	21.7152374819977	0.0000298500016349341	0.207354354621204	0.0311785439224622
661.5	2468.20684117338	186.543840201748	21.1618262343598	0.0000297756588805384	0.204737038727745	0.0302704011614923
661.75	2473.43166409176	185.157395544805	20.6421036917549	0.0000297050410944535	0.202237833344035	0.0294188027355841
662	2478.53044321803	183.819188485288	20.1529956361938	0.0000296378776495372	0.19984824183971	0.0286185251044435
662.25	2483.5104864292	182.526085212766	19.6917921803882	0.0000295739253465123	0.197560602922161	0.0278649699509027
662.5	2488.37846412891	181.275244600085	19.2560954948864	0.0000295129648948231	0.195367987833256	0.0271540736408075
662.75	2493.14048165398	180.064083182284	18.8437762483129	0.0000294547979333126	0.193264112570505	0.0264822319115604
663	2497.80214170521	178.890245178727	18.4529371185957	0.0000293992444952733	0.191243262612138	0.0258462368935267
663.25	2502.36859840154	177.751576717491	18.0818820763586	0.0000293461408414001	0.189300228099907	0.0252432241792563
663.5	2506.84460426647	176.646103579279	17.7290904064572	0.0000292953375989795	0.187430247809223	0.0246706281253606
663.75	2511.23455122416	175.57201190328	17.393194639252	0.0000292466981572811	0.185628960535453	0.0241261439358661
664	2515.54250649593	174.527631397365	17.0729617243041	0.0000292000972783426	0.183892362766103	0.0236076953603434
664.25	2519.77224413822	173.51142067481	16.7672769057471	0.0000291554198896582	0.182216771701948	0.0231134070631608
664.5	2523.92727284012	172.521954404373	16.4751298589977	0.00002911256003117	0.180598792847542	0.0226415808967747
664.75	2528.01086049975	171.55791201265	16.1956027283373	0.0000290714199336822	0.179035291519294	0.0221906754521567
665	2532.02605601586	170.618067720404	15.9278597689797	0.0000290319092096642	0.177523367724335	0.0217592883717089
665.25	2535.97570866484	169.701281729149	15.6711383486566	0.0000289939441405156	0.176060333949008	0.0213461409999489
665.5	2539.86248537631	168.806492403219	15.4247411055762	0.0000289574470469316	0.174643695467459	0.0209500650202489
665.75	2543.68888617487	167.932709315994	15.1880290933854	0.000028922345731095	0.173271132839226	0.0205699907847969
666	2547.45725801651	167.079007048787	14.9604157715505	0.0000288885729811619	0.171940486314215	0.0202049370932946
666.25	2551.16980721557	166.24451964713	14.7413617221828	0.0000288560661299356	0.170649741904084	0.0198540022152124
666.5	2554.82861063125	165.428435653017	14.5303699931126	0.0000288247666608273	0.169397018913711	0.0195163559830035
666.75	2558.43562575906	164.629993643033	14.3269819824154	0.000028794619855193	0.168180558755123	0.0191912328103729
667	2561.99269985356	163.848478212106	14.1307737924755	0.0000287655744759813	0.166998714890854	0.0188779255119985
667.25	2565.50157819181	163.083216350706	13.9413529923408	0.000028737582483326	0.165849943774281	0.0185757798195421
667.5	2568.96391157288	162.333574170364	13.7583557360788	0.00002871059877832	0.164732796672143	0.0182841895042599
667.75	2572.38126313676	161.598953938197	13.5814441923398	0.0000286845809717051	0.163645912269382	0.0180025920294487
668	2575.75511457546	160.878791386255	13.4103042466467	0.0000286594891746486	0.162588009969261	0.0177304646668499
668.25	2579.08687180031	160.17255326579	13.2446434432742	0.000028635285809139	0.161557883812736	0.017467321020323
668.5	2582.37787012159	159.479735120263	13.0841891380893	0.0000286119354358503	0.160554396950448	0.0172127079078632
668.75	2585.62937899019	158.799859254107	12.9286868375589	0.0000285894045975897	0.159576476608849	0.0169662025596214
669	2588.84260634501	158.132472877026	12.777898702415	0.0000285676616766797	0.158623109499039	0.0167274100952225
669.25	2592.01870260482	157.477146405984	12.63160219724	0.0000285466767747257	0.15769333761371	0.0164959612484341
669.5	2595.15876433908	156.833471909129	12.4895888696447	0.0000285264218637488	0.156786254145159	0.0162715103113669
669.75	2598.2638376483	156.201061677683	12.3516632447583	0.0000285068697520888	0.155901000821138	0.0160537332738929
670	2601.33492128098	155.579546913422	12.2176418225167	0.0000284879949937383	0.155036763741249	0.0158423261369904
670.25	2604.37296951169	154.968576520705	12.0873521667638	0.000028469773431568	0.154192770759232	0.0156370033813375
670.5	2607.37889480184	154.367815993268	11.9606320765075	0.0000284521821133203	0.153368288757737	0.015437496574744
670.75	2610.35357026259	153.776946386997	11.8373288307985	0.0000284351992142641	0.152562621138299	0.0152435531039316
671	2613.29783193747	153.195663370863	11.7172984997199	0.000028418803965895	0.151775105506695	0.0150549350179179
671.25	2616.21248092024	152.623676349012	11.6004053148185	0.0000284029765901248	0.151005111535898	0.0148714179716876
671.5	2619.09828532222	152.06070764769	11.4865210930742	0.0000283876982384654	0.150252038990673	0.0146927902601502
671.75	2621.95598210169	151.506491761388	11.3755247091716	0.0000283729509357633	0.149515315899574	0.014518851933508
672	2624.78627876697	150.96077465308	11.2673016113999	0.0000283587175280838	0.148794396861412	0.0143494139861248
672.25	2627.58985496346	150.423313104004	11.1617433770299	0.0000283449816343864	0.148088761474679	0.0141842976118677
672.5	2630.36736395405	149.89387410881	11.0587473034544	0.0000283317276016681	0.147397912879436	0.0140233335196418
672.75	2633.11943400147	149.372234312363	10.9582160317778	0.0000283189404632811	0.146721376402277	0.0138663613035148
673	2635.84666966027	148.858179484793	10.8600571998815	0.0000283066059001616	0.146058698295804	0.0137132288624063
673.25	2638.54965298544	148.351504031732	10.7641831223056	0.0000282947102047314	0.145409444564923	0.0135637918648512
673.5	2641.22894466417	147.852010536938	10.6705104945509	0.000028283240247254	0.144773199872934	0.0134179132547913
673.75	2643.88508507643	147.359509334788	10.5789601196548	0.0000282721834444511	0.144149566521081	0.013275462794775
674	2646.51859528981	146.873818110316	10.4894566551001	0.0000282615277301993	0.143538163495763	0.0131363166432892
674.25	2649.12997799351	146.394761524709	10.4019283783119	0.0000282512615281448	0.142938625578153	0.0130003569632835
674.5	2651.71971837572	145.922170864334	10.3163069691667	0.0000282413737260902	0.142350602511452	0.0128674715592306
674.75	2654.28828494873	145.455883711556	10.2325273080846	0.0000282318536520158	0.141773758221377	0.0127375535403151
675	2656.83613032533	144.995743635726	10.1505272884169	0.0000282226910516151	0.14120777008591	0.0126105010075831
675.25	2659.36369194995	144.541599902907	10.0702476419559	0.0000282138760672301	0.140652328250653	0.0124862167630791
675.5	2661.87139278772	144.093307202949	9.99163177650912	0.0000282053992180845	0.14010713498645	0.0123646080391867
675.75	2664.35964197437	143.65072539273	9.91462562456912	0.0000281972513817208	0.139571904086211	0.0122455862465486
676	2666.82883542955	143.213719254394	9.83917750220528	0.0000281894237765546	0.13904636029814	0.0121290667390946
676.25	2669.27935643603	142.782158267561	9.76523797737633	0.0000281819079454667	0.138530238792776	0.0120149685948303
676.5	2671.71157618718	142.355916394557	9.69275974693641	0.0000281746957403608	0.138023284661489	0.0119032144111675
676.75	2674.12585430463	141.934871877767	9.62169752167035	0.0000281677793076193	0.137525252444261	0.011793730113678
677	2676.52253932819	141.518907048318	9.55200791875076	0.0000281611510743959	0.137035905684716	0.011686444777253
677.25	2678.90196917969	141.107908145318	9.4836493610619	0.0000281548037356886	0.13655501651059	0.0115812904587362
677.5	2681.26447160251	140.701765144987	9.41658198288342	0.0000281487302421398	0.136082365237905	0.0114782020401794
677.75	2683.61036457825	140.300371599009	9.35076754146593	0.0000281429237885162	0.135617739997286	0.0113771170819363
678	2685.93995672202	139.90362448154	9.28616933407511	0.0000281373778028233	0.135160936380968	0.011277975684886
678.25	2688.25354765755	139.511424044305	9.2227521201101	0.0000281320859360133	0.134711757109148	0.0111807203611226
678.5	2690.55142837356	139.123673679283	9.16048204793671	0.0000281270420522491	0.134270011714429	0.011085295912512
678.75	2692.83388156223	138.740279788506	9.09932658610383	0.000028122240219687	0.133835516243211	0.0109916493165575
679	2695.10118194116	138.361151660542	9.03925445864143	0.0000281176747017477	0.133408092972964	0.0108997296190715
679.25	2697.35359655948	137.986201353235	8.98023558415423	0.000028113339948844	0.132987570144378	0.0108094878331734
679.5	2699.59138508929	137.615343582355	8.92224101845774	0.0000281092305905369	0.132573781707483	0.0107208768441897
679.75	2701.81480010315	137.248495615773	8.8652429005134	0.000028105341428094	0.132166567080876	0.0106338513200508
680	2704.02408733839	136.885577172861	8.80921440144597	0.0000281016674274263	0.131765770923265	0.01054836762682
680.25	2706.21948594911	136.526510328794	8.75412967643628	0.0000280982037123803	0.131371242916582	0.0104643837490101
680.5	2708.40122874644	136.171219423476	8.69996381930351	0.0000280949455583646	0.130982837559989	0.0103818592143762
680.75	2710.56954242783	135.819630974824	8.64669281960033	0.0000280918883862904	0.130600413974121	0.0103007550228903
681	2712.72464779582	135.47167359617	8.59429352206101	0.0000280890277568092	0.130223835714976	0.0102210335796298
681.25	2714.86675996701	135.127277917528	8.54274358825171	0.000028086359364829	0.129852970596898	0.0101426586313281
681.5	2716.9960885717	134.786376510531	8.49202146028388	0.0000280838790342943	0.129487690524114	0.0100655952063564
681.75	2719.11283794468	134.448903816832	8.44210632646276	0.0000280815827132139	0.129127871330361	0.00998980955792093
682	2721.21720730771	134.114796079765	8.39297808874983	0.0000280794664689231	0.128773392626127	0.00991526911027522
682.25	2723.30939094398	133.783991279104	8.34461733192889	0.0000280775264835677	0.128424137653102	0.00984194240776242
682.5	2725.3895783652	133.45642906875	8.29700529437134	0.0000280757590497968	0.128079993145412	0.00976979906651385
682.75	2727.45795447146	133.132050717182	8.25012384030452	0.0000280741605666525	0.127740849197292	0.0096988097286433
683	2729.51469970437	132.810799050536	8.20395543349371	0.0000280727275356485	0.127406599136833	0.00962894601878823
683.25	2731.55999019381	132.492618398169	8.15848311225241	0.0000280714565570232	0.127077139405471	0.00956018050285538
683.5	2733.59399789858	132.177454540578	8.11369046570524	0.0000280703443261623	0.126752369442926	0.00949248664884474
683.75	2735.61689074126	131.865254659556	8.0695616112285	0.0000280693876301789	0.126432191577286	0.00942583878962732
684	2737.62883273753	131.555967290473	8.02608117300127	0.0000280685833446444	0.126116510919981	0.00936021208756434
684.25	2739.62998412036	131.249542276558	7.98323426160276	0.0000280679284304616	0.125805235265369	0.00929558250086146
684.5	2741.62050145912	130.94593072511	7.941006454598	0.0000280674199308733	0.125498274994728	0.00923192675156117
684.75	2743.60053777401	130.645084965519	7.89938377805448	0.0000280670549685992	0.125195542984397	0.00916922229507796
685	2745.57024264595	130.346958509006	7.85835268893775	0.0000280668307430941	0.124896954517866	0.00910744729118992
685.25	2747.52976232225	130.051506010025	7.81790005833995	0.0000280667445279225	0.12460242720163	0.00904658057641001
685.5	2749.47923981804	129.75868322921	7.77801315549129	0.0000280667936682422	0.12431188088459	0.00898660163765386
685.75	2751.41881501396	129.468446997818	7.7386796325153	0.0000280669755783934	0.124025237580845	0.00892749058713924
686	2753.34862475001	129.180755183596	7.69988750988631	0.0000280672877395862	0.123742421395711	0.00886922813844769
686.25	2755.26880291589	128.895566657977	7.66162516255067	0.0000280677276976834	0.123463358454787	0.00881179558368478
686.5	2757.17948053799	128.612841264584	7.6238813066779	0.0000280682930610722	0.123187976835938	0.00875517477168255
686.75	2759.08078586304	128.332539788945	7.58664498700767	0.0000280689814986229	0.122916206504054	0.00869934808718749
687	2760.97284443877	128.054623929387	7.54990556476135	0.000028069790737728	0.122647979248445	0.00864429843098239
687.25	2762.85577919157	127.779056269037	7.51365270608913	0.0000280707185624196	0.122383228622746	0.00859000920089353
687.5	2764.72971050132	127.505800248891	7.47787637102432	0.0000280717628115604	0.122121889887223	0.00853646427363632
687.75	2766.59475627357	127.234820141901	7.4425668029203	0.0000280729213771062	0.121863899953357	0.00848364798745869
688	2768.45103200901	126.966081028033	7.40771451834368	0.0000280741922024346	0.121609197330608	0.0084315451255382
688.25	2770.29865087067	126.699548770245	7.37331029740252	0.0000280755732807391	0.121357722075256	0.0083801409000979
688.5	2772.13772374854	126.435189991359	7.33934517448599	0.0000280770626534836	0.121109415741219	0.0083294209372016
688.75	2773.96835932207	126.172972051779	7.30581042939705	0.0000280786584089162	0.120864221332767	0.0082793712621984
689	2775.79066412048	125.912863028016	7.27269757885653	0.0000280803586806386	0.120622083259039	0.00822997828577997
689.25	2777.60474258089	125.654831691991	7.23999836836251	0.0000280821616462289	0.120382947290287	0.00818122879062453
689.5	2779.41069710461	125.398847491075	7.20770476438603	0.000028084065525916	0.120146760515764	0.00813310991859572
689.75	2781.20862811138	125.144880528851	7.17580894688812	0.0000280860685813023	0.119913471303193	0.00808560915847169
690	2782.9986340919	124.89290154654	7.14430330214183	0.0000280881691141335	0.119683029259739	0.00803871433417708
690.25	2784.78081165846	124.642881905089	7.11318041584542	0.0000280903654651129	0.119455385194419	0.00799241359349532
690.5	2786.55525559405	124.394793567883	7.0824330665123	0.0000280926560127587	0.119230491081896	0.0079466953972371
690.75	2788.32205889971	124.148609084049	7.05205421912568	0.0000280950391723019	0.119008300027584	0.00790154850884535
691	2790.0813128404	123.904301572338	7.02203701904411	0.0000280975133946242	0.118788766234021	0.00785696198441345
691.25	2791.83310698936	123.66184470556	6.99237478614817	0.0000281000771652325	0.118571844968453	0.00781292516310101
691.5	2793.57752927102	123.421212695538	6.96306100921548	0.0000281027290032704	0.118357492531566	0.00776942765792568
691.75	2795.31466600255	123.182380278575	6.93408934051421	0.000028105467460563	0.118145666227334	0.00772645934691476
692	2797.04460193408	122.945322701409	6.90545359060634	0.0000281082911206964	0.117936324333932	0.00768401036460233
692.25	2798.76742028766	122.710015707626	6.87714772334897	0.0000281111985981272	0.117729426075664	0.00764207109385232
692.5	2800.48320279494	122.476435524529	6.8491658510867	0.0000281141885373241	0.117524931595867	0.00760063215799611
692.75	2802.19202973375	122.244558850436	6.82150223002571	0.0000281172596119372	0.117322801930758	0.00755968441326921
693	2803.89397996348	122.014362842387	6.79415125578169	0.0000281204105239965	0.117122998984173	0.00751921894153379
693.25	2805.58913095941	121.785825104257	6.76710745909398	0.0000281236400031368	0.116925485503176	0.00747922704327485
693.5	2807.27755884595	121.558923675244	6.74036550169917	0.0000281269468058486	0.116730225054493	0.00743970023085841
693.75	2808.95933842892	121.333637018726	6.71392017235556	0.0000281303297147535	0.116537182001736	0.00740063022203795
694	2810.63454322679	121.109944011476	6.68776638301468	0.0000281337875379038	0.116346321483403	0.00736200893370241
694.25	2812.30324550106	120.887823933214	6.66189916513114	0.0000281373191081054	0.116157609391604	0.00732382847585175
694.5	2813.96551628562	120.667256456485	6.63631366610608	0.0000281409232822616	0.115971012351488	0.00728608114579184
694.75	2815.62142541537	120.448221636855	6.61100514585859	0.0000281445989407393	0.11578649770136	0.00724875942253977
695	2817.27104155391	120.230699903411	6.58596897351939	0.000028148344986755	0.11560403347344	0.00721185596142988
695.25	2818.91443222043	120.014672049548	6.56120062424165	0.0000281521603457805	0.115423588375246	0.00717536358891217
695.5	2820.55166381585	119.800119224047	6.53669567612457	0.0000281560439649674	0.115245131771593	0.00713927529753585
695.75	2822.18280164816	119.587022922415	6.51244980724441	0.0000281599948125897	0.11506863366716	0.00710358424110932
696	2823.80790995708	119.37536497849	6.48845879278924	0.0000281640118775045	0.114894064689614	0.00706828373003036
696.25	2825.42705193797	119.165127556303	6.46471850229247	0.0000281680941686286	0.114721396073282	0.00703336722677833
696.5	2827.04028976508	118.956293142173	6.44122489696204	0.0000281722407144319	0.114550599643328	0.00699882834156337
696.75	2828.64768461416	118.748844537046	6.41797402710039	0.0000281764505624466	0.114381647800436	0.00696466082812458
697	2830.24929668442	118.542764849052	6.39496202961257	0.0000281807227787908	0.114214513505966	0.00693085857967256
697.25	2831.84518521986	118.338037486292	6.37218512559842	0.000028185056447707	0.114049170267577	0.00689741562496992
697.5	2833.43540853004	118.134646149816	6.34963961802528	0.000028189450671115	0.113885592125294	0.00686432612454378
697.75	2835.02002401025	117.932574826826	6.32732188947887	0.000028193904568177	0.113723753637996	0.00683158436702631
698	2836.59908816116	117.731807784062	6.30522839998887	0.0000281984172748776	0.113563629870333	0.00679918476561774
698.25	2838.17265660791	117.532329561377	6.2833556849256	0.0000282029879436143	0.113405196380026	0.00676712185466586
698.5	2839.74078411868	117.334124965504	6.26170035296643	0.000028207615742802	0.11324842920556	0.00673539028635964
698.75	2841.30352462279	117.137179063992	6.24025908412822	0.0000282122998564874	0.113093304854245	0.00670398482753111
699	2842.86093122827	116.941477179312	6.21902862786346	0.0000282170394839762	0.112939800290636	0.00667290035656135
699.25	2844.41305623901	116.747004883137	6.19800580121804	0.0000282218338394704	0.112787892925294	0.0066421318603876
699.5	2845.95995117141	116.55374799077	6.17718748704809	0.000028226682151716	0.112637560603886	0.00661167443160685
699.75	2847.50166677064	116.361692555735	6.15657063229337	0.0000282315836636613	0.112488781596604	0.00658152326567197
700	2849.03825302645	116.170824864512	6.13615224630572	0.0000282365376321248	0.11234153458789	0.00655167365817808
700.25	2850.56975918854	115.981131431421	6.11592939923025	0.0000282415433274724	0.112195798666468	0.006522121002235
700.5	2852.0962337816	115.792598993639	6.09589922043703	0.0000282466000333043	0.11205155331566	0.00649286078592234
700.75	2853.61772461988	115.605214506359	6.07605889700185	0.0000282517070461498	0.111908778403985	0.00646388858982486
701	2855.1342788215	115.418965138071	6.05640567223388	0.0000282568636751716	0.111767454176024	0.00643520008464443
701.25	2856.64594282225	115.233838265983	6.0369368442494	0.000028262069241878	0.111627561243552	0.00640679102888737
701.5	2858.15276238917	115.049821471545	6.01764976458826	0.0000282673230798428	0.111489080576918	0.00637865726662143
701.75	2859.65478263373	114.866902536114	5.9985418368735	0.0000282726245344334	0.111351993496666	0.00635079472530351
702	2861.15204802467	114.685069436713	5.97961051551112	0.0000282779729625464	0.111216281665404	0.00632319941367281
702.25	2862.64460240054	114.504310341916	5.96085330442917	0.0000282833677323496	0.111081927079884	0.00629586741970817
702.5	2864.13248898196	114.324613607829	5.94226775585481	0.0000282888082230321	0.110948912063316	0.00626879490864752
702.75	2865.6157503835	114.145967774188	5.92385146912795	0.0000282942938245609	0.110817219257892	0.00624197812106692
703	2867.09442862533	113.968361560549	5.90560208954998	0.0000282998239374434	0.11068683161751	0.00621541337101698
703.25	2868.56856514459	113.791783862572	5.88751730726635	0.0000283053979724966	0.110557732400709	0.00618909704421436
703.5	2870.03820080644	113.616223748415	5.86959485618269	0.0000283110153506232	0.110429905163787	0.00616302559628813
703.75	2871.50337591489	113.441670455206	5.85183251291177	0.0000283166755025927	0.110303333754112	0.00613719555107642
704	2872.9641302233	113.268113385609	5.83422809575172	0.0000283223778688284	0.110178002303612	0.0061116034989739
704.25	2874.42050294474	113.095542104482	5.81677946369361	0.0000283281218992003	0.110053895222442	0.00608624609532732
704.5	2875.87253276202	112.923946335604	5.79948451545757	0.0000283339070528238	0.109930997192822	0.0060611200588774
704.75	2877.32025783748	112.753315958504	5.78234118855653	0.0000283397327978622	0.109809293163031	0.00603622217024583
705	2878.76371582259	112.58364100535	5.76534745838695	0.0000283455986113361	0.109688768341574	0.0060115492704663
705.25	2880.20294386733	112.414911657928	5.74850133734481	0.0000283515039789365	0.109569408191494	0.00598709825955653
705.5	2881.6379786293	112.247118244686	5.73180087396699	0.0000283574483948431	0.109451198424833	0.00596286609513178
705.75	2883.06885628268	112.080251237858	5.71524415209678	0.0000283634313615472	0.10933412499725	0.00593884979105752
706	2884.49561252691	111.914301250652	5.69882929007213	0.0000283694523896792	0.109218174102759	0.0059150464161393
706.25	2885.91828259528	111.749259034511	5.68255443993741	0.0000283755109978401	0.109103332168626	0.00589145309285079
706.5	2887.3369012632	111.585115476434	5.66641778667605	0.000028381606712438	0.108989585850381	0.00586806699609576
706.75	2888.75150285637	111.42186159637	5.65041754746504	0.0000283877390675276	0.108876922026968	0.00584488535200565
707	2890.16212125874	111.259488544663	5.63455197094933	0.0000283939076046546	0.108765327796015	0.00582190543676965
707.25	2891.56878992027	111.09798759957	5.61881933653642	0.0000284001118727037	0.108654790469223	0.00579912457549744
707.5	2892.97154186456	110.937350164827	5.60321795370974	0.0000284063514277505	0.10854529756788	0.00577654014111246
707.75	2894.37040969625	110.777567767282	5.58774616136099	0.0000284126258329161	0.10843683681848	0.0057541495532763
708	2895.76542560833	110.618632054571	5.57240232713994	0.000028418934658227	0.108329396148455	0.00573195027734107
708.25	2897.15662138923	110.460534792861	5.55718484682202	0.0000284252774804766	0.108222963682015	0.00570993982333099
708.5	2898.54402842977	110.303267864642	5.54209214369264	0.0000284316538830914	0.108117527736093	0.00568811574495102
708.75	2899.92767772996	110.146823266562	5.52712266794769	0.0000284380634559999	0.108013076816385	0.00566647563862183
709	2901.30759990566	109.991193107321	5.51227489611006	0.0000284445057955042	0.107909599613495	0.00564501714254071
709.25	2902.68382519512	109.836369605612	5.49754733046137	0.0000284509805041558	0.107807084999173	0.00562373793576728
709.5	2904.0563834653	109.682345088103	5.48293849848839	0.0000284574871906332	0.107705522022639	0.00560263573733301
709.75	2905.42530421812	109.529111987473	5.46844695234437	0.000028464025469623	0.107604899907005	0.00558170830537492
710	2906.79061659658	109.376662840485	5.45407126832369	0.0000284705949617041	0.107505208045782	0.00556095343629088
710.25	2908.15234939072	109.224990286108	5.43981004635049	0.0000284771952932336	0.107406435999468	0.00554036896391773
710.5	2909.51053104345	109.074087063678	5.42566190948018	0.0000284838260962366	0.107308573492222	0.00551995275873004
710.75	2910.8651896563	108.923946011097	5.41162550341388	0.0000284904870082975	0.107211610408614	0.00549970272706011
711	2912.21635299499	108.774560063085	5.39769949602512	0.0000284971776724547	0.10711553679046	0.0054796168103377
711.25	2913.56404849494	108.625922249451	5.3838825768984	0.0000285038977370972	0.107020342833723	0.00545969298434906
711.5	2914.90830326664	108.478025693418	5.37017345687952	0.0000285106468558635	0.106926018885493	0.00543992925851485
711.75	2916.24914410089	108.330863609977	5.35657086763722	0.0000285174246875432	0.10683255544104	0.00542032367518676
712	2917.58659747397	108.184429304281	5.34307356123564	0.000028524230895981	0.106739943140931	0.00540087430896127
712.25	2918.92068955269	108.03871617007	5.32968030971755	0.0000285310651499819	0.106648172768216	0.00538157926601109
712.5	2920.25144619932	107.893717688133	5.31638990469775	0.0000285379271232196	0.106557235245685	0.00536243668343302
712.75	2921.57889297643	107.749427424801	5.30320115696656	0.0000285448164941467	0.10646712163318	0.00534344472861211
713	2922.90305515166	107.605839030474	5.29011289610319	0.0000285517329459065	0.106377823124978	0.00532460159860186
713.25	2924.22395770234	107.462946238179	5.27712397009824	0.0000285586761662471	0.106289331047227	0.00530590551951921
713.5	2925.54162532007	107.320742862157	5.26423324498566	0.0000285656458474375	0.106201636855445	0.00528735474595474
713.75	2926.85608241517	107.179222796484	5.25143960448347	0.0000285726416861853	0.106114732132073	0.0052689475603972
714	2928.16735312107	107.038380013717	5.23874194964333	0.0000285796633835565	0.106028608584091	0.00525068227267216
714.25	2929.47546129858	106.898208563567	5.22613919850822	0.0000285867106448967	0.105943258040677	0.00523255721939407
714.5	2930.78043054014	106.75870257161	5.21363028577863	0.0000285937831797543	0.105858672450929	0.00521457076343171
714.75	2932.08228417388	106.61985623801	5.20121416248647	0.0000286008807018055	0.105774843881632	0.00519672129338644
715	2933.38104526771	106.481663836278	5.18888979567686	0.0000286080029287805	0.105691764515075	0.00517900722308299
715.25	2934.67673663328	106.344119712059	5.17665616809732	0.0000286151495823915	0.105609426646926	0.00516142699107231
715.5	2935.96938082984	106.207218281932	5.16451227789437	0.0000286223203882626	0.105527822684138	0.00514397906014637
715.75	2937.25900016807	106.07095403225	5.15245713831719	0.0000286295150758605	0.105446945142918	0.00512666191686434
716	2938.54561671385	105.935321517988	5.14048977742813	0.0000286367333784274	0.10536678664673	0.00510947407108985
716.25	2939.82925229185	105.80031536163	5.12860923782006	0.0000286439750329149	0.105287339924343	0.00509241405553928
716.5	2941.10992848923	105.665930252063	5.11681457634022	0.0000286512397799192	0.10520859780793	0.00507548042534062
716.75	2942.38766236976	105.532160943509	5.1051048526009	0.000028658527363618	0.105130553199224	0.0050586717243922
717	2943.6624837143	105.399002254462	5.09347917395729	0.000028665837531709	0.105053199196528	0.00504198661864396
717.25	2944.9344090474	105.266449066663	5.08193662683005	0.0000286731700353486	0.104976528898241	0.005025423693815
717.5	2946.20345904062	105.13449632408	5.07047632244712	0.0000286805246290929	0.104900535531886	0.00500898159046894
717.75	2947.46965414494	105.003139031921	5.05909738500206	0.0000286879010708397	0.104825212419452	0.00499265896952351
718	2948.73301459401	104.872372255657	5.04779895141346	0.0000286952991217716	0.104750552975729	0.00497645451186657
718.25	2949.99356040723	104.74219112007	5.03658017108989	0.0000287027185462999	0.104676550706661	0.00496036691798136
718.5	2951.25131139294	104.612590808317	5.02544020570017	0.0000287101591120105	0.104603199207754	0.00494439490758004
718.75	2952.50628715137	104.483566561016	5.0143782289486	0.0000287176205896103	0.104530492162502	0.00492853721924546
719	2953.75850707766	104.35511367534	5.00339342635535	0.0000287251027528745	0.104458423340852	0.00491279261008108
719.25	2955.00799036481	104.227227504142	4.99248499504153	0.0000287326053785959	0.104386986597703	0.00489715985536855
719.5	2956.25475600648	104.09990345509	4.98165214351929	0.0000287401282465341	0.104316175871435	0.00488163774823328
719.75	2957.4988227999	103.973136989815	4.97089409148609	0.0000287476711393666	0.104245985182467	0.00486622509931686
720	2958.74020934859	103.846923623081	4.96021006962397	0.0000287552338426402	0.104176408631847	0.00485092073645737
720.25	2959.97893406509	103.72125892197	4.94959931940275	0.0000287628161447243	0.10410744039987	0.00483572350437613
720.5	2961.21501517363	103.596138505082	4.9390610928878	0.0000287704178367637	0.104039074744726	0.00482063226437178
720.75	2962.44847071276	103.471558041749	4.92859465255183	0.0000287780387126342	0.103971306001176	0.0048056458940208
721	2963.67931853793	103.347513251263	4.91819927109075	0.0000287856785688971	0.103904128579251	0.00479076328688465
721.25	2964.90757632404	103.223999902125	4.90787423124354	0.0000287933372047563	0.103837536962985	0.00477598335222322
721.5	2966.13326156789	103.101013811297	4.89761882561584	0.0000288010144220149	0.103771525709165	0.00476130501471443
721.75	2967.35639159065	102.978550843478	4.88743235650745	0.0000288087100250339	0.103706089446114	0.00474672721417997
722	2968.57698354026	102.856606910391	4.87731413574342	0.0000288164238206906	0.103641222872495	0.00473224890531691
722.25	2969.79505439378	102.735177970078	4.86726348450864	0.0000288241556183385	0.103576920756139	0.00471786905743494
722.5	2971.01062095975	102.614260026214	4.85727973318603	0.0000288319052297675	0.103513177932899	0.00470358665419923
722.75	2972.22369988039	102.493849127433	4.84736222119808	0.0000288396724691655	0.103449989305521	0.00468940069337895
723	2973.43430763394	102.373941366661	4.83751029685164	0.0000288474571530802	0.103387349842546	0.00467531018660073
723.25	2974.64246053677	102.254532880469	4.82772331718605	0.0000288552591003817	0.103325254577227	0.0046613141591077
723.5	2975.8481747456	102.135619848431	4.81800064782433	0.000028863078132226	0.103263698606472	0.00464741164952328
723.75	2977.05146625962	102.017198492499	4.80834166282751	0.0000288709140720192	0.103202677089801	0.00463360170962012
724	2978.25235092256	101.899265076387	4.79874574455189	0.000028878766745382	0.103142185248336	0.00461988340409371
724.25	2979.45084442478	101.781815904959	4.78921228350922	0.0000288866359801157	0.103082218363795	0.00460625581034065
724.5	2980.64696230524	101.664847323647	4.77974067822997	0.0000288945216061677	0.10302277177752	0.0045927180182419
724.75	2981.84071995357	101.548355717856	4.77033033512896	0.0000289024234555988	0.102963840889513	0.00457926912994982
725	2983.03213261192	101.432337512397	4.76098066837414	0.00002891034136255	0.1029054211575	0.00456590825968021
725.25	2984.22121537698	101.316789170924	4.75169109975771	0.000028918275163211	0.102847508096004	0.00455263453350826
725.5	2985.4079832018	101.201707195376	4.74246105857002	0.0000289262246957886	0.102790097275443	0.00453944708916868
725.75	2986.5924508977	101.087088125441	4.73328998147596	0.0000289341898004756	0.102733184321242	0.00452634507586011
726	2987.77463313605	100.972928538015	4.72417731239378	0.0000289421703194211	0.102676764912964	0.00451332765405321
726.25	2988.95454445011	100.859225046682	4.71512250237634	0.0000289501660967002	0.102620834783453	0.00450039399530276
726.5	2990.13219923678	100.745974301199	4.70612500949477	0.0000289581769782852	0.102565389718	0.00448754328206361
726.75	2991.30761175834	100.633172986988	4.69718429872432	0.0000289662028120169	0.102510425553519	0.00447477470751009
727	2992.48079614417	100.520817824636	4.68829984183263	0.0000289742434475764	0.102455938177745	0.0044620874753593
727.25	2993.65176639241	100.408905569413	4.67947111727	0.0000289822987364574	0.102401923528435	0.00444948079969764
727.5	2994.82053637166	100.297433010786	4.67069761006206	0.0000289903685319396	0.102348377592604	0.00443695390481113
727.75	2995.98711982257	100.186396971946	4.6619788117041	0.0000289984526890616	0.102295296405751	0.0044245060250185
728	2997.15153035948	100.075794309349	4.65331422005808	0.0000290065510645948	0.10224267605112	0.00441213640450837
728.25	2998.31378147197	99.9656219122554	4.64470333925103	0.0000290146635170181	0.102190512658964	0.00439984429717883
728.5	2999.47388652641	99.8558767022819	4.6361456795758	0.0000290227899064922	0.102138802405826	0.00438762896648073
728.75	3000.63185876753	99.7465556329624	4.62764075739357	0.0000290309300948354	0.102087541513832	0.00437548968526368
729	3001.78771131988	99.6376556893138	4.61918809503826	0.0000290390839454989	0.102036726249996	0.0043634257356253
729.25	3002.94145718934	99.5291738874086	4.61078722072271	0.0000290472513235429	0.101986352925543	0.00435143640876307
729.5	3004.09310926455	99.4211072739567	4.60243766844676	0.0000290554320956135	0.101936417895236	0.00433952100482935
729.75	3005.24268031839	99.3134529258941	4.59413897790702	0.0000290636261299193	0.101886917556726	0.0043276788327891
730	3006.39018300934	99.2062079499768	4.5858906944083	0.0000290718332962089	0.101837848349903	0.00431590921028018
730.25	3007.53562988293	99.0993694823815	4.57769236877673	0.0000290800534657485	0.101789206756263	0.00430421146347639
730.5	3008.67903337305	98.992934688316	4.56954355727465	0.0000290882865113006	0.101740989298293	0.00429258492695336
730.75	3009.82040580333	98.886900761631	4.56144382151681	0.0000290965323071016	0.101693192538853	0.00428102894355648
731	3010.95975938848	98.781264924444	4.55339272838849	0.0000291047907288415	0.101645813080586	0.00426954286427193
731.25	3012.09710623556	98.6760244267632	4.54538984996477	0.000029113061653643	0.101598847565321	0.00425812604809954
731.5	3013.23245834531	98.5711765461236	4.53743476343164	0.0000291213449600406	0.101552292673503	0.00424677786192855
731.75	3014.36582761337	98.4667185872245	4.52952705100831	0.0000291296405279612	0.101506145123621	0.00423549768041538
732	3015.49722583158	98.3626478815748	4.52166629987112	0.0000291379482387041	0.101460401671652	0.0042242848858638
732.25	3016.62666468919	98.2589617871442	4.51385210207874	0.0000291462679749218	0.101415059110513	0.00421313886810727
732.5	3017.75415577404	98.155657688019	4.50608405449877	0.0000291545996206008	0.101370114269526	0.00420205902439351
732.75	3018.8797105738	98.0527329940648	4.49836175873577	0.0000291629430610429	0.101325564013887	0.00419104475927132
733	3020.00334047712	97.9501851405931	4.4906848210604	0.0000291712981828471	0.101281405244146	0.00418009548447913
733.25	3021.1250567748	97.8480115880341	4.48305285234003	0.0000291796648738911	0.1012376348957	0.00416921061883597
733.5	3022.24487066091	97.746209821615	4.47546546797056	0.000029188043023314	0.101194249938291	0.00415838958813427
733.75	3023.36279323394	97.6447773510425	4.46792228780938	0.0000291964325214983	0.101151247375513	0.00414763182503461
734	3024.47883549789	97.543711710191	4.46042293610965	0.0000292048332600532	0.101108624244326	0.00413693676896246
734.25	3025.59300836336	97.4430104567958	4.45296704145568	0.0000292132451317974	0.101066377614588	0.0041263038660067
734.5	3026.70532264865	97.3426711721501	4.44555423669946	0.0000292216680307427	0.101024504588578	0.00411573256882001
734.75	3027.81578908079	97.2426914608081	4.43818415889841	0.0000292301018520773	0.100983002300542	0.00410522233652107
735	3028.92441829658	97.143068950292	4.43085644925411	0.0000292385464921503	0.100941867916244	0.00409477263459854
735.25	3030.03122084364	97.0438012908034	4.42357075305219	0.0000292470018484554	0.100901098632516	0.0040843829348167
735.5	3031.13620718143	96.9448861549404	4.41632671960328	0.0000292554678196153	0.100860691676827	0.00407405271512285
735.75	3032.23938768221	96.8463212374165	4.40912400218493	0.0000292639443053671	0.100820644306852	0.00406378145955619
736	3033.34077263208	96.7481042547872	4.40196225798462	0.0000292724312065464	0.100780953810049	0.00405356865815858
736.25	3034.44037223189	96.6502329451782	4.39484114804375	0.0000292809284250731	0.100741617503248	0.00404341380688666
736.5	3035.53819659823	96.5527050680188	4.38776033720257	0.0000292894358639364	0.100702632732244	0.00403331640752564
736.75	3036.63425576439	96.4555184037795	4.38071949404611	0.000029297953427181	0.100663996871391	0.00402327596760451
737	3037.72855968126	96.3586707537129	4.37371829085096	0.0000293064810198925	0.100625707323213	0.00401329200031279
737.25	3038.82111821823	96.2621599395994	4.36675640353311	0.0000293150185481839	0.100587761518016	0.0040033640244188
737.5	3039.91194116416	96.1659838034963	4.35983351159654	0.0000293235659191816	0.100550156913505	0.00399349156418921
737.75	3041.00103822819	96.0701402074905	4.35294929808279	0.0000293321230410125	0.100512890994412	0.00398367414931009
738	3042.0884190407	95.9746270334555	4.34610344952133	0.0000293406898227901	0.100475961272126	0.00397391131480932
738.25	3043.17409315408	95.8794421828118	4.33929565588086	0.0000293492661746021	0.100439365284331	0.00396420260098031
738.5	3044.25807004368	95.7845835762897	4.33252561052124	0.0000293578520074973	0.10040310059465	0.00395454755330698
738.75	3045.3403591086	95.6900491536994	4.32579301014659	0.0000293664472334732	0.100367164792294	0.00394494572239028
739	3046.42096967251	95.5958368736982	4.31909755475872	0.0000293750517654634	0.100331555491718	0.00393539666387546
739.25	3047.49991098452	95.501944713568	4.31243894761175	0.0000293836655173255	0.100296270332282	0.00392589993838123
739.5	3048.57719221991	95.4083706689915	4.30581689516728	0.000029392288403829	0.100261306977915	0.00391645511142958
739.75	3049.65282248102	95.3151127538334	4.29923110705032	0.0000294009203406437	0.100226663116789	0.00390706175337707
740	3050.72681079796	95.2221689999241	4.29268129600603	0.0000294095612443278	0.100192336460997	0.00389771943934718
740.25	3051.79916612941	95.1295374568483	4.28616717785716	0.0000294182110323168	0.100158324746233	0.00388842774916395
740.5	3052.8698973634	95.0372161917342	4.27968847146209	0.0000294268696229117	0.10012462573148	0.00387918626728646
740.75	3053.93901331804	94.9452032890472	4.27324489867374	0.0000294355369352684	0.100091237198702	0.00386999458274465
741	3055.00652274227	94.8534968503874	4.26683618429899	0.0000294442128893865	0.100058156952544	0.00386085228907619
741.25	3056.07243431661	94.7620949942877	4.26046205605891	0.0000294528974060986	0.100025382820031	0.00385175898426421
741.5	3057.13675665387	94.6709958560173	4.25412224454952	0.0000294615904070597	0.0999929126502747	0.0038427142706763
741.75	3058.19949829984	94.5801975873861	4.24781648320323	0.0000294702918147366	0.0999607443141884	0.00383371775500438
742	3059.26066773404	94.4896983565531	4.24154450825099	0.0000294790015523982	0.0999288757041999	0.00382476904820557
742.25	3060.3202733704	94.3994963478376	4.23530605868492	0.0000294877195441044	0.0998973047339733	0.0038158677654442
742.5	3061.37832355792	94.3095897615319	4.22910087622166	0.0000294964457146972	0.0998660293381339	0.00380701352603445
742.75	3062.43482658138	94.2199768137179	4.22292870526618	0.0000295051799897901	0.0998350474719972	0.00379820595338423
743	3063.48979066198	94.1306557360856	4.21678929287634	0.0000295139222957587	0.0998043571113024	0.00378944467493985
743.25	3064.54322395802	94.0416247757552	4.21068238872792	0.0000295226725597314	0.0997739562519506	0.00378072932213164
743.5	3065.59513456555	93.9528821951	4.20460774508018	0.0000295314307095796	0.0997438429097462	0.00377205953032033
743.75	3066.64553051899	93.8644262715731	4.19856511674201	0.0000295401966739087	0.0997140151201419	0.00376343493874443
744	3067.69441979179	93.7762552975367	4.19255426103867	0.000029548970382049	0.0996844709379897	0.00375485519046847
744.25	3068.74181029704	93.6883675800925	4.18657493777898	0.0000295577517640467	0.0996552084372936	0.00374631993233194
744.5	3069.78770988807	93.6007614409158	4.18062690922303	0.0000295665407506551	0.099626225710967	0.00373782881489914
744.75	3070.83212635911	93.5134352160917	4.1747099400505	0.0000295753372733257	0.0995975208705943	0.00372938149240996
745	3071.87506744584	93.4263872559521	4.1688237973293	0.0000295841412641999	0.0995690920461945	0.00372097762273106
745.25	3072.916540826	93.3396159249172	4.16296825048488	0.0000295929526561004	0.0995409373859906	0.00371261686730826
745.5	3073.95655411998	93.2531196013381	4.15714307126994	0.0000296017713825231	0.0995130550561812	0.00370429889111951
745.75	3074.99511489141	93.1668966773409	4.15134803373461	0.0000296105973776283	0.0994854432407153	0.00369602336262852
746	3076.0322306477	93.0809455586746	4.1455829141971	0.0000296194305762335	0.0994581001410717	0.00368778995373922
746.25	3077.06790884062	92.995264664559	4.13984749121477	0.0000296282709138045	0.09943102397604	0.00367959833975092
746.5	3078.10215686687	92.9098524275367	4.13414154555575	0.0000296371183264485	0.0994042129815072	0.00367144819931417
746.75	3079.1349820686	92.8247072933263	4.12846486017091	0.0000296459727509054	0.0993776654102456	0.00366333921438738
747	3080.16639173398	92.7398277206769	4.12281722016627	0.0000296548341245411	0.0993513795317044	0.00365527107019395
747.25	3081.19639309772	92.6552121812258	4.11719841277587	0.0000296637023853392	0.0993253536318046	0.00364724345518023
747.5	3082.22499334159	92.5708591593572	4.11160822733499	0.0000296725774718941	0.0992995860127373	0.00363925606097406
747.75	3083.25219959497	92.4867671520633	4.10604645525389	0.0000296814593234035	0.0992740749927641	0.00363130858234396
748	3084.27801893535	92.4029346688072	4.10051288999179	0.0000296903478796613	0.0992488189060212	0.00362340071715896
748.25	3085.30245838881	92.3193602313878	4.09500732703146	0.0000296992430810504	0.0992238161023263	0.00361553216634908
748.5	3086.32552493059	92.2360423738055	4.08952956385391	0.0000297081448685358	0.0991990649469877	0.0036077026338663
748.75	3087.34722548552	92.1529796421316	4.0840793999138	0.0000297170531836578	0.0991745638206174	0.00359991182664632
749	3088.36756692854	92.0701705943772	4.07865663661488	0.0000297259679685248	0.0991503111189457	0.0035921594545707
749.25	3089.38655608521	91.9876138003663	4.07326107728608	0.000029734889165807	0.0991263052526393	0.00358444523042974
749.5	3090.40419973212	91.9053078416076	4.06789252715776	0.0000297438167187299	0.0991025446471219	0.0035767688698858
749.75	3091.42050459743	91.8232513111714	4.06255079333844	0.0000297527505710673	0.0990790277423972	0.00356913009143732
750	3092.43547736129	91.7414428135649	4.05723568479183	0.0000297616906671353	0.0990557529928747	0.00356152861638321
750.25	3093.44912465635	91.659880964612	4.05194701231417	0.0000297706369517858	0.0990327188671981	0.00355396416878793
750.5	3094.46145306816	91.578564391332	4.04668458851196	0.0000297795893704003	0.0990099238480756	0.003546436475447
750.75	3095.47246913564	91.4974917318221	4.04144822777998	0.0000297885478688836	0.0989873664321134	0.00353894526585306
751	3096.48217935156	91.4166616351403	4.03623774627969	0.0000297975123936582	0.0989650451296516	0.00353149027216248
751.25	3097.49059016293	91.33607276119	4.03105296191785	0.0000298064828916577	0.0989429584646012	0.00352407122916238
751.5	3098.49770797145	91.2557237806059	4.02589369432553	0.0000298154593103212	0.0989211049742852	0.00351668787423819
751.75	3099.50353913394	91.1756133746423	4.02075976483746	0.0000298244415975876	0.0988994832092809	0.00350933994734174
752	3100.50808996278	91.0957402350617	4.01565099647154	0.0000298334297018898	0.0988780917332643	0.00350202719095973
752.25	3101.5113667263	91.0161030640252	4.01056721390881	0.0000298424235721486	0.0988569291228579	0.00349474935008271
752.5	3102.51337564921	90.9367005739851	4.00550824347359	0.0000298514231577678	0.0988359939674788	0.00348750617217455
752.75	3103.514122913	90.8575314875776	4.00047391311398	0.0000298604284086285	0.0988152848691912	0.0034802974071423
753	3104.51361465635	90.7785945375178	3.99546405238261	0.0000298694392750831	0.0987948004425586	0.00347312280730653
753.25	3105.51185697553	90.6998884664954	3.99047849241767	0.0000298784557079508	0.0987745393144998	0.00346598212737209
753.5	3106.50885592479	90.6214120270725	3.98551706592421	0.0000298874776585118	0.0987545001241469	0.00345887512439926
753.75	3107.50461751675	90.5431639815822	3.98057960715574	0.000029896505078502	0.0987346815227036	0.00345180155777548
754	3108.49914772278	90.4651431020281	3.97566595189602	0.0000299055379201084	0.0987150821733076	0.00344476118918721
754.25	3109.4924524734	90.387348169986	3.97077593744118	0.0000299145761359633	0.0986957007508937	0.00343775378259248
754.5	3110.48453765861	90.3097779765063	3.9659094025821	0.0000299236196791401	0.0986765359420588	0.00343077910419364
754.75	3111.47540912833	90.2324313220173	3.96106618758694	0.0000299326685031475	0.0986575864449293	0.00342383692241066
755	3112.46507269271	90.1553070162307	3.95624613418404	0.0000299417225619253	0.0986388509690303	0.0034169270078546
755.25	3113.45353412251	90.0784038780474	3.951449085545	0.0000299507818098395	0.0986203282351556	0.00341004913330176
755.5	3114.44079914948	90.0017207354647	3.94667488626799	0.000029959846201677	0.0986020169752413	0.00340320307366789
755.75	3115.42687346667	89.9252564254845	3.94192338236131	0.0000299689156926418	0.0985839159322392	0.00339638860598297
756	3116.41176272882	89.8490097940236	3.93719442122717	0.0000299779902383496	0.0985660238599935	0.00338960550936629
756.25	3117.39547255271	89.7729796958238	3.93248785164575	0.0000299870697948237	0.0985483395231179	0.00338285356500187
756.5	3118.37800851745	89.6971649943637	3.9278035237594	0.0000299961543184903	0.0985308616968757	0.00337613255611424
756.75	3119.35937616489	89.6215645617718	3.92314128905708	0.0000300052437661742	0.0985135891670603	0.00336944226794457
757	3120.33958099988	89.5461772787405	3.91850100035909	0.0000300143380950943	0.0984965207298782	0.00336278248772715
757.25	3121.31862849068	89.4710020344407	3.91388251180189	0.0000300234372628593	0.0984796551918327	0.00335615300466612
757.5	3122.29652406922	89.3960377264385	3.90928567882325	0.0000300325412274636	0.0984629913696105	0.00334955360991265
757.75	3123.27327313147	89.3212832606115	3.90471035814749	0.0000300416499472828	0.0984465280899684	0.00334298409654232
758	3124.24888103772	89.2467375510676	3.90015640777106	0.0000300507633810697	0.0984302641896225	0.00333644425953297
758.25	3125.22335311293	89.1723995200639	3.89562368694814	0.0000300598814879503	0.0984141985151384	0.00332993389574263
758.5	3126.19669464703	89.0982680979263	3.8911120561766	0.0000300690042274197	0.0983983299228229	0.00332345280388795
758.75	3127.16891089522	89.0243422229711	3.88662137718406	0.0000300781315593378	0.0983826572786177	0.00331700078452291
759	3128.14000707828	88.9506208414271	3.88215151291419	0.0000300872634439259	0.0983671794579938	0.00331057764001771
759.25	3129.1099883829	88.8771029073577	3.87770232751312	0.0000300963998417623	0.0983518953458471	0.00330418317453804
759.5	3130.07885996193	88.8037873825857	3.87327368631614	0.0000301055407137788	0.0983368038363969	0.00329781719402463
759.75	3131.04662693472	88.7306732366176	3.86886545583448	0.0000301146860212569	0.098321903833084	0.00329147950617307
760	3132.01329438738	88.6577594465695	3.86447750374235	0.0000301238357258236	0.098307194248471	0.00328516992041391
760.25	3132.97886737309	88.5850449970931	3.86010969886406	0.0000301329897894483	0.0982926740041436	0.00327888824789297
760.5	3133.94335091237	88.512528880304	3.85576191116144	0.0000301421481744389	0.0982783420306139	0.00327263430145207
760.75	3134.90674999338	88.4402100957096	3.85143401172127	0.000030151310843438	0.0982641972672238	0.00326640789560984
761	3135.86906957219	88.3680876501376	3.84712587274304	0.0000301604777594197	0.0982502386620506	0.00326020884654287
761.25	3136.83031457305	88.2961605576677	3.84283736752677	0.0000301696488856859	0.0982364651718138	0.00325403697206727
761.5	3137.79048988869	88.2244278395605	3.83856837046098	0.0000301788241858627	0.0982228757617821	0.00324789209162012
761.75	3138.74960038055	88.1528885241902	3.83431875701092	0.0000301880036238973	0.0982094694056832	0.00324177402624154
762	3139.70765087908	88.0815416469771	3.83008840370684	0.0000301971871640543	0.0981962450856132	0.00323568259855676
762.25	3140.66464618399	88.0103862503202	3.82587718813248	0.0000302063747709126	0.0981832017919484	0.00322961763275854
762.5	3141.62059106453	87.9394213835318	3.82168498891372	0.0000302155664093621	0.0981703385232574	0.00322357895458981
762.75	3142.57549025972	87.8686461027719	3.81751168570733	0.0000302247620445999	0.0981576542862148	0.00321756639132649
763	3143.52934847862	87.798059470984	3.81335715918991	0.0000302339616421282	0.0981451480955159	0.00321157977176062
763.25	3144.4821704006	87.7276605578315	3.80922129104692	0.0000302431651677498	0.0981328189737924	0.00320561892618366
763.5	3145.43396067557	87.6574484396343	3.80510396396197	0.000030252372587566	0.0981206659515292	0.00319968368637
763.75	3146.38472392424	87.5874221993067	3.80100506160606	0.0000302615838679731	0.0981086880669823	0.00319377388556072
764	3147.33446473834	87.5175809262962	3.79692446862718	0.0000302707989756592	0.0980968843660979	0.00318788935844759
764.25	3148.2831876809	87.4479237165223	3.79286207063984	0.0000302800178776015	0.0980852539024321	0.00318202994115722
764.5	3149.23089728647	87.3784496723166	3.78881775421489	0.000030289240541063	0.0980737957370721	0.00317619547123541
764.75	3150.17759806137	87.3091579023637	3.7847914068694	0.0000302984669335898	0.0980625089385583	0.00317038578763185
765	3151.12329448389	87.2400475216414	3.78078291705663	0.0000303076970230081	0.0980513925828066	0.00316460073068474
765.25	3152.06799100459	87.1711176513639	3.77679217415625	0.0000303169307774212	0.0980404457530335	0.00315884014210597
765.5	3153.01169204645	87.1023674189234	3.77281906846453	0.0000303261681652068	0.0980296675396795	0.00315310386496612
765.75	3153.95440200516	87.0337959578341	3.76886349118484	0.0000303354091550144	0.0980190570403365	0.00314739174368001
766	3154.89612524932	86.9654024076754	3.76492533441808	0.000030344653715762	0.0980086133596734	0.00314170362399213
766.25	3155.83686612066	86.8971859140372	3.76100449115335	0.0000303539018166338	0.0979983356093643	0.00313603935296247
766.5	3156.77662893427	86.829145628464	3.75710085525871	0.0000303631534270774	0.0979882229080168	0.00313039877895242
766.75	3157.71541797882	86.7612807084018	3.75321432147206	0.0000303724085168008	0.0979782743811019	0.00312478175161093
767	3158.65323751676	86.6935903171438	3.74934478539211	0.0000303816670557703	0.0979684891608837	0.00311918812186074
767.25	3159.59009178458	86.6260736237774	3.74549214346952	0.0000303909290142076	0.0979588663863514	0.00311361774188494
767.5	3160.52598499294	86.558729803132	3.74165629299806	0.0000304001943625871	0.0979494052031504	0.0031080704651135
767.75	3161.46092132697	86.4915580357272	3.73783713210599	0.0000304094630716337	0.0979401047635161	0.00310254614621024
768	3162.3949049464	86.4245575077211	3.73403455974743	0.0000304187351123199	0.0979309642262069	0.00309704464105964
768.25	3163.32793998583	86.3577274108601	3.73024847569398	0.0000304280104558636	0.0979219827564392	0.00309156580675411
768.5	3164.26003055489	86.2910669424285	3.72647878052629	0.0000304372890737255	0.0979131595258224	0.00308610950158127
768.75	3165.19118073845	86.2245753051991	3.72272537562585	0.0000304465709376068	0.0979044937122952	0.00308067558501142
769	3166.12139459685	86.1582517073839	3.71898816316683	0.0000304558560194465	0.0978959845000625	0.00307526391768515
769.25	3167.05067616604	86.0920953625859	3.71526704610802	0.0000304651442914195	0.0978876310795329	0.00306987436140116
769.5	3167.97902945783	86.0261054897509	3.71156192818489	0.0000304744357259338	0.097879432647257	0.00306450677910415
769.75	3168.90645846004	85.9602813131205	3.70787271390176	0.0000304837302956284	0.0978713884058673	0.00305916103487299
770	3169.83296713674	85.8946220621844	3.70419930852399	0.0000304930279733711	0.097863497564017	0.00305383699390888
770.25	3170.75855942837	85.8291269716351	3.70054161807038	0.0000305023287322561	0.0978557593363216	0.00304853452252379
770.5	3171.68323925202	85.7637952813206	3.69689954930555	0.0000305116325456018	0.0978481729432994	0.00304325348812893
770.75	3172.60701050151	85.6986262362006	3.69327300973252	0.0000305209393869485	0.0978407376113143	0.00303799375922352
771	3173.52987704766	85.6336190863006	3.68966190758526	0.0000305302492300565	0.0978334525725179	0.00303275520538351
771.25	3174.45184273845	85.5687730866674	3.68606615182146	0.0000305395620489034	0.0978263170647933	0.00302753769725057
771.5	3175.37291139914	85.504087497326	3.68248565211527	0.0000305488778176828	0.097819330331699	0.00302234110652121
771.75	3176.29308683255	85.439561583235	3.67892031885023	0.0000305581965108013	0.0978124916224139	0.00301716530593592
772	3177.21237281915	85.3751946142447	3.67537006311219	0.0000305675181028769	0.0978058001916823	0.00301201016926864
772.25	3178.13077311729	85.3109858650543	3.6718347966824	0.0000305768425687372	0.0977992552997603	0.00300687557131614
772.5	3179.04829146333	85.2469346151692	3.66831443203064	0.0000305861698834166	0.0977928562123625	0.00300176138788772
772.75	3179.96493157186	85.18304014886	3.66480888230838	0.0000305955000221549	0.0977866022006089	0.00299666749579486
773	3180.88069713582	85.1193017551212	3.66131806134217	0.0000306048329603951	0.0977804925409735	0.00299159377284119
773.25	3181.79559182669	85.0557187276306	3.65784188362696	0.0000306141686737816	0.0977745265152323	0.00298654009781241
773.5	3182.70961929467	84.9922903647085	3.65438026431956	0.000030623507138158	0.0977687034104127	0.00298150635046642
773.75	3183.62278316882	84.9290159692785	3.65093311923218	0.0000306328483295652	0.0977630225187432	0.00297649241152357
774	3184.53508705726	84.8658948488276	3.64750036482606	0.0000306421922242398	0.0977574831376038	0.00297149816265699
774.25	3185.44653454726	84.8029263153672	3.64408191820513	0.0000306515387986119	0.097752084569477	0.00296652348648305
774.5	3186.35712920548	84.7401096853947	3.64067769710978	0.0000306608880293035	0.0977468261218989	0.00296156826655198
774.75	3187.26687457809	84.6774442798551	3.63728761991071	0.0000306702398931263	0.0977417071074117	0.0029566323873385
775	3188.17577419092	84.6149294241034	3.63391160560282	0.0000306795943670803	0.0977367268435162	0.00295171573423272
775.25	3189.08383154964	84.5525644478667	3.63054957379919	0.0000306889514283517	0.0977318846526247	0.00294681819353095
775.5	3189.99105013988	84.4903486852079	3.62720144472512	0.0000306983110543114	0.097727179862015	0.0029419396524268
775.75	3190.89743342741	84.4282814744886	3.62386713921228	0.000030707673222513	0.0977226118037846	0.00293707999900228
776	3191.80298485831	84.3663621583327	3.62054657869289	0.0000307170379106911	0.0977181798148051	0.00293223912221908
776.25	3192.70770785905	84.304590083591	3.6172396851939	0.0000307264050967597	0.097713883236678	0.00292741691190981
776.5	3193.61160583671	84.2429646013054	3.61394638133146	0.0000307357747588106	0.0977097214156903	0.00292261325876957
776.75	3194.51468217909	84.1814850666736	3.61066659030514	0.0000307451468751112	0.0977056937027703	0.0029178280543474
777	3195.41694025485	84.1201508390151	3.60740023589253	0.0000307545214241035	0.0977017994534453	0.00291306119103799
777.25	3196.31838341367	84.0589612817357	3.60414724244364	0.0000307638983844022	0.0976980380277981	0.00290831256207336
777.5	3197.21901498641	83.997915762294	3.60090753487554	0.0000307732777347928	0.0976944087904251	0.00290358206151475
777.75	3198.11883828521	83.9370136521682	3.59768103866702	0.0000307826594542305	0.0976909111103946	0.00289886958424457
778	3199.01785660364	83.8762543268216	3.59446767985321	0.0000307920435218383	0.0976875443612054	0.00289417502595834
778.25	3199.91607321688	83.8156371656705	3.59126738502044	0.0000308014299169053	0.0976843079207458	0.0028894982831569
778.5	3200.81349138179	83.7551615520512	3.58808008130099	0.0000308108186188856	0.0976812011712536	0.00288483925313862
778.75	3201.7101143371	83.6948268731878	3.58490569636801	0.0000308202096073964	0.0976782234992762	0.00288019783399167
779	3202.60594530354	83.6346325201596	3.58174415843045	0.0000308296028622165	0.0976753742956307	0.0028755739245864
779.25	3203.50098748391	83.5745778878703	3.57859539622806	0.000030838998363285	0.0976726529553652	0.00287096742456789
779.5	3204.39524406331	83.514662375016	3.57545933902643	0.0000308483960906996	0.0976700588777203	0.00286637823434846
779.75	3205.2887182092	83.4548853840542	3.57233591661213	0.0000308577960247155	0.0976675914660907	0.00286180625510036
780	3206.18141307156	83.3952463211736	3.56922505928784	0.0000308671981457433	0.0976652501279877	0.00285725138874849
780.25	3207.07333178299	83.3357445962628	3.56612669786761	0.0000308766024343483	0.0976630342750017	0.00285271353796324
780.5	3207.96447745888	83.2763796228808	3.56304076367209	0.0000308860088712485	0.0976609433227654	0.00284819260615339
780.75	3208.8548531975	83.2171508182272	3.55996718852388	0.0000308954174373134	0.0976589766909175	0.00284368849745908
781	3209.74446208014	83.1580576031122	3.5569059047429	0.0000309048281135628	0.0976571338030661	0.00283920111674489
781.25	3210.63330717125	83.0990994019278	3.55385684514185	0.0000309142408811652	0.0976554140867537	0.00283473036959303
781.5	3211.5213915185	83.0402756426187	3.55081994302163	0.0000309236557214364	0.0976538169734212	0.00283027616229646
781.75	3212.408718153	82.9815857566538	3.54779513216695	0.0000309330726158383	0.0976523418983736	0.00282583840185232
782	3213.29529008932	82.9230291789975	3.54478234684183	0.0000309424915459776	0.097650988300745	0.00282141699595521
782.25	3214.18111032569	82.8646053480821	3.54178152178529	0.0000309519124936044	0.097649755623465	0.00281701185299066
782.5	3215.06618184406	82.8063137057794	3.538792592207	0.0000309613354406107	0.0976486433132242	0.0028126228820287
782.75	3215.95050761025	82.7481536973738	3.53581549378302	0.0000309707603690295	0.0976476508204415	0.00280824999281743
783	3216.83409057405	82.6901247715346	3.53285016265154	0.0000309801872610332	0.0976467775992305	0.00280389309577666
783.25	3217.71693366937	82.6322263802892	3.52989653540876	0.0000309896160989327	0.0976460231073672	0.00279955210199173
783.5	3218.59903981428	82.5744579789966	3.52695454910469	0.0000309990468651757	0.0976453868062576	0.00279522692320725
783.75	3219.48041191121	82.5168190263202	3.52402414123911	0.0000310084795423458	0.0976448681609053	0.002790917471821
784	3220.36105284699	82.4593089842026	3.5211052497575	0.0000310179141131612	0.0976444666398808	0.00278662366087792
784.25	3221.24096549302	82.4019273178385	3.51819781304702	0.0000310273505604732	0.0976441817152888	0.00278234540406405
784.5	3222.12015270533	82.3446734956505	3.51530176993263	0.0000310367888672656	0.097644012862739	0.00277808261570073
784.75	3222.99861732471	82.2875469892623	3.51241705967306	0.000031046229016653	0.0976439595613136	0.00277383521073861
785	3223.87636217683	82.2305472734739	3.50954362195704	0.0000310556709918798	0.0976440212935386	0.00276960310475196
785.25	3224.75339007234	82.1736738262372	3.50668139689941	0.0000310651147763192	0.0976441975453528	0.00276538621393293
785.5	3225.62970380696	82.1169261286305	3.50383032503738	0.0000310745603534717	0.0976444878060785	0.00276118445508587
785.75	3226.5053061616	82.0603036648347	3.50099034732671	0.0000310840077069643	0.0976448915683922	0.00275699774562177
786	3227.38019990245	82.0038059221086	3.49816140513809	0.0000310934568205492	0.0976454083282956	0.00275282600355268
786.25	3228.25438778112	81.9474323907651	3.49534344025339	0.0000311029076781028	0.0976460375850866	0.00274866914748626
786.5	3229.12787253469	81.8911825641476	3.49253639486209	0.0000311123602636244	0.0976467788413311	0.00274452709662038
786.75	3230.00065688586	81.8350559386059	3.48974021155765	0.0000311218145612353	0.097647631602835	0.00274039977073772
787	3230.872743543	81.7790520134737	3.48695483333403	0.0000311312705551777	0.0976485953786161	0.00273628709020057
787.25	3231.74413520032	81.7231702910448	3.48418020358206	0.0000311407282298137	0.0976496696808766	0.00273218897594546
787.5	3232.61483453788	81.6674102765505	3.48141626608606	0.0000311501875696239	0.0976508540249761	0.00272810534947805
787.75	3233.48484422178	81.611771478137	3.47866296502036	0.0000311596485592069	0.0976521479294045	0.00272403613286804
788	3234.35416690417	81.5562534068431	3.47592024494591	0.0000311691111832776	0.0976535509157552	0.00271998124874402
788.25	3235.22280522341	81.5008555765776	3.4731880508069	0.0000311785754266669	0.0976550625086988	0.0027159406202885
788.5	3236.09076180416	81.4455775040974	3.47046632792747	0.0000311880412743203	0.0976566822359572	0.00271191417123296
788.75	3236.95803925742	81.390418708986	3.46775502200831	0.0000311975087112966	0.0976584096282774	0.00270790182585289
789	3237.8246401807	81.3353787136317	3.46505407912355	0.0000312069777227676	0.097660244219406	0.00270390350896302
789.25	3238.69056715803	81.2804570432059	3.4623634457174	0.0000312164482940167	0.0976621855460642	0.00269991914591242
789.5	3239.55582276015	81.2256532256424	3.45968306860101	0.0000312259204104378	0.0976642331479223	0.00269594866257981
789.75	3240.42040954451	81.1709667916163	3.45701289494933	0.0000312353940575348	0.097666386567575	0.00269199198536887
790	3241.28433005541	81.1163972745229	3.45435287229794	0.0000312448692209202	0.0976686453505173	0.00268804904120352
790.25	3242.14758682408	81.0619442104574	3.45170294853998	0.0000312543458863142	0.0976710090451196	0.0026841197575234
790.5	3243.01018236877	81.0076071381944	3.44906307192308	0.0000312638240395444	0.097673477202604	0.00268020406227926
790.75	3243.87211919483	80.9533855991678	3.44643319104634	0.0000312733036665438	0.0976760493770207	0.00267630188392851
791	3244.73339979481	80.8992791374503	3.44381325485732	0.0000312827847533508	0.0976787251252237	0.00267241315143069
791.25	3245.59402664854	80.8452872997341	3.44120321264904	0.0000312922672861079	0.0976815040068484	0.00266853779424312
791.5	3246.4540022232	80.7914096353111	3.43860301405712	0.000031301751251061	0.097684385584288	0.00266467574231653
791.75	3247.31332897344	80.7376456960535	3.4360126090568	0.000031311236634558	0.0976873694226707	0.00266082692609075
792	3248.17200934144	80.6839950363938	3.43343194796011	0.0000313207234230487	0.0976904550898374	0.00265699127649039
792.25	3249.03004575701	80.6304572133069	3.43086098141297	0.0000313302116030833	0.0976936421563188	0.00265316872492066
792.5	3249.88744063764	80.57703178629	3.42829966039241	0.0000313397011613119	0.0976969301953136	0.00264935920326318
792.75	3250.74419638861	80.5237183173446	3.42574793620381	0.0000313491920844835	0.097700318782667	0.00264556264387185
793	3251.6003154031	80.4705163709576	3.42320576047804	0.0000313586843594451	0.0977038074968479	0.00264177897956873
793.25	3252.4558000622	80.4174255140826	3.42067308516883	0.000031368177973141	0.0977073959189284	0.00263800814364
793.5	3253.31065273504	80.3644453161225	3.41814986254999	0.0000313776729126121	0.0977110836325621	0.00263425006983197
793.75	3254.16487577886	80.3115753489101	3.41563604521279	0.0000313871691649945	0.0977148702239629	0.00263050469234707
794	3255.01847153909	80.2588151866918	3.41313158606325	0.0000313966667175194	0.0977187552818848	0.00262677194583996
794.25	3255.87144234942	80.2061644061083	3.41063643831957	0.000031406165557512	0.0977227383976005	0.00262305176541363
794.5	3256.72379053189	80.1536225861776	3.40815055550948	0.0000314156656723905	0.0977268191648813	0.00261934408661555
794.75	3257.57551839696	80.1011893082781	3.40567389146773	0.0000314251670496656	0.0977309971799771	0.00261564884543386
795	3258.42662824357	80.0488641561305	3.40320640033347	0.0000314346696769398	0.097735272041596	0.00261196597829363
795.25	3259.27712235926	79.9966467157812	3.40074803654781	0.0000314441735419062	0.0977396433508845	0.0026082954220531
795.5	3260.12700302019	79.9445365755845	3.39829875485124	0.000031453678632348	0.0977441107114081	0.00260463711399999
795.75	3260.97627249127	79.8925333261873	3.39585851028124	0.0000314631849361381	0.097748673729132	0.00260099099184787
796	3261.82493302618	79.8406365605109	3.39342725816977	0.0000314726924412376	0.0977533320124009	0.00259735699373254
796.25	3262.67298686749	79.7888458737352	3.3910049541409	0.0000314822011356957	0.0977580851719214	0.00259373505820842
796.5	3263.52043624671	79.7371608632825	3.38859155410836	0.0000314917110076484	0.0977629328207419	0.00259012512424505
796.75	3264.36728338434	79.6855811288006	3.38618701427323	0.0000315012220453186	0.0977678745742345	0.00258652713122356
797	3265.21353048999	79.6341062721473	3.38379129112152	0.0000315107342370143	0.0977729100500764	0.0025829410189332
797.25	3266.05917976243	79.5827358973744	3.3814043414219	0.000031520247571129	0.0977780388682317	0.00257936672756792
797.5	3266.90423338964	79.5314696107116	3.37902612222339	0.00003152976203614	0.0977832606509327	0.00257580419772296
797.75	3267.74869354891	79.4803070205512	3.37665659085302	0.0000315392776206085	0.0977885750226629	0.00257225337039148
798	3268.59256240689	79.429247737432	3.37429570491366	0.0000315487943131782	0.0977939816101381	0.00256871418696121
798.25	3269.43584211967	79.3782913740248	3.37194342228172	0.0000315583121025755	0.0977994800422899	0.00256518658921122
798.5	3270.27853483284	79.3274375451165	3.36959970110495	0.0000315678309776077	0.0978050699502472	0.00256167051930856
798.75	3271.12064268155	79.2766858675949	3.36726449980026	0.0000315773509271634	0.0978107509673195	0.0025581659198051
799	3271.96216779061	79.2260359604346	3.36493777705154	0.0000315868719402111	0.0978165227289802	0.00255467273363429
799.25	3272.80311227451	79.1754874446809	3.36261949180753	0.0000315963940057989	0.0978223848728486	0.00255119090410803
799.5	3273.64347823753	79.1250399434362	3.36030960327964	0.0000316059171130538	0.0978283370386738	0.00254772037491347
799.75	3274.48326777379	79.0746930818447	3.35800807093989	0.0000316154412511808	0.097834378868318	0.00254426109010999
800	3275.32248296727	79.0244464870781	3.3557148545188	0.0000316249664094627	0.09784051000574	0.00254081299412602
800.25	3276.16112589197	78.9742997883216	3.35342991400336	0.000031634492577259	0.0978467300969789	0.0025373760317561
800.5	3276.99919861187	78.9242526167592	3.35115320963489	0.0000316440197440057	0.0978530387901378	0.00253395014815781
800.75	3277.83670318108	78.8743046055601	3.34888470190712	0.0000316535478992144	0.0978594357353682	0.00253053528884879
801	3278.67364164384	78.8244553898644	3.34662435156414	0.0000316630770324716	0.0978659205848536	0.0025271313997038
801.25	3279.51001603461	78.7747046067693	3.34437211959836	0.0000316726071334386	0.0978724929927942	0.00252373842695176
801.5	3280.34582837815	78.7250518953153	3.34212796724862	0.0000316821381918501	0.0978791526153913	0.00252035631717291
801.75	3281.18108068953	78.6754968964731	3.33989185599821	0.0000316916701975145	0.0978858991108318	0.0025169850172959
802	3282.01577497424	78.6260392531295	3.3376637475729	0.0000317012031403124	0.0978927321392731	0.00251362447459495
802.25	3282.84991322822	78.5766786100743	3.33544360393908	0.0000317107370101969	0.0978996513628278	0.00251027463668707
802.5	3283.68349743795	78.527414613987	3.33323138730184	0.0000317202717971921	0.0979066564455487	0.00250693545152922
802.75	3284.51652958048	78.4782469134238	3.33102706010309	0.0000317298074913935	0.0979137470534146	0.00250360686741562
803	3285.34901162349	78.4291751588045	3.32883058501971	0.0000317393440829666	0.0979209228543145	0.00250028883297496
803.25	3286.18094552538	78.3801990023992	3.32664192496171	0.0000317488815621466	0.0979281835180341	0.00249698129716774
803.5	3287.01233323528	78.3313180983162	3.32446104307037	0.0000317584199192382	0.0979355287162408	0.00249368420928355
803.75	3287.84317669316	78.2825321024888	3.32228790271649	0.0000317679591446146	0.0979429581224697	0.00249039751893846
804	3288.67347782984	78.2338406726629	3.32012246749855	0.000031777499228717	0.0979504714121093	0.00248712117607238
804.25	3289.50323856709	78.1852434683845	3.31796470124099	0.0000317870401620543	0.0979580682623874	0.00248385513094642
804.5	3290.33246081763	78.1367401509871	3.31581456799237	0.0000317965819352022	0.0979657483523575	0.00248059933414037
804.75	3291.16114648527	78.0883303835799	3.31367203202371	0.0000318061245388032	0.0979735113628849	0.00247735373655014
805	3291.98929746486	78.0400138310352	3.31153705782676	0.0000318156679635654	0.0979813569766331	0.0024741182893852
805.25	3292.81691564245	77.9917901599764	3.3094096101122	0.0000318252122002625	0.0979892848780501	0.00247089294416607
805.5	3293.64400289525	77.9436590387666	3.3072896538081	0.0000318347572397331	0.0979972947533555	0.00246767765272195
805.75	3294.47056109177	77.8956201374957	3.30517715405808	0.0000318443030728801	0.0980053862905268	0.00246447236718811
806	3295.29659209181	77.8476731279696	3.3030720762198	0.0000318538496906704	0.0980135591792862	0.00246127704000357
806.25	3296.12209774653	77.7998176836979	3.30097438586319	0.000031863397084134	0.0980218131110883	0.00245809162390863
806.5	3296.94707989852	77.7520534798829	3.29888404876891	0.000031872945244364	0.0980301477791063	0.00245491607194255
806.75	3297.77154038186	77.7043801934076	3.2968010309267	0.0000318824941625158	0.0980385628782199	0.00245175033744111
807	3298.59548102211	77.6567975028244	3.29472529853374	0.0000318920438298067	0.0980470581050022	0.00244859437403432
807.25	3299.41890363643	77.6093050883445	3.29265681799317	0.0000319015942375152	0.0980556331577077	0.00244544813564412
807.5	3300.24181003362	77.5619026318255	3.29059555591241	0.0000319111453769809	0.0980642877362591	0.002442311576482
807.75	3301.06420201414	77.5145898167617	3.28854147910167	0.0000319206972396038	0.0980730215422358	0.00243918465104684
808	3301.88608137016	77.467366328272	3.28649455457238	0.0000319302498168438	0.0980818342788612	0.00243606731412256
808.25	3302.70744988567	77.4202318530893	3.28445474953567	0.0000319398031002201	0.0980907256509907	0.00243295952077593
808.5	3303.52830933645	77.3731860795501	3.28242203140087	0.0000319493570813112	0.0980996953650997	0.00242986122635438
808.75	3304.34866149019	77.3262286975833	3.280396367774	0.000031958911751754	0.0981087431292719	0.00242677238648377
809	3305.16850810647	77.2793593986997	3.27837772645626	0.0000319684671032435	0.0981178686531875	0.00242369295706623
809.25	3305.98785093687	77.2325778759815	3.27636607544261	0.0000319780231275322	0.0981270716481113	0.00242062289427804
809.5	3306.80669172498	77.1858838240718	3.27436138292027	0.0000319875798164301	0.0981363518268813	0.00241756215456748
809.75	3307.62503220648	77.1392769391641	3.27236361726729	0.0000319971371618035	0.0981457089038974	0.00241451069465269
810	3308.44287410914	77.0927569189923	3.2703727470511	0.0000320066951555755	0.0981551425951099	0.00241146847151964
810.25	3309.26021915291	77.0463234628205	3.26838874102712	0.0000320162537897246	0.0981646526180083	0.00240843544242005
810.5	3310.07706904997	76.9999762714321	3.26641156813734	0.0000320258130562849	0.0981742386916097	0.00240541156486926
810.75	3310.89342550472	76.9537150471208	3.26444119750892	0.0000320353729473456	0.0981839005364488	0.00240239679664432
811	3311.70929021389	76.9075394936802	3.26247759845282	0.0000320449334550503	0.098193637874566	0.0023993910957819
811.25	3312.52466486657	76.8614493163938	3.2605207404624	0.0000320544945715969	0.0982034504294969	0.0023963944205763
811.5	3313.33955114421	76.8154442220252	3.25857059321212	0.0000320640562892368	0.0982133379262616	0.00239340672957749
811.75	3314.15395072074	76.7695239188087	3.25662712655614	0.0000320736186002749	0.0982233000913538	0.00239042798158916
812	3314.96786526255	76.7236881164395	3.25469031052702	0.000032083181497069	0.0982333366527306	0.00238745813566677
812.25	3315.78129642858	76.6779365260636	3.2527601153344	0.0000320927449720292	0.0982434473398018	0.0023844971511156
812.5	3316.59424587032	76.6322688602694	3.25083651136368	0.000032102309017618	0.0982536318834194	0.00238154498748891
812.75	3317.4067152319	76.5866848330774	3.2489194691747	0.0000321118736263493	0.0982638900158675	0.00237860160458601
813	3318.21870615011	76.5411841599311	3.24700895950051	0.0000321214387907883	0.0982742214708524	0.00237566696245037
813.25	3319.03022025442	76.4957665576881	3.24510495324606	0.0000321310045035514	0.0982846259834916	0.00237274102136782
813.5	3319.84125916708	76.4504317446101	3.24320742148692	0.0000321405707573052	0.0982951032903048	0.00236982374186469
813.75	3320.65182450311	76.4051794403548	3.24131633546809	0.0000321501375447665	0.0983056531292032	0.00236691508470597
814	3321.46191787037	76.3600093659662	3.2394316666027	0.0000321597048587019	0.0983162752394802	0.00236401501089354
814.25	3322.27154086959	76.3149212438655	3.23755338647079	0.0000321692726919273	0.0983269693618013	0.00236112348166437
814.5	3323.08069509442	76.269914797843	3.23568146681813	0.0000321788410373076	0.0983377352381945	0.00235824045848876
814.75	3323.88938213147	76.2249897530485	3.23381587955497	0.0000321884098877564	0.0983485726120407	0.00235536590306857
815	3324.69760356034	76.1801458359828	3.23195659675487	0.0000321979792362353	0.0983594812280643	0.00235249977733547
815.25	3325.50536095367	76.1353827744891	3.23010359065347	0.0000322075490757541	0.0983704608323238	0.00234964204344928
815.5	3326.31265587718	76.0907002977443	3.2282568336474	0.0000322171193993697	0.0983815111722023	0.00234679266379618
815.75	3327.11948988972	76.0460981362506	3.22641629829301	0.0000322266902001866	0.0983926319963981	0.00234395160098708
816	3327.92586454327	76.0015760218265	3.22458195730528	0.0000322362614713559	0.0984038230549159	0.00234111881785592
816.25	3328.73178138305	75.9571336875995	3.22275378355666	0.0000322458332060749	0.0984150840990576	0.00233829427745799
816.5	3329.53724194748	75.9127708679962	3.22093175007595	0.0000322554053975874	0.0984264148814131	0.00233547794306834
816.75	3330.34224776827	75.8684872987356	3.21911583004712	0.0000322649780391827	0.0984378151558513	0.00233266977818008
817	3331.14680037045	75.8242827168195	3.21730599680825	0.0000322745511241955	0.0984492846775116	0.00232986974650282
817.25	3331.95090127241	75.7801568605256	3.21550222385041	0.0000322841246460057	0.0984608232027948	0.00232707781196101
817.5	3332.75455198592	75.7361094693982	3.21370448481655	0.0000322936985980376	0.0984724304893543	0.00232429393869243
817.75	3333.55775401617	75.6921402842412	3.21191275350041	0.0000323032729737604	0.0984841062960878	0.00232151809104651
818	3334.36050886184	75.6482490471096	3.21012700384548	0.0000323128477666868	0.0984958503831284	0.00231875023358289
818.25	3335.1628180151	75.6044355013018	3.20834720994386	0.0000323224229703737	0.0985076625118364	0.00231599033106976
818.5	3335.96468296167	75.5606993913513	3.20657334603527	0.0000323319985784209	0.0985195424447905	0.0023132383484824
818.75	3336.76610518084	75.5170404630197	3.20480538650598	0.0000323415745844716	0.0985314899457798	0.00231049425100165
819	3337.56708614551	75.4734584632885	3.20304330588775	0.0000323511509822117	0.0985435047797953	0.00230775800401237
819.25	3338.36762732225	75.4299531403515	3.20128707885681	0.0000323607277653695	0.0985555867130218	0.00230502957310198
819.5	3339.16773017131	75.3865242436072	3.19953668023283	0.0000323703049277154	0.0985677355128296	0.00230230892405898
819.75	3339.96739614665	75.3431715236511	3.19779208497793	0.0000323798824630616	0.0985799509477666	0.00229959602287144
820	3340.766626696	75.2998947322689	3.19605326819563	0.0000323894603652617	0.0985922327875503	0.00229689083572562
820.25	3341.56542326088	75.2566936224281	3.1943202051299	0.0000323990386282105	0.0986045808030595	0.00229419332900445
820.5	3342.36378727664	75.2135679482714	3.19259287116412	0.0000324086172458439	0.098616994766327	0.00229150346928618
820.75	3343.16172017249	75.170517465109	3.19087124182017	0.0000324181962121381	0.0986294744505313	0.00228882122334287
821	3343.95922337155	75.1275419294114	3.18915529275737	0.0000324277755211097	0.0986420196299891	0.00228614655813909
821.25	3344.75629829085	75.0846410988024	3.18744499977158	0.0000324373551668152	0.0986546300801475	0.00228347944083043
821.5	3345.5529463414	75.0418147320517	3.18574033879423	0.0000324469351433508	0.0986673055775765	0.0022808198387622
821.75	3346.34916892821	74.9990625890681	3.18404128589135	0.0000324565154448521	0.0986800458999614	0.00227816771946803
822	3347.14496745032	74.956384430892	3.18234781726267	0.0000324660960654937	0.0986928508260952	0.00227552305066849
822.25	3347.94034330084	74.913780019689	3.18065990924065	0.0000324756769994892	0.0987057201358715	0.00227288580026978
822.5	3348.73529786698	74.8712491187424	3.17897753828955	0.0000324852582410906	0.0987186536102765	0.00227025593636238
822.75	3349.52983253007	74.8287914924469	3.17730068100457	0.0000324948397845881	0.0987316510313825	0.00226763342721976
823	3350.32394866562	74.7864069063012	3.17562931411089	0.0000325044216243098	0.09874471218234	0.00226501824129702
823.25	3351.11764764333	74.744095126902	3.17396341446278	0.0000325140037546218	0.0987578368473709	0.00226241034722963
823.5	3351.91093082713	74.7018559219361	3.1723029590427	0.0000325235861699271	0.0987710248117611	0.00225980971383212
823.75	3352.70379957522	74.6596890601749	3.17064792496045	0.0000325331688646663	0.0987842758618536	0.00225721631009681
824	3353.49625524008	74.6175943114673	3.16899828945224	0.0000325427518333165	0.0987975897850416	0.00225463010519257
824.25	3354.28829916852	74.5755714467329	3.16735402987985	0.0000325523350703917	0.0988109663697613	0.00225205106846354
824.5	3355.07993270172	74.5336202379559	3.16571512372978	0.0000325619185704419	0.0988244054054849	0.00224947916942786
824.75	3355.87115717521	74.4917404581784	3.16408154861233	0.0000325715023280534	0.0988379066827143	0.00224691437777649
825	3356.66197391899	74.449931881494	3.16245328226082	0.0000325810863378482	0.0988514699929738	0.00224435666337197
825.25	3357.45238425746	74.4081942830415	3.16083030253072	0.0000325906705944839	0.0988650951288036	0.00224180599624719
825.5	3358.24238950953	74.3665274389984	3.1592125873988	0.0000326002550926531	0.0988787818837529	0.00223926234660419
825.75	3359.03199098861	74.3249311265749	3.15760011496233	0.0000326098398270839	0.0988925300523738	0.00223672568481299
826	3359.82119000265	74.2834051240075	3.1559928634382	0.0000326194247925387	0.0989063394302141	0.0022341959814104
826.25	3360.60998785415	74.2419492105527	3.1543908111622	0.0000326290099838147	0.0989202098138111	0.00223167320709884
826.5	3361.39838584025	74.2005631664811	3.15279393658812	0.0000326385953957432	0.0989341410006852	0.00222915733274516
826.75	3362.18638525268	74.1592467730711	3.151202218287	0.0000326481810231897	0.0989481327893334	0.00222664832937955
827	3362.97398737785	74.117999812603	3.1496156349463	0.0000326577668610533	0.0989621849792228	0.00222414616819431
827.25	3363.76119349684	74.0768220683528	3.14803416536915	0.0000326673529042666	0.0989762973707846	0.00222165082054279
827.5	3364.54800488545	74.0357133245868	3.14645778847355	0.0000326769391477957	0.0989904697654076	0.00221916225793825
827.75	3365.33442281424	73.9946733665546	3.14488648329155	0.0000326865255866395	0.099004701965432	0.00221668045205271
828	3366.12044854853	73.9537019804844	3.14332022896857	0.0000326961122158299	0.0990189937741436	0.00221420537471588
828.25	3366.90608334843	73.9127989535767	3.14175900476255	0.0000327056990304312	0.0990333449957669	0.00221173699791407
828.5	3367.69132846888	73.8719640739979	3.14020279004326	0.0000327152860255402	0.0990477554354601	0.00220927529378907
828.75	3368.47618515971	73.8311971308757	3.13865156429148	0.0000327248731962858	0.0990622248993081	0.00220682023463709
829	3369.26065466559	73.7904979142926	3.13710530709832	0.0000327344605378286	0.0990767531943173	0.00220437179290773
829.25	3370.04473822612	73.7498662152804	3.13556399816444	0.000032744048045361	0.0990913401284091	0.00220192994120283
829.5	3370.82843707585	73.7093018258149	3.13402761729933	0.0000327536357141068	0.0991059855104144	0.00219949465227552
829.75	3371.61175244427	73.6688045388097	3.13249614442058	0.000032763223539321	0.0991206891500678	0.00219706589902911
830	3372.39468555589	73.6283741481113	3.13096955955317	0.0000327728115162895	0.0991354508580014	0.00219464365451606
830.25	3373.17723763022	73.5880104484933	3.12944784282874	0.0000327823996403291	0.0991502704457396	0.00219222789193702
830.5	3373.95940988182	73.5477132356508	3.12793097448487	0.0000327919879067869	0.0991651477256932	0.00218981858463971
830.75	3374.74120352034	73.5074823061953	3.1264189348644	0.0000328015763110406	0.0991800825111534	0.00218741570611802
831	3375.5226197505	73.4673174576494	3.12491170441471	0.0000328111648484978	0.0991950746162869	0.00218501923001093
831.25	3376.30365977217	73.4272184884407	3.12340926368707	0.0000328207535145962	0.0992101238561299	0.00218262913010154
831.5	3377.08432478035	73.3871851978974	3.12191159333587	0.0000328303423048028	0.0992252300465825	0.00218024538031611
831.75	3377.86461596524	73.3472173862427	3.12041867411803	0.0000328399312146145	0.0992403930044036	0.00217786795472307
832	3378.64453451222	73.3073148545895	3.11893048689226	0.0000328495202395572	0.0992556125472054	0.00217549682753204
832.25	3379.4240816019	73.2674774049351	3.11744701261841	0.0000328591093751858	0.0992708884934474	0.00217313197309288
832.5	3380.20325841016	73.2277048401564	3.11596823235681	0.0000328686986170844	0.0992862206624321	0.00217077336589475
832.75	3380.98206610814	73.1879969640045	3.11449412726759	0.0000328782879608653	0.0993016088742989	0.00216842098056515
833	3381.76050586229	73.1483535810999	3.11302467861006	0.0000328878774021696	0.0993170529500193	0.00216607479186899
833.25	3382.53857883438	73.1087744969271	3.111559867742	0.0000328974669366664	0.0993325527113912	0.00216373477470764
833.5	3383.31628618155	73.0692595178299	3.11009967611909	0.0000329070565600529	0.0993481079810342	0.00216140090411808
833.75	3384.09362905629	73.0298084510061	3.1086440852942	0.0000329166462680543	0.0993637185823845	0.00215907315527186
834	3384.87060860651	72.990421104503	3.10719307691681	0.0000329262360564231	0.0993793843396891	0.00215675150347434
834.25	3385.64722597554	72.9510972872123	3.10574663273235	0.0000329358259209398	0.0993951050780016	0.00215443592416369
834.5	3386.42348230216	72.9118368088652	3.10430473458155	0.0000329454158574115	0.0994108806231767	0.00215212639291002
834.75	3387.1993787206	72.8726394800273	3.1028673643999	0.000032955005861673	0.0994267108018653	0.00214982288541451
835	3387.97491636062	72.8335051120946	3.10143450421694	0.0000329645959295855	0.0994425954415098	0.00214752537750854
835.25	3388.75009634749	72.7944335172878	3.10000613615573	0.0000329741860570372	0.0994585343703386	0.00214523384515279
835.5	3389.52491980199	72.7554245086484	3.09858224243219	0.0000329837762399427	0.099474527417362	0.0021429482644364
835.75	3390.29938784052	72.7164779000332	3.09716280535451	0.0000329933664742429	0.0994905744123668	0.00214066861157609
836	3391.07350157502	72.6775935061104	3.09574780732257	0.0000330029567559049	0.0995066751859117	0.00213839486291535
836.25	3391.84726211306	72.6387711423545	3.09433723082734	0.0000330125470809216	0.0995228295693227	0.00213612699492355
836.5	3392.62067055786	72.6000106250419	3.0929310584503	0.0000330221374453119	0.099539037394688	0.00213386498419516
836.75	3393.39372800827	72.5613117712461	3.09152927286283	0.0000330317278451202	0.0995552984948536	0.00213160880744884
837	3394.16643555883	72.5226743988337	3.09013185682566	0.0000330413182764163	0.0995716127034189	0.0021293584415267
837.25	3394.93879429979	72.4840983264592	3.08873879318829	0.0000330509087352952	0.0995879798547314	0.00212711386339344
837.5	3395.71080531711	72.445583373561	3.0873500648884	0.0000330604992178771	0.0996043997838826	0.00212487505013555
837.75	3396.48246969251	72.4071293603569	3.08596565495132	0.000033070089720307	0.0996208723267035	0.00212264197896048
838	3397.25378850345	72.3687361078397	3.08458554648946	0.0000330796802387547	0.0996373973197598	0.00212041462719592
838.25	3398.02476282321	72.3304034377726	3.08320972270172	0.0000330892707694145	0.0996539746003475	0.00211819297228889
838.5	3398.79539372086	72.2921311726851	3.08183816687299	0.0000330988613085049	0.099670604006489	0.00211597699180509
838.75	3399.56568226132	72.2539191358686	3.08047086237355	0.000033108451852269	0.0996872853769276	0.00211376666342799
839	3400.33562950534	72.2157671513722	3.07910779265858	0.0000331180423969737	0.0997040185511242	0.00211156196495818
839.25	3401.10523650956	72.1776750439983	3.07774894126758	0.0000331276329389098	0.0997208033692523	0.00210936287431249
839.5	3401.87450432653	72.1396426392985	3.07639429182383	0.0000331372234743918	0.0997376396721939	0.00210716936952334
839.75	3402.64343400467	72.1016697635693	3.07504382803391	0.0000331468139997579	0.0997545273015353	0.00210498142873787
840	3403.41202658838	72.0637562438481	3.07369753368713	0.0000331564045113694	0.0997714660995628	0.00210279903021732
840.25	3404.180283118	72.0259019079088	3.07235539265499	0.0000331659950056112	0.0997884559092583	0.00210062215233615
840.5	3404.94820462986	71.9881065842578	3.07101738889072	0.0000331755854788911	0.0998054965742954	0.00209845077358144
840.75	3405.71579215627	71.9503701021302	3.06968350642871	0.0000331851759276397	0.099822587939035	0.00209628487255203
841	3406.48304672557	71.9126922914855	3.06835372938405	0.0000331947663483104	0.0998397298485216	0.00209412442795791
841.25	3407.24996936213	71.8750729830035	3.06702804195196	0.0000332043567373795	0.0998569221484785	0.00209196941861941
841.5	3408.0165610864	71.83751200808	3.06570642840733	0.0000332139470913453	0.0998741646853043	0.00208981982346655
841.75	3408.78282291489	71.8000091988239	3.06438887310422	0.0000332235374067286	0.099891457306069	0.00208767562153828
842	3409.54875586021	71.7625643880522	3.06307536047535	0.0000332331276800725	0.0999087998585092	0.00208553679198182
842.25	3410.31436093109	71.7251774092866	3.06176587503161	0.0000332427179079418	0.099926192191025	0.00208340331405194
842.5	3411.0796391324	71.6878480967492	3.06046040136156	0.0000332523080869234	0.0999436341526755	0.00208127516711028
842.75	3411.84459146517	71.6505762853592	3.05915892413098	0.0000332618982136257	0.0999611255931754	0.00207915233062462
843	3412.60921892659	71.6133618107287	3.05786142808235	0.0000332714882846787	0.0999786663628904	0.00207703478416828
843.25	3413.37352251006	71.576204509159	3.05656789803441	0.0000332810782967338	0.0999962563128338	0.00207492250741938
843.5	3414.1375032052	71.5391042176366	3.05527831888163	0.0000332906682464637	0.100013895294663	0.00207281548016016
843.75	3414.90116199784	71.5020607738297	3.05399267559381	0.0000333002581305622	0.100031583160675	0.00207071368227639
844	3415.66449987009	71.4650740160845	3.05271095321555	0.000033309847945744	0.100049319763802	0.00206861709375661
844.25	3416.4275178003	71.4281437834213	3.05143313686583	0.0000333194376887447	0.100067104957611	0.00206652569469157
844.5	3417.19021676313	71.3912699155308	3.05015921173753	0.0000333290273563205	0.100084938596296	0.00206443946527349
844.75	3417.95259772955	71.3544522527708	3.04888916309697	0.0000333386169452482	0.100102820534675	0.00206235838579549
845	3418.71466166684	71.3176906361619	3.04762297628348	0.000033348206452325	0.10012075062819	0.00206028243665089
845.25	3419.47640953864	71.2809849073847	3.04636063670891	0.0000333577958743684	0.100138728732898	0.00205821159833262
845.5	3420.23784230493	71.2443349087755	3.04510212985722	0.000033367385208216	0.100156754705472	0.00205614585143257
845.75	3420.99896092209	71.2077404833234	3.04384744128403	0.0000333769744507253	0.100174828403194	0.00205408517664096
846	3421.75976634289	71.171201474666	3.04259655661616	0.0000333865635987739	0.100192949683953	0.00205202955474569
846.25	3422.52025951653	71.1347177270864	3.04134946155121	0.0000333961526492588	0.100211118406244	0.0020499789666318
846.5	3423.28044138862	71.0982890855098	3.04010614185712	0.0000334057415990969	0.100229334429158	0.00204793339328079
846.75	3424.04031290122	71.0619153954997	3.03886658337176	0.0000334153304452244	0.100247597612386	0.00204589281577005
847	3424.79987499289	71.0255965032546	3.03763077200245	0.0000334249191845968	0.100265907816208	0.0020438572152722
847.25	3425.55912859864	70.9893322556046	3.03639869372562	0.0000334345078141889	0.100284264901497	0.00204182657305459
847.5	3426.31807465	70.9531225000081	3.03517033458628	0.0000334440963309946	0.10030266872971	0.00203980087047861
847.75	3427.07671407502	70.9169670845479	3.03394568069773	0.0000334536847320267	0.100321119162887	0.00203778008899915
848	3427.83504779829	70.8808658579287	3.03272471824101	0.0000334632730143166	0.100339616063649	0.002035764210164
848.25	3428.59307674093	70.8448186694732	3.03150743346461	0.0000334728611749149	0.100358159295191	0.00203375321561329
848.5	3429.35080182066	70.8088253691186	3.03029381268396	0.0000334824492108902	0.10037674872128	0.00203174708707888
848.75	3430.10822395178	70.772885807414	3.02908384228111	0.00003349203711933	0.100395384206256	0.00202974580638382
849	3430.86534404518	70.7369998355166	3.02787750870427	0.0000335016248973399	0.100414065615021	0.00202774935544175
849.25	3431.62216300839	70.7011673051886	3.02667479846742	0.0000335112125420436	0.100432792813042	0.00202575771625636
849.5	3432.37868174555	70.6653880687941	3.02547569814993	0.0000335208000505832	0.100451565666345	0.00202377087092085
849.75	3433.13490115748	70.6296619792955	3.02428019439616	0.0000335303874201185	0.100470384041514	0.0020217888016173
850	3433.89082214166	70.593988890251	3.02308827391505	0.0000335399746478271	0.100489247805683	0.00201981149061622
850.25	3434.64644559225	70.5583686558108	3.02189992347977	0.0000335495617309046	0.10050815682654	0.00201783892027593
850.5	3435.40177240011	70.5228011307142	3.02071512992728	0.000033559148666564	0.100527110972316	0.00201587107304202
850.75	3436.15680345283	70.4872861702866	3.01953388015801	0.0000335687354520358	0.100546110111789	0.00201390793144687
851	3436.91153963472	70.4518236304361	3.01835616113541	0.0000335783220845679	0.100565154114276	0.00201194947810903
851.25	3437.66598182684	70.416413367651	3.01718195988565	0.0000335879085614254	0.100584242849632	0.00200999569573279
851.5	3438.42013090702	70.3810552389959	3.01601126349717	0.0000335974948798906	0.100603376188248	0.00200804656710754
851.75	3439.17398774988	70.3457491021095	3.01484405912037	0.0000336070810372629	0.100622554001045	0.00200610207510734
852	3439.92755322681	70.3104948152008	3.01368033396719	0.0000336166670308586	0.100641776159473	0.00200416220269036
852.25	3440.68082820603	70.2752922370469	3.01252007531079	0.0000336262528580105	0.100661042535508	0.00200222693289836
852.5	3441.43381355257	70.2401412269894	3.01136327048515	0.0000336358385160685	0.100680353001647	0.0020002962488562
852.75	3442.18651012833	70.2050416449317	3.01020990688471	0.000033645424002399	0.10069970743091	0.0019983701337713
853	3442.93891879202	70.169993351336	3.00905997196404	0.0000336550093143846	0.100719105696831	0.00199644857093319
853.25	3443.69104039928	70.1349962072204	3.00791345323746	0.0000336645944494246	0.100738547673459	0.00199453154371294
853.5	3444.44287580257	70.1000500741562	3.0067703382787	0.0000336741794049343	0.100758033235354	0.00199261903556272
853.75	3445.19442585131	70.0651548142645	3.00563061472052	0.0000336837641783454	0.100777562257583	0.00199071103001527
854	3445.9456913918	70.0303102902139	3.00449427025439	0.0000336933487671055	0.10079713461572	0.00198880751068346
854.25	3446.69667326729	69.995516365217	3.00336129263015	0.0000337029331686781	0.10081675018584	0.00198690846125973
854.5	3447.44737231795	69.9607729030286	3.00223166965563	0.0000337125173805426	0.100836408844519	0.00198501386551566
854.75	3448.19778938093	69.9260797679417	3.00110538919634	0.0000337221014001942	0.10085611046883	0.00198312370730149
855	3448.94792529036	69.8914368247856	2.99998243917513	0.0000337316852251436	0.100875854936337	0.00198123797054562
855.25	3449.69778087733	69.8568439389226	2.99886280757181	0.0000337412688529171	0.1008956421251	0.00197935663925415
855.5	3450.44735696995	69.8223009762456	2.99774648242289	0.0000337508522810564	0.100915471913664	0.00197747969751044
855.75	3451.19665439335	69.7878078031749	2.99663345182119	0.0000337604355071186	0.100935344181061	0.00197560712947457
856	3451.94567396969	69.7533642866563	2.99552370391551	0.0000337700185286758	0.100955258806808	0.00197373891938297
856.25	3452.69441651815	69.7189702941572	2.99441722691035	0.0000337796013433156	0.1009752156709	0.00197187505154788
856.5	3453.442882855	69.6846256936652	2.99331400906555	0.0000337891839486403	0.100995214653811	0.00197001551035695
856.75	3454.19107379357	69.6503303536844	2.99221403869594	0.0000337987663422673	0.101015255636489	0.00196816028027278
857	3454.93899014427	69.6160841432334	2.9911173041711	0.0000338083485218287	0.101035338500358	0.00196630934583244
857.25	3455.68663271461	69.5818869318422	2.99002379391496	0.0000338179304849715	0.101055463127309	0.00196446269164705
857.5	3456.43400230921	69.5477385895499	2.98893349640553	0.0000338275122293572	0.1010756293997	0.00196262030240133
857.75	3457.18109972984	69.513638986902	2.98784640017457	0.000033837093752662	0.101095837200357	0.00196078216285318
858	3457.92792577538	69.479587994948	2.98676249380728	0.0000338466750525763	0.101116086412565	0.00195894825783321
858.25	3458.67448124188	69.4455854852383	2.98568176594201	0.0000338562561268051	0.101136376920071	0.00195711857224434
858.5	3459.42076692254	69.4116313298221	2.9846042052699	0.0000338658369730677	0.101156708607078	0.00195529309106132
858.75	3460.16678360776	69.3777254012449	2.98352980053464	0.0000338754175890972	0.101177081358245	0.00195347179933039
859	3460.91253208512	69.3438675725456	2.98245854053213	0.0000338849979726413	0.101197495058681	0.00195165468216876
859.25	3461.65801313941	69.3100577172543	2.98139041411017	0.0000338945781214612	0.101217949593948	0.00194984172476426
859.5	3462.40322755263	69.2762957093898	2.98032541016821	0.0000339041580333324	0.101238444850053	0.00194803291237487
859.75	3463.14817610403	69.242581423457	2.97926351765698	0.0000339137377060438	0.101258980713449	0.00194622823032837
860	3463.89285957007	69.2089147344445	2.97820472557826	0.0000339233171373986	0.10127955707103	0.00194442766402185
860.25	3464.63727872452	69.175295517822	2.97714902298456	0.0000339328963252129	0.101300173810132	0.00194263119892136
860.5	3465.38143433836	69.1417236495381	2.97609639897882	0.000033942475267317	0.101320830818528	0.00194083882056148
860.75	3466.12532717989	69.108199006018	2.97504684271415	0.0000339520539615544	0.101341527984426	0.00193905051454492
861	3466.8689580147	69.0747214641606	2.9740003433935	0.0000339616324057817	0.101362265196467	0.00193726626654213
861.25	3467.61232760568	69.0412909013367	2.97295689026943	0.0000339712105978693	0.101383042343722	0.00193548606229088
861.5	3468.35543671304	69.0079071953859	2.97191647264377	0.0000339807885357005	0.101403859315693	0.00193370988759588
861.75	3469.09828609431	68.9745702246152	2.9708790798674	0.0000339903662171717	0.101424716002305	0.00193193772832839
862	3469.8408765044	68.9412798677958	2.96984470133989	0.0000339999436401923	0.101445612293908	0.00193016957042583
862.25	3470.58320869553	68.9080360041614	2.96881332650933	0.000034009520802685	0.101466548081273	0.0019284053998914
862.5	3471.32528341732	68.8748385134053	2.96778494487194	0.0000340190977025849	0.101487523255591	0.00192664520279366
862.75	3472.06710141676	68.8416872756787	2.96675954597189	0.0000340286743378401	0.101508537708468	0.00192488896526619
863	3472.80866343823	68.8085821715879	2.96573711940096	0.0000340382507064115	0.101529591331927	0.00192313667350721
863.25	3473.54997022352	68.7755230821924	2.96471765479834	0.0000340478268062724	0.101550684018402	0.00192138831377917
863.5	3474.29102251183	68.7425098890026	2.96370114185028	0.0000340574026354088	0.101571815660737	0.00191964387240842
863.75	3475.03182103979	68.7095424739772	2.9626875702899	0.0000340669781918191	0.101592986152185	0.0019179033357848
864	3475.77236654147	68.6766207195214	2.96167692989688	0.0000340765534735141	0.101614195386405	0.00191616669036131
864.25	3476.51265974838	68.6437445084845	2.96066921049719	0.0000340861284785168	0.101635443257458	0.0019144339226537
864.5	3477.25270138952	68.6109137241578	2.95966440196289	0.0000340957032048626	0.101656729659808	0.00191270501924015
864.75	3477.99249219132	68.5781282502723	2.9586624942118	0.0000341052776505989	0.101678054488318	0.00191097996676088
865	3478.73203287774	68.5453879709964	2.95766347720728	0.0000341148518137853	0.101699417638249	0.00190925875191782
865.25	3479.47132417021	68.5126927709342	2.95666734095798	0.0000341244256924933	0.101720819005255	0.00190754136147422
865.5	3480.21036678768	68.4800425351227	2.95567407551755	0.0000341339992848062	0.101742258485384	0.00190582778225433
865.75	3480.9491614466	68.4474371490304	2.95468367098443	0.0000341435725888193	0.101763735975078	0.00190411800114302
866	3481.68770886098	68.4148764985545	2.95369611750159	0.0000341531456026398	0.101785251371162	0.00190241200508546
866.25	3482.42600974234	68.3823604700193	2.95271140525624	0.0000341627183243862	0.101806804570854	0.00190070978108676
866.5	3483.16406479978	68.3498889501737	2.95172952447965	0.000034172290752189	0.101828395471752	0.0018990113162116
866.75	3483.90187473994	68.3174618261895	2.95075046544685	0.00003418186288419	0.101850023971838	0.00189731659758397
867	3484.63944026706	68.2850789856591	2.94977421847642	0.0000341914347185426	0.101871689969477	0.00189562561238673
867.25	3485.37676208293	68.2527403165934	2.94880077393021	0.0000342010062534114	0.10189339336341	0.00189393834786134
867.5	3486.11384088697	68.2204457074199	2.94783012221316	0.0000342105774869726	0.101915134052756	0.00189225479130751
867.75	3486.85067737619	68.1881950469807	2.94686225377301	0.0000342201484174135	0.101936911937009	0.00189057493008286
868	3487.58727224522	68.1559882245302	2.94589715910006	0.0000342297190429325	0.101958726916033	0.0018888987516026
868.25	3488.32362618631	68.1238251297334	2.94493482872697	0.0000342392893617394	0.101980578890067	0.00188722624333919
868.5	3489.05973988936	68.0917056526637	2.94397525322851	0.0000342488593720547	0.102002467759716	0.00188555739282204
868.75	3489.79561404192	68.0596296838012	2.94301842322132	0.00003425842907211	0.102024393425953	0.00188389218763717
869	3490.53124932919	68.0275971140303	2.94206432936369	0.0000342679984601479	0.102046355790116	0.00188223061542687
869.25	3491.26664643405	67.9956078346381	2.9411129623553	0.0000342775675344218	0.102068354753905	0.00188057266388942
869.5	3492.00180603705	67.9636617373122	2.94016431293705	0.0000342871362931958	0.102090390219382	0.00187891832077874
869.75	3492.73672881642	67.931758714139	2.93921837189079	0.0000342967047347447	0.102112462088968	0.00187726757390413
870	3493.47141544813	67.8998986576016	2.93827513003909	0.0000343062728573539	0.102134570265443	0.00187562041112987
870.25	3494.20586660582	67.868081460578	2.93733457824505	0.0000343158406593195	0.102156714651939	0.00187397682037499
870.5	3494.94008296087	67.836307016339	2.93639670741205	0.000034325408138948	0.102178895151946	0.00187233678961293
870.75	3495.67406518238	67.8045752185465	2.93546150848353	0.0000343349752945563	0.102201111669302	0.00187070030687122
871	3496.40781393722	67.7728859612517	2.93452897244281	0.0000343445421244718	0.102223364108198	0.00186906736023122
871.25	3497.14132988996	67.7412391388929	2.93359909031281	0.0000343541086270322	0.10224565237317	0.00186743793782777
871.5	3497.87461370298	67.709634646294	2.93267185315587	0.0000343636748005851	0.102267976369105	0.0018658120278489
871.75	3498.60766603641	67.6780723786623	2.93174725207355	0.0000343732406434888	0.102290336001229	0.00186418961853559
872	3499.34048754816	67.646552231587	2.93082527820638	0.0000343828061541113	0.102312731175116	0.00186257069818137
872.25	3500.07307889391	67.6150741010374	2.92990592273367	0.0000343923713308308	0.102335161796677	0.00186095525513213
872.5	3500.80544072718	67.5836378833604	2.92898917687328	0.0000344019361720355	0.102357627772164	0.00185934327778576
872.75	3501.53757369928	67.5522434752798	2.92807503188146	0.0000344115006761235	0.102380129008167	0.00185773475459189
873	3502.26947845933	67.5208907738934	2.92716347905257	0.0000344210648415027	0.102402665411611	0.0018561296740516
873.25	3503.00115565429	67.4895796766721	2.92625450971893	0.000034430628666591	0.102425236889755	0.00185452802471711
873.5	3503.73260592896	67.4583100814576	2.92534811525058	0.0000344401921498157	0.10244784335019	0.00185292979519155
873.75	3504.46382992597	67.4270818864609	2.92444428705511	0.0000344497552896142	0.102470484700838	0.0018513349741286
874	3505.19482828582	67.3958949902603	2.92354301657742	0.0000344593180844331	0.10249316084995	0.0018497435502323
874.25	3505.92560164688	67.3647492917999	2.92264429529954	0.0000344688805327288	0.102515871706104	0.00184815551225668
874.5	3506.65615064539	67.3336446903878	2.92174811474044	0.0000344784426329672	0.102538617178204	0.00184657084900557
874.75	3507.38647591546	67.3025810856943	2.92085446645581	0.0000344880043836236	0.102561397175476	0.00184498954933225
875	3508.11657808912	67.2715583777504	2.91996334203785	0.0000344975657831826	0.10258421160747	0.00184341160213923
875.25	3508.84645779629	67.2405764669455	2.91907473311513	0.0000345071268301381	0.102607060384055	0.00184183699637795
875.5	3509.5761156648	67.2096352540268	2.91818863135233	0.0000345166875229936	0.102629943415421	0.00184026572104853
875.75	3510.30555232039	67.1787346400964	2.91730502845008	0.0000345262478602614	0.102652860612073	0.00183869776519948
876	3511.03476838676	67.1478745266105	2.91642391614478	0.0000345358078404631	0.102675811884832	0.00183713311792747
876.25	3511.76376448551	67.1170548153775	2.91554528620838	0.0000345453674621295	0.102698797144834	0.00183557176837702
876.5	3512.49254123623	67.086275408556	2.91466913044819	0.0000345549267238002	0.102721816303527	0.00183401370574026
876.75	3513.22109925642	67.0555362086536	2.91379544070673	0.0000345644856240241	0.102744869272668	0.0018324589192567
877	3513.94943916158	67.0248371185252	2.91292420886148	0.0000345740441613587	0.102767955964326	0.00183090739821292
877.25	3514.67756156518	66.9941780413711	2.91205542682475	0.0000345836023343706	0.102791076290875	0.00182935913194232
877.5	3515.40546707866	66.9635588807358	2.91118908654348	0.0000345931601416352	0.102814230164997	0.00182781410982492
877.75	3516.13315631144	66.932979540506	2.91032517999903	0.0000346027175817366	0.102837417499676	0.00182627232128702
878	3516.86062987098	66.9024399249091	2.90946369920703	0.0000346122746532674	0.102860638208202	0.00182473375580103
878.25	3517.58788836271	66.8719399385118	2.90860463621718	0.0000346218313548293	0.102883892204164	0.00182319840288517
878.5	3518.31493239009	66.8414794862186	2.90774798311308	0.0000346313876850323	0.102907179401451	0.00182166625210322
878.75	3519.04176255461	66.8110584732696	2.90689373201202	0.000034640943642495	0.102930499714251	0.00182013729306431
879	3519.76837945578	66.7806768052398	2.90604187506487	0.0000346504992258446	0.102953853057048	0.00181861151542263
879.25	3520.49478369118	66.7503343880368	2.90519240445581	0.0000346600544337165	0.102977239344622	0.00181708890887723
879.5	3521.2209758564	66.7200311278999	2.90434531240225	0.0000346696092647547	0.103000658492046	0.00181556946317174
879.75	3521.94695654512	66.689766931398	2.90350059115457	0.0000346791637176116	0.103024110414686	0.00181405316809414
880	3522.67272634908	66.6595417054284	2.90265823299601	0.0000346887177909477	0.103047595028198	0.00181254001347653
880.25	3523.39828585807	66.6293553572154	2.90181823024245	0.0000346982714834318	0.103071112248527	0.0018110299891949
880.5	3524.12363566001	66.5992077943082	2.90098057524229	0.000034707824793741	0.103094661991907	0.00180952308516886
880.75	3524.84877634088	66.5690989245803	2.90014526037621	0.0000347173777205603	0.103118244174856	0.00180801929136143
881	3525.57370848475	66.5390286562271	2.89931227805708	0.0000347269302625831	0.10314185871418	0.00180651859777881
881.25	3526.29843267383	66.5089968977651	2.89848162072972	0.0000347364824185105	0.103165505526966	0.00180502099447014
881.5	3527.02294948841	66.4790035580302	2.89765328087078	0.0000347460341870519	0.103189184530583	0.00180352647152727
881.75	3527.74725950693	66.4490485461759	2.89682725098856	0.0000347555855669245	0.103212895642683	0.00180203501908453
882	3528.47136330595	66.4191317716726	2.89600352362283	0.0000347651365568533	0.103236638781193	0.00180054662731851
882.25	3529.19526146016	66.3892531443051	2.89518209134469	0.0000347746871555714	0.103260413864322	0.00179906128644781
882.5	3529.91895454242	66.3594125741724	2.89436294675639	0.0000347842373618193	0.103284220810552	0.00179757898673287
882.75	3530.64244312373	66.3296099716852	2.89354608249116	0.0000347937871743457	0.103308059538641	0.00179609971847567
883	3531.36572777325	66.2998452475651	2.8927314912131	0.0000348033365919068	0.103331929967621	0.00179462347201959
883.25	3532.08880905831	66.2701183128429	2.89191916561693	0.0000348128856132663	0.103355832016795	0.00179315023774911
883.5	3532.81168754442	66.2404290788573	2.89110909842792	0.0000348224342371957	0.103379765605738	0.00179168000608967
883.75	3533.53436379529	66.2107774572535	2.89030128240169	0.000034831982462474	0.103403730654293	0.00179021276750739
884	3534.25683837278	66.1811633599817	2.88949571032403	0.0000348415302878878	0.103427727082572	0.00178874851250889
884.25	3534.97911183701	66.1515866992961	2.8886923750108	0.0000348510777122311	0.103451754810953	0.00178728723164105
884.5	3535.70118474625	66.1220473877528	2.88789126930773	0.0000348606247343052	0.103475813760079	0.00178582891549083
884.75	3536.42305765703	66.0925453382093	2.88709238609029	0.0000348701713529191	0.103499903850857	0.00178437355468502
885	3537.14473112407	66.0630804638222	2.88629571826351	0.0000348797175668888	0.103524025004457	0.00178292113989006
885.25	3537.86620570035	66.0336526780469	2.88550125876187	0.0000348892633750378	0.10354817714231	0.00178147166181181
885.5	3538.58748193705	66.0042618946353	2.8847090005491	0.0000348988087761967	0.103572360186107	0.00178002511119537
885.75	3539.30856038364	65.974908027635	2.88391893661807	0.0000349083537692035	0.103596574057797	0.00177858147882482
886	3540.0294415878	65.9455909913879	2.88313105999062	0.0000349178983529032	0.103620818679587	0.00177714075552309
886.25	3540.75012609549	65.9163107005287	2.88234536371739	0.0000349274425261479	0.103645093973938	0.00177570293215169
886.5	3541.47061445093	65.8870670699837	2.88156184087773	0.0000349369862877968	0.10366939986357	0.00177426799961053
886.75	3542.19090719663	65.8578600149696	2.88078048457951	0.0000349465296367163	0.103693736271451	0.00177283594883774
887	3542.91100487335	65.8286894509919	2.88000128795898	0.0000349560725717796	0.103718103120804	0.00177140677080945
887.25	3543.63090802016	65.799555293844	2.87922424418062	0.0000349656150918668	0.103742500335103	0.00176998045653957
887.5	3544.35061717443	65.7704574596055	2.87844934643701	0.0000349751571958652	0.10376692783807	0.00176855699707964
887.75	3545.07013287181	65.7413958646413	2.87767658794869	0.0000349846988826685	0.103791385553676	0.00176713638351859
888	3545.78945564627	65.7123704256001	2.87690596196401	0.0000349942401511776	0.10381587340614	0.00176571860698257
888.25	3546.50858603009	65.683381059413	2.87613746175896	0.0000350037810003001	0.103840391319924	0.00176430365863477
888.5	3547.22752455389	65.6544276832927	2.87537108063709	0.0000350133214289503	0.103864939219737	0.00176289152967517
888.75	3547.94627174659	65.6255102147319	2.87460681192931	0.0000350228614360491	0.10388951703053	0.00176148221134041
889	3548.66482813548	65.5966285715019	2.8738446489938	0.0000350324010205242	0.103914124677496	0.00176007569490357
889.25	3549.38319424617	65.5677826716519	2.87308458521582	0.0000350419401813099	0.103938762086069	0.00175867197167398
889.5	3550.10137060262	65.5389724335073	2.87232661400763	0.0000350514789173471	0.103963429181921	0.00175727103299706
889.75	3550.81935772716	65.5101977756686	2.87157072880832	0.000035061017227583	0.103988125890966	0.00175587287025407
890	3551.53715614047	65.4814586170105	2.87081692308365	0.0000350705551109716	0.104012852139351	0.00175447747486201
890.25	3552.2547663616	65.4527548766798	2.87006519032599	0.0000350800925664733	0.10403760785346	0.00175308483827336
890.5	3552.97218890798	65.4240864740954	2.86931552405409	0.0000350896295930547	0.104062392959912	0.00175169495197594
890.75	3553.68942429544	65.3954533289463	2.86856791781305	0.0000350991661896891	0.10408720738556	0.00175030780749271
891	3554.40647303817	65.3668553611905	2.8678223651741	0.000035108702355356	0.104112051057489	0.00174892339638161
891.25	3555.12333564877	65.338292491054	2.8670788597345	0.0000351182380890411	0.104136923903013	0.00174754171023535
891.5	3555.84001263825	65.3097646390296	2.86633739511744	0.0000351277733897365	0.104161825849678	0.00174616274068124
891.75	3556.55650451602	65.2812717258757	2.86559796497185	0.0000351373082564405	0.104186756825258	0.00174478647938104
892	3557.2728117899	65.2528136726148	2.86486056297233	0.0000351468426881576	0.104211716757754	0.00174341291803074
892.25	3557.98893496613	65.2243904005332	2.86412518281897	0.0000351563766838984	0.104236705575395	0.00174204204836041
892.5	3558.70487454941	65.1960018311787	2.86339181823726	0.0000351659102426798	0.104261723206632	0.00174067386213404
892.75	3559.42063104284	65.1676478863604	2.86266046297796	0.0000351754433635246	0.104286769580142	0.00173930835114931
893	3560.13620494797	65.1393284881471	2.86193111081693	0.0000351849760454616	0.104311844624825	0.0017379455072375
893.25	3560.8515967648	65.1110435588664	2.86120375555507	0.0000351945082875258	0.104336948269801	0.00173658532226325
893.5	3561.56680699178	65.0827930211032	2.86047839101815	0.000035204040088758	0.104362080444412	0.0017352277881244
893.75	3562.28183612583	65.0545767976992	2.85975501105669	0.0000352135714482051	0.104387241078219	0.00173387289675188
894	3562.99668466232	65.0263948117508	2.85903360954586	0.0000352231023649199	0.104412430101001	0.00173252064010943
894.25	3563.71135309511	64.9982469866092	2.85831418038534	0.0000352326328379608	0.104437647442753	0.00173117101019357
894.5	3564.42584191651	64.9701332458784	2.8575967174992	0.0000352421628663924	0.104462893033688	0.00172982399903331
894.75	3565.14015161735	64.9420535134143	2.85688121483577	0.0000352516924492849	0.104488166804232	0.00172847959869007
895	3565.85428268692	64.914007713324	2.85616766636754	0.0000352612215857142	0.104513468685024	0.00172713780125747
895.25	3566.56823561302	64.8859957699642	2.85545606609103	0.0000352707502747621	0.104538798606918	0.00172579859886117
895.5	3567.28201088195	64.8580176079402	2.85474640802667	0.0000352802785155161	0.104564156500978	0.00172446198365875
895.75	3567.99560897853	64.8300731521053	2.85403868621868	0.0000352898063070691	0.104589542298478	0.00172312794783949
896	3568.70903038606	64.8021623275591	2.85333289473495	0.0000352993336485199	0.104614955930901	0.00172179648362425
896.25	3569.4222755864	64.7742850596469	2.85262902766695	0.0000353088605389728	0.10464039732994	0.00172046758326529
896.5	3570.13534505991	64.7464412739584	2.85192707912957	0.0000353183869775377	0.104665866427491	0.00171914123904612
896.75	3570.84823928549	64.7186308963265	2.85122704326104	0.00003532791296333	0.10469136315566	0.00171781744328136
897	3571.56095874058	64.6908538528268	2.85052891422279	0.0000353374384954706	0.104716887446755	0.00171649618831655
897.25	3572.27350390115	64.663110069776	2.84983268619935	0.0000353469635730858	0.104742439233289	0.001715177466528
897.5	3572.98587524175	64.6353994737313	2.84913835339825	0.0000353564881953074	0.104768018447978	0.00171386127032267
897.75	3573.69807323544	64.6077219914888	2.84844591004988	0.0000353660123612726	0.104793625023737	0.00171254759213799
898	3574.41009835388	64.5800775500832	2.84775535040739	0.000035375536070124	0.104819258893683	0.0017112364244417
898.25	3575.12195106728	64.5524660767862	2.84706666874657	0.0000353850593210094	0.104844919991133	0.0017099277597317
898.5	3575.83363184441	64.5248874991057	2.84637985936576	0.0000353945821130821	0.104870608249602	0.00170862159053593
898.75	3576.54514115264	64.4973417447849	2.84569491658573	0.0000354041044455004	0.1048963236028	0.00170731790941218
899	3577.25647945791	64.4698287418011	2.84501183474955	0.0000354136263174282	0.104922065984635	0.00170601670894797
899.25	3577.96764722476	64.4423484183648	2.84433060822251	0.0000354231477280343	0.104947835329211	0.00170471798176039
899.5	3578.6786449163	64.4149007029186	2.843651231392	0.0000354326686764929	0.104973631570822	0.00170342172049594
899.75	3579.38947299426	64.3874855241365	2.84297369866741	0.0000354421891619832	0.10499945464396	0.00170212791783041
900	3580.10013191897	64.3601028109227	2.84229800447999	0.0000354517091836894	0.105025304483303	0.00170083656646873`` = ! ```

### Stainless-steel conductivity

Columns are T (K) and k (W/m·K). This is the original eight-point input table,
not a replacement material specification.

¢``` KT = ``T	k
300	13.4
400	15.2
500	16.75
600	18.3
700	19.8
800	21.3
900	22.75
1000	24.2`` ```

## Inputs

Input symbols omit underscores from the Excel defined names; e.g. N\_steam
becomes Nsteam. Values marked Input are editable constants; values marked
Derived are live calculations.

*   **WP\_dT**: ¢` WPdT = 0.25 `; **Units**: K; **Type**: Input; **Original note**:
    Embedded water table

*   **WP\_T0**: ¢` WPT0 = 555 `; **Units**: K; **Type**: Input; **Original note**:
    Embedded water table

*   **Reactor thermal power**: ¢` Pth = 1500 `; **Units**: MW; **Type**: Input;
    **Original note**: Wielenga Fast Salt System presentation

*   **Plant electric output**: ¢` Pe = 600 `; **Units**: MW; **Type**: Input;
    **Original note**: Wielenga Fast Salt System presentation

*   **Number of steam generators**: ¢` Ngen = 3 `; **Units**: -; **Type**: Input;
    **Original note**: Sponsor meeting 10/8

*   **Reference Rankine-cycle efficiency**: ¢` etaR = 0.44 `; **Units**: -;
    **Type**: Input; **Original note**: Kim et al. 2025 (team reference)

*   **Salt inlet temperature (top)**: ¢` Tsaltin = 890 `; **Units**: K; **Type**:
    Input; **Original note**: counterSG.xlsx (cell labelled "outlet" in sheet)

*   **Salt outlet temperature (bottom)**: ¢` Tsaltout = 810 `; **Units**: K;
    **Type**: Input; **Original note**: counterSG.xlsx (cell labelled "inlet"
    in sheet)

*   **Water inlet temperature (bottom)**: ¢` Twin = 560 `; **Units**: K; **Type**:
    Input; **Original note**: counterSG.xlsx

*   **Steam outlet temperature (top)**: ¢` Twout = 830 `; **Units**: K; **Type**:
    Input; **Original note**: counterSG.xlsx

*   **Steam pressure**: ¢` Psteam = 24 `; **Units**: MPa; **Type**: Input;
    **Original note**: Properties table is generated at 24 MPa (information only)

*   **Number of march segments**: ¢` Nseg = 540 `; **Units**: -; **Type**: Input;
    **Original note**: Fixed by the number of rows in the march sheets

*   **Steam tubes per steam generator**: ¢` Nsteam = 6536 `; **Units**: -; **Type**:
    Input; **Original note**: counterSG.xlsx value; checked in calc sheet §9

*   **Salt tubes per steam tube**: ¢` saltratio = 0.75 `; **Units**: -; **Type**:
    Input; **Original note**: 3 salt + 1 air-pass contact per steam tube → 3/4
    (calc sheet §7.1)

*   **Tube inner diameter (both tube sets)**: ¢` Di = 0.02 `; **Units**: m;
    **Type**: Input

*   **Tube wall thickness**: ¢` twall = 0.002 `; **Units**: m; **Type**: Input

*   **Density ρ = a + bT : a**: ¢` rhoa = 2112.68 `; **Units**: kg/m³; **Type**: Input

*   **Density : b**: ¢` rhob = -0.5635 `; **Units**: kg/m³·K; **Type**: Input

*   **Specific heat c\_p = a + bT : a**: ¢` cpa = 1437.88 `; **Units**: J/kg·K;
    **Type**: Input

*   **Specific heat : b**: ¢` cpb = -0.5 `; **Units**: J/kg·K²; **Type**: Input

*   **Viscosity μ = a·exp(b/T) : a**: ¢` mua = 0.00070645 `; **Units**: Pa·s;
    **Type**: Input

*   **Viscosity : b**: ¢` mub = 1204.1 `; **Units**: K; **Type**: Input

*   **Conductivity k = a + bT : a**: ¢` ka = 0.65318 `; **Units**: W/m·K; **Type**: Input

*   **Conductivity : b**: ¢` kb = -0.00026 `; **Units**: W/m·K²; **Type**: Input

*   **Salt freezing temperature**: ¢` Tfreeze = 675 `; **Units**: K; **Type**:
    Input; **Original note**: Conservative end of published 656-675 K range

*   **Nu = C·Re^a·Pr^b : C**: ¢` NuC = 0.0266 `; **Units**: -; **Type**: Input;
    **Original note**: Not traceable to a standard reference

*   **Nu correlation : a**: ¢` Nua = 0.805 `; **Units**: -; **Type**: Input

*   **Wall conductivity (fixed)**: ¢` kwallss = 19 `; **Units**: W/m·K; **Type**:
    Input; **Original note**: Spreadsheet value

*   **Tube-to-tube contact conductance h\_c**: ¢` hcontact = 3700 `; **Units**:
    W/m²·K; **Type**: Input; **Original note**: Enter 0 for perfect contact.
    Published SS/SS in air: 2,000-3,700

*   **Multiplier on water h in deterioration zone**: ¢` HTDmult = 1 `; **Units**: -;
    **Type**: Input; **Original note**: 1 = none; e.g. 0.5 for a 50% penalty
    (sensitivity)

*   **Jackson: coefficient**: ¢` JC = 0.0183 `; **Units**: -; **Type**: Input;
    **Original note**: Nu = C Re^a Pr^b (ρw/ρb)^c (c̄p/cp)^n

*   **Jackson: Re exponent**: ¢` JRe = 0.82 `; **Units**: -; **Type**: Input

*   **Jackson: Pr exponent**: ¢` JPr = 0.5 `; **Units**: -; **Type**: Input

*   **Jackson: density-ratio exponent**: ¢` Jrho = 0.3 `; **Units**: -; **Type**: Input

*   **Pseudo-critical temperature at 24 MPa**: ¢` Tpc = 654.38 `; **Units**: K;
    **Type**: Input; **Original note**: Temperature of the c\_p peak

*   **First-segment wall-temperature guess (wall − bulk)**: ¢` wallguess = 96 `;
    **Units**: K; **Type**: Input; **Original note**: Only seeds pass 1 of row 1

*   **Steam-tube fin arc 1 (non-salt contact)**: ¢` gap1 = 60 `; **Units**: deg;
    **Type**: Input; **Original note**: Between salt contacts at a steam neighbour

*   **Steam-tube fin arc 2 (non-salt contact)**: ¢` gap2 = 120 `; **Units**: deg;
    **Type**: Input; **Original note**: Steam neighbour + air-pass tube

*   **Salt-tube fin arc**: ¢` saltgap = 60 `; **Units**: deg; **Type**: Input;
    **Original note**: Side arcs touching in-row neighbours

*   **Wall roughness**: ¢` rough = 0.0000015 `; **Units**: m; **Type**: Input;
    **Original note**: Assumed drawn stainless tubing

*   **Gravity**: ¢` gacc = 9.81 `; **Units**: m/s²; **Type**: Input

*   **Salt minor-loss coefficient (total)**: ¢` Ksalt = 2.1 `; **Units**: -;
    **Type**: Input; **Original note**: Entrance 0.5 + exit 1.0 + two bends 0.3

*   **Water minor loss at inlet**: ¢` Kwin = 0.8 `; **Units**: -; **Type**: Input;
    **Original note**: Entrance 0.5 + bend 0.3

*   **Water minor loss at outlet**: ¢` Kwout = 1.3 `; **Units**: -; **Type**: Input;
    **Original note**: Exit 1.0 + bend 0.3

*   **Table start T**: ¢` K316T0 = 300 `; **Units**: K; **Type**: Input

*   **Table step**: ¢` K316dT = 100 `; **Units**: K; **Type**: Input

*   **Plant efficiency**: ¢?` etaplant = (Pe / Pth) = 〔0.4〕 `; **Units**: -;
    **Type**: Derived; **Original note**: η = 600/1500

*   **Heat duty per steam generator, Q**: ¢?` QSG = (Pth / Ngen) = 〔500〕 `;
    **Units**: MW; **Type**: Derived; **Original note**: 1500/3

*   **Electric share per steam generator**: ¢?` WeSG = (etaplant * QSG) = 〔200〕 `;
    **Units**: MWe; **Type**: Derived; **Original note**: η·Q

*   **Cold-end ΔT (salt out − water in)**: ¢?` dTcold = (Tsaltout - Twin) = 〔250〕 `;
    **Units**: K; **Type**: Derived

*   **Hot-end ΔT (salt in − steam out)**: ¢?` dThot = (Tsaltin - Twout) = 〔60〕 `;
    **Units**: K; **Type**: Derived

*   **Water temperature step per segment**: ¢?` dTstep = ((Twout - Twin) / Nseg) =
    〔0.5〕 `; **Units**: K; **Type**: Derived

*   **Water enthalpy at inlet**: ¢?` hwin = (WP[(floor(((Twin - WPT0) / WPdT)) +
    1),2] + ((((Twin - WPT0) / WPdT) - floor(((Twin - WPT0) / WPdT))) *
    (WP[(floor(((Twin - WPT0) / WPdT)) + 2),2] - WP[(floor(((Twin - WPT0) /
    WPdT)) + 1),2]))) = 〔1,264.67695015652〕 `; **Units**: kJ/kg; **Type**:
    Derived; **Original note**: From Water\_Properties

*   **Steam enthalpy at outlet**: ¢?` hwout = (WP[(floor(((Twout - WPT0) / WPdT)) +
    1),2] + ((((Twout - WPT0) / WPdT) - floor(((Twout - WPT0) / WPdT))) *
    (WP[(floor(((Twout - WPT0) / WPdT)) + 2),2] - WP[(floor(((Twout - WPT0) /
    WPdT)) + 1),2]))) = 〔3,372.39468555589〕 `; **Units**: kJ/kg; **Type**:
    Derived; **Original note**: From Water\_Properties

*   **Water/steam mass flow**: ¢?` mw = ((QSG * 1000) / (hwout - hwin)) =
    〔237.223415451908〕 `; **Units**: kg/s; **Type**: Derived; **Original
    note**: Q = ṁ_w (h_out − h\_in)

*   **Salt Δh = ∫c\_p dT from outlet to inlet**: ¢?` dhsalt = ((cpa * (Tsaltin -
    Tsaltout)) + ((cpb / 2) * ((Tsaltin ^ 2) - (Tsaltout ^ 2)))) = 〔81,030.4〕
    `; **Units**: J/kg; **Type**: Derived; **Original note**: c\_p linear in T
    → exact integral

*   **Salt mass flow**: ¢?` ms = ((QSG * 1000000) / dhsalt) = 〔6,170.52365531949〕 `;
    **Units**: kg/s; **Type**: Derived; **Original note**: Q = ṁ_s ∫c_p dT

*   **Salt capacity rate C\_salt**: ¢?` Csalt = (QSG / (Tsaltin - Tsaltout)) =
    〔6.25〕 `; **Units**: MW/K; **Type**: Derived; **Original note**: Q/ΔT\_salt

*   **Water average capacity rate C\_water**: ¢?` Cwavg = (QSG / (Twout - Twin)) =
    〔1.85185185185185〕 `; **Units**: MW/K; **Type**: Derived; **Original
    note**: Q/ΔT\_water (average only)

*   **Cycle work per kg steam**: ¢?` wnet = (etaR * (hwout - hwin)) =
    〔927.395803575723〕 `; **Units**: kJ/kg; **Type**: Derived; **Original
    note**: η\_R (h1 − h4)

*   **Salt tubes**: ¢?` Nsalt = round((Nsteam * saltratio), "f0") = 〔4,902〕 `;
    **Units**: -; **Type**: Derived

*   **Air-pass tubes**: ¢?` Nair = (Nsteam - Nsalt) = 〔1,634〕 `; **Units**: -;
    **Type**: Derived; **Original note**: Occupy the remaining salt-row positions

*   **Tube outer diameter**: ¢?` Do = (Di + (2 * twall)) = 〔0.024〕 `; **Units**: m;
    **Type**: Derived

*   **Flow area per tube**: ¢?` Aflow = ((π * (Di ^ 2)) / 4) =
    〔0.000314159265358979〕 `; **Units**: m²; **Type**: Derived

*   **Salt-contact width per steam tube**: ¢?` wcontact = ((0.5 * π) * Do) =
    〔0.0376991118430775〕 `; **Units**: m; **Type**: Derived; **Original note**:
    3 contacts × 60° = half of OD circumference

*   **Inner radius**: ¢?` ri = (Di / 2) = 〔0.01〕 `; **Units**: m; **Type**: Derived

*   **Mid-wall radius**: ¢?` rm = ((Di + twall) / 2) = 〔0.011〕 `; **Units**: m;
    **Type**: Derived

*   **Water flow per steam tube**: ¢?` mwtube = (mw / Nsteam) = 〔0.0362948922050043〕
    `; **Units**: kg/s; **Type**: Derived

*   **Salt flow per salt tube**: ¢?` mstube = (ms / Nsalt) = 〔1.25877675547113〕 `;
    **Units**: kg/s; **Type**: Derived

*   **Steam-side mass flux G**: ¢?` Gw = (mwtube / Aflow) = 〔115.530230068279〕 `;
    **Units**: kg/m²·s; **Type**: Derived

*   **Nu correlation : b**: ¢?` Nub = (1 / 3) = 〔0.333333333333333〕 `; **Units**: -;
    **Type**: Derived

*   **Fraction of salt-tube bore backed by contacts**: ¢?` saltbacked = (2 / 3) =
    〔0.666666666666667〕 `; **Units**: -; **Type**: Derived; **Original note**:
    4 × 60° of 360°

¢` iv = [WPdT; WPT0; Pth; Pe; Ngen; etaplant; QSG; WeSG; etaR; Tsaltin;
Tsaltout; Twin; Twout; Psteam; dTcold; dThot; Nseg; dTstep; hwin; hwout; mw;
dhsalt; ms; Csalt; Cwavg; wnet; Nsteam; saltratio; Nsalt; Nair; Di; twall; Do;
Aflow; wcontact; ri; rm; mwtube; mstube; Gw; rhoa; rhob; cpa; cpb; mua; mub;
ka; kb; Tfreeze; NuC; Nua; Nub; kwallss; hcontact; HTDmult; JC; JRe; JPr; Jrho;
Tpc; wallguess; gap1; gap2; saltgap; saltbacked; rough; gacc; Ksalt; Kwin;
Kwout; K316T0; K316dT] = ! `

## Live segment calculations

The following calls calculate all 540 segments in workbook order. Large matrices
are intentionally not rendered in full; the segment inspector and column maps
below let you inspect any result without filling the document with more than
70,000 displayed numbers.

¢` TM = sgMarch(iv, WP, KT, 0) = ! `

¢` TP = dataframe(TM[,1], TM[,2], TM[,3], TM[,4], TM[,5], TM[,6], TM[,7],
TM[,8], TM[,9], TM[,10], TM[,11], TM[,12], TM[,13], TM[,14], TM[,15], TM[,16],
TM[,17], TM[,18], TM[,19], TM[,20], TM[,21], TM[,22], TM[,23], TM[,24],
TM[,25], TM[,26], TM[,27], TM[,28], TM[,29], TM[,30]) = ! `

¢` SS = sgSponsor(iv, WP, KT, TP) = ! `

¢` SP = dataframe(SS[,1], SS[,2], SS[,3], SS[,4], SS[,5], SS[,6], SS[,7],
SS[,8], SS[,9], SS[,10], SS[,11], SS[,12], SS[,13], SS[,14], SS[,15], SS[,16],
SS[,17], SS[,18], SS[,19], SS[,20], SS[,21], SS[,22], SS[,23], SS[,24],
SS[,25], SS[,26], SS[,27], SS[,28], SS[,29], SS[,30], SS[,31], SS[,32]) = ! `

¢` BE = sgBest(iv, WP, KT, TP) = ! `

¢` BP = dataframe(BE[,1], BE[,2], BE[,3], BE[,4], BE[,5], BE[,6], BE[,7],
BE[,8], BE[,9], BE[,10], BE[,11], BE[,12], BE[,13], BE[,14], BE[,15], BE[,16],
BE[,17], BE[,18], BE[,19], BE[,20], BE[,21], BE[,22], BE[,23], BE[,24],
BE[,25], BE[,26], BE[,27], BE[,28], BE[,29], BE[,30], BE[,31], BE[,32],
BE[,33], BE[,34], BE[,35], BE[,36], BE[,37], BE[,38], BE[,39], BE[,40],
BE[,41], BE[,42], BE[,43], BE[,44], BE[,45], BE[,46], BE[,47], BE[,48],
BE[,49], BE[,50], BE[,51], BE[,52], BE[,53], BE[,54], BE[,55], BE[,56],
BE[,57], BE[,58], BE[,59], BE[,60], BE[,61], BE[,62], BE[,63], BE[,64],
BE[,65], BE[,66]) = ! `

## Results

Side-by-side results retain the original workbook formulas. The Results row
identifier is included to make comparisons straightforward, and the units
column applies to both models.

*   **Thermodynamics (same for any tube design)**

*   **6: Heat duty Q**; **Sponsor-physics model**: ¢?` rC6 = QSG = 〔500〕 `; **Best
    estimate**: ¢?` rD6 = QSG = 〔500〕 `; **Units**: MW; **Calculation note**: Inputs

*   **7: Water / steam mass flow**; **Sponsor-physics model**: ¢?` rC7 = mw =
    〔237.223415451908〕 `; **Best estimate**: ¢?` rD7 = mw = 〔237.223415451908〕
    `; **Units**: kg/s; **Calculation note**: Inputs

*   **8: Salt mass flow**; **Sponsor-physics model**: ¢?` rC8 = ms =
    〔6,170.52365531949〕 `; **Best estimate**: ¢?` rD8 = ms =
    〔6,170.52365531949〕 `; **Units**: kg/s; **Calculation note**: Inputs

*   **9: Required UA (sum over segments)**; **Sponsor-physics model**: ¢?` rC9 =
    sum(TM[,16]) = 〔3.03378704475921〕 `; **Best estimate**: ¢?` rD9 =
    sum(TM[,16]) = 〔3.03378704475921〕 `; **Units**: MW/K; **Calculation note**:
    Σ Q_i/LMTD_i (Temperature\_March)

*   **10: Single LMTD (reference only)**; **Sponsor-physics model**: ¢?` rC10 =
    ((dTcold - dThot) / ln((dTcold / dThot))) = 〔133.135605410936〕 `; **Best
    estimate**: ¢?` rD10 = ((dTcold - dThot) / ln((dTcold / dThot))) =
    〔133.135605410936〕 `; **Units**: K; **Calculation note**: (ΔT_cold −
    ΔT_hot)/ln(ΔT_cold/ΔT_hot)

*   **11: True mean ΔT (use for sizing)**; **Sponsor-physics model**: ¢?` rC11 =
    (QSG / rC9) = 〔164.810513270448〕 `; **Best estimate**: ¢?` rD11 = (QSG /
    rD9) = 〔164.810513270448〕 `; **Units**: K; **Calculation note**: Q / UA

*   **12: UA a single LMTD would require**; **Sponsor-physics model**: ¢?` rC12 =
    (QSG / rC10) = 〔3.75556935694775〕 `; **Best estimate**: ¢?` rD12 = (QSG /
    rD10) = 〔3.75556935694775〕 `; **Units**: MW/K; **Calculation note**: Q /
    single LMTD

*   **13: Single-LMTD sizing error**; **Sponsor-physics model**: ¢?` rC13 = ((rC12 /
    rC9) - 1) = 〔0.237914626682648〕 `; **Best estimate**: ¢?` rD13 = ((rD12 /
    rD9) - 1) = 〔0.237914626682648〕 `; **Units**: -; **Calculation note**:
    Oversize (+) vs exact

*   **14: Capacity ratio C\_r (average)**; **Sponsor-physics model**: ¢?` rC14 =
    (Cwavg / Csalt) = 〔0.296296296296296〕 `; **Best estimate**: ¢?` rD14 =
    (Cwavg / Csalt) = 〔0.296296296296296〕 `; **Units**: -; **Calculation
    note**: C_water,avg / C_salt

*   **15: Effectiveness ε (exact, enthalpy basis)**; **Sponsor-physics model**: ¢?`
    rC15 = (QSG / ((mw * ((WP[(floor(((Tsaltin - WPT0) / WPdT)) + 1),2] +
    ((((Tsaltin - WPT0) / WPdT) - floor(((Tsaltin - WPT0) / WPdT))) *
    (WP[(floor(((Tsaltin - WPT0) / WPdT)) + 2),2] - WP[(floor(((Tsaltin - WPT0)
    / WPdT)) + 1),2]))) - hwin)) / 1000)) = 〔0.921664441877197〕 `; **Best
    estimate**: ¢?` rD15 = (QSG / ((mw * ((WP[(floor(((Tsaltin - WPT0) /
    WPdT)) + 1),2] + ((((Tsaltin - WPT0) / WPdT) - floor(((Tsaltin - WPT0) /
    WPdT))) * (WP[(floor(((Tsaltin - WPT0) / WPdT)) + 2),2] -
    WP[(floor(((Tsaltin - WPT0) / WPdT)) + 1),2]))) - hwin)) / 1000)) =
    〔0.921664441877197〕 `; **Units**: -; **Calculation note**: Q / \[ṁ_w
    (h_w(T_salt,in) − h_w,in)]

*   **16: Effectiveness ε (constant-c\_p form)**; **Sponsor-physics model**: ¢?`
    rC16 = (QSG / (Cwavg * (Tsaltin - Twin))) = 〔0.818181818181818〕 `; **Best
    estimate**: ¢?` rD16 = (QSG / (Cwavg * (Tsaltin - Twin))) =
    〔0.818181818181818〕 `; **Units**: -; **Calculation note**: Q / \[C_min
    (T_salt,in − T\_w,in)]

*   **17: NTU**; **Sponsor-physics model**: ¢?` rC17 = (rC9 / Cwavg) =
    〔1.63824500416997〕 `; **Best estimate**: ¢?` rD17 = (rD9 / Cwavg) =
    〔1.63824500416997〕 `; **Units**: -; **Calculation note**: UA / C\_min

*   **18: ε predicted by counterflow ε-NTU formula**; **Sponsor-physics model**: ¢?`
    rC18 = ((1 - exp(((-rC17) * (1 - rC14)))) / (1 - (rC14 * exp(((-rC17) *
    (1 - rC14)))))) = 〔0.754881863351735〕 `; **Best estimate**: ¢?` rD18 =
    ((1 - exp(((-rD17) * (1 - rD14)))) / (1 - (rD14 * exp(((-rD17) * (1 -
    rD14)))))) = 〔0.754881863351735〕 `; **Units**: -; **Calculation note**:
    Does not match ε above → formula invalid here

*   **19: NTU the formula says is needed**; **Sponsor-physics model**: ¢?` rC19 =
    (ln(((rC16 - 1) / ((rC16 * rC14) - 1))) / (rC14 - 1)) = 〔2.02800745275179〕
    `; **Best estimate**: ¢?` rD19 = (ln(((rD16 - 1) / ((rD16 * rD14) - 1))) /
    (rD14 - 1)) = 〔2.02800745275179〕 `; **Units**: -; **Calculation note**:
    Inverse counterflow formula

*   **20: Segments where water is the larger stream**; **Sponsor-physics model**:
    ¢?` rC20 = sum(TM[,20]) = 〔18〕 `; **Best estimate**: ¢?` rD20 =
    sum(TM[,20]) = 〔18〕 `; **Units**: segments; **Calculation note**: C\_min
    swaps identity there

*   **Size**

*   **22: Heated tube length L**; **Sponsor-physics model**: ¢?` rC22 = sum(SS[,21])
    = 〔11.8521532043218〕 `; **Best estimate**: ¢?` rD22 = sum(BE[,51]) =
    〔15.3599133218892〕 `; **Units**: m; **Calculation note**: Σ ΔL

*   **23: Overall U, contact-area basis**; **Sponsor-physics model**: ¢?` rC23 =
    ((rC9 * 1000000) / ((Nsteam * wcontact) * rC22)) = 〔1,038.83045574023〕 `;
    **Best estimate**: ¢?` rD23 = ((rD9 * 1000000) / ((Nsteam * wcontact) *
    rD22)) = 〔801.59161427053〕 `; **Units**: W/m²·K; **Calculation note**: UA /
    (N w L)

*   **24: Overall U, steam-bore basis**; **Sponsor-physics model**: ¢?` rC24 =
    ((rC9 * 1000000) / (((Nsteam * π) * Di) * rC22)) = 〔623.298273444138〕 `;
    **Best estimate**: ¢?` rD24 = ((rD9 * 1000000) / (((Nsteam * π) * Di) *
    rD22)) = 〔480.954968562318〕 `; **Units**: W/m²·K; **Calculation note**: UA
    / (N π D L)

*   **25: Contact heat-transfer area**; **Sponsor-physics model**: ¢?` rC25 =
    ((Nsteam * wcontact) * rC22) = 〔2,920.38708337392〕 `; **Best estimate**:
    ¢?` rD25 = ((Nsteam * wcontact) * rD22) = 〔3,784.7040696902〕 `; **Units**:
    m²; **Calculation note**: N w L

*   **26: Steam-bore area**; **Sponsor-physics model**: ¢?` rC26 = (((Nsteam * π) *
    Di) * rC22) = 〔4,867.3118056232〕 `; **Best estimate**: ¢?` rD26 =
    (((Nsteam * π) * Di) * rD22) = 〔6,307.84011615033〕 `; **Units**: m²;
    **Calculation note**: N π D L

*   **27: Total tube length (steam + salt tubes)**; **Sponsor-physics model**: ¢?`
    rC27 = (((Nsteam + Nsalt) * rC22) / 1000) = 〔135.564928351032〕 `; **Best
    estimate**: ¢?` rD27 = (((Nsteam + Nsalt) * rD22) / 1000) =
    〔175.686688575769〕 `; **Units**: km

*   **Pressure drop**

*   **29: Mean salt velocity**; **Sponsor-physics model**: ¢?` rC29 = (sum(SS[,11])
    / Nseg) = 〔2.45847140664602〕 `; **Best estimate**: ¢?` rD29 = (sum(BE[,6])
    / Nseg) = 〔2.45847140664602〕 `; **Units**: m/s

*   **30: Salt friction ΔP**; **Sponsor-physics model**: ¢?` rC30 = (sum(SS[,32])
    / 1000) = 〔71.7025066487057〕 `; **Best estimate**: ¢?` rD30 = (sum(BE[,66])
    / 1000) = 〔92.9247519083103〕 `; **Units**: kPa; **Calculation note**: Σ segments

*   **31: Salt minor losses**; **Sponsor-physics model**: ¢?` rC31 = ((((Ksalt *
    0.5) * (rhoa + ((rhob * (Tsaltin + Tsaltout)) / 2))) * (rC29 ^ 2)) / 1000)
    = 〔10.3679587451295〕 `; **Best estimate**: ¢?` rD31 = ((((Ksalt * 0.5) *
    (rhoa + ((rhob * (Tsaltin + Tsaltout)) / 2))) * (rD29 ^ 2)) / 1000) =
    〔10.3679587451295〕 `; **Units**: kPa; **Calculation note**: K ρ v²/2

*   **32: Salt total ΔP**; **Sponsor-physics model**: ¢?` rC32 = (rC30 + rC31) =
    〔82.0704653938352〕 `; **Best estimate**: ¢?` rD32 = (rD30 + rD31) =
    〔103.29271065344〕 `; **Units**: kPa

*   **33: Salt hydraulic pump power**; **Sponsor-physics model**: ¢?` rC33 =
    ((rC32 * ms) / (rhoa + ((rhob * (Tsaltin + Tsaltout)) / 2))) =
    〔309.981145993762〕 `; **Best estimate**: ¢?` rD33 = ((rD32 * ms) / (rhoa +
    ((rhob * (Tsaltin + Tsaltout)) / 2))) = 〔390.137824459815〕 `; **Units**:
    kW; **Calculation note**: ΔP ṁ/ρ

*   **34: Water friction ΔP**; **Sponsor-physics model**: ¢?` rC34 = (sum(SS[,29])
    / 1000) = 〔0.618809855147751〕 `; **Best estimate**: ¢?` rD34 =
    (sum(BE[,63]) / 1000) = 〔0.751721154709387〕 `; **Units**: kPa

*   **35: Water gravity ΔP**; **Sponsor-physics model**: ¢?` rC35 = (sum(SS[,30])
    / 1000) = 〔27.732016110958〕 `; **Best estimate**: ¢?` rD35 = (sum(BE[,64])
    / 1000) = 〔38.1850689975919〕 `; **Units**: kPa

*   **36: Water acceleration ΔP**; **Sponsor-physics model**: ¢?` rC36 = (((Gw
    ^ 2) * ((((1 / WP[(floor(((Twout - WPT0) / WPdT)) + 1),3]) + ((((Twout -
    WPT0) / WPdT) - floor(((Twout - WPT0) / WPdT))) * (WP[(floor(((Twout -
    WPT0) / WPdT)) + 2),3] - WP[(floor(((Twout - WPT0) / WPdT)) + 1),3]))) - (1
    / WP[(floor(((Twin - WPT0) / WPdT)) + 1),3])) + ((((Twin - WPT0) / WPdT) -
    floor(((Twin - WPT0) / WPdT))) * (WP[(floor(((Twin - WPT0) / WPdT)) +
    2),3] - WP[(floor(((Twin - WPT0) / WPdT)) + 1),3])))) / 1000) =
    〔0.163819838076549〕 `; **Best estimate**: ¢?` rD36 = (((Gw ^ 2) * ((((1 /
    WP[(floor(((Twout - WPT0) / WPdT)) + 1),3]) + ((((Twout - WPT0) / WPdT) -
    floor(((Twout - WPT0) / WPdT))) * (WP[(floor(((Twout - WPT0) / WPdT)) +
    2),3] - WP[(floor(((Twout - WPT0) / WPdT)) + 1),3]))) - (1 /
    WP[(floor(((Twin - WPT0) / WPdT)) + 1),3])) + ((((Twin - WPT0) / WPdT) -
    floor(((Twin - WPT0) / WPdT))) * (WP[(floor(((Twin - WPT0) / WPdT)) +
    2),3] - WP[(floor(((Twin - WPT0) / WPdT)) + 1),3])))) / 1000) =
    〔0.163819838076549〕 `; **Units**: kPa; **Calculation note**: G²(1/ρ_out −
    1/ρ_in)

*   **37: Water minor losses**; **Sponsor-physics model**: ¢?` rC37 = (((((((Kwin *
    0.5) * (Gw ^ 2)) / WP[(floor(((Twin - WPT0) / WPdT)) + 1),3]) + ((((Twin -
    WPT0) / WPdT) - floor(((Twin - WPT0) / WPdT))) * (WP[(floor(((Twin - WPT0)
    / WPdT)) + 2),3] - WP[(floor(((Twin - WPT0) / WPdT)) + 1),3]))) +
    (((Kwout * 0.5) * (Gw ^ 2)) / WP[(floor(((Twout - WPT0) / WPdT)) +
    1),3])) + ((((Twout - WPT0) / WPdT) - floor(((Twout - WPT0) / WPdT))) *
    (WP[(floor(((Twout - WPT0) / WPdT)) + 2),3] - WP[(floor(((Twout - WPT0) /
    WPdT)) + 1),3]))) / 1000) = 〔0.124814387613819〕 `; **Best estimate**: ¢?`
    rD37 = (((((((Kwin * 0.5) * (Gw ^ 2)) / WP[(floor(((Twin - WPT0) / WPdT)) +
    1),3]) + ((((Twin - WPT0) / WPdT) - floor(((Twin - WPT0) / WPdT))) *
    (WP[(floor(((Twin - WPT0) / WPdT)) + 2),3] - WP[(floor(((Twin - WPT0) /
    WPdT)) + 1),3]))) + (((Kwout * 0.5) * (Gw ^ 2)) / WP[(floor(((Twout - WPT0)
    / WPdT)) + 1),3])) + ((((Twout - WPT0) / WPdT) - floor(((Twout - WPT0) /
    WPdT))) * (WP[(floor(((Twout - WPT0) / WPdT)) + 2),3] - WP[(floor(((Twout -
    WPT0) / WPdT)) + 1),3]))) / 1000) = 〔0.124814387613819〕 `; **Units**: kPa

*   **38: Water total ΔP**; **Sponsor-physics model**: ¢?` rC38 = (((rC34 + rC35) +
    rC36) + rC37) = 〔28.6394601917961〕 `; **Best estimate**: ¢?` rD38 =
    (((rD34 + rD35) + rD36) + rD37) = 〔39.2254243779916〕 `; **Units**: kPa

*   **Checks**

*   **40: Maximum steam-side wall temperature**; **Sponsor-physics model**: ¢?` rC40
    = max(SS[,24]) = 〔870.33931841553〕 `; **Best estimate**: ¢?` rD40 =
    max(BE[,54]) = 〔863.414740025536〕 `; **Units**: K

*   **41: Minimum salt-side wall temperature**; **Sponsor-physics model**: ¢?` rC41
    = min(SS[,25]) = 〔738.33093872589〕 `; **Best estimate**: ¢?` rD41 =
    min(BE[,55]) = 〔759.399962934506〕 `; **Units**: K

*   **42: Margin above salt freezing**; **Sponsor-physics model**: ¢?` rC42 =
    (rC41 - Tfreeze) = 〔63.33093872589〕 `; **Best estimate**: ¢?` rD42 =
    (rD41 - Tfreeze) = 〔84.399962934506〕 `; **Units**: K; **Calculation note**:
    vs 675 K

*   **43: Steam mass flux G**; **Sponsor-physics model**: ¢?` rC43 = Gw =
    〔115.530230068279〕 `; **Best estimate**: ¢?` rD43 = Gw = 〔115.530230068279〕
    `; **Units**: kg/m²·s

*   **44: Top of deterioration-prone zone**; **Sponsor-physics model**: N/A; **Best
    estimate**: ¢?` rD44 = flagged(BE[,52],BE[,58],1, 1) = 〔4.57329584344266〕
    `; **Units**: m; **Calculation note**: Highest segment with T_b \< T_pc \<
    T\_wall

*   **45: q″/G in that zone (max)**; **Sponsor-physics model**: N/A; **Best
    estimate**: ¢?` rD45 = flagged(BE[,57],BE[,58],1, 1) = 〔1.14472944772794〕
    `; **Units**: kJ/kg; **Calculation note**: Concern above 0.4

*   **46: q″/G in that zone (min)**; **Sponsor-physics model**: N/A; **Best
    estimate**: ¢?` rD46 = flagged(BE[,57],BE[,58],1, 0) = 〔0.89592807920064〕
    `; **Units**: kJ/kg

*   **47: Bore heat flux in that zone (max)**; **Sponsor-physics model**: N/A;
    **Best estimate**: ¢?` rD47 = flagged(BE[,56],BE[,58],1, 1) =
    〔132.250856461943〕 `; **Units**: kW/m²; **Calculation note**: Compare with
    Yamagata limit below

*   **48: Yamagata limiting heat flux 0.2 G\^1.2**; **Sponsor-physics model**: N/A;
    **Best estimate**: ¢?` rD48 = (0.2 * (Gw ^ 1.2)) = 〔59.7399371695961〕 `;
    **Units**: kW/m²; **Calculation note**: Deterioration expected above this

*   **49: Buoyancy parameter Bo\* in zone (max)**; **Sponsor-physics model**: N/A;
    **Best estimate**: ¢?` rD49 = flagged(BE[,59],BE[,58],1, 1) =
    〔0.0000567868149720135〕 `; **Units**: -; **Calculation note**: > 8×10⁻⁶ =
    buoyancy-dominated

*   **50: Acceleration parameter K\_v (max)**; **Sponsor-physics model**: N/A;
    **Best estimate**: ¢?` rD50 = max(BE[,60]) = 〔1.31671860583887e-7〕 `;
    **Units**: -; **Calculation note**: > 3×10⁻⁶ = laminarization

*   **51: Steam-tube hoop stress P D/(2t)**; **Sponsor-physics model**: ¢?` rC51 =
    ((Psteam * Di) / (2 * twall)) = 〔120〕 `; **Best estimate**: ¢?` rD51 =
    ((Psteam * Di) / (2 * twall)) = 〔120〕 `; **Units**: MPa; **Calculation
    note**: Thin-wall estimate

## Charts

All three native drawings use live march results. The height coordinate uses
segment ends, just as in the source chart-helper data; wall temperatures are
segment representative values, so they are not measurements taken at precisely
those axial points.

¢` function makeCharts(TM, SS, BE, Nseg)
    for i in 1:Nseg
        row = [BE[i,52], TM[i,11], TM[i,3], BE[i,54], TM[i,9], TM[i,14], TM[i,17], TM[i,4], (SS[i,10] / 1000), (BE[i,37] / 1000)]
        if i == 1
            mat = row
        else
            mat = vcat(mat, row)
        end
    end
    return mat
end `

¢` CH = makeCharts(TP, SP, BP, Nseg) = ! `

¢` format = "h8" `

### Temperature profile

Horizontal axis: temperature (K). Vertical axis: heated length from the water
inlet (m). Blue = water; orange = salt; red = inner steam-tube wall; green
dashed = salt freezing temperature; purple dashed = pseudo-critical temperature.

![Temperature profile][2]

### Actual driving temperature difference versus straight-line assumption

Horizontal axis: cumulative duty fraction. Vertical axis: driving temperature
difference (K). Blue = actual segment-end difference; red = the straight line
used by the single-LMTD assumption.

![Actual driving temperature difference versus straight-line assumption][3]

### Water-side convection coefficient

Horizontal axis: bulk water temperature (K). Vertical axis: h (kW/m²·K). Blue =
sponsor correlation; red = Jackson best estimate including the workbook's
wall-property corrections and selected HTD multiplier.

![Water-side convection coefficient][4]

### Original chart reference-line values

These six helper cells preserve the source workbook's freezing and
pseudo-critical reference-line endpoints. The native drawing uses the same
temperatures and length.

*   **C6**; **Hurmet calculation**: ¢?` chC6 = Tfreeze = 〔675〕 `

*   **C7**; **Hurmet calculation**: ¢?` chC7 = Tfreeze = 〔675〕 `

*   **D7**; **Hurmet calculation**: ¢?` chD7 = rD22 = 〔15.359913〕 `

*   **C8**; **Hurmet calculation**: ¢?` chC8 = Tpc = 〔654.38〕 `

*   **C9**; **Hurmet calculation**: ¢?` chC9 = Tpc = 〔654.38〕 `

*   **D9**; **Hurmet calculation**: ¢?` chD9 = rD22 = 〔15.359913〕 `

## Segment inspector and column maps

Change segment to any integer from 1 to 540. Each displayed result is the
corresponding live matrix element; the matrix itself contains every segment,
not just the selected row.

¢` segment = 189 `

### Temperature\_March

*   **A / 1**; **Quantity (original units)**: Segment number; **Purpose / formula
    description**: 1 … 540; **Selected segment**: ¢?` TM[segment, 1] = 〔189〕 `

*   **B / 2**; **Quantity (original units)**: Water temperature at segment start
    (K); **Purpose / formula description**: Row 1 = water inlet; then =
    previous end; **Selected segment**: ¢?` TM[segment, 2] = 〔654〕 `

*   **C / 3**; **Quantity (original units)**: Water temperature at segment end (K);
    **Purpose / formula description**: Start + step; **Selected segment**: ¢?`
    TM[segment, 3] = 〔654.5〕 `

*   **D / 4**; **Quantity (original units)**: Water mean temperature in segment (K);
    **Purpose / formula description**: (start + end)/2; **Selected segment**:
    ¢?` TM[segment, 4] = 〔654.25〕 `

*   **E / 5**; **Quantity (original units)**: Water enthalpy at segment start
    (kJ/kg); **Purpose / formula description**: Water\_Properties lookup;
    **Selected segment**: ¢?` TM[segment, 5] = 〔2,093.4592〕 `

*   **F / 6**; **Quantity (original units)**: Water enthalpy at segment end (kJ/kg);
    **Purpose / formula description**: Water\_Properties lookup; **Selected
    segment**: ¢?` TM[segment, 6] = 〔2,152.7062〕 `

*   **G / 7**; **Quantity (original units)**: Heat transferred in segment, whole SG
    (MW); **Purpose / formula description**: ṁ_w (h_end − h\_start); **Selected
    segment**: ¢?` TM[segment, 7] = 〔14.054783〕 `

*   **H / 8**; **Quantity (original units)**: Cumulative heat at segment end (MW);
    **Purpose / formula description**: Running sum of segment heat; **Selected
    segment**: ¢?` TM[segment, 8] = 〔210.66134〕 `

*   **I / 9**; **Quantity (original units)**: Fraction of total duty at segment end
    (-); **Purpose / formula description**: Cumulative / Q; **Selected
    segment**: ¢?` TM[segment, 9] = 〔0.42132268〕 `

*   **J / 10**; **Quantity (original units)**: Salt temperature at segment start
    (K); **Purpose / formula description**: Solve ∫c_p dT = Q_cum/ṁ\_s from
    salt outlet (quadratic); **Selected segment**: ¢?` TM[segment, 10] =
    〔841.08177〕 `

*   **K / 11**; **Quantity (original units)**: Salt temperature at segment end (K);
    **Purpose / formula description**: Same, with cumulative heat at segment
    end; **Selected segment**: ¢?` TM[segment, 11] = 〔843.32191〕 `

*   **L / 12**; **Quantity (original units)**: Salt mean temperature in segment (K);
    **Purpose / formula description**: (start + end)/2; **Selected segment**:
    ¢?` TM[segment, 12] = 〔842.20184〕 `

*   **M / 13**; **Quantity (original units)**: Salt − water ΔT at segment start (K);
    **Purpose / formula description**: T_salt,start − T_water,start; **Selected
    segment**: ¢?` TM[segment, 13] = 〔187.08177〕 `

*   **N / 14**; **Quantity (original units)**: Salt − water ΔT at segment end (K);
    **Purpose / formula description**: T_salt,end − T_water,end; **Selected
    segment**: ¢?` TM[segment, 14] = 〔188.82191〕 `

*   **O / 15**; **Quantity (original units)**: Segment log-mean temperature
    difference (K); **Purpose / formula description**: (ΔT1 − ΔT2)/ln(ΔT1/ΔT2);
    **Selected segment**: ¢?` TM[segment, 15] = 〔187.95049〕 `

*   **P / 16**; **Quantity (original units)**: UA required for segment (MW/K);
    **Purpose / formula description**: Segment heat / segment LMTD; **Selected
    segment**: ¢?` TM[segment, 16] = 〔0.074779177〕 `

*   **Q / 17**; **Quantity (original units)**: ΔT a single LMTD assumes at segment
    end (K); **Purpose / formula description**: Straight line: ΔT_cold +
    (ΔT_hot − ΔT\_cold)·fraction; **Selected segment**: ¢?` TM[segment, 17] =
    〔169.94869〕 `

*   **R / 18**; **Quantity (original units)**: Water effective c_p in segment
    (kJ/kg·K); **Purpose / formula description**: (h_end − h_start)/(T_end −
    T\_start); **Selected segment**: ¢?` TM[segment, 18] = 〔118.49406〕 `

*   **S / 19**; **Quantity (original units)**: Local water capacity rate ṁ_w·c_p
    (MW/K); **Purpose / formula description**: ṁ_w × effective c_p; **Selected
    segment**: ¢?` TM[segment, 19] = 〔28.109567〕 `

*   **T / 20**; **Quantity (original units)**: Stream with larger capacity rate;
    **Purpose / formula description**: Water if ṁ_w c_p > C_salt (ε-NTU "C_min"
    swaps) (1 = Water; 0 = Salt); **Selected segment**: ¢?` TM[segment, 20] = 〔1〕 `

*   **U / 21**; **Quantity (original units)**: Water density at mean T (kg/m³);
    **Purpose / formula description**: Water\_Properties lookup; **Selected
    segment**: ¢?` TM[segment, 21] = 〔323.82811〕 `

*   **V / 22**; **Quantity (original units)**: Water viscosity at mean T (Pa·s);
    **Purpose / formula description**: Water\_Properties lookup; **Selected
    segment**: ¢?` TM[segment, 22] = 〔0.000040321056〕 `

*   **W / 23**; **Quantity (original units)**: Water conductivity at mean T (W/m·K);
    **Purpose / formula description**: Water\_Properties lookup; **Selected
    segment**: ¢?` TM[segment, 23] = 〔0.44559522〕 `

*   **X / 24**; **Quantity (original units)**: Water true c_p at mean T (kJ/kg·K);
    **Purpose / formula description**: Water_Properties lookup (used by
    Jackson); **Selected segment**: ¢?` TM[segment, 24] = 〔120.40438〕 `

*   **Y / 25**; **Quantity (original units)**: Water enthalpy at mean T (kJ/kg);
    **Purpose / formula description**: Water\_Properties lookup (used by
    Jackson); **Selected segment**: ¢?` TM[segment, 25] = 〔2,122.3391〕 `

*   **Z / 26**; **Quantity (original units)**: Water expansion coefficient β at mean
    T (1/K); **Purpose / formula description**: Water\_Properties lookup
    (buoyancy checks); **Selected segment**: ¢?` TM[segment, 26] = 〔0.21004131〕 `

*   **AA / 27**; **Quantity (original units)**: Salt density at mean T (kg/m³);
    **Purpose / formula description**: ρ = a + bT; **Selected segment**: ¢?`
    TM[segment, 27] = 〔1,638.0993〕 `

*   **AB / 28**; **Quantity (original units)**: Salt specific heat at mean T
    (J/kg·K); **Purpose / formula description**: c\_p = a + bT; **Selected
    segment**: ¢?` TM[segment, 28] = 〔1,016.7791〕 `

*   **AC / 29**; **Quantity (original units)**: Salt viscosity at mean T (Pa·s);
    **Purpose / formula description**: μ = a·exp(b/T); **Selected segment**:
    ¢?` TM[segment, 29] = 〔0.0029511707〕 `

*   **AD / 30**; **Quantity (original units)**: Salt conductivity at mean T (W/m·K);
    **Purpose / formula description**: k = a + bT; **Selected segment**: ¢?`
    TM[segment, 30] = 〔0.43420752〕 `

### Model\_Spreadsheet

*   **A / 1**; **Quantity (original units)**: Segment number; **Purpose / formula
    description**: From Temperature\_March; **Selected segment**: ¢?`
    SS[segment, 1] = 〔189〕 `

*   **B / 2**; **Quantity (original units)**: Water mean temperature (K); **Purpose
    / formula description**: From Temperature\_March; **Selected segment**: ¢?`
    SS[segment, 2] = 〔654.25〕 `

*   **C / 3**; **Quantity (original units)**: Salt mean temperature (K); **Purpose /
    formula description**: From Temperature\_March; **Selected segment**: ¢?`
    SS[segment, 3] = 〔842.20184〕 `

*   **D / 4**; **Quantity (original units)**: Segment LMTD (K); **Purpose / formula
    description**: From Temperature\_March; **Selected segment**: ¢?`
    SS[segment, 4] = 〔187.95049〕 `

*   **E / 5**; **Quantity (original units)**: Heat per steam tube in segment (W);
    **Purpose / formula description**: Segment heat × 10⁶ / N\_steam;
    **Selected segment**: ¢?` SS[segment, 5] = 〔2,150.3646〕 `

*   **F / 6**; **Quantity (original units)**: Water velocity (m/s); **Purpose /
    formula description**: ṁ\_tube/(ρ A); **Selected segment**: ¢?` SS[segment,
    6] = 〔0.35676405〕 `

*   **G / 7**; **Quantity (original units)**: Water Reynolds number (-); **Purpose /
    formula description**: ρ v D/μ; **Selected segment**: ¢?` SS[segment, 7] =
    〔57,305.161〕 `

*   **H / 8**; **Quantity (original units)**: Water Prandtl number (-); **Purpose /
    formula description**: c\_p,eff μ/k; **Selected segment**: ¢?` SS[segment,
    8] = 〔10.7223〕 `

*   **I / 9**; **Quantity (original units)**: Water Nusselt number (-); **Purpose /
    formula description**: Spreadsheet: 0.0266 Re^0.805 Pr^(1/3); **Selected
    segment**: ¢?` SS[segment, 9] = 〔396.8779〕 `

*   **J / 10**; **Quantity (original units)**: Water-side h (W/m²·K); **Purpose /
    formula description**: Nu k/D; **Selected segment**: ¢?` SS[segment, 10] =
    〔8,842.3449〕 `

*   **K / 11**; **Quantity (original units)**: Salt velocity (m/s); **Purpose /
    formula description**: ṁ\_tube/(ρ A); **Selected segment**: ¢?` SS[segment,
    11] = 〔2.4460122〕 `

*   **L / 12**; **Quantity (original units)**: Salt Reynolds number (-); **Purpose /
    formula description**: ρ v D/μ; **Selected segment**: ¢?` SS[segment, 12] =
    〔27,154.043〕 `

*   **M / 13**; **Quantity (original units)**: Salt Prandtl number (-); **Purpose /
    formula description**: c\_p μ/k; **Selected segment**: ¢?` SS[segment, 13]
    = 〔6.9107247〕 `

*   **N / 14**; **Quantity (original units)**: Salt Nusselt number (-); **Purpose /
    formula description**: Spreadsheet: 0.0266 Re^0.805 Pr^(1/3); **Selected
    segment**: ¢?` SS[segment, 14] = 〔187.91421〕 `

*   **O / 15**; **Quantity (original units)**: Salt-side h (W/m²·K); **Purpose /
    formula description**: Nu k/D; **Selected segment**: ¢?` SS[segment, 15] =
    〔4,079.6881〕 `

*   **P / 16**; **Quantity (original units)**: Water film resistance (m²·K/kW);
    **Purpose / formula description**: 1000/h\_water (on contact width);
    **Selected segment**: ¢?` SS[segment, 16] = 〔0.11309217〕 `

*   **Q / 17**; **Quantity (original units)**: Salt film resistance (m²·K/kW);
    **Purpose / formula description**: 1000/h\_salt (on contact width);
    **Selected segment**: ¢?` SS[segment, 17] = 〔0.24511678〕 `

*   **R / 18**; **Quantity (original units)**: Two tube walls (m²·K/kW); **Purpose /
    formula description**: 1000 × 2t/k (no interface resistance); **Selected
    segment**: ¢?` SS[segment, 18] = 〔0.21052632〕 `

*   **S / 19**; **Quantity (original units)**: Total resistance (m²·K/kW); **Purpose
    / formula description**: Sum of the three; **Selected segment**: ¢?`
    SS[segment, 19] = 〔0.56873527〕 `

*   **T / 20**; **Quantity (original units)**: Local U, contact-area basis (W/m²·K);
    **Purpose / formula description**: 1000/R\_total; **Selected segment**: ¢?`
    SS[segment, 20] = 〔1,758.2873〕 `

*   **U / 21**; **Quantity (original units)**: Tube length for segment (m);
    **Purpose / formula description**: Q\_tube R /(LMTD × contact width);
    **Selected segment**: ¢?` SS[segment, 21] = 〔0.17260274〕 `

*   **V / 22**; **Quantity (original units)**: Height at segment end (m); **Purpose
    / formula description**: Running sum of segment lengths; **Selected
    segment**: ¢?` SS[segment, 22] = 〔3.1881877〕 `

*   **W / 23**; **Quantity (original units)**: Heat flux at contact strip (kW/m²);
    **Purpose / formula description**: LMTD/R\_total; **Selected segment**: ¢?`
    SS[segment, 23] = 〔330.47097〕 `

*   **X / 24**; **Quantity (original units)**: Steam-side wall temperature (K);
    **Purpose / formula description**: T_water + q/h_water; **Selected
    segment**: ¢?` SS[segment, 24] = 〔691.62368〕 `

*   **Y / 25**; **Quantity (original units)**: Salt-side wall temperature (K);
    **Purpose / formula description**: T_salt − q/h_salt; **Selected segment**:
    ¢?` SS[segment, 25] = 〔761.19786〕 `

*   **Z / 26**; **Quantity (original units)**: Heat flux, steam-bore average
    (kW/m²); **Purpose / formula description**: Q\_tube/(ΔL π D)/1000;
    **Selected segment**: ¢?` SS[segment, 26] = 〔198.28258〕 `

*   **AA / 27**; **Quantity (original units)**: Heat flux / mass flux q″/G (kJ/kg);
    **Purpose / formula description**: Bore-average q″/G (HTD indicator, >
    0.4); **Selected segment**: ¢?` SS[segment, 27] = 〔1.7162831〕 `

*   **AB / 28**; **Quantity (original units)**: Water Darcy friction factor (-);
    **Purpose / formula description**: (8/6.0516)\[ln(ε/D + (7/Re)^0.9)]^-2;
    **Selected segment**: ¢?` SS[segment, 28] = 〔0.021254128〕 `

*   **AC / 29**; **Quantity (original units)**: Water friction ΔP (Pa); **Purpose /
    formula description**: f (ΔL/D) ρ v²/2; **Selected segment**: ¢?`
    SS[segment, 29] = 〔3.7801385〕 `

*   **AD / 30**; **Quantity (original units)**: Water gravity ΔP (Pa); **Purpose /
    formula description**: ρ g ΔL (upflow); **Selected segment**: ¢?`
    SS[segment, 30] = 〔548.3164〕 `

*   **AE / 31**; **Quantity (original units)**: Salt Darcy friction factor (-);
    **Purpose / formula description**: Same form as water; **Selected
    segment**: ¢?` SS[segment, 31] = 〔0.024690612〕 `

*   **AF / 32**; **Quantity (original units)**: Salt friction ΔP (Pa); **Purpose /
    formula description**: f (ΔL/D) ρ v²/2; **Selected segment**: ¢?`
    SS[segment, 32] = 〔1,044.1839〕 `

### Model\_BestEstimate

*   **A / 1**; **Quantity (original units)**: Segment number; **Purpose / formula
    description**: From Temperature\_March; **Selected segment**: ¢?`
    BE[segment, 1] = 〔189〕 `

*   **B / 2**; **Quantity (original units)**: Water mean temperature (K); **Purpose
    / formula description**: From Temperature\_March; **Selected segment**: ¢?`
    BE[segment, 2] = 〔654.25〕 `

*   **C / 3**; **Quantity (original units)**: Salt mean temperature (K); **Purpose /
    formula description**: From Temperature\_March; **Selected segment**: ¢?`
    BE[segment, 3] = 〔842.20184〕 `

*   **D / 4**; **Quantity (original units)**: Segment LMTD (K); **Purpose / formula
    description**: From Temperature\_March; **Selected segment**: ¢?`
    BE[segment, 4] = 〔187.95049〕 `

*   **E / 5**; **Quantity (original units)**: Heat per steam tube in segment (W);
    **Purpose / formula description**: Segment heat × 10⁶ / N\_steam;
    **Selected segment**: ¢?` BE[segment, 5] = 〔2,150.3646〕 `

*   **F / 6**; **Quantity (original units)**: Salt velocity (m/s); **Purpose /
    formula description**: ṁ\_tube/(ρ A); **Selected segment**: ¢?` BE[segment,
    6] = 〔2.4460122〕 `

*   **G / 7**; **Quantity (original units)**: Salt Reynolds number (-); **Purpose /
    formula description**: ρ v D/μ; **Selected segment**: ¢?` BE[segment, 7] =
    〔27,154.043〕 `

*   **H / 8**; **Quantity (original units)**: Salt Prandtl number (-); **Purpose /
    formula description**: c\_p μ/k; **Selected segment**: ¢?` BE[segment, 8] =
    〔6.9107247〕 `

*   **I / 9**; **Quantity (original units)**: Petukhov friction factor (-);
    **Purpose / formula description**: (0.790 ln Re − 1.64)\^-2; **Selected
    segment**: ¢?` BE[segment, 9] = 〔0.024221935〕 `

*   **J / 10**; **Quantity (original units)**: Salt Nusselt, Gnielinski (-);
    **Purpose / formula description**: (f/8)(Re − 1000)Pr / \[1 + 12.7
    √(f/8)(Pr\^(2/3) − 1)]; **Selected segment**: ¢?` BE[segment, 10] =
    〔192.92413〕 `

*   **K / 11**; **Quantity (original units)**: Salt-side h (W/m²·K); **Purpose /
    formula description**: Nu k/D; **Selected segment**: ¢?` BE[segment, 11] =
    〔4,188.4554〕 `

*   **L / 12**; **Quantity (original units)**: Water bulk Reynolds number (-);
    **Purpose / formula description**: G D/μ\_bulk; **Selected segment**: ¢?`
    BE[segment, 12] = 〔57,305.161〕 `

*   **M / 13**; **Quantity (original units)**: Water bulk Prandtl number (-);
    **Purpose / formula description**: c\_p,bulk μ/k; **Selected segment**: ¢?`
    BE[segment, 13] = 〔10.895161〕 `

*   **N / 14**; **Quantity (original units)**: Pass 1: assumed steam-side wall T
    (K); **Purpose / formula description**: Pass 1: previous row's final wall
    T + ΔT\_bulk; Pass 2: result of pass 1; **Selected segment**: ¢?`
    BE[segment, 14] = 〔708.13789〕 `

*   **O / 15**; **Quantity (original units)**: Pass 1: water density at wall T
    (kg/m³); **Purpose / formula description**: Water\_Properties
    interpolation; **Selected segment**: ¢?` BE[segment, 15] = 〔110.53143〕 `

*   **P / 16**; **Quantity (original units)**: Pass 1: water enthalpy at wall T
    (kJ/kg); **Purpose / formula description**: Water\_Properties
    interpolation; **Selected segment**: ¢?` BE[segment, 16] = 〔2,896.5328〕 `

*   **Q / 17**; **Quantity (original units)**: Pass 1: integrated c̄_p wall-bulk
    (J/kg·K); **Purpose / formula description**: (h_wall − h_bulk)/(T_wall −
    T\_bulk); **Selected segment**: ¢?` BE[segment, 17] = 〔14,366.746〕 `

*   **R / 18**; **Quantity (original units)**: Pass 1: Jackson exponent n (-);
    **Purpose / formula description**: 0.4, or 0.4 + 0.2(Tw/Tpc − 1)\[…] by
    T_b, T_w vs T\_pc; **Selected segment**: ¢?` BE[segment, 18] = 〔0.41643018〕 `

*   **S / 19**; **Quantity (original units)**: Pass 1: water-side h, Jackson
    (W/m²·K); **Purpose / formula description**: Nu = 0.0183 Re^0.82 Pr^0.5
    (ρw/ρb)^0.3 (c̄p/cp)^n; h = Nu k/D; **Selected segment**: ¢?` BE[segment,
    19] = 〔3,207.4908〕 `

*   **T / 20**; **Quantity (original units)**: Pass 1: wall conductivity, 316 SS
    (W/m·K); **Purpose / formula description**: Table interpolation at
    (T_wall + T_salt)/2; **Selected segment**: ¢?` BE[segment, 20] = 〔20.927548〕 `

*   **U / 21**; **Quantity (original units)**: Pass 1: fin efficiency, 60° arc (-);
    **Purpose / formula description**: tanh(mL)/(mL), m = √(h/kt), L = r\_m
    θ/2; **Selected segment**: ¢?` BE[segment, 21] = 〔0.57753214〕 `

*   **V / 22**; **Quantity (original units)**: Pass 1: fin efficiency, 120° arc (-);
    **Purpose / formula description**: Same, longer arc; **Selected segment**:
    ¢?` BE[segment, 22] = 〔0.31253187〕 `

*   **W / 23**; **Quantity (original units)**: Pass 1: effective water-wetted
    perimeter (m); **Purpose / formula description**: r\_i \[π + η1 θ1 + η2
    θ2]; **Selected segment**: ¢?` BE[segment, 23] = 〔0.044009481〕 `

*   **X / 24**; **Quantity (original units)**: Pass 1: salt-tube fin efficiency (-);
    **Purpose / formula description**: tanh(mL)/(mL) with h\_salt; **Selected
    segment**: ¢?` BE[segment, 24] = 〔0.52088092〕 `

*   **Y / 25**; **Quantity (original units)**: Pass 1: effective salt-wetted
    perimeter per steam tube (m); **Purpose / formula description**:
    (N_salt/N_steam) 2π r_i \[backed + (1 − backed) η_s]; **Selected segment**:
    ¢?` BE[segment, 25] = 〔0.039597905〕 `

*   **Z / 26**; **Quantity (original units)**: Pass 1: water film resistance
    (K·m/W); **Purpose / formula description**: 1/(h P\_w); **Selected
    segment**: ¢?` BE[segment, 26] = 〔0.0070841596〕 `

*   **AA / 27**; **Quantity (original units)**: Pass 1: salt film resistance
    (K·m/W); **Purpose / formula description**: 1/(h_salt P_s); **Selected
    segment**: ¢?` BE[segment, 27] = 〔0.0060293972〕 `

*   **AB / 28**; **Quantity (original units)**: Pass 1: two walls (K·m/W); **Purpose
    / formula description**: 2t/(k w); **Selected segment**: ¢?` BE[segment,
    28] = 〔0.00507003〕 `

*   **AC / 29**; **Quantity (original units)**: Pass 1: tube-to-tube interface
    (K·m/W); **Purpose / formula description**: 1/(h_c w); 0 if h_c = 0;
    **Selected segment**: ¢?` BE[segment, 29] = 〔0.0071691416〕 `

*   **AD / 30**; **Quantity (original units)**: Pass 1: total resistance per steam
    tube (K·m/W); **Purpose / formula description**: Sum of four; **Selected
    segment**: ¢?` BE[segment, 30] = 〔0.025352728〕 `

*   **AE / 31**; **Quantity (original units)**: Pass 1: updated steam-side wall T
    (K); **Purpose / formula description**: T_water + (LMTD/R_total) ×
    R\_water; **Selected segment**: ¢?` BE[segment, 31] = 〔706.76787〕 `

*   **AF / 32**; **Quantity (original units)**: Pass 2: assumed steam-side wall T
    (K); **Purpose / formula description**: Pass 1: previous row's final wall
    T + ΔT\_bulk; Pass 2: result of pass 1; **Selected segment**: ¢?`
    BE[segment, 32] = 〔706.76787〕 `

*   **AG / 33**; **Quantity (original units)**: Pass 2: water density at wall T
    (kg/m³); **Purpose / formula description**: Water\_Properties
    interpolation; **Selected segment**: ¢?` BE[segment, 33] = 〔111.41025〕 `

*   **AH / 34**; **Quantity (original units)**: Pass 2: water enthalpy at wall T
    (kJ/kg); **Purpose / formula description**: Water\_Properties
    interpolation; **Selected segment**: ¢?` BE[segment, 34] = 〔2,888.8523〕 `

*   **AI / 35**; **Quantity (original units)**: Pass 2: integrated c̄_p wall-bulk
    (J/kg·K); **Purpose / formula description**: (h_wall − h_bulk)/(T_wall −
    T\_bulk); **Selected segment**: ¢?` BE[segment, 35] = 〔14,595.284〕 `

*   **AJ / 36**; **Quantity (original units)**: Pass 2: Jackson exponent n (-);
    **Purpose / formula description**: 0.4, or 0.4 + 0.2(Tw/Tpc − 1)\[…] by
    T_b, T_w vs T\_pc; **Selected segment**: ¢?` BE[segment, 36] = 〔0.41601145〕 `

*   **AK / 37**; **Quantity (original units)**: Pass 2: water-side h, Jackson
    (W/m²·K); **Purpose / formula description**: Nu = 0.0183 Re^0.82 Pr^0.5
    (ρw/ρb)^0.3 (c̄p/cp)^n; h = Nu k/D × HTD multiplier in zone; **Selected
    segment**: ¢?` BE[segment, 37] = 〔3,239.1811〕 `

*   **AL / 38**; **Quantity (original units)**: Pass 2: wall conductivity, 316 SS
    (W/m·K); **Purpose / formula description**: Table interpolation at
    (T_wall + T_salt)/2; **Selected segment**: ¢?` BE[segment, 38] = 〔20.917273〕 `

*   **AM / 39**; **Quantity (original units)**: Pass 2: fin efficiency, 60° arc (-);
    **Purpose / formula description**: tanh(mL)/(mL), m = √(h/kt), L = r\_m
    θ/2; **Selected segment**: ¢?` BE[segment, 39] = 〔0.57533599〕 `

*   **AN / 40**; **Quantity (original units)**: Pass 2: fin efficiency, 120° arc
    (-); **Purpose / formula description**: Same, longer arc; **Selected
    segment**: ¢?` BE[segment, 40] = 〔0.31095724〕 `

*   **AO / 41**; **Quantity (original units)**: Pass 2: effective water-wetted
    perimeter (m); **Purpose / formula description**: r\_i \[π + η1 θ1 + η2
    θ2]; **Selected segment**: ¢?` BE[segment, 41] = 〔0.043953504〕 `

*   **AP / 42**; **Quantity (original units)**: Pass 2: salt-tube fin efficiency
    (-); **Purpose / formula description**: tanh(mL)/(mL) with h\_salt;
    **Selected segment**: ¢?` BE[segment, 42] = 〔0.52077741〕 `

*   **AQ / 43**; **Quantity (original units)**: Pass 2: effective salt-wetted
    perimeter per steam tube (m); **Purpose / formula description**:
    (N_salt/N_steam) 2π r_i \[backed + (1 − backed) η_s]; **Selected segment**:
    ¢?` BE[segment, 43] = 〔0.039596279〕 `

*   **AR / 44**; **Quantity (original units)**: Pass 2: water film resistance
    (K·m/W); **Purpose / formula description**: 1/(h P\_w); **Selected
    segment**: ¢?` BE[segment, 44] = 〔0.0070237858〕 `

*   **AS / 45**; **Quantity (original units)**: Pass 2: salt film resistance
    (K·m/W); **Purpose / formula description**: 1/(h_salt P_s); **Selected
    segment**: ¢?` BE[segment, 45] = 〔0.0060296448〕 `

*   **AT / 46**; **Quantity (original units)**: Pass 2: two walls (K·m/W); **Purpose
    / formula description**: 2t/(k w); **Selected segment**: ¢?` BE[segment,
    46] = 〔0.0050725205〕 `

*   **AU / 47**; **Quantity (original units)**: Pass 2: tube-to-tube interface
    (K·m/W); **Purpose / formula description**: 1/(h_c w); 0 if h_c = 0;
    **Selected segment**: ¢?` BE[segment, 47] = 〔0.0071691416〕 `

*   **AV / 48**; **Quantity (original units)**: Pass 2: total resistance per steam
    tube (K·m/W); **Purpose / formula description**: Sum of four; **Selected
    segment**: ¢?` BE[segment, 48] = 〔0.025295093〕 `

*   **AW / 49**; **Quantity (original units)**: Pass 2: updated steam-side wall T
    (K); **Purpose / formula description**: T_water + (LMTD/R_total) ×
    R\_water; **Selected segment**: ¢?` BE[segment, 49] = 〔706.43894〕 `

*   **AX / 50**; **Quantity (original units)**: Heat per unit length per steam tube
    (W/m); **Purpose / formula description**: LMTD / R\_total (pass 2);
    **Selected segment**: ¢?` BE[segment, 50] = 〔7,430.3145〕 `

*   **AY / 51**; **Quantity (original units)**: Tube length for segment (m);
    **Purpose / formula description**: Q\_tube / q′; **Selected segment**: ¢?`
    BE[segment, 51] = 〔0.28940426〕 `

*   **AZ / 52**; **Quantity (original units)**: Height at segment end (m); **Purpose
    / formula description**: Running sum of segment lengths; **Selected
    segment**: ¢?` BE[segment, 52] = 〔4.5732958〕 `

*   **BA / 53**; **Quantity (original units)**: Local U, contact-area basis
    (W/m²·K); **Purpose / formula description**: 1/(R\_total × w); **Selected
    segment**: ¢?` BE[segment, 53] = 〔1,048.6549〕 `

*   **BB / 54**; **Quantity (original units)**: Final steam-side wall temperature
    (K); **Purpose / formula description**: T_water + q′ R_water (pass 2);
    **Selected segment**: ¢?` BE[segment, 54] = 〔706.43894〕 `

*   **BC / 55**; **Quantity (original units)**: Salt-side wall temperature (K);
    **Purpose / formula description**: T_salt − q′ R_salt; **Selected
    segment**: ¢?` BE[segment, 55] = 〔797.39968〕 `

*   **BD / 56**; **Quantity (original units)**: Heat flux, steam-bore average
    (kW/m²); **Purpose / formula description**: q′/(π D)/1000; **Selected
    segment**: ¢?` BE[segment, 56] = 〔118.25713〕 `

*   **BE / 57**; **Quantity (original units)**: Heat flux / mass flux q″/G (kJ/kg);
    **Purpose / formula description**: HTD indicator; concern above 0.4;
    **Selected segment**: ¢?` BE[segment, 57] = 〔1.0236033〕 `

*   **BF / 58**; **Quantity (original units)**: In deterioration-prone zone? (1 =
    yes); **Purpose / formula description**: T_bulk \< T_pc \< T\_wall;
    **Selected segment**: ¢?` BE[segment, 58] = 〔1〕 `

*   **BG / 59**; **Quantity (original units)**: Buoyancy parameter Bo\* (-);
    **Purpose / formula description**: Gr_/(Re^3.425 Pr^0.8), Gr_ =
    gβD⁴q″/(kν²); **Selected segment**: ¢?` BE[segment, 59] = 〔0.000042164345〕 `

*   **BH / 60**; **Quantity (original units)**: Acceleration parameter K_v (-);
    **Purpose / formula description**: 4 q″ β/(G c_p Re); **Selected segment**:
    ¢?` BE[segment, 60] = 〔1.2464085e-7〕 `

*   **BI / 61**; **Quantity (original units)**: Water velocity (m/s); **Purpose /
    formula description**: G/ρ; **Selected segment**: ¢?` BE[segment, 61] =
    〔0.35676405〕 `

*   **BJ / 62**; **Quantity (original units)**: Water Darcy friction factor (-);
    **Purpose / formula description**: (8/6.0516)\[ln(ε/D + (7/Re)^0.9)]^-2;
    **Selected segment**: ¢?` BE[segment, 62] = 〔0.021254128〕 `

*   **BK / 63**; **Quantity (original units)**: Water friction ΔP (Pa); **Purpose /
    formula description**: f (ΔL/D) ρ v²/2; **Selected segment**: ¢?`
    BE[segment, 63] = 〔6.3381856〕 `

*   **BL / 64**; **Quantity (original units)**: Water gravity ΔP (Pa); **Purpose /
    formula description**: ρ g ΔL; **Selected segment**: ¢?` BE[segment, 64] =
    〔919.36607〕 `

*   **BM / 65**; **Quantity (original units)**: Salt Darcy friction factor (-);
    **Purpose / formula description**: Same form; **Selected segment**: ¢?`
    BE[segment, 65] = 〔0.024690612〕 `

*   **BN / 66**; **Quantity (original units)**: Salt friction ΔP (Pa); **Purpose /
    formula description**: f (ΔL/D) ρ v²/2; **Selected segment**: ¢?`
    BE[segment, 66] = 〔1,750.7908〕 `

### Chart helper matrix

CH has 540 rows. Its ten columns reproduce original Charts R:AA in order.

*   **1**; **Original Excel column**: R; **Meaning**: Height, best estimate (m)

*   **2**; **Original Excel column**: S; **Meaning**: Salt T at segment end (K)

*   **3**; **Original Excel column**: T; **Meaning**: Water T at segment end (K)

*   **4**; **Original Excel column**: U; **Meaning**: Steam-side wall T, best (K)

*   **5**; **Original Excel column**: V; **Meaning**: Duty fraction (-)

*   **6**; **Original Excel column**: W; **Meaning**: Actual ΔT at segment end (K)

*   **7**; **Original Excel column**: X; **Meaning**: ΔT single LMTD assumes (K)

*   **8**; **Original Excel column**: Y; **Meaning**: Water mean T (K)

*   **9**; **Original Excel column**: Z; **Meaning**: h\_water spreadsheet (kW/m²K)

*   **10**; **Original Excel column**: AA; **Meaning**: h\_water Jackson (kW/m²K)

## Studies: original static results

These values are copied from the original Studies sheet and are intentionally
not recalculated. Several study cases were solved by the external script with a
different iteration/convergence configuration, so their baseline lengths can
differ slightly from the live two-pass workbook.

### Validation and model decomposition (heated length, 6,536 × 20 mm tubes)

*   **Replica of counterSG.xlsx (5 K steps) : workbook value 11.92 m**; **Length
    (m)**: 11.9628549490461

*   **Spreadsheet physics (0.5 K steps)**; **Length (m)**: 11.8521532043238

*   **Spreadsheet physics + Jackson water-side h**; **Length (m)**: 15.4832813970088

*   **Independent model, perfect contact**; **Length (m)**: 12.4037392514854

*   **Independent model, h\_c = 3,700 W/m2K (best estimate)**; **Length (m)**:
    15.3598874649616

### Contact conductance sensitivity (best-estimate model)

*   **Perfect contact**; **Length (m)**: 12.4037392514854; **U contact (W/m²K)**:
    992.634355263244; **Salt ΔP (kPa)**: 85.4082066276642; **Max steam wall
    (K)**: 870.745505150995

*   **10,000**; **Length (m)**: 13.4835650635133; **U contact (W/m²K)**:
    913.139637533181; **Salt ΔP (kPa)**: 91.9410191380872; **Max steam wall
    (K)**: 867.694528397423

*   **3,700**; **Length (m)**: 15.3598874649616; **U contact (W/m²K)**:
    801.592963674903; **Salt ΔP (kPa)**: 103.292551805917; **Max steam wall
    (K)**: 863.41470014111

*   **2,000**; **Length (m)**: 17.9575262145625; **U contact (W/m²K)**:
    685.638855131781; **Salt ΔP (kPa)**: 119.008071468968; **Max steam wall
    (K)**: 858.95460467417

### Heat-transfer deterioration sensitivity (h_water multiplier in T_b \< T_pc \< T_wall zone)

*   **1**; **Length (m)**: 15.3598874649616; **Zone top (m)**: 4.57221863068192

*   **0.7**; **Length (m)**: 16.1379463672621; **Zone top (m)**: 5.35027745084437

*   **0.5**; **Length (m)**: 17.1756897582061; **Zone top (m)**: 6.38802083210906

### Steam tubes needed to keep L = 11.92 m (3:4 salt ratio kept)

*   **Perfect contact**; **N steam**: 7270; **N salt**: 5452; **Salt v (m/s)**:
    2.21045975257817; **G (kg/m²s)**: 103.865967500175; **Salt ΔP (kPa)**:
    68.0591057867303

*   **10,000**; **N steam**: 8801; **N salt**: 6601; **Salt v (m/s)**:
    1.82569710211426; **G (kg/m²s)**: 85.7977029571949; **Salt ΔP (kPa)**:
    48.2288196318514

*   **3,700**; **N steam**: 11246; **N salt**: 8434; **Salt v (m/s)**:
    1.42890995625518; **G (kg/m²s)**: 67.1443698849611; **Salt ΔP (kPa)**:
    31.0903620487504

*   **2,000**; **N steam**: 14348; **N salt**: 10761; **Salt v (m/s)**:
    1.11991697528633; **G (kg/m²s)**: 52.6279330726424; **Salt ΔP (kPa)**:
    20.1499906020328

### Tube count / diameter sweep (best estimate, h\_c = 3,700, 2 mm walls)

*   **16**; **N steam**: 5000; **L (m)**: 17.2256244633486; **Salt v (m/s)**:
    5.02142773794008; **G (kg/m²s)**: 235.97049491446; **Salt ΔP (kPa)**:
    539.821521382649; **Salt pump (kW)**: 2038.91245196788; **Water ΔP (kPa)**:
    48.7550564010859

*   **16**; **N steam**: 6536; **L (m)**: 14.6725842522869; **Salt v (m/s)**:
    3.84136148863225; **G (kg/m²s)**: 180.515984481686; **Salt ΔP (kPa)**:
    286.040452613918; **Salt pump (kW)**: 1080.37826855673; **Water ΔP (kPa)**:
    39.6177290556614

*   **16**; **N steam**: 8000; **L (m)**: 13.0985997743122; **Salt v (m/s)**:
    3.13839233621255; **G (kg/m²s)**: 147.481559321538; **Salt ΔP (kPa)**:
    178.855163364436; **Salt pump (kW)**: 675.538127395264; **Water ΔP (kPa)**:
    34.4840714031904

*   **16**; **N steam**: 10000; **L (m)**: 11.6440721941427; **Salt v (m/s)**:
    2.51071386897004; **G (kg/m²s)**: 117.98524745723; **Salt ΔP (kPa)**:
    107.51016077914; **Salt pump (kW)**: 406.06718488031; **Water ΔP (kPa)**:
    30.0344587606027

*   **20**; **N steam**: 5000; **L (m)**: 17.6744310257473; **Salt v (m/s)**:
    3.21371375228165; **G (kg/m²s)**: 151.021116745255; **Salt ΔP (kPa)**:
    190.399882951692; **Salt pump (kW)**: 719.142673691687; **Water ΔP (kPa)**:
    46.0112495375648

*   **20**; **N steam**: 6536; **L (m)**: 15.3605799245547; **Salt v (m/s)**:
    2.45847135272464; **G (kg/m²s)**: 115.530230068279; **Salt ΔP (kPa)**:
    103.296735020485; **Salt pump (kW)**: 390.153024543093; **Water ΔP (kPa)**:
    39.2249524139937

*   **20**; **N steam**: 8000; **L (m)**: 13.9101622686809; **Salt v (m/s)**:
    2.00857109517603; **G (kg/m²s)**: 94.3881979657841; **Salt ΔP (kPa)**:
    65.6654900478659; **Salt pump (kW)**: 248.019354582683; **Water ΔP (kPa)**:
    35.1469197378294

*   **20**; **N steam**: 10000; **L (m)**: 12.5488973290414; **Salt v (m/s)**:
    1.60685687614083; **G (kg/m²s)**: 75.5105583726272; **Salt ΔP (kPa)**:
    40.1430413539396; **Salt pump (kW)**: 151.620755442967; **Water ΔP (kPa)**:
    31.4226084620086

### Alternative temperatures (kickoff list: salt 875→810 K, steam 560→860 K), spreadsheet physics

*   **Heated length (m)**; **Value**: 16.9375374205729

*   **UA (MW/K)**; **Value**: 3.97215043932806

*   **Effectiveness**; **Value**: 0.980287537953583

*   **NTU**; **Value**: 2.38329026359684

## Original workbook guidance

The following original README guidance is retained for provenance. References to
sheet colors, cell clicking and the rebuilding script describe Excel; use the
Hurmet instructions above for this file.

*   **Purpose**; **Original text**: Step-by-step (marching) heat-transfer sizing of
    one steam generator. Every calculated cell is a live formula: click any
    cell to see exactly where its value comes from.

*   **How the march works**; **Original text**: The water is heated from inlet to
    outlet in 540 equal temperature steps (0.5 K). Each row is one segment. For
    each segment: energy balance → salt temperature → local LMTD →
    heat-transfer coefficients → thermal resistance → tube length needed for
    that segment. Summing the lengths gives the heated tube length.

*   **Sheet: Inputs**; **Original text**: All inputs (blue) and derived design
    quantities. Change blue cells to explore; everything recalculates.

*   **Sheet: Temperature\_March**; **Original text**: Energy balance and
    temperatures for every segment. These do NOT depend on the tube design or
    heat-transfer model, so both models below use this sheet.

*   **Sheet: Model\_Spreadsheet**; **Original text**: Heat transfer using the
    physics of the sponsor's counterSG.xlsx (Nu = 0.0266 Re^0.805 Pr^(1/3),
    contact-width film areas, k = 19 W/m·K, no contact resistance). Replaces
    the old profile\_caseDesign.csv.

*   **Sheet: Model\_BestEstimate**; **Original text**: Independent best estimate:
    Gnielinski (salt), Jackson 2002 (supercritical water, with wall-temperature
    update in two passes), 316 SS k(T), tube-to-tube contact conductance,
    circumferential fin efficiency.

*   **Sheet: Results**; **Original text**: Side-by-side summary of both models:
    length, U, area, LMTD vs true mean ΔT, effectiveness, NTU, pressure drop,
    wall-temperature and deterioration checks.

*   **Sheet: Charts**; **Original text**: Temperature profile, LMTD straight-line vs
    actual ΔT, and water-side h comparison (live charts).

*   **Sheet: Studies**; **Original text**: Parametric results produced by
    wistr_sg_model.py (STATIC values, not formulas) : they need many full
    re-runs with different geometry, which the script does automatically.

*   **Sheet: Water\_Properties**; **Original text**: Trusted input data: IAPWS-95
    water properties at 24 MPa (same formulation as the NIST WebBook used in
    counterSG.xlsx), 0.25 K spacing, 555-900 K. Lookups interpolate linearly
    between rows.

*   **Colour legend**; **Original text**: Blue text = hard-coded input. Black text =
    formula. Green text = direct link to another sheet.

*   **March sheet headers**; **Original text**: Row 2 = group of columns, Row 3 =
    quantity (units), Row 4 = how it is calculated. Data start in row 5.

*   **Limits of live editing**; **Original text**: You can change any blue input
    (temperatures, tube count, diameter, contact conductance, etc.). The number
    of segments is fixed at 540 rows; the step size adjusts automatically.
    Water temperatures must stay within the 555-900 K property table.

*   **Source of the script**; **Original text**: wistr_sg_model.py rebuilds this
    workbook, the Studies sheet and the report figures.

## Conversion verification

All **74,631 original formula-cell results** were compared with the source
workbook's cached values, including all 540 rows of both models and the chart
helpers. The comparison also checked the named input constants; there were
**zero mismatches** at the acceptance tolerance of 1×10⁻¹⁰ absolute plus 1×10⁻⁸
relative.

The largest relative discrepancy was 3.690e-11 (about 3.690e-9%). This is a
numerical equivalence check, not validation of the physical heat-transfer
assumptions.

*   **Sponsor-physics heated length:** 11.852153204 m.
*   **Best-estimate heated length:** 15.359913322 m.
*   **Required UA:** 3.033787045 MW/K.
*   **Best-estimate inner wall, segment 189 / Excel row 193:** 706.438937891 K.

A live recalculation test changed hcontact from 3,700 to 7,400 W/m²·K: heated
length decreased from 15.359913 m to 13.867200 m. A second test set hcontact =
0 (the workbook's perfect-contact convention), producing 12.403613 m; the
delivered document retains the original 3,700 W/m²·K baseline.

All native calculation entries were parsed from the actual Markdown file, not
merely checked as separate snippets. The three native chart drawings were
evaluated successfully, and the file was recalculated and saved through the
Hurmet engine.

The Hurmet source is self-contained: there are no spreadsheet links, network
property lookups, Python dependencies or JavaScript calculations in the
delivered file. The converter and verification harness are development tools
only; all delivered engineering calculations run in Hurmet.

[1]: https://hurmet.org/manual

[2]: draw(CH, rD22, Tfreeze, Tpc)␤    title "Temperature profile"␤    frame 600, 380␤    view 480, 960, -0.1*rD22, rD22*1.12␤    axes 50, 2, "labels"␤    strokewidth 2␤    stroke "blue"␤    path hcat(CH[,3], CH[,1])␤    stroke "orange"␤    path hcat(CH[,2], CH[,1])␤    stroke "red"␤    path hcat(CH[,4], CH[,1])␤    strokedasharray "6 4"␤    stroke "green"␤    line [Tfreeze, 0; Tfreeze, rD22]␤    stroke "purple"␤    line [Tpc, 0; Tpc, rD22]␤end

[3]: draw(CH, rD22, Tfreeze, Tpc)␤    title "Actual driving temperature difference versus straight-line assumption"␤    frame 600, 380␤    view -0.05, 1.05, -30, 300␤    axes 0.2, 50, "labels"␤    strokewidth 2␤    stroke "blue"␤    path hcat(CH[,5], CH[,6])␤    stroke "red"␤    path hcat(CH[,5], CH[,7])␤end

[4]: draw(CH, rD22, Tfreeze, Tpc)␤    title "Water-side convection coefficient"␤    frame 600, 380␤    view 540, 860, -0.1*max(max(CH[,9]), max(CH[,10])), max(max(CH[,9]), max(CH[,10]))*1.15␤    axes 50, 1, "labels"␤    strokewidth 2␤    stroke "blue"␤    path hcat(CH[,8], CH[,9])␤    stroke "red"␤    path hcat(CH[,8], CH[,10])␤end
