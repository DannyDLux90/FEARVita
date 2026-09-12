# M29BG progress — 2026-09-12

## M29BF hardware result

M29BF/0.03 was positively identified by its startup banner. The log confirms synchronous Vita MAIN 48 kHz stereo initialization and independent SFX/music/voice levels. It also confirms that the direct loading callback is bound. The real local server reaches `Intro.World00p`; instead of the former data-abort crash, world startup now returns `LT_INVALIDWORLDFILE` (42).

## Confirmed World00p parser mismatch

The Vita `ILTStream` adapter's `ReadString` implementation was incompatible with LithTech. It scanned for a NUL byte. The reference `CGenLTStream::ReadString` reads a little-endian `uint16` length followed by exactly that many bytes, with no terminator stored in the stream. `WorldBsp::Load` uses this API immediately for its world-model name, so the Vita adapter shifted the packed world stream and made subsequent fields invalid. M29BG changes the adapter to match `CGenLTStream` semantics exactly.

This is a functional parser fix, not a diagnostic workaround.

## Real loading progress and visible bar

The synchronous loading bridge remains in place. `CWorldSharedBSP::Load` now emits real milestones after the packed header, world metadata, world tree and each world model. These callbacks redraw `CLoadingScreen` synchronously while the blocking server load is in progress.

The Vita fallback bar no longer relies on a generic F4 conversion or database-derived position. It uses the direct GT4 DrawPrim path used successfully by the retail frontend, with a fixed screen-relative track and fill. The track is visible at 0%, while the fill remains driven exclusively by real load progress.

## Audio path

The 48 kHz stereo hardware initialization and retail SFX/music/voice main-level separation from M29BF are retained. For 44.1 kHz assets, M29BG replaces the decode-time short sinc loop with an exact rational 160/147 polyphase converter using precomputed 160-phase, 16-tap Blackman-windowed FIR coefficients. This both improves reconstruction quality and removes trigonometric work from the per-sample loop.

For the menu reference track, the exact post-resample PCM is exported once as `ux0:data/FEARVita/debug/IntroIntLp1v2_48k.wav` and logged with FNV-1a, peak and RMS. If the Vita still sounds different from the PC recording, this file lets the next analysis distinguish digital backend output from speaker/recording coloration without another speculative build.

## Build/package validation

- ARM/Vita build and link: success
- Runtime checkpoint: M29BG
- App version: 00.04
- Full payload: 22 files
- VPK SHA-256: `a33ec3f11a7455024c3ee5242930dcb6d7d3534bf28933b4e4b0ff123d66cb33`
- EBOOT SHA-256: `0928929712abba23bb666aecad5c0ee8a3499e22be7f7134213b9723693b3eeb`

## Next hardware run

One base-game run only: F.E.A.R. -> New Game -> Medium. The useful outcomes are (1) visible/moving loading bar, (2) whether `Intro` enters, and (3) whether the menu audio character changes. On failure, collect `fear_fear.log`; only collect a coredump if a real crash occurs. Keep `debug/IntroIntLp1v2_48k.wav` if the sound mismatch remains.
