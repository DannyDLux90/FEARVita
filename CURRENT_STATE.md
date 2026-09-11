# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AP  
**Date:** 2026-09-11

The launcher/loading flow and the F.E.A.R. base-game menu are accepted on hardware and remain unchanged. M29AN cleared the remaining frontend blocker for both expansions: Extraction Point and Perseus Mandate reach `frontend-main-ok`, `complete`, engine init result 0 and enter their retail menus.

M29AP is the three-game frontend/menu milestone candidate. The exact user-exported expansion menu Binks have been converted to Vita-compatible H.264 caches and packaged only in the private hardware-test VPK:
- F.E.A.R.: `Videos\\Menu.bik` -> `video_cache/fear/videos/menu.mp4`
- Extraction Point: `VideosXP\\Menu.bik` -> `video_cache/ep/videosxp/menu.mp4` (512x512, 420 frames, 30 fps, 14.000 s)
- Perseus Mandate: `VideosXP2\\MenuXP2.bik` -> `video_cache/pm/videosxp2/menuxp2.mp4` (640x480, 466 frames, 29.97 fps, 15.548882 s)

Both expansion Binks are silent. Their retail ScreenMedia definitions request `Music\\IntroIntLp1v2.wav`, so FEARVita keeps the original separate menu WAV and normal retail UI select/selectchange sounds. No synthetic menu audio is added. The menu videos are rendered to the complete 960x544 Vita framebuffer, matching the already accepted base-game Vita presentation.

No retail Binks, converted MP4s, menu music or private artwork are committed to this public repository.

Next hardware priority: verify EP and PM each report AvPlayer `add-source result=0` plus `first-frame`, visibly animate/loop behind the retail menus, and retain the correct retail music/UI sounds. If both pass, the three-game frontend/menu milestone is complete.
