# Steam-generator source workbook

`counterSG.xlsx` is Thomas Wielenga's newer counterflow steam-generator calculation, supplied on 14 October 2026 from `Documents/Ideas/Nuclear Reactor/Steam Generator/Calculations/counterSG.xlsx`.

At the owner's request, only `counter!AB16` and `AB17` were corrected to label 890 K as salt inlet and 810 K as salt outlet. Values, formulas, formatting and charts are unchanged. The uncorrected original is preserved in `../revisions/before-counterSG-2026-10-14/counterSG-original-labels.xlsx`. The corrected file is also saved at the original external location.

The workbook was recalculated with Artifact Tool and the 62 length increments independently reproduced with standard-library Python (`../counter_sg_basis.py`). The two authored labels were transferred to the original package so unrelated Excel parts remain byte-identical. The saved total remains 11.920866244 m. This verifies arithmetic, not exchanger performance or pressure-wall design.

D-063 adopts 4,902 salt tubes per SG, 20 mm ID, 24 mm OD, and 11.920866 m as a provisional straight hydraulic length. Its 6,536 steam tubes are not salt-flow passages. The 17 m casing and the reactor's 24,576 × 14 mm channels are separate dimensions and remain unchanged. Extra unheated length, collectors and actual contact/heat-transfer behavior remain to be resolved.

The workbook's 500 MW duty uses 6,170.524 kg/s salt per SG and 810–890 K. Normal hydraulic calculations retain 18,500 kg/s total and UM properties. The old Generator sizing Hurmet conversion and exploratory Brayton studies remain historical calculations; they do not define the current pump duty.
