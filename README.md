# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AY**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

M29AY is the active source/build checkpoint. M29AX remains the last hardware-proven VPK. M29AY is bringing the shared FEAR/EP/PM ObjectDLL/server/world runtime online and is not yet hardware validated.

The three-game frontend milestone is complete on real PS Vita hardware. F.E.A.R., Extraction Point and Perseus Mandate reach their retail frontends and play their original animated menu backgrounds with retail music and UI sounds.

M29AW standardized the Vita gameplay control profile across all three campaigns. M29AX keeps that gameplay layout intact and adds native retail-menu navigation: the physical D-pad follows UI directions, while the front touchscreen acts as an absolute pointer/tap source through the original LithTech menu hit-testing path. The built-in Vita Bubble manual documents both the gameplay map and menu controls.

All three campaigns now reach the same accepted local `StartGame` frontier. M29AY is bringing up one shared retail ObjectDLL/server/world runtime for F.E.A.R., Extraction Point and Perseus Mandate, using the published F.E.A.R. SDK 1.08 to restore interfaces missing from the older public LithTech snapshot. The complete retail ObjectDLL now compiles **533/533 for ARM/Vita**, including `PlayerObj.cpp` and `GameServerShell.cpp`. There is not yet an M29AY hardware VPK; the active work is the full ClientShell/executable build followed by real server/world link bring-up.

For German Vita system language, M29AY extends the FEARVita-authored first-intro/loading fallback to all three campaign tags (`fear`, `ep`, `pm`) with campaign-specific briefing text. These fallback strings are project-authored and are not presented as official retail German localization.

Start with `NEXT_CHAT_M29AY.md`, `CURRENT_STATE.md`, `CURRENT_STATE_M29AY.txt`, and `M29AY_PROGRESS_2026-09-11.md`. The canonical reproducible M29AY delta is documented under `patches/`.

## Source layout

- `project/` — FEARVita compatibility/build sources represented by milestone source exports.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `patches/` — reproducible checkpoint patches.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). Public source/build artifacts do not ship converted retail movies or private campaign artwork.

## Screenshots
<img width="960" height="544" alt="grafik" src="https://github.com/user-attachments/assets/97160c2d-c08e-447f-a9ef-03dfba91868d" />
