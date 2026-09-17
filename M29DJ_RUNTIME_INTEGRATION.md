# M29DJ runtime integration — 2026-09-17

Base: complete M29DH workspace from `FEARVita_M29DH_CURRENT_WORKSPACE_SOURCE_2026-09-17.zip`.
Target branch: `m29di-graphics-pool-fix` / PR #5.

## What is integrated

### Graphics pool crash

- Integrates the PR #5 allocator correction into the complete M29DH source.
- CPU-only projected vertices use reusable heap scratch instead of the 8 MiB vita2d transient pool.
- Every draw preflights the complete output-vertex budget, alignment slop and the hidden 16-byte textured-draw RGBA uniform.
- Overflow at the Vita allocator's unsigned-int boundary is rejected.
- Renderer shutdown releases the retained scratch allocation.

Host allocator-contract test result:

`PASS: 403264 accepted draw layouts satisfy the libvita2d contract`

The modified `vita_gxm_frame_backend.cpp` also compiles successfully with the supplied VitaSDK/libvita2d toolchain.

### Timer semantics

- Adds an explicit timer frame boundary before the retail `PreUpdate -> Update -> PostUpdate` sequence.
- The system clock is sampled once per engine frame.
- Repeated elapsed/accumulated-time getters in the same frame observe the same cached interval.
- Child timers continue to derive elapsed time from their parent accumulation and retain pause/time-scale/update-range behavior.
- The old compatibility `FrameSeconds() == 1/60` path now reads the cached engine-frame interval instead.

The modified timer implementation, ILTClient compatibility layer and retail runtime gate all compile successfully for ARM/Vita.

### MP4 cinematic playback, audio and transitions

- Keeps the existing campaign-aware virtual `.bik` -> `app0:video_cache/<campaign>/<relative>.mp4` mapping.
- Adds AvPlayer PCM audio delivery for videos opened with `eVTO_PlaySound`.
- Detects AvPlayer end-of-stream for non-looping/non-menu movies and marks the video texture finished, allowing the stock splash/intro transition logic to advance.
- Restart clears EOF/activity state.
- Restores stock frontend defaults (`SkipTitle=0`, `NoMovies=0`) instead of forcing movies off.
- VPK packaging now recursively includes every converted `video_cache/**/*.mp4`, with private assets overriding matching source-tree assets. It is no longer restricted to the three menu MP4 names.

The modified Bink/AvPlayer backend compiles successfully for ARM/Vita.

## Package inspection

The attached `FEARVita_0.42_M29DH.vpk` is readable and ZIP-valid. It contains exactly three MP4 files:

- `video_cache/fear/videos/menu.mp4`
- `video_cache/ep/videosxp/menu.mp4`
- `video_cache/pm/videosxp2/menuxp2.mp4`

All three are H.264 Constrained Baseline / yuv420p and contain video only; none has an audio stream. No intro/cinematic MP4 is present in the supplied VPK. Therefore intro playback cannot be hardware-validated from this package even though the runtime and packaging paths are now prepared for campaign-relative intro MP4s.

The existing converter already produces H.264/AAC MP4s and recursively discovers Bink inputs, so the remaining asset requirement is to provide/cache the actual converted intro BIKs under their original campaign-relative paths.

## Build validation

Workspace ZIP and VPK both passed archive integrity checks. Approximately 29 GiB remains free on `/mnt/data`; the prior storage-exhaustion condition is not present.

A complete VitaSDK + pinned LithTech tree was reconstructed from the supplied packages and the workspace overlay. The following changed Vita objects compile successfully:

- `project/src/vita_gxm_frame_backend.cpp`
- `project/integration/lithtech/fearvita_ilttimer_vita.cpp`
- `project/integration/lithtech/fearvita_menu_runtime_gate.cpp`
- `project/integration/lithtech/fearvita_iltclient_vita.cpp`
- `project/integration/lithtech/fearvita_bink_vita.cpp`

A clean full link/VPK requires rebuilding roughly 1,041 legacy translation units because the workspace archive does not contain the prior object files. The clean build was started and did not expose an error in the changed code, but it has not reached the final ELF/VPK link in this environment. No new VPK or hardware result is claimed yet.

## Required Vita hardware gate

1. Extraction Point -> Options -> Performance -> Performance Test.
2. Let the full authored benchmark camera/keyframer sequence complete and reach the stock result dialog.
3. Repeat the benchmark once without restarting the application; check for pool errors, memory growth, missing geometry and a new core dump.
4. Start a normal new game with title movies enabled.
5. Verify each intro MP4: first frame, audio, A/V pacing, EOF transition, skip input and return to the next stock screen/world.
6. Confirm the normal `Intro.World00p` -> player-control path after the movie sequence.

The existing performance-only AI node-tracker compatibility guard remains separate and should only be removed after the benchmark completes with the underlying AI compatibility path enabled.
