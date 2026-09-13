# FEARVita M29CL / 0.34 current state — 2026-09-13

## Current canonical local state

- Workspace root: `/mnt/data/fear_work`
- Project source: `/mnt/data/fear_work/m29ay_src`
- LithTech runtime tree: `/mnt/data/fear_work/m29ay_lithtech/lithtech-master`
- Build tree: `/mnt/data/fear_work/m29ay_build`
- VitaSDK used for the successful current conversion/link flow: `/mnt/data/vitasdk_m29bu`
- Current milestone/version: **M29CL / 0.34**
- Current VPK: `/mnt/data/FEARVita_0.34_M29CL.vpk`
- Current source snapshot: `/mnt/data/FEARVita_0.34_M29CL_Source.zip`
- Current linked ELF: `/mnt/data/FEARVita_M29CL_0.34.elf`
- Current EBOOT: `/mnt/data/FEARVita_M29CL_0.34_eboot.bin`
- Current SFO: `/mnt/data/FEARVita_M29CL_0.34_param.sfo`

SHA-256:
- VPK `5142634839655bc6bff276cf6360fec5b6ec8f29bcefb8ac01f3fbdb67cd0a62`
- Source snapshot `b6a0ce45729597eff6f390d1589e11c69739e8268b7f89ace264a1721fb90209`
- ELF `bf3646ebc120333590bcfb162bdc628652ec843ad09b068a31fbe9eee2bfed4f`

## Last hardware-tested build and evidence

Last hardware test was M29CK / 0.33. It proved the previous Model00p, monolithic-scope, SharedFXStructs and PlayerBody gates were crossed. Both campaigns reach `player-local-model-ok`; PlayerBody reaches filenames/animations/physics/reset-complete and `player-local-init-complete`; Extraction Point reaches ScreenPostload and the real `ClientInWorld` send attempt.

Remaining 0.33 crash classes:
- Data abort in `ClientConnectionMgr::SendClientInWorldMessage()` because `g_pLTGameUtil == NULL` at `WriteServerKeyData`.
- `std::bad_alloc` for a normal `0x00400000` byte texture decode allocation in `CVitaTextureMgr::CreateTextureFromFile`, reached from `CScreenPostload::OnFocus`.
- `vitaGL.log` contains normal GLSL translation and no renderer/GPU error signature near the crash.
- `client-player-characterfx-create-failed` remains visible and must be localized, not bypassed.

## M29CL / 0.34 changes

- Keeps stock `ILTGameUtil` when present; only for Vita local singleplayer when unavailable, client/server use a paired raw `uint32` world-CRC fallback in the same ClientInWorld wire slot. Multiplayer refuses the fallback. No connection state or `GS_PLAYING` is forged.
- Adds normalized-filename shared texture caching/refcounting for file-backed FakeTexture objects.
- Catches remaining decode `bad_alloc` and degrades only that texture to a transparent 1x1 fallback instead of terminating the process.
- Adds CharacterFX stage diagnostics plus postload/texture/gameutil fallback markers.

## Non-negotiable architecture rules

- authentic local-client flow only; real server-side player.
- preserve StartGameRequest and stock postload ClientInWorld flow.
- server/client player objects remain separate; separate native client ModelInstance proxy.
- real CharacterFX SFX create message; stock OnEnterWorld.
- stock state machine must reach `GS_PLAYING`; never force it.
- no model-less/fake player.
- generic MID_SFX_MESSAGE (231) remains dropped except explicitly parsed/retargeted safe local-player subtypes.
- no broad unsafe HOBJECT forwarding.

## Immediate 0.34 hardware-test ladder

1. startup `FEARVita 0.34 / M29CL`.
2. `player-local-model-ok`.
3. `player-body-reset-complete` and `player-local-init-complete`.
4. inspect `characterfx-stage ...`.
5. inspect `postload background-texture=...`, `texture-cache hit`, and any `texture-load oom-fallback`.
6. at retail ClientInWorld send, expect `client-inworld-gameutil-fallback raw-worldcrc` only when ILTGameUtil is absent.
7. server paired `server-inworld-gameutil-fallback raw-worldcrc`.
8. then Respawn, `player-state-alive-enter/complete`, stock `ChangeState(GS_PLAYING)`.

Do not claim Vita gameplay success until new hardware logs prove it.

GitHub handoff branch: `m29cl-0.34-handoff`, based on M29BW commit `5cd48609d9a01e452e1212c0f93e8713fd933436`. Source/docs only; no VPK, private game assets or coredumps are committed.
