# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AX  
**Date:** 2026-09-11

The three-game frontend/menu-video milestone is complete on real PS Vita hardware: **F.E.A.R.**, **Extraction Point** and **Perseus Mandate** reach their retail menus and play their original animated menu backgrounds with retail menu music/UI sounds.

M29AV hardware testing proved the base-game loading state machine now reaches `FinishStartGame`, accepts the Vita `STARTGAME_NORMAL` local-session bridge and advances to the explicit `waiting-for-world/server-object-runtime` frontier. The remaining blocker to entering the first mission is therefore the real FEAR ObjectDLL/server/world runtime rather than ScreenPreload.

M29AW makes the Killzone-inspired Vita control map the canonical default profile for all three campaigns. **Restore Defaults** loads exactly this map; leaving the PC-oriented Configure screen can no longer erase the Vita symbolic bindings. The layout includes both the front touchscreen and rear touchpad.

M29AX keeps that gameplay map unchanged and adds frontend-specific input routing. The physical D-pad is translated to matching retail UI directions in `GS_SCREEN` and `GS_MENU`, and front-touch coordinates/press edges are passed through the existing `CInterfaceMgr` mouse hit-testing path. Gameplay touch zones remain flashlight/melee/next-weapon.

The Vita Bubble manual has been refreshed from the old M16 four-page manual to a five-page current guide. It documents installation/data layout, selector behavior, per-campaign logs and the complete default control map. The pages are reproducible with `project/tools/generate_vita_manual.py`.

The current Steam distribution of F.E.A.R. exposes English game-interface data. M29AW/M29AX therefore use a FEARVita-authored German fallback for the first **base-game** load screen when the Vita system language is German; it does not claim those strings are official retail German localization and does not apply base-game text to EP or PM. Loading diagnostics now report mission, level, briefing and help StringDB ids so later expansion localization can be implemented against the real ids.
