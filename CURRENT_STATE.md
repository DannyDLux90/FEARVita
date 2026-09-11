# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AU  
**Date:** 2026-09-11

The three-game frontend/menu-video milestone is complete on real PS Vita hardware: **F.E.A.R.**, **Extraction Point** and **Perseus Mandate** all reach their retail menus and play their original animated menu backgrounds with retail menu music/UI sounds. Vita-system-language localization is restored and the accepted frontend presentation remains unchanged.

M29AT hardware testing proved the first single-player world path is now selected correctly in all three campaigns. F.E.A.R., Extraction Point and Perseus Mandate each resolve `Worlds\\Release\\Intro`, confirm the world exists, reset the player camera and switch successfully to `ScreenPreload`. The separate per-campaign logs (`fear_fear.log`, `fear_ep.log`, `fear_pm.log`) are working as intended.

The M29AT stall was not a missing world file. The Vita frontend optimization intentionally skipped `CScreenMgr::UpdateInterfaceSFX()` on all retail screens to avoid still-partial ClientFX/model services. `CScreenPreload::UpdateInterfaceSFX()` is special, however: it drives the mission start state machine (`FinishStartGame` -> `StartClientServer` -> client loading handshake). Because that update was skipped, all three campaigns remained on ScreenPreload while the outer retail loop continued indefinitely.

M29AU preserves the stable frontend behavior for normal screens but enables retail `UpdateInterfaceSFX()` for the state-machine screens `SCREEN_ID_PRELOAD` and `SCREEN_ID_POSTLOAD`. The next hardware target is therefore to move beyond preload into `FinishStartGameFromLevel`, the local `STARTGAME_NORMAL` bridge and the real server/world-runtime frontier.

The Weapons options priority editor from M29AT is retained: X selects a weapon, Left/Right reorders it, and the existing retail profile save/apply path persists the list.

The full FEAR ObjectDLL/server runtime is still not claimed complete. M29AU is an authentic loading-state handoff checkpoint intended to expose the next real ObjectDLL/world-loading blocker rather than mask it.
