# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AJ**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The base F.E.A.R. retail front-end boots on real PS Vita hardware, renders, accepts controller input, follows Vita system language, and now plays the real menu animation through a Menu.bik-derived H.264 cache using SceAvPlayer. The movie is presented over the full 960x544 Vita framebuffer. The retail menu music is decoded from `Music\\IntroIntLp1v2.wav` and mixed through the Vita 48 kHz HQ path at the game-requested gain.

M29AI replaces the old diagnostic-heavy loading screen with a minimal campaign-specific presentation: optional background art plus progress bar and percentage. Public source does not ship proprietary campaign artwork; private/user builds can provide `project/boot_art/fear.png`, `ep.png`, and `pm.png`.

M29AJ focuses on Extraction Point and Perseus Mandate. Both supplied expansion logs reached PlayerMgr MoveMgr and then failed before WeaponMgr completion. Their main packed GADB tables are substantially decoded but stop late on an unsupported record-name construct. M29AJ allows valid RecordLinks into already-decoded categories and adds a Vita frontend-only WeaponMgr fallback so a gameplay subsystem cannot abort an otherwise usable menu frontend.

Start with `CURRENT_STATE.md` and `M29AJ_PROGRESS_2026-09-10.md`.

## Source layout

- `project/` — FEARVita source, compatibility layer, tools, tests, and Vita build files.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `patches/` — checkpoint patches.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). The cache generator accepts user-owned exported Bink movies and produces SceAvPlayer-compatible MP4 files while preserving virtual paths. Public builds do not ship converted game movies.
