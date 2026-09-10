# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AG**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The retail F.E.A.R. front-end boots on real PS Vita hardware, renders, accepts controller input, and follows Vita system language. The current target is presentation parity with the original PC main menu.

The real `videos\\Menu.bik` has been validated as BIKi: 6,301,124 bytes, 512x512, 420 frames, 30 fps, 14 seconds, no embedded audio. The menu music is the separate retail `Music\\IntroIntLp1v2.wav`.

M29AF proved that a per-frame JPEG fallback is the wrong direction: the packaged JPEGs were detected but failed to decode on hardware, and the retries introduced menu stutter. M29AG returns to the scalable hardware-video path: one H.264 MP4 cache per Bink, using `SceAvPlayer` and a virtual-path-preserving cache layout. It also removes FEARVita-only audio attenuation so the retail volume controls determine the menu sound.

Start with `CURRENT_STATE.md` and `M29AG_PROGRESS_2026-09-10.md`.

## Source layout

- `project/` — FEARVita source, compatibility layer, tools, tests, and Vita build files.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `LITHTECH_OVERLAY_MANIFEST.txt` — overlay file manifest.

## User-owned video cache

For an exported directory that preserves F.E.A.R.'s virtual paths, build the MP4 cache with:

```bash
python3 project/tools/prepare_video_cache.py exported_binks video_cache
```

For example, `exported_binks/videos/Menu.bik` becomes `video_cache/videos/Menu.mp4`. Copy that cache below `ux0:data/FEARVita/video_cache/`. The current private hardware-test VPK packages only the user's converted menu movie; public builds do not.
