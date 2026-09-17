# FEARVita M29DH — current workspace/source handoff

Date: 2026-09-17
Purpose: full continuation snapshot before moving to a new ChatGPT conversation.

## Most important status

- Current source/build marker: `FEARVita 0.42-WIP / M29DH; raw menu keys + performance AI tracker guard + fade diagnostics`.
- M29DH VPK has been built successfully and packaged as a complete 22-file VPK, but **M29DH has NOT yet been hardware-tested** at the time of this snapshot.
- Last hardware-tested build: **M29DG**.
- M29DG user report: menu digital-button navigation regressed, Performance Test screen stayed visually black, then crashed.
- M29DG log proved that the benchmark Camera and CameraKeyFramer actually started and moved. Do **not** revert that conclusion or resume debugging from “camera never starts”.
- M29DG crash was symbolized to the server AI node-tracker / model animation transform path, not the world renderer and not the Camera/KeyFramer path.

## M29DG hardware evidence

Latest log in the downloadable workspace bundle: `hardware/latest_m29dg/fear_ep(20260917-154014).log`.
Latest core in the bundle: `hardware/latest_m29dg/psp2core-1789659741-0x0000742399-eboot.bin.psp2dmp`.

Confirmed from the log:

1. Performance Camera was forced ON:
   - `[perf-camera] server-initial forcing Camera ON for performance world`
   - `[perf-camera] server-turn-on`
2. A real camera keyframer exists:
   - `name=CameraKeyFramer object=Camera00;Pusher basekey=CKFKey keys=22 ... tracks-camera=1`
3. Client camera positions changed every frame, e.g. roughly:
   - frame 1: `3210.45,-96,1436.64`
   - frame 2: `3179.78,-96,1380.30`
   - frame 3: `3172.62,-96,1372.23`
   This proves the cinematic camera/keyframer motion path is alive in M29DG.
4. World renderer also submitted geometry while the screen was reported black:
   - frame 1: 31 chunks / 16906 tris
   - following frames around 13-14 chunks / ~9004 tris
   So “black screen” is not equivalent to “nothing is rendered”.
5. Retail postload reaches `GS_PLAYING`.
6. Renderer currently treats `Materials\\Invisible.Mat00` as diffuse `Tex\\flat_black_noAlpha.dds`; this is a concrete future graphics bug to investigate, but M29DH intentionally does not change it yet.

## M29DG crash root cause

The CPU core was symbolized against the matching Vita ELF. The fault path is in the server AI node-tracker/model animation transform chain, approximately:

`CAINodeTrackerContext::UpdateNodeTrackers`
→ `CServerNodeTrackerContext::UpdateNodeTrackers`
→ `CNodeTracker::Update`
→ `ILTModel::GetNodeTransform`
→ `ModelInstance::GetNodeTransform`
→ animation transform internals
→ `AnimNode::GetData`
→ Data Abort / invalid animation-channel data pointer.

This occurred after the benchmark cinematic started ATC/Soldier actions. It is not evidence of a GPU crash.

## What M29DH changes

M29DH is deliberately narrow. It does **not** add more renderer/camera experiments.

### 1. Menu digital-button ownership restored

File: `m29ay_lithtech/lithtech-master/FEAR/ClientShellDLL/GameClientShell.cpp`

- Frontend digital buttons use a raw edge path in `GS_SCREEN` / `GS_MENU`:
  - D-pad → arrow keys
  - Cross/Triangle → Return
  - Circle/Start → Escape
- The same held digital button is ignored by the CBindMgr command callback in frontend states so it cannot fire twice.
- Analog-stick menu navigation remains on the retail command path.
- Diagnostic marker: `[menu-input] raw=... key=... state=...`.

This is intended to restore the button navigation that worked before M29DG. It is **untested on hardware** in M29DH as of this snapshot.

### 2. Performance-only AI node-tracker crash guard

File: `m29ay_lithtech/lithtech-master/FEAR/ObjectDLL/AINodeTrackerContext.cpp`

- If `FearVita_RuntimeIsPerformanceWorld()` is true, `CAINodeTrackerContext::UpdateNodeTrackers` returns before the crashing node-transform path.
- This is intentionally scoped only to the authored Performance Test world.
- It does not globally weaken `ILTModel::GetNodeTransform` or all animations.
- Diagnostic marker: `[perf-node-tracker] skip ai=... active-flags=...`.

Expected trade-off: cinematic AI head/aim node tracking may be absent in Performance Test until the underlying Model00p animation compatibility is fixed.

### 3. Fade diagnostics only

File: `m29ay_lithtech/lithtech-master/FEAR/ClientShellDLL/InterfaceMgr.cpp`

- `UpdateScreenFade` logs performance-test fade state/alpha/time.
- No fade behavior is changed in M29DH.
- Diagnostic marker: `[perf-fade] active=... initialized=... fade-in=... alpha=... cur=... total=... state=...`.

This exists to determine whether the reported black screen is a normal/blocked fullscreen fade or a renderer/material issue.

## Do not lose these previously required fixes

Current worktree also contains earlier post-M29CU fixes, including:

- Performance Camera POD bridge and client cinematic application.
- CameraKeyFramer performance recovery used by M29DG.
- Flashlight guard so socket lookup only happens on real `OT_MODEL` objects.
- Long `GenericProp`/CommandObject property support used to avoid truncating benchmark scripts.
- Runtime legacy-object compatibility sentinels.
- `MID_END_GAME` whitelist work.
- Vita world renderer 120000 triangle budget and 256px normal world texture mip cap.
- vita2d 8 MiB transient pool work.

Do not assume GitHub `main` or `m29cu-menu-input-fix` already contains these later changes.

## First task in the next chat

1. Use the downloadable M29DH workspace bundle as the source of truth.
2. Test `FEARVita_0.42_M29DH.vpk` on real Vita.
3. Verify menu **buttons** before starting the benchmark.
4. Run Extraction Point → Performance Test.
5. Send the new `fear_ep*.log` and any new core dump.
6. Inspect first:
   - `[menu-input]`
   - `[perf-node-tracker]`
   - `[perf-fade]`
   - `[perf-camera]`
   - `[perf-keyframer]`
   - `[retail-camera]`
   - `[world-v113-cache]`
   - `MID_END_GAME` / message 184.
7. If M29DH survives >3 seconds but remains black:
   - use `[perf-fade]` to prove whether fade alpha/time is stuck;
   - only then investigate/render-skip `Materials\\Invisible.Mat00` and other opaque helper surfaces.
8. If it still crashes, symbolize the new core against the exact M29DH ELF in the downloadable bundle before changing code.

## Local Git state at snapshot

- Local branch: `master`
- Local base commit: `d049583 base_m29cu_reconstructed`
- The post-M29CU/M29D* work is intentionally still an uncommitted worktree in the local reconstruction.
