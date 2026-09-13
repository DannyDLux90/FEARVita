# FEARVita M29BW / 0.19 WIP checkpoint — 2026-09-13

## Status

M29BW is an **in-progress checkpoint**, not a hardware-tested release. It was created directly from the clean M29BV/0.18 workspace so that older reconstructed-tree regressions are not reintroduced.

M29BV/0.18 itself was cleanly rebased on the hardware-proven M29BS/0.16 baseline. Against M29BS, its intended runtime changes were limited to:
- `runtime/model/src/model_load.cpp` — typed Jupiter EX Model00p physics-shape parser.
- `FEAR/ClientShellDLL/InterfaceMgr.cpp` — retail postload diagnostics.
- `FEAR/ClientShellDLL/ScreenPostload.cpp` — retail press-any-key diagnostics.

No old `world_shared_bsp`, `classbind`, `servermgr`, SDK timer, SurfaceDB, or similar reconstructed-tree regressions should be reintroduced.

## Last hardware result (M29BT / 0.17)

The retail world reaches 100% and `DoStartWorld` succeeds. The real local client exists, but `PLAYER.MODEL00P` fails in the old ambiguous physics-shape solver and `ServerShell::OnClientEnterWorld` returns `LTNULL`, leaving `player=0`. The original postload/press-any-key screen therefore cannot be reached yet.

The 0.17 diagnostics proved that the old field labelled `node` at byte 41 is actually the Jupiter EX shape type. The observed player sequence starts with values `7 -> 6 -> 3`, matching the typed parser design and the independent FEAR Model00p reader evidence.

## M29BV / 0.18 parser/postload work

The brute-force 57/81 boundary solver was replaced with a typed Model00p physics-shape parser. The goal remains strict: do not bypass the player model, do not make a model-less player, and do not force `GS_PLAYING`.

The original retail postload path was traced and instrumented. Intended flow:

`real OnClientEnterWorld player -> client InWorld state -> SCREEN_ID_POSTLOAD -> IDS_PRESS_ANY_KEY -> Cross/VK_RETURN -> SendClientInWorldMessage -> GS_PLAYING`

Cross already reaches `CScreenPostload::HandleKeyDown`, so no Vita-specific fake confirmation screen is required.

## M29BW / 0.19 current WIP goal

After the parser succeeds, the connectionless local-client path still needs an authentic client-side representation of the real server player. The current WIP adds a native client `ModelInstance` bridge that uses the same already-loaded/refcounted `Model*` as the real server player while keeping a separate client object for prediction. It also exposes the real saved server-player CharacterFX SFX message so the normal client `CCharacterFX` path can be used instead of inventing a fake player.

Current M29BW differences relative to M29BV are intentionally limited to these source files:
- `m29ay_src/project/CMakeLists.txt` — version 00.19.
- `m29ay_src/project/src/main.cpp` — M29BW startup markers.
- `m29ay_src/project/integration/lithtech/fearvita_iltclient_vita.cpp` — native local-player/client-model bridge WIP.
- `m29ay_src/project/integration/lithtech/fearvita_runtime_server_bridge.h` — bridge API declarations.
- `m29ay_src/project/integration/lithtech/fearvita_runtime_server_platform_vita.cpp` — native client ModelInstance/SFX bridge implementation.

The `m29ay_lithtech/lithtech-master` runtime tree is unchanged between M29BV and M29BW.

## Critical build warning

The files currently present in `m29ay_build/` inside the M29BW workspace were inherited from the successful M29BV build cache. They predate the current M29BW/0.19 native client-model changes and **must not be treated as a valid 0.19 build or test VPK**. A rebuild is required after this checkpoint is resumed.

## Non-negotiable implementation rules

- Keep the real `CGameServerShell::OnClientEnterWorld` path.
- Keep the real player model; never bypass Model00p loading.
- Do not force client state or `GS_PLAYING`.
- Do not substitute a fake/model-less player.
- Preserve the M29BS v113 world loader and all M29BS connectionless-local-client null-safety fixes.
- Keep server and client player objects separate as in normal LithTech prediction; sharing the loaded `Model*` is acceptable, sharing the server `LTObject` as the client object is not.
- Do not broadly forward server messages containing raw `HOBJECT` values until proper client object mapping exists.

## Resume checklist

1. Re-verify `diff -qr` M29BV -> M29BW before changing anything.
2. Compile the five M29BW source changes using the M29BV build cache or do a clean build.
3. Resolve compile/ABI issues only in the Vita integration layer unless evidence requires a runtime change.
4. Verify final ELF still contains M29BS `LoadJupiterEx113`, local-client dispatch, and `m_ConnectionID` null-safety.
5. Verify typed Model00p parser and postload markers in the final ELF.
6. Hardware test Base F.E.A.R. first. Required evidence before calling it successful: Model00p `runtime-model-ready`, real player returned by `OnClientEnterWorld`, client reaches retail postload screen, Cross acknowledges it, and the game enters normal gameplay.
