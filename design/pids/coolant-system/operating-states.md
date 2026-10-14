# Coolant operating states — working concept

14 October 2026. Owner-selected arrangement, consolidated in D-057. This is a draft flow-path/state record, not an operating procedure. D-059 sets an approximate normal pressure target; pressure bands, vessel volumes, transfer triggers, instrumentation technology and protection remain unresolved.

## Gas collection and pressure control

Each SG has a top gas-collection vessel AC-101–103, with a continuously open salt/gas connection L-101G–103G. Its gas branch G-101–103 and valve V-101G–103G connect to H-401. Closing a gas valve does not isolate its vessel from the SG. Pressure and salt-level indications are included for each vessel; measurement methods remain unselected.

A single functional pressure-control station at coolant preparation supplies and receives gas through G-400. It is intended to hold the common SG bias-pressure band. Makeup and return hardware, receiving arrangements, pressure band, mode transitions and independent overpressure protection are not yet designed. This is the coolant gas system, separate from fuel off-gas treatment.

G-401 is removed. TK-401 uses G-402 / V-402G for both gas admission and return through H-401 / G-400. During tank emptying and gas sweep the three SG gas valves are closed. Tank pressurization settings are not assumed equal to the normal SG bias pressure.

## Normal pressure, level and leak basis — D-059

The owner specifies approximately **1 bar gauge (100 kPa gauge) at the steam-generator tops**, with a lower pressure potentially acceptable. This is a normal operating target, not the system design pressure or a relief setpoint. Other locations require a pressure profile accounting for elevation, circulation and pressure losses.

TK-401 is normally nearly empty so expansion space is available. P-401 adjusts circuit inventory to establish the levels in AC-101–103; the common gas station controls pressure separately. Numerical level targets and transfer logic remain unresolved. The selected tank envelope is recorded in D-058; relocation remains deferred.

The intended steam-side leak path is into the SG air side, **not directly into the coolant**. This corrects the earlier generic tube-failure wording. Air-space pressure response, leak detection and discharge arrangements still require the SG design interface to be developed.

Returning coolant overpressure to TK-401 is a **proposal for review**, not an adopted relief connection. The normal state closes V-401 and V-402 and stops P-401, so the current transfer route is not credited for relief. A proposed return must address path availability and displacement of tank gas/backpressure as well as liquid capacity. No relief hardware, sizing or setpoint is selected.

## Agreed states

The authoritative state values are in `coolant-system.toml`; sheet 4 is generated from them. All three SG gas valves share the position shown below.

| State | V-401 | V-402 | V-403 | SG gas valves | V-402G | P-401 |
| --- | --- | --- | --- | --- | --- | --- |
| Normal / between transfers | Closed | Closed | Closed | Open | Closed | Stopped |
| Expansion to storage | Open | Open | Closed | Open | Open | Reactor to storage |
| Contraction from storage | Open | Open | Closed | Open | Open | Storage to reactor |
| Reactor / SG drain | Open | Open | Closed | Open | Open | Reactor to storage |
| Reactor / SG refill | Open | Open | Closed | Open | Open | Storage to reactor |
| Tank to preparation | Closed | Closed | Open | Closed | Open | Stopped |
| Gas sweep to preparation | Closed | Closed | Open | Closed | Open | Stopped |

P-401 is stopped during tank-to-preparation transfer and gas sweep. The owner notes tank transfer may occur while the reactor is operating; this pump state does not establish the full concurrent-operation sequence. V-401 is closed in both states, as specified by the owner.

Transfers occur as needed, not continuously. The owner assigns most expansion capacity to TK-401, allowing nominal SG gas vessels. No numeric vessel volume has been selected. Transfer triggers, rate, control logic, available tank inventory/freeboard and restoration of the between-transfer state require development. The state table specifies intent without selecting automatic actions or implying that a stopped positive-displacement pump seals the circuit.

## Intended paths

- Reactor drain or expansion: R-101 bottom → L-401 → P-401 → L-402 → J-401 → L-404 → TK-401 bottom.
- Refill or contraction makeup: the same path in reverse, using reversed P-401.
- Tank emptying: preparation → G-400 → H-401 → G-402 → TK-401 gas space; displaced coolant leaves through L-404 → J-401 → L-403 → preparation.
- Subsequent gas sweep: gas follows the same path through the empty tank and its bottom connection. This applies to the tank/return line; reactor and SG drainage are handled separately through P-401.
- Supply from preparation: preparation → L-403 → J-401 → L-404 → tank. Supply driver and the full valve state remain unassigned.

J-401 is the intended physical low point at the tank bottom, joining L-402, L-403 and the single tank branch L-404. Drawing coordinates do not establish physical pipe slopes or complete drainage. The earlier reference to “fuel” in describing this operation is interpreted as **coolant salt**.

## Normal pressure follow-up — 14 October 2026

The [normal pressure worksheet](../../../calculations/reactor/Normal%20coolant%20pressure%20profile%20-%20Hurmet.md) provides a preliminary elevation/pump/loss envelope. It does not select relief settings or alter the state table. The owner explicitly defers SG failure assessment; retain it as unresolved work for later. Tank relocation also remains deferred.

## Remaining work

Refine the provisional inventory/storage screen and resolve gas-vessel volumes, pressure profiles, transfer triggers and controls, relief destinations, SG steam-to-air leak response, thermal protection of isolated salt, gas receiving arrangements, and physical drainage gradients. Nominal gas volumes and pressure control do not establish independent overpressure protection.

This batch updates P&ID sources, generated drawings/registers and documentation only. The gas system remains P&ID-only; no Blender regeneration or commit is included.

## Emergency relief is separate from operating states — D-062

14 October 2026. The owner selects one dedicated high-level coolant-side emergency relief connection on each SG, separate from the normal gas-collection/pressure-control piping. Add shared ports `SG-101/102/103.relief_high`, lines L-101R/102R/103R, and rupture-disc concepts RD-101/102/103. No intervening isolation valves are included. Discs are normally intact and remain open after actuation; they are not operable valves in the normal state table.

The requirement is to preserve reactor coolant inventory and prevent continued gravity drainage or siphoning after relief. A high takeoff alone does not prove retention during pressure-driven two-phase discharge. B-501 is an unresolved receiving-system interface with three separate terminations; it does not select a common header, number of receivers, pit, or vent route. No cold-leg downward dump is adopted.

Exact elevations, burst differential pressure at actual disc temperature, flow area/capacity, expelled salt volume, receiving/venting arrangement, backpressure, freeze protection, burst detection/response and subsequent cooling remain unresolved. Detailed SG-failure/transient assessment remains deferred. P&ID sheet 5 records the concept; sheet 1 cross-references it. Physical 3D nozzles/routing remain pending; no Blender rebuild or pressure-calculation change.
