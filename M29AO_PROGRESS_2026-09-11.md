# M29AO / 0.02 — EP/PM menu-video cache capture

## Confirmed M29AN milestone progress
Hardware logs now show both Extraction Point and Perseus Mandate reaching the retail frontend successfully (`frontend-main-ok`, `complete`, engine init result 0).

The remaining visible difference is the animated retail menu background:

- F.E.A.R.: `Videos\\Menu.bik` -> packaged H.264 cache already working.
- Extraction Point: `VideosXP\\Menu.bik`, 512x512, 420 frames, 30 fps. The Bink already exports as `ux0:data/FEARVita/debug/Menu_ep.bik`.
- Perseus Mandate: `VideosXP2\\MenuXP2.bik`, 640x480, 466 frames, 29.97 fps. M29AN did not export this file because menu detection only recognized names ending in `Menu.bik`.

## M29AO changes
- Menu-Bink detection is now basename based: any `.bik` whose basename begins with `menu` is treated as a looping frontend menu movie.
- This recognizes PM's `MenuXP2.bik` correctly and exports it as `ux0:data/FEARVita/debug/Menu_pm.bik`.
- PM menu playback is now marked looping once its MP4 cache is present.
- The generic video-cache preparation documentation/tool was corrected to the actual expansion paths:
  - `ep/videosxp/menu.mp4`
  - `pm/videosxp2/menuxp2.mp4`
- Existing campaign-isolated cache lookup remains unchanged, so F.E.A.R., EP and PM cannot accidentally use each other's menu movie.

## Next / final step for this milestone
Run M29AO once in EP and PM and copy the exported retail Binks:
- `ux0:data/FEARVita/debug/Menu_ep.bik`
- `ux0:data/FEARVita/debug/Menu_pm.bik`

Convert those exact user-owned Binks to H.264 MP4 and package them at:
- `app0:video_cache/ep/videosxp/menu.mp4`
- `app0:video_cache/pm/videosxp2/menuxp2.mp4`

Once hardware confirms both expansion menu videos are visible/looping, the three-game frontend/menu milestone is complete.
