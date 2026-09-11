# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AQ**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The three-game frontend/menu milestone is complete on real PS Vita hardware. **F.E.A.R.**, **Extraction Point**, and **Perseus Mandate** all reach their retail frontends and can play their original animated menu backgrounds through campaign-isolated user-generated H.264/SceAvPlayer caches. Retail menu music and normal UI sounds stay on the game's own audio path.

M29AQ begins the next milestone: bring all menu and submenu entries to full retail correctness, starting with the Performance/`Leistung` pages and the Weapons options screen. The Vita StringEdit bridge now attempts to decode the packed retail SKDB v2 id/value/TOC tables so the real localized `.Strdb00p` strings can replace the previous small built-in language safety net.

M29AQ also adds screen transition/build diagnostics, Performance command diagnostics, and a weapon-menu audit that records the retail default-priority weapon records together with their StringDB ids and silhouette icons. This establishes the menu/database/client-weapon linkage before deeper in-game weapon work.

Start with `CURRENT_STATE.md` and `M29AQ_PROGRESS_2026-09-11.md`.

## Source layout

The exact full checkpoint source is distributed as the source-export ZIP for each milestone. This repository tracks progress/state documents, reproducible patches and public helper tools. Proprietary game assets are never committed.

- `project/tools/` — public user-side conversion/cache helpers.
- `patches/` — checkpoint patches against the documented source baseline.
- `CURRENT_STATE.md` — latest checkpoint/status.
- `M29AQ_PROGRESS_2026-09-11.md` — current milestone details.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). User-owned exported Bink movies can be converted to SceAvPlayer-compatible MP4 files while preserving their retail virtual paths. Public source/build artifacts do not ship converted game movies.
