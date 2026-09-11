# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AY  
**Date:** 2026-09-11

The three-game frontend milestone remains hardware-proven: **F.E.A.R.**, **Extraction Point** and **Perseus Mandate** reach their retail menus with the canonical M29AW Vita gameplay controls and the M29AX D-pad/front-touch menu navigation.

Fresh M29AX hardware logs place all three campaigns at the same next frontier: campaign data selection and the local `StartGame` path succeed, then execution needs the real **ObjectDLL/server/world runtime**. M29AY therefore develops one shared server/runtime foundation for all three games instead of advancing only the base campaign.

M29AY also extends the FEARVita-authored German intro/loading fallback to campaign tags `fear`, `ep` and `pm` for `Worlds\\Release\\Intro`. The common labels are `INTERVALL 01` and `EINFÜHRUNG`, with campaign-specific FEARVita briefing text. These strings are not claimed as official retail German localization.

The pinned upstream remains `jsj2008/lithtech` commit `0eab18289bed72879eddb648d3311075b108cf46`. The Vita ObjectDLL target is aligned to the original retail server project and currently contains **533** translation units with `_FINAL=1`; `AIGoalGotoCombat.cpp` and `MeleeWeaponModel.cpp` are excluded because they are not part of the original `Game_ServerShell.vcproj`.

The public LithTech snapshot predates several F.E.A.R.-specific SDK interfaces. M29AY is restoring those contracts against the existing runtime using the published **F.E.A.R. SDK 1.08** as the reference. Implemented compatibility already includes command/class/property metadata, `LTOBB`, ObjectBank mapping, a real `ILTServer::GetClientObject`, shadow-LOD compatibility, global SFX broadcast, FEAR-style GenericProp accessors, reference-form server calls, ObjectCreateStruct physics/child-model handling, scalar `LTIsNaN`, the C++17 `CRange<T>` fix and `LTIntersect::Point_Segment_DistSqr`.

The ARM ObjectDLL compile now passes `AI.cpp` and the previous `AIActionGotoValidPosition.cpp` blocker and is advancing incrementally through the AI action/activity sources. **There is not yet a complete ObjectDLL link or an M29AY VPK.**

For a new chat, start with branch `m29ay-objectdll-world-runtime` and read `CURRENT_STATE_M29AY.txt`, `M29AY_PROGRESS_2026-09-11.md` and `patches/M29AY.patch`. Continue the ARM target `fearvita_fear_server_objects` from its first compiler error, then link the server/runtime, instantiate `Worlds\\Release\\Intro`, and validate the same runtime path for FEAR/EP/PM on hardware.
