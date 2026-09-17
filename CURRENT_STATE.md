# FEARVita current state — M29DJ

**Date:** 2026-09-17  
**Runtime lineage:** 0.42-WIP / M29DH -> M29DJ  
**Integration PR:** #5 (`m29di-graphics-pool-fix`, legacy branch name)

## What is integrated

### Graphics pool

The M29DI graphics-pool correction has been integrated against the complete M29DH source. CPU-only projected vertices use reusable heap scratch instead of consuming a second copy in the per-frame vita2d pool. Before a draw, FEARVita budgets output vertices, worst-case alignment and the hidden 16-byte textured color uniform together, respecting libvita2d's strict end-of-pool rule.

The host allocator-contract test passes **403,264** accepted layouts. The modified Vita renderer translation unit compiles for ARM/Vita with the supplied toolchain.

### Timer semantics

The compatibility timer now samples the system clock once at the outer retail frame boundary. All timer getters during the same `PreUpdate -> Update -> PostUpdate` frame observe the same elapsed interval. Timer hierarchy, pause, scale and accumulated time remain in the compatibility backend. The old fixed `FrameSeconds() == 1/60` path now consumes the cached frame interval.

### Movie runtime

The Vita Bink/AvPlayer bridge now handles `eVTO_PlaySound`, requests AvPlayer audio PCM, transitions non-looping movies to the finished state at EOF, and resets playback state on restart. Frontend defaults are restored to `skiptitle=0` and `NoMovies=0` so the authored movie path can run.

Packaging now discovers campaign-relative `video_cache/**/*.mp4` recursively rather than hard-coding only the three menu movie files.

### Validation

The changed graphics, timer, ILTClient/runtime-gate and Bink/AvPlayer source units compile successfully for ARM/Vita with the supplied VitaSDK and pinned LithTech tree. `patches/M29DJ_RUNTIME_INTEGRATION.patch` passes `git apply --check` against a freshly extracted, unmodified M29DH workspace source tree. The M29DJ GitHub Actions integration check is passing.

## Known hardware/asset gate

The attached M29DH VPK contains only:

- `fear/videos/menu.mp4`
- `ep/videosxp/menu.mp4`
- `pm/videosxp2/menuxp2.mp4`

Those files are menu-video caches and do not contain audio streams. No intro/cinematic MP4 is present in that VPK, so intro video/audio/EOF cannot be claimed as hardware-validated from it.

A new VPK is intentionally not the current priority. The next meaningful runtime gate is the complete original Performance Test flow, including its result dialog and a second run, followed by the normal New Game/title-movie path once actual intro MP4 assets are available.

## Repository state

M29DJ is the active checkpoint. The current delta, tests, workflow and integration documentation are on GitHub. Superseded top-level `CURRENT_STATE_M29*`, progress and chat-handoff documents have been removed from the active tree; Git history and the old milestone branches preserve them.

See `SOURCE_STATE_M29DJ.json` for exact source/checkpoint identifiers and SHA-256 values.
