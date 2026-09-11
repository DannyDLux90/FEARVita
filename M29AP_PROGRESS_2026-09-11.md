# M29AP / 0.02 — three retail menu-video caches

M29AP is the private milestone-candidate package for matching the three retail frontends on Vita.

The exact user-exported expansion menu Binks are now converted to H.264 Constrained Baseline level 3.1, yuv420p while preserving their source geometry, frame count and timing:

- F.E.A.R.: `Videos\\Menu.bik` -> `video_cache/fear/videos/menu.mp4`
- Extraction Point: `VideosXP\\Menu.bik` -> `video_cache/ep/videosxp/menu.mp4` — 512x512, 420 frames, 30 fps, 14.000 s
- Perseus Mandate: `VideosXP2\\MenuXP2.bik` -> `video_cache/pm/videosxp2/menuxp2.mp4` — 640x480, 466 frames, 29.97 fps, 15.548882 s

The two expansion Binks contain no embedded audio. Their retail ScreenMedia entries request `Music\\IntroIntLp1v2.wav` separately, so FEARVita continues to use the original retail WAV at the requested gain through the Vita 48 kHz HQ resampler. Normal retail UI `select.wav` / `selectchange.wav` sounds remain active.

Private/user-owned Binks, MP4 cache files, music and artwork are not committed to the public repository.

Hardware acceptance target for both EP and PM: AvPlayer `add-source result=0`, `first-frame`, visible looping animated menu background, and unchanged retail menu music/UI sounds. Passing both closes the three-game frontend/menu milestone.
