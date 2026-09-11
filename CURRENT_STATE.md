# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AT  
**Date:** 2026-09-11

The three-game frontend/menu-video milestone is complete on real PS Vita hardware: **F.E.A.R.**, **Extraction Point** and **Perseus Mandate** all reach their retail menus and play their original animated menu backgrounds with retail menu music/UI sounds. The Vita-system-language overlay is restored and was confirmed German on hardware in M29AS.

M29AT begins the next milestone: advance from the retail menu into a real single-player session while keeping the accepted frontend unchanged.

Diagnostics are now split so one campaign never overwrites another: `fear_launcher.log`, `fear_fear.log`, `fear_ep.log`, and `fear_pm.log` under `ux0:data/FEARVita/`.

The Weapons options screen now has Vita-native priority editing. X selects a weapon; Left/Right moves that selected weapon up/down in the retail priority list. The existing profile save/apply path is retained.

For New Game, the Vita ILTClient now accepts a **local `STARTGAME_NORMAL` session shim only** instead of returning `LT_UNSUPPORTED`. The client can therefore proceed through first mission/world selection, preload and the local StartGame seam. The full FEAR ObjectDLL/server transport is still not online, so M29AT intentionally defers `MID_START_GAME` / `MID_START_LEVEL` CAutoMessages and logs the exact point where the real world/server-object runtime is still required. This checkpoint does **not** claim playable gameplay yet.

A separate ObjectDLL compile probe confirms the next server milestone still has real portability work: FEAR server-object property macros and several server-side SDK/API contracts differ from the currently exposed open runtime interfaces.

Next hardware step: base F.E.A.R. -> Single Player -> New Game -> choose difficulty, then collect `ux0:data/FEARVita/fear_fear.log` and any core dump. That trace decides the next ingame implementation seam.
