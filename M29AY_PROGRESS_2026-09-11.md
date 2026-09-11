# FEARVita M29AY — ObjectDLL / world-runtime progress

Date: 2026-09-11

M29AY builds on the hardware-proven M29AX frontend and targets the first real in-world single-player execution for **F.E.A.R., Extraction Point and Perseus Mandate**.

## Three-campaign parity

Hardware logs place all three campaigns at the same frontend/start frontier. M29AY therefore advances one shared ObjectDLL/server/world layer. The German Vita intro fallback also now covers `fear`, `ep` and `pm` with shared labels plus campaign-specific FEARVita briefing text.

## Retail ObjectDLL alignment

The server target is aligned to the original `Game_ServerShell.vcproj`, not a blind ObjectDLL glob. It contains 533 retail translation units, is built with `_FINAL=1`, and excludes two confirmed non-retail/orphaned files: `AIGoalGotoCombat.cpp` and `MeleeWeaponModel.cpp`.

## Compatibility work completed

The older public LithTech/Jupiter snapshot is being extended against published F.E.A.R. SDK 1.08 contracts. Completed areas include:

- FEAR class/property/command metadata and property accessors/setters;
- `IAggregate` type-name contract;
- FEAR geometry helpers (`LTOBB`, `LTSphere`, segment/OBB/AABB tests);
- NavMesh compile compatibility and C++17 allocator corrections;
- FEAR model animation keyframe/node-transform helpers;
- physics visibility node fallback;
- client/server object accessors, object transform/position helpers, shadow LOD compatibility;
- server game-time/real-time millisecond helpers;
- HMODELANIM message serialization and vector clamp;
- SFX save/load message support and SFX message readback;
- FEAR 32-bit unguaranteed per-object payload wired into object state, server packet serialization and client receipt;
- newer object-created callback carrying `GenericPropList` actually dispatched by the server;
- GameSpy/PunkBuster/content-transfer/UDP source compatibility for offline Vita SP;
- GUID and WorldEdit/WorldPacker SDK contracts;
- Light object API compatibility;
- ObjectTemplate scalar/uniform-scale serialization bridge;
- safe treatment of unsupported new engine features (`GetSectorID` not found; delayed-client-visible no-op due old-bit collision).

## Confirmed ARM/Vita milestones

The following important blocks/TUs compile under the Vita ARM toolchain:

- AI actions, activities, goals, NavMesh generator/link types, nodes, PathMgr, sensors, states and target selection;
- `AIStimulusMgr`, AI weapons/world state;
- `ActiveWorldModel`, `BanUserMgr`, CTF objects;
- `Character`, `CharacterHitBox`, `CommandMgr`;
- `DEditHook`;
- destructibles/dialogue/display objects;
- `Door`, `DynamicSectorVolume`;
- `GameBase`, `GameServerShell`;
- `GameStartPoint`, `GameStartPointMgr`, `GameWorldEditImpl`, `GameWorldPackerImpl`;
- `KeyFramer`, `KeyframeToRigidBody`;
- current Light object family;
- `NavMarker`, `ObjectTemplateMgr`, `PickupItem`;
- `PlayerInventory`, `PlayerLeash`, `PlayerLure`, `PlayerNodeGoto`;
- **`PlayerObj.cpp`**.

A complete validation run of `fearvita_fear_server_objects` now finishes **533/533 with Ninja rc=0**. The ObjectDLL compile phase is therefore complete. The full `FEARVita` target is the active frontier. Its first client-side regression was caused by FEAR `LT_PT_COMMAND`/`LT_PT_STRINGID` being visible only through the server PCH; M29AY now defines those compatibility values at the shared `ltproperty.h` layer so both ClientShell and ObjectDLL use the same contract. Client compilation proceeds beyond that point. A later ClientShell regression where `compat/ltintersect.h` referenced `LTOBB` without explicitly including `ltobb.h` is also fixed; the full target proceeds beyond that point.

## Current next phase

With `fearvita_fear_server_objects` fully clean at 533/533, complete the full ClientShell/shared/executable build and then link the ObjectDLL together with the real portable runtime/server/world implementation. The target must use the existing VFS-capable server file manager and static class binding, then replace the temporary Vita `StartGame` local-session shim with the real local server/world path.

Target world path: `Worlds\\Release\\Intro`.

## Critical runtime caveats

- Verify actual FEAR world-property decoding; FEAR 1.08 property numbering differs from the older public SDK.
- Verify physics-group application during object creation.
- Root-node physics visibility is a fallback pending newer model metadata.
- Jupiter-EX sector visibility IDs are not present in the old runtime.
- Some newer light metadata has no exact old-renderer representation.

## New-chat continuation

Read `NEXT_CHAT_M29AY.md` first, then `CURRENT_STATE_M29AY.txt`. Continue the ARM target from the first actual error. Do not regress the existing menu/gameplay controls, do not fake an ingame state, and keep FEAR/EP/PM on the same runtime level.
