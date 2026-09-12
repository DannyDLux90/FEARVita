# FEARVita M29BL build checkpoint — 2026-09-12

## Goal

Continue from M29BK/0.08's verified 100% Intro world load and restore the authentic local LithTech client/server handoff so stock FEAR can leave the loading screen and enter `Worlds\\Release\\Intro` without forcing `GS_PLAYING`.

## Source basis

Authoritative input was `FEARVita_M29BL_WIP_WORKSPACE_NEW_CHAT_2026-09-12` / `FEARVita_M29BL_WIP_SOURCE_FULL_NEW_CHAT_2026-09-12`, package marker 00.09.

## Toolchain restoration

Restored VitaSDK under `/mnt/data/vitasdk_m29ay` using vitasdk-core 2026.08.1, libvita2d r188, freetype 2.14.3, libjpeg-turbo 3.2.0, libpng 1.6.58, and zlib 1.3.2. Historical workspace symlinks were restored (`/mnt/data/fear_ws`, `/mnt/data/m29ay_src`, `/mnt/data/m29ay_lithtech`, `/mnt/data/m29ay_build`).

## Compile fix

The first M29BL rebuild reached compilation and exposed one source access-control error:

```text
fearvita_iltclient_vita.cpp:817: CGameClientShell::OnMessage is protected
```

The bridge now dispatches through the public `IClientShell` base interface:

```cpp
static_cast<IClientShell*>(g_pGameClientShell)->OnMessage(pMsg);
```

This preserves virtual dispatch to the real `CGameClientShell::OnMessage` implementation. No game state is forced and no server LTObject pointer is exposed to the client object namespace.

## Build result

`cmake --build /mnt/data/fear_ws/m29ay_build --target FEARVita.vpk -j2` completed successfully and produced FEARVita, VELF, FSELF/`eboot.bin`, and VPK outputs.

Fresh build SHA-256:

- `FEARVita`: `41906cbe2359aa5972665f6ffaa6901817e5308027ba18c3867d16b40a17895c`
- `FEARVita.velf`: `15700ba8d8de1d17ef591ae4b52af128a3f41f1e4a51f88b1c4748b42c83e850`
- `eboot.bin`: `1372d2771f6630ce33ce4eea1ba5876ee1c46a50b600e972846c76fe0f2c46b9`

## Full installable VPK

The CMake-produced VPK contains only the core 12 files, while the hardware-verified M29BK installable layout contains 22 payload files. M29BL was therefore repackaged from the verified M29BK layout, replacing only `eboot.bin` with the fresh M29BL FSELF and `sce_sys/param.sfo` with the fresh 00.09 SFO.

Final test VPK: `FEARVita_M29BL_0.09_LOCAL_CLIENT_HANDOFF_2026-09-12.vpk`

SHA-256: `8a5085a4752ebb8e50acd44df05a575c5af648d66e9eddb1427d0ab68e8a565b`

Validation: 22 non-directory payload files; APP_VER `00.09`; TITLE_ID `FEAR00001`; embedded `eboot.bin` is byte-identical to the fresh build; every payload other than `eboot.bin` and `sce_sys/param.sfo` is byte-identical to the verified M29BK/0.08 VPK.

## Static handoff review

The WIP follows the stock FEAR single-player state path:

1. `STARTGAME_NORMAL` creates a real local server-side LithTech `Client`.
2. Single-player `ServerConnectionMgr::OnAddClient` enters `LoggedIn`, then `Loading`.
3. `FinishClientConnect` drives the engine client into the world once the server world is running.
4. `CGameServerShell::OnClientEnterWorld` creates/attaches the real `CPlayerObj`.
5. The Vita frame pump waits for engine `CLIENT_INWORLD` plus a real server player, creates only a client-local proxy, then invokes stock `CGameClientShell::OnEnterWorld()`.
6. Stock FEAR sets `m_bInWorld`, its loading-state update sends the real `eClientConnectionState_Loading` acknowledgement, the server advances through `Loaded` to `InWorld`, and the client can hide the loading screen.

No `GS_PLAYING` or connection state is fabricated by the Vita bridge.

## Hardware test

Test only Base F.E.A.R. -> New Game -> Medium first. Useful diagnostic sequence:

```text
[local-handoff] server-client-ready ...
[local-handoff] server-to-client msg=245 connection-state=...
[server-world] do-start-world ok world=Worlds\\Release\\Intro
[local-handoff] engine-client state=... player=1
[local-handoff] client-on-enter-world begin ...
[local-handoff] client-on-enter-world complete
[local-handoff] client-to-server msg=245 ...
[local-handoff] server-to-client msg=245 connection-state=...
```

If the loading screen still remains, the next hardware log should show exactly which connection-state edge is missing. If it closes, the next major frontier is client-side world/object/model rendering (`.Model00p` / Jupiter EX `MODL!`).
