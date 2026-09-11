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

A full validation rebuild is/was running at handoff. The exact latest first error (or success) must be taken from the newest build log or by rerunning:

```sh
ninja -C build-vita -j6 fearvita_fear_server_objects
```

Do not infer 533/533 from the milestone list; require an actual `rc=0`.

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

## After ObjectDLL compiles

The next large task is **not** another menu patch. Bring in the actual runtime/server/world core. Upstream `runtime/server/CMakeLists.txt` is the source-list reference. Create a Vita runtime-server target from the portable server/shared/world/model sources while replacing or excluding platform-specific Windows/Linux sys sources.

Useful existing FEARVita seams:
- `runtime/server/src/server_filemgr.cpp` already routes file access through FEARVita VFS.
- `runtime/shared/src/classbind.cpp` already has static-module support.
- `project/integration/lithtech/fearvita_iltclient_vita.cpp` still contains the temporary local-session `StartGameFn` shim and must be replaced/wired to the real server.

The real upstream flow to preserve is:
`CClientMgr::StartShell` -> local server `StartupLocal` -> `g_pServerMgr->DoStartWorld(worldName, LOADWORLD_LOADWORLDOBJECTS | LOADWORLD_RUNWORLD, ...)` -> server world file load -> object load -> real client object/start-level flow.

The first world is `Worlds\\Release\\Intro` and must come through FEARVita VFS from user-owned game data.

## Patch handoff

The canonical M29AY incremental patch is too large for a single connector write, so GitHub stores a compressed/base64 split representation. Read `patches/M29AY_PATCH_RECONSTRUCT.md`. Expected reconstructed patch SHA-256:

`347014192e81f6aa96c4555352bd8652387530e3f93325ceb3d33b7c44307bf4`

The patch was independently verified with `git apply --check` against the M29AX source baseline.

## Hardware policy

Do not publish or call M29AY successful until a new VPK is built and tested on real Vita for all three campaigns with fresh logs. Keep FEAR, EP and PM at the same runtime level.
