# FEARVita current state — M29CO / 0.37 — 2026-09-14

## Hardware facts from M29CM / 0.35

M29CM fixed the Vita SpecialFX-manager initialization bug. Hardware now reaches:
- `sfx-mgr-ok`;
- local-player `CharacterFX` registration with `add-list-ok lookup=same`;
- stock retail `ChangeState(GS_PLAYING)` in Base F.E.A.R. and Extraction Point.

Base F.E.A.R. continues advancing the retail loop for thousands of frames after the postload X confirmation. The apparent freeze is therefore visual, not the old local-client/CharacterFX handoff failure.

## Intro versus direct benchmark path

A normal mission can still cross intro/cinematic/postload logic before the first gameplay frame. That path remains a possible independent blocker.

Extraction Point's **Performance Test** is now treated as the mandatory direct-3D control path: it loads the configured performance-test world directly and is the best way to separate intro/screen-transition problems from renderer/GPU problems.

A second Vita early-return bug was found while auditing this path: the frontend returned before `m_pPerformanceTest = new CPerformanceTest`. The benchmark level could still load, but `StartPerformanceTest()` silently did nothing because the manager was null. M29CO moves construction of `CPerformanceTest` before the Vita frontend return.

## Rendering frontier

The Vita `ILTClient::RenderCamera` world-scene implementation is still not wired to Jupiter's client renderer. M29CN/M29CO therefore use a diagnostic **gameplay present proof**: a genuine retail camera call opens/clears a fresh frame, stock HUD/interface rendering continues, and `FlipScreen` presents it. This does not fabricate world geometry.

Expected runtime markers:
- `retail-camera`
- `retail-present`
- `input-heartbeat`

If these appear after `GS_PLAYING`, the simulation, camera call, presentation and controller path are alive; the next blocker is specifically world-scene submission.

## M29CO benchmark diagnostics

New markers:
- `perf-test frontend-init manager=ready`
- `perf-test start-request manager=ready`
- `perf-test start result=1 ...`
- `perf-test start-level world=<performance world>`
- `perf-test set-level ok`

This makes the EP benchmark a reliable direct-render control path.

## EP GPU crash

The supplied PSP2 dump is a valid ARM ELF core containing explicit `GPU_INFO` and `GPU_ACT_INFO` notes and the system event log reports `render gpu crash`. It does not by itself identify the exact user draw call. The M29CO benchmark + camera/present markers are intended to bracket the failing stage on the next hardware run.

## Packaging

M29CO / 0.37 is packaged with the complete private launcher/menu asset set from the user-provided older VPK. File-for-file, all 22 non-directory VPK entries are present, including:
- 3 `boot_art` graphics;
- 4 `launcher_art` graphics;
- 3 menu videos;
- LiveArea/manual assets.

Private binary/media assets remain local packaging inputs and are not committed to the public source branch.
