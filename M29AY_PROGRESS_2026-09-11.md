# FEARVita M29AY — shared ObjectDLL/world-runtime checkpoint

Date: 2026-09-11

M29AY continues from the full Vita-build-verified M29AX frontend milestone. Its goal is to move F.E.A.R., Extraction Point and Perseus Mandate together from the accepted local StartGame handshake into the real ObjectDLL/server/world runtime.

## Campaign parity

Fresh M29AX hardware logs show all three campaigns reaching the same technical frontier: retail frontend active, campaign archives/databases selected, local start accepted, then waiting for real ObjectDLL/server/world runtime. M29AY therefore implements one shared server/runtime foundation and keeps campaign-specific behavior limited to archive/database overlays and localization data.

## German addon mission/loading screens

The Vita German-system-language intro fallback now covers campaign tags `fear`, `ep` and `pm` for `Worlds\\Release\\Intro`.

Common labels:
- `INTERVALL 01`
- `EINFÜHRUNG`
- `Tipp: SELECT öffnet die Missionsziele. Linker Stick: bewegen. Rechter Stick: umsehen.`

Campaign-specific FEARVita fallback briefing:
- F.E.A.R.: `F.E.A.R.: Einsatzdaten werden vorbereitet.`
- Extraction Point: `Extraction Point: Einsatzdaten werden vorbereitet.`
- Perseus Mandate: `Perseus Mandate: Einsatzdaten werden vorbereitet.`

These are FEARVita-authored fallback strings, not claimed to be official retail German localization.

## ObjectDLL target alignment

Pinned upstream remains `jsj2008/lithtech` commit `0eab18289bed72879eddb648d3311075b108cf46`, with `lithtech-overlay/` applied.

The Vita server target is aligned to the original retail `Game_ServerShell.vcproj` rather than blindly compiling every ObjectDLL source. `AIGoalGotoCombat.cpp` and `MeleeWeaponModel.cpp` are excluded because neither belongs to the retail server project and both target older/incompatible API generations.

Configured translation-unit counts:
- ClientShell: 229
- ObjectDLL/server: 533
- ClientFX: 31
- Shared: 69
- LTGUI: 20

The server target uses `_FINAL=1` to match retail behavior and avoid editor/debug-only dependencies.

## FEAR SDK 1.08 compatibility

The public LithTech pin predates interfaces required by the retail F.E.A.R. ObjectDLL. M29AY restores those contracts against the public runtime, using the published F.E.A.R. SDK 1.08 as reference instead of inventing gameplay behavior.

Implemented so far:
- retail command/class/property metadata adapters (`ICommandDef`, `ICommandMessageDef`, command/string-id properties);
- `LTOBB`;
- FEAR memory-category `ObjectBank<T, category>` mapped to the public runtime bank where used;
- real `ILTServer::GetClientObject(HCLIENT)` backed by `Client::m_pObject`;
- server shadow-LOD compatibility (render metadata only);
- global `SendSFXMessage(msg, flags)` broadcast form;
- FEAR-style `GenericProp` / `GenericPropList` accessors;
- reference overloads for `IntersectSegment`, `SetObjectPos`, and `SetObjectRotation` while retaining the old runtime function pointers;
- `ObjectCreateStruct` physics-group compatibility;
- FEAR child-model index 0 mapped to legacy runtime child slot 1 (slot 0 remains the main model);
- scalar `LTIsNaN`;
- C++17 dependent-base lookup fix for `CRange<T>`;
- `LTIntersect::Point_Segment_DistSqr`, clamping the existing line projection to `[0,1]`.

Important caveat: F.E.A.R. SDK 1.08 property type numbering differs from the older public runtime around FLAGS/BOOL/LONGINT/ROTATION/COMMAND/STRINGID. Compile compatibility is in place, but property decoding must be verified during real world instantiation before claiming gameplay correctness.

## ARM validation frontier

CMake configures successfully with `FEARVITA_MENU_LINK_ONLY=OFF` and all 533 retail server translation units.

The ARM/Vita ObjectDLL compile has passed `AI.cpp` and the previous `AIActionGotoValidPosition.cpp` blocker. It is continuing incrementally through the AI action/activity sources. This checkpoint is compile-progress only: there is not yet a completed ObjectDLL link and there is no M29AY VPK yet.

## Reproduce

```sh
export VITASDK=/path/to/vitasdk
export PATH="$VITASDK/bin:$PATH"

cmake -S project -B build-vita -G Ninja \
  -DFEARVITA_ENABLE_GAME_MODULES=ON \
  -DFEARVITA_MENU_LINK_ONLY=OFF \
  -DFEARVITA_LITHTECH_ROOT=/path/to/patched/lithtech \
  -DCMAKE_BUILD_TYPE=Release

ninja -C build-vita fearvita_fear_server_objects -j6
```

## Next-chat handoff

1. Start from GitHub branch `m29ay-objectdll-world-runtime`.
2. Read `CURRENT_STATE_M29AY.txt`, this file and `patches/M29AY.patch` first.
3. Recreate upstream commit `0eab18289bed72879eddb648d3311075b108cf46`, apply `lithtech-overlay/`, then configure with `FEARVITA_MENU_LINK_ONLY=OFF`.
4. Continue `fearvita_fear_server_objects` from the first ARM compiler error. Prefer central SDK/runtime adapters verified against F.E.A.R. SDK 1.08 over per-callsite stubs.
5. After all 533 server TUs compile, link the real server/runtime into the Vita executable, instantiate `Worlds\\Release\\Intro`, and advance the local path through the real start-level messages.
6. Keep F.E.A.R., Extraction Point and Perseus Mandate on the same runtime implementation; only archive/database/localization selection should diverge.
7. Do not claim hardware validation until a new VPK is tested on a real Vita and fresh per-campaign logs are supplied.
