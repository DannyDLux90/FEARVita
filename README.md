# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AS**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The three-game frontend/menu-video milestone is complete on real PS Vita hardware. **F.E.A.R.**, **Extraction Point**, and **Perseus Mandate** all reach their retail frontends and play their original animated menu backgrounds through campaign-isolated user-generated H.264/SceAvPlayer caches. Retail menu music and normal UI sounds stay on the game's own audio path.

M29AR completed the current menu-link/touch pass: the reachable single-player/options screen graph is audited, Performance RecordLinks are bounds-checked, Advanced CPU/GPU layout state is separated, and the campaign selector uses the original retail select/selectchange sounds with proper touch highlight/activation behavior.

M29AS fixes a language regression introduced when packed SKDB values were decoded in M29AQ. The Vita system-language overlay once again has priority for ids it covers, while decoded retail StringDB values remain the fallback for every other id. This restores the previous behavior where the game-facing frontend follows the Vita system language.

The weapon milestone is now entering the actual client runtime. M29AS traces CClientWeaponMgr weapon-object creation and weapon-change dispatch so the next gameplay passes can follow WeaponDB -> CClientWeapon -> viewmodel -> animation -> ammo -> fire. Full gameplay weapon behavior is not yet claimed complete.

The PC Multiplayer entry belongs to a separate FEARMP executable/network browser stack and is tracked as a separate networking milestone rather than being hidden as a single-player menu-link fix.

Start with `CURRENT_STATE.md`, `M29AS_PROGRESS_2026-09-11.md` and `M29AR_MENU_AUDIT.txt`.

## Source layout

The exact full checkpoint source is distributed as the source-export ZIP for each milestone. This repository tracks progress/state documents, reproducible patches and public helper tools. Proprietary game assets are never committed.

- `project/tools/` — public user-side conversion/cache helpers.
- `patches/` — checkpoint patches against the documented source baseline.
- `CURRENT_STATE.md` — latest checkpoint/status.
- `M29AS_PROGRESS_2026-09-11.md` — current milestone details.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). User-owned exported Bink movies can be converted to SceAvPlayer-compatible MP4 files while preserving their retail virtual paths. Public source/build artifacts do not ship converted game movies.
