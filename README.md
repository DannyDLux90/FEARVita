# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AU**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The three-game frontend/menu-video milestone is complete on real PS Vita hardware. F.E.A.R., Extraction Point and Perseus Mandate reach their retail frontends and play the original animated menu backgrounds through campaign-isolated user-generated H.264/SceAvPlayer caches. Retail menu music and UI sounds remain on the game's own audio path. Vita system-language menu localization is restored.

M29AT established the first real single-player loading path and separate `fear_launcher.log`, `fear_fear.log`, `fear_ep.log` and `fear_pm.log` diagnostics. Hardware testing then showed all three campaigns select `Worlds\\Release\\Intro`, verify the world exists and reach `ScreenPreload` successfully.

M29AU fixes the reason that path stalled there. The Vita frontend had globally skipped `CScreenMgr::UpdateInterfaceSFX()` to protect the stable menu from incomplete ClientFX/model services. The retail preload/postload screens use that same callback to advance the mission state machine, not just to draw effects. M29AU therefore enables the original update path only for `SCREEN_ID_PRELOAD` and `SCREEN_ID_POSTLOAD`, while ordinary frontend screens retain the safe bypass.

The next ingame checkpoint is `FinishStartGame` -> local single-player StartGame -> loading handshake -> the real ObjectDLL/server/world-runtime frontier. Playable gameplay is not yet claimed.

The Weapons options screen priority editor remains available: X selects a weapon and Left/Right moves it in the retail priority list, using the existing profile-save path.

Start with `CURRENT_STATE.md`, `M29AU_PROGRESS_2026-09-11.md`, and `CURRENT_STATE_M29AU.txt`.

## Source layout

- `project/` — FEARVita compatibility/build sources represented by milestone source exports.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `patches/` — reproducible checkpoint patches.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). Public source/build artifacts do not ship converted retail game movies or private artwork.
