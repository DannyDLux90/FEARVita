# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AY  
**Date:** 2026-09-11

M29AX remains the last hardware-proven frontend milestone: **F.E.A.R.**, **Extraction Point** and **Perseus Mandate** reach their retail menus on PS Vita with the canonical M29AW gameplay controls plus M29AX physical D-pad/front-touch retail-menu navigation.

M29AY advances all three campaigns together from the accepted local `StartGame` handshake into the real F.E.A.R. ObjectDLL/server/world runtime. Fresh Vita logs put FEAR/EP/PM at the same technical frontier, so the server/runtime foundation is shared; campaign-specific divergence is limited to archive/database/localization selection.

The FEARVita-authored German intro/loading fallback for `Worlds\\Release\\Intro` now covers campaign tags `fear`, `ep` and `pm`. It uses `INTERVALL 01`, `EINFÜHRUNG`, a German Vita control hint, and campaign-specific FEARVita briefing text. These strings are fallbacks and are not claimed as official retail German localization.

Pinned public LithTech upstream: `jsj2008/lithtech` @ `0eab18289bed72879eddb648d3311075b108cf46`. Published F.E.A.R. SDK 1.08 reference: `xfw5/Fear-SDK-1.08` @ `2fc3557b0037d5fe01ac607b907d4b8511b9e4b2`.

The Vita ObjectDLL target is aligned to the original retail `Game_ServerShell.vcproj`, uses `_FINAL=1`, and contains **533 retail server translation units**. `AIGoalGotoCombat.cpp` and `MeleeWeaponModel.cpp` are deliberately excluded because they are not part of the retail server project.

M29AY now restores a large part of the Jupiter-EX/F.E.A.R. 1.08 API surface against the older public runtime: FEAR property/class metadata, NavMesh/math helpers, model keyframe/node transforms, object/client/server helpers, SFX save/load messages, Player object unguaranteed Pitch/Roll payload transport, light/world/editor interfaces, GameSpy/content-transfer offline compatibility, C++17 allocator/template fixes, ObjectTemplate uniform-scale bridging, and the newer object-create/property callback path.

**Important current compile milestone:** `PlayerObj.cpp` now compiles successfully for ARM/Vita. The latest full ObjectDLL rebuild also passes the previously blocking Character/CharacterHitBox/CommandMgr, DEditHook, Door/DynamicSectorVolume, GameServerShell, GameStartPoint/GameWorldEdit/GameWorldPacker, KeyFramer and Light blocks. A handoff rebuild is still running through the remaining server objects; no final 533/533 completion or executable link is claimed yet.

There is **no M29AY VPK yet**. After the server target reaches 533/533, the next phase is to link the real server/world runtime into the Vita executable, replace the local-session shim with the real local server path, instantiate `Worlds\\Release\\Intro`, advance through the genuine start-level message flow, and then hardware-test FEAR/EP/PM at the same runtime level.

For a new chat, start from GitHub branch **`m29ay-objectdll-world-runtime`** and read, in order:
1. `NEXT_CHAT_M29AY.md`
2. `CURRENT_STATE_M29AY.txt`
3. `M29AY_PROGRESS_2026-09-11.md`
4. `patches/M29AY_PATCH_RECONSTRUCT.md` and the split compressed patch parts.
