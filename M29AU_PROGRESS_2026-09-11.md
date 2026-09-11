# M29AU progress — Preload state-machine handoff

## Hardware result from M29AT

All three campaigns now reach the same first single-player load seam on Vita:

- F.E.A.R.: `Worlds\\Release\\Intro` exists and `ScreenPreload` becomes active.
- Extraction Point: same virtual intro path resolves through the campaign overlay and reaches `ScreenPreload`.
- Perseus Mandate: same virtual intro path resolves through the campaign overlay and reaches `ScreenPreload`.

The separate per-campaign logs are working as intended.

## Root cause of the M29AT preload stall

The Vita frontend milestone intentionally bypassed `CScreenMgr::UpdateInterfaceSFX()` for all frontend screens because normal retail screen SFX can enter still-partial ClientFX/model-rendering services.

That optimization is valid for ordinary menu screens, but `CScreenPreload::UpdateInterfaceSFX()` is not merely visual. It drives the mission start state machine:

`FinishExitLevel()` -> `FinishStartGame()` -> `FinishStartGameFromLevel()` -> `StartClientServer()` -> client loading handshake.

Because Vita skipped `UpdateInterfaceSFX()` globally, all three campaigns sat forever on `ScreenPreload` while the outer retail loop kept running.

## M29AU change

On Vita, normal frontend screens still bypass interface-SFX updates, preserving the stable menu milestone. Only the state-machine screens:

- `SCREEN_ID_PRELOAD`
- `SCREEN_ID_POSTLOAD`

are allowed to call the retail `UpdateInterfaceSFX()` path.

This should make the existing M29AT diagnostics become active:

- `preload-screen update-enter`
- `finish-start world=...`
- `ingame-connection start-single-player enter`
- `ingame-client start-game ... accepted`
- `client-handshake ok; waiting-for-world/server-object-runtime`

The build still does not claim a working ObjectDLL/server/world runtime. M29AU is the next authentic loading-state handoff and is expected to expose the first server/world blocker after preload.

## Hardware test

Start F.E.A.R. -> Single Player -> New Game -> choose a difficulty and let it continue.

Copy only `ux0:data/FEARVita/fear_fear.log` afterward. If a crash occurs, also copy the new core dump.

EP and PM do not need to be repeated until the base game advances beyond this seam; M29AT already proves that all three campaigns reach the same preload state.
