# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AV**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `.bik`, `.mp4`, archives, music, generated frames, campaign artwork, and other proprietary/retail-derived assets are intentionally excluded from this repository.

## Current status

The three-game frontend/menu-video milestone is complete on real PS Vita hardware. F.E.A.R., Extraction Point and Perseus Mandate reach their retail frontends and play the original animated menu backgrounds through campaign-isolated user-generated H.264/SceAvPlayer caches. Retail menu music and UI sounds remain on the game's own audio path, and Vita system-language menu localization is active.

M29AU hardware testing moved New Game into the real first-mission loading screen. `Worlds\\Release\\Intro` is selected and found, `FinishStartGame` runs, the constrained local `STARTGAME_NORMAL` bridge succeeds, and the client loading handshake completes. The remaining infinite load is the expected missing FEAR **ObjectDLL/server/world runtime**, not the old ScreenPreload state-machine issue.

M29AV adds a Killzone-inspired fixed Vita control preset with front and rear touch support. R fires, L aims, X jumps, Circle crouches, Square reloads, Triangle activates, D-pad maps SlowMo/grenade/weapon cycling, the front touchscreen provides flashlight/melee/next-weapon zones, and rear-touch double-tap + hold sprints. FEAR's loading/help and Configure Controls UI now shows these Vita labels instead of `key unassigned` for mapped actions.

Generic loading-screen framework strings now follow the Vita language overlay. M29AV also records the exact dynamic mission name/briefing/help StringDB ids under `loading-localize`, allowing remaining campaign-specific loading text to be localized without guessing.

The ObjectDLL compile bring-up has advanced past FEAR's extended property-macro mismatch. The next server work is the missing private Jupiter contracts and ILTServer methods required to create the actual world/server object runtime. Playable gameplay is not yet claimed.

Start with `CURRENT_STATE.md`, `M29AV_PROGRESS_2026-09-11.md`, and `CURRENT_STATE_M29AV.txt`.

## Source layout

- `project/` — FEARVita compatibility/build sources represented by milestone source exports.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `patches/` — reproducible checkpoint patches.

## User-owned video cache

Converted movies are namespaced by campaign (`fear`, `ep`, `pm`). Public source/build artifacts do not ship converted retail game movies or private artwork.
