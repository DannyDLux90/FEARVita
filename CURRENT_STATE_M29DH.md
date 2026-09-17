# FEARVita M29DH snapshot — 2026-09-17

This branch is a safety/handoff checkpoint created from the current local FEARVita workspace after M29DG hardware testing and before moving to a new conversation.

## Build state

- Marker: `FEARVita 0.42-WIP / M29DH; raw menu keys + performance AI tracker guard + fade diagnostics`
- M29DH builds successfully into the complete private 22-file test VPK.
- M29DH has **not yet been hardware-tested** at snapshot time.
- Last hardware-tested build: M29DG.

## M29DG findings carried into M29DH

- Performance Camera is ON and CameraKeyFramer moves the cinematic camera; this is confirmed by the hardware log.
- The reported black screen is therefore not explained by a stationary camera or absent world submission.
- M29DG crash symbols point to the server AI node-tracker/model animation transform path (`CAINodeTrackerContext` → `CNodeTracker` → `ILTModel::GetNodeTransform` → animation node data), after cinematic ATC/Soldier activity begins.
- Menu digital-button handling regressed in M29DG.

## M29DH changes

1. Restores a raw frontend digital-button edge path in `GameClientShell.cpp`, with CBindMgr duplicate ownership suppressed for those same physical buttons in `GS_SCREEN`/`GS_MENU`.
2. Adds a Performance-Test-only early return in `CAINodeTrackerContext::UpdateNodeTrackers` to avoid the symbolized crash while preserving the rest of AI/animation behavior.
3. Adds `[perf-fade]` diagnostics to `InterfaceMgr::UpdateScreenFade` without changing fade behavior.

See `NEXT_CHAT_HANDOFF_M29DH.md` for full continuation details and `patches/M29DH_CURRENT_WORKTREE.patch` for the exact tracked worktree delta.

The full local workspace/source ZIP is intentionally distributed separately from GitHub; this branch stores the reproducible source delta and handoff metadata rather than duplicating the full public LithTech upstream.
