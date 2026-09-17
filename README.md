# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

**Current internal checkpoint: M29DJ**  
**Current integration PR: #5**  
**Date: 2026-09-17**

The original retail game data is **not** included. Users must provide their own legally obtained F.E.A.R. data. Retail archives, movies, music and other proprietary assets are intentionally excluded from the repository.

## Current development state

M29DJ is based on the complete M29DH workspace snapshot and consolidates the current runtime work in `patches/M29DJ_RUNTIME_INTEGRATION.patch`.

The current work includes:

- the vita2d transient-pool crash fix and reusable CPU projection scratch;
- one cached timer sample per engine frame and removal of the fixed `1/60` frame-time compatibility path;
- Vita AvPlayer movie audio delivery, non-looping EOF/finished handling and restart-state reset;
- normal movie defaults (`skiptitle=0`, `NoMovies=0`);
- recursive packaging of campaign-relative `video_cache/**/*.mp4` files.

The graphics allocation host test passes 403,264 accepted layouts. The changed graphics, timer, client/runtime-gate and Bink/AvPlayer translation units compile for ARM/Vita with the supplied VitaSDK and pinned LithTech source.

The supplied M29DH test VPK contains only the three menu MP4 caches and no intro/cinematic MP4 files, so the normal intro sequence still requires a hardware test with the actual intro assets. Building another VPK is not the current repository milestone.

## Source of truth

For active development, start with:

1. `CURRENT_STATE.md`
2. `M29DJ_RUNTIME_INTEGRATION.md`
3. `SOURCE_STATE_M29DJ.json`
4. `patches/M29DJ_RUNTIME_INTEGRATION.patch`
5. `UPSTREAM_PIN.txt`

The repository is deliberately a checkpoint/delta repository rather than a duplicate of the public LithTech upstream. The pinned upstream commit is recorded in `UPSTREAM_PIN.txt`. The M29DH source checkpoint is retained in Git history/its snapshot branch; M29DJ contains the complete current delta on top of that checkpoint. No M29DJ source modification is intended to exist only in the local workspace.

Historical `CURRENT_STATE_M29*`, progress and handoff files were removed from the active M29DJ tree because they described superseded milestones. Their commits and historical branches remain available in Git.

## Current target

The next hardware gate is the stock Extraction Point Performance Test through the normal result dialog, followed by a second run without restarting. After that, test the normal New Game/title-movie flow with the actual intro MP4 assets, including audio, EOF/skip transition and `Intro.World00p` to player control.
