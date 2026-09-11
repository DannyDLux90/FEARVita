# FEARVita M29AY — New-chat handoff

Use this file as the first entry point in a fresh ChatGPT session.

## Repository state

- Repository: `DannyDLux90/FEARVita`
- Branch: `m29ay-objectdll-world-runtime`
- Public app version remains `0.02`.
- Internal development checkpoint: `M29AY`.
- Last hardware-proven binary remains M29AX; M29AY is source/build work and is **not yet hardware validated**.

## Objective

Bring **F.E.A.R., Extraction Point and Perseus Mandate** into the real single-player world on Vita using one shared ObjectDLL/server/world implementation. All three currently reach the same accepted local `StartGame` frontier on real Vita logs.

Do not simulate success by forcing the client state to playing. The target is the genuine LithTech local-server path: local server startup -> `CServerMgr::DoStartWorld` -> load `.dat` world -> create server objects/ObjectDLL -> real client object -> normal start-level messages.

## Source pins

- LithTech: `jsj2008/lithtech` commit `0eab18289bed72879eddb648d3311075b108cf46`.
- F.E.A.R. SDK compatibility reference: `xfw5/Fear-SDK-1.08` commit `2fc3557b0037d5fe01ac607b907d4b8511b9e4b2`.

Apply the FEARVita `lithtech-overlay/` to the pinned LithTech tree before building.

## Build target and current milestone

The ObjectDLL target mirrors the original retail `Game_ServerShell.vcproj`: **533 server translation units**, `_FINAL=1`. `AIGoalGotoCombat.cpp` and `MeleeWeaponModel.cpp` are intentionally excluded because they are absent from the retail project.

Major confirmed ARM/Vita compile milestones include:
- full AI action/goal/NavMesh/node/path/sensor/state/target-selection blocks;
- `Character.cpp`, `CharacterHitBox.cpp`, `CommandMgr.cpp`;
- `GameServerShell.cpp`;
- `GameStartPoint*`, `GameWorldEditImpl`, `GameWorldPackerImpl`;
- `KeyFramer.cpp`;
- full current Light object block;
- `ObjectTemplateMgr.cpp`;
- **`PlayerObj.cpp` PASS**.

The ObjectDLL validation is complete: **533/533 retail server translation units compile for ARM/Vita and Ninja returned `rc=0`**. Do not spend the next chat redoing ObjectDLL bring-up unless a later shared-header change invalidates it.

The active build frontier is now the complete executable:

```sh
ninja -C build-vita -j6 FEARVita
```

The first full-build client failure (`LT_PT_COMMAND` / `LT_PT_STRINGID` not visible in ClientShell) is fixed in shared `ltproperty.h`. A later ClientShell failure where `compat/ltintersect.h` referenced `LTOBB` without explicitly including `ltobb.h` is also fixed. The current full ClientShell rebuild proceeds beyond that point; rerun the full target and continue from the first actual remaining ClientShell/shared/link error.

## High-value compatibility decisions already made

1. Use published FEAR SDK 1.08 contracts for missing API signatures; avoid per-callsite fake gameplay stubs.
2. FEAR/EP/PM share the same runtime foundation.
3. German addon loading/mission fallback is already adapted for all three campaign tags.
4. `GetSectorID` returns `LT_NOTFOUND`; the old runtime has no Jupiter-EX sector table. Never synthesize IDs.
5. `FLAG_DELAYCLIENTVISIBLE` is no-op on Vita because FEAR's bit value collides with a different old-runtime flag.
6. GameSpy/PunkBuster/content-transfer/UDP pieces are offline/unavailable for Vita SP.
7. FEAR uniform template scale maps to old `LTVector` scale without changing the old object ABI.
8. The Player Pitch/Roll unguaranteed payload has been wired end-to-end in the old networking structures.
9. New `OnObjectCreated(GenericPropList*, reason)` must actually be dispatched by the server; this was added because otherwise world properties for newer classes would silently be skipped.

## After ObjectDLL compile (now complete)

The next large task is **not** another menu patch. Bring in the actual runtime/server/world core. Upstream `runtime/server/CMakeLists.txt` is the source-list reference. Create a Vita runtime-server target from the portable server/shared/world/model sources while replacing or excluding platform-specific Windows/Linux sys sources.

Useful existing FEARVita seams:
- `runtime/server/src/server_filemgr.cpp` already routes file access through FEARVita VFS.
- `runtime/shared/src/classbind.cpp` already has static-module support.
- `project/integration/lithtech/fearvita_iltclient_vita.cpp` still contains the temporary local-session `StartGameFn` shim and must be replaced/wired to the real server.

The real upstream flow to preserve is:
`CClientMgr::StartShell` -> local server `StartupLocal` -> `g_pServerMgr->DoStartWorld(worldName, LOADWORLD_LOADWORLDOBJECTS | LOADWORLD_RUNWORLD, ...)` -> server world file load -> object load -> real client object/start-level flow.

The first world is `Worlds\\Release\\Intro` and must come through FEARVita VFS from user-owned game data.

## Patch handoff

The canonical incremental M29AY patch is over 1 MB. The rescued workspace stores a gzip/base64 split representation with reconstruction metadata in `patches/M29AY_PATCH_RECONSTRUCT.md`.

Expected reconstructed patch SHA-256:

`9a499ec2fcd6300b6c6f843beb3066d0f2f51847b5c0160ac5c5aaf852c2df22`

The patch was independently verified with `git apply --check` against the M29AX baseline.

## Hardware policy

Do not publish or call M29AY successful until a new VPK is built and tested on real Vita for all three campaigns with fresh logs. Keep FEAR, EP and PM at the same runtime level.
