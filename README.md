# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AW**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The three-game frontend milestone is complete on real PS Vita hardware. F.E.A.R., Extraction Point and Perseus Mandate reach their retail frontends and play their original animated menu backgrounds with retail music and UI sounds.

M29AW standardizes the Vita gameplay control profile across all three campaigns. Restore Defaults reloads the same Killzone-inspired layout, including front touchscreen actions and rear-touch sprint. The built-in Vita Bubble manual now documents this map and the current per-campaign log locations.

The base-game loading path now reaches the local single-player handshake. The remaining blocker to entering the first mission is the real FEAR ObjectDLL/server/world runtime.

Steam currently marks German game-interface support for F.E.A.R. as unavailable. FEARVita can still follow the Vita system language for its own UI overlay. M29AW adds an original German fallback for the first base-game loading screen only; official German retail localization is not bundled or reconstructed.

Start with `CURRENT_STATE.md`, `M29AW_PROGRESS_2026-09-11.md`, and `CURRENT_STATE_M29AW.txt`.

## Source layout

- `project/` — FEARVita compatibility/build sources represented by milestone source exports.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `patches/` — reproducible checkpoint patches.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). Public source/build artifacts do not ship converted retail movies or private campaign artwork.
