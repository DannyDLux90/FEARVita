# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AR**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The three-game frontend/menu-video milestone is complete on real PS Vita hardware. **F.E.A.R.**, **Extraction Point**, and **Perseus Mandate** all reach their retail frontends and play their original animated menu backgrounds through campaign-isolated user-generated H.264/SceAvPlayer caches. Retail menu music and normal UI sounds stay on the game's own audio path.

M29AR continues the menu-completeness/weapon milestone. The complete reachable single-player/options screen graph has been audited. Main/Single/Profile, Load/Save, Display, Audio, Game/Crosshair, Performance/Advanced CPU/Advanced GPU, Controls/Configure/Mouse/Joystick and Weapons all have registered screen targets. Performance option RecordLink bounds are corrected, and the dormant Keyboard target aliases to Configure controls instead of dead-ending if a data variant exposes it.

The campaign selector now has proper touch selection: first tap selects/highlights a campaign and keeps its border visible, while a second tap starts it. D-pad/touch selection uses the original retail `interface\Snd\selectchange.wav`; activation uses `interface\Snd\select.wav`. These sounds are read from the user's base F.E.A.R. VFS rather than bundled replacements.

M29AQ's packed SKDB v2 StringDB decoder, screen diagnostics and weapon-menu audit remain active as the foundation for the next weapon work. Full gameplay weapon behavior is not yet claimed complete.

The PC Multiplayer entry belongs to a separate FEARMP executable/network browser stack and is tracked as a separate networking milestone rather than being hidden as a single-player menu-link fix.

Start with `CURRENT_STATE.md`, `M29AR_PROGRESS_2026-09-11.md` and `M29AR_MENU_AUDIT.txt`.

## Source layout

The exact full checkpoint source is distributed as the source-export ZIP for each milestone. This repository tracks progress/state documents, reproducible patches and public helper tools. Proprietary game assets are never committed.

- `project/tools/` — public user-side conversion/cache helpers.
- `patches/` — checkpoint patches against the documented source baseline.
- `CURRENT_STATE.md` — latest checkpoint/status.
- `M29AR_PROGRESS_2026-09-11.md` — current milestone details.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). User-owned exported Bink movies can be converted to SceAvPlayer-compatible MP4 files while preserving their retail virtual paths. Public source/build artifacts do not ship converted game movies.
