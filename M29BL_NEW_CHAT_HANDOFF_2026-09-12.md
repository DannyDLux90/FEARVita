# FEARVita new-chat handoff — M29BL WIP / M29BK hardware baseline

Date: 2026-09-12

## Important status

The source tree in this snapshot is **M29BL WIP / package marker 0.09**. It contains the started authentic local-client/player handoff work described below.

The binaries currently present in `m29ay_build/` are still the **last verified M29BK / 0.08 build**. M29BL has not been rebuilt or hardware-tested yet. A rebuild was attempted in the previous chat, but CMake regeneration stopped before compilation because the temporary `/mnt/data/vitasdk_m29ay` toolchain mount was no longer present in that runtime. This is not evidence of a source compile error.

The last hardware-verified installable VPK is:
`FEARVita_M29BK_0.08_NAVMESH_ABI_COMPLETE_2026-09-12.vpk`

## Last verified hardware frontier: M29BK / 0.08

M29BK is the first build that loads the real F.E.A.R. Intro world completely without crashing.

Base F.E.A.R. hardware log (`fear_fear(6).log`) proves:
- World object list reaches object index 1987 (all 1,988 objects).
- Retail loading progress reaches 100%.
- `Loaded world: Worlds\\Release\\Intro` completes.
- NavMesh ABI preflight is exact: 67,492 bytes consumed out of 67,492, 557 edges, 244 polys, enum width 4, edge size 72.
- `DoRunWorld completed`.
- `[server-world] do-start-world ok world=Worlds\\Release\\Intro`.
- `[ingame-start] server-world result=0`.
- `[ingame-start] preload FinishStartGame result=1`.
- After that, the retail main loop continues for many thousands of frames, but the loading screen does not transition into the Intro. There is no crash.

Extraction Point and Perseus Mandate hardware logs show the same successful 100% / NavMesh / `do-start-world ok` / `FinishStartGame result=1` frontier.

Therefore the current blocker is **not world loading or NavMesh anymore**. It is the authentic local client/server handoff after the server world has successfully started.

## M29BL WIP goal

Do **not** fake `GS_PLAYING` and do not fabricate a successful intro. The goal is to restore the original local-client flow:

1. Create a genuine server-side local LithTech `Client` when `STARTGAME_NORMAL` prepares the local server.
2. Preserve/copy the original `StartGameRequest` client data into the server client.
3. Route Vita `ILTClient::SendToServer` messages into the real server/ObjectDLL message path.
4. Route safe server-to-client control/state messages into `CGameClientShell::OnMessage`.
5. Detect when the real server client is in-world and has a genuine server-side player object.
6. Expose a Vita local client proxy for `GetClientObject()` without leaking server LTObject pointers into the client object namespace.
7. Call the stock client `OnEnterWorld()` at the authentic engine transition point, then let FEAR's own loading / client-connection state machine acknowledge Loading -> InWorld and leave the loading screen.

## M29BL WIP files already modified

Compared with the M29BK workspace, current M29BL WIP modifies:

Project/integration:
- `m29ay_src/project/CMakeLists.txt` — package version bumped to 00.09.
- `m29ay_src/project/src/main.cpp` — runtime marker bumped to M29BL / authentic local client + player handoff.
- `m29ay_src/project/integration/lithtech/fearvita_iltclient_vita.cpp`
- `m29ay_src/project/integration/lithtech/fearvita_menu_runtime_gate.cpp`
- `m29ay_src/project/integration/lithtech/fearvita_runtime_server_bridge.h`
- `m29ay_src/project/integration/lithtech/fearvita_runtime_server_platform_vita.cpp`

LithTech runtime server:
- `m29ay_lithtech/lithtech-master/runtime/server/src/s_client.cpp`
- `m29ay_lithtech/lithtech-master/runtime/server/src/serverde_impl.cpp`

The key WIP additions already present include:
- `FearVita_RuntimePrepareLocalServer(..., client_data, client_data_len)`.
- `FearVita_RuntimeSendLocalClientMessage(...)`.
- `FearVita_RuntimeLocalClientEngineInWorld()`.
- `FearVita_RuntimeGetLocalServerPlayer()`.
- `FearVita_ClientReceiveServerMessage(...)`.
- `FearVita_PumpLocalClientWorldHandoff()` called once per retail frame after the local server update.
- Vita `ILTClient::SendToServer` now attempts to pass real messages to the local server rather than only logging/discarding them.
- A client-local player proxy is allocated only after a genuine server player exists; then the stock `CGameClientShell::OnEnterWorld()` is invoked. No game state is forced.

This code is **WIP and unverified** until rebuilt and run on Vita.

## Known separate compatibility frontier

F.E.A.R. `.Model00p` is a Jupiter EX `MODL!` container. M29BJ allowed the extension through the old model path, which revealed the real incompatibility:
`Model::Load Error Incorrect LTB file type (77)` / `ltb file type is not model type`.

This remains a major model-loader task, but it did **not** prevent M29BK from completing the server world load and is not the immediate reason the loading screen stays after 100%.

## Audio state

Audio is still not considered matched to PC by the user. The current backend does synchronous 48 kHz stereo hardware init, separate SFX/music/voice gains, and 44.1 -> 48 kHz polyphase resampling. It exports the decoded/resampled menu music to:
- `ux0:data/FEARVita/debug/IntroIntLp1v2.wav`
- `ux0:data/FEARVita/debug/IntroIntLp1v2_48k.wav`

Do not retune audio from phone recordings alone; use those exported WAVs for digital comparison when returning to the sound issue.

## Build/toolchain notes

Historically the build used a restored VitaSDK under `/mnt/data/vitasdk_m29ay` and these packages from the conversation:
- vitasdk-core 2026.08.1 x86_64-linux-gnu
- libvita2d r188
- freetype 2.14.3
- libjpeg-turbo 3.2.0
- libpng 1.6.58
- zlib 1.3.2

Historical compatibility symlinks used by CMake/build files:
- `/mnt/data/fear_ws -> <current workspace>`
- `/mnt/data/m29ay_src -> <workspace>/m29ay_src`
- `/mnt/data/m29ay_lithtech -> <workspace>/m29ay_lithtech`
- `/mnt/data/m29ay_build -> <workspace>/m29ay_build`

Before rebuilding M29BL in a fresh environment, restore the VitaSDK path above or reconfigure CMake with a valid VitaSDK path.

## GitHub baseline

Repository: `DannyDLux90/FEARVita`
Last fully secured/verified branch before this WIP snapshot:
`m29bk-navmesh-abi`

Current WIP branch:
`m29bl-wip-local-client-handoff`

The exact M29BK -> M29BL-WIP source delta is stored under `recovery/` on this branch. VPKs, retail game data, proprietary assets and local build artifacts are intentionally not committed.

## Recommended first actions in the new chat

1. Read this handoff and inspect the M29BL WIP diff against M29BK.
2. Restore VitaSDK and rebuild M29BL completely (`FEARVita`, VELF, FSELF/eboot).
3. Resolve any compile/link errors in the local-client bridge without replacing the authentic FEAR state machine with a fake state.
4. Package from the known complete 22-payload-file VPK layout, bump/retain APP_VER 00.09, and verify embedded EBOOT byte-for-byte.
5. Hardware test only base F.E.A.R. -> New Game -> Medium.
6. Look for `[local-handoff]` messages, especially client creation, client->server state messages, server->client `MID_CLIENTCONNECTION`, real server player availability, and `client-on-enter-world complete`.
7. If the loading screen closes, continue into the real Intro and then address Model00p/rendering as the next major frontier.
