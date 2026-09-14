# FEARVita next-chat handoff — M29CO / 0.37 — 2026-09-14

## Canonical workspace
- project: `/mnt/data/fear_work/m29ay_src/project`
- LithTech overlay: `/mnt/data/fear_work/m29ay_lithtech/lithtech-master`
- build: `/mnt/data/fear_work/m29ay_build`
- VitaSDK: `/mnt/data/vitasdk_m29bu`
- private packaging assets: `/mnt/data/fear_work/private_assets_m29cn`

## Hardware-proven baseline
M29CM / 0.35:
- fixes SFX list initialization;
- CharacterFX reaches `add-list-ok lookup=same`;
- Base F.E.A.R. and EP reach authentic `ChangeState(GS_PLAYING)`;
- Base retail loop continues beyond frame 3600 after X, so the observed freeze is visual;
- EP performance test still causes a GPU crash on hardware.

## M29CO / 0.37 changes
M29CN gameplay-present proof is retained:
- `RenderCamera` opens/clears a fresh gameplay frame instead of leaving the final loadscreen visible;
- stock HUD/interface rendering remains intact;
- `FlipScreen` presents normally;
- markers: `retail-camera`, `retail-present`, `input-heartbeat`.

M29CO additionally fixes the authentic performance-test manager on Vita:
- construct `CPerformanceTest` before the Vita frontend early return;
- log `perf-test` manager/start/result/world/set-level stages.

Patch: `M29CN_to_M29CO.patch`.

## Required hardware test matrix
### A. Base F.E.A.R. normal mission
This path may include intro/cinematic/postload transitions. Start a mission, allow the intro path to run, confirm postload with X, then observe the screen and controls.

Collect `fear_fear.log`.

Key ladder:
1. `0.37 / M29CO`
2. `sfx-mgr-ok`
3. `add-list-ok lookup=same`
4. `ChangeState(GS_PLAYING)`
5. `retail-camera`
6. `retail-present`
7. `input-heartbeat`

### B. Extraction Point Performance Test — mandatory direct-3D control
Run the EP Leistungstest from the performance menu. This path is used specifically to remove the normal mission intro as a confounder.

Collect `fear_ep.log`, `vitaGL.log` if generated, and a new `.psp2dmp` if the GPU crashes.

Key additional ladder:
1. `perf-test frontend-init manager=ready`
2. `perf-test start-request manager=ready`
3. `perf-test start result=1`
4. `perf-test start-level world=...`
5. `perf-test set-level ok`
6. then note the last `retail-camera` / `retail-present` marker before any GPU crash.

Interpretation:
- Base-only failure before camera/present => intro/screen-transition path.
- EP benchmark reaches camera but crashes before/around present => direct renderer/GPU frontier.
- both reach repeated camera/present heartbeats => proceed to real Jupiter world-scene submission.

## Packaging
Use the complete M29CO VPK. The private old-VPK media are local-only and must not be committed publicly.
