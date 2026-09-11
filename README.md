# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AT**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The three-game frontend/menu-video milestone is complete on real PS Vita hardware. F.E.A.R., Extraction Point and Perseus Mandate reach their retail frontends and play the original animated menu backgrounds through campaign-isolated user-generated H.264/SceAvPlayer caches. Retail menu music and UI sounds remain on the game's own audio path. Vita system-language menu localization is restored.

M29AT starts the **ingame bring-up** milestone. Diagnostics are separated into `fear_launcher.log`, `fear_fear.log`, `fear_ep.log` and `fear_pm.log`. The Weapons options screen now supports priority reordering with X to select and Left/Right to move the selected weapon, using the existing retail profile-save path.

The menu-only ILTClient previously rejected `StartGame`, so New Game could never advance into a session. M29AT adds a deliberately constrained local `STARTGAME_NORMAL` bridge and traces first mission/world selection, preload and connection startup. The real FEAR ObjectDLL/server transport is not yet ported, so this is a bring-up checkpoint rather than a claim of playable gameplay.

Start with `CURRENT_STATE.md`, `M29AT_PROGRESS_2026-09-11.md`, and `CURRENT_STATE_M29AT.txt`.

## Source layout

- `project/` — FEARVita source, compatibility layer, public tools and Vita build files.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `patches/` — checkpoint patches.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). Public source/build artifacts do not ship converted retail game movies or private artwork.
