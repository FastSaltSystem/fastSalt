# Generator sizing in Pluto

**Comparison experiment retained for reference.** Hurmet is the preferred project worksheet; this notebook is not maintained as a parallel official calculation. See the [calculation conventions](../README.md).

This is the same preliminary generator-sizing calculation as the Calca and Hurmet worksheets, converted to Julia with Unitful quantities.

## Open it

In Finder, double-click **Open generator sizing in Pluto.command** in this folder. A Terminal window starts Pluto and opens the notebook in your browser. Keep that Terminal window open while working. When finished, press Control-C in that window.

If Pluto is already running, open **Generator sizing - Pluto.jl** from its start page instead.

The launcher uses the project's separate `pluto-environment` and does not add packages to your default Julia environment. The first launch on another computer needs Julia and an internet connection to obtain the recorded packages. Subsequent launches reuse the installed packages.

## Try a small edit

1. Find the first visible input cell containing `NGen = 3` and `ReactorPower = 1500u"MW"`.
2. Change 3 to 4, then press **Shift+Enter**.
3. Watch the results summary update: heat duty becomes **375 MW per generator**, and salt mass flow becomes **5,674.85788 kg/s per generator**.
4. Change 4 back to 3 and press Shift+Enter to restore the original case.

`1500u"MW"` means 1500 megawatts. Inputs remain close to their relevant calculation sections. Click the eye control beside a result cell to show its formulas; most calculation code starts folded to keep the document readable. You can edit formulas there as well. Pluto saves the notebook automatically.

The text, calculations, package environment, and displayed cell order are stored in the `.jl` file. `Generator sizing - Pluto.html` is a snapshot of the checked baseline results for reading and sharing; it does not recalculate by itself. Its viewer may need an internet connection to load Pluto's display assets.

## What was checked

- Julia 1.12.6, Pluto 1.0.4, Unitful 1.29.0.
- All 103 source calculation lines and eight functions are represented in 54 notebook cells.
- All 54 cells executed successfully in Pluto with no cell errors.
- All 84 numerical results displayed in Calca were compared with Julia results. **83 match within the source's displayed rounding precision.** The remaining difference is the same feet-of-water convention used in the Hurmet conversion: 2989 Pa per ftH₂O gives 63.8584111 rather than 63.8588, approximately 0.0006% lower. The pressure result in kPa agrees.
- Pluto's dependency-driven recalculation was checked by changing `NGen` from 3 to 4, verifying the updated duty, flow, tube length, and pumping power, and restoring 3. The restored results exactly matched the baseline.
- Original Calca and Hurmet files were left unchanged.

| Per-generator quantity | Original case: 3 generators | Recalculation check: 4 generators |
|:--|--:|--:|
| Heat duty | 500 MW | 375 MW |
| Salt flow | 7,566.47718 kg/s | 5,674.85788 kg/s |
| Tube length | 19.8790057 m | 18.3497129 m |
| Hydraulic pump power | 881.743122 kW | 368.025388 kW |

The original correlations and assumptions are retained. In particular, steam properties are fixed source inputs at 24 MPa, not a live property lookup, and pump power includes no efficiency allowance. The calculation checks establish conversion fidelity rather than design adequacy. Syntax changes and unit conventions are explained at the end of the notebook.

## Files

- **Generator sizing - Pluto.jl** — editable notebook, including its Unitful package environment.
- **Open generator sizing in Pluto.command** — double-click launcher for macOS.
- **pluto-environment/** — recorded package environment used to start Pluto.
- **Generator sizing - Pluto.html** — exported baseline results.
- **Pluto - comparison.tsv** — comparison of all 84 original displayed results.

Source: `/Users/thomaswielenga/Documents/Ideas/Nuclear Reactor/Steam Generator/Calculations/Generator sizing.calca`.
