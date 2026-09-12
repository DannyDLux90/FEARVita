# M29BL WIP recovery

Base branch/checkpoint: `m29bk-navmesh-abi` / M29BK 0.08.

Current branch: `m29bl-wip-local-client-handoff`.

This branch preserves the **unbuilt/unverified M29BL WIP source delta** for the authentic local client/player handoff. It intentionally does not contain a VPK, EBOOT, retail game data, proprietary campaign assets, local logs, or build artifacts.

## Reconstructing the workspace delta

From an M29BK workspace:

```sh
cd m29ay_src
patch -p2 < ../recovery/M29BL_WIP_FROM_M29BK_PROJECT.patch

cd ../m29ay_lithtech
patch -p2 < ../recovery/M29BL_WIP_FROM_M29BK_SERVER.patch
```

The patch paths are based on the exported workspace names `m29bk_ws/...` and `m29bl_ws/...`; `-p2` removes the snapshot/workspace prefixes and targets `project/...` and `lithtech-master/...` respectively.

## Integrity

- `M29BL_WIP_FROM_M29BK_PROJECT.patch` SHA-256: `7417601320726d5cf4a4514854e0075a6db0fd7ae9d1018e3e926f0e7fb6f2f9`
- `M29BL_WIP_FROM_M29BK_SERVER.patch` SHA-256: `068eee9d21b80414ec2080f47db71b6d69b5cec71c49a762cbc86ffc5c1fda5f`
- `M29BL_NEW_CHAT_HANDOFF_2026-09-12.md` SHA-256: `1a7f039588f7ef9e573934cdab3acfc7ed51b6d4b5ff2226e59a3fdc85e6f6aa`

Local exported snapshots from the same source state (not committed to this public repository):

- Full source ZIP SHA-256: `797269839f4fb625890051bc326936151afcc70cdb3830c2924e95a47c389e8a`
- Full workspace ZIP SHA-256: `06c2328967f641e9a2505291e11467e6d998f3ed7752bceaef56f78ccaf81f61`

## Hardware baseline inherited from M29BK

M29BK is hardware-verified to complete the real Intro world load to 100%, consume the full bounded NavMesh payload, finish `DoRunWorld`, and return `do-start-world ok` / `FinishStartGame result=1` without a crash. The retail loop then remains alive on the completed loading screen.

M29BL WIP addresses only the next frontier: creating and driving the authentic local LithTech server client/player handoff so the stock FEAR client connection state machine can leave the loading screen. It does not force `GS_PLAYING`.

## Build status

M29BL WIP carries package marker `00.09` in source but has not yet produced a verified M29BL binary. The last verified installable binary remains M29BK / 0.08. A rebuild attempt stopped during CMake toolchain setup because the temporary VitaSDK path was absent; no M29BL source compile/link failure was established.
