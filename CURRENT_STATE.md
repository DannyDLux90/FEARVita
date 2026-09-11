# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AO  
**Date:** 2026-09-11

The launcher / loading flow and the F.E.A.R. base-game menu are accepted on hardware and should remain unchanged. M29AN also cleared the remaining frontend blocker for both expansions: Extraction Point and Perseus Mandate now reach `frontend-main-ok`, `complete`, engine init result 0 and enter their retail menus.

The remaining milestone item is now only the animated retail menu background for EP/PM. Hardware identifies the exact movies and cache targets:
- F.E.A.R.: `Videos\\Menu.bik` -> `video_cache/fear/videos/menu.mp4` (already working)
- Extraction Point: `VideosXP\\Menu.bik` -> `video_cache/ep/videosxp/menu.mp4`
- Perseus Mandate: `VideosXP2\\MenuXP2.bik` -> `video_cache/pm/videosxp2/menuxp2.mp4`

M29AN already exports EP's movie as `ux0:data/FEARVita/debug/Menu_ep.bik`. PM did not export because the old menu-movie detector only recognized names ending in `Menu.bik`; PM uses `MenuXP2.bik`.

M29AO fixes menu-movie classification to accept any `.bik` whose basename starts with `menu`. This makes PM's `MenuXP2.bik` a looping menu movie, exports it as `ux0:data/FEARVita/debug/Menu_pm.bik`, and keeps the existing campaign-isolated MP4 cache lookup. The cache-preparation tool/docs are also corrected to the actual EP/PM virtual paths.

Next hardware step: run M29AO once, collect `Menu_ep.bik` and `Menu_pm.bik`, convert those exact user-owned files to H.264 MP4, package them into the two expansion cache paths above, then verify both menu backgrounds visible/looping. That closes the three-game frontend/menu milestone.
