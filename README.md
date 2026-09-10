# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AH**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The retail F.E.A.R. front-end boots on real PS Vita hardware, renders, accepts controller input, and follows Vita system language. M29AG proved real SceAvPlayer playback of the user-derived menu MP4 on hardware. M29AH stretches that movie to the full 960x544 framebuffer and namespaces converted movie caches by campaign (`fear`, `ep`, `pm`).

The real base-game `videos\\Menu.bik` is BIKi: 6,301,124 bytes, 512x512, 420 frames, 30 fps, 14 seconds, with no embedded audio. The menu music is the separate retail `Music\\IntroIntLp1v2.wav` and is mixed at the retail-requested gain through the Vita 48 kHz HQ path.

The abandoned per-frame JPEG fallback has been removed. Expansion movie caches cannot accidentally reuse the base-game movie when virtual paths are identical.

Extraction Point and Perseus Mandate still need current hardware boot logs. Their known older blockers occurred before ScreenMovie playback, so missing converted video is not assumed to be the reason they fail to enter the menu.

Start with `CURRENT_STATE.md` and `M29AH_PROGRESS_2026-09-10.md`.

## Source layout

- `project/` — FEARVita source, compatibility layer, tools, tests, and Vita build files.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `LITHTECH_OVERLAY_MANIFEST.txt` — overlay file manifest.
- `patches/` — checkpoint diffs, including the current M29AH delta.

## User-owned video cache

Campaign-aware cache paths are:

- base F.E.A.R.: `ux0:data/FEARVita/video_cache/fear/...`
- Extraction Point: `ux0:data/FEARVita/video_cache/ep/...`
- Perseus Mandate: `ux0:data/FEARVita/video_cache/pm/...`

For a prepared campaign-organized directory of user-owned Bink movies, run:

```bash
python3 project/tools/prepare_video_cache.py binks video_cache
```

The batch converter keeps source geometry, encodes H.264 baseline/yuv420p, and converts an optional first embedded audio track to AAC stereo/48 kHz for future cinematics. Public builds never ship converted game movies.
