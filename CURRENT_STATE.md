# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AY  
**Date:** 2026-09-11

The hardware-proven M29AX frontend remains the base: F.E.A.R., Extraction Point and Perseus Mandate reach their retail menus with the canonical M29AW Vita gameplay controls and M29AX D-pad/front-touch navigation. Fresh logs put all three campaigns at the same accepted `StartGame` frontier, so M29AY advances a single shared ObjectDLL/server/world runtime for all three.

M29AY also extends the FEARVita-authored German intro/loading fallback to `fear`, `ep` and `pm` for `Worlds\\Release\\Intro`, with common German mission labels and campaign-specific briefing text. These strings are FEARVita fallbacks, not claimed as official retail localization.

The pinned upstream remains `jsj2008/lithtech` @ `0eab18289bed72879eddb648d3311075b108cf46`. Current CMake counts are **223 ClientShell, 533 ObjectDLL/server, 31 ClientFX, 69 Shared and 20 LTGUI** translation units. The server uses `_FINAL=1`; `AIGoalGotoCombat.cpp` and `MeleeWeaponModel.cpp` are excluded because they are absent from the retail `Game_ServerShell.vcproj`.

The public LithTech snapshot predates many F.E.A.R. SDK 1.08 contracts. M29AY now supplies central compatibility for command/class/property metadata, FEAR property types/flags, `LTOBB`/`LTSphere`, ObjectBank, real client-object lookup, shadow LOD, global SFX broadcast, FEAR GenericProp helpers, ObjectCreateStruct physics/child-model fields, C++17 allocator/template fixes, NavMesh geometry helpers, model animation keyframe/node transforms, real-time server milliseconds, HMODELANIM message serialization, vector clamp, and other signature adapters. The compatibility is based on published F.E.A.R. SDK 1.08 contracts rather than per-callsite gameplay stubs.

The last completed full ARM/Vita pass reached the **AI weapon block at approximately 374/533**. Everything before that — including AI actions/goals, NavMesh generation/links, nodes, path manager, sensors, sounds, squads, states and target-selection — compiled. The three API deltas exposed there (`GetRealTimeMS`, HMODELANIM message IO and `TVector3::Clamp`) are now implemented, which triggered a new full validation rebuild. **ObjectDLL has not yet completed all 533 TUs, the final executable has not yet linked, and there is no M29AY VPK/hardware validation yet.**

For a new chat, use branch `m29ay-objectdll-world-runtime` and read `CURRENT_STATE_M29AY.txt` plus `M29AY_PROGRESS_2026-09-11.md`. Recreate the pinned upstream, apply `lithtech-overlay/`, configure with `FEARVITA_MENU_LINK_ONLY=OFF`, and continue `fearvita_fear_server_objects`. After 533/533, build the complete executable, resolve link/runtime dependencies, instantiate `Worlds\\Release\\Intro`, wire the real local start-level flow, produce a private VPK and test FEAR/EP/PM on hardware.
